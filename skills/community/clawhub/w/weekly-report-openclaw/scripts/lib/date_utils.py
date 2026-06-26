"""Date utility functions for weekly report system."""

from datetime import date, datetime, timedelta
from typing import Tuple


def get_week_range(target_date: date = None) -> Tuple[date, date]:
    """
    Get the Monday and Sunday of the week containing the target date.

    Args:
        target_date: The date to find the week range for. Defaults to today.

    Returns:
        A tuple of (monday, sunday) dates.
    """
    if target_date is None:
        target_date = date.today()

    days_since_monday = target_date.weekday()
    monday = target_date - timedelta(days=days_since_monday)
    sunday = monday + timedelta(days=6)

    return monday, sunday


def get_last_week_range() -> Tuple[date, date]:
    """
    Get the Monday and Sunday of last week.

    Returns:
        A tuple of (monday, sunday) dates for last week.
    """
    this_week_monday, _ = get_week_range()
    last_week_monday = this_week_monday - timedelta(days=7)
    last_week_sunday = last_week_monday + timedelta(days=6)
    return last_week_monday, last_week_sunday


def parse_date_input(date_input: str = None) -> Tuple[date, date]:
    """
    Parse date input and return week range.

    Supported formats:
    - None or 'today': Current week
    - 'last' or 'last week': Last week
    - 'YYYY-MM-DD': Specific date, returns its week
    - 'YYYY.MM.DD': Specific date with dots, returns its week

    Args:
        date_input: String representing the date or None for today.

    Returns:
        A tuple of (start_date, end_date) for the week.

    Raises:
        ValueError: If the date format is not recognized.
    """
    if date_input is None or date_input.lower() == "today":
        return get_week_range()

    date_input = date_input.strip().lower()

    if date_input in ("last", "last week"):
        return get_last_week_range()

    for fmt in ("%Y-%m-%d", "%Y.%m.%d", "%Y/%m/%d"):
        try:
            parsed_date = datetime.strptime(date_input, fmt).date()
            return get_week_range(parsed_date)
        except ValueError:
            continue

    raise ValueError(
        f"Unrecognized date format: '{date_input}'. "
        "Supported: 'today', 'last', 'YYYY-MM-DD', 'YYYY.MM.DD'"
    )


def format_date_for_api(d: date) -> str:
    """Format date for API requests."""
    return d.strftime("%Y-%m-%d")


def format_date_for_display(d: date) -> str:
    """Format date for display in reports."""
    return d.strftime("%Y年%m月%d日")


def get_week_number(d: date = None) -> int:
    """Get the week number of the year."""
    if d is None:
        d = date.today()
    return d.isocalendar()[1]
