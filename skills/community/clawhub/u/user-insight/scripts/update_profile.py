#!/usr/bin/env python3
"""
Update user profile with new insights.
Manages the user-profile.json file.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

PROFILE_PATH = Path.home() / ".openclaw" / "workspace" / "memory" / "user-profile.json"

def load_profile() -> Dict[str, Any]:
    """Load existing profile or create new one."""
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "basic_info": {},
        "interests": {},
        "preferences": {},
        "patterns": {},
        "interaction_stats": {
            "total_messages": 0,
            "first_interaction": None,
            "last_interaction": None
        },
        "conversation_history": []
    }

def save_profile(profile: Dict[str, Any]):
    """Save profile to disk."""
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

def update_interests(profile: Dict, new_interests: Dict[str, int]):
    """Update interest frequencies."""
    for interest, count in new_interests.items():
        profile["interests"][interest] = profile["interests"].get(interest, 0) + count

def update_preferences(profile: Dict, new_prefs: Dict[str, Any]):
    """Update preferences (latest value wins)."""
    for key, value in new_prefs.items():
        if key not in profile["preferences"]:
            profile["preferences"][key] = {"value": value, "confidence": 0.5}
        else:
            # Increase confidence if same value repeated
            if profile["preferences"][key]["value"] == value:
                profile["preferences"][key]["confidence"] = min(
                    1.0, profile["preferences"][key]["confidence"] + 0.1
                )
            else:
                # New value replaces old but with lower initial confidence
                profile["preferences"][key] = {"value": value, "confidence": 0.5}

def detect_patterns(profile: Dict, message: str, timestamp: str):
    """Detect and update usage patterns."""
    hour = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).hour
    
    # Active hours pattern
    if "active_hours" not in profile["patterns"]:
        profile["patterns"]["active_hours"] = {"morning": 0, "afternoon": 0, "evening": 0, "night": 0}
    
    if 6 <= hour < 12:
        profile["patterns"]["active_hours"]["morning"] += 1
    elif 12 <= hour < 18:
        profile["patterns"]["active_hours"]["afternoon"] += 1
    elif 18 <= hour < 23:
        profile["patterns"]["active_hours"]["evening"] += 1
    else:
        profile["patterns"]["active_hours"]["night"] += 1
    
    # Question ratio
    if "question_ratio" not in profile["patterns"]:
        profile["patterns"]["question_ratio"] = {"questions": 0, "total": 0}
    
    profile["patterns"]["question_ratio"]["total"] += 1
    if "?" in message or "？" in message:
        profile["patterns"]["question_ratio"]["questions"] += 1

def add_conversation_entry(profile: Dict, message: str, insights: Dict, timestamp: str):
    """Add entry to conversation history (limited size)."""
    entry = {
        "timestamp": timestamp,
        "message_preview": message[:100] + "..." if len(message) > 100 else message,
        "insights_extracted": {
            "interests": insights.get("interests", []),
            "preferences": list(insights.get("preferences", {}).keys())
        }
    }
    
    profile["conversation_history"].append(entry)
    
    # Keep only last 50 entries
    if len(profile["conversation_history"]) > 50:
        profile["conversation_history"] = profile["conversation_history"][-50:]

def update_profile(insights_json: str, original_message: str = ""):
    """Main update function."""
    try:
        insights = json.loads(insights_json)
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)
    
    profile = load_profile()
    timestamp = insights.get("timestamp", datetime.now().isoformat())
    
    # Update stats
    profile["interaction_stats"]["total_messages"] += 1
    if profile["interaction_stats"]["first_interaction"] is None:
        profile["interaction_stats"]["first_interaction"] = timestamp
    profile["interaction_stats"]["last_interaction"] = timestamp
    
    # Update interests
    if insights.get("interests"):
        update_interests(profile, {i: 1 for i in insights["interests"]})
    
    # Update preferences
    if insights.get("preferences"):
        update_preferences(profile, insights["preferences"])
    
    # Detect patterns
    if original_message:
        detect_patterns(profile, original_message, timestamp)
        add_conversation_entry(profile, original_message, insights, timestamp)
    
    save_profile(profile)
    
    # Output summary
    summary = {
        "status": "updated",
        "total_interactions": profile["interaction_stats"]["total_messages"],
        "top_interests": sorted(profile["interests"].items(), key=lambda x: x[1], reverse=True)[:5],
        "confirmed_preferences": [k for k, v in profile["preferences"].items() if v.get("confidence", 0) > 0.7]
    }
    
    print(json.dumps(summary, ensure_ascii=False, indent=2))

def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: update_profile.py '<insights_json>' [original_message]", file=sys.stderr)
        sys.exit(1)
    
    insights_json = sys.argv[1]
    original_message = sys.argv[2] if len(sys.argv) > 2 else ""
    
    update_profile(insights_json, original_message)

if __name__ == "__main__":
    main()
