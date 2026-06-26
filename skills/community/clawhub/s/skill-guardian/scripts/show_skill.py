#!/usr/bin/env python3
"""
Show detailed info for a specific skill.
"""
import argparse
import json
from datetime import datetime
from pathlib import Path

REGISTRY_FILE = Path(__file__).parent.parent / "assets" / "skill-registry.json"

def load_registry():
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE) as f:
            return json.load(f)
    return {"skills": {}, "version": "1.0.0"}

def show_skill(name):
    registry = load_registry()
    
    if name not in registry["skills"]:
        print(f"❌ Skill '{name}' not found in registry")
        return
    
    info = registry["skills"][name]
    
    print(f"\n📦 {name}")
    print("=" * 50)
    print(f"Description: {info.get('description', 'N/A')}")
    print(f"Source: {info.get('source', 'N/A')}")
    print(f"URL: {info.get('source_url', 'N/A')}")
    print(f"\n📊 Trust & Security")
    print(f"  Trust Score: {info.get('trust_score', 'N/A')}/100")
    print(f"  Risk Flags: {', '.join(info.get('risk_flags', [])) or 'None'}")
    print(f"\n📋 Version Info")
    print(f"  Current: {info.get('current_version') or 'N/A'}")
    print(f"  Latest: {info.get('latest_version') or 'N/A'}")
    print(f"  Added: {info.get('added_date', 'N/A')[:10]}")
    print(f"\n🔄 Update Status")
    if info.get("update_available"):
        queued = datetime.fromisoformat(info["update_queued_date"])
        print(f"  ⏳ Update queued: {info['latest_version']}")
        print(f"     Queued on: {queued.strftime('%Y-%m-%d')}")
    else:
        print(f"  ✓ Up to date")
    print(f"  Auto-update: {'Enabled' if info.get('auto_update', True) else 'Disabled'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show skill details")
    parser.add_argument("name", help="Skill name")
    args = parser.parse_args()
    show_skill(args.name)
