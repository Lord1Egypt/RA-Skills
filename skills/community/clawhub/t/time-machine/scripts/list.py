#!/usr/bin/env python3
"""
Way Back - List Snapshots
Usage: python list.py
"""
import os
import json
from pathlib import Path

OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
SNAPSHOT_DIR = os.path.join(OPENCLAW_DIR, "snapshots")

def list_snapshots():
    """List all snapshots"""
    if not os.path.exists(SNAPSHOT_DIR):
        print("📭 No snapshots found")
        return
    
    snapshots = []
    for item in os.listdir(SNAPSHOT_DIR):
        if item.startswith("v") and ("_full" in item or "_inc" in item):
            path = os.path.join(SNAPSHOT_DIR, item)
            if os.path.isdir(path):
                snapshots.append(item)
    
    if not snapshots:
        print("📭 No snapshots found")
        return
    
    # Sort by version
    snapshots.sort(key=lambda x: int(x.split("_")[0].replace("v", "")))
    
    print("📋 Snapshots:")
    print("")
    
    for snap in snapshots:
        version = snap.split("_")[0]
        vtype = snap.split("_")[1]
        
        meta_file = os.path.join(SNAPSHOT_DIR, snap, "meta.json")
        if os.path.exists(meta_file):
            with open(meta_file) as f:
                meta = json.load(f)
                timestamp = meta.get("timestamp", "")
                if "T" in timestamp:
                    timestamp = timestamp.replace("T", " ").split("+")[0]
                
                if vtype == "full":
                    files = meta.get("files", [])
                    has_memory = any("memory" in f for f in files)
                    mem_str = " 📚" if has_memory else ""
                    print(f"  {snap:12} | {vtype:4} | {timestamp:19} | {len(files)} files{mem_str}")
                else:
                    patch_count = meta.get("patch_count", 0)
                    base = meta.get("base_version", "")
                    print(f"  {snap:12} | {vtype:4} | {timestamp:19} | base v{base}, {patch_count} patches")
        else:
            print(f"  {snap:12} | {vtype:4}")
    
    print("")
    print(f"Total: {len(snapshots)} snapshots")
    print("📚 = includes memory files")

if __name__ == "__main__":
    list_snapshots()
