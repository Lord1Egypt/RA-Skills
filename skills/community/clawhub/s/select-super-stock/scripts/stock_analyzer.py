#!/usr/bin/env python3
"""v1.4.0: source-dated, A-share single-symbol daily-bar research."""
import argparse
import json
import math
import re
import subprocess
import sys
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

VERSION = "1.4.0"
TZ = ZoneInfo("Asia/Shanghai")
MISSING = ["实时行情", "ROE/股息率/财报", "行业周期与新闻", "股东与资金流", "港股与美股覆盖", "多股票筛选与排名"]


def valid_symbol(value):
    if not re.fullmatch(r"\d{6}", value):
        raise ValueError("仅支持 6 位 A 股代码")
    return value


def finite(value):
    if isinstance(value, bool):
        raise ValueError("无效数值")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError("无效数值")
    return value


def market_symbol(symbol):
    # 6: Shanghai; 0/3: Shenzhen; 4/8/9: Beijing. The provider validates existence.
    return ("sh" if symbol.startswith("6") else "sz") + symbol


def select_day(calendar, requested, now):
    days = sorted({date.fromisoformat(str(item)[:10]) for item in calendar})
    if not days or max(days) < now.date():
        raise ValueError("交易日历覆盖不足")
    completed = [day for day in days if day < now.date() or (day == now.date() and now.time() >= time(16, 0))]
    if requested:
        target = date.fromisoformat(requested)
        if target not in completed:
            raise ValueError("请求日期不是已完成交易日")
        return target, days
    if not completed:
        raise ValueError("没有可核验的已完成交易日")
    return completed[-1], days


def normalize_rows(frame, provider):
    if provider == "sina":
        mapping = {"date": "date", "open": "open", "high": "high", "low": "low", "close": "close", "volume": "volume"}
    else:
        mapping = {"日期": "date", "开盘": "open", "最高": "high", "最低": "low", "收盘": "close", "成交量": "volume"}
    frame = frame.rename(columns=mapping)
    required = ["date", "open", "high", "low", "close", "volume"]
    if not set(required).issubset(frame.columns):
        raise ValueError("来源字段不完整")
    rows = []
    for row in frame[required].to_dict("records"):
        row["date"] = str(row["date"])[:10]
        for key in required[1:]: row[key] = finite(row[key])
        if row["close"] <= 0 or row["high"] < max(row["open"], row["close"]) or row["low"] > min(row["open"], row["close"]):
            raise ValueError("OHLC 数据不一致")
        rows.append(row)
    if len({row["date"] for row in rows}) != len(rows):
        raise ValueError("重复交易日")
    return sorted(rows, key=lambda row: row["date"])


def fetch_rows(api, symbol, target):
    start = (target - timedelta(days=550)).strftime("%Y%m%d")
    errors = []
    for provider in ("sina", "eastmoney"):
        try:
            if provider == "sina":
                frame = api.stock_zh_a_daily(symbol=market_symbol(symbol), start_date=start, end_date=target.strftime("%Y%m%d"), adjust="qfq")
                source = "AKShare/stock_zh_a_daily · 新浪财经 · 前复权日线"
            else:
                frame = api.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start, end_date=target.strftime("%Y%m%d"), adjust="qfq", timeout=10)
                source = "AKShare/stock_zh_a_hist · 东方财富 · 前复权日线"
            rows = normalize_rows(frame, provider)
            return rows, source, errors
        except Exception as exc:
            errors.append(provider + ": " + type(exc).__name__)
    raise ValueError("；".join(errors) or "无可用数据源")


def rsi(closes, period=14):
    if len(closes) < period + 1: return None
    changes = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [max(change, 0) for change in changes[-period:]]
    losses = [max(-change, 0) for change in changes[-period:]]
    avg_gain, avg_loss = sum(gains) / period, sum(losses) / period
    if avg_loss == 0: return 100.0 if avg_gain else 50.0
    return round(100 - 100 / (1 + avg_gain / avg_loss), 2)


def avg(values, period):
    return round(sum(values[-period:]) / period, 4) if len(values) >= period else None


