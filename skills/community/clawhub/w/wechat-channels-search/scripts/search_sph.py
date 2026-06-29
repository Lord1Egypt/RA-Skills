#!/usr/bin/env python3
"""
视频号作品搜索脚本
调用 Redfox API 搜索视频号热门作品数据
用法: python3 search_sph.py "<关键词>" [--buffer "<cookiesBuffer>"]
"""

import sys
import os
import json
import urllib.request
import urllib.error

API_URL = "https://redfox.hk/story/api/sph/ability/searchWork"
SOURCE = "视频号搜作品-ClawHub"


def get_api_key() -> str:
    """从环境变量获取 API Key"""
    for key_name in ["REDFOX_API_KEY"]:
        val = os.environ.get(key_name)
        if val:
            return val
    print("[error] 未找到环境变量 REDFOX_API_KEY，请确认已设置 API Key", file=sys.stderr)
    sys.exit(1)


from datetime import datetime


def format_number(n) -> str:
    """格式化数字: 12345 -> 1.2w"""
    if n is None:
        return "0"
    try:
        n = int(n)
    except (ValueError, TypeError):
        return str(n)
    if n >= 10000:
        return f"{n/10000:.1f}w"
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)


def ts_to_str(ts) -> str:
    """Unix 时间戳字符串 -> MM-DD HH:MM"""
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(int(ts)).strftime("%m-%d %H:%M")
    except (ValueError, OSError):
        return str(ts)


def parse_like_num(raw) -> int:
    """解析 likeNum，支持 '1.2万'、'12345'、None 等格式"""
    if raw is None:
        return 0
    if isinstance(raw, (int, float)):
        return int(raw)
    s = str(raw).strip()
    if not s:
        return 0
    # 处理中文万
    if "万" in s:
        try:
            return int(float(s.replace("万", "")) * 10000)
        except (ValueError, TypeError):
            return 0
    try:
        return int(s)
    except (ValueError, TypeError):
        return 0


def format_articles(raw_list: list) -> list:
    """将 API 返回的 data.list 转换为统一格式

    API 返回结构：data.list[] 每项包含 dataId 和嵌套 data 对象
    data 对象字段：description, nickname, likeNum, publishTime, image, duration, videoUrl, exportId, opusId
    """
    items = []
    for item in raw_list:
        inner = item.get("data") or {}
        title = (inner.get("description") or "").strip()
        like_raw = inner.get("likeNum")
        like_count = parse_like_num(like_raw)
        like_display = str(like_raw) if like_raw is not None else "0"
        items.append({
            "title": title,
            "author": (inner.get("nickname") or "").strip(),
            "likeCount": like_count,
            "likeCountFmt": format_number(like_raw),
            "likeDisplay": like_display,
            "coverUrl": inner.get("image") or "",
            "videoUrl": inner.get("videoUrl") or "",
            "duration": inner.get("duration") or "",
            "publishTime": ts_to_str(inner.get("publishTime")),
            "publishTimestamp": inner.get("publishTime") or "",
            "opusId": inner.get("opusId") or "",
            "exportId": inner.get("exportId") or "",
        })
    return items


def search(keyword: str, buffer: str = "", search_type: str = "0") -> dict:
    """调用视频号搜索接口，返回完整数据"""
    api_key = get_api_key()

    payload_dict = {
        "key": keyword,
        "buffer": buffer,
        "searchType": search_type,
        "source": SOURCE,
    }
    payload = json.dumps(payload_dict).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": api_key,
            "User-Agent": "QoderWork/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[error] HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[error] 网络请求失败: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"[error] 数据解析异常: {e}", file=sys.stderr)
        sys.exit(1)

    code = result.get("code")
    if code not in (200, 2000):
        print(f"[error] 接口返回错误: code={code}, msg={result.get('msg', '未知')}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data") or {}

    # API 返回结构：data.list[] 每项含 dataId + 嵌套 data 对象
    raw_list = data.get("list") or []
    cookies_buffer = data.get("cookiesBuffer") or ""
    offset = data.get("offset") or 0

    articles = format_articles(raw_list)

    # 翻页判断：cookiesBuffer 非空即可
    has_more = bool(cookies_buffer)

    return {
        "articles": articles,
        "totalCount": len(articles),
        "offset": offset,
        "hasMore": has_more,
        "cookiesBuffer": cookies_buffer,
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="视频号作品搜索脚本")
    parser.add_argument("keyword", help="搜索关键词（多个关键词用逗号分隔）")
    parser.add_argument("--buffer", "-b", default="", help="翻页 buffer，传入上一页返回的 cookiesBuffer")
    parser.add_argument("--sort", "-s", default="0", choices=["0", "1"], help="排序方式：0=不限（默认），1=最新")
    args = parser.parse_args()

    keyword = args.keyword.strip()
    if not keyword:
        print("[error] 关键词不能为空", file=sys.stderr)
        sys.exit(1)

    buffer = args.buffer.strip()
    sort_order = args.sort

    result = search(keyword, buffer=buffer, search_type=sort_order)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
