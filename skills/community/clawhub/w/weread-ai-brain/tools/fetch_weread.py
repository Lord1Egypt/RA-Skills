#!/usr/bin/env python3
"""Fetch explicitly approved data from the fixed WeRead API gateway."""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from typing import Any


GATEWAY_URL = "https://i.weread.qq.com/api/agent/gateway"
SKILL_VERSION = "2.0.0"

COMMANDS: dict[str, tuple[str, str, str]] = {
    "shelf": ("/shelf/sync", "书架列表与用户昵称", "📚 获取书架列表..."),
    "stats": ("/readdata/summary", "阅读统计", "📊 获取阅读统计..."),
    "bookmarks": ("/book/bookmarklist", "指定书籍的划线笔记", "✍️ 获取指定书籍的划线笔记..."),
    "reviews": ("/review/list/mine", "指定书籍的个人想法与评论", "💬 获取指定书籍的想法..."),
    "bookinfo": ("/book/info", "指定书籍的书目信息", "📖 获取指定书籍详情..."),
    "progress": ("/book/getprogress", "指定书籍的阅读进度", "📈 获取指定书籍阅读进度..."),
    "search": ("/store/search", "按关键词搜索书籍", "🔎 搜索书籍..."),
}
ALIASES = {
    "books": "shelf",
    "user": "shelf",
    "summary": "stats",
    "notes": "bookmarks",
    "thoughts": "reviews",
    "detail": "bookinfo",
    "all": "dashboard",
}
BOOK_COMMANDS = {"bookmarks", "reviews", "bookinfo", "progress"}
VALUE_COMMANDS = BOOK_COMMANDS | {"search"}


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="只向微信读书官方网关发送经用户确认的数据请求。"
    )
    parser.add_argument(
        "--confirm-private-data",
        action="store_true",
        help="确认已向用户说明目标接口和数据范围并取得同意。",
    )
    parser.add_argument("command", choices=[*COMMANDS, *ALIASES, "dashboard"])
    parser.add_argument(
        "value",
        nargs="?",
        help="书籍命令传 bookId；search 命令传搜索关键词。",
    )
    return parser.parse_args()


def require_api_key() -> str:
    api_key = os.environ.get("WEREAD_API_KEY", "")
    if not api_key:
        raise ValueError("未设置 WEREAD_API_KEY 环境变量。")
    if not api_key.startswith("wrk-"):
        raise ValueError("WEREAD_API_KEY 必须以 wrk- 开头。")
    return api_key


def build_opener() -> urllib.request.OpenerDirector:
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        NoRedirectHandler(),
        urllib.request.HTTPSHandler(context=context),
    )


def fetch_gateway(api_key: str, api_name: str, **parameters: str) -> Any:
    payload = {"api_name": api_name, "skill_version": SKILL_VERSION, **parameters}
    request = urllib.request.Request(
        GATEWAY_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with build_opener().open(request, timeout=30) as response:
        if response.geturl() != GATEWAY_URL:
            raise RuntimeError("安全停止：请求发生了非预期重定向。")
        return json.loads(response.read().decode("utf-8"))


def fetch_command(api_key: str, command: str, book_id: str | None = None) -> Any:
    api_name = COMMANDS[command][0]
    if command in BOOK_COMMANDS:
        parameters = {"bookId": book_id}
    elif command == "search":
        parameters = {"keyword": book_id, "count": "10"}
    else:
        parameters = {}
    result = fetch_gateway(api_key, api_name, **parameters)
    if command == "stats" and isinstance(result, dict) and result.get("errcode"):
        return fetch_gateway(api_key, "/readdata/detail", mode="overall")
    return result


def main() -> int:
    args = parse_args()
    command = ALIASES.get(args.command, args.command)
    if command in VALUE_COMMANDS and not args.value:
        required_value = "搜索关键词" if command == "search" else "bookId"
        print(f"错误：{command} 命令需要 {required_value}。", file=sys.stderr)
        return 2

    scope = "书架列表、用户昵称与阅读统计" if command == "dashboard" else COMMANDS[command][1]
    print("🔒 隐私提示：即将访问微信读书官方统一网关", file=sys.stderr)
    print(f"   目标：{GATEWAY_URL}", file=sys.stderr)
    print(f"   本次范围：{scope}", file=sys.stderr)
    print("   凭据：WEREAD_API_KEY 仅作为 Bearer Token 发往上述官方网关", file=sys.stderr)
    if not args.confirm_private_data:
        print("请求已停止：请先取得用户明确同意，再添加 --confirm-private-data。", file=sys.stderr)
        return 2

    try:
        api_key = require_api_key()
        if command == "dashboard":
            result = {
                "shelf": fetch_command(api_key, "shelf"),
                "stats": fetch_command(api_key, "stats"),
            }
        else:
            print(COMMANDS[command][2], file=sys.stderr)
            result = fetch_command(api_key, command, args.value)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, RuntimeError, urllib.error.URLError, json.JSONDecodeError) as error:
        print(f"请求失败：{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
