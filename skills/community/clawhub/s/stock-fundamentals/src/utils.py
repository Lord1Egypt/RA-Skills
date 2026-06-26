from datetime import datetime


def format_number(num, decimals=2):
    """Format a number with commas and specified decimals."""
    if num is None:
        return "N/A"
    try:
        return f"{float(num):,.{decimals}f}"
    except (TypeError, ValueError):
        return "N/A"


def normalize_ratio_percent_value(num):
    """Normalize ratio-like metrics into percentage units."""
    try:
        value = float(num)
    except (TypeError, ValueError):
        return None

    if abs(value) <= 10:
        value *= 100

    return value


def normalize_yield_percent_value(num):
    """Normalize dividend yield into percentage units."""
    try:
        value = float(num)
    except (TypeError, ValueError):
        return None

    if abs(value) <= 0.2:
        value *= 100

    return value


def format_percent(num, decimals=1):
    """Format a ratio-like number as a percentage."""
    value = normalize_ratio_percent_value(num)
    if value is None:
        return "N/A"
    return f"{value:,.{decimals}f}%"


def format_yield_percent(num, decimals=1):
    """Format dividend yield values as percentages."""
    value = normalize_yield_percent_value(num)
    if value is None:
        return "N/A"
    return f"{value:,.{decimals}f}%"


def format_large_number(num):
    """Format large numbers into M/B/T units."""
    if num is None:
        return "N/A"

    try:
        value = float(num)
    except (TypeError, ValueError):
        return "N/A"

    abs_value = abs(value)
    if abs_value >= 1_000_000_000_000:
        return f"${format_number(value / 1_000_000_000_000, 2)}T"
    if abs_value >= 1_000_000_000:
        return f"${format_number(value / 1_000_000_000, 2)}B"
    if abs_value >= 1_000_000:
        return f"${format_number(value / 1_000_000, 2)}M"
    return f"${format_number(value, 2)}"


def format_price_value(num):
    """Format a price-like numeric value with a dollar sign."""
    if num is None:
        return "N/A"
    return f"${format_number(num)}"


def get_info_value(info: dict, *keys):
    """Return the first non-empty value from a set of possible keys."""
    for key in keys:
        value = info.get(key)
        if value is not None and value != "":
            return value
    return None


def extract_statement_value(statement, labels: list[str]):
    """Extract the latest non-null value from a financial statement row."""
    if statement is None or getattr(statement, "empty", True):
        return None

    for label in labels:
        try:
            if label not in statement.index:
                continue
            row = statement.loc[label]
            if hasattr(row, "dropna"):
                values = row.dropna()
                if not values.empty:
                    return float(values.iloc[0])
            if row is not None:
                return float(row)
        except (KeyError, TypeError, ValueError):
            continue

    return None


def normalize_recommendation(value) -> str:
    """Normalize recommendation text into a display-friendly label."""
    if value is None:
        return "N/A"
    text = str(value).replace("_", " ").replace("-", " ").strip()
    if not text:
        return "N/A"
    return text.title()


def format_event_date(event_date) -> str:
    """Format an event date value into a GMT timestamp string."""
    if event_date is None:
        return "N/A"
    if isinstance(event_date, (int, float)):
        return datetime.utcfromtimestamp(event_date).strftime("%Y-%m-%d %H:%M:%S GMT")
    if isinstance(event_date, datetime):
        return event_date.strftime("%Y-%m-%d %H:%M:%S GMT")

    value = str(event_date)
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S GMT")
    except ValueError:
        return value
