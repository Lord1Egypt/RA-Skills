#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置模块：存放本项目所有常量配置。

包含：
- 证券之星投资者互动数据源的 BASE_URL 和请求超时
- 股票代码前缀映射（sh/sz）
- 标签领域（domain）的中英文映射
"""

# 证券之星投资者互动页面根地址
BASE_URL = "https://stock.stockstar.com/dmhd"

# 所有 HTTP 请求的超时秒数
TIMEOUT = 15

# 每页默认条数
PAGE_SIZE = 10

# 股票代码前缀规则：6 位代码自动补 sh/sz 前缀
# stockid 格式：sh600000 / sz000001
MARKET_PREFIX = {
    "6": "sh",  # 沪市：60xxxx
    "0": "sz",  # 深市：00xxxx / 002xxx / 003xxx
    "3": "sz",  # 创业板：30xxxx
}

# 标签领域映射（domain）：用户输入中文 → API 参数
DOMAIN_MAP = {
    "热点题材": "hot_topic",
    "业务运营": "business",
    "公司治理": "govern",
    "风险提示": "risk",
    "财务能力": "finance",
    "hot_topic": "hot_topic",
    "business": "business",
    "govern": "govern",
    "risk": "risk",
    "finance": "finance",
}

# 领域中文名映射（JSON 输出用）
DOMAIN_NAME_MAP = {
    "hot_topic": "热点题材",
    "business": "业务运营",
    "govern": "公司治理",
    "risk": "风险提示",
    "finance": "财务能力",
}

# 语义倾向映射
SENTIMENT_MAP = {
    1: "乐观",
    2: "中性",
    3: "谨慎",
}

# 回复质量映射
REPLY_TYPE_MAP = {
    1: "内容详尽",
    2: "模板套话",
    3: "回避敏感问题",
}

# 线索重要性排序权重
IMPORTANCE_WEIGHT = {
    "高": 3,
    "中": 2,
    "低": 1,
}
