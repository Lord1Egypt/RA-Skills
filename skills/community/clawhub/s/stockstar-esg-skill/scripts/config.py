#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置模块：存放本项目所有常量配置。

包含：
- 证券之星 ESG 数据源的 BASE_URL 和请求超时
- 三家评级机构（妙盈/华证/商道融绿）的标识名称与 API 路径
- 评级机构别名的中英文映射表
"""

# 证券之星 ESG 页面根地址
BASE_URL = "https://esg.stockstar.com"
# 所有 HTTP 请求的超时秒数
TIMEOUT = 15

# 三家评级机构的元信息配置
# key=机构英文名，name=中文显示名，api=列表 API 的 URL 路径
PROVIDERS = {
    "miotech": {"name": "妙盈科技", "api": "/data/GetMYESGs"},
    "chindices": {"name": "华证指数", "api": "/data/GetHZESGs"},
    "syntaogf": {"name": "商道融绿", "api": "/data/GetSDLRESGs"},
}

# 内部 key → JSON 输出用中文显示名（AI 自解释，无需映射）
PROVIDER_NAME_MAP = {
    "miotech": "妙盈科技",
    "chindices": "华证指数",
    "syntaogf": "商道融绿",
}

# 用户输入的中英文机构别名 → 映射到 PROVIDERS 的 key
# 支持全称、简称、英文名等多入口
PROVIDER_ALIAS = {
    "妙盈": "miotech", "妙盈科技": "miotech", "miotech": "miotech",
    "华证": "chindices", "华证指数": "chindices", "chindices": "chindices",
    "商道融绿": "syntaogf", "syntaogf": "syntaogf",
}
