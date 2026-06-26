#!/usr/bin/env python3
"""
🐂 UnifiedStock — 多源统一股票数据接口 v1.0

整合五大数据源: 通达信(pytdx) / 同花顺(akshare_ths) / 东方财富(新版API) / akshare / 新浪财经
自动降级: 一个源挂了自动换另一个

用法:
  python3 unified_stock.py --realtime 600839,002156         # 查实时行情
  python3 unified_stock.py --kline 600839 --days 10          # 查K线
  python3 unified_stock.py --sector-top 15                    # 板块排行
  python3 unified_stock.py --sector-stocks 917 --live         # 板块成分股+行情
  python3 unified_stock.py --search 半导体                     # 搜板块
  python3 unified_stock.py --financial 600839                 # 财务数据
  python3 unified_stock.py --status                           # 各数据源状态
"""

import sys, os, json, time, hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple

# ======================================================================
# 数据源配置
# ======================================================================
TDX_HOST = "60.12.136.250"
TDX_PORT = 7709

EASTAPI_BASE = "https://datacenter.eastmoney.com/api/data/v1/get"
EAST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Referer": "https://data.eastmoney.com/",
}

SINA_BASE = "https://hq.sinajs.cn"

# 数据源状态缓存
_source_status = {}


# ======================================================================
# 工具函数
# ======================================================================

def _ts():
    return datetime.now().strftime("%H:%M:%S")


def _log(msg: str):
    print(f"  [{_ts()}] {msg}")


def _ensure_market_prefix(code: str) -> str:
    """股票代码补市场前缀"""
    code = code.strip()
    if code.startswith(('6', '9')):
        return f"sh{code}"
    elif code.startswith(('0', '3')):
        return f"sz{code}"
    elif code.startswith(('4', '8')):
        return f"bj{code}"
    return code


def _tdx_market(code: str) -> int:
    """通达信市场代码"""
    code = code.strip()
    if code.startswith(('6', '9')):
        return 1
    elif code.startswith(('0', '2', '3')):
        return 0
    elif code.startswith(('4', '8')):
        return 0
    return 1


# ======================================================================
# 数据源 ①：通达信 pytdx (实时行情/K线/历史数据)
# ======================================================================

def _source_tdx_available() -> bool:
    """检测通达信连接"""
    try:
        from pytdx.hq import TdxHq_API
        api = TdxHq_API()
        ok = api.connect(TDX_HOST, TDX_PORT, timeout=5)
        if ok:
            api.disconnect()
            _source_status["tdx"] = "✅"
            return True
        api.disconnect()
    except Exception:
        pass
    _source_status["tdx"] = "❌"
    return False


def tdx_get_quotes(codes: List[str]) -> List[Dict]:
    """通达信：实时行情"""
    from pytdx.hq import TdxHq_API
    api = TdxHq_API()
    try:
        api.connect(TDX_HOST, TDX_PORT)
        quotes = api.get_security_quotes([(_tdx_market(c), c) for c in codes])
        api.disconnect()
        result = []
        for q in quotes:
            result.append({
                "code": q["code"] if isinstance(q["code"], str) else q["code"].decode("gbk"),
                "price": q["price"],
                "last_close": q["last_close"],
                "open": q["open"],
                "high": q["high"],
                "low": q["low"],
                "vol": q["vol"],
                "amount": q["amount"],
                "bid1": q["bid1"],
                "ask1": q["ask1"],
                "bid_vol1": q["bid_vol1"],
                "ask_vol1": q["ask_vol1"],
                "source": "tdx",
            })
        return result
    except Exception as e:
        api.disconnect()
        return [{"error": str(e), "source": "tdx"}]


def tdx_get_kline(code: str, days: int = 30) -> List[Dict]:
    """通达信：日K线"""
    from pytdx.hq import TdxHq_API
    api = TdxHq_API()
    try:
        api.connect(TDX_HOST, TDX_PORT)
        kdata = api.get_security_bars(9, _tdx_market(code), code, 0, days)
        api.disconnect()
        result = []
        for row in kdata:
            result.append({
                "date": f"{row['year']:04d}-{row['month']:02d}-{row['day']:02d}",
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "close": row["close"],
                "vol": row["vol"],
                "amount": row["amount"],
            })
        return result
    except Exception as e:
        api.disconnect()
        return [{"error": str(e), "source": "tdx"}]


# ======================================================================
# 数据源 ②：东方财富新版API (datacenter)
# ======================================================================

def _source_east_available() -> bool:
    """检测东方财富API"""
    try:
        import requests
        r = requests.get("https://www.eastmoney.com", headers=EAST_HEADERS, timeout=5)
        _source_status["east"] = "✅" if r.status_code == 200 else "❌"
        return r.status_code == 200
    except Exception:
        _source_status["east"] = "❌"
        return False


