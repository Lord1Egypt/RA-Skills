#!/usr/bin/env python3
"""
小红书爬虫配置文件
整合 Cookie 管理和爬虫配置
"""

import os
from pathlib import Path

# ==================== 基础路径配置 ====================

# 项目根目录
BASE_DIR = Path(__file__).parent

# Chrome 用户数据目录（用于保存 Cookie）
XHS_USER_DATA_DIR = Path.home() / "xhs_chrome_profile"

# Cookie 文件路径（从浏览器提取后保存到这里）
COOKIE_FILE = BASE_DIR / "cookie.txt"

# ==================== 浏览器配置 ====================

BROWSER_VIEWPORT_WIDTH = 1280
BROWSER_VIEWPORT_HEIGHT = 800
BROWSER_HEADLESS = True  # 检测状态时是否无头模式

# ==================== 小红书 API 配置 ====================

# 小红书搜索 API
XHS_SEARCH_URL = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
XHS_NOTE_DETAIL_URL = "https://edith.xiaohongshu.com/api/sns/web/v1/feed"

# 基础请求头（不含 Cookie）
BASE_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "dnt": "1",
    "origin": "https://www.xiaohongshu.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.xiaohongshu.com/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36 Edg/143.0.0"
}

# ==================== 爬虫配置 ====================

# 笔记类型映射
NOTE_TYPE_DICT = {
    "全部": 0,
    "视频": 1,
    "图文": 2
}

# 排序方式映射
SORT_TYPE_DICT = {
    "综合": "general",
    "最新": "time_descending",
    "最多点赞": "popularity_descending",
    "最多评论": "comment_descending",
    "最多收藏": "collect_descending"
}

# 默认爬取数量
DEFAULT_MAX_NOTES = 5

# 请求间隔（秒）
REQUEST_DELAY_MIN = 2.0  # 增加最小间隔，防止风控
REQUEST_DELAY_MAX = 5.0  # 增加最大间隔

# 检查超时时间（秒）
CHECK_TIMEOUT = 30

# 防风控配置
ANTI_DETECT = {
    "max_checks_per_hour": 10,  # 每小时最多检查Cookie次数
    "min_check_interval": 300,   # 两次检查间隔至少5分钟
    "cooldown_after_461": 3600,  # 遇到461错误后冷却1小时
}

# ==================== 飞书应用配置 ====================

# 飞书企业自建应用凭证
FEISHU_APP_ID = "cli_a924d921ce7a9cbd"
FEISHU_APP_SECRET = "5QG92Lp8kvhAkgpPJTd57fIxshnCebEt"

# ==================== 日志配置 ====================

LOG_FILE = BASE_DIR / "logs" / "xhs_crawler.log"
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
