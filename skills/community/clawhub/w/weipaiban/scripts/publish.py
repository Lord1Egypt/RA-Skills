#!/usr/bin/env python3
"""把交互 HTML 方言发布为当前 API Key 用户名下的微排版作品。

创建：POST {WEIPAIBAN_API_BASE}/api/v1/vectors/svg
修改：PUT  {WEIPAIBAN_API_BASE}/api/v1/vectors/{id}/svg（--work-id）

服务端 buildVectorFromSvg 解析后写入作品。不是管理员样式上架。
成功时同时返回编辑链接 `url` 与临时预览链接 `preview`（/links/{previewId}，约 6 小时）。

鉴权：Authorization: Bearer <sk-...>，token 取自 WEIPAIBAN_API_KEY。
key 对应用户须为订阅用户或 developer，不要求 admin。
API 源站经 api_base.validate_api_base 限制为 https://weipaiban.cn（含子域）
或本机 localhost / 127.0.0.1 / ::1。不跳过证书校验。

用法：

    python3 publish.py --body-file ./work.html --title "春季开学刊"
    python3 publish.py --work-id 665f... --body-file ./work.html --title "春季开学刊"
    python3 publish.py --dry-run --body-file ./work.html --title x
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

from api_base import (
    build_ssl_context,
    invalid_api_key_message,
    missing_api_key_message,
    validate_api_base,
)

MAX_HTML_LENGTH = 512 * 1024


def env(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    return value if value not in (None, "") else default


def build_payload(args: argparse.Namespace) -> dict:
    if args.payload_file:
        with open(args.payload_file, "r", encoding="utf-8") as handle:
            return json.load(handle)

    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as handle:
            html = handle.read()
    else:
        html = args.html or ""

    payload: dict = {"html": html}
    if args.title:
        payload["title"] = args.title
    if args.description is not None:
        payload["description"] = args.description
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="发布交互 HTML 方言为用户作品")
    parser.add_argument("--title", help="作品标题（缺省时服务端记为「未命名作品」）")
    parser.add_argument("--description", help="作品描述")
    parser.add_argument("--html", help="HTML 方言正文")
    parser.add_argument("--body-file", help="HTML 文件路径（优先于 --html）")
    parser.add_argument("--work-id", help="已有作品 ID；提供则 PUT 整份替换")
    parser.add_argument("--api-base", help="覆盖 WEIPAIBAN_API_BASE")
    parser.add_argument("--payload-file", help="直接读取完整 payload JSON")
    parser.add_argument("--dry-run", action="store_true", help="只打印 payload，不发送请求")
    args = parser.parse_args()

    try:
        api_base = validate_api_base(
            args.api_base or env("WEIPAIBAN_API_BASE", "https://weipaiban.cn") or ""
        )
    except ValueError as error:
        print(f"错误：{error}", file=sys.stderr)
        return 2
    api_key = env("WEIPAIBAN_API_KEY")

    try:
        payload = build_payload(args)
    except (OSError, json.JSONDecodeError) as error:
        print(f"错误：无法读取输入：{error}", file=sys.stderr)
        return 2

    html = payload.get("html") or ""
    if not str(html).strip():
        print("错误：缺少 HTML 正文（--body-file / --html / --payload-file）", file=sys.stderr)
        return 2
    if len(html) > MAX_HTML_LENGTH:
        print(
            f"错误：HTML 长度 {len(html)} 超过上限 {MAX_HTML_LENGTH}（512KB）。"
            "图片请使用 CDN 链接而非 base64。",
            file=sys.stderr,
        )
        return 2

    if args.work_id:
        url = f"{api_base.rstrip('/')}/api/v1/vectors/{args.work_id}/svg"
        method = "PUT"
    else:
        url = f"{api_base.rstrip('/')}/api/v1/vectors/svg"
        method = "POST"

    if args.dry_run:
        print(
            json.dumps(
                {"url": url, "method": method, "payload": payload},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if not api_key:
        print(missing_api_key_message(), file=sys.stderr)
        return 2

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Content-Type", "application/json;charset=UTF-8")
    request.add_header("Accept", "application/json, text/plain, */*")
    request.add_header("Authorization", f"Bearer {api_key}")

    context = build_ssl_context()
    try:
        with urllib.request.urlopen(request, timeout=30, context=context) as resp:
            status = resp.status
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body_text = error.read().decode("utf-8", errors="replace")
        print(f"请求失败：HTTP {error.code} {error.reason}\n{body_text}", file=sys.stderr)
        if error.code == 401:
            print(invalid_api_key_message(), file=sys.stderr)
        elif error.code == 403:
            print(
                "提示：该用户未订阅且不是 developer（本接口为 /api/v1，不要求 admin）。",
                file=sys.stderr,
            )
        elif error.code == 402:
            print("提示：402 作品容量已满，请清理作品或升级年卡。", file=sys.stderr)
        elif error.code == 404:
            print(
                "提示：404 表示作品不存在、不属于当前用户，或已发布"
                "（仅未发布作品可整份替换）。",
                file=sys.stderr,
            )
        elif error.code == 429:
            print("提示：429 触发限流，请稍后重试。", file=sys.stderr)
        elif error.code == 400:
            print(
                "提示：400 表示 HTML 方言解析失败。对照 references/dialect.md 和所选 format："
                "根节点、overlay/scroller 壳、图片三件套、交互组件结构、"
                "animationGroup 位置以及 300 元素上限。",
                file=sys.stderr,
            )
        return 1
    except urllib.error.URLError as error:
        print(f"请求失败：{error.reason}", file=sys.stderr)
        return 1

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        print(f"响应非 JSON：\n{raw}", file=sys.stderr)
        return 1

    vector = (result.get("data") or {}) if isinstance(result, dict) else {}
    ok_status = 201 if method == "POST" else 200
    if status == ok_status and vector.get("id"):
        origin = api_base.rstrip("/")
        work_id = vector.get("id")
        preview_id = vector.get("previewId")
        print(
            json.dumps(
                {
                    "ok": True,
                    "id": work_id,
                    "title": vector.get("title"),
                    "url": f"{origin}/vectors/{work_id}",
                    "preview": f"{origin}/links/{preview_id}" if preview_id else None,
                    "raw": result,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    print(f"发布失败：HTTP {status} {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
