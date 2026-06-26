#!/usr/bin/env python3
"""巨潮资讯网公告获取模块 - 通过 cninfo API 获取公告列表和全文

巨潮资讯网是证监会指定的上市公司信息披露平台，覆盖沪深京全部A股。
支持按股票代码、日期范围精确查询。

API:
  POST http://www.cninfo.com.cn/new/hisAnnouncement/query
    - searchkey: 股票代码或名称
    - seDate: 日期范围 "YYYY-MM-DD~YYYY-MM-DD"
    - pageNum/pageSize: 分页

  PDF 链接: http://static.cninfo.com.cn/{adjunctUrl}
"""

import json
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Optional

import requests

logger = logging.getLogger(__name__)

CNINFO_QUERY_URL = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
CNINFO_PDF_BASE = "https://static.cninfo.com.cn/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/search",
}


def _parse_date(ts) -> str:
    """将 cninfo 的时间戳（epoch ms）转为 YYYY-MM-DD"""
    try:
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")
        return str(ts)[:10]
    except (TypeError, ValueError, OSError):
        return str(ts)[:10]


def _strip_em(text: str) -> str:
    """去掉 <em> 高亮标签"""
    return re.sub(r"</?em>", "", text) if text else ""


def fetch_cninfo_announcements(
    stock_code: str,
    stock_name: str = "",
    start_date: str = "",
    end_date: str = "",
    page_size: int = 30,
) -> list[dict]:
    """从巨潮资讯网获取指定股票的公告列表

    Args:
        stock_code: 股票代码（如 600519）
        stock_name: 股票名称（可选，用于日志）
        start_date: 开始日期 YYYY-MM-DD（默认 30 天前）
        end_date: 结束日期 YYYY-MM-DD（默认今天）
        page_size: 每页数量

    Returns:
        公告列表，每个包含 title, ann_date, url, art_code 等
    """
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        from datetime import timedelta
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    se_date = f"{start_date}~{end_date}"
    all_anns = []
    page = 1

    while True:
        body = {
            "pageNum": page,
            "pageSize": page_size,
            "column": "szse",
            "tabName": "fulltext",
            "plate": "",
            "stock": "",
            "searchkey": stock_code,
            "secid": "",
            "category": "",
            "trade": "",
            "seDate": se_date,
            "sortName": "",
            "sortType": "",
            "isHLtitle": "true",
        }
        try:
            resp = requests.post(
                CNINFO_QUERY_URL, headers=HEADERS, data=body, timeout=15
            )
            resp.raise_for_status()
            data = resp.json()
            anns = data.get("announcements") or []
            if not anns:
                break

            for a in anns:
                sc = a.get("secCode", "")
                if sc and sc != stock_code:
                    continue
                adjunct_url = a.get("adjunctUrl", "")
                pdf_url = CNINFO_PDF_BASE + adjunct_url if adjunct_url else ""
                all_anns.append({
                    "stock_code": stock_code,
                    "stock_name": _strip_em(a.get("secName", stock_name or stock_code)),
                    "title": _strip_em(a.get("announcementTitle", "")),
                    "ann_date": _parse_date(a.get("announcementTime", "")),
                    "ann_type": "",
                    "url": pdf_url,
                    "art_code": adjunct_url.replace("finalpage/", "").replace(".PDF", "").replace("/", "_"),
                    "notice_id": str(a.get("announcementId", "")),
                    "pdf_url": pdf_url,
                    "market": "A股",
                })

            if not data.get("hasMore") or page >= 20:
                break
            page += 1
            time.sleep(0.3)

        except (requests.RequestException, json.JSONDecodeError) as e:
            logger.warning("巨潮查询失败 stock=%s: %s", stock_code, e)
            break

    return all_anns


def fetch_all_cninfo(
    stocks: list[dict],
    days_back: int = 7,
    delay: float = 0.5,
    max_workers: int = 5,
) -> list[dict]:
    """批量从巨潮资讯网获取所有自选股的公告（并发）"""
    from datetime import timedelta
    end = datetime.now()
    start = end - timedelta(days=days_back)
    start_date = start.strftime("%Y-%m-%d")
    end_date = end.strftime("%Y-%m-%d")

    all_anns = []
    total = len(stocks)

    def _fetch_one(stock):
        code = stock["code"]
        name = stock.get("name", code)
        anns = fetch_cninfo_announcements(
            stock_code=code,
            stock_name=name,
            start_date=start_date,
            end_date=end_date,
        )
        logger.info("巨潮 %s(%s): %d 条", name, code, len(anns))
        return anns

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_fetch_one, s): s for s in stocks}
        for i, future in enumerate(as_completed(futures)):
            stock = futures[future]
            try:
                anns = future.result()
                all_anns.extend(anns)
            except (requests.RequestException, json.JSONDecodeError, KeyError, TypeError) as e:
                logger.warning("巨潮查询失败 %s: %s", stock.get("name", ""), e)

    logger.info("巨潮公告共获取 %d 条", len(all_anns))
    return all_anns
