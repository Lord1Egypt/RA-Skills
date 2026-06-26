from __future__ import annotations

import time

import numpy as np
import pandas as pd
import pytest

from src.data.utils import (
    RealtimeCache,
    calculate_chip_from_daily,
    safe_float,
)


class TestSafeFloat:
    def test_normal_value(self):
        assert safe_float(3.14) == 3.14

    def test_string_value(self):
        assert safe_float("2.5") == 2.5

    def test_none_returns_default(self):
        assert safe_float(None) == 0.0
        assert safe_float(None, default=-1.0) == -1.0

    def test_empty_string_returns_default(self):
        assert safe_float("") == 0.0

    def test_dash_returns_default(self):
        assert safe_float("-") == 0.0

    def test_invalid_string_returns_default(self):
        assert safe_float("abc") == 0.0

    def test_zero_value(self):
        assert safe_float(0) == 0.0

    def test_negative_value(self):
        assert safe_float(-5.5) == -5.5


class TestRealtimeCache:
    def test_empty_cache_returns_none(self):
        cache = RealtimeCache(ttl=600)
        assert cache.get() is None

    def test_set_and_get(self):
        cache = RealtimeCache(ttl=600)
        df = pd.DataFrame({"close": [10.0, 20.0]})
        cache.set(df)
        result = cache.get()
        assert result is not None
        assert len(result) == 2

    def test_expired_cache_returns_none(self):
        cache = RealtimeCache(ttl=0)
        df = pd.DataFrame({"close": [10.0]})
        cache.set(df)

        cache._timestamp = time.time() - 10
        assert cache.get() is None


class TestCalculateChipFromDaily:
    def test_none_df(self):
        assert calculate_chip_from_daily(None) is None

    def test_empty_df(self):
        df = pd.DataFrame()
        assert calculate_chip_from_daily(df) is None

    def test_insufficient_data(self):
        df = pd.DataFrame({"close": [10.0, 11.0], "volume": [100, 200]})
        assert calculate_chip_from_daily(df) is None

    def test_valid_data(self):
        df = pd.DataFrame({
            "close": [10.0] * 5 + [12.0] * 5 + [15.0] * 5,
            "volume": [1000] * 15,
        })
        result = calculate_chip_from_daily(df)
        assert result is not None
        assert isinstance(result.profit_ratio, float)
        assert isinstance(result.avg_cost, float)
        assert isinstance(result.concentration, float)

    def test_zero_volume(self):
        df = pd.DataFrame({
            "close": [10.0] * 15,
            "volume": [0] * 15,
        })
        assert calculate_chip_from_daily(df) is None
