#!/usr/bin/env python3
"""
Way Back - Create Snapshot
Usage: python snapshot.py [--full]
"""
import os
import sys
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime

OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
SNAPSHOT_DIR = os.path.join(OPENCLAW_DIR, "snapshots")
CONFIG_DIR = OPENCLAW_DIR

# Detect workspace directory
WORKSPACE_DIR = os.path.join(OPENCLAW_DIR, "workspace-product")
if not os.path.exists(WORKSPACE_DIR):
    for path in ["/root/.openclaw/workspace-product", os.path.expanduser("~/openclaw/workspace-product")]:
        if os.path.exists(path):
            WORKSPACE_DIR = path
            break

# Config files to backup (in ~/.openclaw/)
TARGETS = [
    "openclaw.json",
    "config.yaml",
    "agents",
    "channels",
    "skills",
    "credentials",
    ".env"
]

# Workspace files (the entire workspace directory)
# These will be backed up to the memory folder in snapshot

def get_openclaw_version():
    """Get OpenClaw version from openclaw.json"""
    config_file = os.path.join(CONFIG_DIR, "openclaw.json")
    if os.path.exists(config_file):
        try:
            with open(config_file) as f:
                data = json.load(f)
                return data.get("meta", {}).get("lastTouchedVersion", "unknown")
        except:
            pass
    return "unknown"

def get_file_hash(path):
    """Get MD5 hash of a file or directory"""
    if os.path.isfile(path):
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    elif os.path.isdir(path):
        hashes = []
        for root, dirs, files in os.walk(path):
            for f in sorted(files):
                fp = os.path.join(root, f)
                with open(fp, 'rb') as fh:
                    hashes.append(hashlib.md5(fh.read()).hexdigest())
        return hashlib.md5(''.join(hashes).encode()).hexdigest() if hashes else ""
    return ""

def find_last_full():
    """Find the last full snapshot version"""
    if not os.path.exists(SNAPSHOT_DIR):
        return 0
    version = 1
    while os.path.exists(os.path.join(SNAPSHOT_DIR, f"v{version}_full")):
        version += 1
    return version - 1

def get_current_version():
    """Get current latest version"""
    index_file = os.path.join(SNAPSHOT_DIR, "index.json")
    if os.path.exists(index_file):
        with open(index_file) as f:
            data = json.load(f)
            return data.get("latest", 0)
    return 0

def has_changes(last_full_version):
    """Check if there are changes since last full snapshot"""
    if last_full_version == 0:
        return True
    
    base_path = os.path.join(SNAPSHOT_DIR, f"v{last_full_version}_full")
    if not os.path.exists(base_path):
        return True
    
    # Check config files
    for target in TARGETS:
        target_path = os.path.join(CONFIG_DIR, target)
        if os.path.exists(target_path):
            current_hash = get_file_hash(target_path)
            last_hash_path = os.path.join(base_path, f"{target}.md5")
            last_hash = ""
            if os.path.exists(last_hash_path):
                with open(last_hash_path) as f:
                    last_hash = f.read().strip()
            if current_hash != last_hash:
                return True
    
    # Check memory files
    if os.path.exists(WORKSPACE_DIR):
        for target in MEMORY_TARGETS:
            target_path = os.path.join(WORKSPACE_DIR, target)
            if os.path.exists(target_path):
                current_hash = get_file_hash(target_path)
                last_hash_path = os.path.join(base_path, f"memory_{target}.md5")
                last_hash = ""
                if os.path.exists(last_hash_path):
                    with open(last_hash_path) as f:
                        last_hash = f.read().strip()
                if current_hash != last_hash:
                    return True
    
    return False

def copy_target(src_path, dest_path, save_hash=True):
    """Copy file or directory, optionally save hash"""
    if os.path.exists(src_path):
        # Create parent directory if needed
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, dest_path)
        if save_hash:
            with open(f"{dest_path}.md5", 'w') as f:
                f.write(get_file_hash(src_path))

