"""
Instant timer management for time-guru.
Supports start/stop with local file-based state for cross-session persistence.
"""
import json
import os
import logging
from typing import Optional, Dict
from datetime import datetime

logger = logging.getLogger(__name__)

DATA_DIR = os.path.expanduser("~/.openclaw/data/time-guru")
ACTIVE_TIMER_FILE = os.path.join(DATA_DIR, ".active-timer.json")


def start_timer(description: str, project: str = "", category: str = "",
                billable: bool = False) -> Dict:
    """
    Start a new timer. If one is already running, it's stopped first.
    
    Args:
        description: Activity description.
        project: Project name.
        category: Category type.
        billable: Whether billable.
        
    Returns:
        Timer status dict.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Check for existing timer
    existing = get_active_timer()
    stopped_previous = None
    if existing:
        stopped_previous = stop_timer()
    
    # Start new timer
    timer = {
        "description": description,
        "project": project,
        "category": category,
        "billable": billable,
        "started_at": datetime.now().isoformat(),
    }
    
    _write_active_timer(timer)
    
    result = {
        "description": description,
        "project": project,
        "started_at": timer["started_at"],
        "status": "started",
        "stopped_previous": stopped_previous,
    }
    
    return result


def stop_timer() -> Optional[Dict]:
    """
    Stop the current timer and save the entry.
    
    Returns:
        Completed timer entry as dict, or None if no active timer.
    """
    timer = get_active_timer()
    if not timer:
        return None
    
    started_at = datetime.fromisoformat(timer["started_at"])
    ended_at = datetime.now()
    duration_minutes = int((ended_at - started_at).total_seconds() / 60)
    
    # Create a log entry
    entry = {
        "description": timer["description"],
        "start": started_at.strftime("%H:%M"),
        "end": ended_at.strftime("%H:%M"),
        "duration_minutes": duration_minutes,
        "category": timer.get("category", ""),
        "project": timer.get("project", ""),
        "billable": timer.get("billable", False),
        "timestamp": ended_at.isoformat(),
    }
    
    # Save the entry
    today_file = _get_today_file()
    _append_entry(today_file, entry)
    
    # Clear active timer
    _clear_active_timer()
    
    entry["started_at"] = timer["started_at"]
    entry["ended_at"] = ended_at.isoformat()
    
    return entry


def get_active_timer() -> Optional[Dict]:
    """
    Get the currently active timer if one exists.
    
    Returns:
        Timer dict or None.
    """
    if not os.path.exists(ACTIVE_TIMER_FILE):
        return None
    
    try:
        with open(ACTIVE_TIMER_FILE, "r") as f:
            timer = json.load(f)
        
        # Calculate elapsed time
        started_at = datetime.fromisoformat(timer["started_at"])
        elapsed = int((datetime.now() - started_at).total_seconds() / 60)
        timer["elapsed_minutes"] = elapsed
        
        return timer
    except (json.JSONDecodeError, KeyError, IOError) as e:
        logger.warning("Error reading active timer: %s", e)
        return None


def format_timer_status(timer: Dict) -> str:
    """Format the timer status for display."""
    desc = timer.get("description", "Untitled")
    elapsed = timer.get("elapsed_minutes", 0)
    hours = elapsed // 60
    mins = elapsed % 60
    
    if hours > 0:
        duration_str = f"{hours}h{mins:02d}m"
    else:
        duration_str = f"{mins}m"
    
    return f"▶️  {desc} | Elapsed: {duration_str}"


def _write_active_timer(timer: Dict):
    """Write the active timer to disk."""
    with open(ACTIVE_TIMER_FILE, "w") as f:
        json.dump(timer, f, ensure_ascii=False)


def _clear_active_timer():
    """Remove the active timer file."""
    if os.path.exists(ACTIVE_TIMER_FILE):
        os.remove(ACTIVE_TIMER_FILE)


def _get_today_file() -> str:
    """Get the log file path for today."""
    today = datetime.now()
    day_dir = os.path.join(DATA_DIR, today.strftime("%Y/%m"))
    os.makedirs(day_dir, exist_ok=True)
    return os.path.join(day_dir, f"{today.strftime('%d')}.json")


def _append_entry(filepath: str, entry: Dict):
    """Append a log entry to the day file."""
    entries = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                entries = json.load(f)
                if not isinstance(entries, list):
                    entries = []
        except (json.JSONDecodeError, IOError):
            entries = []
    
    # Assign ID
    entry["id"] = f"{datetime.now().strftime('%Y%m%d')}-{len(entries) + 1:04d}"
    
    entries.append(entry)
    
    with open(filepath, "w") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
