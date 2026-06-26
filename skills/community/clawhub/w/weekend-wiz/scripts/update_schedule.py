#!/usr/bin/env python3
"""Update schedule HTML with dynamic date labels and current month.

This script updates the existing schedule.html file in place:
1. Updates the page header month (#current-month)
2. Updates date labels (今天/明天/本周/未来) based on current date

Usage:
    python3 update_schedule.py <schedule_html_path>
"""

import sys
import re
from datetime import datetime, timedelta

def get_date_label(date_str, today):
    """Determine date label based on today's date.
    
    Args:
        date_str: String like "3月14日" or "3月15日"
        today: Current date
    
    Returns:
        Tuple of (css_class, label_text)
    """
    # Parse date string like "3月14日"
    match = re.match(r'(\d+)月(\d+)日', date_str)
    if not match:
        return 'upcoming', '未来'
    
    month = int(match.group(1))
    day = int(match.group(2))
    
    # Handle year boundary (assuming current year)
    year = today.year
    try:
        date = datetime(year, month, day)
    except ValueError:
        return 'upcoming', '未来'
    
    # Compare dates
    date_only = date.date()
    today_only = today.date()
    
    if date_only == today_only:
        return 'today', '今天'
    elif date_only == (today_only + timedelta(days=1)):
        return 'tomorrow', '明天'
    elif date_only < (today_only + timedelta(days=7)):
        return 'thisweek', '本周'
    else:
        return 'upcoming', '未来'

def update_schedule_html(html_path):
    """Update schedule HTML file with current date labels."""
    today = datetime.now()
    current_month = f"{today.year}年{today.month}月"
    
    # Read existing HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Update month in header
    html = re.sub(
        r'id="current-month">[^<]+</div>',
        f'id="current-month">{current_month}</div>',
        html
    )
    
    # 2. Update date labels for each date-group
    # Find all date-day patterns and update their corresponding labels
    def update_date_label(match):
        date_str = match.group(1)
        css_class, label_text = get_date_label(date_str, today)
        return f'<span class="date-day">{date_str}</span>\n        <span class="date-label {css_class}">{label_text}</span>'
    
    html = re.sub(
        r'<span class="date-day">([^<]+)</span>\s*<span class="date-label [^"]+">[^<]+</span>',
        update_date_label,
        html
    )
    
    # Write updated HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Schedule updated: {html_path}")
    print(f"📅 Current month: {current_month}")
    print(f"📝 Date labels updated based on today ({today.strftime('%Y-%m-%d')})")

def main():
    if len(sys.argv) < 2:
        print("Usage: update_schedule.py <schedule_html_path>")
        print("Example: update_schedule.py memory/schedule.html")
        sys.exit(1)
    
    html_path = sys.argv[1]
    update_schedule_html(html_path)

if __name__ == "__main__":
    main()
