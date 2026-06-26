"""End-to-end analyze: collect → backtest → score → optional report."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Literal

from tai_alpha.backtest_engine import run_backtest
from tai_alpha.collect import collect_ticker_routed
from tai_alpha.config_load import load_score_dimensions
from tai_alpha.ml_predict import predict_7d_return_from_collect
from tai_alpha.persona_engine import apply_persona_ensemble, resolve_persona_ids
from tai_alpha.report_text import format_report
from tai_alpha.score_engine import get_signal_thresholds, score_data
from tai_alpha.storage_sqlite import (
    connect,
    default_db_path,
    init_db,
    update_run_ml,
    update_run_persona_meta,
    update_run_score,
)

Depth = Literal["lite", "standard", "deep"]
MarketOpt = Literal["auto", "us", "hk", "cn"]


def _safe_alpha(bt: dict[str, Any]) -> float:
    a = bt.get("alpha_vs_spy")
    if a is None:
        return 0.0
    try:
        v = float(a)
        if math.isnan(v):
            return 0.0
        return v
    except (TypeError, ValueError):
        return 0.0


def _resolve_run_flags(
    *,
    fast: bool,
    depth: Depth,
) -> tuple[bool, bool, bool]:
    """
    Returns (collect_fast, skip_ml, deep_risk).

    ``lite`` skips ML and uses a lighter collect (no sector ETF peer fetch).
    ``fast`` skips ML; when combined with ``standard``, collect may still skip
    peers. ``deep`` uses full collect and adds geopolitical ``risk_flags``.
    """
    if depth == "lite":
        return (True, True, False)
    skip_ml = fast
    deep_risk = depth == "deep"
    collect_fast = fast and depth != "deep"
    return (collect_fast, skip_ml, deep_risk)


def run_analyze(
    ticker: str,
    db_path: Path | None = None,
    *,
    strategy: str = "rsi",
    rsi_low: float = 35.0,
    rsi_high: float = 75.0,
    print_report: bool = True,
    fast: bool = False,
    depth: Depth = "standard",
    market: MarketOpt = "auto",
    persona: str | None = None,
    persona_all: bool = False,
    lang: str = "en",
    audience: str = "retail",
    source_policy: str = "auto",
) -> dict[str, Any]:
    """
    Run full pipeline; persists collect, backtest, score, optional ML, persona/meta.

    ``market``: routing for yfinance symbol normalization (US/HK/CN).
    ``persona``: comma-separated persona ids; ``persona_all`` runs ensemble of all.
    ``lang`` / ``audience``: report localization (zh-CN/zh-HK supported).
    ``source_policy``: reserved for future strict-primary fallback (logged in meta).
    """
    db_path = (db_path or default_db_path()).resolve()
    init_db(db_path)

    collect_fast, skip_ml, deep_risk = _resolve_run_flags(fast=fast, depth=depth)
    cfg = load_score_dimensions()
    sig_th = get_signal_thresholds(cfg)
    alpha_cfg = cfg.get("alpha_boost", {})
    alpha_min = float(alpha_cfg.get("if_alpha_vs_spy_above", 10))
    conv_add = int(alpha_cfg.get("conviction_add", 12))
    strong_line = sig_th["strong_buy"]

    persona_ids = resolve_persona_ids(persona, persona_all)

    data, run_id = collect_ticker_routed(
        ticker,
        db_path,
        fast=collect_fast,
        market=market,
    )
    meta_run: dict[str, Any] = {
        "lang": lang,
        "audience": audience,
        "source_policy": source_policy,
        "market": (data.get("adapter_meta") or {}).get("market"),
        "persona_requested": persona_ids,
    }

    if data.get("error"):
        err_score = score_data(data, deep_risk=deep_risk, dimensions=cfg)
        if persona_ids:
            err_score = apply_persona_ensemble(err_score, data, persona_ids)
        conn = connect(db_path)
        try:
            update_run_score(conn, run_id, err_score)
            update_run_persona_meta(
                conn,
                run_id,
                persona=(
                    {"persona_ids": persona_ids, "score": err_score}
                    if persona_ids
                    else None
                ),
                meta=meta_run,
            )
            conn.commit()
        finally:
            conn.close()
        return err_score

    bt = run_backtest(
        db_path,
        run_id,
        strategy=strategy,  # type: ignore[arg-type]
        rsi_low=rsi_low,
        rsi_high=rsi_high,
    )

    ml_pred: float | None = None
    if not skip_ml:
        ml_pred = predict_7d_return_from_collect(data)

    conn = connect(db_path)
    try:
        if ml_pred is not None:
            update_run_ml(conn, run_id, {"pred": ml_pred})
            score = score_data(
                data,
                ml_pred=ml_pred,
                deep_risk=deep_risk,
                dimensions=cfg,
            )
        else:
            score = score_data(
                data,
                ml_pred=None,
                deep_risk=deep_risk,
                dimensions=cfg,
            )

        alpha = _safe_alpha(bt)
        if alpha > alpha_min:
            score["conviction"] = min(100, int(score["conviction"]) + conv_add)
            if score["conviction"] > strong_line:
                score["signal"] = "STRONG BUY"

        if persona_ids:
            score = apply_persona_ensemble(score, data, persona_ids)

        score["backtest"] = bt
        update_run_score(conn, run_id, score)
        update_run_persona_meta(
            conn,
            run_id,
            persona=(
                {"persona_ids": persona_ids, "score": score} if persona_ids else None
            ),
            meta=meta_run,
        )
        conn.commit()
    finally:
        conn.close()

    if print_report:
        text = format_report(score, data, bt, lang=lang, audience=audience)
        print(text)

    return score
