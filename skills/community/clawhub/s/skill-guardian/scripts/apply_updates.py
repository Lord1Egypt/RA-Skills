#!/usr/bin/env python3
"""
Apply queued updates with intelligent trust-based decisions.
- High trust skills (>=90): Update immediately without delay
- Medium trust skills: 10-day grace period before auto-update
"""
import argparse
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

REGISTRY_FILE = Path(__file__).parent.parent / "assets" / "skill-registry.json"
DELAY_DAYS = 10
HIGH_TRUST_THRESHOLD = 90

def load_registry():
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE) as f:
            return json.load(f)
    return {"skills": {}, "pending_skills": {}, "high_trust_threshold": 90, "version": "1.0.0"}

def save_registry(registry):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)

def apply_update(skill_name, force=False, dry_run=False):
    registry = load_registry()
    
    if skill_name not in registry["skills"]:
        print(f"❌ Skill '{skill_name}' not found")
        return False
    
    info = registry["skills"][skill_name]
    
    if not info.get("update_available"):
        print(f"ℹ️  No update queued for {skill_name}")
        return False
    
    trust_score = info.get("trust_score", 0)
    is_high_trust = trust_score >= HIGH_TRUST_THRESHOLD
    
    queued_date = datetime.fromisoformat(info["update_queued_date"])
    eligible_date = queued_date + timedelta(days=DELAY_DAYS)
    
    # High trust skills can update immediately
    if is_high_trust:
        print(f"🌟 {skill_name}: High trust score ({trust_score}) - immediate update allowed")
    elif not force and datetime.now() < eligible_date:
        days_left = (eligible_date - datetime.now()).days
        print(f"⏳ {skill_name}: {days_left} days left in grace period (trust: {trust_score})")
        print(f"   Use --force to override")
        return False
    
    if dry_run:
        print(f"🔄 [DRY RUN] Would update {skill_name} to {info['latest_version']}")
        return True
    
    # Apply update
    print(f"🔄 Updating {skill_name} to {info['latest_version']}...")
    
    try:
        subprocess.run(
            ["clawhub", "update", skill_name, "--version", info["latest_version"]],
            check=True,
            timeout=120
        )
        
        # Update registry
        info["current_version"] = info["latest_version"]
        info["update_available"] = False
        info["update_queued_date"] = None
        info["last_updated"] = datetime.now().isoformat()
        
        save_registry(registry)
        print(f"✅ {skill_name} updated to {info['latest_version']}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Update failed: {e}")
        return False

def apply_all_updates(force=False, dry_run=False):
    registry = load_registry()
    applied = 0
    skipped = 0
    
    for name in list(registry["skills"].keys()):
        if registry["skills"][name].get("update_available"):
            if apply_update(name, force, dry_run):
                applied += 1
            else:
                skipped += 1
    
    print(f"\n✅ Applied: {applied} | ⏳ Skipped: {skipped}")
    return applied

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply queued skill updates")
    parser.add_argument("skill", nargs="?", help="Specific skill to update")
    parser.add_argument("--force", action="store_true", help="Override grace period")
    parser.add_argument("--all", action="store_true", help="Apply all eligible updates")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be updated")
    
    args = parser.parse_args()
    
    if args.skill:
        apply_update(args.skill, args.force, args.dry_run)
    elif args.all:
        apply_all_updates(args.force, args.dry_run)
    else:
        parser.print_help()
