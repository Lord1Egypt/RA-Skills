"""City/airport normalization for Zim.

Maps common city names and aliases to IATA airport codes.
Case-insensitive with alias support.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# City → IATA mapping (top 100+ cities)
# ---------------------------------------------------------------------------

_CITY_TO_IATA: dict[str, str] = {
    # North America
    "new york": "JFK",
    "nyc": "JFK",
    "manhattan": "JFK",
    "newark": "EWR",
    "los angeles": "LAX",
    "la": "LAX",
    "l.a.": "LAX",
    "chicago": "ORD",
    "san francisco": "SFO",
    "sf": "SFO",
    "miami": "MIA",
    "dallas": "DFW",
    "houston": "IAH",
    "atlanta": "ATL",
    "boston": "BOS",
    "seattle": "SEA",
    "denver": "DEN",
    "washington": "IAD",
    "dc": "IAD",
    "washington dc": "IAD",
    "philadelphia": "PHL",
    "phoenix": "PHX",
    "las vegas": "LAS",
    "vegas": "LAS",
    "detroit": "DTW",
    "minneapolis": "MSP",
    "portland": "PDX",
    "austin": "AUS",
    "san diego": "SAN",
    "orlando": "MCO",
    "charlotte": "CLT",
    "salt lake city": "SLC",
    "nashville": "BNA",
    "toronto": "YYZ",
    "vancouver": "YVR",
    "montreal": "YUL",
    "mexico city": "MEX",
    "cancun": "CUN",
    "honolulu": "HNL",
    "hawaii": "HNL",

    # Europe
    "london": "LHR",
    "heathrow": "LHR",
    "gatwick": "LGW",
    "paris": "CDG",
    "amsterdam": "AMS",
    "frankfurt": "FRA",
    "munich": "MUC",
    "berlin": "BER",
    "zurich": "ZRH",
    "geneva": "GVA",
    "vienna": "VIE",
    "brussels": "BRU",
    "madrid": "MAD",
    "barcelona": "BCN",
    "lisbon": "LIS",
    "rome": "FCO",
    "milan": "MXP",
    "copenhagen": "CPH",
    "stockholm": "ARN",
    "gothenburg": "GOT",
    "malmö": "MMX",
    "malmo": "MMX",
    "copenhagen": "CPH",
    "oslo": "OSL",
    "helsinki": "HEL",
    "reykjavik": "KEF",
    "ibiza": "IBZ",
    "mallorca": "PMI",
    "majorca": "PMI",
    "palma": "PMI",
    "tenerife": "TFS",
    "malaga": "AGP",
    "alicante": "ALC",
    "nice": "NCE",
    "mykonos": "JMK",
    "santorini": "JTR",
    "dubrovnik": "DBV",
    "split": "SPU",
    "bali": "DPS",
    "phuket": "HKT",
    "cancun": "CUN",
    "maldives": "MLE",
    "oslo": "OSL",
    "helsinki": "HEL",
    "dublin": "DUB",
    "edinburgh": "EDI",
    "manchester": "MAN",
    "athens": "ATH",
    "istanbul": "IST",
    "moscow": "SVO",
    "warsaw": "WAW",
    "prague": "PRG",
    "budapest": "BUD",
    "bucharest": "OTP",

    # Middle East
    "dubai": "DXB",
    "abu dhabi": "AUH",
    "doha": "DOH",
    "riyadh": "RUH",
    "jeddah": "JED",
    "muscat": "MCT",
    "bahrain": "BAH",
    "kuwait": "KWI",
    "amman": "AMM",
    "beirut": "BEY",
    "tel aviv": "TLV",
    "cairo": "CAI",

    # Asia
    "singapore": "SIN",
    "hong kong": "HKG",
    "tokyo": "NRT",
    "narita": "NRT",
    "haneda": "HND",
    "osaka": "KIX",
    "seoul": "ICN",
    "beijing": "PEK",
    "shanghai": "PVG",
    "taipei": "TPE",
    "bangkok": "BKK",
    "kuala lumpur": "KUL",
    "kl": "KUL",
    "jakarta": "CGK",
    "manila": "MNL",
    "delhi": "DEL",
    "new delhi": "DEL",
    "mumbai": "BOM",
    "bombay": "BOM",
    "bangalore": "BLR",
    "chennai": "MAA",
    "kolkata": "CCU",
    "colombo": "CMB",
    "hanoi": "HAN",
    "ho chi minh": "SGN",
    "saigon": "SGN",
    "bali": "DPS",
    "denpasar": "DPS",
    "phuket": "HKT",
    "kathmandu": "KTM",

    # Oceania
    "sydney": "SYD",
    "melbourne": "MEL",
    "brisbane": "BNE",
    "perth": "PER",
    "auckland": "AKL",
    "wellington": "WLG",

    # Africa
    "johannesburg": "JNB",
    "cape town": "CPT",
    "nairobi": "NBO",
    "lagos": "LOS",
    "addis ababa": "ADD",
    "casablanca": "CMN",
    "marrakech": "RAK",
    "dar es salaam": "DAR",
    "accra": "ACC",

    # South America
    "sao paulo": "GRU",
    "rio de janeiro": "GIG",
    "rio": "GIG",
    "buenos aires": "EZE",
    "santiago": "SCL",
    "lima": "LIM",
    "bogota": "BOG",
    "medellin": "MDE",
    "panama city": "PTY",
    "panama": "PTY",
}


def normalize_airport(input_value: str) -> str:
    """Normalize a city name or alias to an IATA airport code.

    If the input is already a valid-looking IATA code (3 uppercase letters),
    it is returned as-is. Otherwise, the input is looked up in the city
    mapping (case-insensitive).

    Args:
        input_value: City name, alias, or IATA code.

    Returns:
        IATA airport code (uppercase, 3 characters).

    Raises:
        ValueError: If the input cannot be resolved to a known IATA code.
    """
    cleaned = input_value.strip()

    # Extract IATA code from parenthetical format like "New York (JFK)"
    import re as _re
    paren_match = _re.search(r'\(([A-Z]{3})\)', cleaned)
    if paren_match:
        return paren_match.group(1)

    # Strip common noise patterns
    cleaned = _re.sub(r'\s*\([^)]*\)', '', cleaned).strip()  # Remove parentheticals
    cleaned = _re.sub(r'\s+airport$', '', cleaned, flags=_re.IGNORECASE).strip()  # Remove "airport"

    # Look up by city name / alias first (case-insensitive)
    key = cleaned.lower()
    if key in _CITY_TO_IATA:
        return _CITY_TO_IATA[key]

    # Otherwise, accept a raw IATA code.
    if len(cleaned) == 3 and cleaned.isalpha():
        return cleaned.upper()

    raise ValueError(
        f"Cannot resolve '{input_value}' to an IATA airport code. "
        f"Use a 3-letter IATA code directly or a recognized city name."
    )
