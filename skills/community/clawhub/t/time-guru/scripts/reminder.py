"""
Reminder system for time-guru.
Generates daily/weekly reminders based on activity patterns.
"""
import logging
from typing import Optional
from datetime import datetime, date, timedelta

import store as time_logger

logger = logging.getLogger(__name__)


def check_daily_reminder() -> Optional[str]:
    """
    Check if a daily reminder should be sent.
    Returns a message string if reminder is needed, None otherwise.
    """
    now = datetime.now()
    
    # Evening reminder (after 21:00, if few entries recorded today)
    if now.hour >= 21:
        today_entries = time_store.get_today_entries()
        if len(today_entries) < 2:
            daily_total = time_store.get_day_total_minutes(now.date())
            if daily_total < 120:  # Less than 2 hours logged
                return ("🌙 Evening check-in: You've logged "
                       f"{daily_total // 60}h{daily_total % 60}m today. "
                       "How did you spend the rest of your time?")
    
    return None


def check_weekly_reminder() -> Optional[str]:
    """
    Check if a weekly report should be generated.
    Returns a message if it's time for a review.
    """
    now = datetime.now()
    
    # Friday afternoon: preview weekly summary
    if now.weekday() == 4 and 16 <= now.hour <= 18:
        week_start = now.date() - timedelta(days=now.weekday())
        entries = time_store.get_entries(week_start, now.date())
        
        if entries:
            total_minutes = sum(e.get("duration_minutes", 0) for e in entries)
            hours = total_minutes / 60
            return (f"📊 It's Friday! This week you've logged "
                   f"{hours:.1f}h so far. "
                   "Run `time-guru report --period this_week` for the full report.")
    
    return None


def check_inactivity_reminder() -> Optional[str]:
    """
    Check if the user hasn't logged time for a while.
    """
    today = date.today()
    
    # Check if yesterday had any entries
    yesterday = today - timedelta(days=1)
    yesterday_minutes = time_store.get_day_total_minutes(yesterday)
    
    if yesterday_minutes == 0:
        today_minutes = time_store.get_day_total_minutes(today)
        if today_minutes == 0 and datetime.now().hour >= 12:
            return ("⏰ You haven't logged any time yet today or yesterday. "
                   "Quick: `time-guru log '刚才做了什么'`")
    
    # Check if today is blank but it's past noon
    now = datetime.now()
    if now.hour >= 12:
        today_minutes = time_store.get_day_total_minutes(today)
        if today_minutes == 0:
            return ("⏰ Half the day has passed and no time logged yet! "
                   "Quick log: what have you been working on?")
    
    return None


def generate_morning_prompt() -> Optional[str]:
    """
    Generate a morning planning prompt.
    """
    now = datetime.now()
    if 7 <= now.hour <= 10:
        yesterday = now.date() - timedelta(days=1)
        yesterday_minutes = time_store.get_day_total_minutes(yesterday)
        
        if yesterday_minutes > 0:
            yesterday_hours = yesterday_minutes / 60
            return (f"🌅 Good morning! Yesterday: {yesterday_hours:.1f}h logged. "
                   "What's your plan for today?")
        else:
            return ("🌅 Good morning! Ready to track your day? "
                   "Just say what you do when you do it.")
    
    return None
