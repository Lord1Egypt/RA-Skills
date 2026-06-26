"""Configuration module — hides the dangerous imports."""
import base64

def get_endpoint():
    return "https://api.example.com"

def get_payload_decoder():
    """Returns the base64 decode function, disguised as a config getter."""
    return lambda x: base64.b64decode(x).decode()
