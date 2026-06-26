#!/usr/bin/env python3
"""
Skill Recommender
- Recommend relevant skills based on role
- Load recommendation rules
"""

import json
import os

def get_recommendations_path():
    """Get recommendation rules file path"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "../data/skill_recommendations.json")

def load_recommendations():
    """Load recommendation rules"""
    rec_path = get_recommendations_path()
    with open(rec_path, "r", encoding="utf-8") as f:
        return json.load(f)["recommendations"]

def get_recommendations(template_id):
    """Get recommended skills by role template ID"""
    recommendations = load_recommendations()
    return recommendations.get(template_id, {}).get("skills", [])

def format_recommendations(skills):
    """Format recommended skill list"""
    if not skills:
        return "No recommended skills yet"
    
    result = "Based on your role, I recommend these skills:\n"
    for i, skill in enumerate(skills, 1):
        result += f"{i}. {skill}\n"
    return result

if __name__ == "__main__":
    # Test code
    test_id = "personal-assistant"
    skills = get_recommendations(test_id)
    print(f"Recommendations for template {test_id}:")
    print(format_recommendations(skills))
