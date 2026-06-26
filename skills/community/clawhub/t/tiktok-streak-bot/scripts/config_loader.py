import json
import os
import logging

class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = {}

    def load(self):
        if os.path.exists(self.config_path):
            logging.info(f"Loading configuration from {self.config_path}...")
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return self.config
        else:
            logging.error(f"Configuration file not found at {self.config_path}.")
            return None

    def get(self, key, default=None):
        return self.config.get(key, default)
