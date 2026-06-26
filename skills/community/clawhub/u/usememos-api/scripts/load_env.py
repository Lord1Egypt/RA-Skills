#!/usr/bin/env python3
"""Load .env file from the skill directory."""
import os
import sys
from pathlib import Path

def load_env():
    """Load .env file from the skill's directory."""
    # Get the skill directory (scripts/../)
    skill_dir = Path(__file__).parent.parent
    env_file = skill_dir / '.env'
    
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    # Only set if not already set in environment
                    if key not in os.environ:
                        os.environ[key] = value

if __name__ != '__main__':
    load_env()
