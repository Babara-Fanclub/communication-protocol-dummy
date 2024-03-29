from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Connect(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: str
    def __init__(self, version: _Optional[str] = ...) -> None: ...

class Received(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: str
    def __init__(self, version: _Optional[str] = ...) -> None: ...

class Packet(_message.Message):
    __slots__ = ("version", "type", "data")
    class PacketType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNDEFINED: _ClassVar[Packet.PacketType]
        CONNECT: _ClassVar[Packet.PacketType]
        RECEIVED: _ClassVar[Packet.PacketType]
        BOAT_DATA: _ClassVar[Packet.PacketType]
        PATH_DATA: _ClassVar[Packet.PacketType]
    UNDEFINED: Packet.PacketType
    CONNECT: Packet.PacketType
    RECEIVED: Packet.PacketType
    BOAT_DATA: Packet.PacketType
    PATH_DATA: Packet.PacketType
    VERSION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    version: str
    type: Packet.PacketType
    data: bytes
    def __init__(self, version: _Optional[str] = ..., type: _Optional[_Union[Packet.PacketType, str]] = ..., data: _Optional[bytes] = ...) -> None: ...
