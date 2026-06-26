"""Argparse + wiring for CLIs; keeps ``scripts/*.py`` as thin wrappers."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from tai_alpha.backtest_engine import multi_strategy_compare_from_collect, run_backtest
from tai_alpha.collect import collect_ticker
from tai_alpha.ml_predict import predict_7d_return_from_collect
from tai_alpha.pipeline import run_analyze
from tai_alpha.runtime_paths import (
    ensure_output_dir,
    find_project_root,
)
from tai_alpha.storage_sqlite import (
    connect,
    default_db_path,
    get_collect_dict,
    get_latest_score_for_ticker,
    init_db,
    update_run_ml,
)


def analyze_cli(argv: list[str] | None = None) -> int:
    """Full pipeline: collect, backtest, score, optional report."""
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(description="Tai Alpha full analyze")
    p.add_argument("ticker", nargs="?", default="AAPL")
    p.add_argument(
        "--strategy",
        choices=("rsi", "macd", "bb"),
        default="rsi",
        help="Backtest strategy",
    )
    p.add_argument("--rsi-low", type=float, default=35.0)
    p.add_argument("--rsi-high", type=float, default=75.0)
    p.add_argument(
        "--no-report",
        action="store_true",
        help="Skip human-readable report to stdout",
    )
    p.add_argument(
        "--fast",
        action="store_true",
        help="Skip ML step and use lighter collect (skip sector ETF peer fetch)",
    )
    p.add_argument(
        "--depth",
        choices=("lite", "standard", "deep"),
        default="standard",
        help=(
            "lite=fast collect + no ML; standard=default; "
            "deep=ML + expanded risk_flags"
        ),
    )
    p.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="SQLite database path (default: TAI_ALPHA_DB_PATH or output dir)",
    )
    p.add_argument(
        "--market",
        choices=("auto", "us", "hk", "cn"),
        default="auto",
        help="Market for symbol normalization (Yahoo/yfinance)",
    )
    p.add_argument(
        "--persona",
        default=None,
        help="Comma-separated persona ids (see setup/config/personas/)",
    )
    p.add_argument(
        "--persona-all",
        action="store_true",
        help="Run ensemble across all registered personas",
    )
    p.add_argument(
        "--lang",
        choices=("en", "zh-CN", "zh-HK"),
        default="en",
        help="Report language",
    )
    p.add_argument(
        "--audience",
        choices=("retail", "pro"),
        default="retail",
        help="Audience density for reports (reserved)",
    )
    p.add_argument(
        "--source-policy",
        choices=("auto", "strict-primary", "allow-fallback"),
        default="auto",
        help="Source policy (logged; Yahoo primary today)",
    )
    args = p.parse_args(argv)

    db_path = (args.db_path or default_db_path()).resolve()
    ensure_output_dir(db_path.parent)

    print(f"\n🔍 Tai Alpha: {args.ticker}")
    print("• Loading data (fund/quant/macro/peers/news)…")
    run_analyze(
        args.ticker,
        db_path,
        strategy=args.strategy,
        rsi_low=args.rsi_low,
        rsi_high=args.rsi_high,
        print_report=not args.no_report,
        fast=args.fast,
        depth=args.depth,  # type: ignore[arg-type]
        market=args.market,  # type: ignore[arg-type]
        persona=args.persona,
        persona_all=args.persona_all,
        lang=args.lang,
        audience=args.audience,
        source_policy=args.source_policy,
    )
    print("• Done.")
    return 0


def custom_cli(argv: list[str] | None = None) -> int:
    """Collect then backtest with chosen strategy."""
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(
        description="Custom strategy backtest (after collect)",
        epilog="Example: custom.py NVDA --strategy macd",
    )
    p.add_argument("ticker", nargs="?", default="NVDA", help="Symbol")
    p.add_argument(
        "--strategy",
        default="rsi",
        choices=("rsi", "macd", "bb"),
        help="Backtest strategy",
    )
    p.add_argument("--rsi-low", type=float, default=30.0)
    p.add_argument("--rsi-high", type=float, default=70.0)
    p.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="SQLite database path",
    )
    args = p.parse_args(argv)

    db_path = (args.db_path or default_db_path()).resolve()
    ensure_output_dir(db_path.parent)
    init_db(db_path)
    print(
        f"{args.ticker} {args.strategy} backtest "
        f"(RSI entry/exit {args.rsi_low}/{args.rsi_high} when strategy=rsi)"
    )
    _, run_id = collect_ticker(args.ticker, db_path, fast=False)
    bt = run_backtest(
        db_path,
        run_id,
        strategy=args.strategy,  # type: ignore[arg-type]
        rsi_low=args.rsi_low,
        rsi_high=args.rsi_high,
    )
    print(json.dumps(bt, indent=2, default=str))
    return 0 if not bt.get("error") else 1


def ml_cli(argv: list[str] | None = None) -> int:
    """ML 7d forward return estimate."""
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(description="ML 7d forward return estimate")
    p.add_argument("ticker", nargs="?", default="AAPL")
    p.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="SQLite database path",
    )
    args = p.parse_args(argv)

    db_path = (args.db_path or default_db_path()).resolve()
    ensure_output_dir(db_path.parent)
    init_db(db_path)
    data, run_id = collect_ticker(args.ticker, db_path, fast=False)
    pred = predict_7d_return_from_collect(data)
    if pred is None:
        print(f"{args.ticker}: insufficient data or ML unavailable", file=sys.stderr)
        return 1
    conn = connect(db_path)
    try:
        update_run_ml(conn, run_id, {"pred": pred, "ticker": args.ticker.upper()})
        conn.commit()
    finally:
        conn.close()
    sign = "+" if pred >= 0 else ""
    print(f"{args.ticker} 7d pred {sign}{pred * 100:.1f}% (RF returns)")
    return 0


def multi_backtest_cli(argv: list[str] | None = None) -> int:
    """Compare RSI / MACD / BB CAGR."""
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser()
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
        help="Run id whose collect_json to use",
    )
    args = p.parse_args(argv)

    db_path = (args.db_path or default_db_path()).resolve()
    init_db(db_path)
    conn = connect(db_path)
    try:
        raw = get_collect_dict(conn, args.run_id)
    finally:
        conn.close()
    if raw is None:
        print("No collect data for run", file=sys.stderr)
        return 2
    out = multi_strategy_compare_from_collect(raw)
    print(json.dumps(out, indent=2, default=str))
    return 0 if not out.get("error") else 1


def batch_cli(argv: list[str] | None = None) -> int:
    """Run analyze for multiple tickers; print one score line each."""
    argv = argv if argv is not None else sys.argv[1:]
    root = find_project_root()
    p = argparse.ArgumentParser(description="Batch analyze tickers")
    p.add_argument(
        "tickers",
        nargs="*",
        help="Symbols (default NVDA AAPL if omitted)",
    )
    p.add_argument("--fast", action="store_true", help="Forward --fast to analyze")
    p.add_argument(
        "--depth",
        choices=("lite", "standard", "deep"),
        default="standard",
        help="Forward --depth to analyze",
    )
    p.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="SQLite database path",
    )
    args_b = p.parse_args(argv)
    tickers = args_b.tickers if args_b.tickers else ["NVDA", "AAPL"]
    py = sys.executable
    analyze = root / "scripts" / "analyze.py"
    db_path = (args_b.db_path or default_db_path()).resolve()
    ensure_output_dir(db_path.parent)
    init_db(db_path)
    print("Ticker | Signal | Conviction (see full output above)")
    for ticker in tickers:
        cmd = [
            py,
            str(analyze),
            ticker,
            "--no-report",
            "--db-path",
            str(db_path),
            "--depth",
            args_b.depth,
        ]
        if args_b.fast:
            cmd.append("--fast")
        result = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=120,
        )
        line = f"{ticker} | (run failed rc={result.returncode})"
        conn = connect(db_path)
        try:
            sc = get_latest_score_for_ticker(conn, ticker)
            if sc is not None:
                line = f"{ticker} | {sc.get('signal')} " f"{sc.get('conviction')}/100"
        finally:
            conn.close()
        print(line)
    return 0


def cron_cli(argv: list[str] | None = None) -> int:
    """Daily-style hotlist batch (optional Telegram hook via env)."""
    import os

    argv = argv if argv is not None else sys.argv[1:]
    _ = argv  # reserved for future flags
    root = find_project_root()
    sp500_hot = os.environ.get("TAI_ALPHA_HOTLIST", "NVDA,AAPL,MSFT").split(",")
    sp500_hot = [s.strip().upper() for s in sp500_hot if s.strip()]
    print("S&P-style hotlist batch:", ", ".join(sp500_hot))
    py = sys.executable
    analyze = root / "scripts" / "analyze.py"
    for t in sp500_hot:
        subprocess.run([py, str(analyze), t], cwd=str(root), timeout=180)
    hook = os.environ.get("TAI_ALPHA_TELEGRAM_WEBHOOK")
    if hook:
        print("(Telegram webhook URL set — integrate with your notifier.)")
    return 0
