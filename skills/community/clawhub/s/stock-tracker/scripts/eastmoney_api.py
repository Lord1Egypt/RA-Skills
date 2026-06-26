#!/usr/bin/env python3
"""东方财富数据抓取模块 - 自选股列表 & 公告获取

自选股获取优先级:
  1. myfavor API (lite.html 使用的自选股接口)
  2. 从 Cookie 中解析 selfSelectStocks 字段
  3. 从 config.json 手动指定列表
"""

import json
import logging
import os
import re
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import Optional

import requests

logger = logging.getLogger(__name__)

ANNOUNCE_API = "https://np-anotice-stock.eastmoney.com/api/security/ann"
MYFAVOR_API = "https://myfavor.eastmoney.com/v4/webouter"
MYFAVOR_APPKEY = "e9166c7e9cdfad3aa3fd7d93b757e9b1"

# myfavor market code -> 显示标签
MARKET_LABEL_MAP = {
    "0": "SZ", "1": "SH", "100": "US", "104": "FUT",
    "116": "HK", "119": "FX", "124": "HKI", "134": "HKF",
    "251": "OTHER",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://quote.eastmoney.com/zixuan/lite.html",
}


def load_cookie(path: str = "cookie.txt") -> Optional[str]:
    if not os.path.exists(path):
        logger.warning("Cookie 文件不存在: %s", path)
        return None
    with open(path, "r") as f:
        cookie = f.read().strip()
    return cookie if cookie else None


def market_label(market: str) -> str:
    return MARKET_LABEL_MAP.get(market, market)


def make_stock_entry(code: str, market: str, name: Optional[str] = None) -> dict:
    return {
        "code": code,
        "market": market,
        "market_label": market_label(market),
        "symbol": f"{market_label(market)}{code}",
        "name": name,
    }


def parse_selfselect_from_cookie(cookie: str) -> list[dict]:
    decoded = urllib.parse.unquote(cookie)
    combined = cookie + ";" + decoded
    match = re.search(r"selfSelectStocks=([^;]+)", combined)
    if not match:
        logger.warning("Cookie 中未找到 selfSelectStocks 字段")
        return []

    entries = re.findall(r"\((\d+),(\d)\)", match.group(1))
    stocks = [make_stock_entry(code, market) for code, market in entries]
    logger.info("从 Cookie 解析到 %d 只自选股", len(stocks))
    return stocks


