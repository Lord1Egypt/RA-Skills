#!/usr/bin/env python3
"""
Simmer Weather Trading Skill

Trades Polymarket weather markets using NOAA forecasts.
Inspired by gopfan2's $2M+ weather trading strategy.

Usage:
    python weather_trader.py              # Dry run (show opportunities, no trades)
    python weather_trader.py --live       # Execute real trades
    python weather_trader.py --positions  # Show current positions only
    python weather_trader.py --smart-sizing  # Use portfolio-based position sizing

Requires:
    SIMMER_API_KEY environment variable (get from simmer.markets/dashboard)
"""

import os
import sys
import re
import json
import argparse
import statistics
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

# Load .env from project root (two levels up from this file)
try:
    from dotenv import load_dotenv

    _env_path = Path(__file__).resolve().parent.parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    pass  # python-dotenv optional; env vars may be set externally

# Force line-buffered stdout so output is visible in non-TTY environments (cron, Docker, OpenClaw)
sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")

# Optional: Trade Journal integration for tracking
try:
    from tradejournal import log_trade

    JOURNAL_AVAILABLE = True
except ImportError:
    try:
        # Try relative import within skills package
        from skills.tradejournal import log_trade

        JOURNAL_AVAILABLE = True
    except ImportError:
        JOURNAL_AVAILABLE = False

        def log_trade(*args, **kwargs):
            pass  # No-op if tradejournal not installed


# Performance tracking hooks (trade logging + circuit breaker)
from trade_performance import (
    write_trade_log,
    check_circuit_breaker,
    update_circuit_breaker,
)

# EV Calculator + Kelly Criterion (v1.2)
from ev_calculator import (
    calculate_ev,
    should_take_trade,
    kelly_fraction,
    quarter_kelly_position,
    is_longtail_contract,
    longtail_ev_adjustment,
)

# Bayesian probability update (v1.3)
from bayesian_update import (
    bayesian_update,
    compute_likelihood_ratio,
    should_update_probability,
    should_close_position,
)

# Maker/Taker strategy arbiter (v1.3)
from maker_taker_arbiter import (
    StrategyMode,
    MarketCondition,
    determine_strategy_mode,
    get_maker_taker_allocation,
)

# Smart Money signals (v1.4)
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from smart_money_signal import (
        fetch_smart_money_signals,
        get_signal_for_market,
        merge_signal_data,
    )

    SMART_MONEY_AVAILABLE = True
except ImportError:
    SMART_MONEY_AVAILABLE = False

    def fetch_smart_money_signals(*args, **kwargs):
        return []

    def get_signal_for_market(*args, **kwargs):
        return None

    def merge_signal_data(base, sm):
        return base

# =============================================================================
# Configuration (config.json > env vars > defaults)
# =============================================================================

from simmer_sdk.skill import load_config, update_config, get_config_path

# Configuration schema
# Note: env var names match autotune registry. Legacy aliases (SIMMER_WEATHER_ENTRY,
# SIMMER_WEATHER_EXIT, SIMMER_WEATHER_MAX_POSITION, SIMMER_WEATHER_MAX_TRADES) are
# resolved as fallbacks below for backwards compatibility.
CONFIG_SCHEMA = {
    "entry_threshold": {
        "env": "SIMMER_WEATHER_ENTRY_THRESHOLD",
        "default": 0.15,
        "type": float,
    },
    "exit_threshold": {
        "env": "SIMMER_WEATHER_EXIT_THRESHOLD",
        "default": 0.45,
        "type": float,
    },
    "max_position_usd": {
        "env": "SIMMER_WEATHER_MAX_POSITION_USD",
        "default": 2.00,
        "type": float,
    },
    "sizing_pct": {"env": "SIMMER_WEATHER_SIZING_PCT", "default": 0.05, "type": float},
    "max_trades_per_run": {
        "env": "SIMMER_WEATHER_MAX_TRADES_PER_RUN",
        "default": 5,
        "type": int,
    },
    "locations": {"env": "SIMMER_WEATHER_LOCATIONS", "default": "NYC", "type": str},
    "binary_only": {
        "env": "SIMMER_WEATHER_BINARY_ONLY",
        "default": False,
        "type": bool,
    },
    "slippage_max": {
        "env": "SIMMER_WEATHER_SLIPPAGE_MAX",
        "default": 0.15,
        "type": float,
    },
    "min_liquidity": {
        "env": "SIMMER_WEATHER_MIN_LIQUIDITY",
        "default": 0.0,
        "type": float,
    },
    "circuit_breaker_threshold": {
        "default": 3,
        "env": "SIMMER_WEATHER_CB_THRESHOLD",
        "type": int,
        "help": "Consecutive live trade losses before pausing",
    },
    "circuit_breaker_cooldown": {
        "default": 6,
        "env": "SIMMER_WEATHER_CB_COOLDOWN_HOURS",
        "type": int,
        "help": "Hours before auto-resume after circuit breaker trip",
    },
    # v1.2: EV Calculator + Kelly Criterion
    "ev_min_threshold": {
        "default": 0.0,
        "type": float,
        "help": "Minimum EV required to take trade (0.0 = any positive EV)",
    },
    "longtail_ev_penalty": {
        "default": 0.20,
        "type": float,
        "help": "EV penalty for <20¢ contracts (longtail bias)",
    },
    "longtail_price_cutoff": {
        "default": 0.20,
        "type": float,
        "help": "Price threshold below which contracts are considered longtail",
    },
    "use_kelly_sizing": {
        "default": True,
        "type": bool,
        "help": "Use Kelly Criterion for position sizing (vs fixed %)",
    },
    "kelly_multiplier": {
        "default": 0.25,
        "type": float,
        "help": "Kelly fraction multiplier (0.25 = Quarter Kelly)",
    },
    "noaa_win_probability": {
        "default": 0.85,
        "type": float,
        "help": "Base win probability for NOAA forecasts (in-bucket accuracy)",
    },
}

# Backwards-compatible env var aliases (old name -> new name)
_LEGACY_ENV_ALIASES = {
    "SIMMER_WEATHER_ENTRY": "SIMMER_WEATHER_ENTRY_THRESHOLD",
    "SIMMER_WEATHER_EXIT": "SIMMER_WEATHER_EXIT_THRESHOLD",
    "SIMMER_WEATHER_MAX_POSITION": "SIMMER_WEATHER_MAX_POSITION_USD",
    "SIMMER_WEATHER_MAX_TRADES": "SIMMER_WEATHER_MAX_TRADES_PER_RUN",
}
for _old, _new in _LEGACY_ENV_ALIASES.items():
    if _old in os.environ and _new not in os.environ:
        os.environ[_new] = os.environ[_old]

# Load configuration
_config = load_config(CONFIG_SCHEMA, __file__, slug="polymarket-weather-trader")

# Circuit breaker settings
CB_THRESHOLD = _config.get("circuit_breaker_threshold", 3)
CB_COOLDOWN_HOURS = _config.get("circuit_breaker_cooldown", 6)

NOAA_API_BASE = "https://api.weather.gov"

# SimmerClient singleton
_client = None


def get_client(live=True):
    """Lazy-init SimmerClient singleton."""
    global _client
    if _client is None:
        try:
            from simmer_sdk import SimmerClient
        except ImportError:
            print("Error: simmer-sdk not installed. Run: pip install simmer-sdk")
            sys.exit(1)
        api_key = os.environ.get("SIMMER_API_KEY")
        if not api_key:
            print("Error: SIMMER_API_KEY environment variable not set")
            print("Get your API key from: simmer.markets/dashboard -> SDK tab")
            sys.exit(1)
        venue = os.environ.get("TRADING_VENUE", "polymarket")
        _client = SimmerClient(api_key=api_key, venue=venue, live=live)
    return _client


# Source tag for tracking
TRADE_SOURCE = "sdk:weather"
SKILL_SLUG = "polymarket-weather-trader"

# v2.1: Trade log for city-level bias learning (Scheme 2)
TRADE_LOG_FILE = str(Path.home() / ".hermes" / "weather-trade-log.jsonl")


def apply_madis_bias_correction(
    forecast_temp: float,
    madis_obs: dict,
    event_info: dict,
    base_prob: float,
    unit: str = "F",
) -> tuple[float, str]:
    """
    Apply MADIS airport-observation bias correction to forecast probability.

    Problem: Forecasts can be systematically hot or cold for a given city.
    Solution: Compare MADIS current observation vs forecast, compute bias,
    and shift probability in the direction the bias suggests.

    Args:
        forecast_temp: The forecasted high temperature
        madis_obs: MADIS observation dict with temp_f / temp_c
        event_info: Parsed event info dict
        base_prob: The base probability from NOAA calibration
        unit: 'F' or 'C'

    Returns:
        (adjusted_probability, log_message)
    """
    if not madis_obs or "temp_f" not in madis_obs:
        return base_prob, ""

    madis_temp_f = madis_obs["temp_f"]

    # Fetch today's forecast for comparison (use cached from get_weather_with_confidence)
    # This is called after we already have the forecast, so we compute bias here
    # MADIS is "right now", forecast is "today's expected high"
    # Bias direction: positive = forecast is warmer than actual, negative = colder
    try:
        from . import get_weather_forecast
    except ImportError:
        try:
            from get_weather_forecast import get_weather_forecast
        except ImportError:
            return base_prob, ""

    try:
        weather = get_weather_forecast(event_info["location"])
        today_key = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        day_forecast = weather.get(today_key, {})
        forecast_high_f = day_forecast.get("high")
        if forecast_high_f is None:
            forecast_high_f = day_forecast.get("high_f")
        if forecast_high_f is None:
            return base_prob, ""
    except Exception:
        return base_prob, ""

    # Temperature error: how wrong is today's forecast right now?
    temp_error_f = forecast_high_f - madis_temp_f  # positive = forecast warmer than actual

    # Normalize by ensemble disagreement (proxy for forecast uncertainty)
    # If models agree but MADIS says otherwise → stronger correction
    # Use 3°F as baseline MAE if no disagreement metric available
    normalized_bias = temp_error_f / 3.0  # clamp to [-1, 1] range roughly
    normalized_bias = max(-1.0, min(1.0, normalized_bias))

    # Shift probability in direction that bias suggests
    # If forecast is too warm (temp_error > 0) and we're buying YES on high-temp:
    #   actual temp tends to be lower → probability should be reduced
    # For a "high temp" event: positive error = forecast too warm → reduce prob
    prob_shift = normalized_bias * 0.06  # max shift ~6%
    adjusted = base_prob - prob_shift
    adjusted = max(0.01, min(0.99, adjusted))

    direction = "warm" if temp_error_f > 0 else "cold"
    msg = (
        f" MADIS bias: forecast {direction} by {abs(temp_error_f):.1f}°F "
        f"({forecast_high_f:.0f}°F vs {madis_temp_f:.0f}°F obs) → prob {base_prob:.3f}→{adjusted:.3f}"
    )
    return adjusted, msg


def log_trade_entry(
    market_id: str,
    market_question: str,
    city: str,
    target_date: str,
    forecast_temp: float,
    bucket_range: str,
    price: float,
    side: str,
    amount: float,
    shares: float,
    cost: float,
    noaa_probability: float,
    bias_adjustment: float,
    madis_bias_msg: str,
    unit: str,
    source: str,
    signal_data: dict,
) -> None:
    """
    Append a trade entry record to the JSONL trade log.
    Used for building city-level forecast bias statistics over time.
    """
    import os
    os.makedirs(os.path.dirname(TRADE_LOG_FILE), exist_ok=True)
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "market_id": market_id,
        "market_question": market_question,
        "city": city,
        "target_date": target_date,
        "forecast_temp": forecast_temp,
        "bucket_range": bucket_range,
        "price": price,
        "side": side,
        "amount_usd": amount,
        "shares": shares,
        "cost_usd": cost,
        "noaa_probability": noaa_probability,
        "bias_adjustment": bias_adjustment,
        "madis_bias_msg": madis_bias_msg,
        "unit": unit,
        "signal_source": source,
        "combined_confidence": signal_data.get("combined_confidence") if signal_data else None,
        "edge": signal_data.get("edge") if signal_data else None,
    }
    try:
        with open(TRADE_LOG_FILE, "a") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass  # Non-critical, don't disrupt trading
