#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 解析模块：解析线索挖掘页面的 HTML，提取结构化信号数据。

页面结构：
- 多个 <ul class="clue_ul"> 块，每个块对应一个线索类别
- 每个块包含表头 <li>（含"线索名"）+ 数据 <li>（含实际信号）
- 每个数据 <li> 包含 clue_id（5个字段）+ clue_detail（时间线）

包含：
- parse_signal_page: 解析信号页面 HTML，返回结构化信号列表
- _extract_text: 从 HTML 标签中提取纯文本
- _decode_html_entities: 解码 HTML 实体
"""

import re
import html as html_module


def _decode_html_entities(text):
    """解码 HTML 实体（如 &#183; → ·）"""
    if not text:
        return ""
    return html_module.unescape(text)


def _extract_text(html_fragment):
    """从 HTML 片段中提取纯文本，去除所有标签并解码实体"""
    if not html_fragment:
        return ""
    text = re.sub(r'<[^>]+>', '', html_fragment)
    text = _decode_html_entities(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _parse_timeline(detail_html):
    """
    解析信号详情中的时间线。

    时间线结构：
    - 每个时间点包含：日期、变化标签、态度、Q&A 链接
    """
    timeline = []

    # 提取每个时间线项：日期 + 标签 + 态度 + 链接
    time_blocks = re.split(r'<div class="timeline_dot">', detail_html)

    for block in time_blocks[1:]:  # 跳过第一个空块
        item = {}

        # 提取日期
        date_match = re.search(r'class="detail_time">\s*(\d{4}-\d{2}-\d{2})', block)
        if date_match:
            item["date"] = date_match.group(1)

        # 提取变化标签（detail_item1）
        label_match = re.search(r'class="detail_item1">\s*(.*?)\s*</li>', block, re.DOTALL)
        if label_match:
            item["label"] = _extract_text(label_match.group(1))

        # 提取态度（detail_item2 detail_item4）
        sentiment_match = re.search(r'class="detail_item2 detail_item4">\s*(.*?)\s*</li>', block, re.DOTALL)
        if sentiment_match:
            item["sentiment"] = _extract_text(sentiment_match.group(1))

        # 提取详情链接
        link_match = re.search(r'href="(https://stock\.stockstar\.com/dmhd/detail/\d+)"', block)
        if link_match:
            item["detail_url"] = link_match.group(1)

        if item.get("date"):
            timeline.append(item)

    return timeline


def _parse_signal_block(block_html):
    """
    解析单个信号块，提取结构化数据。

    信号块结构：
    - clue_id div: 包含5个字段（线索名/线索类别/变化类别/边际变化总结/重要性）
    - clue_detail div: 包含时间线

    参数：
        block_html: 单个信号项的 HTML 内容

    返回：
        dict: 信号数据，解析失败返回 None
    """
    signal = {}

    # 提取 clue_id 中的5个字段
    clue_id_match = re.search(r'class="clue_id">(.*?)</div>\s*(?:<div class="clue_detail"|<div class="detail_btn")', block_html, re.DOTALL)
    if not clue_id_match:
        # 兜底：尝试提取到 clue_detail 为止
        clue_id_match = re.search(r'class="clue_id">(.*?)class="clue_detail"', block_html, re.DOTALL)

    if clue_id_match:
        clue_id_html = clue_id_match.group(1)
        # 提取 clue_id 中的直接子 div 内容
        divs = re.findall(r'<div(?:\s+class="[^"]*")?\s*>(.*?)</div>', clue_id_html, re.DOTALL)
        div_texts = [_extract_text(d) for d in divs if _extract_text(d)]

        # 过滤掉按钮文本（展开详情/收起详情）
        div_texts = [t for t in div_texts if t not in ('展开详情', '收起详情')]

        # div 顺序：线索名, 线索类别, 变化类别, 边际变化总结, 重要性
        if len(div_texts) >= 5:
            signal["name"] = div_texts[0]
            signal["category"] = div_texts[1]
            signal["change_type"] = div_texts[2]
            signal["summary"] = div_texts[3]
            signal["importance"] = div_texts[4]

    # 提取详情中的时间线
    detail_match = re.search(r'class="clue_detail"[^>]*>(.*?)$', block_html, re.DOTALL)
    if detail_match:
        signal["timeline"] = _parse_timeline(detail_match.group(1))
    else:
        signal["timeline"] = []

    if signal.get("name"):
        return signal
    return None


def parse_signal_page(html):
    """
    解析线索挖掘页面 HTML，返回结构化信号列表。

    策略：找到所有包含 clue_id 的 <li> 块，每个块是一个独立信号。
    跳过包含"线索名"的表头块。

    参数：
        html: 信号页面的完整 HTML 文本

    返回：
        dict: {
            "stock_name": str,
            "stock_code": str,
            "signals": [...]
        }
    """
    result = {"stock_name": "", "stock_code": "", "signals": []}

    # 提取股票名称（处理 HTML 实体 &#183; → ·）
    name_match = re.search(r'nav_header.*?<h2>(.*?)</h2>', html, re.DOTALL)
    if name_match:
        raw_name = _extract_text(name_match.group(1))
        # 去掉 "线索挖掘·" 前缀
        raw_name = re.sub(r'^线索挖掘[···]', '', raw_name).strip()
        result["stock_name"] = raw_name

    # 提取股票代码
    code_match = re.search(r'breadcrumbCode[^>]*>\((\d{6})\)', html)
    if not code_match:
        code_match = re.search(r'\((\d{6})\)', html)
    if code_match:
        result["stock_code"] = code_match.group(1)

    # 检查是否有"暂无信息"
    if re.search(r'暂无信息', html):
        return result

    # 策略：找到所有 <li> 位置和所有 clue_id 位置
    # 每个 clue_id 对应一个 <li>（header 或 data）
    # 正则 <li\b[^>]*> 兼容无属性 <li> 和带属性 <li class="...">
    li_positions = [m.start() for m in re.finditer(r'<li\b[^>]*>', html)]
    clue_id_positions = [m.start() for m in re.finditer(r'clue_id', html)]

    # 对每个 clue_id，找到它所在的 <li> 起始位置
    signal_li_starts = []
    for cid_pos in clue_id_positions:
        # 找到最近的、在 clue_id 之前的 <li>
        nearest_li = None
        for li_pos in li_positions:
            if li_pos < cid_pos:
                nearest_li = li_pos
            else:
                break
        if nearest_li is not None:
            signal_li_starts.append(nearest_li)

    # 去重并排序
    signal_li_starts = sorted(set(signal_li_starts))

    # 对每个 <li> 块，提取从该 <li> 到下一个 <li>（或 </ul>）之间的内容
    for i, li_start in enumerate(signal_li_starts):
        # 确定块的结束位置
        if i + 1 < len(signal_li_starts):
            li_end = signal_li_starts[i + 1]
        else:
            # 最后一个块：找到最近的 </ul>
            ul_end = html.find('</ul>', li_start)
            li_end = ul_end if ul_end > li_start else len(html)

        block_html = html[li_start:li_end]

        # 跳过表头块（包含"线索名"）
        if '线索名' in block_html and '线索类别' in block_html:
            continue

        signal = _parse_signal_block(block_html)
        if signal:
            result["signals"].append(signal)

    return result
