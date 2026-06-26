#!/usr/bin/env python3
"""
Main exploration orchestrator.
Decides when and how to initiate topic exploration with user.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

# Import our modules
sys.path.insert(0, str(Path(__file__).parent))
from topic_recommender import (
    load_profile, load_exploration_log, recommend_topic, should_explore_now
)

def get_last_interaction_time() -> datetime:
    """Get timestamp of last user interaction from memory files."""
    memory_dir = Path.home() / ".openclaw/workspace/memory"
    
    latest = None
    for pattern in ["*.md", "*.json"]:
        for file in memory_dir.glob(pattern):
            if file.name.startswith("user-profile") or file.name.startswith("topic-exploration"):
                continue
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if latest is None or mtime > latest:
                latest = mtime
    
    return latest or datetime.now() - timedelta(days=7)

def generate_exploration_prompt(profile: Dict, recommendation: Dict) -> str:
    """Generate a natural conversation starter."""
    
    # Get user's preferred style
    style = profile.get("communication_style", {})
    formality = style.get("formality", "casual")
    verbosity = style.get("verbosity", "moderate")
    
    base_message = recommendation["suggested_opening"]
    
    # Adjust based on formality
    if formality == "casual":
        # Add emoji or casual opener occasionally
        casual_starters = ["嘿，", "话说，", "刚想到，"]
        import random
        if random.random() < 0.3:
            base_message = random.choice(casual_starters) + base_message
    elif formality == "formal":
        # Remove any emojis, make more polished
        base_message = base_message.replace("😄", "").replace("哈哈", "")
    
    # Adjust based on verbosity preference
    if verbosity == "minimal":
        # Keep it short
        base_message = base_message.split("。")[0] + "。"
    elif verbosity == "detailed" and len(base_message) < 50:
        # Add more context for users who like detail
        base_message += " 我查了些资料，发现几个值得关注的点..."
    
    return base_message

def run_exploration_check(dry_run: bool = False) -> Dict:
    """
    Main entry point for exploration check.
    Returns recommendation if exploration should happen, else None.
    """
    
    profile = load_profile()
    log = load_exploration_log()
    
    # Check if we should explore now
    if not should_explore_now(profile, log):
        return {
            "should_explore": False,
            "reason": "Too soon since last exploration or insufficient pending topics"
        }
    
    # Check time since last interaction
    last_interaction = get_last_interaction_time()
    hours_since = (datetime.now() - last_interaction).total_seconds() / 3600
    
    if hours_since < 12:
        return {
            "should_explore": False,
            "reason": f"Last interaction was only {hours_since:.1f} hours ago"
        }
    
    # Generate recommendation
    recommendation = recommend_topic(profile, log)
    
    # Generate the actual message
    prompt = generate_exploration_prompt(profile, recommendation)
    
    result = {
        "should_explore": True,
        "hours_since_last_interaction": round(hours_since, 1),
        "recommendation": recommendation,
        "suggested_message": prompt,
        "timestamp": datetime.now().isoformat()
    }
    
    if not dry_run:
        # Update profile with exploration attempt
        profile["exploration_state"]["last_exploration_date"] = datetime.now().isoformat()
        profile["exploration_state"]["explored_categories"].append(
            recommendation["category"]
        )
        
        # Save updated profile
        profile_path = Path.home() / ".openclaw/workspace/memory/user-profile.json"
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
    
    return result

def record_exploration_result(topic: str, category: str, reaction: str, notes: str = ""):
    """Record the result of an exploration attempt."""
    
    log_path = Path.home() / ".openclaw/workspace/memory/topic-exploration.json"
    
    # Load existing log
    if log_path.exists():
        with open(log_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"exploration_log": [], "success_patterns": []}
    
    # Determine interest level
    interest_detected = reaction in ["high", "medium", "asked_followup"]
    
    # Add new entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "category": category,
        "user_reaction": reaction,
        "interest_detected": interest_detected,
        "notes": notes
    }
    data["exploration_log"].append(entry)
    
    # Save
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Update profile interests if high interest
    if interest_detected:
        profile = load_profile()
        existing = [i for i in profile.get("interests", []) if i["topic"] == topic]
        
        if existing:
            existing[0]["score"] = min(1.0, existing[0].get("score", 0.5) + 0.15)
            existing[0].setdefault("engagement_history", []).append({
                "date": datetime.now().isoformat()[:10],
                "reaction": reaction
            })
        else:
            profile.setdefault("interests", []).append({
                "topic": topic,
                "category": category,
                "score": 0.6 if reaction == "medium" else 0.8,
                "discovery_method": "exploration",
                "engagement_history": [{
                    "date": datetime.now().isoformat()[:10],
                    "reaction": reaction
                }]
            })
        
        profile_path = Path.home() / ".openclaw/workspace/memory/user-profile.json"
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
    
    return {"recorded": True, "interest_detected": interest_detected}

def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="User topic exploration")
    parser.add_argument("--check", action="store_true", help="Check if should explore now")
    parser.add_argument("--dry-run", action="store_true", help="Don't update files")
    parser.add_argument("--record", nargs=4, metavar=("TOPIC", "CATEGORY", "REACTION", "NOTES"),
                       help="Record exploration result")
    
    args = parser.parse_args()
    
    if args.record:
        result = record_exploration_result(args.record[0], args.record[1], 
                                          args.record[2], args.record[3])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.check:
        result = run_exploration_check(dry_run=args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Default: check and recommend
        result = run_exploration_check(dry_run=args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
