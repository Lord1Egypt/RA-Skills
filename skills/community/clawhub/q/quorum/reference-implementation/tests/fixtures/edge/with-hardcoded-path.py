"""File with hardcoded paths for testing PS-001."""

import os

DATA_DIR = "/Users/john/projects/data"
CONFIG_PATH = "/etc/myapp/config.yaml"
TEMP_DIR = "/tmp/myapp/cache"
WINDOWS_PATH = r"C:\Users\john\Documents\project"

def load_data():
    return open(DATA_DIR + "/input.csv").read()
