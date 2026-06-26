#!/usr/bin/env python3
"""
Tool for reading local pet profiles.
Used as an auxiliary script for the OpenClaw skill 'zuozuo' to retrieve saved user pet information.
Adheres to the "Local Data Only" privacy principle.
"""
import os
import json
import argparse

# Default profile storage at user's ~/.openclaw/profiles directory
PROFILE_DIR = os.path.expanduser("~/.openclaw/profiles")
PROFILE_PATH = os.path.join(PROFILE_DIR, "zuozuo_pet_profile.json")

def read_profile():
    if not os.path.exists(PROFILE_PATH):
        return {"status": "not_found", "message": "Local pet profile not found. Please guide the user to provide information to establish a profile."}
    
    try:
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": f"Failed to read profile: {str(e)}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read local profile for zuozuo pet assistant")
    args = parser.parse_args()
    
    result = read_profile()
    # Print JSON for OpenClaw agent to capture
    print(json.dumps(result, ensure_ascii=False, indent=2))
