"""Distance utilities for Weekend Scout.

Provides Haversine straight-line distance and a driving time heuristic
calibrated for Poland/Central Europe. No external API required.
"""

from __future__ import annotations

import datetime
from math import atan2, cos, radians, sin, sqrt


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points in kilometres.

    Args:
        lat1: Latitude of point 1 in decimal degrees.
        lon1: Longitude of point 1 in decimal degrees.
        lat2: Latitude of point 2 in decimal degrees.
        lon2: Longitude of point 2 in decimal degrees.

    Returns:
        Distance in kilometres.
    """
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def estimated_drive_minutes(distance_km: float) -> float:
    """Estimate driving time using a heuristic for Poland/Central Europe.

    Tiers:
      < 30 km  -> ~40 km/h average (urban)
      30-80 km -> ~60 km/h average (mixed)
      > 80 km  -> ~80 km/h average (highway-heavy)

    Args:
        distance_km: Straight-line distance in kilometres.

    Returns:
        Estimated driving time in minutes.
    """
    if distance_km < 30:
        return distance_km * 1.5
    elif distance_km < 80:
        return distance_km * 1.0
    else:
        return distance_km * 0.75


def format_drive_time(minutes: float) -> str:
    """Format driving minutes as a human-readable string like '1h40'.

    Args:
        minutes: Driving time in minutes.

    Returns:
        String such as '45min', '1h00', or '2h15'.
    """
    total = int(round(minutes))
    if total < 60:
        return f"{total}min"
    h = total // 60
    m = total % 60
    return f"{h}h{m:02d}"


def next_weekend_dates() -> tuple[str, str]:
    """Return ISO date strings for the next upcoming Saturday and Sunday.

    Always returns a future weekend — if today is Saturday, returns next Saturday.

    Returns:
        Tuple of (saturday_iso, sunday_iso) e.g. ('2026-03-28', '2026-03-29').
    """
    today = datetime.date.today()
    days_ahead = (5 - today.weekday()) % 7  # 5 = Saturday
    if days_ahead == 0:
        days_ahead = 7  # today is Saturday — skip to next week
    saturday = today + datetime.timedelta(days=days_ahead)
    sunday = saturday + datetime.timedelta(days=1)
    return saturday.isoformat(), sunday.isoformat()
