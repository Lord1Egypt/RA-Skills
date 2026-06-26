"""Equal-weight portfolio simulation from multiple tickers (real pipeline per name)."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from tai_alpha.pipeline import run_analyze


def simulate_top_n(
    tickers: list[str],
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    """
    Run analyze for each ticker in an isolated temp database and aggregate
    equal-weight average conviction and strategy CAGR.
    """
    _ = root  # reserved for future workspace roots
    results: list[dict[str, Any]] = []
    for t in tickers:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            db_path = Path(tmp.name)
        try:
            out = run_analyze(t, db_path, print_report=False)
            if out.get("signal") == "ERROR":
                results.append(
                    {
                        "ticker": t,
                        "error": out.get("risks", ["unknown"])[0],
                    }
                )
                continue
            bt = out.get("backtest") or {}
            results.append(
                {
                    "ticker": t,
                    "conviction": out.get("conviction"),
                    "signal": out.get("signal"),
                    "strategy_cagr": bt.get("strategy_cagr"),
                    "alpha_vs_spy": bt.get("alpha_vs_spy"),
                }
            )
        finally:
            db_path.unlink(missing_ok=True)

    ok = [r for r in results if "error" not in r]
    if not ok:
        return {"error": "No successful tickers", "details": results}

    n = len(ok)
    avg_conv = sum(float(r["conviction"] or 0) for r in ok) / n
    cagrs = [
        float(r["strategy_cagr"] or 0) for r in ok if r.get("strategy_cagr") is not None
    ]
    avg_cagr = sum(cagrs) / len(cagrs) if cagrs else 0.0

    # Simple $10k 3y mark-to-market proxy: compound by avg CAGR
    # (not reinvestment-perfect).
    growth_3y = (1 + avg_cagr) ** 3 - 1 if avg_cagr else 0.0
    end_val = 10000 * (1 + growth_3y)

    return {
        "tickers": tickers,
        "avg_conviction": round(avg_conv, 1),
        "avg_strategy_cagr": round(avg_cagr, 4),
        "equal_weight_notional_end_10k": round(end_val, 2),
        "per_ticker": results,
    }


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    tickers = argv if argv else ["NVDA", "TSLA", "SOFI"]
    root = Path(__file__).resolve().parent.parent
    out = simulate_top_n(tickers, root=root)
    print(json.dumps(out, indent=2, default=str))
    return 0 if "error" not in out else 1
