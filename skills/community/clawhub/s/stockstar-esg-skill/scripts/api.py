#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 调用层：封装所有对外的 HTTP 请求。

包含：
- fetch_detail: 获取个股详情页 HTML
- fetch_list: 获取某家机构的评级列表 JSON
- search_by_suggest: 通过 suggest API 模糊搜索股票
- search_in_list: 通过逐页扫描评级列表来搜索
- search_heuristic: 试探式搜索（提取数字作为代码尝试）
"""

import json
import re
import urllib.parse

from config import BASE_URL, PROVIDERS
from utils import http_get
from parser import parse_detail_html


def fetch_detail(stock_code):
    """
    获取个股 ESG 详情页的 HTML 源码。

    数据来源：证券之星 ESG 详情页
        GET https://esg.stockstar.com/esg/pjdetail/{stock_code}

    参数：
        stock_code: 股票代码，如 "600519"（A 股 6 位）或 "00001"（港股 5 位）

    返回：
        详情页的完整 HTML 文本（交由 parser.parse_detail_html 解析）
    """
    url = f"{BASE_URL}/esg/pjdetail/{stock_code}"
    return http_get(url)


def fetch_list(provider_api, page=1, size=20):
    """
    获取某家评级机构的 ESG 评级列表（JSON 格式）。

    数据来源：证券之星 ESG 列表 API
        GET {BASE_URL}{provider_api}?page={page}&size={size}

    参数：
        provider_api: 机构 API 路径，如 "/data/GetHZESGs"
        page: 页码，从 1 开始
        size: 每页条数，固定 20

    返回：
        API 返回的原始 JSON 文本
    """
    url = f"{BASE_URL}{provider_api}?page={page}&size={size}"
    return http_get(url)


def search_by_suggest(keyword, retries=2):
    """
    通过东方财富 suggest API 搜索股票。

    此接口支持代码、中文全称、拼音缩写等多种输入，
    是首选搜索方式。与证券之星前端 JS 使用相同的请求格式。

    注意：请求参数 q 需要经过双重 URL 编码
        encodeURIComponent(encodeURIComponent(q))

    参数：
        keyword: 用户输入的搜索词（代码、名称或拼音）
        retries: API 请求异常时的重试次数（默认 2，含首次）

    返回：
        list[dict]，每个元素包含 name/code/type/source
        搜索失败或无可匹配时返回空列表
    """
    q = keyword
    # 如果输入全是数字，只提取数字部分（去掉可能的空格）
    match = re.search(r'\d+', keyword)
    if match and match.group() == keyword.strip():
        q = match.group()

    url = (
        "https://q.ssajax.cn/info/handler/xsuggesthandler.ashx?"
        f"q={urllib.parse.quote(urllib.parse.quote(q))}"
        "&type=101,102,103,104,105,107&n=result"
        "&ls=1,2,3,4&key=0&order=2&rows=10"
    )
    # 针对短名称（2-3 个中文字符），使用原始关键词检索，
    # 避免 suggest 对非标准输入格式处理异常
    for attempt in range(retries):
        try:
            text = http_get(url)
            # 提取 JSON 部分（接口返回有时包含前缀字符）
            data = json.loads(text[text.index("{"):text.rindex("}") + 1])
            candidates = []
            for item in data.get("datas", []):
                if len(item) >= 2:
                    # item[0]=代码, item[1]=名称, item[3]=市场类型
                    candidates.append({
                        "name": item[1],
                        "code": item[0],
                        "type": item[3] if len(item) > 3 else "",
                        "source": "suggest"
                    })
            return candidates
        except Exception:
            # suggest API 不稳定，异常时安静重试
            if attempt == retries - 1:
                return []


def search_in_list(keyword, max_pages=10):
    """
    通过逐页扫描评级列表 API 来搜索股票。

    当 suggest API 无结果时兜底使用。遍历华证和妙盈的列表 API，
    每页 20 条，最多扫描 max_pages 页，用名称子串匹配。

    参数：
        keyword: 搜索关键词
        max_pages: 最多扫描页数（每页 20 条）

    返回：
        list[dict]，匹配到的候选股票列表
    """
    candidates = []
    seen = set()
    kw = keyword.upper()
    # 华证列表数据量更大，优先扫描
    for prov_key in ["chindices", "miotech"]:
        prov = PROVIDERS[prov_key]
        for page in range(1, max_pages + 1):
            try:
                text = fetch_list(prov["api"], page, 20)
                resp = json.loads(text)
                # ret != 0 表示 API 返回错误，停止当前机构扫描
                if resp.get("ret") != 0:
                    break
                items = resp.get("data", [])
                if not items:
                    break
                for item in items:
                    name = item.get("STOCKNAME", "").strip()
                    code = item.get("STOCKCODE", "")
                    key = f"{code}_{name}"
                    if key in seen:
                        continue
                    seen.add(key)
                    # 名称或代码中包含关键词才保留
                    if kw in name.upper() or kw in code:
                        candidates.append({
                            "name": name,
                            "code": code,
                            "provider": prov["name"],
                            "source": "list_search"
                        })
            except Exception:
                break
    return candidates


def search_heuristic(keyword):
    """
    试探式搜索：从关键词中提取数字片段，直接当作股票代码请求详情页验证。

    当 suggest API 和列表扫描都无结果时的最后尝试手段。
    只适用于关键词中至少包含一组数字的情况。

    参数：
        keyword: 搜索关键词

    返回：
        list[dict]，能在详情页验证通过的股票列表
    """
    candidates = []
    # 提取关键词中的所有数字片段
    nums = re.findall(r'\d+', keyword)
    # 最多尝试前 3 个数字片段
    for num in nums[:3]:
        try:
            html = fetch_detail(num)
            data = parse_detail_html(html)
            name = data.get("stock_name", "")
            if name:
                candidates.append({
                    "name": name,
                    "code": data.get("stock_code", num),
                    "source": "heuristic"
                })
        except Exception:
            continue
    return candidates
