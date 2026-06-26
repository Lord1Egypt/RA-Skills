#!/usr/bin/env python3
from datetime import datetime

def calculate_cognitive_weight(item_type: str, energy: str, tiny: bool) -> int:
    weight = 2
    if item_type == "commitment":
        weight += 2
    if energy == "high":
        weight += 2
    if tiny:
        return 1
    return weight

def calculate_temperature(created_at: str, last_touched_at: str = None) -> str:
    now = datetime.now()
    ref = last_touched_at or created_at
    age_days = (now - datetime.fromisoformat(ref)).total_seconds() / 86400
    if age_days <= 3:
        return "hot"
    if age_days <= 14:
        return "warm"
    return "cold"

def calculate_hot_score(created_at: str, last_touched_at: str = None) -> int:
    now = datetime.now()
    ref = last_touched_at or created_at
    age_days = (now - datetime.fromisoformat(ref)).total_seconds() / 86400
    score = max(0, int(100 - age_days * 5))
    return score
