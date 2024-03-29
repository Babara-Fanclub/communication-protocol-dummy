import latlng_pb2 as _latlng_pb2
import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoatData(_message.Message):
    __slots__ = ("version", "features")
    class Layer(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SURFACE: _ClassVar[BoatData.Layer]
        MIDDLE: _ClassVar[BoatData.Layer]
        SEA_BED: _ClassVar[BoatData.Layer]
    SURFACE: BoatData.Layer
    MIDDLE: BoatData.Layer
    SEA_BED: BoatData.Layer
    class BoatDataFeature(_message.Message):
        __slots__ = ("temperature", "depth", "layer", "time", "geometry")
        TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
        DEPTH_FIELD_NUMBER: _ClassVar[int]
        LAYER_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        GEOMETRY_FIELD_NUMBER: _ClassVar[int]
        temperature: float
        depth: float
        layer: BoatData.Layer
        time: _timestamp_pb2.Timestamp
        geometry: _latlng_pb2.LatLng
        def __init__(self, temperature: _Optional[float] = ..., depth: _Optional[float] = ..., layer: _Optional[_Union[BoatData.Layer, str]] = ..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., geometry: _Optional[_Union[_latlng_pb2.LatLng, _Mapping]] = ...) -> None: ...
    VERSION_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    version: str
    features: _containers.RepeatedCompositeFieldContainer[BoatData.BoatDataFeature]
    def __init__(self, version: _Optional[str] = ..., features: _Optional[_Iterable[_Union[BoatData.BoatDataFeature, _Mapping]]] = ...) -> None: ...

class PathData(_message.Message):
    __slots__ = ("version", "points")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    version: str
    points: _containers.RepeatedCompositeFieldContainer[_latlng_pb2.LatLng]
    def __init__(self, version: _Optional[str] = ..., points: _Optional[_Iterable[_Union[_latlng_pb2.LatLng, _Mapping]]] = ...) -> None: ...
