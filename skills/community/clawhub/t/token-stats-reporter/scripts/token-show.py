#!/usr/bin/env python3
"""
token-show.py - Token 统计输出脚本（通用版）
支持自定义参考费率，默认使用 Anthropic Claude Opus 4 费率

用法:
    python3 token-show.py                          # 使用默认 Opus 4 费率
    python3 token-show.py --model sonnet           # 使用 Sonnet 费率
    python3 token-show.py --rates 3 15 0.3         # 自定义费率 (input output cache)
"""
import json
import argparse
from pathlib import Path
from datetime import datetime

HOME = Path.home()
SESSIONS_DIR = HOME / ".openclaw/agents/main/sessions"

# 默认 Anthropic Claude Opus 4 费率
# Anthropic Claude Opus 4.7 参考费率
OPENAI_INPUT_RATE = 15.00   # $/MTok for input (Opus 4.7)
OPENAI_OUTPUT_RATE = 75.00   # $/MTok for output (Opus 4.7)
OPENAI_CACHE_RATE = 1.125    # $/MTok for cache read (Opus 4.7)
USD_TO_CNY = 7.20           # 美元换人民币汇率

# OpenAI GPT-5.5 参考费率
OPENAI_INPUT_RATE_OPENAI = 5.00   # $/MTok for input (GPT-5.5)
OPENAI_OUTPUT_RATE_OPENAI = 30.00  # $/MTok for output (GPT-5.5)
OPENAI_CACHE_RATE_OPENAI = 1.25    # $/MTok for cache read (GPT-5.5)

DEFAULT_RATES = {
    "opus4.7": {"input": OPENAI_INPUT_RATE, "output": OPENAI_OUTPUT_RATE, "cache": OPENAI_CACHE_RATE, "name": "Opus 4.7"},
    "openai": {"input": OPENAI_INPUT_RATE_OPENAI, "output": OPENAI_OUTPUT_RATE_OPENAI, "cache": OPENAI_CACHE_RATE_OPENAI, "name": "OpenAI GPT-5.5"},
}

USD_TO_CNY = 7.20


def get_current_month():
    return datetime.now().strftime("%Y-%m")


def format_int(n):
    return str(int(n))


def format_compact(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.2f}k"
    return str(int(n))


def format_cost(c):
    if c < 0.01:
        return f"¥{c:.4f}"
    return f"¥{c:.2f}"


def calc_cost(inp, out, cache, rates):
    inp_usd = inp / 1_000_000 * rates["input"]
    out_usd = out / 1_000_000 * rates["output"]
    cache_usd = cache / 1_000_000 * rates["cache"]
    return (inp_usd + out_usd + cache_usd) * USD_TO_CNY


def get_model():
    try:
        files = list(SESSIONS_DIR.glob("*.jsonl"))
        if not files:
            return "unknown"
        latest = max(files, key=lambda f: f.stat().st_mtime)
        with open(latest) as f:
            for line in reversed(f.readlines()):
                if not line.strip():
                    continue
                try:
                    d = json.loads(line.strip())
                    if d.get("type") == "message":
                        m = d.get("message", {}).get("model", "")
                        if m:
                            return m.split("/")[-1] if "/" in m else m
                except:
                    continue
        return "unknown"
    except:
        return "unknown"


def get_last_msg_usage():
    try:
        files = list(SESSIONS_DIR.glob("*.jsonl"))
        if not files:
            return {}
        latest = max(files, key=lambda f: f.stat().st_mtime)
        with open(latest) as f:
            for line in reversed(f.readlines()):
                if not line.strip():
                    continue
                try:
                    d = json.loads(line.strip())
                    if d.get("type") == "message":
                        msg = d.get("message", {})
                        if msg.get("role") == "assistant":
                            u = msg.get("usage", {})
                            if u:
                                inp = u.get("input", 0) or u.get("inputTokens", 0)
                                out = u.get("output", 0) or u.get("outputTokens", 0)
                                cache = u.get("cacheRead", 0) or u.get("cacheTokens", 0)
                                return {"input": inp, "output": out, "cacheRead": cache}
                except:
                    continue
        return {}
    except:
        return {}


def scan_monthly_tokens(month=None):
    if month is None:
        month = get_current_month()
    total_in = total_out = total_cache = 0
    msg_count = 0
    for jf in list(SESSIONS_DIR.glob("*.jsonl")):
        try:
            with open(jf) as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        d = json.loads(line.strip())
                    except:
                        continue
                    if d.get("type") != "message":
                        continue
                    msg = d.get("message", {})
                    if msg.get("role") != "assistant":
                        continue
                    u = msg.get("usage", {})
                    if not u:
                        continue
                    inp = u.get("input", 0) or u.get("inputTokens", 0)
                    out = u.get("output", 0) or u.get("outputTokens", 0)
                    if inp <= 0 and out <= 0:
                        continue
                    ts = msg.get("timestamp", 0)
                    if ts:
                        msg_month = datetime.fromtimestamp(ts / 1000).strftime("%Y-%m")
                        if msg_month != month:
                            continue
                    total_in += inp
                    total_out += out
                    total_cache += u.get("cacheRead", 0) or u.get("cacheTokens", 0)
                    msg_count += 1
        except:
            continue
    return {
        "input": total_in,
        "output": total_out,
        "cacheRead": total_cache,
        "msg_count": msg_count,
    }


def main():
    parser = argparse.ArgumentParser(description="Token 统计输出")
    parser.add_argument("--model", "-m", choices=["opus4.7", "openai"], default="opus4.7",
                        help="选择参考费率模型 (默认: opus4.7)")
    parser.add_argument("--rates", "-r", nargs=3, type=float, metavar=("INPUT", "OUTPUT", "CACHE"),
                        help="自定义费率 (美元/百万tokens)")
    args = parser.parse_args()

    if args.rates:
        rates = {"input": args.rates[0], "output": args.rates[1], "cache": args.rates[2], "name": "custom"}
    else:
        rates = DEFAULT_RATES[args.model]

    monthly = scan_monthly_tokens(get_current_month())
    last = get_last_msg_usage()
    si = last.get("input", 0)
    so = last.get("output", 0)
    sc = last.get("cacheRead", 0)
    st = si + so + sc
    monthly_total = monthly["input"] + monthly["output"] + monthly["cacheRead"]

    single_cost = calc_cost(si, so, sc, rates)
    monthly_cost = calc_cost(monthly["input"], monthly["output"], monthly["cacheRead"], rates)

    line = (
        f"📊 Token: {format_int(si)} in / {format_int(so)} out | "
        f"cacheRead: {format_int(sc)} | "
        f"本次总消耗: {format_compact(st)} | "
        f"本月: {format_int(monthly['msg_count'])} 次 | "
        f"月累计: {format_compact(monthly_total)} | "
        f"💰 本次({rates['name']}参考){format_cost(single_cost)} | "
        f"💰 本月({rates['name']}参考){format_cost(monthly_cost)} | "
        f"模型: {get_model()}"
    )
    print(line)


if __name__ == "__main__":
    main()