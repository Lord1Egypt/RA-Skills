CITIES = {
    "New York": {
        "lat": 40.7128, "lon": -74.0060,
        "wunderground": "ny/new-york",
        "timezone": "America/New_York"
    },
    "New York City": {
        "lat": 40.7128, "lon": -74.0060,
        "wunderground": "ny/new-york",
        "timezone": "America/New_York"
    },
    "NYC": {
        "lat": 40.7128, "lon": -74.0060,
        "wunderground": "ny/new-york",
        "timezone": "America/New_York"
    },
    "Los Angeles": {
        "lat": 34.0522, "lon": -118.2437,
        "wunderground": "ca/los-angeles",
        "timezone": "America/Los_Angeles"
    },
    "Chicago": {
        "lat": 41.8781, "lon": -87.6298,
        "wunderground": "il/chicago",
        "timezone": "America/Chicago"
    },
    "Miami": {
        "lat": 25.7617, "lon": -80.1918,
        "wunderground": "fl/miami",
        "timezone": "America/New_York"
    },
    "Houston": {
        "lat": 29.7604, "lon": -95.3698,
        "wunderground": "tx/houston",
        "timezone": "America/Chicago"
    },
    "Phoenix": {
        "lat": 33.4484, "lon": -112.0740,
        "wunderground": "az/phoenix",
        "timezone": "America/Phoenix"
    },
    "Philadelphia": {
        "lat": 39.9526, "lon": -75.1652,
        "wunderground": "pa/philadelphia",
        "timezone": "America/New_York"
    },
    "San Francisco": {
        "lat": 37.7749, "lon": -122.4194,
        "wunderground": "ca/san-francisco",
        "timezone": "America/Los_Angeles"
    },
    "Seattle": {
        "lat": 47.6062, "lon": -122.3321,
        "wunderground": "wa/seattle",
        "timezone": "America/Los_Angeles"
    },
    "Denver": {
        "lat": 39.7392, "lon": -104.9903,
        "wunderground": "co/denver",
        "timezone": "America/Denver"
    },
    "Boston": {
        "lat": 42.3601, "lon": -71.0589,
        "wunderground": "ma/boston",
        "timezone": "America/New_York"
    },
    "Atlanta": {
        "lat": 33.7490, "lon": -84.3880,
        "wunderground": "ga/atlanta",
        "timezone": "America/New_York"
    },
    "Dallas": {
        "lat": 32.7767, "lon": -96.7970,
        "wunderground": "tx/dallas",
        "timezone": "America/Chicago"
    },
    "Minneapolis": {
        "lat": 44.9778, "lon": -93.2650,
        "wunderground": "mn/minneapolis",
        "timezone": "America/Chicago"
    },
    "Las Vegas": {
        "lat": 36.1699, "lon": -115.1398,
        "wunderground": "nv/las-vegas",
        "timezone": "America/Los_Angeles"
    },
    "Detroit": {
        "lat": 42.3314, "lon": -83.0458,
        "wunderground": "mi/detroit",
        "timezone": "America/Detroit"
    },
    "Portland": {
        "lat": 45.5051, "lon": -122.6750,
        "wunderground": "or/portland",
        "timezone": "America/Los_Angeles"
    },
    "San Antonio": {
        "lat": 29.4241, "lon": -98.4936,
        "wunderground": "tx/san-antonio",
        "timezone": "America/Chicago"
    },
    "San Diego": {
        "lat": 32.7157, "lon": -117.1611,
        "wunderground": "ca/san-diego",
        "timezone": "America/Los_Angeles"
    },
    "Milan": {
        "lat": 45.4654, "lon": 9.1859,
        "wunderground": "italy/milan",
        "timezone": "Europe/Rome",
        "unit": "C"
    },
    "Madrid": {
        "lat": 40.4168, "lon": -3.7038,
        "wunderground": "spain/madrid",
        "timezone": "Europe/Madrid",
        "unit": "C"
    },
    "Tel Aviv": {
        "lat": 32.0853, "lon": 34.7818,
        "wunderground": "israel/tel-aviv",
        "timezone": "Asia/Jerusalem",
        "unit": "C"
    },
    "London": {
        "lat": 51.5074, "lon": -0.1278,
        "wunderground": "england/london",
        "timezone": "Europe/London",
        "unit": "C"
    },
    "Paris": {
        "lat": 48.8566, "lon": 2.3522,
        "wunderground": "france/paris",
        "timezone": "Europe/Paris",
        "unit": "C"
    },
    "Berlin": {
        "lat": 52.5200, "lon": 13.4050,
        "wunderground": "germany/berlin",
        "timezone": "Europe/Berlin",
        "unit": "C"
    },
    "Tokyo": {
        "lat": 35.6762, "lon": 139.6503,
        "wunderground": "japan/tokyo",
        "timezone": "Asia/Tokyo",
        "unit": "C"
    },
}


def resolve_city(city_name: str) -> dict:
    """Returns city data dict or raises ValueError if not found."""
    city_lower = city_name.lower().strip()
    for key, data in CITIES.items():
        if key.lower() == city_lower:
            return data
    for key, data in CITIES.items():
        if key.lower() in city_lower or city_lower in key.lower():
            return data
    raise ValueError(
        f"City '{city_name}' not found in city map. "
        f"Available: {', '.join(CITIES.keys())}. Add it to city_map.py."
    )


def celsius_to_fahrenheit(c: float) -> int:
    return int(round((c * 9 / 5) + 32))
