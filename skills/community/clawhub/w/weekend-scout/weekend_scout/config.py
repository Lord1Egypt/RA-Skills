"""Configuration management for Weekend Scout.

Handles reading, writing, and interactive setup of the YAML config file.
Config and cache files live in the repo-local `.weekend_scout/` directory for
editable/dev installs, or `~/.weekend_scout/` for global pip installs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


APP_NAME = "weekend-scout"

# Country code -> search language
COUNTRY_LANGUAGE_MAP: dict[str, str] = {
    "Poland": "pl",
    "Germany": "de",
    "France": "fr",
    "Czech Republic": "cs",
    "Slovakia": "sk",
    "Austria": "de",
    "Hungary": "hu",
    "Ukraine": "uk",
    "Lithuania": "lt",
    "Latvia": "lv",
    "Estonia": "et",
    "Belarus": "be",
    "Italy": "it",
    "Spain": "es",
    "Portugal": "pt",
    "Netherlands": "nl",
    "Sweden": "sv",
    "Norway": "no",
    "Denmark": "da",
    "Finland": "fi",
    "Romania": "ro",
    "Croatia": "hr",
    "Bulgaria": "bg",
    "Serbia": "sr",
    "Greece": "el",
    "Turkey": "tr",
    "Russia": "ru",
    "United States": "en",
    "Canada": "en",
    "United Kingdom": "en",
    "Ireland": "en",
    "Australia": "en",
    "New Zealand": "en",
    "Singapore": "en",
    "Japan": "ja",
    "South Korea": "ko",
}

# ISO 3166-1 alpha-2 -> country name (matches COUNTRY_LANGUAGE_MAP keys)
COUNTRY_CODE_MAP: dict[str, str] = {
    "PL": "Poland",
    "DE": "Germany",
    "FR": "France",
    "CZ": "Czech Republic",
    "SK": "Slovakia",
    "AT": "Austria",
    "HU": "Hungary",
    "UA": "Ukraine",
    "LT": "Lithuania",
    "LV": "Latvia",
    "EE": "Estonia",
    "BY": "Belarus",
    "IT": "Italy",
    "ES": "Spain",
    "PT": "Portugal",
    "NL": "Netherlands",
    "SE": "Sweden",
    "NO": "Norway",
    "DK": "Denmark",
    "FI": "Finland",
    "RO": "Romania",
    "HR": "Croatia",
    "BG": "Bulgaria",
    "RS": "Serbia",
    "GR": "Greece",
    "TR": "Turkey",
    "RU": "Russia",
    "US": "United States",
    "CA": "Canada",
    "GB": "United Kingdom",
    "IE": "Ireland",
    "AU": "Australia",
    "NZ": "New Zealand",
    "SG": "Singapore",
    "JP": "Japan",
    "KR": "South Korea",
}

DEFAULT_CONFIG: dict[str, Any] = {
    "home_city": "",
    "home_country": "",                               # populated during setup
    "home_coordinates": {"lat": 0.0, "lon": 0.0},   # 0,0 = unset sentinel
    "radius_km": 150,
    "search_language": "en",
    "max_city_options": 3,
    "max_trip_options": 10,
    "output_language": "en",
    "telegram_bot_token": "",
    "telegram_chat_id": "",
    "auto_run": False,
    "run_day": "friday",
    "run_time": "18:00",
    "max_searches": 15,
    "max_fetches": 15,
    "exclude_served": False,
}


def get_config_dir() -> Path:
    """Return the config directory for Weekend Scout.

    - Editable/dev install (pyproject.toml present at __file__'s grandparent):
      returns <repo>/.weekend_scout/ so config/cache stay in the checkout.
    - Global pip install (parents[1] = site-packages, no pyproject.toml):
      returns ~/.weekend_scout/ for a stable user-scoped location.
    """
    candidate_root = Path(__file__).resolve().parents[1]
    if (candidate_root / "pyproject.toml").exists():
        return candidate_root / ".weekend_scout"
    return Path.home() / ".weekend_scout"


def get_config_path() -> Path:
    """Return the full path to the config YAML file."""
    return get_config_dir() / "config.yaml"


def get_cache_dir(config: dict[str, Any]) -> Path:
    """Return the directory used for cache files (DB, city list JSON, logs).

    Cache lives at <config_dir>/cache/ — separate from config.yaml.
    On first call after upgrade, migrates legacy files from <config_dir>/ root.

    Args:
        config: Loaded configuration dictionary (unused; reserved for
                future per-profile cache directories).

    Returns:
        Path to the cache directory (created if absent).
    """
    if "_cache_dir" in config:
        # Test-only override
        cache_dir = Path(config["_cache_dir"])
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    import shutil as _shutil

    base = get_config_dir()
    cache_dir = base / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    # One-time migration from legacy layout (files lived in base dir)
    _MIGRATE_FILES = ["cache.db", "action_log.jsonl", "scout_message.txt"]
    for fname in _MIGRATE_FILES:
        old = base / fname
        if old.exists() and not (cache_dir / fname).exists():
            _shutil.move(str(old), str(cache_dir / fname))
    for old_json in base.glob("cities_*.json"):
        dest = cache_dir / old_json.name
        if not dest.exists():
            _shutil.move(str(old_json), str(dest))
    # Migrate geonames directory
    old_geonames = base / "geonames"
    new_geonames = cache_dir / "geonames"
    if old_geonames.exists() and not new_geonames.exists():
        _shutil.move(str(old_geonames), str(new_geonames))

    return cache_dir


def load_config() -> dict[str, Any]:
    """Load config from disk, returning defaults merged with stored values.

    Returns:
        Merged configuration dictionary.
    """
    path = get_config_path()
    if not path.exists():
        return dict(DEFAULT_CONFIG)
    with path.open("r", encoding="utf-8") as f:
        stored = yaml.safe_load(f) or {}
    merged = dict(DEFAULT_CONFIG)
    merged.update(stored)
    return merged


def save_config(config: dict[str, Any]) -> None:
    """Write config dictionary to disk.

    Args:
        config: Configuration dictionary to persist.
    """
    path = get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)


def _prompt(label: str, default: str = "") -> str:
    """Prompt the user for input, showing default in brackets."""
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value if value else default


def run_setup_wizard(_geonames_path: "Path | None" = None) -> dict[str, Any]:
    """Run interactive setup wizard to configure Weekend Scout.

    Asks only for city name and radius. Coordinates, country, and search
    language are resolved automatically from the GeoNames database.
    If the city is not found, the user is prompted for coordinates.

    Args:
        _geonames_path: Override GeoNames file path (used in tests).

    Returns:
        Completed configuration dictionary.
    """
    print("=== Weekend Scout Setup ===")
    print(f"Config will be saved to: {get_config_path()}\n")

    config = load_config()

    # -- City --
    while True:
        city = input("Home city: ").strip()
        if city:
            break
        print("  City name is required.")

    config["home_city"] = city

    # -- Auto-geocode from GeoNames --
    if _geonames_path is None:
        from weekend_scout.cities import ensure_geonames
        _geonames_path = ensure_geonames()

    if _geonames_path.exists():
        from weekend_scout.cities import find_city_candidates
        candidates = find_city_candidates(city, _geonames_path)
        if len(candidates) == 1:
            c = candidates[0]
            print(f"  Found: {c['name']}, {c['country_name']} (pop. {c['population']:,})")
            config["home_city"] = c["name"]
            config["home_coordinates"] = {"lat": c["lat"], "lon": c["lon"]}
            config["home_country"] = c["country_name"]
            config["search_language"] = c["language"]
        elif len(candidates) > 1:
            print(f"  '{city}' found in multiple countries:")
            for i, c in enumerate(candidates, 1):
                print(f"    {i}. {c['name']}, {c['country_name']} (pop. {c['population']:,})")
            while True:
                choice = input("  Enter number [1]: ").strip() or "1"
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(candidates):
                        c = candidates[idx]
                        config["home_city"] = c["name"]
                        config["home_coordinates"] = {"lat": c["lat"], "lon": c["lon"]}
                        config["home_country"] = c["country_name"]
                        config["search_language"] = c["language"]
                        break
                    print("  Invalid choice, try again.")
                except ValueError:
                    print("  Please enter a number.")
        else:
            print(f"  '{city}' not found in local database.")
            print("  Enter coordinates manually (or press Enter to skip):")
            lat_str = input("  Latitude: ").strip()
            lon_str = input("  Longitude: ").strip()
            if lat_str and lon_str:
                try:
                    config["home_coordinates"] = {"lat": float(lat_str), "lon": float(lon_str)}
                except ValueError:
                    print("  Invalid coordinates — skipping.")
            country = input("  Country name: ").strip()
            if country:
                config["home_country"] = country
                config["search_language"] = COUNTRY_LANGUAGE_MAP.get(country, "en")
    else:
        print("  Tip: Run 'python -m weekend_scout download-data' to enable nearby city suggestions.\n")

    # -- Radius --
    radius_str = input(f"Search radius in km [{config.get('radius_km', 150)}]: ").strip()
    if radius_str:
        try:
            config["radius_km"] = int(radius_str)
        except ValueError:
            print("  Invalid radius, keeping default.")

    # -- Telegram (optional) --
    print("\nTelegram settings (press Enter to skip — configure later with 'config' command):")
    token = input("  Bot token: ").strip()
    if token:
        config["telegram_bot_token"] = token
    chat_id = input("  Chat ID: ").strip()
    if chat_id:
        config["telegram_chat_id"] = chat_id

    save_config(config)
    print(f"\nConfig saved. Run /weekend-scout to start scouting!")
    return config
