"""
Time log persistence for time-guru.
Stores and retrieves time entries from JSON files organized by date.
"""
import json
import os
import shutil
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta, date

logger = logging.getLogger(__name__)

DATA_DIR = os.path.expanduser("~/.openclaw/data/time-guru")
BACKUP_DIR = os.path.join(DATA_DIR, ".backups")
MAX_BACKUPS = 7


def log_entry(entry: Dict) -> Dict:
    """
    Save a single time log entry.
    
    Args:
        entry: Dict with start, end, duration_minutes, description, etc.
        
    Returns:
        The saved entry with assigned ID.
    """
    now = datetime.now()
    
    # Determine the date this entry belongs to
    entry_date = now.date()
    
    # Auto-categorize if not set
    if not entry.get("category"):
        from classifier import classify_activity
        entry["category"] = classify_activity(entry.get("description", ""))
    
    # Generate ID
    entry_date_str = entry_date.strftime("%Y%m%d")
    filepath = _get_day_file(entry_date)
    
    entries = _load_day(entry_date)
    entry["id"] = f"{entry_date_str}-{len(entries) + 1:04d}"
    entry["date"] = entry_date_str
    entry["created_at"] = now.isoformat()
    
    entries.append(entry)
    _save_day(entry_date, entries)
    
    return entry


def get_entries(date_from: date, date_to: date) -> List[Dict]:
    """
    Get all log entries within a date range.
    
    Args:
        date_from: Start date (inclusive).
        date_to: End date (inclusive).
        
    Returns:
        List of entry dicts sorted by date then time.
    """
    entries = []
    current = date_from
    
    while current <= date_to:
        day_entries = _load_day(current)
        entries.extend(day_entries)
        current += timedelta(days=1)
    
    return entries


def get_today_entries() -> List[Dict]:
    """Get today's entries."""
    return _load_day(datetime.now().date())


def get_day_total_minutes(day: date) -> int:
    """Get total logged minutes for a day."""
    entries = _load_day(day)
    return sum(e.get("duration_minutes", 0) for e in entries)


def update_entry(entry_id: str, updates: Dict) -> bool:
    """Update an existing entry by ID."""
    # Search all recent files
    for day_offset in range(30):
        day = datetime.now().date() - timedelta(days=day_offset)
        entries = _load_day(day)
        for i, entry in enumerate(entries):
            if entry.get("id") == entry_id:
                entries[i].update(updates)
                _save_day(day, entries)
                return True
    return False


def delete_entry(entry_id: str) -> bool:
    """Delete an entry by ID."""
    for day_offset in range(30):
        day = datetime.now().date() - timedelta(days=day_offset)
        entries = _load_day(day)
        for i, entry in enumerate(entries):
            if entry.get("id") == entry_id:
                entries.pop(i)
                _save_day(day, entries)
                return True
    return False


def get_stats() -> Dict:
    """Get overall stats about logged time."""
    today = datetime.now().date()
    first_of_month = today.replace(day=1)
    
    this_month_entries = get_entries(first_of_month, today)
    total_minutes = sum(e.get("duration_minutes", 0) for e in this_month_entries)
    
    # Categorized
    by_category = {}
    for entry in this_month_entries:
        cat = entry.get("category", "其他")
        minutes = entry.get("duration_minutes", 0)
        by_category[cat] = by_category.get(cat, 0) + minutes
    
    return {
        "total_logged_days": len(set(e.get("date", "") for e in this_month_entries)),
        "total_entries": len(this_month_entries),
        "total_hours_this_month": round(total_minutes / 60, 1),
        "by_category": {k: round(v / 60, 1) for k, v in by_category.items()},
    }


def create_backup():
    """Create a backup of all data."""
    if not os.path.exists(DATA_DIR):
        return
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup_{timestamp}")
    
    # Copy data files
    shutil.copytree(DATA_DIR, backup_path, 
                    ignore=lambda d, f: {".backups"})
    
    # Clean up old backups
    backups = sorted(os.listdir(BACKUP_DIR), reverse=True)
    for old_backup in backups[MAX_BACKUPS:]:
        old_path = os.path.join(BACKUP_DIR, old_backup)
        if os.path.isdir(old_path):
            shutil.rmtree(old_path)


def _get_day_file(day: date) -> str:
    """Get the file path for a specific day."""
    day_dir = os.path.join(DATA_DIR, day.strftime("%Y/%m"))
    os.makedirs(day_dir, exist_ok=True)
    return os.path.join(day_dir, f"{day.strftime('%d')}.json")


def _load_day(day: date) -> List[Dict]:
    """Load entries for a specific day."""
    filepath = _get_day_file(day)
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        logger.warning("Failed to load day file: %s", filepath)
        return []


def _save_day(day: date, entries: List[Dict]):
    """Save entries for a specific day."""
    filepath = _get_day_file(day)
    with open(filepath, "w") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
