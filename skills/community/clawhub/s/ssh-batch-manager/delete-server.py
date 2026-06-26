#!/usr/bin/env python3
"""
Delete Server - Secure server deletion script
Uses index parameter to avoid any shell escaping issues
"""

import sys
import json
from pathlib import Path

CREDENTIALS_DIR = Path.home() / ".openclaw" / "credentials"
CONFIG_FILE = CREDENTIALS_DIR / "ssh-batch.json"

def delete_server(index: int) -> bool:
    """Delete server from configuration securely."""
    # Load existing config
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    # Check index
    if index < 0 or index >= len(config['servers']):
        print(f"❌ Invalid index: {index}")
        return False
    
    # Remove server
    removed = config['servers'].pop(index)
    
    # Save config
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Set secure permissions
    CONFIG_FILE.chmod(0o600)
    
    print(f"✅ Deleted server: {removed['user']}@{removed['host']}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: delete-server.py <index>")
        sys.exit(1)
    
    try:
        index = int(sys.argv[1])
        
        if delete_server(index):
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
