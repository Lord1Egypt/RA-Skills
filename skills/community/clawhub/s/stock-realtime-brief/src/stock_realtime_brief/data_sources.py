"""
数据源策略 — 按可靠性降级:
  1. 腾讯财经（实时,最稳）
  2. 新浪财经批量（实时,多只）
  3. AKShare（历史K线,带超时）
  4. 腾讯日 K（历史备源）

踩过的坑: AKShare 主源 82.push2.eastmoney.com 在交易日早盘经常超时。
"""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timedelta
from typing import Any

# 配置
DEFAULT_TIMEOUT = 15
TENCENT_REALTIME_HOSTS = ["qt.gtimg.cn", "sqt.gtimg.cn"]
SINA_REALTIME_BASE = "https://hq.sinajs.cn/list="
TENCENT_HISTKLINE_BASE = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
USER_AGENT = "Mozilla/5.0 (compatible; StockRealtimeBrief/2.2)"


# ====== 实时行情：腾讯（首选） ======

def _tencent_code(code: str) -> str:
    """6 位代码转腾讯前缀: 60xx/68xx → sh, 其他 → sz"""
    if code.startswith(("60", "68", "90")):
        return "sh" + code
    return "sz" + code


def fetch_tencent_realtime(code: str) -> dict[str, Any] | None:
    """单只股票实时行情（腾讯）"""
    sym = _tencent_code(code)
    url = f"https://qt.gtimg.cn/q={sym}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": USER_AGENT,
            "Referer": "https://gu.qq.com/",
        })
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            txt = resp.read().decode("gbk", errors="replace")
        # 格式: v_sh600519="1~贵州茅台~600519~1380.00~1376.00~..."
        if "=" not in txt:
            return None
        parts = txt.split("=", 1)[1].strip(' ;\n"').split("~")
        if len(parts) < 35:
            return None
        return {
            "code": code,
            "name": parts[1],
            "price": float(parts[3]) if parts[3] else None,
            "prev_close": float(parts[4]) if parts[4] else None,
            "open": float(parts[5]) if parts[5] else None,
            "volume": float(parts[6]) * 100 if parts[6] else 0,  # 手→股
            "high": float(parts[33]) if parts[33] else None,
            "low": float(parts[34]) if parts[34] else None,
            "pct_change": float(parts[32]) if parts[32] else None,
            "amount": float(parts[37]) * 10000 if parts[37] else 0,  # 万元→元
            "turnover_rate": float(parts[38]) if len(parts) > 38 and parts[38] else None,
        }
    except Exception:
        return None


def fetch_sina_batch(codes: list[str]) -> dict[str, dict]:
    """新浪批量行情（一次请求拿多只）"""
    if not codes:
        return {}
    syms = [_tencent_code(c) for c in codes]
    url = SINA_REALTIME_BASE + ",".join(syms)
    out: dict[str, dict] = {}
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": USER_AGENT,
            "Referer": "https://finance.sina.com.cn/",
        })
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            txt = resp.read().decode("gbk", errors="replace")
        for line in txt.strip().split("\n"):
            if "=" not in line:
                continue
            head, body = line.split("=", 1)
            sym = head.split("_")[-1]  # var hq_str_sh600519 → sh600519
            code = sym[2:]  # 去前缀
            parts = body.strip(' ;\n"').split(",")
            if len(parts) < 32:
                continue
            try:
                out[code] = {
                    "code": code,
                    "name": parts[0],
                    "open": float(parts[1]) if parts[1] else None,
                    "prev_close": float(parts[2]) if parts[2] else None,
                    "price": float(parts[3]) if parts[3] else None,
                    "high": float(parts[4]) if parts[4] else None,
                    "low": float(parts[5]) if parts[5] else None,
                    "volume": float(parts[8]) if parts[8] else 0,
                    "amount": float(parts[9]) if parts[9] else 0,
                }
                # 算涨跌幅
                if out[code]["price"] and out[code]["prev_close"]:
                    out[code]["pct_change"] = round(
                        (out[code]["price"] - out[code]["prev_close"]) / out[code]["prev_close"] * 100, 2
                    )
            except (ValueError, IndexError):
                continue
    except Exception:
        pass
    return out


def fetch_realtime(codes: list[str]) -> dict[str, dict]:
    """统一入口：先腾讯逐个 + 新浪批量兜底"""
    out: dict[str, dict] = {}
    # 先尝试新浪批量（一次省时间）
    sina_data = fetch_sina_batch(codes)
    out.update(sina_data)
    # 缺的用腾讯补
    for c in codes:
        if c not in out or not out[c].get("price"):
            q = fetch_tencent_realtime(c)
            if q:
                out[c] = q
    return out


# ====== 历史 K 线：AKShare 主源 + 腾讯日 K 备源 ======

def fetch_hist_akshare(code: str, days_back: int = 120):
    """AKShare 历史 K 线（首选）"""
    try:
        import akshare as ak
        end = datetime.now().strftime("%Y%m%d")
        start = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")
        df = ak.stock_zh_a_hist(
            symbol=code, period="daily",
            start_date=start, end_date=end, adjust="qfq",
        )
        if df is not None and not df.empty:
            return df
    except Exception:
        pass
    return None


def fetch_hist_tencent(code: str, days_back: int = 120):
    """腾讯日 K 备源"""
    sym = _tencent_code(code)
    url = f"{TENCENT_HISTKLINE_BASE}?param={sym},day,,,90,qfq"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        kline = (
            data.get("data", {}).get(sym, {}).get("qfqday")
            or data.get("data", {}).get(sym, {}).get("day")
            or []
        )
        rows = []
        for r in kline:
            try:
                rows.append({
                    "日期": r[0],
                    "开盘": float(r[1]),
                    "收盘": float(r[2]),
                    "最高": float(r[3]),
                    "最低": float(r[4]),
                    "成交量": float(r[5]) if len(r) > 5 else 0,
                })
            except Exception:
                continue
        if rows:
            import pandas as pd
            return pd.DataFrame(rows)
    except Exception:
        pass
    return None


def fetch_hist_kline(code: str, days_back: int = 120, retry: int = 2):
    """统一历史 K 线入口：AKShare 重试 + 腾讯兜底"""
    df = None
    for _ in range(retry):
        df = fetch_hist_akshare(code, days_back)
        if df is not None and not df.empty:
            return df
    return fetch_hist_tencent(code, days_back)