def create_snapshot(force_full=False):
    """Create a new snapshot"""
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    
    current_version = get_current_version()
    next_version = current_version + 1
    last_full = find_last_full()
    
    # Determine snapshot type
    if force_full or current_version == 0 or not has_changes(last_full):
        snapshot_type = "full"
    else:
        snapshot_type = "inc"
    
    snapshot_name = f"v{next_version}_{snapshot_type}"
    snapshot_path = os.path.join(SNAPSHOT_DIR, snapshot_name)
    
    print(f"📦 Creating snapshot {snapshot_name}...")
    
    if snapshot_type == "full":
        os.makedirs(snapshot_path, exist_ok=True)
        
        # Backup config files
        for target in TARGETS:
            target_path = os.path.join(CONFIG_DIR, target)
            dest = os.path.join(snapshot_path, target)
            copy_target(target_path, dest)
        
        # Backup entire workspace
        if os.path.exists(WORKSPACE_DIR):
            workspace_dest = os.path.join(snapshot_path, "workspace")
            # Copy workspace excluding .git, __pycache__, etc
            exclude_dirs = {'.git', '__pycache__', '.openclaw', '.pi', 'node_modules', 'skills'}
            for item in os.listdir(WORKSPACE_DIR):
                if item in exclude_dirs:
                    continue
                src = os.path.join(WORKSPACE_DIR, item)
                dest = os.path.join(workspace_dest, item)
                copy_target(src, dest)
        
        all_files = [t for t in TARGETS if os.path.exists(os.path.join(CONFIG_DIR, t))]
        if os.path.exists(WORKSPACE_DIR):
            all_files.append("workspace/*")
        
        meta = {
            "version": next_version,
            "type": "full",
            "timestamp": datetime.now().isoformat(),
            "openclaw_version": get_openclaw_version(),
            "files": all_files
        }
    else:
        # Incremental - store changed files
        patches_dir = os.path.join(snapshot_path, "patches")
        os.makedirs(patches_dir, exist_ok=True)
        
        base_path = os.path.join(SNAPSHOT_DIR, f"v{last_full}_full")
        patch_count = 0
        
        # Check config files
        for target in TARGETS:
            target_path = os.path.join(CONFIG_DIR, target)
            if os.path.exists(target_path):
                dest = os.path.join(patches_dir, target)
                copy_target(target_path, dest, save_hash=False)
                patch_count += 1
        
        # Check workspace files
        if os.path.exists(WORKSPACE_DIR):
            workspace_base = os.path.join(base_path, "workspace")
            exclude_dirs = {'.git', '__pycache__', '.openclaw', '.pi', 'node_modules', 'skills'}
            for item in os.listdir(WORKSPACE_DIR):
                if item in exclude_dirs:
                    continue
                src = os.path.join(WORKSPACE_DIR, item)
                dest = os.path.join(patches_dir, f"workspace_{item}")
                copy_target(src, dest, save_hash=False)
                patch_count += 1
        
        meta = {
            "version": next_version,
            "type": "incremental",
            "base_version": last_full,
            "timestamp": datetime.now().isoformat(),
            "openclaw_version": get_openclaw_version(),
            "patch_count": patch_count
        }
    
    # Save metadata
    with open(os.path.join(snapshot_path, "meta.json"), 'w') as f:
        json.dump(meta, f, indent=2)
    
    # Update index
    index = {
        "latest": next_version,
        "type": snapshot_type,
        "last_full": last_full
    }
    with open(os.path.join(SNAPSHOT_DIR, "index.json"), 'w') as f:
        json.dump(index, f)
    
    print(f"✅ Created snapshot {snapshot_name}")
    print(f"📝 Based on v{last_full}_full")
    if snapshot_type == "inc":
        print(f"📁 Incremental: {patch_count} patches")

if __name__ == "__main__":
    force_full = "--full" in sys.argv
    create_snapshot(force_full)
