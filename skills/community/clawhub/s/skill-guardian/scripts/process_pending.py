#!/usr/bin/env python3
"""
Process pending skills that have passed the 5-10 day waiting period.
"""
import json
from datetime import datetime
from pathlib import Path

REGISTRY_FILE = Path(__file__).parent.parent / "assets" / "skill-registry.json"

def load_registry():
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE) as f:
            return json.load(f)
    return {"skills": {}, "pending_skills": {}, "high_trust_threshold": 90, "version": "1.0.0"}

def save_registry(registry):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)

def process_pending():
    """Process pending skills that have passed the waiting period."""
    registry = load_registry()
    processed = 0
    
    if "pending_skills" not in registry or not registry["pending_skills"]:
        print("📭 No pending skills")
        return 0
    
    print(f"🔍 Checking {len(registry['pending_skills'])} pending skill(s)...\n")
    
    for name in list(registry["pending_skills"].keys()):
        pending = registry["pending_skills"][name]
        eligible_date = datetime.fromisoformat(pending["eligible_date"])
        days_waited = (datetime.now() - datetime.fromisoformat(pending["pending_date"])).days
        
        if datetime.now() >= eligible_date:
            # Move from pending to active
            registry["skills"][name] = {
                "name": name,
                "source": pending["source"],
                "source_url": pending["source_url"],
                "description": pending["description"],
                "trust_score": pending["trust_score"],
                "risk_flags": pending["risk_flags"],
                "current_version": None,
                "latest_version": None,
                "added_date": datetime.now().isoformat(),
                "last_updated": None,
                "update_available": False,
                "update_queued_date": None,
                "auto_update": pending.get("auto_update", True)
            }
            del registry["pending_skills"][name]
            processed += 1
            print(f"✅ {name}: Promoted to active registry (waited {days_waited} days)")
        else:
            days_left = (eligible_date - datetime.now()).days
            print(f"⏳ {name}: {days_left} days remaining ({days_waited}/{pending['pending_days']} days waited)")
    
    save_registry(registry)
    
    if processed > 0:
        print(f"\n🎉 Processed {processed} skill(s) from pending to active")
    else:
        print("\n📭 No skills ready for promotion yet")
    
    return processed

if __name__ == "__main__":
    process_pending()
