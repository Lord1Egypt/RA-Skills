"""
Bilibili Search Collector
搜索B站指定关键词的最新视频（默认24小时内）。
"""

import json
import os
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta, timezone


# ---- Config ----
BILIBILI_SEARCH_API = "https://api.bilibili.com/x/web-interface/search/type"
TIMEOUT = 15  # seconds
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def _make_request(url: str, params: dict) -> dict:
    """发起 HTTP GET 请求，支持代理，返回 JSON dict。"""
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"

    headers = {
        "User-Agent": UA,
        "Referer": "https://search.bilibili.com",
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "buvid3=placeholder; b_nut=1",
    }

    req = urllib.request.Request(full_url, headers=headers)

    # 支持代理
    proxy = os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY")
    if proxy:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({
            "http": proxy,
            "https": proxy,
        }))
    else:
        opener = urllib.request.build_opener()

    with opener.open(req, timeout=TIMEOUT) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw)


def _ts_to_str(ts: int) -> str:
    """Unix timestamp -> 'YYYY-MM-DD HH:MM' (Asia/Shanghai)"""
    tz = timezone(timedelta(hours=8))
    return datetime.fromtimestamp(ts, tz=tz).strftime("%Y-%m-%d %H:%M")


def collect(keyword: str = "OpenClaw", hours: int = 24) -> dict:
    """
    搜索B站上与 keyword 相关的最新视频（最近 hours 小时内）。

    Returns:
        {
            "source": "bilibili",
            "items": [{"title", "url", "author", "publish_time", "views", "description"}],
            "total": int,
            "query_time": "YYYY-MM-DD HH:MM"
        }
    """
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    cutoff = now - timedelta(hours=hours)

    items = []
    page = 1
    max_pages = 5  # 安全上限，防止死循环

    try:
        while page <= max_pages:
            params = {
                "search_type": "video",
                "keyword": keyword,
                "order": "pubdate",
                "page": page,
                "pagesize": 20,
            }

            data = _make_request(BILIBILI_SEARCH_API, params)

            if data.get("code") != 0:
                # API 返回错误（常见：-412 被风控）
                msg = data.get("message", "unknown error")
                if page == 1:
                    return {
                        "source": "bilibili",
                        "items": [],
                        "total": 0,
                        "query_time": now.strftime("%Y-%m-%d %H:%M"),
                        "error": f"API error: {msg}",
                    }
                break

            result = data.get("data", {})
            videos = result.get("result", [])
            numPages = result.get("numPages", 1)

            if not videos:
                break

            reached_old = False
            for v in videos:
                pubdate = v.get("pubdate", v.get("senddate", 0))
                if isinstance(pubdate, str):
                    try:
                        pubdate = int(pubdate)
                    except ValueError:
                        pubdate = 0

                pub_dt = datetime.fromtimestamp(pubdate, tz=tz) if pubdate else None

                # 超出时间范围就停止
                if pub_dt and pub_dt < cutoff:
                    reached_old = True
                    continue

                # 构造BV号链接
                bvid = v.get("bvid", "")
                url = f"https://www.bilibili.com/video/{bvid}" if bvid else v.get("arcurl", "")

                # 清理标题HTML标签
                title = v.get("title", "")
                title = title.replace("<em class=\"keyword\">", "").replace("</em>", "")
                title = title.replace("&amp;", "&").replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">")

                items.append({
                    "title": title,
                    "url": url,
                    "author": v.get("author", ""),
                    "publish_time": _ts_to_str(pubdate) if pubdate else "",
                    "views": v.get("play", 0),
                    "description": v.get("description", "")[:200],
                })

            if reached_old or page >= numPages:
                break

            page += 1
            time.sleep(0.5)  # 限流保护

    except urllib.error.HTTPError as e:
        error_msg = f"HTTP {e.code}: {e.reason}"
        if e.code == 412:
            error_msg = "被B站风控拦截(412)，请稍后重试或更换IP"
        return {
            "source": "bilibili",
            "items": items,
            "total": len(items),
            "query_time": now.strftime("%Y-%m-%d %H:%M"),
            "error": error_msg,
        }
    except urllib.error.URLError as e:
        return {
            "source": "bilibili",
            "items": items,
            "total": len(items),
            "query_time": now.strftime("%Y-%m-%d %H:%M"),
            "error": f"网络错误: {e.reason}",
        }
    except TimeoutError:
        return {
            "source": "bilibili",
            "items": items,
            "total": len(items),
            "query_time": now.strftime("%Y-%m-%d %H:%M"),
            "error": f"请求超时({TIMEOUT}s)",
        }
    except Exception as e:
        return {
            "source": "bilibili",
            "items": items,
            "total": len(items),
            "query_time": now.strftime("%Y-%m-%d %H:%M"),
            "error": f"未知错误: {str(e)}",
        }

    return {
        "source": "bilibili",
        "items": items,
        "total": len(items),
        "query_time": now.strftime("%Y-%m-%d %H:%M"),
    }


if __name__ == "__main__":
    import sys, io
    # Windows 终端默认 GBK，强制 UTF-8 输出
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    kw = sys.argv[1] if len(sys.argv) > 1 else "OpenClaw"
    h = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    print(f"[bilibili] Searching '{kw}' (last {h}h)...")
    result = collect(kw, h)
    print(json.dumps(result, ensure_ascii=False, indent=2))
