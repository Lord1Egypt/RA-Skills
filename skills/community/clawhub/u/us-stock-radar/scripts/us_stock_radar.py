#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import io
import json
import math
import statistics
from typing import Dict, List, Optional

import requests

SKILL_VERSION = "0.1.1"
YQ = "https://query1.finance.yahoo.com/v7/finance/quote"
YH_CHART = "https://query1.finance.yahoo.com/v8/finance/chart"
YH_SUMMARY = "https://query2.finance.yahoo.com/v10/finance/quoteSummary"
PUBLIC_SOURCES = [
    "Yahoo Finance quote API: /v7/finance/quote",
    "Yahoo Finance chart API: /v8/finance/chart",
    "Yahoo Finance quoteSummary API: /v10/finance/quoteSummary",
    "Stooq public quote/history CSV endpoints (fallback)",
]


def req_json(url: str, params: Dict = None, timeout: int = 12):
    r = requests.get(url, params=params or {}, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.json()


def detect_language(text: str) -> str:
    return "zh" if any("\u4e00" <= c <= "\u9fff" for c in text) else "en"


def sma(values: List[float], n: int) -> Optional[float]:
    if len(values) < n:
        return None
    return statistics.mean(values[-n:])


def calc_rsi(values: List[float], period: int = 14) -> Optional[float]:
    if len(values) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(values)):
        d = values[i] - values[i - 1]
        gains.append(max(0, d))
        losses.append(max(0, -d))
    avg_gain = statistics.mean(gains[-period:])
    avg_loss = statistics.mean(losses[-period:])
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def val_or_raw(x):
    if isinstance(x, dict):
        return x.get("raw", x.get("fmt"))
    return x


