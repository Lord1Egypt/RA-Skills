"""A safe helper module"""
import json
from pathlib import Path

def read_config(path):
    with open(path) as f:
        return json.load(f)

def format_output(data):
    return json.dumps(data, indent=2)