def get_groups(cookie: str) -> list[dict]:
    """获取自选股分组列表"""
    headers = HEADERS.copy()
    headers["Cookie"] = cookie
    try:
        r = requests.get(
            MYFAVOR_API + "/ggdefstkindexinfos",
            params={"appkey": MYFAVOR_APPKEY},
            headers=headers, timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("data", {}).get("ginfolist", [])
    except (requests.RequestException, json.JSONDecodeError) as e:
        logger.warning("myfavor 分组列表获取失败: %s", e)
        return []


def fetch_stocks_from_myfavor(cookie: str, group_name: Optional[str] = None) -> list[dict]:
    """通过 myfavor API 获取自选股列表.

    group_name: 可选，只获取指定分组的股票（模糊匹配）
    """
    headers = HEADERS.copy()
    headers["Cookie"] = cookie

    # 获取分组列表
    groups = get_groups(cookie)
    if not groups:
        return []

    # 如果指定了分组名，进行过滤
    if group_name:
        matched = [g for g in groups if group_name in str(g.get("gname", ""))]
        if not matched:
            logger.warning("未匹配到分组: %s，可用分组: %s",
                           group_name, [g.get("gname") for g in groups])
            return []
        groups = matched
        logger.info("myfavor API: 匹配到分组 %s", [g.get("gname") for g in groups])
    else:
        logger.info("myfavor API: 获取到 %d 个分组", len(groups))

    # 遍历分组获取股票
    all_stocks = []
    seen = set()
    for group in groups:
        gid = group.get("gid", "")
        gname = group.get("gname", gid)
        try:
            r2 = requests.get(
                MYFAVOR_API + "/gstkinfos",
                params={"appkey": MYFAVOR_APPKEY, "g": gid},
                headers=headers, timeout=15,
            )
            r2.raise_for_status()
            stk_data = r2.json()
            stk_list = stk_data.get("data", {}).get("stkinfolist", [])
            for item in stk_list:
                security = item.get("security", "")
                parts = security.split("$")
                if len(parts) < 2:
                    continue
                market = parts[0]
                code = parts[1]
                key = f"{market}_{code}"
                if key in seen:
                    continue
                seen.add(key)
                all_stocks.append(make_stock_entry(code, market, item.get("name", "")))
            logger.debug("  分组 %s(%s): %d 只股票", gname, gid, len(stk_list))
        except (requests.RequestException, json.JSONDecodeError) as e:
            logger.warning("  分组 %s 获取失败: %s", gid, e)

    logger.info("myfavor API: 共获取 %d 只自选股 (去重后)", len(all_stocks))
    return all_stocks


def fetch_stock_names(stocks: list[dict]) -> list[dict]:
    """填充股票名称。API 未返回名称时，尝试从巨潮资讯网补查。"""
    missing = [s for s in stocks if not s.get("name")]
    if not missing:
        return stocks

    # 批量补查：通过巨潮 API 用代码搜索获取名称
    try:
        from cninfo_api import CNINFO_QUERY_URL, HEADERS as CNINFO_HEADERS
        for stock in missing:
            try:
                resp = requests.post(
                    CNINFO_QUERY_URL,
                    headers=CNINFO_HEADERS,
                    data={"searchkey": stock["code"], "pageNum": 1, "pageSize": 1,
                          "column": "szse", "tabName": "fulltext"},
                    timeout=10,
                )
                resp.raise_for_status()
                anns = resp.json().get("announcements") or []
                if anns:
                    name = anns[0].get("secName", "")
                    if name:
                        stock["name"] = name
                        continue
            except (requests.RequestException, json.JSONDecodeError):
                pass
            # 兜底：用代码代替
            stock["name"] = stock["code"]
    except ImportError:
        for s in missing:
            if not s.get("name"):
                s["name"] = s["code"]

    return stocks


def fetch_announcements(
    stock: dict,
    cookie: Optional[str] = None,
    page_size: int = 10,
    days_back: int = 7,
) -> list[dict]:
    since_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    market = stock["market"]
    code = stock["code"]
    # 港股用 ann_type=H，A 股用 ann_type=A
    ann_type = "H" if market == "116" else "A"
    params = {
        "sr": -1,
        "page_size": page_size,
        "page_index": 1,
        "ann_type": ann_type,
        "stock_list": f"{market},{code}",
        "f_node": 0,
        "s_node": 0,
        "begin_time": since_date,
        "end_time": datetime.now().strftime("%Y-%m-%d"),
    }

    try:
        headers = HEADERS.copy()
        if cookie:
            headers["Cookie"] = cookie
        resp = requests.get(ANNOUNCE_API, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        announcements = data.get("data", {}).get("list", [])
        results = []
        for ann in announcements:
            art_code = ann.get("art_code", "")
            ann_url = (
                ann.get("ann_url")
                or f"https://data.eastmoney.com/notices/detail/{code}/{art_code}.html"
            )
            codes_list = ann.get("codes", [])
            ann_type_local = ""
            if codes_list:
                ann_type_local = codes_list[0].get("ann_type", "")

            results.append({
                "stock_code": stock["code"],
                "stock_name": stock.get("name", stock["code"]),
                "title": ann.get("title", ""),
                "ann_date": ann.get("notice_date", ""),
                "ann_type": ann_type_local,
                "url": ann_url,
                "art_code": art_code,
                "notice_id": str(ann.get("notice_date", "")),  # 实际存的是日期，字段名兼容旧数据
                "market": market,
            })
        logger.debug(
            "股票 %s(%s): 获取到 %d 条公告",
            stock.get("name", ""), stock["code"], len(results),
        )
        return results
    except (requests.RequestException, json.JSONDecodeError) as e:
        logger.warning("获取股票 %s(%s) 公告失败: %s", stock.get("name", ""), stock["code"], e)
        return []


def fetch_all_announcements(
    stocks: list[dict],
    cookie: Optional[str] = None,
    days_back: int = 7,
    delay: float = 0.5,
    max_workers: int = 5,
) -> list[dict]:
    all_anns = []
    total = len(stocks)

    def _fetch_one(stock):
        return stock, fetch_announcements(stock, cookie, days_back=days_back)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_fetch_one, s): s for s in stocks}
        for i, future in enumerate(as_completed(futures)):
            try:
                stock, anns = future.result()
                logger.info(
                    "获取完成 [%d/%d] %s(%s): %d 条",
                    i + 1, total, stock.get("name", ""), stock["code"], len(anns),
                )
                all_anns.extend(anns)
            except Exception as e:
                logger.warning("获取失败 [%d/%d] %s: %s", i + 1, total, futures[future].get("name", ""), e)

    return all_anns


