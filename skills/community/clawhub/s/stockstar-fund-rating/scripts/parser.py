#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 解析模块：从证券之星基金评级页中提取结构化数据。

评级页面结构（简化）：
  <span>评级日期：2026-06-30</span>
  <table>
    <tr>
      <td><a href="/funds/001075.shtml">001075</a></td>           ← 基金代码
      <td><a href="/funds/001075.shtml">宝盈转型动力混合A</a></td>← 基金名称
      <td><a href="/archives/...">宝盈基金</a></td>               ← 基金公司（跳过）
      <td><span class="fund-rating" data-rating="5">...</span></td>← 星级评级
      <td><span class="red_color">↑...</span></td>                 ← 评级变动
    </tr>
  </table>

核心业务流程：
  parse_rating_page  → 全量解析所有基金（用于缓存构建）
  extract_fund       → 按代码检索单只基金（用于缓存未命中时的补查）
  parse_rating_change→ 提取某只基金的评级变动方向（↑/↓/--）
"""

import re

from config import INSTITUTIONS


def parse_rating_date(html):
    """
    从页面中提取"评级日期"。
    数据位于页面顶部的 <span> 标签中，格式为 "评级日期：2026-06-30"。
    返回空字符串表示未找到（页面结构异常或已改变）。
    """
    m = re.search(r'评级日期：(\d{4}-\d{2}-\d{2})', html)
    return m.group(1) if m else ""


def parse_rating_page(html, inst_key):
    """
    全量解析某机构的评级页面，返回 {基金代码: 评级数据} 字典。

    每行包含基金代码、名称、星级评级。
    使用 data-rating 属性（值 1~5）作为数字评级来源。

    此函数在缓存构建（build_cache）时调用，下载 7 个页面后各调用一次。
    """
    funds = {}
    rows = re.findall(
        r'<tr>.*?<td[^>]*><a[^>]*>(\d{6})</a></td>'   # 基金代码（6位数字）
        r'.*?<td[^>]*><a[^>]*>(.*?)</a></td>'          # 基金名称
        r'.*?<td[^>]*>.*?</td>'                         # 基金公司列（跳过）
        r'.*?<td[^>]*><span[^>]*data-rating="(\d+)"',  # 星级评级（data-rating 属性）
        html, re.DOTALL
    )
    for code, name, rating in rows:
        funds[code] = {
            "name": name.strip(),
            "rating": rating,
            "rating_text": _rating_to_text(rating),
            "rating_stars": _rating_to_stars(rating),
        }
    return funds


def parse_rating_change(html, code):
    """
    解析某基金在页面中的评级变动方向。
    证券之星的评级变动用 ↑/↓ 标注在评级所在行的最后一列。
    返回 "up" / "down" / ""（无变动或未找到）。
    """
    pattern = rf'<a[^>]*>{code}</a>.*?</tr>'
    m = re.search(pattern, html, re.DOTALL)
    if not m:
        return ""
    row = m.group(0)
    if "↑" in row:
        return "up"
    if "↓" in row:
        return "down"
    return ""


def extract_fund(html, code, inst_key):
    """
    从页面上提取某只特定基金的评级数据。
    当缓存未命中时调用——基金不在全量缓存中，但可能已被该机构评级。
    使用两次正则：第一次取名称，第二次取 data-rating 值。
    同时调用 parse_rating_change 获取变动方向。
    """
    name = ""
    rating = ""

    # 提取基金名称：通过基金代码链接定位到所在行
    pattern = rf'<a[^>]*href="/funds/{code}.shtml">{code}</a></td>.*?<td[^>]*><a[^>]*href="/funds/{code}.shtml">(.*?)</a>'
    m = re.search(pattern, html, re.DOTALL)
    if m:
        name = m.group(1).strip()

    # 提取星级评级
    rating_m = re.search(
        rf'<a[^>]*href="/funds/{code}.shtml">.*?</a>.*?data-rating="(\d+)"',
        html, re.DOTALL
    )
    if rating_m:
        rating = rating_m.group(1)

    if not name and not rating:
        return None

    return {
        "name": name,
        "rating": rating,
        "rating_text": _rating_to_text(rating) if rating else "",
        "rating_stars": _rating_to_stars(rating) if rating else "",
        "change": parse_rating_change(html, code),
    }


def _rating_to_text(rating):
    """数字评级（1-5）→ 文字评级（一星~五星）。"""
    mapping = {"1": "一星", "2": "二星", "3": "三星", "4": "四星", "5": "五星"}
    return mapping.get(rating, "")


def _rating_to_stars(rating):
    """
    数字评级（1-5）→ 星星图案（★★★★★等）。
    1 星：★☆☆☆☆，5 星：★★★★★。
    非 1~5 的数字返回空字符串。
    """
    try:
        n = int(rating)
        if n < 1 or n > 5:
            return ""
        return "★" * n + "☆" * (5 - n)
    except (ValueError, TypeError):
        return ""
