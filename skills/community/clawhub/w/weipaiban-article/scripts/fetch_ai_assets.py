#!/usr/bin/env python3
"""按一个 tag 拉取微排版已发布 AI 素材的全部分页。

    python3 fetch_ai_assets.py --list-tags
    python3 fetch_ai_assets.py --tag 中秋节 --out /tmp/weipaiban-task/asset-pool.json
    python3 fetch_ai_assets.py --self-test

鉴权：Authorization: Bearer <WEIPAIBAN_API_KEY>。
API 源站经 api_base.validate_api_base 限制为 https://weipaiban.cn（含子域）
或本机 localhost / 127.0.0.1 / ::1。不跳过证书校验。
不传 tag 会扫全库，因此 --tag 与 --out 必须成对出现。空 items 仍算成功。
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from api_base import (
    build_ssl_context,
    invalid_api_key_message,
    missing_api_key_message,
    self_test as api_base_self_test,
    validate_api_base,
)

MAX_TAG_LENGTH = 32
PER_PAGE = 48
ITEM_FIELDS = (
    "id",
    "title",
    "description",
    "tags",
    "orientation",
    "transparent",
    "width",
    "height",
    "url",
    "thumb",
)


def env(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    return value if value not in (None, "") else default


def validate_tag(raw: str) -> str:
    tag = raw.strip()
    if not tag or len(tag) > MAX_TAG_LENGTH:
        raise ValueError("tag 必须是 1–32 个字符")
    return tag


def normalize_item(raw: object) -> dict | None:
    if not isinstance(raw, dict):
        return None
    if not raw.get("id") or not raw.get("url"):
        return None
    item = {field: raw.get(field) for field in ITEM_FIELDS}
    item["tags"] = list(item["tags"] or [])
    item["transparent"] = bool(item["transparent"])
    return item


def collect_pages(fetch_page) -> list[dict]:
    """翻到 nextCursor 为空。重复 cursor 视为失败，避免死循环。"""
    items: list[dict] = []
    cursor = None
    seen: set[str] = set()
    while True:
        page = fetch_page(cursor)
        if not isinstance(page, dict):
            raise RuntimeError("素材页不是对象")
        batch = page.get("items") or []
        if not isinstance(batch, list):
            raise RuntimeError("素材页 items 不是数组")
        for raw in batch:
            item = normalize_item(raw)
            if item:
                items.append(item)
        next_cursor = page.get("nextCursor")
        if not next_cursor:
            return items
        if not isinstance(next_cursor, str) or next_cursor in seen:
            raise RuntimeError("素材分页 cursor 无效或重复")
        seen.add(next_cursor)
        cursor = next_cursor


def api_error_message(status: int, payload: object) -> str:
    if isinstance(payload, dict):
        error = payload.get("error")
        if isinstance(error, dict) and error.get("message"):
            return f"HTTP {status} {error['message']}"
    return f"HTTP {status}"


class ApiError(RuntimeError):
    def __init__(self, status: int, payload: object):
        super().__init__(api_error_message(status, payload))
        self.status = status


def request_json(url: str, api_key: str, context: ssl.SSLContext) -> dict:
    request = urllib.request.Request(url, method="GET")
    request.add_header("Authorization", f"Bearer {api_key}")
    request.add_header("Accept", "application/json")

    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(request, timeout=30, context=context) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                payload = {"error": {"message": body, "code": error.code}}
            if error.code == 429 and attempt == 1:
                time.sleep(2)
                continue
            raise ApiError(error.code, payload) from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"请求失败：{error.reason}") from error

        if not isinstance(payload, dict) or "data" not in payload:
            raise RuntimeError("响应缺少 data")
        data = payload["data"]
        if not isinstance(data, dict):
            raise RuntimeError("响应 data 不是对象")
        return data
    raise RuntimeError("请求未完成")


def list_tags(api_base: str, api_key: str, context: ssl.SSLContext) -> dict:
    url = f"{api_base.rstrip('/')}/api/v1/ai-assets/tags"
    return request_json(url, api_key, context)


def fetch_tag_pool(
    api_base: str,
    api_key: str,
    tag: str,
    context: ssl.SSLContext,
) -> dict:
    def fetch_page(cursor: str | None) -> dict:
        query = {"tag": tag, "per_page": str(PER_PAGE)}
        if cursor:
            query["cursor"] = cursor
        url = (
            f"{api_base.rstrip('/')}/api/v1/ai-assets?"
            + urllib.parse.urlencode(query)
        )
        return request_json(url, api_key, context)

    return {"tag": tag, "items": collect_pages(fetch_page)}


def self_test() -> int:
    pages = [
        {"items": [{"id": "a", "url": "https://svg-cdn.creatby.com/a.png", "title": "甲", "orientation": "background", "transparent": False, "width": 10, "height": 30, "extra": 1}], "nextCursor": "c1"},
        {"items": [{"id": "b", "url": "https://svg-cdn.creatby.com/b.png", "transparent": True}], "nextCursor": None},
    ]

    def fetch_page(cursor: str | None) -> dict:
        if cursor is None:
            return pages[0]
        if cursor == "c1":
            return pages[1]
        raise AssertionError(cursor)

    items = collect_pages(fetch_page)
    assert [item["id"] for item in items] == ["a", "b"]
    assert "extra" not in items[0]
    assert items[1]["transparent"] is True
    assert collect_pages(lambda _cursor: {"items": [], "nextCursor": None}) == []

    def looping(cursor: str | None) -> dict:
        return {"items": [], "nextCursor": "again"}

    try:
        collect_pages(looping)
    except RuntimeError:
        pass
    else:
        raise AssertionError("重复 cursor 应失败")

    validate_tag("中秋节")
    for bad in ("", "   ", "x" * 33):
        try:
            validate_tag(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(bad)

    assert normalize_item({"id": "a"}) is None
    api_base_self_test()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="按 tag 拉取全部已发布 AI 素材")
    parser.add_argument("--list-tags", action="store_true", help="打印推荐标签分组")
    parser.add_argument("--tag", help="单个标签；会翻完所有分页")
    parser.add_argument("--out", help="把 asset-pool.json 写到这个路径")
    parser.add_argument("--api-base", help="覆盖 WEIPAIBAN_API_BASE")
    parser.add_argument("--self-test", action="store_true", help="用本地分页夹具自测，不访问网络")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    if args.list_tags == bool(args.tag):
        print("错误：请只使用 --list-tags，或同时使用 --tag 与 --out", file=sys.stderr)
        return 2
    if args.tag and not args.out:
        print("错误：--tag 必须搭配 --out", file=sys.stderr)
        return 2

    api_key = env("WEIPAIBAN_API_KEY")
    if not api_key:
        print(missing_api_key_message(), file=sys.stderr)
        return 2

    try:
        tag = validate_tag(args.tag) if args.tag else ""
    except ValueError as error:
        print(f"错误：{error}", file=sys.stderr)
        return 2

    try:
        api_base = validate_api_base(
            args.api_base or env("WEIPAIBAN_API_BASE", "https://weipaiban.cn") or ""
        )
    except ValueError as error:
        print(f"错误：{error}", file=sys.stderr)
        return 2
    context = build_ssl_context()
    try:
        if args.list_tags:
            payload = list_tags(api_base, api_key, context)
        else:
            payload = fetch_tag_pool(api_base, api_key, tag, context)
    except ApiError as error:
        print(f"错误：{error}", file=sys.stderr)
        if error.status == 401:
            print(invalid_api_key_message(), file=sys.stderr)
        elif error.status == 403:
            print("提示：该用户未订阅且不是 developer。", file=sys.stderr)
        elif error.status == 429:
            print("提示：限流仍未恢复，请稍后重试。", file=sys.stderr)
        return 1
    except (RuntimeError, json.JSONDecodeError, OSError) as error:
        print(f"错误：{error}", file=sys.stderr)
        return 1

    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.list_tags:
        print(text)
        return 0

    try:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    except OSError as error:
        print(f"错误：无法写入 {args.out}：{error}", file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, "tag": tag, "count": len(payload["items"]), "out": args.out}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
