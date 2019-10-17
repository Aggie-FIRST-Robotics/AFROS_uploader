from typing import Union
from functools import lru_cache
from serial.tools import list_ports as list_ports
from afros_uploader.util import *

def bytes_to_str(arr):
    if isinstance(arr, str):
        arr = bytes(arr)
    if hasattr(arr, '__iter__'):
        return ''.join('{:02X} '.format(x) for x in arr).strip()
    else:  # actually just a single byte
        return '0x{:02X}'.format(arr)


def decode_bytes_to_str(data: Union[bytes, bytearray], encoding: str = 'utf-8', errors: str = 'strict') -> str:
    return data.split(b'\0', 1)[0].decode(encoding=encoding, errors=errors)

@lru_cache()
def list_all_comports():
    ports = list_ports.comports()
    logger(__name__).debug('Connected: {}'.format(';'.join([str(p.__dict__) for p in ports])))
    return ports