def study(rows, symbol, target, source, now):
    target_rows = [row for row in rows if row["date"] == target.isoformat()]
    if len(target_rows) != 1: raise ValueError("来源缺少目标交易日")
    prior_rows = [row for row in rows if row["date"] < target.isoformat()]
    if not prior_rows: raise ValueError("来源缺少前一交易日")
    prior = prior_rows[-1]
    if prior["date"] != (target - timedelta(days=1)).isoformat():
        # Calendar is the authority; natural calendar yesterday may be a weekend.
        pass
    closes = [row["close"] for row in rows if row["date"] <= target.isoformat()]
    window = [row for row in rows if row["date"] <= target.isoformat()][-252:]
    current = target_rows[0]
    obs = {"close": current["close"], "day_change_pct": round((current["close"] / prior["close"] - 1) * 100, 4),
           "ma20": avg(closes, 20), "ma60": avg(closes, 60), "ma250": avg(closes, 250), "rsi14": rsi(closes),
           "range_52w_high": max((row["high"] for row in window), default=None) if len(window) == 252 else None,
           "range_52w_low": min((row["low"] for row in window), default=None) if len(window) == 252 else None}
    if obs["range_52w_high"]:
        obs["drawdown_from_52w_high_pct"] = round((current["close"] / obs["range_52w_high"] - 1) * 100, 4)
    else: obs["drawdown_from_52w_high_pct"] = None
    remarks = []
    if obs["ma20"] is not None: remarks.append("收盘相对 MA20：" + ("上方" if current["close"] >= obs["ma20"] else "下方"))
    if obs["ma60"] is not None: remarks.append("收盘相对 MA60：" + ("上方" if current["close"] >= obs["ma60"] else "下方"))
    if obs["ma250"] is not None: remarks.append("收盘相对 MA250：" + ("上方" if current["close"] >= obs["ma250"] else "下方"))
    return {"version": VERSION, "status": "partial", "symbol": symbol, "market": "A股", "trade_date": target.isoformat(),
            "collected_at": now.isoformat(), "source": source, "adjustment": "前复权", "kind": "已完成交易日日线；非实时行情",
            "observation": obs, "technical_remarks": remarks, "missing": list(MISSING),
            "conclusion": "仅作技术观察；证据不足以判断公司质量或给出交易建议", "errors": []}


def failure(symbol, now, reason):
    return {"version": VERSION, "status": "unavailable", "symbol": symbol, "market": "A股", "trade_date": None,
            "collected_at": now.isoformat(), "source": None, "adjustment": None, "kind": "无可用行情数据",
            "observation": {}, "technical_remarks": [], "missing": list(MISSING),
            "conclusion": "数据不可用，未生成股票研究结论", "errors": [reason]}


def collect(api, symbol, requested=None, now=None):
    now = now or datetime.now(TZ)
    try:
        target, _ = select_day(api.tool_trade_date_hist_sina()["trade_date"].tolist(), requested, now)
        rows, source, _ = fetch_rows(api, symbol, target)
        return study(rows, symbol, target, source, now)
    except Exception as exc:
        return failure(symbol, now, type(exc).__name__ + "；请检查网络、数据源、代码和交易日")


def render(result):
    lines = ["📊 A股单股日线研究（非实时）", "代码：" + result["symbol"], "交易日：" + str(result["trade_date"] or "不可用"),
             "采集时间：" + result["collected_at"]]
    if result["status"] == "partial":
        o = result["observation"]
        lines += ["来源：" + result["source"], "复权口径：" + result["adjustment"],
                  f"收盘：{o['close']:.2f} | 单日变化：{o['day_change_pct']:+.2f}%"]
        for key, label in [("ma20", "MA20"), ("ma60", "MA60"), ("ma250", "MA250"), ("rsi14", "RSI14"), ("drawdown_from_52w_high_pct", "距52周高点")]:
            if o.get(key) is not None: lines.append(label + "：" + str(o[key]))
        lines += ["技术观察：" + "；".join(result["technical_remarks"]), "研究结论：" + result["conclusion"]]
    else: lines.append("状态：" + result["conclusion"])
    lines += ["未覆盖/缺失：" + "、".join(result["missing"])]
    if result["errors"]: lines += ["异常：" + "；".join(result["errors"])]
    lines += ["仅供学习与信息参考，不构成投资建议。"]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbol", required=True, type=valid_symbol)
    parser.add_argument("--date")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.date:
        try:
            if date.fromisoformat(args.date).isoformat() != args.date: raise ValueError()
        except ValueError: parser.error("--date 必须为 YYYY-MM-DD")
    if not 1 <= args.timeout <= 180: parser.error("--timeout 必须在 1-180 秒间")
    if args.worker:
        try:
            import akshare as ak
            result = collect(ak, args.symbol, args.date)
        except ImportError:
            result = failure(args.symbol, datetime.now(TZ), "缺少 AKShare；不会自动安装依赖")
        print(json.dumps(result, ensure_ascii=False, allow_nan=False)); return 0
    command = [sys.executable, str(Path(__file__).resolve()), "--worker", "--symbol", args.symbol]
    if args.date: command += ["--date", args.date]
    try:
        child = subprocess.run(command, capture_output=True, text=True, timeout=args.timeout)
        result = json.loads(child.stdout) if child.returncode == 0 else failure(args.symbol, datetime.now(TZ), "采集进程失败")
    except subprocess.TimeoutExpired:
        result = failure(args.symbol, datetime.now(TZ), "真实数据采集超时；未使用默认值或缓存")
    except (ValueError, OSError):
        result = failure(args.symbol, datetime.now(TZ), "采集结果无效；未生成研究结论")
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) if args.json else render(result))
    return 0 if result["status"] == "partial" else 2


if __name__ == "__main__": sys.exit(main())
