"""
Goal tracker for time-guru.
Set, check, and track time allocation goals.
"""
import json
import os
import logging
from typing import Dict, List, Optional
from datetime import datetime, date, timedelta

import store

logger = logging.getLogger(__name__)

DATA_DIR = os.path.expanduser("~/.openclaw/data/time-guru")
GOALS_FILE = os.path.join(DATA_DIR, "goals.json")


def set_goal(category: str, target_hours_per_day: Optional[float] = None,
             target_hours_per_week: Optional[float] = None) -> Dict:
    """
    Set a time allocation goal for a category.
    
    Args:
        category: Activity category.
        target_hours_per_day: Daily target hours.
        target_hours_per_week: Weekly target hours.
        
    Returns:
        Goal status dict.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    
    goals = _load_goals()
    
    if category not in goals:
        goals[category] = {}
    
    if target_hours_per_day is not None:
        goals[category]["target_hours_per_day"] = target_hours_per_day
    if target_hours_per_week is not None:
        goals[category]["target_hours_per_week"] = target_hours_per_week
    
    goals[category]["set_at"] = datetime.now().isoformat()
    
    _save_goals(goals)
    
    return {
        "category": category,
        "target_hours_per_day": target_hours_per_day,
        "target_hours_per_week": target_hours_per_week,
        "status": "set",
    }


def get_goals() -> Dict:
    """Get all goals with current progress."""
    goals = _load_goals()
    today_entries = store.get_today_entries()
    week_start = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
    week_entries = store.get_entries(week_start, datetime.now().date())
    
    result = {}
    for category, goal in goals.items():
        # Calculate current progress
        daily_minutes = sum(
            e.get("duration_minutes", 0) for e in today_entries
            if e.get("category") == category
        )
        weekly_minutes = sum(
            e.get("duration_minutes", 0) for e in week_entries
            if e.get("category") == category
        )
        
        daily_hours = round(daily_minutes / 60, 1) if daily_minutes else 0
        weekly_hours = round(weekly_minutes / 60, 1) if weekly_minutes else 0
        
        target_day = goal.get("target_hours_per_day", 0)
        target_week = goal.get("target_hours_per_week", 0)
        
        progress = {}
        if target_day:
            progress["daily"] = {
                "current": daily_hours,
                "target": target_day,
                "progress_percent": round(min(daily_hours / target_day * 100, 100), 1),
            }
        if target_week:
            progress["weekly"] = {
                "current": weekly_hours,
                "target": target_week,
                "progress_percent": round(min(weekly_hours / target_week * 100, 100), 1),
            }
        
        result[category] = {
            "goal": goal,
            "progress": progress,
        }
    
    return result


def check_goal_status(category: Optional[str] = None) -> Dict:
    """
    Check progress against goals.
    
    Args:
        category: Specific category to check, or None for all.
        
    Returns:
        Dict with goal status data.
    """
    goals = _load_goals()
    
    if category:
        goals = {k: v for k, v in goals.items() if k == category}
    
    if not goals:
        return {"status": "no_goals", "message": "No goals set. Use `goal set <category> <hours>/day` to start."}
    
    return {"status": "ok", "goals": get_goals()}


def _load_goals() -> Dict:
    """Load goals from file."""
    if not os.path.exists(GOALS_FILE):
        return {}
    try:
        with open(GOALS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_goals(goals: Dict):
    """Save goals to file."""
    with open(GOALS_FILE, "w") as f:
        json.dump(goals, f, ensure_ascii=False, indent=2)


def reset_goals() -> Dict:
    """Clear all goals."""
    if os.path.exists(GOALS_FILE):
        os.remove(GOALS_FILE)
    return {"status": "reset", "message": "All goals have been cleared."}
