from datetime import datetime, timedelta
from dateutil.parser import parse  # or use pendulum for even nicer relative parsing
import re

def resolve_relative_date(relative_expr: str, timezone: str = "Asia/Singapore", reference_time: str = None) -> str:
    """
    Takes natural language like "Wednesday", "this Wed", "next Friday", "Fri",
    "tomorrow", "day after tomorrow", "in 3 days", "this weekend", etc.
    and returns an ISO date string for the *upcoming* occurrence.
    """
    now = datetime.now() if reference_time is None else datetime.fromisoformat(reference_time)
    expr = relative_expr.lower().strip()

    # Handle common relative patterns
    if expr == "tomorrow":
        return (now + timedelta(days=1)).date().isoformat()
    
    elif expr == "day after tomorrow" or expr == "in 2 days":
        return (now + timedelta(days=2)).date().isoformat()
    
    elif re.match(r'^in (\d+) days?$', expr):
        days = int(re.match(r'^in (\d+) days?$', expr).group(1))
        return (now + timedelta(days=days)).date().isoformat()
    
    elif "this weekend" in expr or "weekend" in expr:
        # Saturday
        days_ahead = (5 - now.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return (now + timedelta(days=days_ahead)).date().isoformat()
    
    else:
        # Handle weekday expressions: "Wednesday", "next Friday", "Fri", "this Wed"
        # "next" keyword means second occurrence (skip one week)
        is_next = expr.startswith("next ")
        
        target = parse(relative_expr, fuzzy=True)  # handles "Wed", "next Friday", etc.
        
        # Adjust to future occurrence
        days_ahead = (target.weekday() - now.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7  # "this Wednesday" when today IS Wednesday → next one
        
        # If "next" specified, add another 7 days (second occurrence)
        if is_next:
            days_ahead += 7
        
        result = now + timedelta(days=days_ahead)
        return result.date().isoformat()  # "2026-03-11"