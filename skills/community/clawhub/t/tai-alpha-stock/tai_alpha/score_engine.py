"""Conviction score from normalized collect payload."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from tai_alpha.config_load import load_score_dimensions
from tai_alpha.risk_flags import compute_risk_flags
from tai_alpha.schema import normalize_collect_data
from tai_alpha.storage_sqlite import connect, default_db_path, get_collect_dict, init_db


def get_signal_thresholds(cfg: dict[str, Any] | None = None) -> dict[str, int]:
    """Thresholds for signal bands (used by pipeline alpha boost)."""
    c = cfg if cfg is not None else load_score_dimensions()
    th = c.get("thresholds", {})
    return {
        "strong_buy": int(th.get("signal_strong_buy", 85)),
        "buy": int(th.get("signal_buy", 75)),
        "avoid": int(th.get("signal_avoid_high", 65)),
        "sell": int(th.get("signal_sell", 55)),
    }


def _signal_from_score(score: int, cfg: dict[str, Any]) -> str:
    th = cfg.get("thresholds", {})
    sb = int(th.get("signal_strong_buy", 85))
    b = int(th.get("signal_buy", 75))
    av = int(th.get("signal_avoid_high", 65))
    s = int(th.get("signal_sell", 55))
    if score > sb:
        return "STRONG BUY"
    if score > b:
        return "BUY"
    if score < s:
        return "SELL"
    if score < av:
        return "AVOID"
    return "HOLD"


def score_data(
    data: dict[str, Any],
    ml_pred: float | None = None,
    *,
    deep_risk: bool = False,
    dimensions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Compute conviction 0–100 and signal from collect fields.
    ``ml_pred`` is optional forward return estimate (e.g. 0.05 = +5%).
    """
    cfg = dimensions if dimensions is not None else load_score_dimensions()
    p = cfg.get("points", {})
    th = cfg.get("thresholds", {})
    base = float(cfg.get("base_score", 50))

    if data.get("error"):
        return {
            "ticker": data.get("ticker", "UNKNOWN"),
            "conviction": 0,
            "signal": "ERROR",
            "risks": [str(data["error"])],
            "risk_flags": [],
            "ml_pred": None,
            "backtest": {},
        }

    normalize_collect_data(data)

    score = base
    risks: list[str] = []

    fund = p.get("fundamentals", {})
    tec = p.get("technicals", {})
    ana = p.get("analyst", {})
    macro = p.get("macro", {})
    peers = p.get("peers", {})
    ml_cfg = p.get("ml", {})
    sent = p.get("sentiment", {})
    fg_cfg = p.get("fear_greed", {})
    sh_cfg = p.get("shorts", {})
    iv_dup = p.get("iv_dup", {})
    vix_pen = p.get("vix", {})

    pe_rule = fund.get("pe_low_if_below", {})
    if data["pe"] < float(pe_rule.get("threshold", 20)):
        score += float(pe_rule.get("points", 12))

    roe_rule = fund.get("roe_if_above", {})
    if data["roe"] > float(roe_rule.get("threshold", 0.2)):
        score += float(roe_rule.get("points", 15))

    debt_rule = fund.get("debt_if_below", {})
    if data["debt"] < float(debt_rule.get("threshold", 40)):
        score += float(debt_rule.get("points", 10))

    div_rule = fund.get("div_yield_if_above", {})
    if data["div_yield"] > float(div_rule.get("threshold", 0.04)):
        score += float(div_rule.get("points", 5))

    sharpe_rule = tec.get("sharpe_if_above", {})
    if data["sharpe"] > float(sharpe_rule.get("threshold", 1.5)):
        score += float(sharpe_rule.get("points", 18))

    if data["macd"] == "bull":
        score += float(tec.get("macd_bull", 10))

    rsi_ob = float(th.get("rsi_overbought", 75))
    rsi_os = float(th.get("rsi_oversold", 35))
    if data["rsi"] < rsi_os:
        score += float(tec.get("rsi_oversold_bonus", 8))
    if data["rsi"] > rsi_ob:
        score += float(tec.get("rsi_overbought_penalty", -12))
        risks.append("Overbought")

    beta_rule = tec.get("beta_if_below", {})
    if data["beta"] < float(beta_rule.get("threshold", 1.2)):
        score += float(beta_rule.get("points", 5))

    vol_rule = tec.get("vol_if_above", {})
    if data["vol"] > float(vol_rule.get("threshold", 2_000_000)):
        score += float(vol_rule.get("points", 6))

    rating_rule = ana.get("rating_if_below", {})
    if data["rating_mean"] < float(rating_rule.get("threshold", 2.2)):
        score += float(rating_rule.get("points", 20))

    tgt_rule = ana.get("target_vs_price_pct", {})
    mult = float(tgt_rule.get("multiplier", 1.15))
    if data["analyst_target"] > data["price"] * mult:
        score += float(tgt_rule.get("points", 12))

    eps_rule = ana.get("eps_growth_if_above", {})
    if data["eps_growth"] > float(eps_rule.get("threshold", 0.2)):
        score += float(eps_rule.get("points", 8))

    vix_low = float(th.get("vix_low", 20))
    if data["vix"] < vix_low:
        score += float(macro.get("vix_low_bonus", 8))

    spy_th = float(th.get("spy_mom_high", 5))
    if data["spy_mom"] > spy_th:
        score += float(macro.get("spy_mom_bonus", 6))

    if data["yield_curve"] > 0:
        score += float(macro.get("yield_curve_if_positive", 3))

    iv_th = float(th.get("iv_low", 0.4))
    if data["iv"] < iv_th:
        score += float(macro.get("iv_low_bonus", 4))

    if data["peer_score"] > 0:
        score += float(peers.get("peer_score_if_positive", 5))

    pred = ml_pred if ml_pred is not None else 0.0
    score += pred * float(ml_cfg.get("pred_multiplier", 10))

    fg_th = int(th.get("fear_greed_elevated", 80))
    if int(data["fear_greed"]) > fg_th:
        score += float(fg_cfg.get("if_above_penalty", -10))

    shorts_th = float(th.get("shorts_elevated", 0.15))
    shorts = float(data.get("shortRatio", 0.1))
    if shorts > shorts_th:
        score += float(sh_cfg.get("if_elevated_penalty", -8))

    iv_imp = float(data.get("impliedVolatility", 0.3))
    if iv_imp < iv_th:
        score += float(iv_dup.get("if_low_bonus", 4))

    vix_hi = float(th.get("vix_high", 25))
    if data["vix"] > vix_hi:
        score += float(vix_pen.get("if_high_penalty", -5))

    pos_kw = sent.get("positive_keywords", ["beat", "upgrade", "buy", "growth"])
    neg_kw = sent.get("negative_keywords", ["miss", "downgrade", "sell"])
    per = float(sent.get("news_keyword_per_delta", 4))
    pos = sum(
        1 for n in data["news"] if any(str(p).lower() in n.lower() for p in pos_kw)
    )
    neg = sum(
        1 for n in data["news"] if any(str(nw).lower() in n.lower() for nw in neg_kw)
    )
    score += (pos - neg) * per

    score_i = min(100, max(0, int(round(score))))
    signal = _signal_from_score(score_i, cfg)

    risk_flags = compute_risk_flags(data, deep=deep_risk)

    return {
        "ticker": data["ticker"],
        "conviction": score_i,
        "signal": signal,
        "risks": risks,
        "risk_flags": risk_flags,
        "ml_pred": pred,
    }


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(description="Score collect payload for a run")
    p.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="SQLite database path",
    )
    p.add_argument(
        "--run-id",
        type=int,
        required=True,
        help="Run id with collect_json",
    )
    p.add_argument(
        "--deep-risk",
        action="store_true",
        help="Include geopolitical keyword scans in risk_flags",
    )
    args = p.parse_args(argv)

    db_path = args.db_path or default_db_path()
    init_db(db_path)
    conn = connect(db_path)
    try:
        data = get_collect_dict(conn, args.run_id)
        if data is None:
            print("No collect_json for run", file=sys.stderr)
            return 2
        row = conn.execute(
            "SELECT ml_json FROM runs WHERE id = ?", (args.run_id,)
        ).fetchone()
        ml_pred: float | None = None
        if row and row[0]:
            try:
                blob = json.loads(row[0])
                if "pred" in blob:
                    ml_pred = float(blob["pred"])
            except (TypeError, ValueError, KeyError):
                pass
        out = score_data(data, ml_pred=ml_pred, deep_risk=args.deep_risk)
        print(json.dumps(out, default=str))
        return 0 if out["signal"] != "ERROR" else 1
    finally:
        conn.close()