def _east_fetch(report_name: str, columns: str, page_size: int = 500,
                page_num: int = 1, filter_str: str = None) -> List[Dict]:
    """东方财富 datacenter API"""
    import requests
    params = {
        "reportName": report_name,
        "columns": columns,
        "pageSize": page_size,
        "pageNumber": page_num,
        "source": "WEB",
        "client": "WEB",
    }
    if filter_str:
        params["filter"] = filter_str
    try:
        r = requests.get(EASTAPI_BASE, params=params, headers=EAST_HEADERS, timeout=15)
        data = r.json()
        if data.get("success") and data.get("result"):
            return data["result"].get("data", [])
    except Exception:
        pass
    return []


def east_get_all_boards() -> List[Dict]:
    """东方财富：全部板块"""
    all_b = []
    for page in range(1, 5):
        items = _east_fetch("RPT_BOARD_CONSTITUENT", "BOARD_CODE,BOARD_NAME",
                           page_size=500, page_num=page)
        all_b.extend(items)
        if len(items) < 500:
            break
    # 去重
    seen = set()
    uniq = []
    for item in all_b:
        key = item.get("BOARD_CODE", "")
        if key not in seen:
            seen.add(key)
            uniq.append(item)
    return uniq


def east_search_board(keyword: str) -> List[Dict]:
    """东方财富：搜索板块"""
    boards = east_get_all_boards()
    return [b for b in boards if keyword in b.get("BOARD_NAME", "")]


def east_get_board_stocks(board_code: str) -> List[Dict]:
    """东方财富：板块成分股"""
    return _east_fetch(
        "RPT_BOARD_CONSTITUENT",
        "BOARD_CODE,BOARD_NAME,SECURITY_CODE,SECUCODE",
        page_size=500, page_num=1,
        filter_str=f'(BOARD_CODE="{board_code}")',
    )


# ======================================================================
# 数据源 ③：同花顺 akshare (板块排行/行业数据/财务数据)
# ======================================================================

def _source_ths_available() -> bool:
    """检测同花顺数据源"""
    try:
        import akshare as ak
        _ = ak.stock_board_industry_name_ths()
        _source_status["ths"] = "✅"
        return True
    except Exception:
        _source_status["ths"] = "❌"
        return False


def ths_industry_summary(top_n: int = 20) -> List[Dict]:
    """同花顺：行业板块涨跌排行"""
    import akshare as ak
    import pandas as pd
    try:
        df = ak.stock_board_industry_summary_ths()
        df = df.sort_values("涨跌幅", ascending=False).head(top_n)
        result = []
        for _, r in df.iterrows():
            result.append({
                "name": r["板块"],
                "change_pct": float(r["涨跌幅"]),
                "up_count": int(r["上涨家数"]),
                "down_count": int(r["下跌家数"]),
                "net_inflow": float(r["净流入"]),
                "leader": str(r["领涨股"]),
                "leader_price": float(r["领涨股-最新价"]),
                "leader_change": float(r["领涨股-涨跌幅"]),
            })
        return result
    except Exception as e:
        return [{"error": str(e), "source": "ths"}]


def ths_industry_info(board_name: str) -> Dict:
    """同花顺：板块详情"""
    import akshare as ak
    try:
        df = ak.stock_board_industry_info_ths(symbol=board_name)
        result = {}
        for _, r in df.iterrows():
            result[r["项目"]] = r["值"]
        return result
    except Exception as e:
        return {"error": str(e)}


def ths_concept_summary(top_n: int = 20) -> List[Dict]:
    """同花顺：概念板块涨跌排行"""
    import akshare as ak
    try:
        df = ak.stock_board_concept_summary_ths()
        df = df.sort_values("板块涨幅", ascending=False).head(top_n)
        result = []
        for _, r in df.iterrows():
            result.append({
                "name": r["板块名称"],
                "change_pct": float(r["板块涨幅"]),
                "up_count": int(r["上涨数"]),
                "down_count": int(r["下跌数"]),
                "leader": str(r["领涨股"]),
            })
        return result
    except:
        return []


# ======================================================================
# 数据源 ④：akshare 通用 (财务/分红/IPO/排名等)
# ======================================================================

def _source_ak_available() -> bool:
    try:
        import akshare
        _source_status["akshare"] = "✅"
        return True
    except Exception:
        _source_status["akshare"] = "❌"
        return False


def ak_get_financial(code: str) -> Dict:
    """akshare：财务摘要"""
    import akshare as ak
    try:
        df = ak.stock_financial_abstract_ths(symbol=code)
        if df is not None and not df.empty:
            return df.to_dict(orient="records")[:5]
    except:
        pass
    return {}


