"""Normalized data schema and safe defaults for scoring and reporting."""

from __future__ import annotations

from typing import Any

# Keys required after normalization (collect or defaults).
REQUIRED_SCORE_KEYS: frozenset[str] = frozenset(
    {
        "ticker",
        "error",
        "timestamp",
        "price",
        "pe",
        "roe",
        "debt",
        "div_yield",
        "rsi",
        "vol",
        "news",
        "sector",
        "sharpe",
        "macd",
        "analyst_target",
        "rating_mean",
        "beta",
        "eps_growth",
        "vix",
        "spy_mom",
        "peers",
        "peer_score",
        "hy_spread",
        "yield_curve",
        "iv",
        "fear_greed",
        "shortRatio",
        "impliedVolatility",
    }
)


def fear_greed_from_vix(vix: float) -> int:
    """
    Proxy Fear & Greed when CNN index is unavailable.
    Lower VIX -> higher greed (bounded 0–100).
    """
    raw = 50.0 - (float(vix) - 20.0) * 2.0
    return int(max(0, min(100, round(raw))))


def normalize_collect_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Fill missing optional keys so score.py never KeyErrors on real provider gaps.
    Mutates and returns the same dict for convenience.
    """
    defaults: dict[str, Any] = {
        "pe": 999.0,
        "roe": 0.0,
        "debt": 999.0,
        "div_yield": 0.0,
        "rsi": 50.0,
        "vol": 0.0,
        "news": [],
        "sector": None,
        "sharpe": 0.0,
        "macd": "bear",
        "analyst_target": 0.0,
        "rating_mean": 3.0,
        "beta": 1.0,
        "eps_growth": 0.0,
        "vix": 20.0,
        "spy_mom": 0.0,
        "peers": "N/A",
        "peer_score": 0,
        "hy_spread": 350.0,
        "yield_curve": 0.0,
        "iv": 0.35,
        "shortRatio": 0.1,
        "impliedVolatility": 0.3,
    }
    for k, v in defaults.items():
        if k not in data or data[k] is None:
            data[k] = v
    if not isinstance(data.get("news"), list):
        data["news"] = []
    data["news"] = [str(n) for n in data["news"] if n]
    # Ensure fear_greed numeric if only vix was present
    if "fear_greed" not in data or data["fear_greed"] is None:
        data["fear_greed"] = fear_greed_from_vix(float(data.get("vix", 20)))
    return data


def empty_backtest() -> dict[str, Any]:
    """Neutral backtest dict when stats unavailable."""
    return {
        "strategy_cagr": float("nan"),
        "strategy_sharpe": float("nan"),
        "strategy_max_dd": float("nan"),
        "bh_cagr": float("nan"),
        "bh_sharpe": float("nan"),
        "bh_max_dd": float("nan"),
        "spy_cagr": float("nan"),
        "alpha_vs_spy": float("nan"),
        "win_rate": float("nan"),
        "trades": float("nan"),
    }
