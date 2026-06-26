#!/usr/bin/env python3
"""
Calendar Importer — Analyzes Google Calendar for schedule patterns and lifestyle insights.
Requires Google Calendar OAuth (reuses Gmail credentials with calendar scope).
"""
import os
import sys
import json
from datetime import datetime, timezone, timedelta
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"
WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
DAYS_BACK = 90  # Analyze last N days

def get_calendar_service():
    """Initialize Google Calendar API service."""
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        print(json.dumps({"error": "Google API dependencies not installed."}))
        sys.exit(1)
    
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    
    token_paths = [
        os.path.join(WORKSPACE, "mission-control", "data", "gmail_token.json"),
        os.path.join(WORKSPACE, "email-agent", "token.json"),
    ]
    
    token_path = next((p for p in token_paths if os.path.exists(p)), None)
    if not token_path:
        print(json.dumps({"error": "No Google OAuth token found. Need calendar scope."}))
        sys.exit(1)
    
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    
    return build("calendar", "v3", credentials=creds)

def analyze_calendar(service):
    """Analyze recent calendar events for patterns."""
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=DAYS_BACK)).isoformat()
    end = now.isoformat()
    
    events_result = service.events().list(
        calendarId="primary",
        timeMin=start, timeMax=end,
        maxResults=500, singleEvents=True,
        orderBy="startTime"
    ).execute()
    
    events = events_result.get("items", [])
    
    # Analyze patterns
    event_hours = Counter()
    event_days = Counter()
    event_types = Counter()
    recurring_count = 0
    meeting_count = 0
    all_day_count = 0
    total_duration_hours = 0
    
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for event in events:
        start_time = event.get("start", {})
        
        if "dateTime" in start_time:
            dt = datetime.fromisoformat(start_time["dateTime"])
            event_hours[dt.hour] += 1
            event_days[day_names[dt.weekday()]] += 1
            
            # Estimate duration
            end_time = event.get("end", {}).get("dateTime")
            if end_time:
                end_dt = datetime.fromisoformat(end_time)
                duration = (end_dt - dt).total_seconds() / 3600
                total_duration_hours += duration
        elif "date" in start_time:
            all_day_count += 1
        
        # Count meetings (events with attendees)
        if event.get("attendees"):
            meeting_count += 1
        
        if event.get("recurringEventId"):
            recurring_count += 1
        
        # Categorize by summary keywords
        summary = event.get("summary", "").lower()
        for keyword in ["meeting", "call", "sync", "standup", "1:1"]:
            if keyword in summary:
                event_types["meetings"] += 1
                break
        for keyword in ["lunch", "dinner", "coffee", "gym", "workout", "doctor"]:
            if keyword in summary:
                event_types["personal"] += 1
                break
    
    # Synthesize
    peak_hours = [h for h, _ in event_hours.most_common(3)]
    busiest_days = [d for d, _ in event_days.most_common(3)]
    avg_events_per_week = len(events) / max(DAYS_BACK / 7, 1)
    avg_duration = total_duration_hours / max(len(events) - all_day_count, 1)
    
    # Determine lifestyle patterns
    patterns = []
    if avg_events_per_week > 15:
        patterns.append("Very busy schedule — heavily calendared")
    elif avg_events_per_week > 7:
        patterns.append("Moderately scheduled")
    else:
        patterns.append("Light calendar — flexible schedule")
    
    if meeting_count / max(len(events), 1) > 0.5:
        patterns.append("Meeting-heavy — lots of collaboration")
    
    weekend_events = event_days.get("Saturday", 0) + event_days.get("Sunday", 0)
    if weekend_events / max(sum(event_days.values()), 1) > 0.2:
        patterns.append("Active on weekends")
    else:
        patterns.append("Weekends mostly free")
    
    return {
        "source": "calendar",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": {
            "work_patterns": "; ".join(patterns),
            "schedule_density": f"{avg_events_per_week:.1f} events/week avg",
            "peak_hours": [f"{h}:00" for h in peak_hours],
            "busiest_days": busiest_days,
            "meeting_ratio": f"{meeting_count}/{len(events)} events are meetings",
            "avg_event_duration": f"{avg_duration:.1f} hours",
            "interests": list(event_types.keys()),
        },
        "confidence": min(len(events) / 100, 1.0),
        "items_processed": len(events),
    }

if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)
    
    try:
        service = get_calendar_service()
        result = analyze_calendar(service)
        
        output_path = os.path.join(IMPORT_DIR, "calendar.json")
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
