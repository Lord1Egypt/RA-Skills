"""
Productivity analyzer for time-guru.
Analyzes peak hours, interruptions, deep work, and trends.
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta, date
from collections import defaultdict

import store

logger = logging.getLogger(__name__)

DEEP_WORK_THRESHOLD = 60  # minutes


def analyze_productivity(period: str = "this_week",
                          aspects: Optional[list] = None) -> Dict:
    """
    Analyze time tracking data for productivity insights.
    
    Args:
        period: Analysis period ('this_week', 'last_week', 'this_month', etc.).
        aspects: Specific aspects to analyze ('peak_hours', 'interruptions', 
                 'deep_work', 'trends', 'all').
        
    Returns:
        Analysis dict with findings and recommendations.
    """
    today = datetime.now().date()
    
    if period == "this_week":
        start = today - timedelta(days=today.weekday())
        end = today
    elif period == "last_week":
        start = today - timedelta(days=today.weekday() + 7)
        end = start + timedelta(days=6)
    elif period == "this_month":
        start = today.replace(day=1)
        end = today
    else:
        start = today - timedelta(days=7)
        end = today
    
    entries = store.get_entries(start, end)
    
    if not entries:
        return {
            "peak_hours": [],
            "interruption_pattern": None,
            "deep_work_hours": 0,
            "trends": None,
            "recommendations": ["Not enough data to analyze. Start logging your time!"],
        }
    
    if aspects is None:
        aspects = ["all"]
    
    analyze_all = "all" in aspects
    
    result = {}
    
    # Peak hours analysis
    if analyze_all or "peak_hours" in aspects:
        result["peak_hours"] = _analyze_peak_hours(entries)
    
    # Interruption pattern analysis
    if analyze_all or "interruptions" in aspects:
        result["interruption_pattern"] = _analyze_interruptions(entries)
    
    # Deep work analysis
    if analyze_all or "deep_work" in aspects:
        result["deep_work"] = _analyze_deep_work(entries)
    
    # Trends
    if analyze_all or "trends" in aspects:
        result["trends"] = _analyze_trends(entries, start, end)
    
    # Recommendations
    result["recommendations"] = _generate_recommendations(result, entries)
    
    return result


def _analyze_peak_hours(entries: list) -> list:
    """Find peak productivity hours based on activity density."""
    hourly_density = defaultdict(int)
    hourly_count = defaultdict(int)
    
    for e in entries:
        start_time = e.get("start", "")
        duration = e.get("duration_minutes", 0)
        
        try:
            hour = int(start_time.split(":")[0])
            hourly_density[hour] += duration
            hourly_count[hour] += 1
        except (ValueError, IndexError):
            continue
    
    if not hourly_density:
        return []
    
    # Sort by total duration descending
    sorted_hours = sorted(hourly_density.items(), key=lambda x: -x[1])
    
    result = []
    for hour, total_minutes in sorted_hours[:5]:
        count = hourly_count.get(hour, 0)
        result.append({
            "hour_range": f"{hour:02d}:00-{hour + 1:02d}:00",
            "total_minutes": total_minutes,
            "total_hours": round(total_minutes / 60, 1),
            "session_count": count,
            "avg_minutes_per_session": round(total_minutes / count, 1) if count > 0 else 0,
        })
    
    return result


def _analyze_interruptions(entries: list) -> Dict:
    """Analyze task switching and interruption patterns."""
    # Group entries by day
    daily_entries = defaultdict(list)
    for e in entries:
        day = e.get("date", "")
        daily_entries[day].append(e)
    
    total_switches = 0
    total_days = len(daily_entries)
    focus_durations = []
    
    for day, day_entries in daily_entries.items():
        sorted_entries = sorted(day_entries, key=lambda e: e.get("start", ""))
        
        # Count category switches
        prev_category = None
        switches = 0
        for e in sorted_entries:
            cat = e.get("category", "")
            if prev_category and cat != prev_category:
                switches += 1
            prev_category = cat
        
        total_switches += switches
        
        # Track focus durations (periods without switching)
        for e in sorted_entries:
            dur = e.get("duration_minutes", 0)
            if dur >= 25:  # Sessions >= 25 min are focus blocks
                focus_durations.append(dur)
    
    avg_switches = round(total_switches / total_days, 1) if total_days > 0 else 0
    avg_focus = round(sum(focus_durations) / len(focus_durations), 1) if focus_durations else 0
    
    # Assessment
    if avg_switches <= 3:
        assessment = "Good — minimal task switching, deep focus maintained"
    elif avg_switches <= 6:
        assessment = "Moderate — some switching, consider batching similar tasks"
    else:
        assessment = "High — frequent context switches reducing productivity"
    
    return {
        "avg_focus_duration_minutes": avg_focus,
        "task_switches_per_day": avg_switches,
        "assessment": assessment,
    }


def _analyze_deep_work(entries: list) -> Dict:
    """Analyze deep work sessions (continuous single-category work ≥ 60 min)."""
    deep_work_sessions = []
    
    for e in entries:
        duration = e.get("duration_minutes", 0)
        if duration >= DEEP_WORK_THRESHOLD:
            deep_work_sessions.append(e)
    
    total_deep_minutes = sum(e.get("duration_minutes", 0) for e in deep_work_sessions)
    
    # By category
    deep_by_category = defaultdict(int)
    for e in deep_work_sessions:
        cat = e.get("category", "其他")
        deep_by_category[cat] += e.get("duration_minutes", 0)
    
    # Daily average
    unique_days = set(e.get("date", "") for e in entries)
    num_days = len(unique_days) if unique_days else 1
    
    # Categories that had deep work
    category_breakdown = []
    for cat, minutes in sorted(deep_by_category.items(), key=lambda x: -x[1]):
        category_breakdown.append({
            "category": cat,
            "deep_work_hours": round(minutes / 60, 1),
        })
    
    return {
        "total_sessions": len(deep_work_sessions),
        "total_deep_work_minutes": total_deep_minutes,
        "total_deep_work_hours": round(total_deep_minutes / 60, 1),
        "daily_avg_deep_work_hours": round(total_deep_minutes / 60 / num_days, 1),
        "by_category": category_breakdown,
    }


def _analyze_trends(entries: list, start: date, end: date) -> Dict:
    """Analyze week-over-week trends."""
    # Group by week
    weekly_minutes = defaultdict(int)
    for e in entries:
        day_str = e.get("date", "")
        try:
            day = date.fromisoformat(day_str)
            week_start = day - timedelta(days=day.weekday())
            weekly_minutes[week_start.isoformat()] += e.get("duration_minutes", 0)
        except (ValueError, TypeError):
            continue
    
    weeks = sorted(weekly_minutes.keys())
    
    week_over_week = "N/A"
    if len(weeks) >= 2:
        current = weekly_minutes[weeks[-1]]
        previous = weekly_minutes[weeks[-2]]
        if previous > 0:
            change = ((current - previous) / previous) * 100
            direction = "↑" if change > 0 else "↓"
            week_over_week = f"{direction} {abs(change):.0f}% ({round(current/60,1)}h vs {round(previous/60,1)}h)"
    
    # Most productive day of week
    day_total = defaultdict(int)
    for e in entries:
        day_str = e.get("date", "")
        try:
            day = date.fromisoformat(day_str)
            day_total[day.strftime("%A")] += e.get("duration_minutes", 0)
        except (ValueError, TypeError):
            continue
    
    most_productive_day = max(day_total, key=day_total.get) if day_total else "Unknown"
    
    return {
        "week_over_week_change": week_over_week,
        "most_productive_day": most_productive_day,
        "weekly_hours": {w: round(m / 60, 1) for w, m in weekly_minutes.items()},
    }


def _generate_recommendations(analysis: Dict, entries: list) -> list:
    """Generate actionable recommendations based on analysis."""
    recommendations = []
    
    interruption = analysis.get("interruption_pattern")
    if interruption:
        switches = interruption.get("task_switches_per_day", 0)
        if switches > 5:
            recommendations.append("High task switching detected. Try time-blocking: "
                                    "focus on one type of task per 90-minute block.")
        
        avg_focus = interruption.get("avg_focus_duration_minutes", 0)
        if avg_focus < 30:
            recommendations.append("Short focus sessions. Consider the Pomodoro Technique "
                                    "(25 min work + 5 min break) to build focus stamina.")
    
    deep_work = analysis.get("deep_work", {})
    if deep_work:
        daily_deep = deep_work.get("daily_avg_deep_work_hours", 0)
        if daily_deep < 2:
            recommendations.append("Less than 2 hours of deep work daily. "
                                    "Book 2-3 hour blocks in your morning for focused work.")
    
    peak = analysis.get("peak_hours", [])
    if peak:
        best_hour = peak[0]["hour_range"] if peak else ""
        if best_hour:
            recommendations.append(f"Your peak hours are {best_hour}. "
                                    f"Schedule complex tasks during this window.")
    
    if not recommendations:
        recommendations.append("Good productivity patterns. Keep maintaining your routine!")
    
    return recommendations
