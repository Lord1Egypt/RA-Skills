"""Human-readable report lines from score + data + backtest."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

from tai_alpha.localize import disclaimer_short, signal_label
from tai_alpha.storage_sqlite import connect, default_db_path, init_db


def _safe_float(x: Any, default: float = 0.0) -> float:
    if x is None:
        return default
    try:
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return default
        return v
    except (TypeError, ValueError):
        return default


def format_report(
    score: dict[str, Any],
    raw: dict[str, Any],
    bt: dict[str, Any],
    *,
    lang: str = "en",
    audience: str = "retail",
) -> str:
    """Build multi-line report string (``lang``: en | zh-CN | zh-HK)."""
    lines: list[str] = []
    ticker = score.get("ticker", raw.get("ticker", "?"))
    sig = score.get("signal", "?")
    conv = int(score.get("conviction", 0))
    sig_d = signal_label(str(sig), lang) if lang.startswith("zh") else sig
    lines.append(f"• {ticker}: {sig_d} {conv}/100")
    if score.get("persona_id") or score.get("persona_ensemble"):
        pid = score.get("persona_id", "")
        pzh = score.get("persona_display_name_zh") or score.get(
            "persona_display_name", ""
        )
        if lang.startswith("zh") and pzh:
            lines.append(f"• 人格视角：{pzh} ({pid})")
        else:
            lines.append(f"• Persona: {score.get('persona_display_name', pid)} ({pid})")

    price = _safe_float(raw.get("price"))
    pe = _safe_float(raw.get("pe"), 999)
    roe = _safe_float(raw.get("roe"))
    lines.append(f"• Price: ${price:.2f} | PE: {pe:.1f} | ROE: {roe:.1%}")

    rsi = _safe_float(raw.get("rsi"), 50)
    sharpe = _safe_float(raw.get("sharpe"))
    beta = _safe_float(raw.get("beta"), 1)
    lines.append(f"• RSI: {rsi:.0f} | Sharpe: {sharpe:.2f} | Beta: {beta:.2f}")

    at = _safe_float(raw.get("analyst_target"))
    rm = _safe_float(raw.get("rating_mean"), 3)
    up_pct = ((at / price - 1) * 100) if price else 0
    lines.append(f"• IB Target: ${at:.0f} ↑{up_pct:.0f}% | Rating: {rm:.1f}")

    macd = raw.get("macd", "?")
    eps_g = _safe_float(raw.get("eps_growth"))
    vol = _safe_float(raw.get("vol"))
    lines.append(f"• MACD: {macd} | EPS Gr: {eps_g:.1%} | Vol: {vol:,.0f}")

    vix = _safe_float(raw.get("vix"), 20)
    sm = _safe_float(raw.get("spy_mom"))
    lines.append(f"• Macro: VIX {vix:.0f} | SPY Mom {sm:.1f}%")

    sc = _safe_float(bt.get("strategy_cagr"))
    alpha = _safe_float(bt.get("alpha_vs_spy"))
    ss = _safe_float(bt.get("strategy_sharpe"))
    dd = _safe_float(bt.get("strategy_max_dd"))
    wr = _safe_float(bt.get("win_rate"))
    tr = _safe_float(bt.get("trades"))
    lines.append(
        f"• Backtest: CAGR {sc:.1f}% Alpha+{alpha:.1f}% | Sharpe {ss:.2f} | "
        f"DD {dd:.1f}% | Win {wr:.0f}% ({tr:.0f} trades)"
    )

    bh = _safe_float(bt.get("bh_cagr"))
    spy = _safe_float(bt.get("spy_cagr"))
    news = raw.get("news") or []
    pos_n = len([n for n in news if "beat" in n.lower() or "upgrade" in n.lower()])
    lines.append(f"• vs Ticker BH {bh:.1f}% SPY {spy:.1f}% | News Pos {pos_n}/5")

    for risk in score.get("risks") or []:
        lines.append(f"⚠️ {risk}")
    rflags = score.get("risk_flags") or []
    if rflags:
        preview = ", ".join(str(x) for x in rflags[:6])
        extra = f" (+{len(rflags) - 6} more)" if len(rflags) > 6 else ""
        lines.append(f"• Risk flags: {preview}{extra}")
    for title in (news or [])[:4]:
        t = (title or "")[:90]
        lines.append(f"📰 {t}...")
    lines.append(disclaimer_short(lang))
    _ = audience  # reserved for density tuning
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(description="Print formatted report for a run")
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
        help="Run id with score_json (and collect_json)",
    )
    args = p.parse_args(argv)

    db_path = args.db_path or default_db_path()
    init_db(db_path)
    conn = connect(db_path)
    try:
        row = conn.execute(
            "SELECT collect_json, backtest_json, score_json FROM runs WHERE id = ?",
            (args.run_id,),
        ).fetchone()
        if not row:
            print("Run not found", file=sys.stderr)
            return 2
        collect_s, bt_s, score_s = row[0], row[1], row[2]
        if not score_s:
            print("No score_json for run", file=sys.stderr)
            return 2
        score = json.loads(score_s)
        raw = json.loads(collect_s) if collect_s else {}
        bt = score.get("backtest") or {}
        if not bt and bt_s:
            bt = json.loads(bt_s)
        if not raw and score.get("ticker"):
            raw = {"ticker": score["ticker"]}
        print(format_report(score, raw, bt))
        return 0
    finally:
        conn.close()
