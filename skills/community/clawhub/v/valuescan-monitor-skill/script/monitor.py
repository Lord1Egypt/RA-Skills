#!/usr/bin/env python3
# Dependencies: pip install sseclient-py requests pysocks
"""
ValueScan Stream Monitor (Python)

Usage:
  python monitor.py --market [--config=~/.vs-monitor/config.json]
  python monitor.py --signal [--tokens=BTC,ETH] [--config=~/.vs-monitor/config.json]

Config (~/.vs-monitor/config.json):
  {
    "apiKey": "...",
    "secretKey": "...",
    "outputDir": "/path/to/output",
    "streamBaseUrl": "https://stream.valuescan.ai"  # optional
  }
"""

import argparse
import hashlib
import hmac
import json
import os
import signal as signal_module
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

import requests
import sseclient

PID_DIR = Path.home() / ".vs-monitor"


# ── Auth ──────────────────────────────────────────────────────────────────────

def _hmac_hex(secret_key: str, message: str) -> str:
    return hmac.new(
        secret_key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def build_stream_params(api_key: str, secret_key: str) -> dict:
    """Query params for SSE connections (GET requests, body fixed as '{}')."""
    timestamp = str(int(time.time() * 1000))
    nonce = str(uuid.uuid4())
    sign = _hmac_hex(secret_key, timestamp + nonce)
    return {"apiKey": api_key, "timestamp": timestamp, "nonce": nonce, "sign": sign}


def build_api_headers(api_key: str, secret_key: str, body: str) -> dict:
    """Request headers for main API calls (POST)."""
    timestamp = str(int(time.time() * 1000))
    sign = _hmac_hex(secret_key, timestamp + body)
    return {
        "X-API-KEY": api_key,
        "X-TIMESTAMP": timestamp,
        "X-SIGN": sign,
        "Content-Type": "application/json; charset=utf-8",
    }


# ── Token resolution ──────────────────────────────────────────────────────────

def resolve_token_ids(symbols: list, api_key: str, secret_key: str, api_base_url: str) -> list:
    """Convert token symbols (e.g. 'BTC') to vsTokenId strings."""
    token_ids = []
    for symbol in symbols:
        body = json.dumps({"search": symbol})
        headers = build_api_headers(api_key, secret_key, body)
        try:
            resp = requests.post(
                f"{api_base_url}/api/open/v1/vs-token/list",
                headers=headers,
                data=body,
                timeout=10,
            )
            records = resp.json().get("data", [])
        except Exception as e:
            print(f"[warn] Failed to resolve symbol {symbol}: {e}", file=sys.stderr)
            continue
        if not records:
            print(f"[warn] Symbol not found: {symbol}", file=sys.stderr)
            continue
        match = next((r for r in records if r.get("symbol", "").upper() == symbol.upper()), None)
        if match is None:
            match = records[0]
        if match:
            token_ids.append(str(match["id"]))
        else:
            print(f"[warn] Symbol not found: {symbol}", file=sys.stderr)
    return token_ids


# ── File writing ──────────────────────────────────────────────────────────────

def write_market(content: str, output_dir: str) -> None:
    now = datetime.now()
    dir_path = Path(output_dir) / "大盘分析"
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / f"大盘分析-{now.strftime('%Y-%m-%d')}.txt"
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"[{now.strftime('%H:%M:%S')}]\n{content}\n---\n")


def write_signal(payload: str, output_dir: str) -> None:
    msg = json.loads(payload)
    signal_type = msg.get("type", "UNKNOWN")
    try:
        inner = json.loads(msg.get("content", "{}"))
    except Exception:
        inner = {}
    symbol = inner.get("symbol", "UNKNOWN")
    content = msg.get("content", "")
    now = datetime.now()
    dir_path = Path(output_dir) / "代币信号" / now.strftime("%Y-%m-%d")
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / f"{symbol}.txt"
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"[{now.strftime('%H:%M:%S')}] [{signal_type}]\n{content}\n---\n")


# ── PID management ────────────────────────────────────────────────────────────

def write_pid(mode: str) -> None:
    PID_DIR.mkdir(parents=True, exist_ok=True)
    (PID_DIR / f"{mode}.pid").write_text(str(os.getpid()))


def cleanup_pid(mode: str) -> None:
    pid_file = PID_DIR / f"{mode}.pid"
    if pid_file.exists():
        pid_file.unlink(missing_ok=True)


# ── Monitor loops ─────────────────────────────────────────────────────────────

def run_market(config: dict) -> None:
    stream_base = config.get("streamBaseUrl", "https://stream.valuescan.ai")
    output_dir = config["outputDir"]
    params = build_stream_params(config["apiKey"], config["secretKey"])

    resp = requests.get(
        f"{stream_base}/stream/market/subscribe",
        params=params,
        stream=True,
        timeout=None,
    )
    resp.raise_for_status()
    for event in sseclient.SSEClient(resp).events():
        if event.event in ("heartbeat", "connected"):
            continue
        if event.event == "market":
            write_market(event.data, output_dir)


def run_signal(config: dict, token_ids: list = None) -> None:
    stream_base = config.get("streamBaseUrl", "https://stream.valuescan.ai")
    output_dir = config["outputDir"]
    params = build_stream_params(config["apiKey"], config["secretKey"])
    if token_ids:
        params["tokens"] = ",".join(token_ids)

    resp = requests.get(
        f"{stream_base}/stream/signal/subscribe",
        params=params,
        stream=True,
        timeout=None,
    )
    resp.raise_for_status()
    for event in sseclient.SSEClient(resp).events():
        if event.event in ("heartbeat", "connected"):
            continue
        if event.event == "signal":
            write_signal(event.data, output_dir)


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="ValueScan Stream Monitor")
    parser.add_argument("--market", action="store_true", help="Subscribe to market analysis stream")
    parser.add_argument("--signal", action="store_true", help="Subscribe to token signal stream")
    parser.add_argument("--tokens", type=str, default="", help="Comma-separated token symbols, e.g. BTC,ETH")
    parser.add_argument("--config", type=str, default=str(PID_DIR / "config.json"))
    args = parser.parse_args()

    if not args.market and not args.signal:
        print("Error: specify --market or --signal", file=sys.stderr)
        sys.exit(1)
    if args.market and args.signal:
        print("Error: use --market or --signal in separate processes", file=sys.stderr)
        sys.exit(1)

    with open(Path(args.config).expanduser(), "r", encoding="utf-8") as f:
        config = json.load(f)

    mode = "market" if args.market else "signal"
    write_pid(mode)

    def _shutdown(signum=None, frame=None):
        cleanup_pid(mode)
        sys.exit(0)

    signal_module.signal(signal_module.SIGTERM, _shutdown)
    signal_module.signal(signal_module.SIGINT, _shutdown)

    try:
        if args.market:
            run_market(config)
        else:
            token_ids = None
            if args.tokens:
                symbols = [s.strip() for s in args.tokens.split(",") if s.strip()]
                api_base = config.get("apiBaseUrl", "https://api.valuescan.io")
                token_ids = resolve_token_ids(symbols, config["apiKey"], config["secretKey"], api_base)
                if not token_ids:
                    print("Error: none of the specified tokens could be resolved", file=sys.stderr)
                    sys.exit(1)
            run_signal(config, token_ids)
    finally:
        cleanup_pid(mode)


if __name__ == "__main__":
    main()
