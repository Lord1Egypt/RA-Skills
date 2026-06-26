#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""doctor — 医生与排班查询。"""

from __future__ import annotations

import json
import os
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from lib.soyoung_runtime import (  # noqa: E402
    SoyoungRuntimeError,
    gen_api_request_id,
    get_state_paths,
    load_api_key,
    read_api_base_url,
    read_debug_mode,
)


API_BASE_URL = "https://skill.soyoung.com"
SOYOUNG_DEBUG: bool = os.environ.get("SOYOUNG_DEBUG", "false").lower() in ("1", "true", "yes")
_last_req_id: str = ""
_last_elapsed_ms: float = 0.0
_script_start: float = 0.0

_DUMP_INTENT_KEYWORDS = {
    "全部", "所有", "全量", "全库", "列出所有", "列出全部", "全部医生", "导出", "export", "dump",
}


def _validate_search_content(content: str) -> None:
    stripped = (content or "").strip()
    if len(stripped) < 2:
        raise SoyoungRuntimeError("❌ 关键词过短：请提供医生姓名、门店或城市关键词（至少 2 个字符）。")
    lower = stripped.lower()
    for kw in _DUMP_INTENT_KEYWORDS:
        if kw in lower:
            raise SoyoungRuntimeError(
                "❌ 不支持全量导出：本接口仅支持关键词检索，不提供全部医生列表。"
                "请输入具体医生姓名、门店或城市关键词。"
            )


def _debug_footer() -> str:
    if not SOYOUNG_DEBUG or not _last_req_id:
        return ""
    total_ms = (time.monotonic() - _script_start) * 1000 if _script_start else 0.0
    return (
        f"\n\n> 🔍 **req_id**: `{_last_req_id}`"
        f" · **接口**: `{_last_elapsed_ms:.0f} ms`"
        f" · **总计**: `{total_ms:.0f} ms`"
    )


def make_request(endpoint, body=None, api_key=None):
    global _last_req_id, _last_elapsed_ms
    req_id = gen_api_request_id()
    _last_req_id = req_id
    url = f"{API_BASE_URL}{endpoint}"
    payload = {"api_key": api_key or "", "request_id": req_id}
    if body:
        payload.update(body)
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Soyoung-Clinic-Tools-Doctor/2.2.0",
            "X-Request-Id": req_id,
        },
        method="POST",
    )
    _t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body_bytes = resp.read()
        _last_elapsed_ms = (time.monotonic() - _t0) * 1000
        raw = json.loads(body_bytes)
        if isinstance(raw, list):
            return {"success": True, "data": raw}
        return raw
    except urllib.error.HTTPError as exc:
        _last_elapsed_ms = (time.monotonic() - _t0) * 1000
        code = exc.code
        if code == 401:
            return {"success": False, "error": "API Key 无效或已过期，请重新生成"}
        if code == 403:
            return {"success": False, "error": "无权限访问，请检查 API Key"}
        return {"success": False, "error": f"HTTP 错误：{code}"}
    except urllib.error.URLError as exc:
        _last_elapsed_ms = (time.monotonic() - _t0) * 1000
        if isinstance(exc.reason, (TimeoutError, socket.timeout)):
            return {"success": False, "error": "请求超时，请稍后重试"}
        return {"success": False, "error": "网络连接失败，请检查网络"}
    except (TimeoutError, socket.timeout):
        _last_elapsed_ms = (time.monotonic() - _t0) * 1000
        return {"success": False, "error": "请求超时，请稍后重试"}
    except Exception as exc:
        _last_elapsed_ms = (time.monotonic() - _t0) * 1000
        return {"success": False, "error": f"请求失败：{str(exc)}"}


def doctor_search(content, city_name=None, api_key=None):
    body = {"content": content}
    if city_name:
        body["city_name"] = city_name
    return make_request("/project/skill/clinic_doctor/search", body=body, api_key=api_key)


def format_doctor_info(result):
    if not result.get("success"):
        return f"❌ **查询失败**：{result.get('error', '未知错误')}"

    doctors = result.get("data", [])
    if not doctors:
        return "👨‍⚕️ **未找到相关医生**"

    lines = ["👨‍⚕️ **医生信息**\n"]
    for i, d in enumerate(doctors, 1):
        name = d.get("医生名称") or d.get("name", "未知医生")
        lines.append(f"**{i}. {name}**")
        if d.get("医生职称"):
            lines.append(f"职称：{d.get('医生职称')}")
        if d.get("医生所在城市"):
            lines.append(f"城市：{d.get('医生所在城市')}")
        if d.get("医生常驻门店"):
            lines.append(f"常驻门店：{d.get('医生常驻门店')}")
        if d.get("医生认证信息"):
            lines.append(f"认证信息：{d.get('医生认证信息')}")
        if d.get("医生排班信息"):
            lines.append(f"排班信息：{d.get('医生排班信息')}")
        lines.append("")
    return "\n".join(lines)


def main():
    global _script_start
    _script_start = time.monotonic()
    import argparse

    parser = argparse.ArgumentParser(description="doctor")
    parser.add_argument("--action", choices=["doctor_search"])
    parser.add_argument("--workspace-key")
    parser.add_argument("--content")
    parser.add_argument("--city_name")
    parser.add_argument("--api-key")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        paths = get_state_paths(args.workspace_key)
        global SOYOUNG_DEBUG, API_BASE_URL
        SOYOUNG_DEBUG = read_debug_mode(paths)
        API_BASE_URL = read_api_base_url(paths)
        api_key = load_api_key(paths, args.api_key)
        if not api_key:
            print(
                "❌ 未找到 API Key\n\n"
                "请先由主人在私聊中说：「配置新氧 API Key 为 xxx」\n"
                "（群聊绝不能发送 API Key）"
            )
            sys.exit(1)

        if not args.action:
            parser.print_help()
            return

        if not args.content:
            print("❌ 缺少 --content")
            return
        _validate_search_content(args.content)
        result = doctor_search(args.content, city_name=args.city_name, api_key=api_key)

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_doctor_info(result) + _debug_footer())

    except SoyoungRuntimeError as exc:
        print(str(exc))


if __name__ == "__main__":
    main()
