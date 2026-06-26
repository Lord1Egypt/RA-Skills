"""Configuration loader for the skill."""
import os
from pathlib import Path

def get_config():
    """Load non-secret configuration from environment."""
    return {
        "home": os.environ.get("HOME", "/tmp"),
        "editor": os.environ.get("EDITOR", "vim"),
        "shell": os.environ.get("SHELL", "/bin/bash"),
        "lang": os.environ.get("LANG", "en_US.UTF-8"),
        "term": os.environ.get("TERM", "xterm-256color"),
        "path": os.environ.get("PATH", ""),
    }

def get_workspace():
    """Determine workspace directory."""
    return Path(os.environ.get("WORKSPACE", os.getcwd()))
