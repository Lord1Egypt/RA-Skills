#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 解析模块：从证券之星科技频道页面提取大模型调用排行榜。

排行榜数据服务端直出，周榜（id="week"）与日榜（id="day"）
以两个 <ul> 形式内嵌在页面中，无独立 API。

单个 <li> 结构（当前线上版本）：
    <li>
        <div>
            <p> DeepSeek V4 Flash 0731</p>   ← 模型名（<p> 内，带前导空格）
            <p class="source">deepseek</p>    ← 厂商（vendor，新字段）
        </div>
        <div>
            <p>11.3T</p>                      ← Tokens 值（T/B 单位）
            <p class="tokens_num">
                <svg ... fill="#FF0000">...</svg>  ← 趋势箭头（红涨/绿跌，可选）
                <span>20%</span>                   ← 变动百分比
                （或 <span style="color:#6467F2">new</span> → 新上榜）
            </p>
        </div>
    </li>

历史版本模型名曾直接写在 <div> 内（<div>ModelName</div>），
解析器对两种结构均兼容。

页脚数据来源（最新结构，含更新日期）：
    <div class="data_source" style="...">
        <p style="...">更新日期：2026-08-20</p>
        <p>数据来源：openrouter</p>
    </div>

核心业务流程：
    parse_ranking_html → 提取日榜 + 周榜两个列表 + 页脚数据来源 + 更新日期
"""

import re

from config import TREND_COLORS

# 页面中两个 <ul> 的 id（week 对应周榜，day 对应日榜）
LIST_IDS = ("week", "day")


def parse_ranking_html(html):
    """
    解析排行榜页面 HTML。

    返回：
        {"week": [...], "day": [...], "data_source": "数据来源：openrouter",
         "updated_at": "2026-08-20"}

    每条包含 rank / model / vendor / tokens / change / trend / is_new。
    updated_at 为页面页脚标注的榜单更新日期，缺失返回空字符串。
    页面结构缺失或变化时，对应周期返回空列表，不抛异常。
    """
    result = {
        "data_source": _extract_data_source(html),
        "updated_at": _extract_update_date(html),
    }
    for pid in LIST_IDS:
        block = _extract_ul(html, pid)
        result[pid] = _parse_items(block) if block else []
    return result


def _extract_data_source(html):
    """
    提取页脚数据来源（如"数据来源：openrouter"）；找不到返回空字符串。

    兼容 data_source div 带任意属性（如 style），且通过前缀匹配
    定位"数据来源："所在的 <p>，与"更新日期："的先后顺序无关。
    """
    return _extract_footer_value(html, "数据来源：", keep_prefix=True)


def _extract_update_date(html):
    """提取页脚榜单更新日期（如"2026-08-20"）；找不到返回空字符串。"""
    return _extract_footer_value(html, "更新日期：", keep_prefix=False)


def _extract_footer_value(html, prefix, keep_prefix):
    """
    在数据来源页脚 <div class="data_source"> 内，取以 prefix 开头的 <p> 文本。

    keep_prefix=True 返回含前缀的完整文本，否则只返回值部分。
    """
    m = re.search(r'<div[^>]*class="[^"]*data_source[^"]*"[^>]*>(.*?)</div>',
                  html, re.DOTALL)
    if not m:
        return ""
    for pm in re.findall(r'<p[^>]*>(.*?)</p>', m.group(1), re.DOTALL):
        text = pm.strip()
        if text.startswith(prefix):
            return text if keep_prefix else text[len(prefix):]
    return ""


def _extract_ul(html, period_id):
    """提取指定 id 的 <ul> 块内容；找不到返回空字符串。"""
    m = re.search(r'<ul[^>]*id="%s"[^>]*>(.*?)</ul>' % period_id, html, re.DOTALL)
    return m.group(1) if m else ""


def _parse_items(block):
    """解析 <ul> 块内的全部 <li> 条目，rank 从 1 开始递增。"""
    items = []
    for idx, li in enumerate(re.findall(r'<li>(.*?)</li>', block, re.DOTALL), 1):
        item = _parse_item(li)
        if item is not None:
            item["rank"] = idx
            items.append(item)
    return items


def _parse_item(li):
    """解析单条 <li>，结构异常时返回 None（由调用方跳过）。"""
    model = _extract_model(li)
    tokens = _extract_tokens(li)
    if not model or not tokens:
        return None
    is_new, change = _extract_change(li)
    return {
        "model": model,
        "vendor": _extract_vendor(li),
        "tokens": tokens,
        "change": change,
        "trend": _extract_trend(li),
        "is_new": is_new,
    }


def _extract_model(li):
    """
    提取模型名：取首个 <div> 内容。

    新结构：模型名在 <p> 内，取其中首个无属性 <p>。
    旧结构：<div> 直接是文本，兜底取 <div> 原始文本。
    """
    m = re.search(r'<div>(.*?)</div>', li, re.DOTALL)
    if not m:
        return ""
    block = m.group(1)
    pm = re.search(r'<p>(.*?)</p>', block, re.DOTALL)
    return pm.group(1).strip() if pm else block.strip()


def _extract_vendor(li):
    """提取厂商字段（<p class="source">），缺失返回空字符串。"""
    m = re.search(r'<p class="source">(.*?)</p>', li, re.DOTALL)
    return m.group(1).strip() if m else ""


def _extract_tokens(li):
    """提取 Tokens 值：取第二个 <div> 中首个无属性 <p>。"""
    divs = re.findall(r'<div>(.*?)</div>', li, re.DOTALL)
    if len(divs) < 2:
        return ""
    m = re.search(r'<p>(.*?)</p>', divs[1], re.DOTALL)
    return m.group(1).strip() if m else ""


def _extract_trend(li):
    """
    从 svg fill 颜色判断趋势方向：红=up（涨），绿=down（跌），无箭头=空。

    注：取条目内首个 <svg> 的 fill，依赖"趋势箭头是条目标记中第一个 svg"
    的页面结构；若页面在其他元素中先插入带 fill 的 svg 会误判（当前页面安全）。
    """
    m = re.search(r'<svg[^>]*fill="([^"]+)"', li)
    if not m:
        return ""
    return TREND_COLORS.get(m.group(1).strip().lower(), "")


def _extract_change(li):
    """
    提取变动百分比与新上榜标记。

    注：取条目内首个 <span> 文本，依赖"变动/新上榜是条目标记中第一个 span"
    的页面结构；若模型名等文本内先出现 <span> 会误取（当前页面安全）。

    返回 (is_new, change)：
        - 含 "new" 标记 → (True, "")，变动百分比为空
        - 含百分比 span → (False, "20%")
        - 无 span → (False, "")（页面结构变化时兜底）
    """
    m = re.search(r'<span[^>]*>(.*?)</span>', li, re.DOTALL)
    if not m:
        return False, ""
    text = m.group(1).strip()
    if text.lower() == "new":
        return True, ""
    return False, text