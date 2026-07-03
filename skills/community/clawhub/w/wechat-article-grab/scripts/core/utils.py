"""
core/utils.py - Common utility functions
"""

import subprocess
import re


def resolve_article_url(title: str) -> str:
    """
    根据文章标题获取微信文章的干净链接（不含 sn token）。

    使用 curl 多 UA 策略搜索微信文章，返回第一个匹配的 clean mid URL。

    Args:
        title: 文章标题

    Returns:
        str: 干净的微信文章链接，如 'https://mp.weixin.qq.com/s/xxx'
             如果搜索失败或未找到，返回空字符串 ''
    """
    # 微信搜索 API
    search_url = "https://weixin.sogou.com/weixin"
    query = f"site:mp.weixin.qq.com {title}"

    strategies = [
        {
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "referer": "https://weixin.sogou.com/",
        },
        {
            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "referer": "https://www.sogou.com/",
        },
    ]

    for strat in strategies:
        try:
            cmd = [
                "curl", "-s", "-L",
                "-G",  # GET request
                "--data-urlencode", f"query={query}",
                "-A", strat["ua"],
                "-H", f"Referer: {strat['referer']}",
                "--connect-timeout", "15",
                "--max-time", "30",
                search_url
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
            html = result.stdout

            if not html or len(html) < 500:
                continue
            if "访问过于频繁" in html or "验证码" in html:
                continue

            # 从搜索结果中提取微信文章链接
            # 匹配 patterns: mp.weixin.qq.com/s/xxx 或 url 包含 biz 和 mid
            patterns = [
                r'(https?://mp\.weixin\.qq\.com/s/[a-zA-Z0-9]+)',
                r'url\s*:\s*[\'"](https?://mp\.weixin\.qq\.com/s/[^\s\'"]+)',
                r'(https?://mp\.weixin\.qq\.com/s\?[^"\'>\s]+)',
            ]

            for pattern in patterns:
                matches = re.findall(pattern, html)
                for match in matches:
                    url = match.strip()
                    # 构建干净链接：提取 mid 部分
                    if '/s/' in url:
                        mid_match = re.search(r'/s/([a-zA-Z0-9]+)', url)
                        if mid_match:
                            mid = mid_match.group(1)
                            # 验证是否看起来像有效的 mid (字母数字组合)
                            if len(mid) >= 10:
                                return f'https://mp.weixin.qq.com/s/{mid}'
        except Exception:
            continue

    return ''


def parse_count(value):
    """
    Parse count value, handling 'w' suffix for 万.

    Args:
        value: int, float, or str representation of a number.
               Supports formats like "17w+", "1.5w", "12,345"

    Returns:
        int: Parsed count value, 0 if parsing fails
    """
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    value_str = str(value).replace('+', '').replace(',', '').strip()
    if 'w' in value_str.lower():
        value_str = value_str.lower().replace('w', '')
        try:
            return int(float(value_str) * 10000)
        except Exception:
            return 0
    try:
        return int(float(value_str))
    except Exception:
        return 0


def format_number(value: int) -> str:
    """
    Format number to Chinese format with 万/亿 suffix.

    Args:
        value: int number to format

    Returns:
        str: Formatted string (e.g., "1万", "150万", "1亿")
    """
    if value < 10000:
        return str(value)
    if value < 100000000:
        wan = value // 10000
        remainder = value % 10000
        if remainder == 0:
            return f"{wan}万"
        return f"{value / 10000:.1f}万"
    yi = value // 100000000
    remainder = value % 100000000
    if remainder == 0:
        return f"{yi}亿"
    return f"{value / 100000000:.1f}亿"