"""
Report generator for time-guru.
Generates daily, weekly, monthly, and custom range reports.
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta, date
from collections import defaultdict

import store

logger = logging.getLogger(__name__)


def generate_report(period: str = "today",
                    date_from: Optional[str] = None,
                    date_to: Optional[str] = None,
                    group_by: str = "category",
                    include_billing: bool = False,
                    hourly_rate: float = 0) -> Dict:
    """
    Generate a time report for a given period.
    
    Args:
        period: Predefined period ('today', 'yesterday', 'this_week', etc.)
        date_from: Custom start date (YYYY-MM-DD).
        date_to: Custom end date (YYYY-MM-DD).
        group_by: Grouping method ('category', 'project', 'day', 'week').
        include_billing: Include billing information.
        hourly_rate: Default hourly rate for billing.
        
    Returns:
        Report dict with summary, breakdowns, and optional billing info.
    """
    today = datetime.now().date()
    
    # Determine date range
    if period == "today":
        start = end = today
    elif period == "yesterday":
        start = end = today - timedelta(days=1)
    elif period == "this_week":
        start = today - timedelta(days=today.weekday())
        end = today
    elif period == "last_week":
        start = today - timedelta(days=today.weekday() + 7)
        end = start + timedelta(days=6)
    elif period == "this_month":
        start = today.replace(day=1)
        end = today
    elif period == "last_month":
        first_this = today.replace(day=1)
        start = (first_this - timedelta(days=1)).replace(day=1)
        end = first_this - timedelta(days=1)
    elif period == "custom" and date_from and date_to:
        start = date.fromisoformat(date_from)
        end = date.fromisoformat(date_to)
    else:
        start = end = today
    
    # Get entries
    entries = store.get_entries(start, end)
    
    if not entries:
        return {
            "period": period,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "total_hours": 0,
            "by_category": [],
            "by_project": [],
            "daily_breakdown": [],
            "raw_text": f"📊 {period.capitalize()} Report ({start} to {end})\n\nNo entries found for this period.",
            "empty": True,
        }
    
    # Calculate totals
    total_minutes = sum(e.get("duration_minutes", 0) for e in entries)
    total_hours = round(total_minutes / 60, 1)
    
    billable_minutes = sum(e.get("duration_minutes", 0) for e in entries if e.get("billable"))
    billable_hours = round(billable_minutes / 60, 1)
    billable_amount = billable_hours * hourly_rate
    
    # Group by category
    by_category = _group_by(entries, "category")
    category_lines = []
    for cat, minutes in sorted(by_category.items(), key=lambda x: -x[1]):
        hours = round(minutes / 60, 1)
        pct = round(minutes / total_minutes * 100, 1) if total_minutes > 0 else 0
        bar_len = int(pct / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        category_lines.append({
            "category": cat,
            "hours": hours,
            "percentage": pct,
            "bar": bar,
            "minutes": minutes,
        })
    
    # Group by project
    by_project = _group_by(entries, "project")
    project_lines = []
    for proj, minutes in sorted(by_project.items(), key=lambda x: -x[1]):
        hours = round(minutes / 60, 1)
        billable_min = sum(
            e.get("duration_minutes", 0) for e in entries
            if e.get("project") == proj and e.get("billable")
        )
        project_lines.append({
            "project": proj if proj else "(No Project)",
            "hours": hours,
            "billable_hours": round(billable_min / 60, 1),
            "minutes": minutes,
        })
    
    # Daily breakdown
    day_groups = defaultdict(list)
    for e in entries:
        day = e.get("date", e.get("created_at", "")[:10])
        day_groups[day].append(e)
    
    daily_lines = []
    for day_str in sorted(day_groups.keys()):
        day_entries = day_groups[day_str]
        day_minutes = sum(e.get("duration_minutes", 0) for e in day_entries)
        daily_lines.append({
            "date": day_str,
            "total_hours": round(day_minutes / 60, 1),
            "entries": sorted(day_entries, key=lambda e: e.get("start", "")),
        })
    
    # Build raw text
    raw_text = _build_report_text(period, start, end, total_hours, billable_hours,
                                   billable_amount, category_lines, daily_lines, include_billing)
    
    return {
        "period": period,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "total_hours": total_hours,
        "total_billable_hours": billable_hours,
        "billable_amount": billable_amount if include_billing else None,
        "by_category": category_lines,
        "by_project": project_lines,
        "daily_breakdown": daily_lines,
        "raw_text": raw_text,
        "empty": False,
    }


def _group_by(entries: list, key: str) -> dict:
    """Group entries by a key and sum durations."""
    groups = defaultdict(int)
    for e in entries:
        group_key = e.get(key, "其他") if e.get(key) else "其他"
        groups[group_key] += e.get("duration_minutes", 0)
    return dict(groups)


def _build_report_text(period, start, end, total_hours, billable_hours,
                       billable_amount, category_lines, daily_lines, include_billing) -> str:
    """Build the human-readable report text."""
    period_names = {
        "today": "Today", "yesterday": "Yesterday", "this_week": "This Week",
        "last_week": "Last Week", "this_month": "This Month", "last_month": "Last Month",
    }
    period_name = period_names.get(period, f"{start} ~ {end}")
    
    lines = [
        f"📊 {period_name} Time Report",
        "=" * 40,
        f"⏱  Total: {total_hours}h",
        "",
    ]
    
    if category_lines:
        lines.append("By Category:")
        for cat in category_lines:
            pct_str = f"({cat['percentage']}%)" if cat['percentage'] > 0 else ""
            lines.append(f"  {cat['category']:12s} {cat['bar']} {cat['hours']}h {pct_str}")
        lines.append("")
    
    if include_billing and billable_amount > 0:
        lines.append(f"💰 Billable: {billable_hours}h × ¥{billable_amount / billable_hours if billable_hours else 0:.0f}/h = ¥{billable_amount:,.0f}" if billable_hours else "")
        lines.append("")
    
    if daily_lines:
        lines.append("Daily Timeline:")
        for day in daily_lines:
            lines.append(f"  {day['date']}: {day['total_hours']}h")
        lines.append("")
    
    return "\n".join(lines)


def format_billing_report(period: str, hourly_rate: float, entries: list) -> str:
    """Format a billing report."""
    # Group by project
    project_groups = defaultdict(lambda: {"minutes": 0, "billable_minutes": 0})
    
    for e in entries:
        proj = e.get("project", "No Project")
        project_groups[proj]["minutes"] += e.get("duration_minutes", 0)
        if e.get("billable"):
            project_groups[proj]["billable_minutes"] += e.get("duration_minutes", 0)
    
    lines = [f"💰 Billing Report ({period})", "=" * 40]
    total_billable = 0
    
    for proj, data in sorted(project_groups.items(), key=lambda x: -x[1]["minutes"]):
        hours = data["minutes"] / 60
        billable_hours = data["billable_minutes"] / 60
        amount = billable_hours * hourly_rate
        total_billable += amount
        
        lines.append(f"\n{proj}:")
        lines.append(f"  Total: {hours:.1f}h | Billable: {billable_hours:.1f}h")
        if billable_hours > 0:
            lines.append(f"  Amount: ¥{amount:,.0f}")
    
    lines.extend([
        "",
        "─" * 40,
        f"Total Billable: ¥{total_billable:,.0f}",
    ])
    
    return "\n".join(lines)
