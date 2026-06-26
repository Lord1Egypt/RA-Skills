#!/usr/bin/env python3
"""
Check for skill updates and queue them with 10-day delay.
"""
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

REGISTRY_FILE = Path(__file__).parent.parent / "assets" / "skill-registry.json"
DELAY_DAYS = 10

def load_registry():
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE) as f:
            return json.load(f)
    return {"skills": {}, "version": "1.0.0"}

def save_registry(registry):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)

def get_latest_version(skill_name):
    """Query clawhub for latest version."""
    try:
        result = subprocess.run(
            ["clawhub", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )
        # Parse output to find version (simplified)
        for line in result.stdout.split("\n"):
            if skill_name in line:
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1]  # Version column
        return None
    except Exception as e:
        print(f"⚠️  Could not check version for {skill_name}: {e}")
        return None

def check_updates():
    registry = load_registry()
    updates_found = 0
    
    for name, info in registry["skills"].items():
        if not info.get("auto_update", True):
            continue
            
        latest = get_latest_version(name)
        if latest and latest != info.get("current_version"):
            if not info.get("update_available"):
                # New update detected - queue with delay
                info["latest_version"] = latest
                info["update_available"] = True
                info["update_queued_date"] = datetime.now().isoformat()
                updates_found += 1
                print(f"📦 {name}: {info['current_version']} → {latest} (queued, {DELAY_DAYS}d delay)")
            else:
                print(f"⏳ {name}: already queued ({info['latest_version']})")
    
    save_registry(registry)
    print(f"\n✅ Found {updates_found} new update(s)")
    return updates_found

if __name__ == "__main__":
    print("🔍 Checking for skill updates...")
    check_updates()
