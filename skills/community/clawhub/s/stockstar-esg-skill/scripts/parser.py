#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 解析模块：从证券之星 ESG 详情页的 HTML 中提取结构化数据。

这是本项目的核心解析逻辑。详情页 HTML 结构如下：

    ┌─────────────────────────────────────┐
    │  <h2>贵州茅台</h2>                   │  ← 股票名称
    │  <p>600519</p>                      │  ← 股票代码
    ├─────────────────────────────────────┤
    │  <div id="my_content">              │  ← 妙盈科技区块
    │    <h2>A</h2>                       │     ← 综合评级 A
    │    <p>2025-06-30</p>                │     ← 评级日期
    │    <ul class="bot_list">            │     ← E/S/G 三维度评分
    │      <li><div>85.01</div></li>      │     ← E 评分
    │      <li><div>84.38</div></li>      │     ← S 评分
    │      <li><div>68.94</div></li>      │     ← G 评分
    │    </ul>
    │  </div>
    │  <div id="hz_content">...</div>     │  ← 华证指数区块（含评级和行业排名）
    │  <div id="sdrl_content">...</div>   │  ← 商道融绿区块（仅综合评级）
    └─────────────────────────────────────┘

三家机构的 ID 分别是：my_content / hz_content / sdrl_content。
华证额外提供 E/S/G 的评级字母和行业排名（如 5/29），
商道融绿只提供综合评级，E/S/G 维度数据为空占位。

正则解析策略：
    - 名称/代码：<h2>...</h2>\n<p>数字</p>
    - 等级：区块内的 <h2>...</h2>
    - 日期：区块内的 YYYY-MM-DD 格式字符串
    - E/S/G 评分：bot_list 中 <div>数值</div>
    - 评级字母：bot_list 中 <div>A</div> / <div>BBB</div> 等
    - 行业排名：bot_list 中 <div>5/29</div> 格式
