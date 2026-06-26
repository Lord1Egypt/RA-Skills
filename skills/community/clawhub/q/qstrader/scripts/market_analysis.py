#!/usr/bin/env python3
"""
QStrader — Unified Market Analysis
Runs technical analysis + LSTM prediction for a given ticker.
"""
import subprocess, json, sys, os
from datetime import datetime, timedelta

# Auto-detect mcporter config
MCP_CONFIG = os.environ.get("MCP_CONFIG", "")
if not MCP_CONFIG:
    for p in [
        os.path.expanduser("~/.openclaw/workspace/config/mcporter.json"),
        os.path.expanduser("~/.mcporter/mcporter.json"),
        "./config/mcporter.json"
    ]:
        if os.path.exists(p):
            MCP_CONFIG = p
            break

MCP_ARGS = []
# Ensure we run from a directory with mcporter config
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
if os.path.exists(f"{WORKSPACE}/config/mcporter.json"):
    os.chdir(WORKSPACE)


def mcporter_call(args):
    """Call mcporter CLI and return parsed JSON."""
    cmd = ["mcporter", "call"] + MCP_ARGS + args
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        return {"error": result.stderr.strip()[:500]}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout.strip()[:500]}


def analyze(ticker_yf):
    """Full analysis: tech + LSTM"""
    print(f"📊 Analyzing {ticker_yf}...")

    # 1. Technical Analysis
    print("  ↳ Technical analysis...")
    tech = mcporter_call(["my-n8n-mcp.get_technical_analysis", f"ticker={ticker_yf}"])

    # 2. LSTM Prediction
    print("  ↳ LSTM prediction...")
    end = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d-00-00")
    start = (datetime.now() - timedelta(days=330)).strftime("%Y-%m-%d-00-00")
    lstm = mcporter_call([
        "my-n8n-mcp.predict_future_price_lstm",
        f"ticker={ticker_yf}",
        f"start_date={start}",
        f"end_date={end}",
        "interval=1h",
        "future_steps=10",
        "time_step=512"
    ])

    # 3. Account data (for context)
    print("  ↳ Account data...")
    account = mcporter_call(["my-n8n-mcp.Get_account_data"])

    report = {
        "ticker": ticker_yf,
        "timestamp": datetime.now().isoformat(),
        "technical": tech,
        "lstm": lstm,
        "account": account
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python market_analysis.py <yahoo_finance_ticker>")
        print("Example: python market_analysis.py ^GSPC")
        sys.exit(1)
    analyze(sys.argv[1])
