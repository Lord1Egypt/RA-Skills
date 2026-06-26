"""7-day forward return estimate with RandomForest on recent returns (optional ML)."""

from __future__ import annotations

from typing import Any

import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor

from tai_alpha.yfinance_utils import close_series, ensure_datetime_index


def predict_7d_return_from_collect(raw: dict[str, Any]) -> float | None:
    """
    Predict next-step 7-day cumulative return from past daily returns.
    Returns a single float (e.g. 0.03) or None if insufficient data.
    """
    if raw.get("error"):
        return None
    meta = raw.get("adapter_meta") or {}
    ticker = str(meta.get("symbol_resolved") or raw.get("ticker", ""))
    if not ticker:
        return None
    hist = yf.download(ticker, period="120d", progress=False)
    close = close_series(hist, ticker)
    close = ensure_datetime_index(close).dropna()
    if len(close) < 30:
        return None

    r = close.pct_change().dropna()
    if len(r) < 25:
        return None

    # Target: 7-day forward return from each day
    y = (close.shift(-7) / close - 1.0).dropna()
    X = r.to_frame("r")
    aligned = X.join(y.rename("target"), how="inner").dropna()
    if len(aligned) < 20:
        return None

    X_train = aligned[["r"]].values[:-1]
    y_train = aligned["target"].values[:-1]

    model = RandomForestRegressor(
        n_estimators=50, max_depth=4, random_state=42, n_jobs=1
    )
    model.fit(X_train, y_train)
    last_r = np.array([[float(r.iloc[-1])]])
    pred = float(model.predict(last_r)[0])
    if np.isnan(pred) or np.isinf(pred):
        return None
    return max(-0.5, min(0.5, pred))
