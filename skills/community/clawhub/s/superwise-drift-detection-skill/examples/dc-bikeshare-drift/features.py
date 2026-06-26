"""
Shared categorical feature engineering for DC Bikeshare drift detection.
All features are strings so every column supports JSD drift detection in Superwise.
"""


def station_size_bucket(slots: int) -> str:
    if slots < 10:
        return "small"
    elif slots < 20:
        return "medium"
    return "large"


def hour_bucket(hour: int) -> str:
    if 0 <= hour < 6:
        return "night"
    elif 6 <= hour < 10:
        return "morning_rush"
    elif 10 <= hour < 16:
        return "midday"
    elif 16 <= hour < 20:
        return "evening_rush"
    return "evening"


def day_type(weekday: int) -> str:
    return "weekend" if weekday >= 5 else "weekday"


def season(month: int) -> str:
    if month in (3, 4, 5):
        return "spring"
    elif month in (6, 7, 8):
        return "summer"
    elif month in (9, 10, 11):
        return "fall"
    return "winter"


def availability_bucket(bikes: int, total_slots: int) -> str:
    if total_slots == 0:
        return "unknown"
    pct = bikes / total_slots
    if pct < 0.2:
        return "empty"
    elif pct < 0.4:
        return "low"
    elif pct < 0.7:
        return "medium"
    return "high"


FEATURE_COLS = ["station_size_bucket", "has_ebikes", "hour_bucket", "day_type", "season"]
TARGET_COL = "availability_bucket"
