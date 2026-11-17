#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 调用层：封装所有对外的 HTTP 请求。

包含：
- fetch_qa: 获取投资者互动问答列表（JSON API）
- fetch_qa_by_tag: 按标签筛选问答
- fetch_tag_stats: 获取标签统计数据
- fetch_signal_page: 获取线索挖掘页面 HTML
- search_stock: 通过 suggest API 模糊搜索股票
"""

import json
import re
import urllib.parse

from config import BASE_URL, PAGE_SIZE
from utils import http_get, normalize_stock_id


def fetch_qa(stock_code, page=1, size=PAGE_SIZE):
    """
    获取投资者互动问答列表（JSON API）。

    数据来源：证券之星投资者互动 API
        GET {BASE_URL}/data/GetIrmQuestAnnotation/{stockid}/{page}/{size}

    参数：
        stock_code: 股票代码（6 位数字或 sh/sz 前缀格式）
        page: 页码，从 1 开始
        size: 每页条数，默认 10

    返回：
        dict: {"items": [...], "has_more": bool, "stock_name": str, "stock_code": str}
    """
    stockid = normalize_stock_id(stock_code)
    url = f"{BASE_URL}/data/GetIrmQuestAnnotation/{stockid}/{page}/{size}"
    text = http_get(url)
    resp = json.loads(text)

    if resp.get("ret") != 0:
        return {"items": [], "has_more": False, "stock_name": "", "stock_code": stock_code}

    items = resp.get("data", [])
    has_more = not resp.get("is_end", True)
    stock_name = items[0].get("STOCKNAME", "") if items else ""
    stock_code_raw = items[0].get("STOCKCODE", "") if items else stock_code

    return {
        "items": items,
        "has_more": has_more,
        "stock_name": stock_name,
        "stock_code": stock_code_raw,
    }


def fetch_qa_by_tag(stock_code, domain, tag_name, page=1, size=PAGE_SIZE):
    """
    按标签筛选投资者互动问答。

    数据来源：
        GET {BASE_URL}/data/GetIrmQuestAnnotationByTagName/{stockid}/{domain}/{tagname}/{page}/{size}

    参数：
        stock_code: 股票代码
        domain: 标签领域（如 govern/risk/business/finance/hot_topic）
        tag_name: 标签名称（URL 编码）
        page: 页码
        size: 每页条数

    返回：
        dict: {"items": [...], "has_more": bool, "stock_name": str, "stock_code": str}
    """
    stockid = normalize_stock_id(stock_code)
    encoded_tag = urllib.parse.quote(tag_name)
    url = f"{BASE_URL}/data/GetIrmQuestAnnotationByTagName/{stockid}/{domain}/{encoded_tag}/{page}/{size}"
    text = http_get(url)
    resp = json.loads(text)

    if resp.get("ret") != 0:
        return {"items": [], "has_more": False, "stock_name": "", "stock_code": stock_code}

    items = resp.get("data", [])
    has_more = not resp.get("is_end", True)
    stock_name = items[0].get("STOCKNAME", "") if items else ""
    stock_code_raw = items[0].get("STOCKCODE", "") if items else stock_code

    return {
        "items": items,
        "has_more": has_more,
        "stock_name": stock_name,
        "stock_code": stock_code_raw,
    }


def fetch_tag_stats(stock_code, domain="all"):
    """
    获取标签统计数据（词云）。

    数据来源：
        GET {BASE_URL}/data/GetIrmQuestTagStat/{stockid}/{domain}

    参数：
        stock_code: 股票代码
        domain: 标签领域（all 表示全部）

    返回：
        list[dict]: 标签列表，每项含 TAG_NAME, TAG_DOMAIN, TAG_COUNT
    """
    stockid = normalize_stock_id(stock_code)
    url = f"{BASE_URL}/data/GetIrmQuestTagStat/{stockid}/{domain}"
    text = http_get(url)
    resp = json.loads(text)

    if resp.get("ret") != 0:
        return []

    return resp.get("data", [])


def fetch_signal_page(stock_code):
    """
    获取线索挖掘页面的完整 HTML。

    数据来源：
        GET https://stock.stockstar.com/dmhd/signal/{stockid}

    参数：
        stock_code: 股票代码

    返回：
        str: 信号页面的完整 HTML 文本（交由 parser 解析）
    """
    stockid = normalize_stock_id(stock_code)
    url = f"https://stock.stockstar.com/dmhd/signal/{stockid}"
    return http_get(url)


def search_stock(keyword, retries=2):
    """
    通过 suggest API 搜索股票。

    此接口支持代码、中文全称、拼音缩写等多种输入，
    与证券之星前端 JS 使用相同的请求格式。

    注意：请求参数 q 需要经过双重 URL 编码

    参数：
        keyword: 用户输入的搜索词
        retries: 重试次数（默认 2）

    返回：
        list[dict]: 每项含 name, code, stockid, source；
                   所有重试均失败时返回空列表
    """
    q = keyword.strip()

    url = (
        "https://q.ssajax.cn/info/handler/xsuggesthandler.ashx?"
        f"q={urllib.parse.quote(urllib.parse.quote(q))}"
        "&type=101,102,103,104,105,106,107&n=result"
        "&ls=1,2,3,4&key=0&order=2&rows=10"
    )

    for attempt in range(retries):
        try:
            text = http_get(url, raise_on_error=False)
            if not text:
                continue
            data = json.loads(text[text.index("{"):text.rindex("}") + 1])
            candidates = []
            for item in data.get("datas", []):
                if len(item) >= 2:
                    code = item[0]
                    name = item[1]
                    # 只保留 A 股（6 位代码）
                    if re.match(r'^\d{6}$', code):
                        stockid = normalize_stock_id(code)
                        candidates.append({
                            "name": name,
                            "code": code,
                            "stockid": stockid,
                            "source": "suggest"
                        })
            return candidates
        except Exception:
            if attempt == retries - 1:
                return []
    return []
