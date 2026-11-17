#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
证券之星科技频道 — 大模型调用排行榜配置模块。

定义排行榜页面地址、周期（日榜/周榜）配置与别名映射，
以及全局超时时间和 HTTP 请求头。
"""

# 证券之星科技频道首页（排行榜数据服务端直出，无独立 API）
BASE_URL = "https://tech.stockstar.com/"

# 周期配置
# key：内部唯一标识（短英文，用于 JSON 键名）
# name：中文展示名，最终输出给用户
PERIODS = {
    "day": {"name": "日榜"},
    "week": {"name": "周榜"},
}

# 周期别名映射（CLI 参数 → 内部 key）
# 覆盖中英文各种问法，未知别名统一指向 "all"
PERIOD_ALIAS = {
    "day": "day", "today": "day", "日": "day", "今日": "day", "今天": "day", "日榜": "day",
    "week": "week", "this-week": "week", "周": "week", "本周": "week", "这周": "week", "周榜": "week",
    "all": "all", "全部": "all", "both": "all", "双榜": "all",
}

# 趋势箭头颜色 → 方向
# 红色箭头表示 Tokens 环比上升，绿色箭头表示下降
# 统一小写存储，解析时对页面取到的 fill 值做 lower() 归一化
TREND_UP = "#FF0000"
TREND_DOWN = "#228c02"
TREND_COLORS = {TREND_UP.lower(): "up", TREND_DOWN.lower(): "down"}

# 厂商 slug → 展示名（仅用于终端文本表格，JSON 中 vendor 保持页面原始 slug）
# 中国厂商显示中文名，海外厂商保留英文品牌；未知 slug 由 get() 兜底返回原文
VENDOR_NAMES = {
    "deepseek": "深度求索",
    "tencent": "腾讯",
    "xiaomi": "小米",
    "z-ai": "智谱（Z.ai）",
    "moonshotai": "月之暗面（Kimi）",
    "stepfun": "阶跃星辰",
    "minimax": "MiniMax",
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "google": "Google",
    "nvidia": "NVIDIA",
    "poolside": "Poolside",
}

# HTTP 请求超时（秒）
TIMEOUT = 15

# HTTP 请求头：模拟浏览器 + gzip 压缩传输
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip",
}