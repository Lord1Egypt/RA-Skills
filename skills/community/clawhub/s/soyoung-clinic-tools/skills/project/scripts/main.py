#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""project — 项目查询与商品查询。"""

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

# 调试开关：req_id 始终会发给后端，仅此开关控制会话中是否展示
SOYOUNG_DEBUG: bool = os.environ.get("SOYOUNG_DEBUG", "false").lower() in ("1", "true", "yes")

# 拖库防护：命中任意一个词即视为全量枚举意图，直接拒绝
_DUMP_INTENT_KEYWORDS = {
    "全部", "所有", "全量", "全库", "列出所有", "列出全部", "全部项目",
    "所有项目", "所有介绍", "全部介绍", "输出全部", "导出", "export", "dump",
}


def _validate_search_content(content: str) -> None:
    """拒绝空关键词和明显的全量枚举请求。"""
    stripped = (content or "").strip()
    if len(stripped) < 2:
        raise SoyoungRuntimeError(
            "❌ 关键词过短：请提供具体的项目名称或症状（至少 2 个字符）。"
        )
    lower = stripped.lower()
    for kw in _DUMP_INTENT_KEYWORDS:
        if kw in lower:
            raise SoyoungRuntimeError(
                "❌ 不支持全量导出：本接口仅支持关键词检索，不提供全部项目列表。"
                "请输入具体项目名称或症状关键词。"
            )
_last_req_id: str = ""
_last_elapsed_ms: float = 0.0
_script_start: float = 0.0


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
            "User-Agent": "Soyoung-Clinic-Tools-Project/2.2.2",
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
        # 后端偶尔直接返回裸 list，统一包装成标准信封
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


def project_search(content, api_key=None):
    return make_request("/project/skill/clinic_solution/search", body={"content": content}, api_key=api_key)


def product_search(content, city_name=None, api_key=None):
    body = {"content": content}
    if city_name: body["city_name"] = city_name
    return make_request("/project/skill/clinic_product/search", body=body, api_key=api_key)


def format_project_info(result):
    if not result.get("success"):
        return f"❌ **查询失败**：{result.get('error', '未知错误')}"
    data = result.get("data")
    if not data:
        return "💉 **未找到相关项目**\n\n请尝试其他关键词"
    projects = data if isinstance(data, list) else [data]
    lines = []
    for p in projects:
        name = p.get("品项名称") or p.get("name", "未知项目")
        lines.append(f"💉 **{name}**")
        if p.get("品项id"): lines.append(f"ID：{p.get('品项id')}")
        lines.append("")
        if p.get("核心原理"): lines += ["📋 **核心原理**", f"{p.get('核心原理')}", ""]
        for k, label in [
            ("核心属性", "核心属性"), ("service_type", "类型"), ("category", "分类"),
            ("principle", "作用原理"),
        ]:
            if p.get(k): lines.append(f"• {label}：{p.get(k)}")
        if any(p.get(k) for k in ["features", "suitable_people", "maintain_duration"]):
            lines.append("\n✨ **产品特点**")
            for k, label in [("features", "特点"), ("suitable_people", "适合人群"), ("maintain_duration", "维持时间")]:
                if p.get(k): lines.append(f"• {label}：{p.get(k)}")
        if any(p.get(k) for k in ["anesthesia", "pain_level", "operation_method", "treatment_duration", "treatment_steps"]):
            lines += ["", "👨‍⚕️ **医学操作**"]
            for k, label in [
                ("anesthesia", "麻醉方式"), ("pain_level", "疼痛度"), ("operation_method", "操作方式"),
                ("can_combine", "能否一起做"), ("treatment_duration", "治疗时长"),
                ("treatment_steps", "治疗步骤"), ("treatment_notes", "治疗备注"),
            ]:
                if p.get(k): lines.append(f"• {label}：{p.get(k)}")
        indications = p.get("indications", [])
        if indications:
            lines += ["", "🎯 **适应症 / 功效**"]
            for ind in (indications if isinstance(indications, list) else [indications]):
                line = f"• {ind.get('name', '')}" if isinstance(ind, dict) else f"• {ind}"
                if isinstance(ind, dict):
                    if ind.get("degree"): line += f"（{ind['degree']}）"
                    if ind.get("cause"): line += f"：{ind['cause']}"
                lines.append(line)
        if any(p.get(k) for k in ["aftercare_notes", "aftercare_reaction", "safety_tips", "recovery"]):
            lines += ["", "📝 **术后护理**"]
            for k, label in [("aftercare_notes", "注意事项"), ("aftercare_reaction", "术后反应"),
                              ("safety_tips", "安全提示"), ("recovery", "恢复时间")]:
                if p.get(k): lines.append(f"• {label}：{p.get(k)}")
        faqs = p.get("faqs", [])
        if faqs:
            lines += ["", "❓ **常见问题**"]
            for faq in faqs[:5]:
                q = faq.get("question", "") if isinstance(faq, dict) else str(faq)
                a = faq.get("answer", "") if isinstance(faq, dict) else ""
                lines.append(f"**Q: {q}**")
                if a: lines.append(f"A: {a}")
                lines.append("")
        lines += ["---", ""]
    return "\n".join(lines)


def format_product_info(result):
    if not result.get("success"):
        return f"❌ **查询失败**：{result.get('error', '未知错误')}"
    products = result.get("data", [])
    if not products:
        return "🛒 **未找到相关商品**"
    lines = ["🛒 **商品信息**\n"]
    for i, p in enumerate(products, 1):
        name = p.get("商品名称") or p.get("name", "未知")
        lines.append(f"**{i}. {name}**")
        if p.get("商品数量"): lines.append(f"📦 规格：{p.get('商品数量')}")
        sell_price = p.get("售卖价格") or p.get("price", "")
        final_price = p.get("到手价格") or p.get("final_price", "")
        if sell_price: lines.append(f"💰 售价：{sell_price}")
        if final_price and final_price != sell_price: lines.append(f"🎯 到手价：{final_price}")
        if p.get("使用产品信息"):
            prod_info = p.get("使用产品信息")
            if isinstance(prod_info, list):
                for item in prod_info: lines.append(f"  • {item}")
            else:
                lines.append(f"  • {prod_info}")
        lines.append("")
    return "\n".join(lines)


def main():
    global _script_start
    _script_start = time.monotonic()
    import argparse

    parser = argparse.ArgumentParser(description="project")
    parser.add_argument("--action", choices=["project_search", "product_search"])
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

        def fmt(result, formatter):
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(formatter(result) + _debug_footer())

        if args.action == "project_search":
            if not args.content:
                print("❌ 缺少 --content")
                return
            _validate_search_content(args.content)
            fmt(project_search(args.content, api_key), format_project_info)
        elif args.action == "product_search":
            if not args.content:
                print("❌ 缺少 --content")
                return
            _validate_search_content(args.content)
            fmt(product_search(args.content, city_name=args.city_name, api_key=api_key), format_product_info)
    except SoyoungRuntimeError as exc:
        print(str(exc))


if __name__ == "__main__":
    main()