def _is_real_stock(market: str, code: str) -> bool:
    """判断是否是有公告价值的真实个股（排除指数/ETF/债券/权证等）"""
    if market == "1":
        # SH: 60xxxx(主板) / 68xxxx(科创板) 为真实个股
        return bool(re.match(r"^60\d{4}$|^688\d{3}$", code))
    elif market == "0":
        # SZ: 00xxxx(主板/中小板) / 30xxxx(创业板) 为真实个股
        return bool(re.match(r"^00\d{4}$|^30\d{4}$", code))
    elif market == "116":
        # HK: 大部分是真实个股, 排除少数特殊代码(权证/牛熊证等)
        return bool(re.match(r"^\d{4,5}$", code))
    return False


def filter_real_stocks(stocks: list[dict]) -> list[dict]:
    """过滤出有公告价值的真实个股"""
    return [s for s in stocks if _is_real_stock(s["market"], s["code"])]


def load_stocks_from_config(config_path: str = "config.json") -> list[dict]:
    if not os.path.exists(config_path):
        return []
    try:
        with open(config_path, "r") as f:
            cfg = json.load(f)
        stocks_cfg = cfg.get("stocks", [])
        result = []
        for s in stocks_cfg:
            code = str(s.get("code", ""))
            market = str(s.get("market", "1"))
            if not code:
                continue
            result.append(make_stock_entry(code, market, s.get("name", None)))
        return result
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("加载配置文件自选股失败: %s", e)
        return []


def get_stocks(cookie_path: str = "cookie.txt", group_name: Optional[str] = None) -> list[dict]:
    """综合获取自选股列表.

    group_name: 可选，只获取指定分组的股票（模糊匹配分组名）
    优先级: myfavor API > Cookie 解析 > config.json
    """
    cookie = load_cookie(cookie_path)
    if not cookie:
        logger.info("未找到 Cookie, 尝试从 config.json 加载...")
        stocks = load_stocks_from_config()
        if stocks:
            logger.info("从 config.json 加载了 %d 只自选股", len(stocks))
        else:
            logger.warning("未获取到任何自选股！")
        return stocks

    # 1. myfavor API (lite.html 使用的方式)
    stocks = fetch_stocks_from_myfavor(cookie, group_name=group_name)
    if stocks:
        stocks = fetch_stock_names(stocks)
        # 过滤：仅保留有公告价值的真实个股 (SH/SZ/HK, 排除指数/ETF/债券)
        stocks = filter_real_stocks(stocks)
        logger.info("过滤后(仅真实个股): %d 只", len(stocks))
        return stocks

    # 2. Cookie 解析 (兜底)
    stocks = parse_selfselect_from_cookie(cookie)
    if stocks:
        return fetch_stock_names(stocks)

    # 3. config.json
    logger.info("API 未获取到, 尝试 config.json...")
    stocks = load_stocks_from_config()
    if stocks:
        logger.info("从 config.json 加载了 %d 只自选股", len(stocks))
    else:
        logger.warning("所有方式均未获取到自选股！")
    return stocks


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    stocks = get_stocks()
    if stocks:
        for s in stocks:
            print(f"  {s['name']:>8s} ({s['code']}) [{s['market_label']}]")
        anns = fetch_all_announcements(stocks, days_back=3)
        print(f"\n共获取 {len(anns)} 条公告")
        for a in anns[:5]:
            print(f"  [{a['ann_date']}] {a['stock_name']}: {a['title']}")