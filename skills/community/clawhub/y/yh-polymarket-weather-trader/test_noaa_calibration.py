"""
Tests for v1.5 NOAA horizon-based probability calibration.
"""

import sys
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

sys.path.insert(0, ".")
from weather_trader import (
    NOAA_HORIZON_ACCURACY,
    get_forecast_horizon,
    calibrate_noaa_probability,
)


def test_horizon_accuracy_table_has_all_keys():
    """NOAA_HORIZON_ACCURACY covers keys 0-7."""
    for i in range(8):
        assert i in NOAA_HORIZON_ACCURACY, f"Missing horizon {i}"
    # Values should decrease with horizon
    for i in range(1, 8):
        assert NOAA_HORIZON_ACCURACY[i] < NOAA_HORIZON_ACCURACY[i - 1], (
            f"Horizon {i} should be less accurate than {i - 1}"
        )


def test_get_forecast_horizon_today():
    """D+0 (today) returns 0."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    info = {"date": today}
    assert get_forecast_horizon(info) == 0


def test_get_forecast_horizon_tomorrow():
    """D+1 (tomorrow) returns 1."""
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")
    info = {"date": tomorrow}
    assert get_forecast_horizon(info) == 1


def test_get_forecast_horizon_d3():
    """D+3 returns 3."""
    d3 = (datetime.now(timezone.utc) + timedelta(days=3)).strftime("%Y-%m-%d")
    info = {"date": d3}
    assert get_forecast_horizon(info) == 3


def test_get_forecast_horizon_d7():
    """D+7 returns 7."""
    d7 = (datetime.now(timezone.utc) + timedelta(days=7)).strftime("%Y-%m-%d")
    info = {"date": d7}
    assert get_forecast_horizon(info) == 7


def test_get_forecast_horizon_unknown():
    """Missing date returns 1 (safe default)."""
    assert get_forecast_horizon(None) == 1
    assert get_forecast_horizon({}) == 1
    assert get_forecast_horizon({"location": "NYC"}) == 1


def test_calibrate_noaa_probability_d1():
    """D+1 calibrated prob should reflect higher accuracy (0.90 base)."""
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")
    info = {"date": tomorrow}
    result = calibrate_noaa_probability(info, base_prob=0.85)
    # D+1 accuracy is 0.90; ratio = 0.90/0.85 ≈ 1.059; 0.85 * 1.059 ≈ 0.90
    assert 0.88 <= result <= 0.95


def test_calibrate_noaa_probability_d5():
    """D+5 calibrated prob should reflect lower accuracy (0.74 base)."""
    d5 = (datetime.now(timezone.utc) + timedelta(days=5)).strftime("%Y-%m-%d")
    info = {"date": d5}
    result = calibrate_noaa_probability(info, base_prob=0.85)
    # D+5 accuracy is 0.74; ratio = 0.74/0.85 ≈ 0.871; 0.85 * 0.871 ≈ 0.74
    assert 0.70 <= result <= 0.78


def test_calibrate_noaa_probability_d7():
    """D+7 calibrated prob should be lowest (0.66 base)."""
    d7 = (datetime.now(timezone.utc) + timedelta(days=7)).strftime("%Y-%m-%d")
    info = {"date": d7}
    result = calibrate_noaa_probability(info, base_prob=0.85)
    assert 0.62 <= result <= 0.70


def test_calibrate_noaa_probability_today():
    """D+0 calibrated prob should be highest (0.95 base)."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    info = {"date": today}
    result = calibrate_noaa_probability(info, base_prob=0.85)
    assert 0.92 <= result <= 0.99


def test_calibrate_noaa_probability_bounded():
    """Calibrated probability stays within [0.01, 0.99]."""
    for days in [0, 1, 3, 5, 7, 14]:
        d = (datetime.now(timezone.utc) + timedelta(days=days)).strftime("%Y-%m-%d")
        result = calibrate_noaa_probability({"date": d}, base_prob=0.85)
        assert 0.01 <= result <= 0.99


def test_calibrate_noaa_probability_none_event_info():
    """None event_info returns safe default near base_prob."""
    result = calibrate_noaa_probability(None, base_prob=0.85)
    assert 0.80 <= result <= 0.90


def test_calibrate_noaa_probability_custom_base():
    """Custom base_prob is respected in scaling."""
    d3 = (datetime.now(timezone.utc) + timedelta(days=3)).strftime("%Y-%m-%d")
    info = {"date": d3}
    result = calibrate_noaa_probability(info, base_prob=0.80)
    # D+3 accuracy 0.82 / 0.80 = 1.025; 0.80 * 1.025 ≈ 0.82
    assert 0.78 <= result <= 0.86
