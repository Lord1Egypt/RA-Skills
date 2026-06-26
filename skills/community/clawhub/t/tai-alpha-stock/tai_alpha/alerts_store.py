"""Persistent watchlist with target / stop prices and optional live check."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

import yfinance as yf

from tai_alpha.storage_sqlite import (
    connect,
    default_db_path,
    init_db,
    load_watchlist,
    upsert_watchlist_row,
)
from tai_alpha.yfinance_utils import close_series


def check_alerts_conn(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Compare last price to targets/stops using watchlist in SQLite."""
    w = load_watchlist(conn)
    triggered: list[dict[str, Any]] = []
    for sym, cfg in w.items():
        try:
            px = float(yf.Ticker(sym).info.get("regularMarketPrice") or 0)
            if not px:
                h = yf.Ticker(sym).history(period="5d")
                if not h.empty:
                    px = float(close_series(h, sym).iloc[-1])
        except Exception as e:
            triggered.append({"ticker": sym, "error": str(e)})
            continue
        t = float(cfg.get("target", 0))
        s = cfg.get("stop")
        msg = None
        if t and px >= t:
            msg = f"At or above target ${t:.2f} (last ${px:.2f})"
        if s is not None and px <= float(s):
            msg = (msg + "; ") if msg else ""
            msg = f"{msg}At or below stop ${float(s):.2f} (last ${px:.2f})"
        if msg:
            triggered.append({"ticker": sym, "last": px, "message": msg})
    return triggered


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(description="Tai Alpha watchlist alerts")
    p.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="SQLite database path (watchlist table)",
    )
    sub = p.add_subparsers(dest="cmd", required=False)

    a = sub.add_parser("add", help="Add ticker with target and optional stop")
    a.add_argument("ticker")
    a.add_argument("target", type=float)
    a.add_argument("--stop", type=float, default=None)

    sub.add_parser("list", help="Print watchlist")

    sub.add_parser("check", help="Compare last price to targets/stops")

    ns = argv if argv else ["list"]
    args = p.parse_args(ns)

    db_path = args.db_path or default_db_path()
    init_db(db_path)
    conn = connect(db_path)
    try:
        if not getattr(args, "cmd", None) or args.cmd == "list":
            print(json.dumps(load_watchlist(conn), indent=2))
            return 0

        if args.cmd == "add":
            upsert_watchlist_row(conn, args.ticker, args.target, args.stop)
            conn.commit()
            print(json.dumps(load_watchlist(conn), indent=2))
            return 0

        if args.cmd == "check":
            out = check_alerts_conn(conn)
            print(json.dumps(out, indent=2, default=str))
            return 0

        return 2
    finally:
        conn.close()
