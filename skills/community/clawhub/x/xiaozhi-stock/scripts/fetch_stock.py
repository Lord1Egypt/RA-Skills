#!/usr/bin/env python3
"""
小智A股数据引擎 — 多源行情抓取脚本
数据源优先级：新浪财经（主）→ 东方财富（备）→ 腾讯行情（再备）
融合自 a-stock-trading-assistant + BigA 的数据层设计
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime

# 解决Windows GBK终端emoji输出问题
if sys.stdout.encoding and sys.stdout.encoding.upper() in ('GBK', 'GB2312', 'CP936'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://finance.sina.com.cn",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

# ============ 市场识别 ============

def get_market_prefix(code: str) -> tuple:
    """返回 (prefix, clean_code)"""
    code = code.strip().upper()
    if code.startswith(("SH", "SZ")):
        return code[:2].lower(), code[2:]
    if code.startswith(("BJ",)):
        return "bj", code[2:]
    clean = re.sub(r"[^0-9]", "", code)
    if clean.startswith(("60", "68", "51", "58", "11")):
        return "sh", clean
    elif clean.startswith(("00", "30", "15", "12", "16", "13")):
        return "sz", clean
    elif clean.startswith(("8", "4")) and len(clean) == 6:
        return "bj", clean
    return "sh", clean

# ============ HTTP 工具 ============

def fetch_url(url: str, extra_headers: dict = None, encoding: str = None) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    if extra_headers:
        for k, v in extra_headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            enc = encoding or ("gbk" if "sina" in url or "sinajs" in url else "utf-8")
            return resp.read().decode(enc, errors="replace")
    except Exception:
        return ""

# ============ 新浪财经（主） ============

def parse_sina_stock(raw: str, symbol: str) -> dict:
    match = re.search(r'"([^"]*)"', raw)
    if not match:
        return {}
    parts = match.group(1).split(",")
    if len(parts) < 32:
        return {}
    try:
        name = parts[0]
        prev_close = float(parts[2]) if parts[2] else 0
        open_price = float(parts[1]) if parts[1] else 0
        current = float(parts[3]) if parts[3] else 0
        high = float(parts[4]) if parts[4] else 0
        low = float(parts[5]) if parts[5] else 0
        volume = int(parts[8]) if parts[8] else 0
        amount = float(parts[9]) if parts[9] else 0
        date_str = parts[30] if len(parts) > 30 else ""
        time_str = parts[31] if len(parts) > 31 else ""
        change = current - prev_close
        change_pct = (change / prev_close * 100) if prev_close else 0
        return {
            "symbol": symbol,
            "name": name,
            "current": round(current, 2),
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
            "open": round(open_price, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "prev_close": round(prev_close, 2),
            "volume_lot": volume,
            "amount_yuan": round(amount, 2),
            "amount_yi": round(amount / 1e8, 2),
            "turnover_pct": None,
            "date": date_str,
            "time": time_str,
            "source": "新浪财经",
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    except (ValueError, IndexError):
        return {}

def fetch_sina(code: str) -> dict:
    prefix, clean = get_market_prefix(code)
    symbol = f"{prefix}{clean}"
    url = f"http://hq.sinajs.cn/list={symbol}"
    raw = fetch_url(url)
    if raw:
        data = parse_sina_stock(raw, symbol)
        if data:
            return data
    return {}

# ============ 东方财富（备） ============

def fetch_eastmoney(code: str) -> dict:
    _, clean = get_market_prefix(code)
    if clean.startswith(("60", "68")):
        market = 1
    elif clean.startswith(("00", "30", "15")):
        market = 0
    elif clean.startswith(("8", "4")):
        market = 2
    else:
        market = 1
    url = (
        f"http://push2.eastmoney.com/api/qt/stock/get"
        f"?secid={market}.{clean}"
        f"&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f107,f169,f170,f171,f116"
    )
    raw = fetch_url(url, {"Referer": "https://www.eastmoney.com"}, encoding="utf-8")
    if not raw:
        return {}
    try:
        obj = json.loads(raw)
        d = obj.get("data", {}) or {}
        if not d.get("f43"):
            return {}
        prev = d["f60"] / 100
        curr = d["f43"] / 100
        chg = d["f169"] / 100
        chg_pct = d["f170"] / 100
        return {
            "symbol": f"{'sh' if market == 1 else 'sz'}{clean}",
            "name": d.get("f58", ""),
            "current": round(curr, 2),
            "change": round(chg, 2),
            "change_pct": round(chg_pct, 2),
            "open": round(d["f46"] / 100, 2) if d.get("f46") else 0,
            "high": round(d["f44"] / 100, 2) if d.get("f44") else 0,
            "low": round(d["f45"] / 100, 2) if d.get("f45") else 0,
            "prev_close": round(prev, 2),
            "volume_lot": d.get("f47", 0) or 0,
            "amount_yuan": d.get("f48", 0) or 0,
            "amount_yi": round((d.get("f48", 0) or 0) / 1e8, 2),
            "turnover_pct": round((d.get("f171", 0) or 0) / 100, 2),
            "pe": round((d.get("f116", 0) or 0) / 100, 2) if d.get("f116") else None,
            "source": "东方财富",
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception:
        return {}

# ============ 腾讯行情（再备） ============

def fetch_tencent(code: str) -> dict:
    prefix, clean = get_market_prefix(code)
    symbol_map = {"sh": "sh", "sz": "sz", "bj": "bj"}
    tencent_prefix = symbol_map.get(prefix, "sh")
    url = f"http://qt.gtimg.cn/q={tencent_prefix}{clean}"
    raw = fetch_url(url, encoding="gbk")
    if not raw:
        return {}
    try:
        parts = raw.split("~")
        if len(parts) < 40:
            return {}
        return {
            "symbol": f"{prefix}{clean}",
            "name": parts[1],
            "current": float(parts[3]) if parts[3] else 0,
            "change": float(parts[31]) if parts[31] else 0,
            "change_pct": float(parts[32]) if parts[32] else 0,
            "open": float(parts[5]) if parts[5] else 0,
            "high": float(parts[33]) if parts[33] else 0,
            "low": float(parts[34]) if parts[34] else 0,
            "prev_close": float(parts[4]) if parts[4] else 0,
            "volume_lot": int(parts[6]) if parts[6] else 0,
            "amount_yuan": float(parts[37]) if parts[37] else 0,
            "amount_yi": round(float(parts[37]) / 1e8, 2) if parts[37] else 0,
            "turnover_pct": float(parts[38]) if parts[38] else 0,
            "pe": float(parts[39]) if parts[39] else None,
            "source": "腾讯行情",
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    except (ValueError, IndexError):
        return {}

# ============ 统一入口 ============

def fetch_stock(code: str) -> dict:
    """多源自动切换：新浪主 → 东财备 → 腾讯再备"""
    data = fetch_sina(code)
    if data:
        return data
    data = fetch_eastmoney(code)
    if data:
        return data
    data = fetch_tencent(code)
    if data:
        return data
    return {"error": f"所有数据源均无法获取 {code}", "symbol": code}

def fetch_stocks(codes: list) -> list:
    """批量查询"""
    return [fetch_stock(c) for c in codes]

# ============ 大盘指数 ============

def fetch_indices() -> list:
    symbols = "s_sh000001,s_sz399001,s_sz399006,s_sh000688,s_bj899050"
    names = {
        "s_sh000001": "上证指数", "s_sz399001": "深证成指",
        "s_sz399006": "创业板指", "s_sh000688": "科创50", "s_bj899050": "北证50",
    }
    url = f"http://hq.sinajs.cn/list={symbols}"
    raw = fetch_url(url)
    results = []
    if raw:
        for sym, name in names.items():
            m = re.search(rf'hq_str_{re.escape(sym)}="([^"]*)"', raw)
            if m:
                parts = m.group(1).split(",")
                if len(parts) >= 6:
                    try:
                        results.append({
                            "name": parts[0] or name,
                            "current": float(parts[1]),
                            "change": float(parts[2]),
                            "change_pct": float(parts[3]),
                            "amount_yi": round(float(parts[5]) / 1e8, 2),
                        })
                    except (ValueError, IndexError):
                        pass
    if not results:
        # 备选：东财指数
        for idx_name, eid in [("上证指数", "1.000001"), ("深证成指", "0.399001"),
                               ("创业板指", "0.399006"), ("科创50", "1.000688")]:
            url2 = f"http://push2.eastmoney.com/api/qt/stock/get?secid={eid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f170,f169"
            raw2 = fetch_url(url2, {"Referer": "https://www.eastmoney.com"})
            if raw2:
                try:
                    d = json.loads(raw2).get("data", {}) or {}
                    if d.get("f43"):
                        results.append({
                            "name": d.get("f58", idx_name),
                            "current": d["f43"] / 100,
                            "change": d["f169"] / 100,
                            "change_pct": d["f170"] / 100,
                            "amount_yi": round((d.get("f48", 0) or 0) / 1e8, 2),
                        })
                except Exception:
                    pass
    return results

# ============ 热点板块 ============

def fetch_hot_sectors() -> list:
    """热点板块，先用行业板块(t:3)，备选概念板块(t:2)"""
    # 行业板块
    url = (
        "http://push2.eastmoney.com/api/qt/clist/get"
        "?pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281"
        "&fltt=2&invt=2&fid=f3"
        "&fs=m:90+t:3"
        "&fields=f2,f3,f4,f12,f14,f20"
    )
    raw = fetch_url(url, {"Referer": "https://www.eastmoney.com"})
    results = []
    if raw:
        try:
            items = json.loads(raw).get("data", {}).get("diff", [])
            for item in items:
                results.append({
                    "name": item.get("f14", ""),
                    "change_pct": round(item.get("f3", 0), 2),
                    "leading_stock": None,
                    "leading_change_pct": None,
                    "amount_yi": round(item.get("f20", 0) / 1e8, 2),
                })
        except Exception:
            pass
    # 如果行业板块为空，试概念板块
    if not results:
        url2 = url.replace("t:3", "t:2")
        raw2 = fetch_url(url2, {"Referer": "https://www.eastmoney.com"})
        if raw2:
            try:
                items = json.loads(raw2).get("data", {}).get("diff", [])
                for item in items:
                    results.append({
                        "name": item.get("f14", ""),
                        "change_pct": round(item.get("f3", 0), 2),
                        "leading_stock": None,
                        "leading_change_pct": None,
                        "amount_yi": round(item.get("f20", 0) / 1e8, 2),
                    })
            except Exception:
                pass
    return results

# ============ 格式化输出 ============

def fmt_stock(d: dict) -> str:
    if "error" in d:
        return f"❌ {d['error']}"
    sign = "+" if d["change"] >= 0 else ""
    emoji = "🔴" if d["change"] >= 0 else "🟢"
    lines = [
        f"{emoji} **{d['name']}**（{d['symbol'].upper()}）",
        f"  当前价：**{d['current']}** 元",
        f"  涨跌幅：{sign}{d['change_pct']}%  涨跌额：{sign}{d['change']}",
        f"  今开：{d['open']}  最高：{d['high']}  最低：{d['low']}  昨收：{d['prev_close']}",
        f"  成交量：{d['volume_lot']:,} 手  成交额：{d['amount_yi']} 亿",
    ]
    if d.get("turnover_pct") is not None:
        lines.append(f"  换手率：{d['turnover_pct']}%")
    if d.get("pe") is not None:
        lines.append(f"  市盈率：{d['pe']}")
    lines.append(f"  📡 {d['source']} | {d['fetch_time']}")
    return "\n".join(lines)

def fmt_indices(items: list) -> str:
    lines = ["📊 **大盘指数**"]
    for d in items:
        sign = "+" if d["change"] >= 0 else ""
        emoji = "🔴" if d["change"] >= 0 else "🟢"
        chg_str = f"{sign}{d['change']:.2f}".lstrip('+')
        lines.append(f"  {emoji} {d['name']}: **{d['current']:,.2f}**  {chg_str} ({sign}{d['change_pct']}%)  成交额 {d['amount_yi']} 亿")
    return "\n".join(lines)

def fmt_sectors(items: list) -> str:
    lines = ["🔥 **热点板块领涨**"]
    for i, d in enumerate(items[:10], 1):
        sign = "+" if d["change_pct"] >= 0 else ""
        if d.get("leading_stock"):
            lines.append(f"  {i}. {d['name']:<12} {sign}{d['change_pct']}%  龙头：{d['leading_stock']}({sign}{d['leading_change_pct']}%)")
        else:
            lines.append(f"  {i}. {d['name']:<12} {sign}{d['change_pct']}%  成交额：{d['amount_yi']}亿")
    if len(items) > 10:
        lines.append(f"  ...还有{len(items)-10}个板块")
    lines.append(f"  📡 东方财富 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return "\n".join(lines)

# ============ CLI ============

def main():
    parser = argparse.ArgumentParser(description="小智A股数据引擎 v1.0")
    parser.add_argument("--code", nargs="+", help="股票代码")
    parser.add_argument("--index", action="store_true", help="大盘指数")
    parser.add_argument("--hot-sectors", action="store_true", help="热点板块")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    if args.index:
        data = fetch_indices()
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(fmt_indices(data))
        return

    if args.hot_sectors:
        data = fetch_hot_sectors()
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(fmt_sectors(data))
        return

    if args.code:
        results = fetch_stocks(args.code)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for d in results:
                print(fmt_stock(d))
                print()
        return

    parser.print_help()

if __name__ == "__main__":
    main()
