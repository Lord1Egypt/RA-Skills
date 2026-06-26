"""
小红书搜索采集器
通过搜索引擎获取小红书上与关键词相关的笔记
小红书没有公开API，使用 web_search 方式获取
"""

import json
import re
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta, timezone


TIMEOUT = 15
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def _search_via_web(keyword: str, hours: int = 24) -> list:
    """
    通过搜索引擎获取小红书笔记
    使用 DuckDuckGo HTML 搜索作为备选方案
    """
    items = []

    # 方式1: 尝试通过 Bing 搜索
    try:
        query = f"site:xiaohongshu.com {keyword}"
        params = {
            "q": query,
            "count": 20,
        }
        url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode(params)

        headers = {
            "User-Agent": UA,
            "Accept": "text/html",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

        req = urllib.request.Request(url, headers=headers)

        proxy = _get_proxy()
        if proxy:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({
                "http": proxy,
                "https": proxy,
            }))
        else:
            opener = urllib.request.build_opener()

        with opener.open(req, timeout=TIMEOUT) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            items = _parse_ddg_results(html)
    except Exception:
        pass

    return items


def _get_proxy():
    """获取代理配置"""
    import os
    return os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY")


def _parse_ddg_results(html: str) -> list:
    """解析 DuckDuckGo 搜索结果"""
    items = []

    # 匹配搜索结果中的链接和标题
    # DDG HTML 结果的 pattern
    pattern = r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>'
    results = re.findall(pattern, html, re.DOTALL)

    # 也匹配通用链接模式
    link_pattern = r'href="(https?://[^"]*xiaohongshu\.com/[^"]*)"'
    links = re.findall(link_pattern, html)

    seen_urls = set()

    for href, title_html in results:
        # 清理标题
        title = re.sub(r'<[^>]+>', '', title_html).strip()
        if not title:
            continue

        # 检查是否是小红书链接
        xhs_match = re.search(r'(https?://[^"]*xiaohongshu\.com/[^"]*)', href)
        if not xhs_match:
            # DDG 的链接可能被编码在 uddg 参数中
            uddg_match = re.search(r'uddg=([^&"]+)', href)
            if uddg_match:
                url = urllib.parse.unquote(uddg_match.group(1))
            else:
                continue
        else:
            url = xhs_match.group(1)

        if url in seen_urls:
            continue
        seen_urls.add(url)

        # 提取作者（从URL或标题中）
        author = ""
        author_match = re.search(r'/user/profile/([^/?]+)', url)
        if author_match:
            author = author_match.group(1)

        items.append({
            "title": title,
            "url": url,
            "author": author,
            "publish_time": "",
            "description": "",
            "type": "note",
        })

    # 补充从通用链接中提取的结果
    for link in links:
        if link not in seen_urls:
            seen_urls.add(link)
            # 从URL提取笔记ID作为标题
            note_match = re.search(r'/explore/([^/?]+)', link)
            title = f"小红书笔记 ({note_match.group(1)[:8]}...)" if note_match else "小红书笔记"
            items.append({
                "title": title,
                "url": link,
                "author": "",
                "publish_time": "",
                "description": "",
                "type": "note",
            })

    return items


def _generate_mock_data(keyword: str, hours: int) -> list:
    """
    生成模拟数据用于测试
    实际部署时替换为真实 API 调用
    """
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)

    mock_items = [
        {
            "title": f"{keyword} 使用体验分享 - 超好用的AI工具",
            "url": "https://www.xiaohongshu.com/explore/abc123def",
            "author": "科技小达人",
            "publish_time": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "description": f"最近发现了{keyword}这个项目，功能真的很强大，适合开发者使用...",
            "type": "note",
        },
        {
            "title": f"{keyword} 安装配置教程，小白也能学会",
            "url": "https://www.xiaohongshu.com/explore/def456ghi",
            "author": "程序员日记",
            "publish_time": (now - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
            "description": f"手把手教你配置{keyword}，从零开始搭建AI助手环境...",
            "type": "note",
        },
    ]

    return mock_items


def collect(keyword: str = "OpenClaw", hours: int = 24) -> dict:
    """
    搜索小红书上与关键词相关的最新笔记

    Returns:
        {
            "source": "xiaohongshu",
            "items": [{"title", "url", "author", "publish_time", "description"}],
            "total": int,
            "query_time": "YYYY-MM-DD HH:MM"
        }
    """
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)

    items = []
    error = None

    try:
        # 尝试通过搜索引擎获取
        items = _search_via_web(keyword, hours)

        # 如果搜索引擎获取失败，使用模拟数据
        if not items:
            items = _generate_mock_data(keyword, hours)
            error = "搜索引擎未返回结果，使用模拟数据（小红书无公开API）"

    except Exception as e:
        # 任何异常都回退到模拟数据
        items = _generate_mock_data(keyword, hours)
        error = f"采集失败: {str(e)}，使用模拟数据"

    result = {
        "source": "xiaohongshu",
        "items": items,
        "total": len(items),
        "query_time": now.strftime("%Y-%m-%d %H:%M"),
    }
    if error:
        result["error"] = error

    return result


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    kw = sys.argv[1] if len(sys.argv) > 1 else "OpenClaw"
    h = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    print(f"[xiaohongshu] Searching '{kw}' (last {h}h)...")
    result = collect(kw, h)
    print(json.dumps(result, ensure_ascii=False, indent=2))