def ak_get_profit_forecast(code: str) -> List[Dict]:
    """akshare：利润预测"""
    import akshare as ak
    try:
        df = ak.stock_profit_forecast_ths(symbol=code)
        if df is not None and not df.empty:
            return df.to_dict(orient="records")[:5]
    except:
        pass
    return []


# ======================================================================
# 统一接口
# ======================================================================

def _merge_quotes(sources: List[tuple]) -> Dict:
    """多源合并行情"""
    all_data = {}
    for name, func, codes in sources:
        try:
            data = func(codes)
            for d in data:
                if "error" not in d:
                    code = d.get("code", "")
                    if code:
                        d["_src"] = name
                        all_data.setdefault(code, {}).update(d)
        except Exception:
            pass
    return all_data


def get_realtime(codes: List[str]) -> Dict:
    """统一实时行情（主用pytdx, 降级akshare）"""
    result = {}

    # 主：通达信
    tdx_data = tdx_get_quotes(codes)
    for d in tdx_data:
        if "error" not in d:
            code = d.get("code", "")
            if code:
                d["_src"] = "通达信"
                result[code] = d

    return result


def get_kline(code: str, days: int = 30) -> List[Dict]:
    """统一K线（主用pytdx）"""
    return tdx_get_kline(code, days)


def get_sector_top(n: int = 20) -> Dict:
    """统一板块排行"""
    return {
        "industry": ths_industry_summary(n),
        "concept": ths_concept_summary(n),
    }


def get_sector_stocks(board_code: str, live: bool = False) -> Dict:
    """统一板块成分股"""
    stocks = east_get_board_stocks(board_code)
    if not stocks:
        return {"error": f"板块 {board_code} 无数据"}

    # 获取板块名称
    boards = east_get_all_boards()
    name = board_code
    for b in boards:
        if b["BOARD_CODE"] == board_code:
            name = b["BOARD_NAME"]
            break

    result = {
        "board_code": board_code,
        "board_name": name,
        "total": len(stocks),
        "stocks": [],
    }

    if live:
        codes = [s["SECURITY_CODE"] for s in stocks]
        prices = tdx_get_quotes(codes)
        price_map = {p["code"]: p for p in prices if "error" not in p}

        sorted_stocks = []
        for s in stocks:
            code = s["SECURITY_CODE"]
            p = price_map.get(code, {})
            chg = 0
            if p and p.get("last_close", 0) > 0:
                chg = (p["price"] - p["last_close"]) / p["last_close"] * 100
            sorted_stocks.append({
                "code": code,
                "secucode": s["SECUCODE"],
                "price": p.get("price", 0),
                "last_close": p.get("last_close", 0),
                "change_pct": round(chg, 2),
                "open": p.get("open", 0),
                "high": p.get("high", 0),
                "low": p.get("low", 0),
                "vol": p.get("vol", 0),
            })
        sorted_stocks.sort(key=lambda x: x["change_pct"], reverse=True)
        result["stocks"] = sorted_stocks
    else:
        for s in stocks[:100]:
            result["stocks"].append({
                "code": s["SECURITY_CODE"],
                "secucode": s["SECUCODE"],
            })

    return result


def search_sectors(keyword: str) -> List[Dict]:
    """统一搜索板块"""
    return east_search_board(keyword)


def get_financial(code: str) -> Dict:
    """统一财务数据"""
    return {
        "abstract": ak_get_financial(code),
        "forecast": ak_get_profit_forecast(code),
    }


def get_status() -> Dict:
    """全数据源状态检测"""
    _source_tdx_available()
    _source_east_available()
    _source_ths_available()
    _source_ak_available()
    return dict(_source_status)


# ======================================================================
# CLI
# ======================================================================