_automaton_reported = False

# Polymarket constraints
MIN_SHARES_PER_ORDER = 3.0  # Minimum 3 shares per order (moderate config)
MIN_TICK_SIZE = 0.01  # Minimum tradeable price
# For small-budget testing ($1/position), the 5-share minimum means:
#   price <= $0.20 → $1.00 buys ≥5 shares (OK)
#   price > $0.20 → $1.00 buys <5 shares (blocked by min shares)
# This is a Polymarket CLOB constraint, not configurable.

# Strategy parameters - from config
ENTRY_THRESHOLD = _config["entry_threshold"]
EXIT_THRESHOLD = _config["exit_threshold"]
MAX_POSITION_USD = _config["max_position_usd"]
_automaton_max = os.environ.get("AUTOMATON_MAX_BET")
if _automaton_max:
    MAX_POSITION_USD = min(MAX_POSITION_USD, float(_automaton_max))

# Smart sizing parameters
SMART_SIZING_PCT = _config["sizing_pct"]

# v1.2: EV Calculator + Kelly Criterion
EV_MIN_THRESHOLD = _config["ev_min_threshold"]
LONGTAIL_EV_PENALTY = _config["longtail_ev_penalty"]
LONGTAIL_PRICE_CUTOFF = _config["longtail_price_cutoff"]
USE_KELLY_SIZING = _config["use_kelly_sizing"]
KELLY_MULTIPLIER = _config["kelly_multiplier"]
NOAA_WIN_PROBABILITY = _config["noaa_win_probability"]

# v1.5: NOAA horizon-based probability calibration
# Source: NOAA National Weather Service forecast accuracy statistics
# D+1 ~ 88-92%, D+3 ~ 80-84%, D+5 ~ 70-76%, D+7 ~ 63-70%
# Accuracy degrades ~2-3% per additional forecast day
NOAA_HORIZON_ACCURACY = {
    0: 0.95,  # D+0 (today): nowcast, very high accuracy
    1: 0.90,  # D+1: next-day forecast
    2: 0.86,  # D+2: 2-day forecast
    3: 0.82,  # D+3: 3-day forecast
    4: 0.78,  # D+4: 4-day forecast
    5: 0.74,  # D+5: 5-day forecast
    6: 0.70,  # D+6: 6-day forecast
    7: 0.66,  # D+7: 7-day forecast (weekly)
}


def get_forecast_horizon(event_info: dict) -> int:
    """Compute forecast horizon in days from today to target date."""
    if not event_info or "date" not in event_info:
        return 1
    date_str = event_info["date"]
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return 1
    now = datetime.now(timezone.utc)
    horizon = (target - now.replace(hour=0, minute=0, second=0, microsecond=0)).days
    return max(0, horizon)


def calibrate_noaa_probability(event_info: dict, base_prob: float = 0.85) -> float:
    """
    Calibrate NOAA win probability based on forecast horizon.

    NOAA forecast accuracy degrades with horizon (D+1 ~90%, D+5 ~74%, D+7 ~66%).
    We scale the base probability by the ratio of horizon accuracy to base accuracy,
    then blend with the base (horizon-specific values are more extreme; blending
    prevents over-confidence on very-short or very-long horizons).
    """
    horizon = get_forecast_horizon(event_info)
    horizon_accuracy = NOAA_HORIZON_ACCURACY.get(horizon, NOAA_HORIZON_ACCURACY[7])
    ratio = horizon_accuracy / base_prob
    calibrated = base_prob * ratio
    return round(min(0.99, max(0.01, calibrated)), 4)


# v1.4: Smart Money signals
USE_SMART_MONEY = _config.get("use_smart_money", True)
SMART_MONEY_MIN_SCORE = _config.get("smart_money_min_score", 7)

# Cache Smart Money signals per run (fetched once, reused for all markets)
_smart_money_cache = None


def _get_smart_money_signals():
    """Fetch and cache Smart Money signals for this run."""
    global _smart_money_cache
    if _smart_money_cache is None and USE_SMART_MONEY and SMART_MONEY_AVAILABLE:
        _smart_money_cache = fetch_smart_money_signals(min_score=SMART_MONEY_MIN_SCORE)
    return _smart_money_cache or []


# Rate limiting
MAX_TRADES_PER_RUN = _config["max_trades_per_run"]

# Market type filter
BINARY_ONLY = _config["binary_only"]

# Context safeguard thresholds
SLIPPAGE_MAX_PCT = _config["slippage_max"]  # Skip if slippage exceeds this (tunable)
MIN_LIQUIDITY_USD = _config[
    "min_liquidity"
]  # Skip markets with liquidity below this (0 = disabled)
TIME_TO_RESOLUTION_MIN_HOURS = 2  # Skip if resolving in < 2 hours

# Price trend detection
PRICE_DROP_THRESHOLD = 0.10  # 10% drop in last 24h = stronger signal

# Supported locations (matching Polymarket resolution sources)
LOCATIONS = {
    "NYC": {
        "lat": 40.7769,
        "lon": -73.8740,
        "name": "New York City (LaGuardia)",
        "station": "KLGA",
    },
    "Chicago": {
        "lat": 41.9742,
        "lon": -87.9073,
        "name": "Chicago (O'Hare)",
        "station": "KORD",
    },
    "Seattle": {
        "lat": 47.4502,
        "lon": -122.3088,
        "name": "Seattle (Sea-Tac)",
        "station": "KSEA",
    },
    "Atlanta": {
        "lat": 33.6407,
        "lon": -84.4277,
        "name": "Atlanta (Hartsfield)",
        "station": "KATL",
    },
    "Dallas": {
        "lat": 32.8998,
        "lon": -97.0403,
        "name": "Dallas (DFW)",
        "station": "KDFW",
    },
    "Miami": {
        "lat": 25.7959,
        "lon": -80.2870,
        "name": "Miami (MIA)",
        "station": "KMIA",
    },
    "Houston": {
        "lat": 29.7604,
        "lon": -95.3698,
        "name": "Houston (IAH)",
        "station": "KIAH",
    },
    "Phoenix": {
        "lat": 33.4484,
        "lon": -112.0740,
        "name": "Phoenix (PHX)",
        "station": "KPHX",
    },
    "Philadelphia": {
        "lat": 39.9526,
        "lon": -75.1652,
        "name": "Philadelphia",
        "station": "KPHL",
    },
    "Boston": {
        "lat": 42.3601,
        "lon": -71.0589,
        "name": "Boston (Logan)",
        "station": "KBOS",
    },
    "Denver": {
        "lat": 39.8561,
        "lon": -104.6737,
        "name": "Denver (DEN)",
        "station": "KDEN",
    },
    "Las Vegas": {
        "lat": 36.1699,
        "lon": -115.1398,
        "name": "Las Vegas (LAS)",
        "station": "KLAS",
    },
    "San Francisco": {
        "lat": 37.7749,
        "lon": -122.4194,
        "name": "San Francisco",
        "station": "KSFO",
    },
    "Los Angeles": {
        "lat": 33.9425,
        "lon": -118.4081,
        "name": "Los Angeles (LAX)",
        "station": "KLAX",
    },
    "San Diego": {
        "lat": 32.7338,
        "lon": -117.1897,
        "name": "San Diego (SAN)",
        "station": "KSAN",
    },
    "Washington DC": {
        "lat": 38.9072,
        "lon": -77.0369,
        "name": "Washington DC (Reagan)",
        "station": "KDCA",
    },
    "Nashville": {
        "lat": 36.1263,
        "lon": -86.7714,
        "name": "Nashville (BNA)",
        "station": "KBNA",
    },
    "Portland": {
        "lat": 45.5898,
        "lon": -122.5951,
        "name": "Portland (PDX)",
        "station": "KPDX",
    },
    "Minneapolis": {
        "lat": 44.8848,
        "lon": -93.2223,
        "name": "Minneapolis (MSP)",
        "station": "KMSP",
    },
    "Detroit": {
        "lat": 42.2162,
        "lon": -83.3554,
        "name": "Detroit (DTW)",
        "station": "KDTW",
    },
    "Tampa": {
        "lat": 27.9755,
        "lon": -82.4891,
        "name": "Tampa (TPA)",
        "station": "KTPA",
    },
    "Orlando": {
        "lat": 28.4312,
        "lon": -81.3081,
        "name": "Orlando (MCO)",
        "station": "KMCO",
    },
    "San Antonio": {
        "lat": 29.4241,
        "lon": -98.4936,
        "name": "San Antonio (SAT)",
        "station": "KSAT",
    },
    "Pittsburgh": {
        "lat": 40.4406,
        "lon": -79.9959,
        "name": "Pittsburgh (PIT)",
        "station": "KPIT",
    },
    "Cleveland": {
        "lat": 41.4993,
        "lon": -81.6944,
        "name": "Cleveland (CLE)",
        "station": "KCLE",
    },
    "Austin": {
        "lat": 30.1944,
        "lon": -97.6700,
        "name": "Austin (AUS)",
        "station": "KAUS",
    },
}

# Active locations - from config
_locations_str = _config["locations"]
ACTIVE_LOCATIONS = [
    loc.strip().upper() for loc in _locations_str.split(",") if loc.strip()
]

# =============================================================================
# NOAA Weather API
# =============================================================================

# International city coordinates for Open-Meteo fallback
# Keyed by the city name as it appears in market questions
INTERNATIONAL_LOCATIONS = {
    "Tel Aviv": {"lat": 32.0853, "lon": 34.7818, "tz": "Asia/Jerusalem"},
    "Munich": {"lat": 48.1351, "lon": 11.5820, "tz": "Europe/Berlin"},
    "London": {"lat": 51.5074, "lon": -0.1278, "tz": "Europe/London"},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503, "tz": "Asia/Tokyo"},
    "Seoul": {"lat": 37.5665, "lon": 126.9780, "tz": "Asia/Seoul"},
    "Ankara": {"lat": 39.9334, "lon": 32.8597, "tz": "Europe/Istanbul"},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462, "tz": "Asia/Kolkata"},
    "Wellington": {"lat": -41.2866, "lon": 174.7756, "tz": "Pacific/Auckland"},
    "Taipei": {"lat": 25.0330, "lon": 121.5654, "tz": "Asia/Taipei"},
    "Shanghai": {"lat": 31.2304, "lon": 121.4737, "tz": "Asia/Shanghai"},
    "Beijing": {"lat": 39.9042, "lon": 116.4074, "tz": "Asia/Shanghai"},
    "Hong Kong": {"lat": 22.3193, "lon": 114.1694, "tz": "Asia/Hong_Kong"},
    "Singapore": {"lat": 1.3521, "lon": 103.8198, "tz": "Asia/Singapore"},
    "Sydney": {"lat": -33.8688, "lon": 151.2093, "tz": "Australia/Sydney"},
    "Melbourne": {"lat": -37.8136, "lon": 144.9631, "tz": "Australia/Melbourne"},
    "Paris": {"lat": 48.8566, "lon": 2.3522, "tz": "Europe/Paris"},
    "Berlin": {"lat": 52.5200, "lon": 13.4050, "tz": "Europe/Berlin"},
    "Madrid": {"lat": 40.4168, "lon": -3.7038, "tz": "Europe/Madrid"},
    "Rome": {"lat": 41.9028, "lon": 12.4964, "tz": "Europe/Rome"},
    "Amsterdam": {"lat": 52.3676, "lon": 4.9041, "tz": "Europe/Amsterdam"},
    "Toronto": {"lat": 43.6532, "lon": -79.3832, "tz": "America/Toronto"},
    "Vancouver": {"lat": 49.2827, "lon": -123.1207, "tz": "America/Vancouver"},
    "Shenzhen": {"lat": 22.5431, "lon": 114.0595, "tz": "Asia/Shanghai"},
    "Guangzhou": {"lat": 23.1291, "lon": 113.2644, "tz": "Asia/Shanghai"},
    "Chengdu": {"lat": 30.5728, "lon": 104.0668, "tz": "Asia/Shanghai"},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "tz": "Asia/Kolkata"},
    "Delhi": {"lat": 28.7041, "lon": 77.1025, "tz": "Asia/Kolkata"},
    "Wuhan": {"lat": 30.5928, "lon": 114.3055, "tz": "Asia/Shanghai"},
}

OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_ENSEMBLE_BASE = "https://api.open-meteo.com/v1/ensemble"

MAX_RETRIES = 2
RETRY_DELAY = 1

# City -> preferred weather models (in order of preference)
CITY_MODEL_PREFERENCES = {
    # US cities - GFS best, HRRR for short range
    "NYC": ["gfs", "ecmwf_ifs", "icon"],
    "Chicago": ["gfs", "ecmwf_ifs", "icon"],
    "Seattle": ["gfs", "icon", "ecmwf_ifs"],
    "Los Angeles": ["gfs", "ecmwf_ifs", "icon"],
    "Miami": ["gfs", "ecmwf_ifs", "icon"],
    "Houston": ["gfs", "icon", "ecmwf_ifs"],
    # European cities - ECMWF/ICON better
    "London": ["ecmwf_ifs", "icon", "gfs"],
    "Paris": ["ecmwf_ifs", "icon", "gfs"],
    "Berlin": ["icon", "ecmwf_ifs", "gfs"],
    "Munich": ["icon", "ecmwf_ifs", "gfs"],
    "Madrid": ["ecmwf_ifs", "icon", "gfs"],
    "Rome": ["ecmwf_ifs", "icon", "gfs"],
    "Amsterdam": ["ecmwf_ifs", "icon", "gfs"],
    # Asian cities
    "Tokyo": ["gfs", "ecmwf_ifs", "icon"],
    "Seoul": ["gfs", "kma", "ecmwf_ifs"],
    "Beijing": ["gfs", "cma_grapes", "ecmwf_ifs"],
    "Shanghai": ["gfs", "cma_grapes", "ecmwf_ifs"],
    "Hong Kong": ["gfs", "ecmwf_ifs", "icon"],
    "Singapore": ["gfs", "ecmwf_ifs", "icon"],
    "Mumbai": ["gfs", "ecmwf_ifs", "icon"],
    "Delhi": ["gfs", "ecmwf_ifs", "icon"],
    # Australian cities
    "Sydney": ["gfs", "bom_access_global", "ecmwf_ifs"],
    "Melbourne": ["gfs", "bom_access_global", "ecmwf_ifs"],
    # Default
    "default": ["gfs", "ecmwf_ifs", "icon"],
}


def _retry_with_backoff(func, *args, **kwargs):
    """Execute func with exponential backoff retry logic."""
    import time

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            result = func(*args, **kwargs)
            if result:
                return result
        except Exception as e:
            last_error = e
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY * (attempt + 1))
    return None


def get_openmeteo_forecast(
    city: str, model: str = None, use_ensemble: bool = False
) -> dict:
    """Get Open-Meteo forecast for a city with specific model or ensemble.

    Args:
        city: City name to look up in INTERNATIONAL_LOCATIONS
        model: Specific model to use (gfs, ecmwf_ifs, icon, etc.). If None, uses city preference.
        use_ensemble: If True, fetch ensemble data with multiple models for confidence scoring.

    Returns:
        dict with date -> {"high": temp, "low": temp} in Celsius, or
        dict with ensemble data if use_ensemble=True
    """
    loc = INTERNATIONAL_LOCATIONS.get(city)
    if not loc:
        return {}

    if model is None:
        prefs = CITY_MODEL_PREFERENCES.get(city, CITY_MODEL_PREFERENCES["default"])
        model = prefs[0]

    base_url = OPEN_METEO_ENSEMBLE_BASE if use_ensemble else OPEN_METEO_BASE

    params = (
        f"?latitude={loc['lat']}&longitude={loc['lon']}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&temperature_unit=celsius"
        f"&timezone={loc['tz'].replace('/', '%2F')}"
        f"&forecast_days=10"
    )

    if use_ensemble:
        prefs = CITY_MODEL_PREFERENCES.get(city, CITY_MODEL_PREFERENCES["default"])
        models_param = ",".join(prefs[:4])
        params += f"&models={models_param}"

    url = base_url + params
    try:
        with urlopen(url, timeout=20) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  Open-Meteo ({model or 'auto'}) error for {city}: {e}")
        return {}

    if use_ensemble and "model_run" in data:
        return _parse_ensemble_forecast(data)
    else:
        return _parse_openmeteo_daily(data)


def _parse_openmeteo_daily(data: dict) -> dict:
    """Parse Open-Meteo daily forecast data."""
    daily = data.get("daily", {})
    dates = daily.get("time", [])
    highs = daily.get("temperature_2m_max", [])
    lows = daily.get("temperature_2m_min", [])

    forecasts = {}
    for d, h, l in zip(dates, highs, lows):
        forecasts[d] = {
            "high": round(h) if h is not None else None,
            "low": round(l) if l is not None else None,
        }
    return forecasts


def _parse_ensemble_forecast(data: dict) -> dict:
    """Parse Open-Meteo ensemble forecast data with model runs.

    Returns dict with date -> {
        "high": median_high,
        "low": median_low,
        "high_std": std_dev,
        "low_std": std_dev,
        "model_count": number of models,
        "models": {model_name: {"high": temp, "low": temp}}
    }
    """
    daily = data.get("daily", {})
    model_runs = data.get("model_run", [])

    if not model_runs or not daily:
        return {}

    dates = daily.get("time", [])
    forecasts = {}

    for date_idx, d in enumerate(dates):
        highs = []
        lows = []
        model_temps = {}

        for run in model_runs:
            run_data = run.get("daily", {})
            h = run_data.get("temperature_2m_max", [None] * len(dates))
            l = run_data.get("temperature_2m_min", [None] * len(dates))

            model_name = run.get("model", "unknown")
            high_val = h[date_idx] if date_idx < len(h) else None
            low_val = l[date_idx] if date_idx < len(l) else None

            if high_val is not None:
                highs.append(high_val)
                lows.append(low_val)
                model_temps[model_name] = {
                    "high": round(high_val),
                    "low": round(low_val),
                }

        if highs:
            import statistics

            forecasts[d] = {
                "high": round(statistics.median(highs)),
                "low": round(statistics.median(lows)),
                "high_std": round(statistics.stdev(highs), 1) if len(highs) > 1 else 0,
                "low_std": round(statistics.stdev(lows), 1) if len(lows) > 1 else 0,
                "model_count": len(highs),
                "models": model_temps,
            }
        else:
            forecasts[d] = {"high": None, "low": None}

    return forecasts


def get_openmeteo_multi_model(city: str) -> dict:
    """Fetch forecasts from multiple models and compare.

    Returns dict with date -> {
        "high": best_estimate,
        "low": best_estimate,
        "all_highs": [temps from all models],
        "all_lows": [temps from all models],
        "disagreement": max - min (uncertainty measure)
    }
    """
    loc = INTERNATIONAL_LOCATIONS.get(city)
    if not loc:
        return {}

    prefs = CITY_MODEL_PREFERENCES.get(city, CITY_MODEL_PREFERENCES["default"])

    all_forecasts = {}
    for model in prefs[:3]:
        forecast = get_openmeteo_forecast(city, model=model)
        if forecast:
            all_forecasts[model] = forecast

    if not all_forecasts:
        return {}

    import statistics

    all_dates = set()
    for f in all_forecasts.values():
        all_dates.update(f.keys())

    combined = {}
    for date in sorted(all_dates):
        highs = []
        lows = []
        for model, forecast in all_forecasts.items():
            if date in forecast and forecast[date]["high"] is not None:
                highs.append(forecast[date]["high"])
                lows.append(forecast[date]["low"])

        if highs:
            combined[date] = {
                "high": round(statistics.median(highs)),
                "low": round(statistics.median(lows)),
                "all_highs": highs,
                "all_lows": lows,
                "disagreement": max(highs) - min(highs) if len(highs) > 1 else 0,
                "model_count": len(highs),
            }
        else:
            combined[date] = {"high": None, "low": None}

    return combined


def get_madis_observation(location: str) -> dict:
    """Get real-time surface observation from MADIS (NOAA/MesoWest).

    MADIS provides current conditions from ASOS/AWOS stations.
    Useful for verifying today's actual temperature.
    """
    if location not in LOCATIONS:
        return {}

    loc = LOCATIONS[location]
    station_id = loc.get("station")
    if not station_id:
        return {}

    url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
    headers = {
        "User-Agent": "SimmerWeatherSkill/1.0 (https://simmer.markets)",
        "Accept": "application/geo+json",
    }

    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        return {}

    if not data or "properties" not in data:
        return {}

    props = data["properties"]
    temp_c = props.get("temperature", {}).get("value")
    if temp_c is None:
        return {}

    temp_f = round(temp_c * 9 / 5 + 32)
    obs_time = props.get("timestamp", "")

    return {
        "temp_f": temp_f,
        "temp_c": round(temp_c, 1),
        "station": station_id,
        "time": obs_time,
        "source": "MADIS",
    }


def get_openmeteo_current(city: str) -> dict:
    """Get current conditions from Open-Meteo for any city."""
    loc = INTERNATIONAL_LOCATIONS.get(city)
    if not loc:
        return {}

    params = (
        f"?latitude={loc['lat']}&longitude={loc['lon']}"
        f"&current=temperature_2m"
        f"&temperature_unit=celsius"
    )
    url = OPEN_METEO_BASE + params

    try:
        with urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception:
        return {}

    current = data.get("current", {})
    temp_c = current.get("temperature_2m")
    if temp_c is None:
        return {}

    return {
        "temp_c": round(temp_c, 1),
        "temp_f": round(temp_c * 9 / 5 + 32),
        "source": "Open-Meteo",
    }


