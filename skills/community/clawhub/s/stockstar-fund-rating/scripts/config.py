#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
证券之星基金评级 — 配置模块。

定义七家评级机构的基础信息（内部 key、中文名、页面路径），
以及全局超时时间和缓存文件命名。
"""

# 证券之星基金评级首页
BASE_URL = "https://fund.stockstar.com"

# 七家评级机构配置
# key：内部唯一标识（短英文，用于缓存字典的键名）
# name：中文展示名，最终输出给用户
# page：机构评级页面的相对路径，拼接 BASE_URL 构成完整 URL
INSTITUTIONS = {
    "shzq":       {"name": "上海证券",   "page": "/rank/rate_shzq.htm"},
    "htsec":      {"name": "国泰海通",   "page": "/rank/rate_htsec.htm"},
    "yhzq":       {"name": "银河证券",   "page": "/rank/rate_yhzq.htm"},
    "cmschina":   {"name": "招商证券",   "page": "/rank/rate_cmschina.htm"},
    "morningstar":{"name": "晨星",       "page": "/rank/rate_morningstar.htm"},
    "jajx":       {"name": "济安金信",   "page": "/rank/rate_jajx.htm"},
    "txsec":      {"name": "天相投顾",   "page": "/rank/rate_txsec.htm"},
}

# HTTP 请求超时（秒）
TIMEOUT = 15

# 缓存目录和文件名
# CACHE_DIR 初始为 None，由 cli.py 入口模块初始化为脚本所在目录
CACHE_DIR = None
CACHE_FILE = "fund_cache.json"
