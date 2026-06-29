"""
Data importer for time-guru.
Imports from external sources (calendar, GitHub, Jira).
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def import_ical(ical_text: str) -> List[Dict]:
    """
    Parse iCal/ICS text and convert to time entries.
    
    Args:
        ical_text: iCal format calendar data.
        
    Returns:
        List of time entry dicts.
    """
    import re
    entries = []
    
    # Simple ICS parser
    events = re.split(r'BEGIN:VEVENT', ical_text)
    
    for event in events[1:]:  # Skip the prelude
        summary_match = re.search(r'SUMMARY:(.+?)\n', event)
        dtstart_match = re.search(r'DTSTART(?:;.*?)?:(\d{8}T\d{6})', event)
        dtend_match = re.search(r'DTEND(?:;.*?)?:(\d{8}T\d{6})', event)
        
        if not (summary_match and dtstart_match and dtend_match):
            continue
        
        try:
            start = datetime.strptime(dtstart_match.group(1), "%Y%m%dT%H%M%S")
            end = datetime.strptime(dtend_match.group(1), "%Y%m%dT%H%M%S")
            duration_minutes = int((end - start).total_seconds() / 60)
            
            entries.append({
                "description": summary_match.group(1).strip(),
                "start": start.strftime("%H:%M"),
                "end": end.strftime("%H:%M"),
                "duration_minutes": duration_minutes,
                "started_at": start.isoformat(),
                "ended_at": end.isoformat(),
                "source": "ical",
                "date": start.strftime("%Y%m%d"),
            })
        except (ValueError, TypeError):
            continue
    
    return entries


def import_github_commits(commits_data: list) -> List[Dict]:
    """
    Parse GitHub commit data and estimate time spent.
    
    Args:
        commits_data: List of GitHub commit dicts.
        
    Returns:
        List of time entry dicts.
    """
    from collections import defaultdict
    import re
    
    # Group commits by day
    daily_commits = defaultdict(list)
    for commit in commits_data:
        date_str = commit.get("commit", {}).get("committer", {}).get("date", "")[:10]
        if date_str:
            daily_commits[date_str].append(commit)
    
    entries = []
    for date_str, commits in daily_commits.items():
        # Estimate: 10 min per commit, 30 min overhead
        total_minutes = len(commits) * 10 + 30
        
        # Get repo and message summary
        repo_name = commits[0].get("repository", {}).get("full_name", commits[0].get("url", "").split("/")[3] + "/" + commits[0].get("url", "").split("/")[4]) if commits[0].get("url") else "unknown"
        
        messages = []
        for c in commits[:3]:
            msg = c.get("commit", {}).get("message", "").split("\n")[0]
            if msg:
                messages.append(msg)
        
        entries.append({
            "description": f"GitHub: {'; '.join(messages)}",
            "duration_minutes": total_minutes,
            "project": repo_name,
            "category": "开发",
            "date": date_str,
            "source": "github",
        })
    
    return entries


def import_jira_worklog(worklog_data: list) -> List[Dict]:
    """
    Parse Jira worklog data.
    
    Args:
        worklog_data: List of Jira worklog entries.
        
    Returns:
        List of time entry dicts.
    """
    entries = []
    for log in worklog_data:
        issue_key = log.get("issueKey", "")
        description = log.get("comment", "")
        time_spent_seconds = log.get("timeSpentSeconds", 0)
        
        if time_spent_seconds <= 0:
            continue
        
        started = log.get("started", "")
        if started:
            try:
                start_dt = datetime.fromisoformat(started.replace("Z", "+00:00"))
                start_str = start_dt.strftime("%H:%M")
            except ValueError:
                start_str = ""
        else:
            start_str = ""
        
        entries.append({
            "description": f"[{issue_key}] {description[:100]}" if issue_key else description,
            "start": start_str,
            "duration_minutes": time_spent_seconds // 60,
            "project": issue_key.split("-")[0] if "-" in issue_key else "",
            "category": "开发",
            "source": "jira",
        })
    
    return entries