def fetch_stooq_quote(ticker: str, gaps: List[str]) -> Dict:
    sym = f"{ticker.lower()}.us"
    url = f"https://stooq.com/q/l/?s={sym}&i=d"
    try:
        r = requests.get(url, timeout=12, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        txt = r.text.strip()
        rows = list(csv.DictReader(io.StringIO(txt)))
        if not rows:
            gaps.append(f"{ticker.upper()}_stooq_quote_empty")
            return {}
        row = rows[0]
        try:
            close = float(row.get("Close", "") or "nan")
        except Exception:
            close = None
        return {
            "symbol": ticker.upper(),
            "regularMarketPrice": None if close is None or math.isnan(close) else close,
            "regularMarketVolume": None,
            "marketCap": None,
            "_source": "stooq_quote_fallback",
        }
    except Exception:
        gaps.append(f"{ticker.upper()}_stooq_quote_unavailable")
        return {}


def fetch_quote(ticker: str, gaps: List[str]) -> Dict:
    try:
        j = req_json(YQ, {"symbols": ticker})
        arr = j.get("quoteResponse", {}).get("result", [])
        if arr:
            out = arr[0]
            out["_source"] = "yahoo_quote"
            return out
        gaps.append(f"{ticker.upper()}_yahoo_quote_empty")
    except Exception:
        gaps.append(f"{ticker.upper()}_yahoo_quote_unavailable")
    return fetch_stooq_quote(ticker, gaps)


def fetch_stooq_history(ticker: str, gaps: List[str]) -> Dict:
    sym = f"{ticker.lower()}.us"
    url = f"https://stooq.com/q/d/l/?s={sym}&i=d"
    try:
        r = requests.get(url, timeout=12, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        rows = list(csv.DictReader(io.StringIO(r.text)))
        closes, vols = [], []
        for row in rows:
            try:
                c = float(row.get("Close", "") or "nan")
                v = float(row.get("Volume", "") or "nan")
                if not math.isnan(c):
                    closes.append(c)
                if not math.isnan(v):
                    vols.append(v)
            except Exception:
                continue
        if not closes:
            gaps.append(f"{ticker.upper()}_stooq_history_empty")
        return {"closes": closes, "volumes": vols, "_source": "stooq_history_fallback"}
    except Exception:
        gaps.append(f"{ticker.upper()}_stooq_history_unavailable")
        return {"closes": [], "volumes": [], "_source": "stooq_history_fallback"}


def fetch_chart(ticker: str, rng: str, interval: str, gaps: List[str]) -> Dict:
    try:
        j = req_json(f"{YH_CHART}/{ticker}", {"range": rng, "interval": interval})
        result = j.get("chart", {}).get("result", [])
        if result:
            r0 = result[0]
            quotes = r0.get("indicators", {}).get("quote", [{}])[0]
            closes = [x for x in (quotes.get("close") or []) if x is not None]
            vols = [x for x in (quotes.get("volume") or []) if x is not None]
            if closes:
                return {"closes": closes, "volumes": vols, "_source": "yahoo_chart"}
        gaps.append(f"{ticker.upper()}_yahoo_chart_empty")
    except Exception:
        gaps.append(f"{ticker.upper()}_yahoo_chart_unavailable")
    return fetch_stooq_history(ticker, gaps)


def fetch_summary(ticker: str, gaps: List[str]) -> Dict:
    modules = "financialData,defaultKeyStatistics,summaryDetail,price,assetProfile"
    try:
        j = req_json(f"{YH_SUMMARY}/{ticker}", {"modules": modules})
        res = j.get("quoteSummary", {}).get("result", [])
        if res:
            out = res[0]
            out["_source"] = "yahoo_summary"
            return out
        gaps.append(f"{ticker.upper()}_yahoo_summary_empty")
    except Exception:
        gaps.append(f"{ticker.upper()}_yahoo_summary_unavailable")
    return {}


def build_metrics(ticker: str) -> Dict:
    gaps: List[str] = []
    q = fetch_quote(ticker, gaps)
    c = fetch_chart(ticker, "6mo", "1d", gaps)
    s = fetch_summary(ticker, gaps)

    closes = c.get("closes", [])
    vols = c.get("volumes", [])

    price = q.get("regularMarketPrice")
    if price is None and closes:
        price = closes[-1]
        gaps.append(f"{ticker.upper()}_price_from_history_fallback")
    ma20 = sma(closes, 20)
    ma50 = sma(closes, 50)
    rsi14 = calc_rsi(closes, 14)

    vol_now = vols[-1] if vols else None
    vol_avg20 = statistics.mean(vols[-20:]) if len(vols) >= 20 else None
    vol_spike = (vol_now / vol_avg20) if (vol_now and vol_avg20 and vol_avg20 > 0) else None

    fin = s.get("financialData", {})
    detail = s.get("summaryDetail", {})
    profile = s.get("assetProfile", {})

    pe = val_or_raw(detail.get("trailingPE") or q.get("trailingPE"))
    fpe = val_or_raw(detail.get("forwardPE") or q.get("forwardPE"))
    pb = val_or_raw(detail.get("priceToBook") or q.get("priceToBook"))
    roe = val_or_raw(fin.get("returnOnEquity"))
    debt_to_equity = val_or_raw(fin.get("debtToEquity"))
    gross_margin = val_or_raw(fin.get("grossMargins"))
    op_margin = val_or_raw(fin.get("operatingMargins"))
    rev_growth = val_or_raw(fin.get("revenueGrowth"))

    missing_fundamentals = []
    for key, value in {
        "pe": pe,
        "forward_pe": fpe,
        "pb": pb,
        "roe": roe,
        "revenue_growth": rev_growth,
    }.items():
        if value is None:
            missing_fundamentals.append(key)

    if missing_fundamentals:
        gaps.append(f"{ticker.upper()}_missing_fundamentals:" + ",".join(missing_fundamentals))

    return {
        "ticker": ticker.upper(),
        "price": price,
        "market_cap": q.get("marketCap"),
        "sector": q.get("sector") or profile.get("sector"),
        "industry": q.get("industry") or profile.get("industry"),
        "pe": pe,
        "forward_pe": fpe,
        "pb": pb,
        "roe": roe,
        "debt_to_equity": debt_to_equity,
        "gross_margin": gross_margin,
        "operating_margin": op_margin,
        "revenue_growth": rev_growth,
        "rsi14": round(rsi14, 2) if rsi14 is not None else None,
        "ma20": round(ma20, 2) if ma20 is not None else None,
        "ma50": round(ma50, 2) if ma50 is not None else None,
        "vol_spike_20d": round(vol_spike, 2) if vol_spike is not None else None,
        "above_ma50": bool(price and ma50 and price > ma50),
        "availability": {
            "quote": bool(q),
            "chart": bool(closes),
            "summary": bool(s),
            "fundamentals_present": len(missing_fundamentals) < 5,
        },
        "data_gaps": sorted(set(gaps)),
        "degraded_mode": bool(gaps),
        "sources_used": sorted(set(x for x in [q.get("_source"), c.get("_source"), s.get("_source")] if x)),
    }


def score_signal(m: Dict, event_mode: str = "normal") -> Dict:
    score = 0
    reasons = []

    pe_max = 35 if event_mode == "high-alert" else 40
    rsi_low, rsi_high = (35, 68) if event_mode == "high-alert" else (30, 70)

    if m.get("pe") is not None and 5 <= m["pe"] <= pe_max:
        score += 1
        reasons.append("reasonable PE range")
    if m.get("rsi14") is not None and rsi_low <= m["rsi14"] <= rsi_high:
        score += 1
        reasons.append("RSI in healthy trend zone")
    if m.get("vol_spike_20d") is not None and m["vol_spike_20d"] >= 1.3:
        score += 1
        reasons.append("volume expansion")
    if m.get("above_ma50"):
        score += 1
        reasons.append("price above MA50")
    if m.get("revenue_growth") is not None and m["revenue_growth"] > 0.08:
        score += 1
        reasons.append("solid revenue growth")
    if m.get("roe") is not None and m["roe"] > 0.12:
        score += 1
        reasons.append("healthy ROE")

    label = "A" if score >= 5 else "B" if score >= 4 else "C" if score >= 2 else "D"
    return {"score": score, "label": label, "reasons": reasons}


def confidence_for_metric(m: Dict) -> Dict:
    score = 40
    avail = m.get("availability", {})
    if avail.get("quote"):
        score += 15
    if avail.get("chart"):
        score += 20
    if avail.get("summary"):
        score += 15
    if avail.get("fundamentals_present"):
        score += 10
    if m.get("degraded_mode"):
        score -= 15
    if m.get("price") is None:
        score -= 20
    score = max(0, min(100, score))
    level = "high" if score >= 75 else "medium" if score >= 50 else "low"
    return {"score": score, "level": level}


def aggregate_availability(rows: List[Dict]) -> Dict:
    usable = [r for r in rows if r.get("ticker")]
    return {
        "tickers_requested": len(rows),
        "tickers_with_price": sum(1 for r in usable if r.get("price") is not None),
        "tickers_with_chart": sum(1 for r in usable if r.get("availability", {}).get("chart")),
        "tickers_with_summary": sum(1 for r in usable if r.get("availability", {}).get("summary")),
    }


def aggregate_data_gaps(rows: List[Dict]) -> List[str]:
    gaps = []
    for r in rows:
        gaps.extend(r.get("data_gaps", []))
        if r.get("error"):
            gaps.append(f"{r.get('ticker','UNKNOWN')}_runtime_error")
    return sorted(set(gaps))


def aggregate_confidence(rows: List[Dict]) -> Dict:
    scores = [r.get("confidence", {}).get("score") for r in rows if r.get("confidence", {}).get("score") is not None]
    if not scores:
        return {"score": 0, "level": "low"}
    score = round(statistics.mean(scores))
    level = "high" if score >= 75 else "medium" if score >= 50 else "low"
    return {"score": score, "level": level}


def mode_screener(tickers: List[str], event_mode: str) -> Dict:
    rows = []
    for t in tickers:
        try:
            m = build_metrics(t)
            sig = score_signal(m, event_mode=event_mode)
            conf = confidence_for_metric(m)
            rows.append({**m, **sig, "confidence": conf})
        except Exception as e:
            rows.append({"ticker": t.upper(), "error": str(e)[:120], "data_gaps": [f"{t.upper()}_runtime_error"], "degraded_mode": True})
    ranked = sorted([r for r in rows if "score" in r], key=lambda x: (x["score"], x.get("confidence", {}).get("score", 0)), reverse=True)
    return {
        "mode": "screener",
        "ranked": ranked,
        "raw": rows,
        "availability": aggregate_availability(rows),
        "data_gaps": aggregate_data_gaps(rows),
        "degraded_mode": any(r.get("degraded_mode") for r in rows),
        "confidence": aggregate_confidence(rows),
    }


def mode_deep_dive(ticker: str, event_mode: str) -> Dict:
    m = build_metrics(ticker)
    sig = score_signal(m, event_mode=event_mode)
    conf = confidence_for_metric(m)
    return {
        "mode": "deep-dive",
        "ticker": ticker.upper(),
        "metrics": m,
        "signal": sig,
        "availability": m.get("availability", {}),
        "data_gaps": m.get("data_gaps", []),
        "degraded_mode": m.get("degraded_mode", False),
        "confidence": conf,
    }


def mode_watchlist(tickers: List[str], event_mode: str) -> Dict:
    out = mode_screener(tickers, event_mode=event_mode)
    alerts = []
    for r in out["ranked"]:
        if r.get("label") in ["A", "B"] and r.get("vol_spike_20d") and r["vol_spike_20d"] >= 1.5:
            alerts.append({"ticker": r["ticker"], "type": "momentum", "why": "high score + volume spike"})
        if r.get("rsi14") is not None and r["rsi14"] < 30:
            alerts.append({"ticker": r["ticker"], "type": "oversold", "why": "RSI < 30"})
    return {
        "mode": "watchlist",
        "alerts": alerts,
        "ranked": out["ranked"],
        "availability": out["availability"],
        "data_gaps": out["data_gaps"],
        "degraded_mode": out["degraded_mode"],
        "confidence": out["confidence"],
    }


def explain_beginner(lang: str, payload: Dict) -> str:
    data = payload["data"]
    if data.get("mode") == "deep-dive":
        m = data["metrics"]
        s = data["signal"]
        conf = data["confidence"]
        gaps = data.get("data_gaps", [])
        if lang == "zh":
            tail = f" 数据缺口: {', '.join(gaps)}。" if gaps else ""
            return (
                f"小白版：{m['ticker']} 当前信号等级 {s['label']}（{s['score']}分，置信度 {conf['score']}/100）。"
                f"PE={m.get('pe')}，RSI={m.get('rsi14')}，是否站上MA50={m.get('above_ma50')}，"
                f"量能放大倍数={m.get('vol_spike_20d')}。"
                f"这表示它目前处于{'偏强' if s['label'] in ['A','B'] else '偏弱/中性'}状态。{tail}"
            )
        tail = f" Data gaps: {', '.join(gaps)}." if gaps else ""
        return (
            f"Beginner view: {m['ticker']} has signal grade {s['label']} ({s['score']} points, confidence {conf['score']}/100). "
            f"PE={m.get('pe')}, RSI={m.get('rsi14')}, above MA50={m.get('above_ma50')}, volume spike={m.get('vol_spike_20d')}x. "
            f"This implies a {'stronger' if s['label'] in ['A','B'] else 'weaker/neutral'} setup right now.{tail}"
        )
    if lang == "zh":
        return f"小白版：A/B 通常代表信号更完整，C/D 代表条件不够，先观察再行动。整体置信度 {data.get('confidence',{}).get('score')} /100。"
    return f"Beginner view: A/B means stronger alignment of conditions; C/D means incomplete setup, watch first. Overall confidence {data.get('confidence',{}).get('score')}/100."


def explain_pro(lang: str, payload: Dict) -> str:
    data = payload["data"]
    mode = data.get("mode")
    if mode == "screener":
        top = data.get("ranked", [])[:5]
        if lang == "zh":
            return "Screener 完成。Top名单: " + ", ".join([f"{x['ticker']}({x['label']}/{x['score']},c{x.get('confidence',{}).get('score')})" for x in top])
        return "Screener complete. Top candidates: " + ", ".join([f"{x['ticker']}({x['label']}/{x['score']},c{x.get('confidence',{}).get('score')})" for x in top])
    if mode == "watchlist":
        alerts = data.get("alerts", [])
        if lang == "zh":
            return f"Watchlist 完成。触发提醒 {len(alerts)} 条，整体置信度 {data.get('confidence',{}).get('score')}/100。"
        return f"Watchlist complete. {len(alerts)} alerts triggered, overall confidence {data.get('confidence',{}).get('score')}/100."
    if mode == "deep-dive":
        m = data["metrics"]
        s = data["signal"]
        conf = data["confidence"]
        if lang == "zh":
            return f"{m['ticker']} 信号 {s['label']}({s['score']})；核心：PE={m.get('pe')}, RSI={m.get('rsi14')}, RevGrowth={m.get('revenue_growth')}；置信度 {conf['score']}/100。"
        return f"{m['ticker']} signal {s['label']}({s['score']}); core: PE={m.get('pe')}, RSI={m.get('rsi14')}, RevGrowth={m.get('revenue_growth')}; confidence {conf['score']}/100."
    return ""


def main():
    ap = argparse.ArgumentParser(description="US Stock Radar: screener / deep-dive / watchlist")
    ap.add_argument("--mode", choices=["screener", "deep-dive", "watchlist"], default="screener")
    ap.add_argument("--tickers", default="AAPL,MSFT,NVDA,AMZN,GOOGL,META,TSLA")
    ap.add_argument("--ticker", default="AAPL")
    ap.add_argument("--event-mode", choices=["normal", "high-alert"], default="normal")
    ap.add_argument("--audience", choices=["pro", "beginner"], default="pro")
    ap.add_argument("--lang", choices=["auto", "en", "zh"], default="auto")
    ap.add_argument("--prompt", default="")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sources", action="store_true", help="Print public data sources and exit")
    ap.add_argument("--version", action="store_true", help="Print script version and exit")
    args = ap.parse_args()

    if args.version:
        print(SKILL_VERSION)
        return

    if args.sources:
        print(json.dumps({
            "version": SKILL_VERSION,
            "read_only": True,
            "authenticated": False,
            "public_sources": PUBLIC_SOURCES,
        }, ensure_ascii=False, indent=2))
        return

    tickers = [x.strip().upper() for x in args.tickers.split(",") if x.strip()]
    if args.mode == "screener":
        data = mode_screener(tickers, args.event_mode)
    elif args.mode == "deep-dive":
        data = mode_deep_dive(args.ticker.upper(), args.event_mode)
    else:
        data = mode_watchlist(tickers, args.event_mode)

    payload = {
        "as_of_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "version": SKILL_VERSION,
        "read_only": True,
        "authenticated": False,
        "event_mode": args.event_mode,
        "sources": PUBLIC_SOURCES,
        "notes": [
            "Free public endpoints can be rate-limited or partially unavailable",
            "Signal grades are heuristic, not investment advice",
            "Missing fundamentals reduce confidence and may activate degraded_mode",
        ],
        "data": data,
    }

    lang = detect_language(args.prompt) if args.lang == "auto" else args.lang
    text = explain_beginner(lang, payload) if args.audience == "beginner" else explain_pro(lang, payload)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(text)
        print("\n--- JSON ---")
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
