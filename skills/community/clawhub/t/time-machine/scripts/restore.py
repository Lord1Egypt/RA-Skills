#!/usr/bin/env python3
"""
Way Back - Restore Snapshot
Usage: python restore.py [version] [--file filename] [--only config|memory|openclaw.json]

Options:
  --file filename    Restore only specific file
  --only target      Restore only: config, memory, or specific file
"""
import os
import sys
import json
import shutil
from pathlib import Path

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

def get_current_openclaw_version():
    """Get current OpenClaw version"""
    config_file = os.path.join(CONFIG_DIR, "openclaw.json")
    if os.path.exists(config_file):
        try:
            with open(config_file) as f:
                data = json.load(f)
                return data.get("meta", {}).get("lastTouchedVersion", "unknown")
        except:
            pass
    return "unknown"

def find_snapshot(version):
    """Find snapshot by version number"""
    for suffix in ["inc", "full"]:
        path = os.path.join(SNAPSHOT_DIR, f"v{version}_{suffix}")
        if os.path.exists(path):
            return path, suffix
    return None, None

def get_base_version(snapshot_path):
    """Get base version for incremental snapshot"""
    meta_file = os.path.join(snapshot_path, "meta.json")
    if os.path.exists(meta_file):
        with open(meta_file) as f:
            meta = json.load(f)
            return meta.get("base_version", meta.get("version"))
    return 1

def check_version_compatibility(snapshot_path):
    """Check if snapshot version matches current OpenClaw version"""
    meta_file = os.path.join(snapshot_path, "meta.json")
    if os.path.exists(meta_file):
        with open(meta_file) as f:
            meta = json.load(f)
            snapshot_version = meta.get("openclaw_version", "unknown")
            current_version = get_current_openclaw_version()
            if snapshot_version != current_version:
                print(f"⚠️ Version mismatch!")
                print(f"   Snapshot: OpenClaw {snapshot_version}")
                print(f"   Current: OpenClaw {current_version}")
                return False
    return True

def restore_full(snapshot_path, target_file=None, restore_memory=False):
    """Restore from full snapshot"""
    for item in os.listdir(snapshot_path):
        if item == "meta.json":
            continue
        if target_file and item != target_file:
            continue
        if item == "workspace":
            if restore_memory:
                # Restore workspace files
                workspace_src = os.path.join(snapshot_path, "workspace")
                exclude_dirs = {'.git', '__pycache__', '.openclaw', '.pi', 'node_modules'}
                for ws_item in os.listdir(workspace_src):
                    src = os.path.join(workspace_src, ws_item)
                    dest = os.path.join(WORKSPACE_DIR, ws_item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dest)
            continue
        # Handle legacy memory folder
        if item == "memory" and restore_memory:
            memory_dir = os.path.join(snapshot_path, "memory")
            if os.path.exists(memory_dir):
                for mem_file in os.listdir(memory_dir):
                    src = os.path.join(memory_dir, mem_file)
                    dest = os.path.join(WORKSPACE_DIR, mem_file)
                    if os.path.isdir(src):
                        shutil.copytree(src, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dest)
            continue
        src = os.path.join(snapshot_path, item)
        dest = os.path.join(CONFIG_DIR, item)
        if os.path.isdir(src):
            shutil.copytree(src, dest, dirs_exist_ok=True)
        elif os.path.isfile(src):
            shutil.copy2(src, dest)

def restore_incremental(version, target_file=None, only_type=None):
    """Restore from incremental snapshot"""
    snapshot_path, _ = find_snapshot(version)
    if not snapshot_path:
        print(f"❌ Snapshot v{version} not found")
        return False
    
    base_version = get_base_version(snapshot_path)
    base_path = os.path.join(SNAPSHOT_DIR, f"v{base_version}_full")
    
    # Restore based on only_type
    restore_memory = only_type in [None, "memory"]
    restore_config = only_type in [None, "config"]
    
    # Restore base first
    if os.path.exists(base_path) and restore_config:
        restore_full(base_path, target_file, restore_memory=restore_memory)
    
    # Apply patches
    patches_dir = os.path.join(snapshot_path, "patches")
    if os.path.exists(patches_dir):
        for patch_file in os.listdir(patches_dir):
            if target_file and patch_file != target_file:
                continue
            
            # Skip based on only_type
            if patch_file.startswith("workspace_"):
                if not restore_memory:
                    continue
            elif patch_file.startswith("memory_"):
                if not restore_memory:
                    continue
            elif not restore_config:
                continue
            
            src = os.path.join(patches_dir, patch_file)
            # Handle workspace files
            if patch_file.startswith("workspace_"):
                filename = patch_file.replace("workspace_", "")
                dest = os.path.join(WORKSPACE_DIR, filename)
            # Handle legacy memory files
            elif patch_file.startswith("memory_"):
                filename = patch_file.replace("memory_", "")
                dest = os.path.join(WORKSPACE_DIR, filename)
            else:
                dest = os.path.join(CONFIG_DIR, patch_file)
            if os.path.isdir(src):
                shutil.copytree(src, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dest)
    
    return True

def restore(version="", single_file=None, only_type=None):
    """Main restore function"""
    # Find version to restore
    index_file = os.path.join(SNAPSHOT_DIR, "index.json")
    if not version:
        if os.path.exists(index_file):
            with open(index_file) as f:
                data = json.load(f)
                current = data.get("latest", 0)
                if current > 1:
                    version = str(current - 1)
                else:
                    print("❌ No previous snapshot to rollback to")
                    return False
        else:
            print("❌ No snapshots found")
            return False
    
    # Find snapshot
    snapshot_path, snapshot_type = find_snapshot(version)
    if not snapshot_path:
        print(f"❌ Snapshot v{version} not found")
        return False
    
    # Check version compatibility
    compatible = check_version_compatibility(snapshot_path)
    if not compatible:
        confirm = input("⚠️ Continue anyway? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ Cancelled")
            return False
    
    print(f"⚠️ About to rollback to v{version}_{snapshot_type}")
    
    if only_type:
        print(f"📄 Will restore only: {only_type}")
    elif single_file:
        print(f"📄 Will restore single file: {single_file}")
    else:
        print("📄 Will restore all files (including memory)")
    
    confirm = input("❓ Confirm? (yes/no): ")
    if confirm.lower() != "yes":
        print("❌ Cancelled")
        return False
    
    # Perform restore
    if snapshot_type == "full":
        restore_full(snapshot_path, single_file, restore_memory=(only_type in [None, "memory"]))
    else:
        restore_incremental(version, single_file, only_type)
    
    if only_type:
        print(f"✅ Restored {only_type} from v{version}")
    elif single_file:
        print(f"✅ Restored {single_file} from v{version}")
    else:
        print(f"✅ Rolled back to v{version}_{snapshot_type}")
        print("📦 Memory files restored to workspace")
    
    # Auto-create rollback point
    print("📦 Creating rollback point snapshot...")
    import snapshot as snap_module
    snap_module.create_snapshot(force_full=True)
    
    print("✅ Done")
    return True

if __name__ == "__main__":
    version = ""
    single_file = None
    only_type = None
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--file":
            if i + 1 < len(args):
                single_file = args[i + 1]
                i += 2
            else:
                i += 1
        elif args[i] == "--only":
            if i + 1 < len(args):
                only_type = args[i + 1]
                if only_type not in ["config", "memory", "openclaw.json"]:
                    print("❌ --only must be: config, memory, or a filename")
                    sys.exit(1)
                i += 2
            else:
                i += 1
        else:
            version = args[i]
            i += 1
    
    restore(version, single_file, only_type)
