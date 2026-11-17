#!/usr/bin/env python3
"""
🐂 UnifiedStock — 多源统一股票数据接口 v3.0

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

import sys, os, json, time, hashlib, re
import urllib.request
import requests as _requests
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

# 新浪复用连接池（大幅加速批量日K/板块拉取）
_sina_session = _requests.Session()
_sina_session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://finance.sina.com.cn",
})

# 数据源状态缓存
_source_status = {}

# A股指数代码映射（查询时 000001→上证指数而非平安银行）
A_INDEX_MAP = {
    "000001": ("sh000001", "上证指数"),
    "399001": ("sz399001", "深证成指"),
    "399006": ("sz399006", "创业板指"),
    "000688": ("sh000688", "科创50"),
    "000300": ("sh000300", "沪深300"),
    "000016": ("sh000016", "上证50"),
    "000905": ("sh000905", "中证500"),
}


# ======================================================================
# 🔥 国际期货品种映射
# ======================================================================

SINA_FUTURES_MAP = {
    # 贵金属
    "GC": ("hf_GC", "COMEX黄金"),
    "SI": ("hf_SI", "COMEX白银"),
    "XAU": ("hf_XAU", "伦敦金(现货)"),
    "XAG": ("hf_XAG", "伦敦银(现货)"),
    # 能源
    "CL": ("hf_CL", "NYMEX原油"),
    "NG": ("hf_NG", "天然气"),
    # 金属
    "CAD": ("hf_CAD", "LME铜"),
    "AHD": ("hf_AHD", "LME铝"),
    "ZSD": ("hf_ZSD", "LME锌"),
    "NID": ("hf_NID", "LME镍"),
    "PBD": ("hf_PBD", "LME铅"),
    "SND": ("hf_SND", "LME锡"),
    # 农产品
    "C": ("hf_C", "CBOT玉米"),
    "S": ("hf_S", "CBOT大豆"),
    "W": ("hf_W", "CBOT小麦"),
    # 外汇
    "DINIW": ("hf_DINIW", "美元指数"),
}

SINA_FUTURES_REVERSE = {v[0]: k for k, v in SINA_FUTURES_MAP.items()}


# ======================================================================
# 工具函数
# ======================================================================

def _ts():
    return datetime.now().strftime("%H:%M:%S")


def _log(msg: str):
    print(f"  [{_ts()}] {msg}")


def _ensure_market_prefix(code: str) -> str:
    """股票/指数代码补市场前缀"""
    code = code.strip()
    # 指数代码：000001 → sh000001, 399001 → sz399001
    if code in A_INDEX_MAP:
        return A_INDEX_MAP[code][0]
    if code.startswith(('6', '9', '5')):
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
    elif code.startswith(('0', '2', '3', '1')):  # 1开头=深市ETF/基金
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


def sina_get_quotes(codes: List[str]) -> List[Dict]:
    """新浪财经：实时行情（支持股票+指数，标记未开盘状态）"""
    result = []
    code_list = [_ensure_market_prefix(c) for c in codes]
    
    for code, sina_code in zip(codes, code_list):
        try:
            url = f"{SINA_BASE}/list={sina_code}"
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Referer": "https://finance.sina.com.cn"
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read().decode('gbk')
            
            m = re.search(r'"([^"]*)"', data)
            if not m:
                result.append({"code": code, "error": "解析失败"})
                continue
            
            parts = m.group(1).split(',')
            if len(parts) < 6:
                result.append({"code": code, "error": "数据不完整"})
                continue
            
            name = parts[0]
            open_p = float(parts[1]) if parts[1] else 0
            last_close = float(parts[2]) if parts[2] else 0
            price = float(parts[3]) if parts[3] else 0
            high = float(parts[4]) if parts[4] else 0
            low = float(parts[5]) if parts[5] else 0
            volume = int(parts[8]) if len(parts) > 8 and parts[8] else 0
            amount = float(parts[9]) if len(parts) > 9 and parts[9] else 0
            
            change_pct = 0
            if last_close > 0 and price > 0:
                change_pct = round((price - last_close) / last_close * 100, 2)
            
            is_pre = (price == 0 and volume == 0)
            
            result.append({
                "code": code,
                "name": name,
                "price": price,
                "change_pct": change_pct,
                "open": open_p,
                "high": high,
                "low": low,
                "last_close": last_close,
                "vol": volume,
                "amount": amount,
                "is_pre_market": is_pre,
                "is_index": code in A_INDEX_MAP or "指数" in name,
            })
        except Exception as e:
            result.append({"code": code, "error": str(e)})
    
    return result


# ======================================================================
# 国际期货行情 (新浪财经)
# ======================================================================

def sina_get_futures(symbols: List[str]) -> List[Dict]:
    """新浪财经：国际期货实时行情
    
    Args:
        symbols: 品种代码列表，如 ["GC", "SI", "XAU", "CL"]
            可用: GC(COMEX黄金) SI(COMEX白银) XAU(伦敦金) XAG(伦敦银)
                  CL(原油) NG(天然气) CAD(LME铜) AHD(LME铝)
                  ZSD(LME锌) NID(LME镍) PBD(LME铅) SND(LME锡)
                  C(玉米) S(大豆) W(小麦) DINIW(美元指数)
    """
    result = []
    
    # 解析新浪代码
    sina_codes = []
    for sym in symbols:
        sym = sym.upper()
        if sym in SINA_FUTURES_MAP:
            sina_codes.append(SINA_FUTURES_MAP[sym][0])
        else:
            result.append({"symbol": sym, "error": f"未知品种: {sym}"})
    
    if not sina_codes:
        return result
    
    url = f"{SINA_BASE}/list={','.join(sina_codes)}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://finance.sina.com.cn"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode('gbk')
    except Exception as e:
        return [{"symbol": s, "error": str(e)} for s in symbols]
    
    for line in data.split(';'):
        if 'var hq_str_hf_' not in line:
            continue
        
        m = re.search(r'var hq_str_(\w+)="([^"]*)"', line)
        if not m:
            continue
        
        sina_code, content = m.groups()
        parts = content.split(',')
        
        if len(parts) < 12:
            continue
        
        # 新浪期货字段:
        # 0:最新价 1:昨收 2:买入 3:卖出 4:最高 5:最低 6:时间 7:卖价 8:买价 ...
        price = float(parts[0]) if parts[0] else 0
        prev_close = float(parts[1]) if parts[1] else 0
        bid = float(parts[2]) if parts[2] else 0
        ask = float(parts[3]) if parts[3] else 0
        high = float(parts[4]) if parts[4] else 0
        low = float(parts[5]) if parts[5] else 0
        time_str = parts[6] if parts[6] else ""
        
        change_pct = 0
        if prev_close > 0 and price > 0:
            change_pct = round((price - prev_close) / prev_close * 100, 2)
        
        symbol = SINA_FUTURES_REVERSE.get(sina_code, sina_code)
        name = SINA_FUTURES_MAP.get(symbol, ("", sina_code))[1]
        
        result.append({
            "symbol": symbol,
            "name": name,
            "price": price,
            "prev_close": prev_close,
            "change_pct": change_pct,
            "bid": bid,
            "ask": ask,
            "high": high,
            "low": low,
            "time": time_str,
            "source": "sina_futures",
        })
    
    return result


def ak_get_financial(code: str) -> Dict:
    """akshare：财务摘要（按报告期降序，取最新）"""
    import akshare as ak
    try:
        df = ak.stock_financial_abstract_ths(symbol=code)
        if df is not None and not df.empty:
            if "报告期" in df.columns:
                df = df.sort_values("报告期", ascending=False)
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
# ETF 数据（akshare）— 大王 2026-09-08 钦定整合
#   ETF历史行情：fund_etf_hist_em（东财）
#   ETF资金流：stock_individual_fund_flow（东财个股资金流，ETF适用）
# ======================================================================

def _etf_market(code: str) -> str:
    """ETF 市场前缀：5开头=上交所(sh)，1开头=深交所(sz)"""
    code = code.strip()
    if code.startswith('5'):
        return 'sh'
    return 'sz'


def get_etf_hist(code: str, days: int = 60) -> Dict:
    """ETF 历史日K — 主：通达信pytdx（稳定，不依赖HTTP代理）；降级：akshare东财"""
    raw = tdx_get_kline(code, days)
    if raw and len(raw) > 0 and "error" not in raw[0]:
        data = []
        prev_close = None
        for r in raw:
            chg = 0.0
            if prev_close and prev_close > 0:
                chg = (r["close"] - prev_close) / prev_close * 100
            data.append({
                "date": r["date"], "open": r["open"], "close": r["close"],
                "high": r["high"], "low": r["low"],
                "vol": r.get("vol", 0), "amount": r.get("amount", 0),
                "change_pct": round(chg, 2),
            })
            prev_close = r["close"]
        closes = [d["close"] for d in data if d["close"] > 0]
        ma5 = round(sum(closes[-5:]) / min(5, len(closes)), 3) if len(closes) >= 3 else None
        ma10 = round(sum(closes[-10:]) / min(10, len(closes)), 3) if len(closes) >= 7 else None
        ma20 = round(sum(closes[-20:]) / min(20, len(closes)), 3) if len(closes) >= 15 else None
        latest = closes[-1] if closes else 0
        prev = closes[-2] if len(closes) >= 2 else latest
        return {
            "code": code, "days": len(data), "data": data, "source": "pytdx",
            "ma": {"MA5": ma5, "MA10": ma10, "MA20": ma20},
            "latest": latest, "prev": prev,
            "change_1d": round((latest - prev) / prev * 100, 2) if prev > 0 else 0,
        }

    # 降级：akshare 东财
    import akshare as ak
    start = (datetime.now() - timedelta(days=days * 2 + 15)).strftime('%Y%m%d')
    end = datetime.now().strftime('%Y%m%d')
    try:
        df = ak.fund_etf_hist_em(symbol=code, period='daily',
                                 start_date=start, end_date=end, adjust='qfq')
        if df is None or df.empty:
            return {"code": code, "error": "无数据", "data": []}
        data = []
        for _, r in df.iterrows():
            data.append({
                "date": str(r['日期']),
                "open": float(r['开盘']), "close": float(r['收盘']),
                "high": float(r['最高']), "low": float(r['最低']),
                "vol": float(r['成交量']), "amount": float(r['成交额']),
                "change_pct": float(r['涨跌幅']) if r.get('涨跌幅') is not None else 0.0,
            })
        closes = [d["close"] for d in data if d["close"] > 0]
        ma5 = round(sum(closes[-5:]) / min(5, len(closes)), 3) if len(closes) >= 3 else None
        ma10 = round(sum(closes[-10:]) / min(10, len(closes)), 3) if len(closes) >= 7 else None
        ma20 = round(sum(closes[-20:]) / min(20, len(closes)), 3) if len(closes) >= 15 else None
        latest = closes[-1] if closes else 0
        prev = closes[-2] if len(closes) >= 2 else latest
        return {
            "code": code, "days": len(data), "data": data, "source": "akshare",
            "ma": {"MA5": ma5, "MA10": ma10, "MA20": ma20},
            "latest": latest, "prev": prev,
            "change_1d": round((latest - prev) / prev * 100, 2) if prev > 0 else 0,
        }
    except Exception as e:
        return {"code": code, "error": str(e), "data": []}


def get_etf_flow(code: str, days: int = 60) -> Dict:
    """ETF 资金流历史（akshare 东财个股资金流，ETF适用）"""
    import akshare as ak
    market = _etf_market(code)
    try:
        df = ak.stock_individual_fund_flow(stock=code, market=market)
        if df is None or df.empty:
            return {"code": code, "error": "无数据", "data": []}
        data = []
        for _, r in df.iterrows():
            data.append({
                "date": str(r['日期']),
                "close": float(r['收盘价']),
                "change_pct": float(r['涨跌幅']) if r.get('涨跌幅') is not None else 0.0,
                "main_net": float(r['主力净流入-净额']) if r.get('主力净流入-净额') is not None else 0.0,
                "super_net": float(r['超大单净流入-净额']) if r.get('超大单净流入-净额') is not None else 0.0,
                "big_net": float(r['大单净流入-净额']) if r.get('大单净流入-净额') is not None else 0.0,
                "mid_net": float(r['中单净流入-净额']) if r.get('中单净流入-净额') is not None else 0.0,
                "small_net": float(r['小单净流入-净额']) if r.get('小单净流入-净额') is not None else 0.0,
            })
        return {"code": code, "days": len(data), "data": data}
    except Exception as e:
        return {"code": code, "error": str(e), "data": []}


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


def tencent_get_quotes(codes: List[str]) -> List[Dict]:
    """腾讯财经：实时行情（备用源，ETF/指数支持好）"""
    result = []
    code_list = [_ensure_market_prefix(c) for c in codes]
    try:
        url = f"https://qt.gtimg.cn/q={','.join(code_list)}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode('gbk', errors='ignore')
        for code, sina_code in zip(codes, code_list):
            m = re.search(rf'v_{re.escape(sina_code)}="([^"]*)"', data)
            if not m:
                result.append({"code": code, "error": "解析失败"})
                continue
            parts = m.group(1).split('~')
            # 腾讯字段: 1名称 2代码 3现价 4昨收 5今开 6成交量(手) ...
            if len(parts) < 6:
                result.append({"code": code, "error": "数据不完整"})
                continue
            name = parts[1]
            price = float(parts[3]) if parts[3] else 0
            last_close = float(parts[4]) if parts[4] else 0
            open_p = float(parts[5]) if parts[5] else 0
            high = float(parts[33]) if len(parts) > 33 and parts[33] else 0
            low = float(parts[34]) if len(parts) > 34 and parts[34] else 0
            volume = int(float(parts[6]) * 100) if parts[6] else 0  # 手→股
            amount = float(parts[37]) if len(parts) > 37 and parts[37] else 0
            change_pct = 0
            if last_close > 0 and price > 0:
                change_pct = round((price - last_close) / last_close * 100, 2)
            is_pre = (price == 0 and volume == 0)
            result.append({
                "code": code,
                "name": name,
                "price": price,
                "change_pct": change_pct,
                "open": open_p,
                "high": high,
                "low": low,
                "last_close": last_close,
                "vol": volume,
                "amount": amount,
                "is_pre_market": is_pre,
                "is_index": code in A_INDEX_MAP or "指数" in name,
                "_src": "tencent",
            })
    except Exception as e:
        for code in codes:
            result.append({"code": code, "error": str(e)})
    return result


def get_realtime(codes: List[str]) -> Dict:
    """统一实时行情（新浪优先，通达信补充）
    
    支持：股票 + 指数（000001→上证指数）
    开盘前：显示昨收 + ⏰ 标记
    """
    result = {}
    all_codes = set(codes)

    # 主：新浪财经（快且稳定，支持指数）
    sina_data = sina_get_quotes(codes)
    for d in sina_data:
        if "error" not in d:
            code = d.get("code", "")
            d["_src"] = "sina"
            result[code] = d
        else:
            code = d.get("code", "")
            if code:
                result[code] = {"code": code, "error": d["error"], "_src": "sina"}

    # 补充：通达信（仅补充交易时段内的实时数据）
    if _source_tdx_available():
        tdx_data = tdx_get_quotes(codes)
        for d in tdx_data:
            if "error" not in d and d.get("price", 0) > 0:
                code = d.get("code", "")
                if code and code in result:
                    # 用通达信实时价更新新浪的盘前数据
                    result[code].update({"price": d["price"], "open": d.get("open", 0),
                                        "high": d.get("high", 0), "low": d.get("low", 0),
                                        "vol": d.get("vol", 0), "amount": d.get("amount", 0),
                                        "is_pre_market": False, "_src": "tdx"})
                elif code:
                    d["_src"] = "tdx"
                    d["is_pre_market"] = False
                    result[code] = d

    # 兜底：腾讯源（仅补新浪/通达信都失败或价格=0的标的）
    failed = [c for c in all_codes if c not in result or result[c].get("price", 0) <= 0]
    if failed:
        tx_data = tencent_get_quotes(failed)
        for d in tx_data:
            if "error" not in d and d.get("price", 0) > 0:
                code = d.get("code", "")
                if code and code in result:
                    result[code].update({"price": d["price"], "name": d.get("name", result[code].get("name", "")),
                                        "open": d.get("open", 0), "high": d.get("high", 0),
                                        "low": d.get("low", 0), "vol": d.get("vol", 0),
                                        "amount": d.get("amount", 0), "last_close": d.get("last_close", 0),
                                        "change_pct": d.get("change_pct", 0),
                                        "is_pre_market": False, "_src": "tencent"})
                elif code:
                    d["is_pre_market"] = False
                    result[code] = d

    return result


def get_kline(code: str, days: int = 30) -> Dict:
    """统一K线（pytdx 优先 → 新浪兜底），附带均线计算"""
    raw = tdx_get_kline(code, days)
    if not raw or (len(raw) == 1 and "error" in raw[0]):
        raw = sina_get_kline(code, days)  # 通达信挂了走新浪
    if not raw or (len(raw) == 1 and "error" in raw[0]):
        return {"error": raw[0].get("error", "获取失败") if raw else "无数据", "data": []}
    
    # 计算均线
    closes = [d["close"] for d in raw if d.get("close", 0) > 0]
    ma5 = round(sum(closes[-5:]) / min(5, len(closes)), 2) if len(closes) >= 3 else None
    ma10 = round(sum(closes[-10:]) / min(10, len(closes)), 2) if len(closes) >= 7 else None
    ma20 = round(sum(closes[-20:]) / min(20, len(closes)), 2) if len(closes) >= 15 else None
    ma60 = round(sum(closes) / len(closes), 2) if len(closes) >= 30 else None  # 近似
    
    latest = closes[-1] if closes else 0
    prev = closes[-2] if len(closes) >= 2 else latest
    
    return {
        "code": code,
        "days": days,
        "data": raw,
        "ma": {
            "MA5": ma5,
            "MA10": ma10,
            "MA20": ma20,
            "MA60": ma60,
        },
        "latest": latest,
        "prev": prev,
        "change_1d": round((latest - prev) / prev * 100, 2) if prev > 0 else 0,
        # 均线位置
        "above_ma5": round(latest, 2) > ma5 if ma5 else None,
        "above_ma10": round(latest, 2) > ma10 if ma10 else None,
        "above_ma20": round(latest, 2) > ma20 if ma20 else None,
    }


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


def sina_get_kline(code: str, days: int = 90) -> List[Dict]:
    """新浪财经：日K线（前复权），返回与 tdx_get_kline 同构的 list"""
    try:
        mkt = 'sh' if code.startswith(('6', '9', '5')) else 'sz'
        url = (f'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/'
               f'CN_MarketData.getKLineData?symbol={mkt}{code}&scale=240&ma=no&datalen={days}')
        data = _sina_session.get(url, timeout=8).json()
        result = []
        for x in data:
            result.append({
                "date": x["day"],
                "open": float(x["open"]),
                "high": float(x["high"]),
                "low": float(x["low"]),
                "close": float(x["close"]),
                "vol": float(x["volume"]),  # 股
                "amount": 0.0,
            })
        return result
    except Exception as e:
        return [{"error": str(e), "source": "sina"}]


def sina_get_sector_list(kind: str = 'hangye') -> List[Dict]:
    """新浪：板块列表。kind='hangye'=证监会84行业，kind='class'=概念板块（约175个）。
    含涨跌幅，按涨跌幅降序。"""
    param = 'class' if kind == 'class' else 'hangye'
    try:
        url = f'http://vip.stock.finance.sina.com.cn/q/view/newFLJK.php?param={param}'
        data = _sina_session.get(url, timeout=10).content.decode('gbk')
        m = re.search(r'=\s*(\{.*\})', data, re.S)
        obj = json.loads(m.group(1))
        result = []
        for key, val in obj.items():
            p = val.split(',')
            if len(p) < 6:
                continue
            try:
                result.append({
                    "node": p[0],
                    "name": p[1],
                    "count": int(p[2]) if p[2].isdigit() else 0,
                    "change_pct": float(p[5]) if p[5] else 0.0,
                })
            except (ValueError, IndexError):
                continue
        result.sort(key=lambda x: -x["change_pct"])
        return result
    except Exception as e:
        return [{"error": str(e), "source": "sina"}]


def sina_get_sector_stocks(node: str) -> List[Dict]:
    """新浪：板块成分股（node 如 hangye_ZA01），自动翻页取全"""
    all_stocks = []
    try:
        for page in range(1, 20):
            url = (f'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/'
                   f'Market_Center.getHQNodeData?page={page}&num=100&sort=symbol&asc=1'
                   f'&node={node}&symbol=&_s_r_a=page')
            data = _sina_session.get(url, timeout=10).json()
            if not data:
                break
            for x in data:
                all_stocks.append({
                    "code": str(x.get("code", "")),
                    "name": x.get("name", ""),
                    "change_pct": float(x.get("changepercent", 0) or 0),
                })
            if len(data) < 100:
                break
        return all_stocks
    except Exception as e:
        return all_stocks if all_stocks else [{"error": str(e), "source": "sina"}]


def get_sector_strength_map(kind: str = 'hangye') -> Dict:
    """板块强度映射：{股票代码: {sector, change_pct}}
    kind='hangye'=证监会84行业；kind='class'=概念板块。并发翻页拉全部成分股。"""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    sectors = sina_get_sector_list(kind)
    if not sectors or "error" in sectors[0]:
        return {"error": "板块列表获取失败", "map": {}, "sectors": []}

    code_map = {}
    members = {}   # 板块名 -> 成员代码列表（供轮动聚合用）
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(sina_get_sector_stocks, s["node"]): s for s in sectors}
        for f in as_completed(futs):
            s = futs[f]
            try:
                stocks = f.result()
            except Exception:
                continue
            if not stocks or "error" in stocks[0]:
                continue
            codes = []
            for st in stocks:
                c = st.get("code", "")
                if c and c not in code_map:
                    code_map[c] = {"sector": s["name"], "change_pct": s["change_pct"]}
                if c:
                    codes.append(c)
            members[s["name"]] = codes
    return {"error": None, "map": code_map, "members": members, "sectors": sectors}


def _parse_amt(s) -> float:
    """解析金额字符串 '1632.21万' / '2.02亿' -> float(元)"""
    if s is None:
        return 0.0
    s = str(s).strip()
    if not s:
        return 0.0
    try:
        if s.endswith('亿'):
            return float(s[:-1]) * 1e8
        if s.endswith('万'):
            return float(s[:-1]) * 1e4
        return float(s)
    except ValueError:
        return 0.0


def get_fund_flow_map() -> Dict:
    """同花顺：全市场个股资金净流入（即时）→ {股票代码: {net, amount}}"""
    import akshare as ak
    try:
        df = ak.stock_fund_flow_individual(symbol='即时')
        m = {}
        for _, row in df.iterrows():
            code = str(row['股票代码']).zfill(6)
            m[code] = {
                'net': _parse_amt(row['净额']),
                'amount': _parse_amt(row['成交额']),
            }
        return {'error': None, 'map': m}
    except Exception as e:
        return {'error': str(e), 'map': {}}


def get_status() -> Dict:
    """全数据源状态检测"""
    _source_tdx_available()
    _source_east_available()
    _source_ths_available()
    _source_ak_available()
    return dict(_source_status)


def get_futures(symbols: List[str]) -> List[Dict]:
    """统一获取国际期货行情"""
    return sina_get_futures(symbols)


# ======================================================================
# 🆕 ① 美股三大指数
# ======================================================================

# 新浪美股指数映射
_US_INDEX_MAP = {
    "DJI":  ("gb_dji",  "道琼斯"),
    "IXIC": ("gb_ixic", "纳斯达克"),
    "INX":  ("gb_inx",  "标普500"),
    "NDX":  ("gb_ndx",  "纳斯达克100"),
    "SOX":  ("gb_sox",  "费城半导体"),
}
_US_INDEX_REVERSE = {v[0]: k for k, v in _US_INDEX_MAP.items()}


def get_us_index(symbols: List[str] = None) -> Dict:
    """统一美股指数行情（新浪财经 → 降级akshare）
    
    Args:
        symbols: 指数代码列表，如 ["DJI", "IXIC", "INX"]
                默认返回三大指数
    Returns:
        {"DJI": {name, price, change_pct, ...}, ...}
    """
    if symbols is None:
        symbols = ["DJI", "IXIC", "INX"]
    
    result = {}
    sina_codes = []
    for sym in symbols:
        sym = sym.upper()
        if sym in _US_INDEX_MAP:
            sina_codes.append(_US_INDEX_MAP[sym][0])
        else:
            result[sym] = {"error": f"未知指数: {sym}"}
    
    if not sina_codes:
        return result
    
    url = f"{SINA_BASE}/list={','.join(sina_codes)}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://finance.sina.com.cn"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode('gbk')
    except Exception as e:
        # 降级：akshare
        return _ak_get_us_index(symbols)
    
    for line in data.split(';'):
        if 'var hq_str_gb_' not in line:
            continue
        m = re.search(r'var hq_str_(gb_\w+)="([^"]*)"', line)
        if not m:
            continue
        sina_code, content = m.groups()
        parts = content.split(',')
        if len(parts) < 3:
            continue
        
        symbol = _US_INDEX_REVERSE.get(sina_code, sina_code)
        name = _US_INDEX_MAP.get(symbol, ("", sina_code))[1]
        
        # 新浪美股字段: 0:名称 1:最新价 2:涨跌幅% 3:日期 4:涨跌额 ...
        price = float(parts[1]) if parts[1] else 0
        change_pct = float(parts[2]) if parts[2] else 0
        change_amount = float(parts[4]) if parts[4] else 0
        
        result[symbol] = {
            "symbol": symbol,
            "name": name,
            "price": price,
            "change_pct": round(change_pct, 2),
            "change_amount": round(change_amount, 2),
            "source": "sina",
        }
    
    # 没数据就降级
    if len(result) < len(symbols):
        return _ak_get_us_index(symbols)
    
    return result


def _ak_get_us_index(symbols: List[str]) -> Dict:
    """akshare 美股指数降级方案"""
    result = {}
    try:
        import akshare as ak
        df = ak.index_us_stock_sina()
        if df is not None and not df.empty:
            for _, row in df.iterrows():
                name = str(row.get("name", ""))
                price = float(row.get("current", 0))
                chg = float(row.get("change", 0))
                prev = price - chg if price and chg else 0
                chg_pct = round(chg / prev * 100, 2) if prev else 0
                
                mapped = None
                if "DJI" in symbols:
                    if "道琼斯" in name or "dji" in name.lower():
                        mapped = "DJI"
                if "IXIC" in symbols:
                    if "纳斯达克" in name or "nasdaq" in name.lower():
                        mapped = "IXIC"
                if "INX" in symbols:
                    if "标普" in name or "s&p" in name.lower():
                        mapped = "INX"
                
                if mapped:
                    result[mapped] = {
                        "symbol": mapped,
                        "name": name,
                        "price": price,
                        "change_pct": chg_pct,
                        "change_amount": chg,
                        "source": "akshare",
                    }
    except Exception:
        pass
    
    for sym in symbols:
        if sym not in result:
            result[sym] = {"symbol": sym, "error": "获取失败", "source": "all_failed"}
    
    return result


# ======================================================================
# 🆕 ② A股指数日K（近N天）
# ======================================================================

# A股主要指数代码
_A_INDEX_MAP = {
    "SH":    ("000001", "上证指数"),
    "SZ":    ("399001", "深证成指"),
    "CYB":   ("399006", "创业板指"),
    "KC50":  ("000688", "科创50"),
    "HS300": ("000300", "沪深300"),
    "ZZ500": ("000905", "中证500"),
    "SZ50":  ("000016", "上证50"),
}


def get_index_daily(codes: List[str] = None, days: int = 5) -> Dict:
    """A股指数近N天日K（主用akshare，降级pytdx），附带均线+趋势判断
    
    Args:
        codes: 指数简称，如 ["SH", "SZ", "CYB", "KC50"]
               默认四大指数
        days: 回溯天数，默认5天
    Returns:
        {"SH": {code, name, data:[...], ma:{}, trend: "...", ...}, ...}
    """
    if codes is None:
        codes = ["SH", "SZ", "CYB", "KC50"]
    
    result = {}
    for key in codes:
        if key not in _A_INDEX_MAP:
            result[key] = {"error": f"未知指数: {key}"}
            continue
        
        tdx_code, name = _A_INDEX_MAP[key]
        
        # 主：akshare（区分指数和个股，不会搞混）
        kline = _ak_get_index_daily(key, days)
        
        if "error" in kline and not kline.get("data"):
            # 降级：pytdx
            kline = get_kline(tdx_code, days=days)
        
        # 趋势判断
        trend = _judge_trend(kline)
        
        result[key] = {
            "key": key,
            "code": tdx_code,
            "name": name,
            **kline,
            "trend": trend,
        }
    
    return result
    
    return result


def _judge_trend(kline: Dict) -> Dict:
    """基于K线数据判断短期趋势"""
    data = kline.get("data", [])
    ma = kline.get("ma", {})
    latest = kline.get("latest", 0)
    
    if not data or len(data) < 3:
        return {"direction": "数据不足", "score": 0}
    
    closes = [d["close"] for d in data if d.get("close", 0) > 0]
    if len(closes) < 3:
        return {"direction": "数据不足", "score": 0}
    
    # 近3天涨跌
    three_day_chg = round((closes[-1] - closes[0]) / closes[0] * 100, 2) if closes[0] else 0
    
    # 均线排列判断
    ma5 = ma.get("MA5") or 0
    ma10 = ma.get("MA10") or 0
    ma20 = ma.get("MA20") or 0
    
    bullish = (latest > ma5 > ma10 > ma20) if (ma5 and ma10 and ma20) else False
    bearish = (latest < ma5 < ma10 < ma20) if (ma5 and ma10 and ma20) else False
    
    # 方向
    if bullish:
        direction = "多头排列 📈"
        score = 80
    elif bearish:
        direction = "空头排列 📉"
        score = 20
    elif latest > ma20 if ma20 else False:
        direction = "偏多震荡"
        score = 60
    elif latest < ma20 if ma20 else False:
        direction = "偏空震荡"
        score = 40
    else:
        direction = "横盘整理"
        score = 50
    
    return {
        "direction": direction,
        "score": score,
        "three_day_chg": three_day_chg,
        "bullish_alignment": bullish,
        "bearish_alignment": bearish,
    }


def _ak_get_index_daily(key: str, days: int) -> Dict:
    """akshare 指数日K降级方案"""
    try:
        import akshare as ak
        code, name = _A_INDEX_MAP[key]
        # 转换代码格式: 000001 → sh000001
        market = "sh" if code.startswith(("0", "6", "9")) else "sz"
        symbol = f"{market}{code}"
        df = ak.stock_zh_index_daily(symbol=symbol)
        if df is not None and not df.empty:
            df = df.tail(days)
            data = []
            for _, r in df.iterrows():
                data.append({
                    "date": str(r["date"])[:10] if "date" in df.columns else "",
                    "open": float(r["open"]),
                    "high": float(r["high"]),
                    "low": float(r["low"]),
                    "close": float(r["close"]),
                    "vol": int(r.get("volume", 0)),
                    "amount": float(r.get("amount", 0)),
                })
            closes = [d["close"] for d in data]
            ma5 = round(sum(closes[-5:]) / min(5, len(closes)), 2) if closes else None
            ma10 = round(sum(closes[-10:]) / min(10, len(closes)), 2) if len(closes) >= 7 else None
            ma20 = round(sum(closes[-20:]) / min(20, len(closes)), 2) if len(closes) >= 15 else None
            latest = closes[-1] if closes else 0
            prev = closes[-2] if len(closes) >= 2 else latest
            return {
                "code": code, "days": days, "data": data,
                "ma": {"MA5": ma5, "MA10": ma10, "MA20": ma20},
                "latest": latest, "prev": prev,
                "change_1d": round((latest - prev) / prev * 100, 2) if prev else 0,
                "above_ma5": latest > ma5 if ma5 else None,
                "above_ma10": latest > ma10 if ma10 else None,
                "above_ma20": latest > ma20 if ma20 else None,
                "source": "akshare",
            }
    except Exception:
        pass
    return {"error": "获取失败", "data": [], "source": "all_failed"}


# ======================================================================
# 🆕 ③ 市场宽度（涨跌家数 / 情绪指标）
# ======================================================================

def get_market_breadth() -> Dict:
    """统一市场宽度：涨跌家数、涨停跌停数、情绪判断（akshare → 东方财富降级）
    
    Returns:
        {
            up_count, down_count, flat_count, total,
            limit_up, limit_down,
            up_ratio, breadth_score, mood, ...
        }
    """
    try:
        import akshare as ak
        # 使用东财全市场行情
        df = ak.stock_zh_a_spot_em()
        if df is not None and not df.empty:
            up = int((df["涨跌幅"] > 0).sum())
            down = int((df["涨跌幅"] < 0).sum())
            flat = int((df["涨跌幅"] == 0).sum())
            total = len(df)
            up_ratio = round(up / total * 100, 1) if total else 0
            
            # 涨停≈涨幅>9.8%（排除ST）
            limit_up = int(((df["涨跌幅"] >= 9.8) & (~df["名称"].str.contains("ST", na=False))).sum())
            limit_down = int((df["涨跌幅"] <= -9.8).sum())
            
            # 情绪判断
            mood, mood_score = _judge_mood(up_ratio, limit_up, limit_down)
            
            return {
                "up_count": up,
                "down_count": down,
                "flat_count": flat,
                "total": total,
                "up_ratio": up_ratio,
                "limit_up": limit_up,
                "limit_down": limit_down,
                "mood": mood,
                "mood_score": mood_score,
                "source": "akshare_em",
            }
    except Exception:
        pass
    
    # 降级：东方财富API
    return _east_get_market_breadth()


def _judge_mood(up_ratio: float, limit_up: int, limit_down: int) -> tuple:
    """判断市场情绪"""
    if up_ratio >= 70 and limit_up >= 200:
        return ("极度亢奋 🔥🔥🔥", 95)
    elif up_ratio >= 60:
        return ("乐观偏强 🟢", 75)
    elif up_ratio >= 45:
        return ("中性偏多 🟡", 55)
    elif up_ratio >= 30:
        return ("中性偏弱 🟠", 40)
    elif up_ratio >= 20:
        return ("悲观走弱 🔴", 25)
    elif up_ratio >= 10:
        return ("极度恐慌 🚨", 10)
    else:
        return ("股灾级别 💀", 5)


def _east_get_market_breadth() -> Dict:
    """东方财富市场宽度降级"""
    try:
        import requests
        url = "https://push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1", "pz": "1", "po": "0", "np": "1",
            "fltt": "2", "invt": "2",
            "fid": "f3", "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
            "fields": "f104,f105",
        }
        r = requests.get(url, params=params, headers=EAST_HEADERS, timeout=10)
        data = r.json()
        if data.get("data"):
            total = data["data"].get("total", 0)
            # 涨跌需要分批获取，简化处理
            return {
                "up_count": 0, "down_count": 0, "flat_count": 0,
                "total": total, "up_ratio": 0,
                "limit_up": 0, "limit_down": 0,
                "mood": "降级模式(数据不完整)",
                "mood_score": 50,
                "source": "east_money",
            }
    except Exception:
        pass
    return {"error": "所有数据源失败", "source": "all_failed"}


# ======================================================================
# 🆕 ④ 北向资金流
# ======================================================================

def get_north_flow(days: int = 5) -> Dict:
    """统一北向资金流（多源兜底：东财KAMT → akshare摘要 → 优雅降级）
    
    Args:
        days: 回溯天数，默认5天
    Returns:
        {summary: {net_inflow, trend, direction}, daily: [...], ...}
    """
    import requests
    
    # 方案1: 东财KAMT API
    try:
        url = 'https://push2his.eastmoney.com/api/qt/kamt.kline/get'
        base_params = {
            'fields1': 'f1,f2,f3,f4',
            'fields2': 'f51,f52,f53,f54,f55,f56',
            'klt': '101', 'lmt': days + 2,
            'ut': 'b2884a393a59ad64002292a3e90d46a5',
        }
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://data.eastmoney.com/hsgt/index.html'}
        
        all_rows = []
        for secid in ['1.0001', '1.0003']:  # 北向沪 + 北向深
            params = {**base_params, 'secid': secid}
            r = requests.get(url, params=params, headers=headers, timeout=10)
            m = re.search(r'\((.*)\)', r.text, re.DOTALL)
            if m:
                d = json.loads(m.group(1))
                for key in ['hk2sh', 'hk2sz']:
                    rows = d.get('data', {}).get(key, [])
                    all_rows.extend(rows)
        
        if all_rows:
            daily = []
            total = 0
            for row in all_rows[-days:]:
                parts = row.split(',')
                if len(parts) >= 3 and parts[1]:
                    net = float(parts[1]) / 10000  # 万元→亿元
                    daily.append({"date": parts[0], "net_inflow": round(net, 2)})
                    total += net
            if daily:
                up_days = sum(1 for d in daily if d["net_inflow"] > 0)
                if up_days >= days * 0.8:
                    direction, score = "持续流入 ✅", 80
                elif up_days >= days * 0.5:
                    direction, score = "波动流入 🟡", 60
                elif up_days >= days * 0.3:
                    direction, score = "偏流出 🟠", 40
                else:
                    direction, score = "持续流出 🔴", 20
                return {
                    "summary": {"total_net_inflow": round(total, 2), "units": "亿元",
                               "up_days": up_days, "total_days": len(daily),
                               "direction": direction, "score": score,
                               "avg_daily": round(total / len(daily), 2)},
                    "daily": daily, "source": "eastmoney_kamt"
                }
    except Exception:
        pass
    
    # 方案2: akshare 当日摘要
    try:
        import akshare as ak
        df = ak.stock_hsgt_fund_flow_summary_em()
        if df is not None and not df.empty:
            north = df[df['资金方向'] == '北向']
            if not north.empty:
                net_val = float(north.iloc[0].get('成交净买额', 0))
                return {
                    "summary": {"total_net_inflow": net_val, "units": "亿元",
                               "up_days": 1 if net_val > 0 else 0, "total_days": 1,
                               "direction": "▲今日流入" if net_val > 0 else "▼今日流出",
                               "score": 60 if net_val > 0 else 40,
                               "avg_daily": net_val},
                    "daily": [{"date": "今日", "net_inflow": net_val}],
                    "source": "akshare_summary"
                }
    except Exception:
        pass
    
    return {"error": "数据源未就绪(非交易时段?)", "source": "unavailable",
            "summary": {"total_net_inflow": 0, "direction": "数据暂不可用 ⏳", "score": 0},
            "daily": []}


def _east_get_north_flow(days: int) -> Dict:
    """(已废弃，保留兼容)"""
    return get_north_flow(days)


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
    parser = argparse.ArgumentParser(description="🐂 UnifiedStock — 多源统一股票数据接口 v3.0")
    parser.add_argument("--realtime", type=str, help="查询实时行情 (逗号分隔)")
    parser.add_argument("--kline", type=str, help="查询K线 (代码)")
    parser.add_argument("--days", type=int, default=10, help="K线天数")
    parser.add_argument("--sector-top", type=int, default=0, help="板块排行 Top N")
    parser.add_argument("--sector-type", type=str, default="both",
                       choices=["industry", "concept", "both"],
                       help="板块类型: industry/concept/both")
    parser.add_argument("--sector-stocks", type=str, help="板块成分股")
    parser.add_argument("--live", action="store_true", help="连带实时行情")
    parser.add_argument("--search", type=str, help="搜索板块")
    parser.add_argument("--financial", type=str, help="查财务数据")
    parser.add_argument("--futures", type=str, help="国际期货行情 (逗号分隔, 如: GC,SI,XAU,CL)")
    parser.add_argument("--us-index", type=str, help="美股指数 (逗号分隔, 如: DJI,IXIC,INX)")
    parser.add_argument("--index-daily", type=str, help="A股指数近N天日K (逗号分隔, 如: SH,SZ,CYB,KC50)")
    parser.add_argument("--breadth", action="store_true", help="市场宽度(涨跌家数/情绪)")
    parser.add_argument("--north-flow", type=int, default=0, help="北向资金流(回溯天数)")
    parser.add_argument("--etf-hist", type=str, help="ETF历史K线 (代码, 如: 512480)")
    parser.add_argument("--etf-flow", type=str, help="ETF资金流 (代码, 如: 512480)")
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
            # 分股票和指数显示
            stocks = []
            indices = []
            for code, d in sorted(data.items()):
                if "error" in d:
                    print(f"  ❌ {code}: {d['error']}")
                    continue
                if d.get("is_index"):
                    indices.append((code, d))
                else:
                    stocks.append((code, d))
            
            # 指数
            if indices:
                print(f"  📈 指数:")
                for code, d in indices:
                    is_pre = d.get("is_pre_market", False)
                    if is_pre:
                        print(f"    {code} {d.get('name', d.get('name',''))} ⏰ 未开盘 | 昨收: {d['last_close']:.2f}")
                    else:
                        chg = d.get("change_pct", 0)
                        print(f"    {code} {d.get('name',code)}  {d['price']:.2f}  ({chg:+.2f}%)  [{d.get('_src','')}]")
            
            # 个股
            if stocks:
                headers = ["代码", "名称", "最新价", "涨幅", "昨收", "量(手)", "状态", "源"]
                rows = []
                for code, d in stocks:
                    is_pre = d.get("is_pre_market", False)
                    if is_pre:
                        rows.append([
                            code, d.get("name", d.get("name",""))[:6],
                            "—", "—",
                            f"¥{d['last_close']:.2f}", "—",
                            "⏰ 未开盘", d.get("_src", ""),
                        ])
                    else:
                        chg = d.get("change_pct", 0)
                        rows.append([
                            code, d.get("name", d.get("name",""))[:6],
                            f"¥{d['price']:.2f}", f"{chg:+.2f}%",
                            f"¥{d['last_close']:.2f}",
                            f"{d.get('vol',0)}手",
                            "🟢" if chg >= 0 else "🔴",
                            d.get("_src", ""),
                        ])
                _print_table(rows, headers)

    elif args.kline:
        kdata = get_kline(args.kline, args.days)
        if args.json:
            _print_json(kdata)
        elif "error" in kdata:
            print(f"  ❌ {kdata['error']}")
        else:
            code = kdata["code"]
            ma = kdata["ma"]
            data_rows = kdata["data"]
            
            # 均线摘要
            print(f"\n📈 {code} 日K线 (最近{len(data_rows)}天)")
            print(f"  📊 均线:")
            for k, v in ma.items():
                if v:
                    above = kdata.get(f"above_{k.lower()}")
                    tag = "✅ 站上" if above else ("❌ 跌破" if above is False else "")
                    print(f"    {k}: ¥{v:.2f}  {tag}")
            
            # K线表
            headers = ["日期", "开盘", "最高", "最低", "收盘", "涨幅", "成交量"]
            rows = []
            for i, row in enumerate(data_rows):
                prev_close = data_rows[i-1]["close"] if i > 0 else row["close"]
                chg = round((row["close"] - prev_close) / prev_close * 100, 2) if prev_close > 0 else 0
                rows.append([
                    row["date"],
                    f"¥{row['open']:.2f}", f"¥{row['high']:.2f}",
                    f"¥{row['low']:.2f}", f"¥{row['close']:.2f}",
                    f"{chg:+.2f}%", f"{row['vol']}手"
                ])
            _print_table(rows, headers)

    elif args.sector_top:
        stype = args.sector_type
        sectors = get_sector_top(args.sector_top)
        if args.json:
            _print_json(sectors)
        else:
            if stype in ("both", "industry"):
                ind = sectors.get("industry", [])
                print(f"\n📊 行业板块 Top {len(ind)}:")
                headers = ["板块", "涨幅", "上涨", "下跌", "净流入(亿)", "领涨股"]
                rows = []
                for s in ind:
                    rows.append([s["name"], f"{s['change_pct']:+.2f}%",
                               str(s["up_count"]), str(s["down_count"]),
                               f"{s['net_inflow']:.1f}", s["leader"]])
                _print_table(rows, headers)
            if stype in ("both", "concept"):
                con = sectors.get("concept", [])
                print(f"\n📊 概念板块 Top {len(con)}:")
                headers = ["板块", "涨幅", "上涨", "下跌", "领涨股"]
                rows = []
                for s in con:
                    rows.append([s["name"], f"{s['change_pct']:+.2f}%",
                               str(s["up_count"]), str(s["down_count"]), s["leader"]])
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

    elif args.etf_hist:
        data = get_etf_hist(args.etf_hist, args.days)
        if args.json:
            _print_json(data)
        elif "error" in data:
            print(f"  ❌ {data['error']}")
        else:
            ma = data.get("ma", {})
            print(f"\n📦 ETF {data['code']} 日K (最近{data.get('days',0)}天)")
            print(f"  现价: ¥{data['latest']:.3f} | 近1日 {data.get('change_1d',0):+.2f}%")
            print(f"  均线: " + "  ".join(f"{k}=¥{v}" for k, v in ma.items() if v))
            rows = []
            for d in data["data"][-args.days:]:
                rows.append([d["date"], f"{d['open']:.3f}", f"{d['close']:.3f}",
                             f"{d['high']:.3f}", f"{d['low']:.3f}", f"{d['change_pct']:+.2f}%",
                             f"{d['amount']/1e8:.2f}亿"])
            _print_table(rows, ["日期", "开", "收", "高", "低", "涨跌", "成交额"])

    elif args.etf_flow:
        data = get_etf_flow(args.etf_flow, args.days)
        if args.json:
            _print_json(data)
        elif "error" in data:
            print(f"  ❌ {data['error']}")
        else:
            print(f"\n💰 ETF {data['code']} 资金流 (最近{data.get('days',0)}天)")
            rows = []
            for d in data["data"][-args.days:]:
                rows.append([d["date"], f"{d['close']:.3f}", f"{d['change_pct']:+.2f}%",
                             f"{d['main_net']/1e8:+.2f}亿", f"{d['super_net']/1e8:+.2f}亿",
                             f"{d['big_net']/1e8:+.2f}亿", f"{d['small_net']/1e8:+.2f}亿"])
            _print_table(rows, ["日期", "收盘", "涨跌", "主力净流入", "超大单", "大单", "小单"])

    elif args.us_index:
        symbols = [s.strip().upper() for s in args.us_index.split(",")]
        data = get_us_index(symbols)
        if args.json:
            _print_json(data)
        else:
            print(f"\n🇺🇸 美股指数:")
            headers = ["指数", "代码", "最新价", "涨跌", "来源"]
            rows = []
            for key, info in data.items():
                if "error" in info:
                    print(f"  ⚠️ {key}: {info['error']}")
                    continue
                rows.append([
                    info.get("name", key),
                    info["symbol"],
                    f"{info['price']:,.2f}",
                    f"{info['change_pct']:+.2f}%",
                    info.get("source", ""),
                ])
            _print_table(rows, headers)
            print(f"\n  📋 可用指数: DJI(道琼斯) IXIC(纳斯达克) INX(标普500) NDX(纳指100) SOX(费城半导体)")

    elif args.index_daily:
        codes = [c.strip().upper() for c in args.index_daily.split(",")]
        data = get_index_daily(codes, days=args.days)
        if args.json:
            _print_json(data)
        else:
            for key, info in data.items():
                if "error" in info:
                    print(f"  ⚠️ {key}: {info['error']}")
                    continue
                trend = info.get("trend", {})
                print(f"\n📈 {info['name']} ({info['code']}) — 近{args.days}天")
                print(f"  趋势: {trend.get('direction', 'N/A')} | 评分: {trend.get('score', 'N/A')}")
                print(f"  3日涨跌: {trend.get('three_day_chg', 0):+.2f}%")
                print(f"  均线: MA5=¥{info['ma'].get('MA5','N/A')} MA10=¥{info['ma'].get('MA10','N/A')} MA20=¥{info['ma'].get('MA20','N/A')}")
                headers = ["日期", "开盘", "收盘", "最高", "最低", "成交量"]
                rows = []
                for d in info.get("data", [])[-args.days:]:
                    rows.append([
                        d["date"], f"¥{d['open']:.2f}", f"¥{d['close']:.2f}",
                        f"¥{d['high']:.2f}", f"¥{d['low']:.2f}", f"{d.get('vol',0)}手"
                    ])
                _print_table(rows, headers)

    elif args.breadth:
        data = get_market_breadth()
        if args.json:
            _print_json(data)
        elif "error" in data:
            print(f"  ❌ {data['error']}")
        else:
            print(f"\n📊 市场宽度 ({data.get('source','')}):")
            print(f"  上涨: {data['up_count']} | 下跌: {data['down_count']} | 平盘: {data['flat_count']}")
            print(f"  上涨比例: {data['up_ratio']}% | 涨停: {data['limit_up']} | 跌停: {data['limit_down']}")
            print(f"  情绪: {data['mood']} (评分: {data['mood_score']})")

    elif args.north_flow > 0:
        data = get_north_flow(days=args.north_flow)
        if args.json:
            _print_json(data)
        elif "error" in data:
            print(f"  ❌ {data['error']}")
        else:
            s = data["summary"]
            print(f"\n💰 北向资金 ({data.get('source','')}) — 近{args.north_flow}天:")
            print(f"  累计净流入: {s['total_net_inflow']:.2f} 亿元")
            print(f"  日均: {s['avg_daily']:.2f} 亿元 | 趋势: {s['direction']}")
            headers = ["日期", "净流入(亿元)", "方向"]
            rows = []
            for d in data["daily"]:
                rows.append([d["date"], f"{d['net_inflow']:+.2f}", "🟢流入" if d['net_inflow'] > 0 else "🔴流出"])
            _print_table(rows, headers)

    elif args.futures:
        symbols = [s.strip() for s in args.futures.split(",")]
        data = get_futures(symbols)
        if args.json:
            _print_json(data)
        else:
            print(f"\n🥇 国际期货行情:")
            headers = ["品种", "代码", "最新价", "涨跌", "最高", "最低", "时间"]
            rows = []
            for f in data:
                if "error" in f:
                    print(f"  ⚠️ {f['symbol']}: {f['error']}")
                    continue
                currency = "$" if f["symbol"] != "DINIW" else ""
                rows.append([
                    f["name"],
                    f["symbol"],
                    f"{currency}{f['price']:.2f}",
                    f"{f['change_pct']:+.2f}%",
                    f"{f['high']:.2f}",
                    f"{f['low']:.2f}",
                    f["time"],
                ])
            _print_table(rows, headers)
            print(f"\n  📋 可用品种: GC(黄金) SI(白银) XAU(伦敦金) CL(原油) NG(天然气)")
            print(f"             CAD(铜) AHD(铝)  C(玉米) S(大豆) DINIW(美元指数)")

    else:
        parser.print_help()
        print(f"\n例:")
        print(f"  python3 unified_stock.py --realtime 600839,002156,002475")
        print(f"  python3 unified_stock.py --kline 600839 --days 10")
        print(f"  python3 unified_stock.py --futures GC,SI,XAU")
        print(f"  python3 unified_stock.py --sector-top 15 --sector-type concept")
        print(f"  python3 unified_stock.py --sector-stocks 917 --live")
        print(f"  python3 unified_stock.py --search 黄金")
        print(f"  python3 unified_stock.py --status")


if __name__ == "__main__":
    main()
