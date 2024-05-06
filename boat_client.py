#!/usr/bin/env python3
"""Test client for communication protocol."""

import logging
import sys
import time

import serial
# https://www.datadoghq.com/blog/engineering/protobuf-parsing-in-python/
from google.protobuf.internal.decoder import _DecodeVarint
from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.message import Message, DecodeError

from comm_proto import connection_pb2, data_pb2, latlng_pb2, timestamp_pb2

PacketType = connection_pb2.Packet.PacketType
nav_data = []


def send_data(port: serial.Serial, packet_type: PacketType, message: Message):
    """Sends a packet to the port."""
    packet = connection_pb2.Packet(
        version="0.1.0", type=packet_type, data=message.SerializeToString()
    )
    try:
        port.write(_VarintBytes(packet.ByteSize()) + packet.SerializeToString())
    except OSError:
        logging.info("Disconnected to the port")
        sys.exit(0)


def handle_data(port: serial.Serial, data: bytes):
    """Handles incoming data."""
    try:
        packet = connection_pb2.Packet()
        packet.ParseFromString(data)
        logging.info("Received %s", packet)
    except DecodeError:
        logging.error("Received an Invalid Packet")
        return

    main_packet = packet.data
    if packet.type == PacketType.CONNECT:
        try:
            connection_pb2.Connect().ParseFromString(main_packet)
            logging.info("Recevied connection request, replying...")
            send_data(
                port, PacketType.CONNECT, connection_pb2.Connect(version="0.1.0")
            )
        except DecodeError:
            logging.error("Expected a Connect message but received and invalid one")
            return
    elif packet.type == PacketType.RECEIVED:
        try:
            connection_pb2.Received().ParseFromString(main_packet)
        except DecodeError:
            logging.error(
                "Expected a Received message but received and invalid one"
            )
            return
    elif packet.type == PacketType.PATH_DATA:
        try:
            path_data = data_pb2.PathData()
            path_data.ParseFromString(main_packet)
            logging.debug("PathData: %s", path_data)
            send_data(
                port, PacketType.RECEIVED, connection_pb2.Received(version="0.1.0")
            )
            logging.info("Received a new path! Sending to path planner.")
            points = [[point.latitude, point.longitude] for point in path_data.points]
            global nav_data
            # nav_data = nav.nav(points)
        except DecodeError:
            logging.error(
                "Expected a PathData message but received and invalid one"
            )
            return
    else:
        logging.error("Received Unexpected Packet Type: %s", packet.type)
        return

    return packet.type


def send_boat_data(port: serial.Serial):
    """Sends a fake data to the desktop."""
    features = []
    for i, data in enumerate(nav_data):
        time_stamp = timestamp_pb2.Timestamp(seconds=int(data[3]))
        point = latlng_pb2.LatLng(
            latitude=data[4],
            longitude=data[5],
        )
        layer = data[2]
        if layer == 1:
            layer_name = data_pb2.BoatData.Layer.SURFACE
        elif layer == 2:
            layer_name = data_pb2.BoatData.Layer.MIDDLE
        elif layer == 3:
            layer_name = data_pb2.BoatData.Layer.SEA_BED
        else:
            layer_name = data_pb2.BoatData.Layer.SEA_BED
            
        feature = data_pb2.BoatData.BoatDataFeature(
            temperature=data[0],
            depth=data[1],
            layer=layer_name,
            time=time_stamp,
            geometry=point,
        )
        features.append(feature)

    data = data_pb2.BoatData(version="0.1.0", features=features)
    logging.debug("Sent Data: %s", data)
    send_data(port, PacketType.BOAT_DATA, data)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    if len(sys.argv) < 2:
        print("Please provide a port to listen to", file=sys.stderr)
        sys.exit(1)

    port = sys.argv[1]
    logging.info("Connecting to %s", port)
    port = serial.Serial(port, timeout=100)
    logging.info("Connected to %s", port)

    next_send = time.time() + 10
    BUF = b""
    STATE = 0
    while True:
        if time.time() > next_send:
            logging.info("Sending Boat Data to Port")
            send_boat_data(port)
            next_send = time.time() + 10

        # TODO: Send data from the controller to the desktop
        try:
            BUF += port.read_all()
        except OSError:
            logging.info("Disconnected to the port")
            break

        if STATE == 0:
            try:
                length, pos = _DecodeVarint(BUF, 0)
                BUF = BUF[pos:]
                STATE = 1
                continue
            except IndexError:
                continue

        if len(BUF) >= length and STATE == 1:
            STATE = 0
            logging.info("Received Data")
            logging.debug("Data %s", BUF[:length])
            handle_data(port, BUF[:length])
            BUF = BUF[length:]

        if BUF is None:
            print("Unable to read port", file=sys.stderr)
            sys.exit(1)
