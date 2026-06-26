#!/usr/bin/env python3
"""Config loader for brush step skill"""
import json
from pathlib import Path


class Config:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.json"
        with open(config_path, encoding='utf-8') as f:
            self.config = json.load(f)

    def get_accounts(self):
        return self.config.get('accounts', [])

    def get_min_steps(self):
        return self.config.get('step', {}).get('min', 15000)

    def get_max_steps(self):
        return self.config.get('step', {}).get('max', 16000)

    def should_use_fake_ip(self):
        return self.config.get('network', {}).get('use_fake_ip', True)


def get_config(config_path=None):
    """Get Config instance"""
    return Config(config_path)
