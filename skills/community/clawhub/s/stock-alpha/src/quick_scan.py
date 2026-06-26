"""全市场快速扫描器

Phase 1 (Quick):  Sina批量实时行情 → 按价格/成交量过滤
Phase 2 (Deep):   Ashare 60日行情 → 三维评分

Sina 批量 API 每次支持 ~50 只股票，5000只约需100次请求
"""

import logging
import time
from datetime import date
from typing import List, Tuple

import pandas as pd
import numpy as np
import requests

logger = logging.getLogger(__name__)


def get_a_share_list() -> List[Tuple[str, str]]:
    """获取全量A股列表（带缓存）"""
    import os
    from src.stock_list_builder import build_stock_list
    cache = os.path.join(os.path.dirname(__file__), "..", ".stock_cache.json")
    return build_stock_list(save_path=cache)


def _code_to_sina(code: str) -> str:
    prefix = code[:3]
    return f"sh{code}" if prefix in ("600","601","603","605","688","689") else f"sz{code}"


def quick_scan(min_price: float = 3.0, min_volume: float = 5e5) -> pd.DataFrame:
    """
    Phase 1: Sina 批量 API 全市场快照

    批量50只并发请求，只取最新一笔报价
    """
    print("[DATA] 获取全量A股列表...", flush=True)
    all_stocks = get_a_share_list()
    n = len(all_stocks)
    print(f"[OK] A股总数: {n}", flush=True)

    # 分批请求 Sina 实时行情
    batch_size = 50
    all_quotes = []
    t0 = time.time()

    for i in range(0, n, batch_size):
        batch = all_stocks[i:i + batch_size]
        sina_codes = ",".join(_code_to_sina(c) for c, _ in batch)

        try:
            headers = {"Referer": "http://finance.sina.com.cn"}
            resp = requests.get(f"http://hq.sinajs.cn/list={sina_codes}", 
                               headers=headers, timeout=10)
            resp.encoding = "gbk"

            for line in resp.text.strip().split("\n"):
                if "hq_str_" not in line:
                    continue
                parts = line.split('="')
                if len(parts) < 2:
                    continue
                data_str = parts[1].rstrip('";')
                fields = data_str.split(",")
                if len(fields) < 32:
                    continue

                var_name = parts[0].replace("var hq_str_", "").strip()
                code = var_name.replace("sh", "").replace("sz", "")
                name = fields[0]

                try:
                    close = float(fields[3]) if fields[3] else 0
                    pre_close = float(fields[2]) if fields[2] else 0
                    high = float(fields[4]) if fields[4] else 0
                    low = float(fields[5]) if fields[5] else 0
                    volume = float(fields[8]) if fields[8] else 0
                    change_pct = ((close - pre_close) / pre_close * 100) if pre_close > 0 else 0
                except (ValueError, IndexError):
                    continue

                if close > 0:
                    all_quotes.append({
                        "code": code,
                        "name": name,
                        "close": close,
                        "pre_close": pre_close,
                        "high": high,
                        "low": low,
                        "volume": volume,
                        "change_pct": change_pct,
                    })
        except Exception as e:
            logger.warning(f"[Scan] Sina batch {i//batch_size} failed: {e}")

        if (i // batch_size + 1) % 10 == 0:
            elapsed = time.time() - t0
            print(f"  >> 进度: {min(i+batch_size, n)}/{n} ({elapsed:.0f}s)", flush=True)

    if not all_quotes:
        print("[FAIL] 无可用实时数据")
        return pd.DataFrame()

    df = pd.DataFrame(all_quotes)
    elapsed = time.time() - t0
    print(f"[OK] 实时行情获取完成: {len(df)} 只股票 ({elapsed:.0f}s)", flush=True)

    # 过滤
    df = df[(df["close"] >= min_price) & (df["volume"] >= min_volume)]
    print(f"[OK] 过滤后: {len(df)} 只 (价格>={min_price}, 成交量>={min_volume/1e4:.0f}万手)", flush=True)

    # 简化评分: 超跌反弹 + 波幅
    df["score_quick"] = (
        np.clip(-df["change_pct"] / 5, 0, 1) * 0.5 +  # 跌幅越深分越高
        np.clip((df["high"] - df["low"]) / df["close"] * 5, 0, 1) * 0.5  # 波幅越宽分越高
    )

    result = df.sort_values("score_quick", ascending=False)
    print(f"[OK] 快速评分完成, Top3: {result.head(3)['code'].tolist()}")
    return result
