#!/usr/bin/env python3
"""
summarize_weather.py - Summarize Shanghai weather via summarize CLI with a local LLM for WeatherPanel Note AI PC.
Passes Open-Meteo URL to summarize. Config in ~/.summarize/config.json.
Writes summaries.json and token_cost.json to Canvas dir.
"""

import json
import os
import sys
import subprocess
import hashlib
import re
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import env_loader

STATE_DIR = env_loader.STATE_DIR
CANVAS_ROOT = os.environ.get("CANVAS_ROOT", env_loader.CANVAS_ROOT_DEFAULT)
CANVAS_DIR = os.path.join(CANVAS_ROOT, "weatherpanel-note-aipc")

TIMESERIES_FILE = os.path.join(CANVAS_DIR, "timeseries.json")
SUMMARIES_FILE = os.path.join(CANVAS_DIR, "summaries.json")
TOKEN_COST_FILE = os.path.join(CANVAS_DIR, "token_cost.json")
QUEUE_FILE = os.path.join(STATE_DIR, "summary_queue.jsonl")
LAST_SUMMARY_FILE = os.path.join(STATE_DIR, "last_summary.txt")

SUMMARIZE_BIN = os.environ.get("SUMMARIZE_BIN", "summarize")
MAX_SUMMARIES = 144

LAT = os.environ.get("WEATHER_LAT", "31.2304")
LON = os.environ.get("WEATHER_LON", "121.4737")
TZ = os.environ.get("WEATHER_TZ", "Asia/Shanghai")
UNITS = os.environ.get("WEATHER_UNITS", "metric")

COST_PER_INPUT_TOKEN = 0.0
COST_PER_OUTPUT_TOKEN = 0.0


def load_json(path, default=None):
    if default is None:
        default = []
    if os.path.exists(path):
        for enc in ["utf-8", "gbk"]:
            try:
                with open(path, "r", encoding=enc) as f:
                    data = json.load(f)
                if enc != "utf-8":
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                return data
            except (json.JSONDecodeError, UnicodeDecodeError, IOError):
                continue
        return default
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_token_cost():
    return load_json(TOKEN_COST_FILE, {
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "total_cost_usd": 0.0,
        "calls": 0,
        "history": []
    })


def build_open_meteo_url():
    temp_unit = "fahrenheit" if UNITS == "imperial" else "celsius"
    wind_unit = "mph" if UNITS == "imperial" else "kmh"
    precip_unit = "inch" if UNITS == "imperial" else "mm"

    base = "https://api.open-meteo.com/v1/forecast"
    params = (
        f"latitude={LAT}&longitude={LON}"
        f"&timezone={TZ}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"precipitation,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m,"
        f"wind_gusts_10m,surface_pressure"
        f"&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"precipitation_probability,precipitation,wind_speed_10m,cloud_cover,weather_code"
        f"&forecast_hours=24"
        f"&temperature_unit={temp_unit}"
        f"&wind_speed_unit={wind_unit}"
        f"&precipitation_unit={precip_unit}"
    )
    return f"{base}?{params}"


def run_summarize(url):
    """Run summarize CLI. Uses shell=True to protect & in URL from cmd.exe."""
    cmd_str = f'"{SUMMARIZE_BIN}" "{url}"'
    print(f"[summarize] URL: {url}")

    try:
        result = subprocess.run(
            cmd_str,
            capture_output=True,
            text=True,
            timeout=180,
            encoding="utf-8",
            shell=True,
        )

        stdout = result.stdout.strip()
        stderr = result.stderr or ""

        if result.returncode != 0:
            print(f"[summarize] CLI error rc={result.returncode}:", file=sys.stderr)
            print(f"[summarize] stderr: {stderr}", file=sys.stderr)
            return None, 0, 0

        if not stdout:
            print("[summarize] CLI returned empty.", file=sys.stderr)
            if stderr:
                print(f"[summarize] stderr: {stderr}", file=sys.stderr)
            return None, 0, 0

        input_tokens = 0
        output_tokens = 0
        tok_match = re.search(r"(\d+)\s*input.*?(\d+)\s*output", stderr, re.IGNORECASE)
        if tok_match:
            input_tokens = int(tok_match.group(1))
            output_tokens = int(tok_match.group(2))
        else:
            tok_total = re.search(r"(\d+)\s*tokens?", stderr, re.IGNORECASE)
            if tok_total:
                total = int(tok_total.group(1))
                input_tokens = int(total * 0.7)
                output_tokens = total - input_tokens
            else:
                input_tokens = 500
                output_tokens = len(stdout) // 4

        return stdout, input_tokens, output_tokens

    except subprocess.TimeoutExpired:
        print("[summarize] Timeout after 180s.", file=sys.stderr)
        return None, 0, 0
    except FileNotFoundError:
        print(f"[summarize] '{SUMMARIZE_BIN}' not found.", file=sys.stderr)
        return None, 0, 0


def enqueue_for_obsidian(summary_text, timestamp):
    record_id = hashlib.sha256(
        f"{timestamp}:{summary_text[:100]}".encode()
    ).hexdigest()[:16]
    record = {"id": record_id, "timestamp": timestamp, "content": summary_text}
    with open(QUEUE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record_id


def main():
    os.makedirs(STATE_DIR, exist_ok=True)
    os.makedirs(CANVAS_DIR, exist_ok=True)

    ts = load_json(TIMESERIES_FILE, [])
    if not ts:
        print("[summarize] No timeseries data. Run fetch_weather.py first.", file=sys.stderr)
        sys.exit(0)

    url = build_open_meteo_url()
    print(f"[summarize] Summarizing for ({LAT}, {LON}) via local LLM...")
    summary, in_tok, out_tok = run_summarize(url)

    if not summary:
        print("[summarize] No summary produced.")
        sys.exit(1)

    now = datetime.now(timezone.utc).isoformat()

    cost = load_token_cost()
    call_cost = (in_tok * COST_PER_INPUT_TOKEN) + (out_tok * COST_PER_OUTPUT_TOKEN)
    cost["total_input_tokens"] += in_tok
    cost["total_output_tokens"] += out_tok
    cost["total_cost_usd"] += call_cost
    cost["calls"] += 1
    cost["history"].append({
        "timestamp": now, "input_tokens": in_tok,
        "output_tokens": out_tok, "cost_usd": round(call_cost, 6),
    })
    if len(cost["history"]) > 1000:
        cost["history"] = cost["history"][-1000:]
    cost["total_cost_usd"] = round(cost["total_cost_usd"], 6)
    save_json(TOKEN_COST_FILE, cost)

    summaries = load_json(SUMMARIES_FILE, [])
    summaries.append({
        "timestamp": now, "summary": summary,
        "input_tokens": in_tok, "output_tokens": out_tok,
        "cost_usd": round(call_cost, 6),
    })
    if len(summaries) > MAX_SUMMARIES:
        summaries = summaries[-MAX_SUMMARIES:]
    save_json(SUMMARIES_FILE, summaries)

    rid = enqueue_for_obsidian(summary, now)

    with open(LAST_SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write(now)

    print(f"[summarize] Done. Tokens: {in_tok} in / {out_tok} out")
    print(f"[summarize] Cumulative: {cost['total_input_tokens']} in / "
          f"{cost['total_output_tokens']} out over {cost['calls']} calls")
    print(f"[summarize] Queued for Obsidian: {rid}")


if __name__ == "__main__":
    main()
