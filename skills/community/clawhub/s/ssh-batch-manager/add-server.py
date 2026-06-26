#!/usr/bin/env python3
"""
Add Server - Secure server addition script
Uses JSON input to avoid any shell escaping issues
"""

import sys
import json
from pathlib import Path

# Import encryption functions from main script
CREDENTIALS_DIR = Path.home() / ".openclaw" / "credentials"
CONFIG_FILE = CREDENTIALS_DIR / "ssh-batch.json"
KEY_FILE = CREDENTIALS_DIR / "ssh-batch.key"

def load_key():
    """Load encryption key."""
    with open(KEY_FILE, 'rb') as f:
        return f.read().strip()

def encrypt_data(data: str, key: bytes) -> str:
    """Encrypt data with AES-256."""
    from cryptography.fernet import Fernet
    import base64
    
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return f"AES256:{base64.b64encode(encrypted).decode()}"

def add_server(server_data: dict) -> bool:
    """Add server to configuration securely."""
    # Load existing config
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    # Prepare server entry
    server_entry = {
        'user': server_data['user'],
        'host': server_data['host'],
        'port': server_data['port'],
        'auth': server_data['auth']
    }
    
    # Encrypt password if provided
    if server_data.get('password'):
        key = load_key()
        server_entry['password'] = encrypt_data(server_data['password'], key)
    
    # Add to config
    config['servers'].append(server_entry)
    
    # Save config
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Set secure permissions
    CONFIG_FILE.chmod(0o600)
    
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: add-server.py <json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    try:
        # Read server data from JSON file (no shell escaping needed)
        with open(json_file, 'r') as f:
            server_data = json.load(f)
        
        # Add server securely
        if add_server(server_data):
            print(f"✅ Added server: {server_data['user']}@{server_data['host']}:{server_data['port']}")
        else:
            print("❌ Failed to add server")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
