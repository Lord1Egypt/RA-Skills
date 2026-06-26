#!/usr/bin/env python3
"""
Soulsync Detector — Assesses current personalization level of an OpenClaw workspace.
Returns: new | partial | established
"""
import os
import sys
import json

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))

def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def assess_file(content, default_markers=None):
    """Score a file's personalization level. Returns 0-1."""
    if content is None:
        return 0.0
    if len(content) < 50:
        return 0.1
    
    # Check for default/template content
    if default_markers:
        for marker in default_markers:
            if marker.lower() in content.lower():
                return 0.2
    
    # Score based on content richness
    lines = [l for l in content.split("\n") if l.strip()]
    word_count = len(content.split())
    
    if word_count < 30:
        return 0.2
    elif word_count < 100:
        return 0.5
    elif word_count < 300:
        return 0.7
    else:
        return 1.0

def detect():
    soul = read_file(os.path.join(WORKSPACE, "SOUL.md"))
    user = read_file(os.path.join(WORKSPACE, "USER.md"))
    memory = read_file(os.path.join(WORKSPACE, "MEMORY.md"))
    identity = read_file(os.path.join(WORKSPACE, "IDENTITY.md"))
    
    # Check for memory files
    memory_dir = os.path.join(WORKSPACE, "memory")
    memory_files = []
    if os.path.isdir(memory_dir):
        memory_files = [f for f in os.listdir(memory_dir) if f.endswith(".md")]
    
    # Score each component
    soul_score = assess_file(soul, default_markers=[
        "you're not a chatbot",
        "this is a starting point",
        "make it yours",
        "_you're not a chatbot_"
    ])
    
    user_score = assess_file(user, default_markers=[
        "preferred name:",
        "example",
        "your name here"
    ])
    
    memory_score = assess_file(memory, default_markers=[
        "no memories yet",
        "this file is empty"
    ])
    
    # Bonus for existing memory day files
    memory_day_bonus = min(len(memory_files) * 0.1, 0.5)
    
    # Overall score
    total = (soul_score * 0.3) + (user_score * 0.3) + (memory_score * 0.2) + (memory_day_bonus * 0.2)
    
    # Determine level
    if total < 0.2:
        level = "new"
    elif total < 0.6:
        level = "partial"
    else:
        level = "established"
    
    result = {
        "level": level,
        "score": round(total, 2),
        "details": {
            "soul_md": {"exists": soul is not None, "score": soul_score},
            "user_md": {"exists": user is not None, "score": user_score},
            "memory_md": {"exists": memory is not None, "score": memory_score},
            "identity_md": {"exists": identity is not None},
            "memory_days": len(memory_files),
        },
        "gaps": []
    }
    
    # Identify specific gaps
    if soul_score < 0.5:
        result["gaps"].append("soul_md — personality and communication style not defined")
    if user_score < 0.5:
        result["gaps"].append("user_md — basic info about the user is missing or sparse")
    if memory_score < 0.3:
        result["gaps"].append("memory_md — no long-term memory established")
    if not identity:
        result["gaps"].append("identity_md — agent identity not configured")
    if len(memory_files) < 3:
        result["gaps"].append("memory_days — limited interaction history")
    
    return result

if __name__ == "__main__":
    result = detect()
    print(json.dumps(result, indent=2))
