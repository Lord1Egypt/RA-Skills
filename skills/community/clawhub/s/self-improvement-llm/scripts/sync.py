#!/usr/bin/env python3
"""Export and import self-improvement data for backup or multi-server sync."""

import json
import os
import sys
import zipfile
from datetime import datetime

WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE_DIR, "memory")
SKILL_DIR = os.path.join(WORKSPACE_DIR, "skills", "self-improvement")

# Files to export
EXPORT_FILES = [
    "memory/MEMORY.md",
    "memory/.learning-trail.json",
    "memory/.memory-index.json",
    "memory/preferences.json",
    "memory/heartbeat-state.json",
]

# Directories to export
EXPORT_DIRS = [
    "memory/sessions",
    "memory/skills",
    "memory/.dreams",
]

def export_data(output_path=None):
    """Export all self-improvement data to a zip file."""
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(WORKSPACE_DIR, f"self-improvement-backup-{timestamp}.zip")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Export individual files
        for file_path in EXPORT_FILES:
            full_path = os.path.join(WORKSPACE_DIR, file_path)
            if os.path.exists(full_path):
                zf.write(full_path, file_path)
                print(f"  Added: {file_path}")
        
        # Export directories
        for dir_path in EXPORT_DIRS:
            full_dir = os.path.join(WORKSPACE_DIR, dir_path)
            if os.path.exists(full_dir):
                for root, dirs, files in os.walk(full_dir):
                    for file in files:
                        file_full = os.path.join(root, file)
                        file_rel = os.path.relpath(file_full, WORKSPACE_DIR)
                        zf.write(file_full, file_rel)
                        print(f"  Added: {file_rel}")
        
        # Export daily logs (last 30 days)
        memory_dir = os.path.join(WORKSPACE_DIR, "memory")
        if os.path.exists(memory_dir):
            for file in os.listdir(memory_dir):
                if file.endswith(".md") and len(file) == 13:  # YYYY-MM-DD.md
                    file_full = os.path.join(memory_dir, file)
                    file_rel = f"memory/{file}"
                    zf.write(file_full, file_rel)
                    print(f"  Added: {file_rel}")
    
    print(f"\n✅ Export complete: {output_path}")
    print(f"   Size: {os.path.getsize(output_path) / 1024:.1f} KB")
    return output_path

def import_data(zip_path, overwrite=False):
    """Import self-improvement data from a zip file."""
    if not os.path.exists(zip_path):
        print(f"❌ File not found: {zip_path}")
        return False
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Check what's in the archive
        files = zf.namelist()
        print(f"Archive contains {len(files)} files:")
        
        # Group by type
        memory_files = [f for f in files if f.startswith("memory/")]
        print(f"  Memory files: {len(memory_files)}")
        
        # Import files
        imported = 0
        skipped = 0
        
        for file_path in files:
            target_path = os.path.join(WORKSPACE_DIR, file_path)
            
            # Skip if exists and not overwriting
            if os.path.exists(target_path) and not overwrite:
                skipped += 1
                continue
            
            # Create directory if needed
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # Extract file
            with zf.open(file_path) as source:
                with open(target_path, 'wb') as target:
                    target.write(source.read())
            
            imported += 1
            print(f"  Imported: {file_path}")
    
    print(f"\n✅ Import complete: {imported} files imported, {skipped} skipped")
    return True

def sync_status():
    """Show current data status."""
    print("=== Self-Improvement Data Status ===\n")
    
    # Check memory directory
    if os.path.exists(MEMORY_DIR):
        files = os.listdir(MEMORY_DIR)
        md_files = [f for f in files if f.endswith(".md")]
        json_files = [f for f in files if f.endswith(".json")]
        dirs = [f for f in files if os.path.isdir(os.path.join(MEMORY_DIR, f))]
        
        print(f"Memory directory:")
        print(f"  Daily logs: {len(md_files)} files")
        print(f"  JSON files: {len(json_files)} files")
        print(f"  Subdirectories: {len(dirs)}")
        
        # Check learning trail
        trail_path = os.path.join(MEMORY_DIR, ".learning-trail.json")
        if os.path.exists(trail_path):
            with open(trail_path) as f:
                trail = json.load(f)
            entries = trail.get("entries", [])
            changes = trail.get("changes", [])
            print(f"\nLearning trail:")
            print(f"  Entries: {len(entries)}")
            print(f"  Changes: {len(changes)}")
            print(f"  Version: {trail.get('version', 'unknown')}")
        
        # Check MEMORY.md
        memory_md = os.path.join(MEMORY_DIR, "MEMORY.md")
        if os.path.exists(memory_md):
            size = os.path.getsize(memory_md)
            print(f"\nMEMORY.md: {size / 1024:.1f} KB")
    else:
        print("❌ Memory directory not found")
    
    # Check skill scripts
    scripts_dir = os.path.join(SKILL_DIR, "scripts")
    if os.path.exists(scripts_dir):
        scripts = os.listdir(scripts_dir)
        print(f"\nSkill scripts: {len(scripts)} files")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 sync.py export [output_path]  - Export data to zip")
        print("  python3 sync.py import <zip_path>     - Import data from zip")
        print("  python3 sync.py status                - Show data status")
        print("  python3 sync.py import <zip_path> --overwrite  - Overwrite existing")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "export":
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        export_data(output_path)
    
    elif command == "import":
        if len(sys.argv) < 3:
            print("❌ Please specify zip file path")
            sys.exit(1)
        zip_path = sys.argv[2]
        overwrite = "--overwrite" in sys.argv
        import_data(zip_path, overwrite)
    
    elif command == "status":
        sync_status()
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
