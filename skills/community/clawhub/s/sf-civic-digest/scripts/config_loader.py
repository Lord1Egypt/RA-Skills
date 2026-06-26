"""
Shared config loader for sf-civic-digest scripts.

District data comes from DISTRICT_DEFAULTS below. Pass --district N to any script.
All fields are optional — scripts use their own defaults when no district is given.

district defaults to None — callers should pass --district explicitly.
"""

import json
import os

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPTS_DIR)
DEFAULT_CONFIG_PATH = os.path.join(SKILL_ROOT, "civic_config.json")  # optional user override, not shipped

# Fallback district data when no config is present.
# Matches sf_civic_digest.py DISTRICT_MAP.
DISTRICT_DEFAULTS = {
    1: {"supervisor": "Connie Chan", "neighborhoods": ["Richmond", "Inner Richmond", "Outer Richmond", "Sea Cliff", "Jordan Park"], "streets": [], "key_addresses": [], "key_people": ["Chan"]},
    2: {"supervisor": "Stephen Sherrill", "neighborhoods": ["Marina", "Cow Hollow", "Pacific Heights", "Presidio Heights"], "streets": [], "key_addresses": [], "key_people": ["Sherrill"]},
    3: {"supervisor": "Danny Sauter", "neighborhoods": ["North Beach", "Chinatown", "Telegraph Hill", "Russian Hill", "Fisherman's Wharf"], "streets": [], "key_addresses": [], "key_people": ["Sauter"]},
    4: {"supervisor": "Alan Wong", "neighborhoods": ["Sunset", "Inner Sunset", "Outer Sunset", "Parkside"], "streets": [], "key_addresses": [], "key_people": ["Wong"]},
    5: {"supervisor": "Bilal Mahmood", "neighborhoods": ["NOPA", "North of Panhandle", "Western Addition", "Haight", "Hayes Valley", "Lower Haight", "Alamo Square", "Cole Valley", "Duboce"], "streets": ["Divisadero", "Fillmore", "Masonic", "Panhandle", "Stanyan", "Fell", "Oak", "Broderick", "Page", "Waller"], "key_addresses": ["400 Divisadero"], "key_people": ["Mahmood", "Dean Preston"]},
    6: {"supervisor": "Matt Dorsey", "neighborhoods": ["SoMa", "South of Market", "Tenderloin", "Civic Center", "Mid-Market"], "streets": [], "key_addresses": [], "key_people": ["Dorsey"]},
    7: {"supervisor": "Myrna Melgar", "neighborhoods": ["West Portal", "Forest Hill", "Twin Peaks", "Diamond Heights", "Glen Park", "Miraloma Park"], "streets": [], "key_addresses": [], "key_people": ["Melgar"]},
    8: {"supervisor": "Rafael Mandelman", "neighborhoods": ["Castro", "Noe Valley", "Corona Heights", "Eureka Valley", "Duboce Triangle"], "streets": [], "key_addresses": [], "key_people": ["Mandelman"]},
    9: {"supervisor": "Jackie Fielder", "neighborhoods": ["Mission", "Bernal Heights", "Portola"], "streets": [], "key_addresses": [], "key_people": ["Fielder"]},
    10: {"supervisor": "Shamann Walton", "neighborhoods": ["Bayview", "Hunters Point", "Visitacion Valley", "Excelsior", "Crocker Amazon"], "streets": [], "key_addresses": [], "key_people": ["Walton"]},
    11: {"supervisor": "Chyanne Chen", "neighborhoods": ["Excelsior", "Ingleside", "Oceanview", "Outer Mission"], "streets": [], "key_addresses": [], "key_people": ["Chen"]},
}


def load_config(config_path=None):
    """Load optional config override file. Returns dict (empty if no file found)."""
    path = config_path or DEFAULT_CONFIG_PATH
    if path and os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def get_district_config(district=None, config_path=None):
    """
    Return a merged config dict for the given district.

    Priority: config file overrides > DISTRICT_DEFAULTS > empty.
    If district is None, returns a sentinel so callers can prompt the user.

    Returns dict with keys:
        district, supervisor_name, neighborhoods, streets,
        key_addresses, key_people, topics, watchlist_addresses,
        watchlist_case_numbers
    """
    cfg = load_config(config_path)
    cfg_district = cfg.get("district", None)
    district = district or cfg_district
    if district is None:
        # Return a sentinel so callers can detect and prompt the user if needed.
        # Scripts should check for district=None before running and print a helpful error.
        return {"district": None, "supervisor_name": "", "neighborhoods": [], "streets": [],
                "key_addresses": [], "key_people": [], "topics": [],
                "watchlist_addresses": [], "watchlist_case_numbers": []}
    defaults = DISTRICT_DEFAULTS.get(district, {})

    # Only use config file overrides if the district matches what's in the config.
    # If someone passes --district 9 but config is set up for D5, use D9 defaults.
    use_cfg = (district == cfg_district)

    return {
        "district": district,
        "supervisor_name": cfg.get("supervisor_name", defaults.get("supervisor", "")) if use_cfg else defaults.get("supervisor", ""),
        "neighborhoods": cfg.get("neighborhoods", defaults.get("neighborhoods", [])) if use_cfg else defaults.get("neighborhoods", []),
        "streets": cfg.get("streets", defaults.get("streets", [])) if use_cfg else defaults.get("streets", []),
        "key_addresses": cfg.get("key_addresses", defaults.get("key_addresses", [])) if use_cfg else defaults.get("key_addresses", []),
        "key_people": cfg.get("key_people", defaults.get("key_people", [])) if use_cfg else defaults.get("key_people", []),
        "topics": cfg.get("topics", []) if use_cfg else [],
        "watchlist_addresses": cfg.get("watchlist_addresses", []) if use_cfg else [],
        "watchlist_case_numbers": cfg.get("watchlist_case_numbers", []) if use_cfg else [],
    }