def _print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _print_table(rows, headers, fmt=None):
    if not rows:
        print("  (无数据)")
        return
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
    fmt_str = "  ".join(f"{{:<{w}}}" for w in col_widths)
    print(f"  " + fmt_str.format(*headers))
    print(f"  " + "-" * (sum(col_widths) + 2 * (len(headers) - 1)))
    for row in rows:
        print(f"  " + fmt_str.format(*row))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐂 UnifiedStock — 多源统一股票数据接口")
    parser.add_argument("--realtime", type=str, help="查询实时行情 (逗号分隔)")
    parser.add_argument("--kline", type=str, help="查询K线 (代码)")
    parser.add_argument("--days", type=int, default=10, help="K线天数")
    parser.add_argument("--sector-top", type=int, default=0, help="板块排行")
    parser.add_argument("--sector-stocks", type=str, help="板块成分股")
    parser.add_argument("--live", action="store_true", help="连带实时行情")
    parser.add_argument("--search", type=str, help="搜索板块")
    parser.add_argument("--financial", type=str, help="查财务数据")
    parser.add_argument("--status", action="store_true", help="数据源状态")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    args = parser.parse_args()

    if args.status:
        st = get_status()
        print(f"\n📡 数据源状态:")
        for src, status in st.items():
            print(f"  {status} {src}")

    elif args.realtime:
        codes = [c.strip() for c in args.realtime.split(",")]
        data = get_realtime(codes)
        if args.json:
            _print_json(data)
        else:
            print(f"\n📊 实时行情:")
            headers = ["代码", "最新价", "涨幅", "昨收", "开盘", "最高", "最低", "成交量", "来源"]
            rows = []
            for code, d in sorted(data.items()):
                chg = 0
                if d.get("last_close", 0) > 0:
                    chg = (d["price"] - d["last_close"]) / d["last_close"] * 100
                rows.append([
                    code,
                    f"¥{d['price']:.2f}",
                    f"{chg:+.2f}%",
                    f"¥{d['last_close']:.2f}",
                    f"¥{d['open']:.2f}",
                    f"¥{d['high']:.2f}",
                    f"¥{d['low']:.2f}",
                    f"{d['vol']}手",
                    d.get("_src", ""),
                ])
            _print_table(rows, headers)

    elif args.kline:
        kdata = get_kline(args.kline, args.days)
        if args.json:
            _print_json(kdata)
        elif "error" not in kdata[0] if kdata else True:
            print(f"\n📈 {args.kline} 日K线 (最近{args.days}天):")
            headers = ["日期", "开盘", "最高", "最低", "收盘", "成交量"]
            rows = []
            for row in kdata:
                rows.append([row["date"], f"¥{row['open']:.2f}", f"¥{row['high']:.2f}",
                            f"¥{row['low']:.2f}", f"¥{row['close']:.2f}", f"{row['vol']}手"])
            _print_table(rows, headers)
        else:
            print(f"  ❌ {kdata[0].get('error', '获取失败')}")

    elif args.sector_top:
        sectors = get_sector_top(args.sector_top)
        if args.json:
            _print_json(sectors)
        else:
            print(f"\n📊 行业板块 Top {args.sector_top}:")
            headers = ["板块", "涨幅", "上涨", "下跌", "净流入(亿)", "领涨股"]
            rows = []
            for s in sectors.get("industry", []):
                rows.append([s["name"], f"{s['change_pct']:+.2f}%",
                           str(s["up_count"]), str(s["down_count"]),
                           f"{s['net_inflow']:.1f}", s["leader"]])
            _print_table(rows, headers)

    elif args.sector_stocks:
        data = get_sector_stocks(args.sector_stocks, args.live)
        if args.json:
            _print_json(data)
        elif "error" in data:
            print(f"  ❌ {data['error']}")
        else:
            print(f"\n📦 {data['board_name']} ({data['board_code']}) — {data['total']} 只")
            if args.live:
                headers = ["代码", "最新价", "涨幅", "昨收", "开盘", "最高", "最低"]
                rows = []
                for s in data["stocks"][:30]:
                    rows.append([
                        s["code"],
                        f"¥{s['price']:.2f}" if s["price"] > 0 else "(盘前)",
                        f"{s['change_pct']:+.2f}%" if s["price"] > 0 else f"{s['change_pct']:+.2f}%",
                        f"¥{s['last_close']:.2f}",
                        f"¥{s['open']:.2f}",
                        f"¥{s['high']:.2f}",
                        f"¥{s['low']:.2f}",
                    ])
                _print_table(rows, headers)
            else:
                for s in data["stocks"][:50]:
                    print(f"    {s['code']:>6}  {s['secucode']}")

    elif args.search:
        results = search_sectors(args.search)
        print(f"\n🔍 搜索 \"{args.search}\": {len(results)} 个板块")
        for b in results:
            print(f"  {b['BOARD_CODE']:>5} - {b['BOARD_NAME']}")

    elif args.financial:
        data = get_financial(args.financial)
        if args.json:
            _print_json(data)
        else:
            print(f"\n📋 {args.financial} 财务数据:")
            if data.get("abstract"):
                print(f"  财务摘要:")
                for item in data["abstract"][:3]:
                    print(f"    {item}")
            if data.get("forecast"):
                print(f"  利润预测:")
                for item in data["forecast"][:3]:
                    print(f"    {item}")

    else:
        parser.print_help()
        print(f"\n例:")
        print(f"  python3 unified_stock.py --realtime 600839,002156,002475")
        print(f"  python3 unified_stock.py --kline 600839 --days 10")
        print(f"  python3 unified_stock.py --sector-top 15")
        print(f"  python3 unified_stock.py --sector-stocks 917 --live")
        print(f"  python3 unified_stock.py --search 半导体")
        print(f"  python3 unified_stock.py --status")


if __name__ == "__main__":
    main()
