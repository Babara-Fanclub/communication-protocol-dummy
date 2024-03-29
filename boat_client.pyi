import serial

from connection_pb2 import Packet

def handle_data(port: serial.Serial, data: bytes) -> None | Packet.PacketType:
    """Handles incoming data."""
    ...