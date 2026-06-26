#!/usr/bin/env python3
"""
List all skills in the registry.
"""
import json
from pathlib import Path

REGISTRY_FILE = Path(__file__).parent.parent / "assets" / "skill-registry.json"

def load_registry():
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE) as f:
            return json.load(f)
    return {"skills": {}, "version": "1.0.0"}

def list_skills():
    registry = load_registry()
    
    if not registry["skills"]:
        print("📭 Registry is empty")
        return
    
    print(f"\n{'Skill':<20} {'Version':<12} {'Trust':<8} {'Status':<15} {'Source'}")
    print("-" * 80)
    
    for name, info in sorted(registry["skills"].items()):
        version = info.get("current_version") or "N/A"
        trust = info.get("trust_score", 0)
        
        if info.get("update_available"):
            status = f"⏳ queued ({info['latest_version']})"
        else:
            status = "✓ current"
        
        source = info.get("source", "unknown")
        print(f"{name:<20} {version:<12} {trust:<8} {status:<15} {source}")
    
    print(f"\n📊 Total: {len(registry['skills'])} skill(s)")

if __name__ == "__main__":
    list_skills()
