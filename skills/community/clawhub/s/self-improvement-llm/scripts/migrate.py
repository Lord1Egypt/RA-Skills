#!/usr/bin/env python3
"""Migration and compatibility check for self-improvement skill updates."""

import json
import os
import sys
from datetime import datetime

MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
LEARNING_TRAIL = os.path.join(MEMORY_DIR, ".learning-trail.json")
MEMORY_INDEX = os.path.join(MEMORY_DIR, ".memory-index.json")

def check_compatibility():
    """Check if existing data is compatible with current version."""
    issues = []
    
    # Check .learning-trail.json
    if os.path.exists(LEARNING_TRAIL):
        try:
            with open(LEARNING_TRAIL, 'r') as f:
                trail = json.load(f)
            
            # Check version
            version = trail.get("version", 0)
            if version < 3:
                issues.append(f".learning-trail.json version {version} < 3, needs migration")
            
            # Check required fields
            required_fields = ["version", "entries", "changes", "watchlist", "stats"]
            for field in required_fields:
                if field not in trail:
                    issues.append(f".learning-trail.json missing field: {field}")
            
            # Check entries structure
            for entry in trail.get("entries", []):
                if not isinstance(entry, dict):
                    issues.append(f"Invalid entry type: {type(entry)}")
                    break
                if "id" not in entry:
                    issues.append("Entry missing 'id' field")
                    break
                    
        except json.JSONDecodeError:
            issues.append(".learning-trail.json is invalid JSON")
        except Exception as e:
            issues.append(f"Error reading .learning-trail.json: {e}")
    else:
        issues.append(".learning-trail.json not found (will be created on first run)")
    
    # Check .memory-index.json
    if os.path.exists(MEMORY_INDEX):
        try:
            with open(MEMORY_INDEX, 'r') as f:
                index = json.load(f)
            # Basic structure check
            if not isinstance(index, dict):
                issues.append(".memory-index.json is not a dict")
        except json.JSONDecodeError:
            issues.append(".memory-index.json is invalid JSON")
        except Exception as e:
            issues.append(f"Error reading .memory-index.json: {e}")
    
    return issues

def migrate_v2_to_v3():
    """Migrate .learning-trail.json from v2 to v3 format."""
    if not os.path.exists(LEARNING_TRAIL):
        print("No .learning-trail.json to migrate")
        return True
    
    try:
        with open(LEARNING_TRAIL, 'r') as f:
            trail = json.load(f)
        
        if trail.get("version", 0) >= 3:
            print("Already at version 3 or higher")
            return True
        
        # Backup original
        backup_path = LEARNING_TRAIL + f".backup.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        with open(backup_path, 'w') as f:
            json.dump(trail, f, indent=2)
        print(f"Backed up to: {backup_path}")
        
        # Migrate entries if needed
        if "entries" not in trail:
            trail["entries"] = []
        
        # Ensure all entries have required fields
        for entry in trail["entries"]:
            if "id" not in entry:
                entry["id"] = f"LRN-{datetime.now().strftime('%Y%m%d')}-000"
            if "status" not in entry:
                entry["status"] = "pending"
            if "priority" not in entry:
                entry["priority"] = "medium"
        
        # Update version
        trail["version"] = 3
        
        # Add missing fields
        if "changes" not in trail:
            trail["changes"] = []
        if "watchlist" not in trail:
            trail["watchlist"] = []
        if "stats" not in trail:
            trail["stats"] = {"total_entries": len(trail["entries"]), "total_changes": len(trail["changes"])}
        
        # Save migrated data
        with open(LEARNING_TRAIL, 'w') as f:
            json.dump(trail, f, indent=2)
        
        print(f"Migration complete: {len(trail['entries'])} entries migrated")
        return True
        
    except Exception as e:
        print(f"Migration failed: {e}")
        return False

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--migrate":
        success = migrate_v2_to_v3()
        sys.exit(0 if success else 1)
    else:
        issues = check_compatibility()
        if issues:
            print("Compatibility issues found:")
            for issue in issues:
                print(f"  - {issue}")
            print("\nRun with --migrate to fix issues")
            sys.exit(1)
        else:
            print("All checks passed")
            sys.exit(0)

if __name__ == "__main__":
    main()
