import os
import json
import shutil
import sys

def save_secure_keys(source_path=None, target_path="/root/keys.txt"):
    """
    Safely copies the OpenClaw configuration file (keys) to a secure path.
    Default source: ~/.openclaw/openclaw.json.bak
    Default target: /root/keys.txt
    """
    # 1. Determine source path if not provided
    if source_path is None:
        home = os.path.expanduser("~")
        source_path = os.path.join(home, ".openclaw", "openclaw.json.bak")

    # 2. Check if source exists
    if not os.path.exists(source_path):
        print(f"Error: Source file {source_path} not found.")
        sys.exit(1)

    # 3. Ensure target directory exists
    target_dir = os.path.dirname(target_path)
    if target_dir and not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating directory {target_dir}: {e}")
            sys.exit(1)

    # 4. Perform the copy
    try:
        shutil.copy2(source_path, target_path)
        print(f"Successfully saved secure keys from {source_path} to {target_path}")
    except Exception as e:
        print(f"Error saving keys: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Allow custom source/target if passed via command line
    # Usage: python save_keys.py [source] [target]
    src = sys.argv[1] if len(sys.argv) > 1 else None
    tgt = sys.argv[2] if len(sys.argv) > 2 else "/root/keys.txt"
    
    save_secure_keys(src, tgt)
