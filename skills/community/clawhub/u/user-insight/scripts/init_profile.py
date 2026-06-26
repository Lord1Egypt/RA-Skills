#!/usr/bin/env python3
"""
Initialize user profile and exploration system.
Run once to set up the memory structure.
"""

import json
from datetime import datetime
from pathlib import Path

def init_user_insight_system():
    """Create initial profile and directory structure."""
    
    memory_dir = Path.home() / ".openclaw/workspace/memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    
    # Create default profile
    profile_path = memory_dir / "user-profile.json"
    if not profile_path.exists():
        default_profile = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "basic_info": {},
            "interests": [],
            "communication_style": {},
            "patterns": {
                "active_hours": [],
                "mood_indicators": {}
            },
            "preferences": {
                "likes": [],
                "dislikes": []
            },
            "interaction_stats": {
                "total_messages": 0,
                "first_interaction": None,
                "last_interaction": None
            },
            "conversation_history": [],
            "exploration_state": {
                "last_exploration_date": None,
                "explored_categories": [],
                "pending_categories": [
                    "technology", "current_events", "lifestyle", 
                    "entertainment", "knowledge", "personal_growth"
                ],
                "avoided_topics": []
            }
        }
        
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(default_profile, f, ensure_ascii=False, indent=2)
        print(f"✅ Created profile: {profile_path}")
    else:
        print(f"ℹ️ Profile already exists: {profile_path}")
    
    # Create exploration log
    exploration_path = memory_dir / "topic-exploration.json"
    if not exploration_path.exists():
        default_log = {
            "exploration_log": [],
            "success_patterns": []
        }
        
        with open(exploration_path, 'w', encoding='utf-8') as f:
            json.dump(default_log, f, ensure_ascii=False, indent=2)
        print(f"✅ Created exploration log: {exploration_path}")
    else:
        print(f"ℹ️ Exploration log already exists: {exploration_path}")
    
    print("\n🎉 User insight system initialized!")
    print("\nNext steps:")
    print("1. Start chatting naturally - insights will be collected passively")
    print("2. Run 'python explore.py --check' to see if topic exploration is recommended")
    print("3. Check your profile at ~/.openclaw/workspace/memory/user-profile.json")

if __name__ == "__main__":
    init_user_insight_system()
