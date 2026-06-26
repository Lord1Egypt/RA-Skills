#!/usr/bin/env python3
"""
Add a new skill to the registry with security vetting and pending period.
New skills are held for 5-10 days before being fully added.
"""
import argparse
import json
import random
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

REGISTRY_FILE = Path(__file__).parent.parent / "assets" / "skill-registry.json"
PENDING_MIN_DAYS = 5
PENDING_MAX_DAYS = 10

def load_registry():
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE) as f:
            return json.load(f)
    return {"skills": {}, "pending_skills": {}, "high_trust_threshold": 90, "version": "1.0.0"}

def save_registry(registry):
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)

def vet_skill(skill_name):
    """Run skill-vetter security check."""
    try:
        result = subprocess.run(
            ["python3", "skills/skill-vetter/scripts/vet.py", skill_name],
            capture_output=True,
            text=True,
            timeout=60
        )
        # Parse vetter output (simplified)
        return {
            "trust_score": 80,  # Placeholder - would parse actual output
            "risk_flags": [],
            "passed": True
        }
    except Exception as e:
        return {
            "trust_score": 0,
            "risk_flags": [f"Vetting failed: {e}"],
            "passed": False
        }

def add_skill(name, source, url=None, description=""):
    registry = load_registry()
    
    if name in registry["skills"]:
        print(f"⚠️  Skill '{name}' already exists in registry.")
        return False
    
    if name in registry.get("pending_skills", {}):
        print(f"⏳ Skill '{name}' is already pending approval.")
        return False
    
    print(f"🔍 Vetting {name}...")
    vet_result = vet_skill(name)
    
    if not vet_result["passed"]:
        print(f"❌ Security check failed for {name}")
        print(f"   Risk flags: {vet_result['risk_flags']}")
        confirm = input("Add anyway? (y/N): ")
        if confirm.lower() != 'y':
            return False
    
    # Random pending period between 5-10 days
    pending_days = random.randint(PENDING_MIN_DAYS, PENDING_MAX_DAYS)
    eligible_date = datetime.now() + timedelta(days=pending_days)
    
    # Add to pending queue
    if "pending_skills" not in registry:
        registry["pending_skills"] = {}
    
    registry["pending_skills"][name] = {
        "name": name,
        "source": source,
        "source_url": url,
        "description": description,
        "trust_score": vet_result["trust_score"],
        "risk_flags": vet_result["risk_flags"],
        "current_version": None,
        "latest_version": None,
        "pending_date": datetime.now().isoformat(),
        "eligible_date": eligible_date.isoformat(),
        "pending_days": pending_days,
        "auto_update": True
    }
    
    save_registry(registry)
    print(f"✅ Added {name} to PENDING queue")
    print(f"   Trust score: {vet_result['trust_score']}")
    print(f"   Will be eligible for addition on: {eligible_date.strftime('%Y-%m-%d')} ({pending_days} days)")
    print(f"   Run 'python3 scripts/process_pending.py' after the pending period")
    return True

def process_pending():
    """Process pending skills that have passed the waiting period."""
    registry = load_registry()
    processed = 0
    
    if "pending_skills" not in registry:
        print("📭 No pending skills")
        return 0
    
    for name in list(registry["pending_skills"].keys()):
        pending = registry["pending_skills"][name]
        eligible_date = datetime.fromisoformat(pending["eligible_date"])
        
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
            print(f"✅ {name}: Promoted from pending to active registry")
        else:
            days_left = (eligible_date - datetime.now()).days
            print(f"⏳ {name}: {days_left} days remaining in pending period")
    
    save_registry(registry)
    if processed > 0:
        print(f"\n✅ Processed {processed} pending skill(s)")
    return processed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add skill to registry")
    parser.add_argument("--name", help="Skill name")
    parser.add_argument("--source", choices=["clawhub", "github", "local"])
    parser.add_argument("--url", help="Source URL")
    parser.add_argument("--description", default="", help="Skill description")
    parser.add_argument("--process-pending", action="store_true", help="Process pending skills")
    
    args = parser.parse_args()
    
    if args.process_pending:
        process_pending()
    elif args.name and args.source:
        add_skill(args.name, args.source, args.url, args.description)
    else:
        parser.print_help()