"""

import re

from config import PROVIDER_NAME_MAP
from utils import normalize_name


def parse_detail_html(html_text):
    """
    解析证券之星 ESG 详情页 HTML，提取三家机构的评级数据。

    参数：
        html_text: 从 fetch_detail() 获取的完整 HTML 文本

    返回：
        dict，结构如下：
        {
            "stock_name": "贵州茅台",
            "stock_code": "600519",
            "妙盈科技": {
                "rate": "A",       "date": "2025-06-30",
                "e_score": "85.01", "s_score": "84.38", "g_score": "68.94",
                "e_rate": "",       "s_rate": "",       "g_rate": "",
                "e_rank": "",       "s_rank": "",       "g_rank": ""
            },
            "华证指数": {
                "rate": "AAA",     "date": "2026-04-30",
                "e_score": "82.73", "s_score": "87.72", "g_score": "92.14",
                "e_rate": "BBB",    "s_rate": "A",      "g_rate": "AA",
                "e_rank": "5/29",   "s_rank": "10/29",  "g_rank": "1/29"
            },
            "商道融绿": {
                "rate": "A",       "date": "2026-03-15",
                "e_score": "",      "s_score": "",      "g_score": "",
                "e_rate": "",       "s_rate": "",       "g_rate": "",
                "e_rank": "",       "s_rank": "",       "g_rank": ""
            }
        }

    注意：
        - 机构键名使用 PROVIDER_NAME_MAP 中的中文显示名，AI 可直接理解
        - 三家机构统一 schema：rate / date / e_score / s_score / g_score /
          e_rate / s_rate / g_rate / e_rank / s_rank / g_rank
        - 缺失字段统一补空字符串 ""，商道融绿的模板占位值主动清空
        - 注意：商道融绿的 E/S/G 字段在页面中为固定模板占位值，
          不应作为真实数据使用，故统一返回空字符串
    """
    # 三家机构统一字段集：综合评级 + 日期 + E/S/G 三维度（评分/评级/排名）
    # 各机构按自身数据深度填充，缺失项统一置空
    FIELDS = ["rate", "date",
              "e_score", "s_score", "g_score",
              "e_rate", "s_rate", "g_rate",
              "e_rank", "s_rank", "g_rank"]

    result = {}
    for ch_name in PROVIDER_NAME_MAP.values():
        result[ch_name] = {}

    # ---- 第一步：提取股票名称和代码 ----
    # HTML 结构：<h2>贵州茅台</h2>\n<p>600519</p>
    # 正则解释：[^<]+ 匹配任意非尖括号字符（股票名），\d{5,6} 匹配 5~6 位数字（代码）
    name_match = re.search(r'<h2>([^<]+)</h2>\s*<p>(\d{5,6})</p>', html_text)
    if name_match:
        result["stock_name"] = normalize_name(name_match.group(1))
        result["stock_code"] = name_match.group(2)

    # ---- 第二步：从 bot_list 中提取 E/S/G 三维度数据 ----
    def extract_scores_from_botlist(section):
        """
        从某个机构区块的 bot_list 中提取三维度数据。

        bot_list 是 ESG 详情页中展示 E/S/G 评分的 UL 列表，
        每个机构区块内的提取方式相同：
          - 数值（如 85.01） → E/S/G 评分
          - 字母（如 BBB）  → E/S/G 评级（仅华证有）
          - 分数（如 5/29） → E/S/G 行业排名（仅华证有）

        参数：
            section: 某机构 div 区块的 HTML 文本

        返回：
            (scores_dict, rates_dict, ranks_dict) 三元组，
            分别包含 e_score/s_score/g_score、e_rate/s_rate/g_rate、e_rank/s_rank/g_rank
        """
        # 定位 bot_list 的起始位置
        pos = section.find('bot_list')
        if pos == -1:
            return {}, {}, {}
        # 取 bot_list 后面 2000 字符作为分析范围（足够覆盖所有 li 内容）
        block = section[pos:pos + 2000]

        # 用三个正则分别提取三类数据：
        # 1. 浮点数评分：<div>85.01</div> → 匹配含小数点的数字
        scores = re.findall(r'<div>\s*([\d.]+)\s*</div>', block)
        # 2. 评级字母：<div>BBB</div> → 匹配 1~3 位大写字母（含 +/-）
        rates = re.findall(r'<div>\s*([A-Z][A-Z+-]{0,2})\s*</div>', block)
        # 3. 行业排名：<div>5/29</div> → 匹配 "数字/数字" 格式
        ranks = re.findall(r'<div>\s*(\d+/\d+)\s*</div>', block)

        # 过滤掉非评分的浮点数（如权重字段权重 0.15 这类只有一位小数的值）
        numeric_scores = [s for s in scores if s.count(".") <= 1]

        # 取前 3 个数值作为 E/S/G 评分
        s = {}
        if len(numeric_scores) >= 3:
            s["e_score"] = numeric_scores[0]
            s["s_score"] = numeric_scores[1]
            s["g_score"] = numeric_scores[2]

        # 取前 3 个评级字母作为 E/S/G 评级
        r = {}
        if len(rates) >= 1:
            r["e_rate"] = rates[0] if len(rates) > 0 else ""
            r["s_rate"] = rates[1] if len(rates) > 1 else ""
            r["g_rate"] = rates[2] if len(rates) > 2 else ""

        # 取前 3 个排名作为 E/S/G 行业排名
        k = {}
        if len(ranks) >= 1:
            k["e_rank"] = ranks[0] if len(ranks) > 0 else ""
            k["s_rank"] = ranks[1] if len(ranks) > 1 else ""
            k["g_rank"] = ranks[2] if len(ranks) > 2 else ""

        return s, r, k

    # ---- 第三步：从指定机构区块中提取综合评级 + 日期 ----
    def extract_rating_data(section_id, result_key):
        """
        提取某个评级机构的完整数据。

        流程：
        1. 按 id 定位到机构区块（如 id="my_content"）
        2. 从该区块的 h2 标签提取综合评级等级
        3. 从该区块提取 YYYY-MM-DD 格式的日期
        4. 从该区块的 bot_list 提取 E/S/G 评分、评级、排名

        参数：
            section_id: HTML DOM 元素的 id，如 "my_content"
            result_key: result 字典的 key，如 "妙盈科技"
        """
        # 兼容双引号和单引号两种 id 写法
        for pattern in [f'id="{section_id}"', f"id='{section_id}'"]:
            section_start = html_text.find(pattern)
            if section_start != -1:
                break
        if section_start == -1:
            return

        # 取该区块后面 8000 字符（足够覆盖整个机构的数据区）
        section = html_text[section_start:section_start + 8000]

        # 提取综合评级等级（区块内第一个 h2 标签）
        h2_match = re.search(r'<h2>([^<]+)</h2>', section)
        if h2_match:
            result[result_key]["rate"] = h2_match.group(1).strip()

        # 提取评级日期（区块内第一个 YYYY-MM-DD 格式字符串）
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', section)
        if date_match:
            result[result_key]["date"] = date_match.group(1)

        # 提取 E/S/G 三维度数据
        scores, rates, ranks = extract_scores_from_botlist(section)
        result[result_key].update(scores)
        result[result_key].update(rates)
        result[result_key].update(ranks)

    # 依次提取三家机构的数据（键名使用 PROVIDER_NAME_MAP 中的中文名）
    extract_rating_data("my_content", PROVIDER_NAME_MAP["miotech"])
    extract_rating_data("hz_content", PROVIDER_NAME_MAP["chindices"])
    extract_rating_data("sdrl_content", PROVIDER_NAME_MAP["syntaogf"])

    # 统一 schema：三家机构输出相同字段集，缺失字段补 ""，模板值清空
    for ch_name in PROVIDER_NAME_MAP.values():
        prov = result[ch_name]
        for field in FIELDS:
            if field not in prov:
                prov[field] = ""
    # 商道融绿的 E/S/G 评分和排名是页面模板占位值（非真实数据），置空
    syntaogf_name = PROVIDER_NAME_MAP["syntaogf"]
    for field in ["e_score", "s_score", "g_score", "e_rank", "s_rank", "g_rank"]:
        result[syntaogf_name][field] = ""

    return result
