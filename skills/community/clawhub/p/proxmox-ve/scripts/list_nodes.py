#!/usr/bin/env python3
from pve_api import build_client
import json

client = build_client()
json.dump(client.get('/nodes'), fp=__import__('sys').stdout, indent=2)
print()
