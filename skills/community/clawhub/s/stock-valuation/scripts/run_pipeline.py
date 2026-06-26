#!/usr/bin/env python3
"""
Orchestrate all stock valuation data collection into a single JSON.
Usage: uv run --with yfinance,matplotlib,lxml python3 scripts/run_pipeline.py TICKER [--peers P1 P2 P3] [--output /tmp/TICKER_data.json]
"""
import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def run_script(name, args, timeout=120):
    """Run a script and return parsed JSON or error dict."""
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, name)] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            return {"error": result.stderr.strip() or f"{name} exited with code {result.returncode}"}
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return {"error": f"{name} timed out after {timeout}s"}
    except json.JSONDecodeError:
        return {"error": f"{name} produced invalid JSON"}
    except Exception as e:
        return {"error": str(e)}


def detect_peers(ticker, count=3):
    """Auto-detect peers, pick top 3 by market cap similarity."""
    data = run_script("detect_peers.py", [ticker, "--count", str(count + 2)])
    if "error" in data:
        return []
    peers = data.get("peers", [])
    # Sort by market cap proximity to target if available
    target_mcap = data.get("market_cap", 0)
    if target_mcap and len(peers) > count:
        peers.sort(key=lambda p: abs((p.get("market_cap") or 0) - target_mcap))
    return [p["ticker"] for p in peers[:count]]


def main():
    parser = argparse.ArgumentParser(description="Run full stock valuation data pipeline.")
    parser.add_argument("ticker", help="Stock ticker symbol")
    parser.add_argument("--peers", nargs="+", help="Peer tickers (auto-detected if omitted)")
    parser.add_argument("--output", help="Output JSON path (default: /tmp/TICKER_data.json)")
    args = parser.parse_args()

    ticker = args.ticker.upper()
    output_path = args.output or f"/tmp/{ticker}_data.json"

    # Detect peers if not provided
    if args.peers:
        peers = [p.upper() for p in args.peers]
    else:
        print(f"Auto-detecting peers for {ticker}...", file=sys.stderr)
        peers = detect_peers(ticker)
        print(f"Peers: {peers}", file=sys.stderr)

    # Define all tasks: (key, script_name, script_args)
    tasks = [
        ("_fundamentals", "fetch_fundamentals.py", [ticker] + peers),
        ("technicals", "fetch_technicals.py", [ticker]),
        ("historical_valuation", "fetch_historical_valuation.py", [ticker]),
        ("dcf", "dcf_model.py", [ticker]),
        ("insiders", "fetch_insiders.py", [ticker]),
        ("options", "fetch_options.py", [ticker]),
        ("earnings", "fetch_earnings_calendar.py", [ticker]),
        ("_charts", "generate_charts.py", [ticker]),
    ]

    results = {}
    print(f"Running {len(tasks)} data scripts in parallel...", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_key = {}
        for key, script, script_args in tasks:
            future = executor.submit(run_script, script, script_args)
            future_to_key[future] = (key, script)

        for future in as_completed(future_to_key):
            key, script = future_to_key[future]
            try:
                results[key] = future.result()
            except Exception as e:
                results[key] = {"error": str(e)}
            status = "error" if "error" in results[key] else "ok"
            print(f"  {script}: {status}", file=sys.stderr)

    # Build merged output
    output = {
        "ticker": ticker,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }

    # Split fundamentals into target + peers
    fund_data = results.get("_fundamentals", {})
    if "error" in fund_data:
        output["fundamentals"] = fund_data
        output["peers"] = {}
    else:
        output["fundamentals"] = fund_data.get(ticker, {})
        output["peers"] = {p: fund_data.get(p, {}) for p in peers if p in fund_data}

    # Add other sections
    for key in ["technicals", "historical_valuation", "dcf", "insiders", "options", "earnings"]:
        output[key] = results.get(key, {"error": "script not run"})

    # Charts: extract paths into a clean dict
    charts_data = results.get("_charts", {})
    if "error" in charts_data:
        output["charts"] = charts_data
    else:
        chart_map = {}
        for c in charts_data.get("charts", []):
            ctype = c.get("type", "")
            # Normalize type names to short keys
            if "price" in ctype:
                chart_map["price"] = c["path"]
            elif "revenue" in ctype:
                chart_map["revenue"] = c["path"]
            elif "margin" in ctype:
                chart_map["margins"] = c["path"]
            elif "pe" in ctype:
                chart_map["pe"] = c["path"]
            else:
                chart_map[ctype] = c["path"]
        output["charts"] = chart_map

    # Write output
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(output_path)


if __name__ == "__main__":
    main()