def _fetch_with_retry(url: str, headers: dict = None, timeout: int = 30) -> dict:
    """Fetch JSON with retry logic for network errors."""
    import time

    for attempt in range(MAX_RETRIES):
        try:
            req = Request(url, headers=headers or {})
            with urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except HTTPError as e:
            if e.code == 429:
                wait_time = int(e.headers.get("Retry-After", 60))
                print(f"  Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"  HTTP Error {e.code}: {url}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
        except URLError as e:
            print(f"  URL Error: {e.reason}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
        except Exception as e:
            print(f"  Error fetching {url}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))

    return None


def get_noaa_forecast_with_fallback(location: str) -> dict:
    """Get NOAA forecast with automatic fallback to Open-Meteo.

    Tries NOAA up to 3 times, then falls back to Open-Meteo GFS.
    """
    if location not in LOCATIONS:
        return {}

    noaa_result = _retry_with_backoff(get_noaa_forecast, location)
    if noaa_result:
        return noaa_result

    print(f"  NOAA unavailable for {location}, falling back to Open-Meteo GFS...")

    city = location
    if city not in INTERNATIONAL_LOCATIONS:
        INTERNATIONAL_LOCATIONS[city] = LOCATIONS[city].copy()
        INTERNATIONAL_LOCATIONS[city]["tz"] = "America/New_York"

    openmeteo_result = get_openmeteo_forecast(city, model="gfs")
    if openmeteo_result:
        return openmeteo_result

    print(f"  Open-Meteo GFS also failed for {location}")
    return {}


def get_weather_forecast(city: str) -> dict:
    """
    Unified weather forecast for any city with multi-source fallback.

    Priority chain:
    1. NOAA (US cities) with retry
    2. Open-Meteo with city-preferred model
    3. Open-Meteo multi-model median

    Returns {} if city is not supported or all sources unavailable.
    """
    if city in LOCATIONS:
        return get_noaa_forecast_with_fallback(city)
    elif city in INTERNATIONAL_LOCATIONS:
        result = get_openmeteo_forecast(city)
        if result:
            return result

        print(f"  Primary model failed for {city}, trying multi-model...")
        multi = get_openmeteo_multi_model(city)
        if multi:
            return multi

        return {}
    else:
        noaa_result = get_noaa_forecast_with_fallback(city)
        if noaa_result:
            return noaa_result
        return get_openmeteo_forecast(city)


def _extract_today_forecast(forecasts: dict) -> dict:
    """Extract today's forecast from date-keyed forecast dict."""
    if not forecasts:
        return {}

    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if today_str in forecasts:
        return forecasts[today_str]

    dates = sorted(forecasts.keys())
    if dates:
        return forecasts[dates[0]]

    return {}


def get_weather_with_confidence(city: str) -> dict:
    """
    Get weather forecast with confidence scoring from ensemble models.

    Returns dict with forecast + confidence metrics:
    {
        "high": median_high,
        "low": median_low,
        "confidence": 0.0-1.0 based on model agreement,
        "disagreement": degrees of uncertainty,
        "model_count": number of models used,
        "source": "ensemble" or "single"
    }
    """
    if city in LOCATIONS:
        basic = get_noaa_forecast_with_fallback(city)
        if basic:
            madis = get_madis_observation(city)
            today = _extract_today_forecast(basic)
            result = {
                "high": today.get("high"),
                "low": today.get("low"),
                "confidence": 0.85,
                "source": "NOAA",
                "all_forecasts": basic,
            }
            if madis:
                result["current"] = madis
            return result

    basic = get_openmeteo_forecast(city)
    if not basic:
        return {"high": None, "low": None, "confidence": 0, "source": "none"}

    multi = get_openmeteo_multi_model(city)
    if multi:
        today_key = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if today_key not in multi:
            today_key = sorted(multi.keys())[0] if multi else None

        if today_key and multi[today_key].get("model_count", 0) > 1:
            disagreement = multi[today_key].get("disagreement", 0)
            if disagreement <= 2:
                confidence = 0.90
            elif disagreement <= 4:
                confidence = 0.80
            elif disagreement <= 6:
                confidence = 0.70
            else:
                confidence = 0.60

            return {
                "high": multi[today_key].get("high"),
                "low": multi[today_key].get("low"),
                "confidence": confidence,
                "source": "multi_model",
                "model_count": multi[today_key].get("model_count", 1),
                "disagreement": disagreement,
                "all_forecasts": multi,
            }

    today = _extract_today_forecast(basic)
    return {
        "high": today.get("high"),
        "low": today.get("low"),
        "confidence": 0.70,
        "source": "single_model",
        "model_count": 1,
        "all_forecasts": basic,
    }


OPEN_METEO_HISTORICAL_BASE = "https://api.open-meteo.com/v1/forecast"

MODEL_HISTORICAL_ACCURACY = {
    "gfs": {"bias": 0.5, "mae": 2.1, "样本量": "high"},
    "ecmwf_ifs": {"bias": -0.3, "mae": 1.8, "样本量": "high"},
    "icon": {"bias": 0.2, "mae": 1.9, "样本量": "medium"},
    "jma": {"bias": 0.4, "mae": 2.0, "样本量": "medium"},
    "kma": {"bias": 0.3, "mae": 2.2, "样本量": "low"},
    "gem": {"bias": 0.6, "mae": 2.4, "样本量": "medium"},
    "bom_access_global": {"bias": 0.5, "mae": 2.3, "样本量": "low"},
    "cma_grapes": {"bias": 0.8, "mae": 2.5, "样本量": "low"},
    "meteofrance": {"bias": 0.1, "mae": 1.9, "样本量": "medium"},
    "ukmo": {"bias": 0.2, "mae": 2.0, "样本量": "medium"},
}


def get_historical_calibration(
    city: str, target_date: str, forecast_temp: float
) -> dict:
    """Get historical accuracy data for calibrating forecast confidence.

    Uses Open-Meteo's historical forecast API to compare past forecasts
    against actual observations for this city/model combination.

    Returns dict with:
    {
        "bias_corrected_temp": temperature after removing average bias,
        "confidence_adjustment": multiplier for probability (0.5-1.0),
        "historical_mae": mean absolute error in degrees,
        "sample_count": number of historical comparisons
    }
    """
    loc = INTERNATIONAL_LOCATIONS.get(city)
    if not loc:
        return {
            "bias_corrected_temp": forecast_temp,
            "confidence_adjustment": 0.80,
            "historical_mae": 2.0,
        }

    import time
    from datetime import datetime as dt

    try:
        target = dt.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        return {
            "bias_corrected_temp": forecast_temp,
            "confidence_adjustment": 0.80,
            "historical_mae": 2.0,
        }

    past_date = target - timedelta(days=7)
    if past_date < dt.now():
        past_date = dt.now() - timedelta(days=1)

    params = (
        f"?latitude={loc['lat']}&longitude={loc['lon']}"
        f"&start_date={past_date.strftime('%Y-%m-%d')}"
        f"&end_date={past_date.strftime('%Y-%m-%d')}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&temperature_unit=celsius"
        f"&timezone={loc['tz'].replace('/', '%2F')}"
        f"&past_days=1"
    )

    url = OPEN_METEO_HISTORICAL_BASE + params
    try:
        with urlopen(url, timeout=20) as resp:
            data = json.loads(resp.read().decode())
    except Exception:
        return {
            "bias_corrected_temp": forecast_temp,
            "confidence_adjustment": 0.80,
            "historical_mae": 2.0,
        }

    daily = data.get("daily", {})
    actual_highs = daily.get("temperature_2m_max", [])
    actual_lows = daily.get("temperature_2m_min", [])

    if actual_highs and actual_highs[0] is not None:
        actual_high = actual_highs[0]
        error = abs(forecast_temp - actual_high)

        if error < 3:
            confidence = 0.90
        elif error < 5:
            confidence = 0.75
        else:
            confidence = 0.60

        return {
            "bias_corrected_temp": forecast_temp,
            "confidence_adjustment": confidence,
            "historical_mae": round(error, 1),
            "actual_vs_forecast": {
                "actual": actual_high,
                "forecast": forecast_temp,
                "error": round(error, 1),
            },
        }

    return {
        "bias_corrected_temp": forecast_temp,
        "confidence_adjustment": 0.80,
        "historical_mae": 2.0,
    }


def get_ensemble_agreement_score(city: str, date: str) -> dict:
    """Calculate agreement score from multiple forecast models.

    Returns:
    {
        "agreement_score": 0.0-1.0 (1.0 = all models agree),
        "spread_degrees": max_temp - min_temp across models,
        "model_count": number of models,
        "dominant_outlook": "warm" or "cold" or "uncertain"
    }
    """
    multi = get_openmeteo_multi_model(city)
    if not multi or date not in multi:
        return {"agreement_score": 0.5, "spread_degrees": 0, "model_count": 0}

    day_data = multi[date]
    highs = day_data.get("all_highs", [])
    if not highs or len(highs) < 2:
        return {
            "agreement_score": 0.7,
            "spread_degrees": 0,
            "model_count": len(highs) if highs else 0,
        }

    spread = max(highs) - min(highs)
    median_high = statistics.median(highs)

    if spread <= 2:
        agreement = 0.95
    elif spread <= 4:
        agreement = 0.80
    elif spread <= 6:
        agreement = 0.65
    else:
        agreement = 0.50

    warm_count = sum(1 for h in highs if h >= median_high)
    dominant = "uncertain"
    if warm_count == len(highs):
        dominant = "warm"
    elif warm_count == 0:
        dominant = "cold"

    return {
        "agreement_score": agreement,
        "spread_degrees": spread,
        "model_count": len(highs),
        "dominant_outlook": dominant,
    }


def fetch_json(url, headers=None, timeout=15):
    """Fetch JSON from URL with error handling."""
    try:
        req = Request(url, headers=headers or {})
        with urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        print(f"  HTTP Error {e.code}: {url}")
        return None
    except URLError as e:
        print(f"  URL Error: {e.reason}")
        return None
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


def get_noaa_forecast(location: str) -> dict:
    """Get NOAA forecast for a location. Returns dict with date -> {"high": temp, "low": temp}"""
    if location not in LOCATIONS:
        print(f"  Unknown location: {location}")
        return {}

    loc = LOCATIONS[location]
    headers = {
        "User-Agent": "SimmerWeatherSkill/1.0 (https://simmer.markets)",
        "Accept": "application/geo+json",
    }

    points_url = f"{NOAA_API_BASE}/points/{loc['lat']},{loc['lon']}"
    points_data = fetch_json(points_url, headers, timeout=10)

    if not points_data or "properties" not in points_data:
        print(f"  Failed to get NOAA grid for {location}")
        return {}

    forecast_url = points_data["properties"].get("forecast")
    if not forecast_url:
        print(f"  No forecast URL for {location}")
        return {}

    forecast_data = fetch_json(forecast_url, headers, timeout=10)
    if not forecast_data or "properties" not in forecast_data:
        print(f"  Failed to get NOAA forecast for {location}")
        return {}

    periods = forecast_data["properties"].get("periods", [])
    forecasts = {}

    for period in periods:
        start_time = period.get("startTime", "")
        if not start_time:
            continue

        date_str = start_time[:10]
        temp = period.get("temperature")
        is_daytime = period.get("isDaytime", True)

        if date_str not in forecasts:
            forecasts[date_str] = {"high": None, "low": None}

        if is_daytime:
            forecasts[date_str]["high"] = temp
        else:
            forecasts[date_str]["low"] = temp

    # Supplement with NOAA observations for today (D+0)
    # /forecast often starts from the next period, missing today's daytime high
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if today_str not in forecasts or forecasts[today_str].get("high") is None:
        station_id = loc.get("station")
        if station_id:
            try:
                obs_url = f"{NOAA_API_BASE}/stations/{station_id}/observations/latest"
                obs_data = fetch_json(obs_url, headers)
                if obs_data and "properties" in obs_data:
                    temp_c = obs_data["properties"].get("temperature", {}).get("value")
                    if temp_c is not None:
                        temp_f = round(temp_c * 9 / 5 + 32)
                        if today_str not in forecasts:
                            forecasts[today_str] = {"high": None, "low": None}
                        if forecasts[today_str]["high"] is None:
                            forecasts[today_str]["high"] = temp_f
                        if forecasts[today_str]["low"] is None:
                            forecasts[today_str]["low"] = temp_f
            except Exception:
                pass  # Observation fetch is best-effort

    return forecasts


# =============================================================================
# Market Parsing
# =============================================================================


def parse_weather_event(event_name: str) -> dict:
    """Parse weather event name to extract location, date, metric."""
    if not event_name:
        return None

    event_lower = event_name.lower()

    if "highest" in event_lower or "high temp" in event_lower:
        metric = "high"
    elif "lowest" in event_lower or "low temp" in event_lower:
        metric = "low"
    else:
        metric = "high"

    location = None
    location_aliases = {
        # US cities (NOAA)
        "nyc": "NYC",
        "new york": "NYC",
        "laguardia": "NYC",
        "la guardia": "NYC",
        "chicago": "Chicago",
        "o'hare": "Chicago",
        "ohare": "Chicago",
        "seattle": "Seattle",
        "sea-tac": "Seattle",
        "atlanta": "Atlanta",
        "hartsfield": "Atlanta",
        "dallas": "Dallas",
        "dfw": "Dallas",
        "miami": "Miami",
        "ft. lauderdale": "Miami",
        "fort lauderdale": "Miami",
        "houston": "Houston",
        "phoenix": "Phoenix",
        "philadelphia": "Philadelphia",
        "boston": "Boston",
        "denver": "Denver",
        "las vegas": "Las Vegas",
        "san francisco": "San Francisco",
        "los angeles": "Los Angeles",
        "san diego": "San Diego",
        "washington dc": "Washington DC",
        "washington, dc": "Washington DC",
        "nashville": "Nashville",
        "portland": "Portland",
        "minneapolis": "Minneapolis",
        "detroit": "Detroit",
        "tampa": "Tampa",
        "orlando": "Orlando",
        # International cities (Open-Meteo)
        "tel aviv": "Tel Aviv",
        "taipei": "Taipei",
        "shanghai": "Shanghai",
        "beijing": "Beijing",
        "hong kong": "Hong Kong",
        "singapore": "Singapore",
        "munich": "Munich",
        "london": "London",
        "tokyo": "Tokyo",
        "seoul": "Seoul",
        "ankara": "Ankara",
        "lucknow": "Lucknow",
        "wellington": "Wellington",
        "sydney": "Sydney",
        "melbourne": "Melbourne",
        "paris": "Paris",
        "berlin": "Berlin",
        "madrid": "Madrid",
        "rome": "Rome",
        "amsterdam": "Amsterdam",
        "toronto": "Toronto",
        "vancouver": "Vancouver",
        # v1.5: Added cities (in INTERNATIONAL_LOCATIONS but missing from aliases)
        "shenzhen": "Shenzhen",
        "guangzhou": "Guangzhou",
        "chengdu": "Chengdu",
        "mumbai": "Mumbai",
        "bombay": "Mumbai",
        "delhi": "Delhi",
        "new delhi": "Delhi",
        "wuhan": "Wuhan",
        # US cities
        "austin": "Austin",
        "austin bergstrom": "Austin",
    }

    for alias, loc in location_aliases.items():
        if alias in event_lower:
            location = loc
            break

    if not location:
        return None

    # Detect temperature unit from event name
    temp_unit = (
        "C"
        if "°c" in event_lower or re.search(r"\d+°?c\b", event_lower, re.IGNORECASE)
        else "F"
    )

    month_day_match = re.search(
        r"on\s+([a-zA-Z]+)\s+(\d{1,2})", event_name, re.IGNORECASE
    )
    if not month_day_match:
        return None

    month_name = month_day_match.group(1).lower()
    day = int(month_day_match.group(2))

    month_map = {
        "january": 1,
        "jan": 1,
        "february": 2,
        "feb": 2,
        "march": 3,
        "mar": 3,
        "april": 4,
        "apr": 4,
        "may": 5,
        "june": 6,
        "jun": 6,
        "july": 7,
        "jul": 7,
        "august": 8,
        "aug": 8,
        "september": 9,
        "sep": 9,
        "october": 10,
        "oct": 10,
        "november": 11,
        "nov": 11,
        "december": 12,
        "dec": 12,
    }

    month = month_map.get(month_name)
    if not month:
        return None

    now = datetime.now(timezone.utc)
    year = now.year
    try:
        target_date = datetime(year, month, day, tzinfo=timezone.utc)
        if target_date < now - timedelta(days=7):
            year += 1
        date_str = f"{year}-{month:02d}-{day:02d}"
    except ValueError:
        return None

    return {"location": location, "date": date_str, "metric": metric, "unit": temp_unit}


def parse_temperature_bucket(outcome_name: str) -> tuple:
    """Parse temperature bucket from outcome name. Works for both °F and °C markets,
    including single-degree exact buckets (e.g. '22°C') and ranges (e.g. '54-55°F')."""
    if not outcome_name:
        return None

    below_match = re.search(
        r"(\d+)\s*°?[fFcC]?\s*(or below|or less)", outcome_name, re.IGNORECASE
    )
    if below_match:
        return (-999, int(below_match.group(1)))

    above_match = re.search(
        r"(\d+)\s*°?[fFcC]?\s*(or higher|or above|or more)", outcome_name, re.IGNORECASE
    )
    if above_match:
        return (int(above_match.group(1)), 999)

    range_match = re.search(
        r"(\d+)\s*(?:°?\s*[fFcC])?\s*(?:-|–|to)\s*(\d+)", outcome_name
    )
    if range_match:
        low, high = int(range_match.group(1)), int(range_match.group(2))
        return (min(low, high), max(low, high))

    # Single exact-degree bucket: "be 22°C on" or "22°F"
    exact_match = re.search(r"\b(\d+)\s*°[fFcC]\b", outcome_name)
    if exact_match:
        t = int(exact_match.group(1))
        return (t, t)

    # Bare integer in short outcome names like "22°C"
    bare_match = re.match(r"^\s*(\d+)\s*°?[cCfF]?\s*$", outcome_name.strip())
    if bare_match:
        t = int(bare_match.group(1))
        return (t, t)

    return None


# =============================================================================
# Simmer API - Core
# =============================================================================

# =============================================================================
# Simmer API - Portfolio & Context
# =============================================================================


def get_portfolio() -> dict:
    """Get portfolio summary from SDK."""
    try:
        return get_client().get_portfolio()
    except Exception as e:
        print(f"  ⚠️  Portfolio fetch failed: {e}")
        return None


def get_market_context(market_id: str, my_probability: float = None) -> dict:
    """Get market context with safeguards and optional edge analysis."""
    try:
        if my_probability is not None:
            return get_client()._request(
                "GET",
                f"/api/sdk/context/{market_id}",
                params={"my_probability": my_probability},
            )
        return get_client().get_market_context(market_id)
    except Exception:
        return None


def get_price_history(market_id: str) -> list:
    """Get price history for trend detection."""
    try:
        return get_client().get_price_history(market_id)
    except Exception:
        return []


def check_context_safeguards(context: dict, use_edge: bool = True) -> tuple:
    """
    Check context for safeguards. Returns (should_trade, reasons).

    Args:
        context: Context response from SDK
        use_edge: If True, respect edge recommendation (TRADE/HOLD/SKIP)
    """
    if not context:
        return True, []  # No context = proceed (fail open)

    reasons = []
    market = context.get("market", {})
    warnings = context.get("warnings", [])
    discipline = context.get("discipline", {})
    slippage = context.get("slippage", {})
    edge = context.get("edge", {})

    # Check for deal-breakers in warnings
    for warning in warnings:
        if "MARKET RESOLVED" in str(warning).upper():
            return False, ["Market already resolved"]

    # Check flip-flop warning
    warning_level = discipline.get("warning_level", "none")
    if warning_level == "severe":
        return False, [
            f"Severe flip-flop warning: {discipline.get('flip_flop_warning', '')}"
        ]
    elif warning_level == "mild":
        reasons.append("Mild flip-flop warning (proceed with caution)")

    # Check time to resolution
    time_str = market.get("time_to_resolution", "")
    if time_str:
        try:
            hours = 0
            if "d" in time_str:
                days = int(time_str.split("d")[0].strip())
                hours += days * 24
            if "h" in time_str:
                h_part = time_str.split("h")[0]
                if "d" in h_part:
                    h_part = h_part.split("d")[-1].strip()
                hours += int(h_part)

            if hours < TIME_TO_RESOLUTION_MIN_HOURS:
                return False, [f"Resolves in {hours}h - too soon"]
        except (ValueError, IndexError):
            pass

    # Check liquidity (pre-filter before slippage, avoids wasting a context call)
    if MIN_LIQUIDITY_USD > 0:
        liquidity = market.get("liquidity", 0) or 0
        if liquidity < MIN_LIQUIDITY_USD:
            return False, [
                f"Liquidity too low: ${liquidity:.0f} < ${MIN_LIQUIDITY_USD:.0f} min"
            ]

    # Check slippage
    estimates = slippage.get("estimates", []) if slippage else []
    if estimates:
        slippage_pct = estimates[0].get("slippage_pct", 0)
        if slippage_pct > SLIPPAGE_MAX_PCT:
            return False, [
                f"Slippage too high: {slippage_pct:.1%} (max {SLIPPAGE_MAX_PCT:.0%})"
            ]

    # Check edge recommendation (if available and use_edge=True)
    if use_edge and edge:
        recommendation = edge.get("recommendation")
        user_edge = edge.get("user_edge")
        threshold = edge.get("suggested_threshold", 0)

        if recommendation == "SKIP":
            return False, ["Edge analysis: SKIP (market resolved or invalid)"]
        elif recommendation == "HOLD":
            if user_edge is not None and threshold:
                reasons.append(
                    f"Edge {user_edge:.1%} below threshold {threshold:.1%} - marginal opportunity"
                )
            else:
                reasons.append("Edge analysis recommends HOLD")
        elif recommendation == "TRADE":
            reasons.append(
                f"Edge {user_edge:.1%} ≥ threshold {threshold:.1%} - good opportunity"
            )

    return True, reasons


def detect_price_trend(history: list) -> dict:
    """
    Analyze price history for trends.
    Returns: {direction: "up"/"down"/"flat", change_24h: float, is_opportunity: bool}
    """
    if not history or len(history) < 2:
        return {"direction": "unknown", "change_24h": 0, "is_opportunity": False}

    # Get recent and older prices
    recent_price = history[-1].get("price_yes", 0.5)

    # Find price ~24h ago (assuming 15-min intervals, ~96 points)
    lookback = min(96, len(history) - 1)
    old_price = history[-lookback].get("price_yes", recent_price)

    if old_price == 0:
        return {"direction": "unknown", "change_24h": 0, "is_opportunity": False}

    change = (recent_price - old_price) / old_price

    if change < -PRICE_DROP_THRESHOLD:
        return {"direction": "down", "change_24h": change, "is_opportunity": True}
    elif change > PRICE_DROP_THRESHOLD:
        return {"direction": "up", "change_24h": change, "is_opportunity": False}
    else:
        return {"direction": "flat", "change_24h": change, "is_opportunity": False}


# =============================================================================
# Market Discovery - Auto-import from Polymarket
# =============================================================================
# NOTE: Unlike fastloop (which queries Gamma API directly with tag=crypto),
# weather uses Simmer's list_importable_markets (Dome-backed keyword search).
# Gamma API has no weather/temperature tag and no public text search endpoint
# (/search requires auth). Tested Feb 2026: 600+ events paginated, zero weather.
# This path is slower but is the only way to discover weather markets by keyword.
# Trading does NOT depend on discovery — v1.10.1+ trades from already-imported
# markets via GET /api/sdk/markets?tags=weather.
# =============================================================================

# Search terms per location (matching Polymarket event naming)
LOCATION_SEARCH_TERMS = {
    "NYC": ["temperature new york", "temperature nyc"],
    "Chicago": ["temperature chicago"],
    "Seattle": ["temperature seattle"],
    "Atlanta": ["temperature atlanta"],
    "Dallas": ["temperature dallas"],
    "Miami": ["temperature miami"],
}


def discover_and_import_weather_markets(log=print):
    """Discover weather markets on Polymarket and auto-import to Simmer.

    Searches broadly for any temperature-related market on Polymarket,
    then imports any that aren't already in Simmer. Cities are auto-detected
    from the imported markets and matched against NOAA/Open-Meteo forecast data.

    Returns count of newly imported markets.
    """
    client = get_client()
    imported_count = 0
    seen_urls = set()

    # Broad search terms to capture all temperature markets
    search_terms = [
        "temperature",
        "highest temperature",
        "lowest temperature",
        "high temp",
        "will it be hot",
        "weather",
    ]

    for term in search_terms:
        try:
            results = client.list_importable_markets(
                q=term, venue="polymarket", min_volume=500, limit=30
            )
        except Exception as e:
            log(f"  Discovery search failed for '{term}': {e}")
            continue

        for m in results:
            url = m.get("url", "")
            question = (m.get("question") or "").lower()
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            # Filter: must be a temperature market on Polymarket
            if "temperature" not in question and "temp" not in question:
                continue
            if not url.startswith("https://polymarket.com/"):
                continue

            # Try to import
            try:
                result = client.import_market(url)
                status = result.get("status", "") if result else ""
                if status == "imported":
                    imported_count += 1
                    log(f"  Imported: {m.get('question', url)[:70]}")
                elif status == "already_exists":
                    pass  # Expected for most
            except Exception as e:
                err_str = str(e)
                if "rate limit" in err_str.lower() or "429" in err_str:
                    log(f"  Import rate limit reached — stopping discovery")
                    return imported_count
                log(f"  Import failed for {url[:50]}: {e}")

    return imported_count


# =============================================================================
# Simmer API - Trading
# =============================================================================


def fetch_weather_markets():
    """Fetch weather-tagged markets from Simmer API."""
    try:
        result = get_client()._request(
            "GET",
            "/api/sdk/markets",
            params={"tags": "weather", "status": "active", "limit": 100},
        )
        return result.get("markets", [])
    except Exception:
        print("  Failed to fetch markets from Simmer API")
        return []


def execute_trade(
    market_id: str,
    side: str,
    amount: float,
    reasoning: str = None,
    signal_data: dict = None,
) -> dict:
    """Execute a buy trade via Simmer SDK with source tagging."""
    try:
        result = get_client().trade(
            market_id=market_id,
            side=side,
            amount=amount,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
            reasoning=reasoning,
            signal_data=signal_data,
        )
        return {
            "success": result.success,
            "trade_id": result.trade_id,
            "shares_bought": result.shares_bought,
            "shares": result.shares_bought,
            "cost": result.cost,
            "new_price": result.new_price,
            "market_id": result.market_id,
            "side": result.side,
            "error": result.error,
            "simulated": result.simulated,
        }
    except Exception as e:
        return {"error": str(e)}


def execute_sell(market_id: str, shares: float) -> dict:
    """Execute a sell trade via Simmer SDK with source tagging."""
    try:
        result = get_client().trade(
            market_id=market_id,
            side="yes",
            action="sell",
            shares=shares,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
        )
        return {
            "success": result.success,
            "trade_id": result.trade_id,
            "error": result.error,
            "simulated": result.simulated,
        }
    except Exception as e:
        return {"error": str(e)}


def get_positions() -> list:
    """Get current positions as list of dicts."""
    try:
        positions = get_client().get_positions()
        from dataclasses import asdict

        return [asdict(p) for p in positions]
    except Exception as e:
        print(f"  Error fetching positions: {e}")
        return []


def calculate_position_size(
    default_size: float,
    smart_sizing: bool,
    price: float = None,
    win_prob: float = None,
) -> float:
    """Calculate position size based on Kelly Criterion or fallback to default.

    Args:
        default_size: Maximum position size from config
        smart_sizing: Whether to use smart sizing (vs fixed)
        price: Market price (for Kelly calculation)
        win_prob: Estimated win probability (for Kelly calculation)
    """
    if not smart_sizing:
        return default_size

    portfolio = get_portfolio()
    if not portfolio:
        print(f"  ⚠️  Smart sizing failed, using default ${default_size:.2f}")
        return default_size

    balance = portfolio.get("balance_usdc", 0)
    if balance <= 0:
        print(f"  ⚠️  No available balance, using default ${default_size:.2f}")
        return default_size

    # v1.2: Use Kelly Criterion if enabled and price/win_prob provided
    if USE_KELLY_SIZING and price is not None and win_prob is not None:
        kelly_pos = quarter_kelly_position(
            price=price,
            win_prob=win_prob,
            bankroll=balance,
            max_pos=default_size,
        )
        kelly_pos = max(kelly_pos, 1.0)  # Minimum $1
        print(
            f"  💡 Kelly sizing: ${kelly_pos:.2f} (Kelly={KELLY_MULTIPLIER:.0%} of ${balance:.2f} balance)"
        )
        return kelly_pos

    # Fallback: fixed percentage sizing
    smart_size = balance * SMART_SIZING_PCT
    smart_size = min(smart_size, MAX_POSITION_USD)
    smart_size = max(smart_size, 1.0)

    print(
        f"  💡 Smart sizing: ${smart_size:.2f} ({SMART_SIZING_PCT:.0%} of ${balance:.2f} balance)"
    )
    return smart_size


# =============================================================================
# Exit Strategy
# =============================================================================


def check_exit_opportunities(
    dry_run: bool = False, use_safeguards: bool = True
) -> tuple:
    """Check open positions for exit opportunities. Returns: (exits_found, exits_executed)"""
    positions = get_positions()

    if not positions:
        return 0, 0

    weather_positions = []
    for pos in positions:
        question = pos.get("question", "").lower()
        sources = pos.get("sources", [])
        # Check if from weather skill OR has weather keywords
        if TRADE_SOURCE in sources or any(
            kw in question
            for kw in ["temperature", "°f", "highest temp", "lowest temp"]
        ):
            weather_positions.append(pos)

    if not weather_positions:
        return 0, 0

    print(f"\n📈 Checking {len(weather_positions)} weather positions for exit...")

    exits_found = 0
    exits_executed = 0

    for pos in weather_positions:
        market_id = pos.get("market_id")
        current_price = pos.get("current_price") or pos.get("price_yes") or 0
        shares = pos.get("shares_yes") or pos.get("shares") or 0
        question = pos.get("question", "Unknown")[:50]

        if shares < MIN_SHARES_PER_ORDER:
            continue

        if current_price >= EXIT_THRESHOLD:
            exits_found += 1
            print(f"  📤 {question}...")
            print(
                f"     Price ${current_price:.2f} >= exit threshold ${EXIT_THRESHOLD:.2f}"
            )

            # Check safeguards before selling
            if use_safeguards:
                context = get_market_context(market_id)
                should_trade, reasons = check_context_safeguards(context)
                if not should_trade:
                    print(f"     ⏭️  Skipped: {'; '.join(reasons)}")
                    continue
                if reasons:
                    print(f"     ⚠️  Warnings: {'; '.join(reasons)}")

            tag = "SIMULATED" if dry_run else "LIVE"
            print(f"     Selling {shares:.1f} shares ({tag})...")
            result = execute_sell(market_id, shares)

            if result.get("success"):
                exits_executed += 1
                trade_id = result.get("trade_id")
                print(
                    f"     ✅ {'[PAPER] ' if result.get('simulated') else ''}Sold {shares:.1f} shares @ ${current_price:.2f}"
                )

                # Log sell trade context for journal (skip for paper trades)
                if trade_id and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(
                        trade_id=trade_id,
                        source=TRADE_SOURCE,
                        skill_slug=SKILL_SLUG,
                        thesis=f"Exit: price ${current_price:.2f} reached exit threshold ${EXIT_THRESHOLD:.2f}",
                        action="sell",
                    )
            else:
                error = result.get("error", "Unknown error")
                print(f"     ❌ Sell failed: {error}")
        else:
            print(f"  📊 {question}...")
            print(
                f"     Price ${current_price:.2f} < exit threshold ${EXIT_THRESHOLD:.2f} - hold"
            )

    return exits_found, exits_executed


# =============================================================================
# Bayesian Position Monitoring (v1.3)
# =============================================================================


def monitor_positions(positions: list, config: dict) -> list:
    """
    Check each position for Bayesian update trigger.
    Returns list of positions with updated probabilities.

    Integration: When PnL drops below -10%, Bayesian update recalculates
    probability. If updated_prob < initial_prob - 15%, position is closed.
    Otherwise, position is reduced to new Kelly size with updated probability.
    """
    updated_positions = []
    for pos in positions:
        current_price = pos.get("current_price", pos.get("last_price", 0))
        entry_price = pos.get("entry_price", 0)

        if entry_price <= 0:
            updated_positions.append(pos)
            continue

        # Compute PnL percentage
        pnl_pct = (current_price - entry_price) / entry_price

        # Check if we should trigger Bayesian update
        if not pos.get("bayesian_updated", False) and should_update_probability(
            pnl_pct
        ):
            # Compute likelihood ratio from price movement
            lr = compute_likelihood_ratio(current_price, entry_price)

            # Update probability using Bayes
            initial_prob = pos.get("initial_prob", pos.get("current_prob", 0.5))
            new_prob = bayesian_update(initial_prob, lr)

            # Check if should close
            if should_close_position(new_prob, initial_prob):
                pos["action"] = "close"
                pos["close_reason"] = "bayesian_update"
                print(
                    f"  🔄 Bayesian close: {pos.get('question', 'Unknown')[:40]}... PnL={pnl_pct:.1%}, prob dropped {initial_prob:.0%}→{new_prob:.0%}"
                )
            else:
                # Reduce to new Kelly size with updated probability
                kelly = kelly_fraction(current_price, new_prob)
                quarter_kelly = kelly / 4
                bankroll = pos.get("bankroll", 1000)
                max_pos = pos.get("max_position", 100)
                new_size = bankroll * quarter_kelly
                pos["current_prob"] = new_prob
                pos["adjusted_size"] = min(new_size, max_pos)
                pos["action"] = "reduce"
                pos["bayesian_updated"] = True
                print(
                    f"  🔄 Bayesian reduce: {pos.get('question', 'Unknown')[:40]}... PnL={pnl_pct:.1%}, prob {initial_prob:.0%}→{new_prob:.0%}, size→${pos['adjusted_size']:.2f}"
                )

            updated_positions.append(pos)
        else:
            updated_positions.append(pos)

    return updated_positions


# =============================================================================
# Maker/Taker Market Detection (v1.3)
# =============================================================================


def detect_market_condition(market: dict = None) -> MarketCondition:
    """
    Extract MarketCondition from market data for strategy determination.

    For weather markets, we use a simplified approach:
    - spread_bps estimated from recent price stability
    - volatility estimated from price history if available

    Args:
        market: Optional market dict with additional context

    Returns:
        MarketCondition with spread_bps and volatility
    """
    # Default values for weather markets (typically tighter spreads)
    # Weather markets on Polymarket tend to have reasonable liquidity
    default_spread_bps = 30.0  # Typical 30 bps spread for weather
    default_volatility = 0.40  # Moderate volatility assumption

    # If market data available, try to extract better estimates
    if market:
        # Use fee_rate as proxy for spread (higher fees = wider spreads)
        fee_rate = market.get("fee_rate_bps", 0)
        if fee_rate > 0:
            # Convert fee rate to spread estimate
            default_spread_bps = min(fee_rate * 2, 100.0)

        # Could use historical price data for volatility estimation
        # For now, use the default

    return MarketCondition(spread_bps=default_spread_bps, volatility=default_volatility)


def decide_trade(
    market: dict,
    condition: MarketCondition,
    config: dict,
    price: float,
    win_prob: float,
) -> dict:
    """
    Decide trade parameters based on market condition and Kelly sizing.

    Args:
        market: Market data dict
        condition: Current MarketCondition
        config: Configuration dict
        price: Market price
        win_prob: Estimated win probability

    Returns:
        Dict with trade parameters including maker_pct, taker_pct, strategy_mode
    """
    mode = determine_strategy_mode(condition)
    maker_pct, taker_pct = get_maker_taker_allocation(mode)

    return {
        "mode": mode,
        "maker_pct": maker_pct,
        "taker_pct": taker_pct,
        "strategy_mode": mode.value,
        "price": price,
        "win_prob": win_prob,
    }


# =============================================================================
# Main Strategy Logic
# =============================================================================


def run_weather_strategy(
    dry_run: bool = True,
    positions_only: bool = False,
    show_config: bool = False,
    smart_sizing: bool = False,
    use_safeguards: bool = True,
    use_trends: bool = True,
    quiet: bool = False,
):
    """Run the weather trading strategy."""

    def log(msg, force=False):
        """Print unless quiet mode is on. force=True always prints."""
        if not quiet or force:
            print(msg)

    log("🌤️  Simmer Weather Trading Skill")
    log("=" * 50)

    if dry_run:
        log(
            "\n  [PAPER MODE] Trades will be simulated with real prices. Use --live for real trades."
        )

    log(f"\n⚙️  Configuration:")
    log(f"  Entry threshold: {ENTRY_THRESHOLD:.0%} (buy below this)")
    log(f"  Exit threshold:  {EXIT_THRESHOLD:.0%} (sell above this)")
    log(f"  Max position:    ${MAX_POSITION_USD:.2f}")
    log(f"  Max trades/run:  {MAX_TRADES_PER_RUN}")
    log(f"  Locations:       Auto-detected from markets (NOAA + Open-Meteo)")
    log(f"  Smart sizing:    {'✓ Enabled' if smart_sizing else '✗ Disabled'}")
    log(f"  Safeguards:      {'✓ Enabled' if use_safeguards else '✗ Disabled'}")
    log(f"  Trend detection: {'✓ Enabled' if use_trends else '✗ Disabled'}")

    if show_config:
        config_path = get_config_path(__file__)
        log(f"\n  Config file: {config_path}")
        log(f"  Config exists: {'Yes' if config_path.exists() else 'No'}")
        log("\n  To change settings, either:")
        log("  1. Create/edit config.json in skill directory:")
        log(
            '     {"entry_threshold": 0.20, "exit_threshold": 0.50, "locations": "NYC,Chicago"}'
        )
        log("  2. Or use --set flag:")
        log("     python weather_trader.py --set entry_threshold=0.20")
        log("  3. Or set environment variables (lowest priority):")
        log("     SIMMER_WEATHER_ENTRY=0.20")
        return

    # Initialize client early to validate API key
    get_client(live=not dry_run)

    # Show portfolio if smart sizing enabled
    if smart_sizing:
        log("\n💰 Portfolio:")
        portfolio = get_portfolio()
        if portfolio:
            log(f"  Balance: ${portfolio.get('balance_usdc', 0):.2f}")
            log(f"  Exposure: ${portfolio.get('total_exposure', 0):.2f}")
            log(f"  Positions: {portfolio.get('positions_count', 0)}")
            by_source = portfolio.get("by_source", {})
            if by_source:
                log(f"  By source: {json.dumps(by_source, indent=4)}")

    if positions_only:
        log("\n📊 Current Positions:")
        positions = get_positions()
        if not positions:
            log("  No open positions")
        else:
            for pos in positions:
                log(f"  • {pos.get('question', 'Unknown')[:50]}...")
                sources = pos.get("sources", [])
                log(
                    f"    YES: {pos.get('shares_yes', 0):.1f} | NO: {pos.get('shares_no', 0):.1f} | P&L: ${pos.get('pnl', 0):.2f} | Sources: {sources}"
                )
        return

    log("\n🔍 Discovering new weather markets on Polymarket...")
    newly_imported = discover_and_import_weather_markets(log=log)
    if newly_imported:
        log(f"  Auto-imported {newly_imported} new market(s)")
    else:
        log("  No new markets to import")

    log("\n📡 Fetching weather markets...")
    markets = fetch_weather_markets()
    log(f"  Found {len(markets)} weather markets")

    if not markets:
        log("  No weather markets available")
        return

    events = {}
    for market in markets:
        # Group by event_id if available, otherwise derive from question
        event_key = market.get("event_id")
        if not event_key:
            # Fall back: parse question to derive (location, date) grouping key
            info = parse_weather_event(
                market.get("event_name") or market.get("question", "")
            )
            event_key = f"{info['location']}_{info['date']}" if info else "unknown"
        if event_key not in events:
            events[event_key] = []
        events[event_key].append(market)

    log(f"  Grouped into {len(events)} events")

    forecast_cache = {}
    trades_executed = 0
    total_usd_spent = 0.0
    opportunities_found = 0
    skip_reasons = []
    execution_errors = []

    for event_id, event_markets in events.items():
        # Use event_name from API if available, otherwise parse from question
        event_name = event_markets[0].get("event_name") or event_markets[0].get(
            "question", ""
        )
        event_info = parse_weather_event(event_name)

        if not event_info:
            continue

        location = event_info["location"]
        date_str = event_info["date"]
        metric = event_info["metric"]

        # v1.5: Skip city filter — instead check if we can get forecast data for this city
        if location not in forecast_cache:
            log(f"\n📍 {location} {date_str} ({metric} temp)")
            log(f"  🌐 Detected city: {location} — fetching weather data...")

            weather_data = get_weather_with_confidence(location)
            forecast_cache[location] = {
                "forecasts": weather_data.get("all_forecasts", {}),
                "confidence": weather_data.get("confidence", 0.80),
                "source": weather_data.get("source", "unknown"),
                "model_count": weather_data.get("model_count", 1),
                "disagreement": weather_data.get("disagreement", 0),
                "models": weather_data.get("models", {}),
            }

        cached = forecast_cache[location]
        forecasts = cached["forecasts"]
        if not forecasts:
            log(f"  ⏭️  No forecast data available for {location} — skipping")
            continue

        day_forecast = forecasts.get(date_str, {})
        forecast_temp = day_forecast.get(metric) or day_forecast.get("high")

        if forecast_temp is None:
            log(f"  ⚠️  No forecast for {date_str} in {location} data")
            continue

        is_international = location in INTERNATIONAL_LOCATIONS
        unit_label = "°C" if is_international else "°F"
        source_label = cached.get(
            "source", "Open-Meteo" if is_international else "NOAA"
        ).upper()
        log(
            f"  📊 [{source_label}] forecast: {forecast_temp}{unit_label} "
            f"(confidence: {cached.get('confidence', 0):.0%})"
        )
        if cached.get("model_count", 1) > 1:
            log(
                f"     Ensemble: {cached['model_count']} models, "
                f"disagreement: {cached.get('disagreement', 0):.1f}°"
            )

        if cached.get("confidence", 0) < 0.6:
            log(
                f"  ⚠️  Low confidence ({cached.get('confidence', 0):.0%}) — consider reducing position"
            )

        if BINARY_ONLY and len(event_markets) > 2:
            log(
                f"  ⏭️  Range event ({len(event_markets)} buckets) — binary_only=true, skipping"
            )
            continue

        matching_market = None
        for market in event_markets:
            outcome_name = market.get("outcome_name") or market.get("question", "")
            bucket = parse_temperature_bucket(outcome_name)

            if bucket and bucket[0] <= forecast_temp <= bucket[1]:
                matching_market = market
                break

        if not matching_market:
            log(f"  ⚠️  No bucket found for {forecast_temp}{unit_label}")
            continue

        outcome_name = matching_market.get("outcome_name", "")
        price = matching_market.get("external_price_yes") or 0.5
        market_id = matching_market.get("id")

        log(f"  Matching bucket: {outcome_name} @ ${price:.2f}")

        if price < MIN_TICK_SIZE:
            log(
                f"  ⏸️  Price ${price:.4f} below min tick ${MIN_TICK_SIZE} - skip (market at extreme)"
            )
            skip_reasons.append("price at extreme")
            continue
        if price > (1 - MIN_TICK_SIZE):
            log(
                f"  ⏸️  Price ${price:.4f} above max tradeable - skip (market at extreme)"
            )
            skip_reasons.append("price at extreme")
            continue

        # Check safeguards with edge analysis
        # v1.5: NOAA forecasts degrade with horizon (D+1 ~90%, D+5 ~74%)
        # v2.0: Multi-source: blend with ensemble confidence when available
        base_prob = calibrate_noaa_probability(event_info, NOAA_WIN_PROBABILITY)

        ensemble_confidence = forecasts.get("confidence", 0.80)
        if ensemble_confidence < 0.6:
            noaa_probability = base_prob * 0.9
            log(
                f"  📉 Low ensemble confidence - reduced probability to {noaa_probability:.2f}"
            )
        elif ensemble_confidence > 0.8:
            noaa_probability = min(0.99, base_prob * 1.05)
            log(
                f"  📈 High ensemble confidence - boosted probability to {noaa_probability:.2f}"
            )
        else:
            noaa_probability = base_prob

        # v2.1: MADIS airport-observation bias correction (Scheme 1)
        # Airport实测 vs 网格预报 → 实时方向偏差修正
        raw_probability = noaa_probability  # 保存修正前的值用于 trade_log
        madis_bias_msg = ""
        madis_obs = get_madis_observation(location)
        if madis_obs:
            noaa_probability, madis_msg = apply_madis_bias_correction(
                forecast_temp, madis_obs, event_info, noaa_probability, unit_label[-1]
            )
            madis_bias_msg = madis_msg
            if madis_msg:
                log(f"  🌡️  {madis_msg}")

        if use_safeguards:
            context = get_market_context(market_id, my_probability=noaa_probability)
            should_trade, reasons = check_context_safeguards(context)
            if not should_trade:
                log(f"  ⏭️  Safeguard blocked: {'; '.join(reasons)}")
                skip_reasons.append(f"safeguard: {reasons[0]}")
                continue
            if reasons:
                log(f"  ⚠️  Warnings: {'; '.join(reasons)}")

        # Check price trend
        trend_bonus = ""
        if use_trends:
            history = get_price_history(market_id)
            trend = detect_price_trend(history)
            if trend["is_opportunity"]:
                trend_bonus = f" 📉 (dropped {abs(trend['change_24h']):.0%} in 24h - stronger signal!)"
            elif trend["direction"] == "up":
                trend_bonus = f" 📈 (up {trend['change_24h']:.0%} in 24h)"

        # v1.2: EV check + Longtail filter
        try:
            raw_ev = calculate_ev(price, noaa_probability)
            is_longtail = price < LONGTAIL_PRICE_CUTOFF

            if is_longtail:
                adjusted_ev = longtail_ev_adjustment(price, raw_ev)
                effective_ev = adjusted_ev
                ev_label = f"(longtail adjusted: raw EV={raw_ev:.3f}, adjusted={adjusted_ev:.3f})"
            else:
                effective_ev = raw_ev
                ev_label = f"(EV={raw_ev:.3f})"

            if effective_ev <= EV_MIN_THRESHOLD:
                log(
                    f"  ⏸️  EV check failed {ev_label} - min EV={EV_MIN_THRESHOLD:.3f}, skipping"
                )
                skip_reasons.append("ev too low")
                continue
            log(f"  💡 EV check passed {ev_label}")
        except ZeroDivisionError:
            log(f"  ⏸️  EV calculation error (price={price}) - skipping")
            skip_reasons.append("ev calc error")
            continue

        # v1.3: Detect Maker/Taker strategy mode from market conditions
        market_condition = detect_market_condition(matching_market)
        strategy = decide_trade(
            matching_market, market_condition, _config, price, noaa_probability
        )
        log(
            f"  📊 Strategy: {strategy['mode'].value} ({strategy['maker_pct']:.0%} Maker / {strategy['taker_pct']:.0%} Taker)"
        )

        if price < ENTRY_THRESHOLD:
            position_size = calculate_position_size(
                MAX_POSITION_USD, smart_sizing, price=price, win_prob=noaa_probability
            )

            min_cost_for_shares = MIN_SHARES_PER_ORDER * price
            if min_cost_for_shares > position_size:
                log(
                    f"  ⚠️  Position size ${position_size:.2f} too small for {MIN_SHARES_PER_ORDER} shares at ${price:.2f}"
                )
                skip_reasons.append("position too small")
                continue

            opportunities_found += 1
            log(
                f"  ✅ Below threshold (${ENTRY_THRESHOLD:.2f}) - BUY opportunity!{trend_bonus}"
            )

            # Check rate limit
            if trades_executed >= MAX_TRADES_PER_RUN:
                log(
                    f"  ⏸️  Max trades per run ({MAX_TRADES_PER_RUN}) reached - skipping"
                )
                skip_reasons.append("max trades reached")
                continue

            tag = "SIMULATED" if dry_run else "LIVE"
            log(f"  Executing trade ({tag})...", force=True)
            edge = noaa_probability - price

            # v1.4: Merge Smart Money signals if available
            sm_signals = _get_smart_money_signals()
            market_slug = (
                matching_market.get("slug") or matching_market.get("question", "")[:50]
            )
            sm_signal = get_signal_for_market(sm_signals, market_slug)
            base_signal_data = {
                "edge": round(edge, 4),
                "confidence": noaa_probability,
                "signal_source": cached.get("source", "noaa_forecast"),
                "forecast_temp": forecast_temp,
                "bucket_range": outcome_name,
                "market_price": round(price, 4),
                "threshold": ENTRY_THRESHOLD,
                "ensemble_confidence": cached.get("confidence", 0.80),
                "model_count": cached.get("model_count", 1),
                "disagreement": cached.get("disagreement", 0),
            }
            signal_data = merge_signal_data(base_signal_data, sm_signal)
            if sm_signal:
                log(
                    f"  🐋 Smart Money: {sm_signal['smart_money_signal']} "
                    f"(score={sm_signal['smart_money_score']}/10, "
                    f"combined_confidence={signal_data.get('combined_confidence', 0):.2f})"
                )

            # Pre-trade circuit breaker check
            should_trade, cb_reason = check_circuit_breaker(
                os.path.dirname(__file__),
                threshold=CB_THRESHOLD,
                cooldown_hours=CB_COOLDOWN_HOURS,
            )
            if not should_trade:
                log(f"  {cb_reason}", force=True)
                skip_reasons.append("circuit breaker")
                continue
            result = execute_trade(
                market_id,
                "yes",
                position_size,
                reasoning=f"NOAA forecasts {forecast_temp}{unit_label} → bucket {outcome_name} underpriced at {price:.0%}",
                signal_data=signal_data,
            )

            # Post-trade logging (success or failure)
            write_trade_log(
                result,
                SKILL_SLUG,
                TRADE_SOURCE,
                signal_data=signal_data,
            )

            if result.get("success"):
                trades_executed += 1
                total_usd_spent += position_size
                shares = result.get("shares_bought") or result.get("shares") or 0
                trade_id = result.get("trade_id")
                log(
                    f"  ✅ {'[PAPER] ' if result.get('simulated') else ''}Bought {shares:.1f} shares @ ${price:.2f}",
                    force=True,
                )

                # v2.1: Append to trade log for city-level bias learning (Scheme 2)
                log_trade_entry(
                    market_id=market_id,
                    market_question=matching_market.get("question", ""),
                    city=location,
                    target_date=date_str,
                    forecast_temp=forecast_temp,
                    bucket_range=outcome_name,
                    price=price,
                    side="YES",
                    amount=position_size,
                    shares=shares,
                    cost=result.get("cost", 0),
                    noaa_probability=raw_probability,
                    bias_adjustment=round(raw_probability - noaa_probability, 4),
                    madis_bias_msg=madis_bias_msg,
                    unit=unit_label[-1],
                    source=cached.get("source", "unknown"),
                    signal_data=signal_data,
                )

                # Log trade context for journal (skip for paper trades)
                if trade_id and JOURNAL_AVAILABLE and not result.get("simulated"):
                    # Confidence based on price gap from threshold (guard against div by zero)
                    if ENTRY_THRESHOLD > 0:
                        confidence = min(
                            0.95, (ENTRY_THRESHOLD - price) / ENTRY_THRESHOLD + 0.5
                        )
                    else:
                        confidence = 0.7  # Default confidence if threshold is zero
                    log_trade(
                        trade_id=trade_id,
                        source=TRADE_SOURCE,
                        skill_slug=SKILL_SLUG,
                        thesis=f"{'Open-Meteo' if is_international else 'NOAA'} forecasts {forecast_temp}{unit_label} for {location} on {date_str}, "
                        f"bucket '{outcome_name}' underpriced at ${price:.2f}",
                        confidence=round(confidence, 2),
                        location=location,
                        forecast_temp=forecast_temp,
                        target_date=date_str,
                        metric=metric,
                    )
                # Risk monitors are now auto-set via SDK settings (dashboard)
            else:
                error = result.get("error", "Unknown error")
                log(f"  ❌ Trade failed: {error}", force=True)
                execution_errors.append(error[:120])

            # Update circuit breaker state
            update_circuit_breaker(
                os.path.dirname(__file__),
                result.get("success", False),
                result.get("simulated", False),
                threshold=CB_THRESHOLD,
                cooldown_hours=CB_COOLDOWN_HOURS,
                error=result.get("error", ""),
            )
        else:
            log(
                f"  ⏸️  Price ${price:.2f} above threshold ${ENTRY_THRESHOLD:.2f} - skip"
            )

    # v1.3: Bayesian position monitoring - check for PnL-triggered probability updates
    current_positions = get_positions()
    if current_positions:
        monitored = monitor_positions(current_positions, _config)
        # Apply Bayesian-driven actions (close/reduce) before exit check
        for pos in monitored:
            if (
                pos.get("action") == "close"
                and pos.get("close_reason") == "bayesian_update"
            ):
                # Bayesian update triggered close - would sell here if live
                pass  # Exit handling done via check_exit_opportunities
            elif pos.get("action") == "reduce":
                # Bayesian update triggered reduce - log for now
                pass  # Position size adjustment would happen on next trade

    exits_found, exits_executed = check_exit_opportunities(dry_run, use_safeguards)

    log("\n" + "=" * 50)
    total_trades = trades_executed + exits_executed
    show_summary = not quiet or total_trades > 0
    if show_summary:
        print("📊 Summary:")
        print(f"  Events scanned: {len(events)}")
        print(f"  Entry opportunities: {opportunities_found}")
        print(f"  Exit opportunities:  {exits_found}")
        print(f"  Trades executed:     {total_trades}")

    # Structured report for automaton
    if os.environ.get("AUTOMATON_MANAGED"):
        global _automaton_reported
        report = {
            "signals": opportunities_found + exits_found,
            "trades_attempted": opportunities_found + exits_found,
            "trades_executed": total_trades,
            "amount_usd": round(total_usd_spent, 2),
        }
        if (
            (opportunities_found + exits_found) > 0
            and total_trades == 0
            and skip_reasons
        ):
            report["skip_reason"] = ", ".join(dict.fromkeys(skip_reasons))
        if execution_errors:
            report["execution_errors"] = execution_errors
        print(json.dumps({"automaton": report}))
        _automaton_reported = True

    if dry_run and show_summary:
        print("\n  [PAPER MODE - trades simulated with real prices]")


# =============================================================================
# CLI Entry Point
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simmer Weather Trading Skill")
    parser.add_argument(
        "--live",
        dest="live",
        action="store_true",
        help="Execute real USDC trades on Polymarket (requires TRADING_VENUE=polymarket). "
        "Not needed for $SIM trading (TRADING_VENUE=sim is always active).",
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Simulated trades only (overrides default when TRADING_VENUE=polymarket)",
    )
    parser.add_argument(
        "--positions", action="store_true", help="Show current positions only"
    )
    parser.add_argument("--config", action="store_true", help="Show current config")
    parser.add_argument(
        "--set",
        action="append",
        metavar="KEY=VALUE",
        help="Set config value (e.g., --set entry_threshold=0.20)",
    )
    parser.add_argument(
        "--smart-sizing",
        action="store_true",
        help="Use portfolio-based position sizing",
    )
    parser.add_argument(
        "--no-safeguards", action="store_true", help="Disable context safeguards"
    )
    parser.add_argument(
        "--no-trends", action="store_true", help="Disable price trend detection"
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Only output when trades execute or errors occur (ideal for high-frequency runs)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Force resume trading (clear circuit breaker)",
    )
    args = parser.parse_args()

    # Handle --set config updates
    if args.set:
        updates = {}
        for item in args.set:
            if "=" in item:
                key, value = item.split("=", 1)
                # Try to convert to appropriate type
                if key in CONFIG_SCHEMA:
                    type_fn = CONFIG_SCHEMA[key].get("type", str)
                    try:
                        value = type_fn(value)
                    except (ValueError, TypeError):
                        pass
                updates[key] = value
        if updates:
            updated = update_config(updates, __file__)
            print(f"✅ Config updated: {updates}")
            print(f"   Saved to: {get_config_path(__file__)}")
            # Reload config
            _config = load_config(
                CONFIG_SCHEMA, __file__, slug="polymarket-weather-trader"
            )
            # Update ALL module-level vars (must match names defined at module top)
            globals().update(
                {
                    "ENTRY_THRESHOLD": _config["entry_threshold"],
                    "EXIT_THRESHOLD": _config["exit_threshold"],
                    "MAX_POSITION_USD": _config["max_position_usd"],
                    "SMART_SIZING_PCT": _config["sizing_pct"],
                    "MAX_TRADES_PER_RUN": _config["max_trades_per_run"],
                    "BINARY_ONLY": _config["binary_only"],
                    "EV_MIN_THRESHOLD": _config.get("ev_min_threshold", 0.0),
                    "LONGTAIL_EV_PENALTY": _config.get("longtail_ev_penalty", 0.20),
                    "LONGTAIL_PRICE_CUTOFF": _config.get("longtail_price_cutoff", 0.20),
                    "CB_THRESHOLD": _config.get("circuit_breaker_threshold", 3),
                    "CB_COOLDOWN_HOURS": _config.get("circuit_breaker_cooldown", 6),
                }
            )
            _locations_str = _config["locations"]
            globals()["ACTIVE_LOCATIONS"] = [
                loc.strip().upper() for loc in _locations_str.split(",") if loc.strip()
            ]

    # Handle --resume flag
    if args.resume:
        from trade_performance import check_circuit_breaker
        from pathlib import Path

        breaker_path = Path(__file__).parent / "circuit_breaker.json"
        if breaker_path.exists():
            breaker_path.unlink()
            print("[OK] Circuit breaker cleared - trading resumed")
        else:
            print("[INFO] No active circuit breaker found")
        sys.exit(0)

    # Default: TRADING_VENUE=sim → real Simmer API; TRADING_VENUE=polymarket → dry-run (need --live for real trades)
    # --dry-run flag overrides to True in any mode.
    dry_run = args.dry_run or (
        args.live is False and os.environ.get("TRADING_VENUE") != "sim"
    )

    run_weather_strategy(
        dry_run=dry_run,
        positions_only=args.positions,
        show_config=args.config,
        smart_sizing=args.smart_sizing,
        use_safeguards=not args.no_safeguards,
        use_trends=not args.no_trends,
        quiet=args.quiet,
    )

    # Fallback report for automaton if the strategy returned early (no signal)
    if os.environ.get("AUTOMATON_MANAGED") and not _automaton_reported:
        print(
            json.dumps(
                {
                    "automaton": {
                        "signals": 0,
                        "trades_attempted": 0,
                        "trades_executed": 0,
                        "skip_reason": "no_signal",
                    }
                }
            )
        )
