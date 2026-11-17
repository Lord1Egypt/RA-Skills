#!/usr/bin/env python3
"""检查 V2 请求结构、引用关系和业务图形文字长度。"""

from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Any

from _client import read_json_input, write_json


KINDS = {"chart", "organization", "flow", "smartart", "schedule", "sequence", "timeline"}
VARIANTS = {
    "chart": {"bar", "line", "pie", "radar", "comparison", "funnel", "matrix"},
    "flow": {"sequence", "graph"},
    "smartart": {"process", "vertical-detail", "cycle", "radial", "petal-radial", "pyramid", "relationship", "comparison", "key-points"},
    "schedule": {"gantt", "time-scale-network", "single-code-network"},
    "timeline": {"wave", "milestone", "path", "ribbon", "blocks", "loop", "staircase", "vertical-spine", "icon-ribbon"},
}
PAGES = {"a4-portrait", "a4-landscape"}
THEMES = {
    "tech-blue", "classic-engineering", "government-red", "black-white", "sky-blue", "mint-green",
    "soft-warm", "pastel-mix", "teal-gold", "lavender", "formal-black", "engineering-green",
    "elegant-purple", "business-blue", "solemn-red", "warm-gold",
}
FLOW_SHAPES = {"start", "end", "process", "decision", "document", "subprocess"}
SMARTART_ICONS = {"cross", "circle", "curve", "card", "nodes", "gear"}
TIMELINE_ICONS = {"briefcase", "handshake", "trophy", "chart", "clock", "globe", "flag"}

LIMITS = {
    "title": (30, 120),
    "subtitle": (50, 180),
    "chart.label": (14, 80),
    "chart.series": (12, 80),
    "organization.name": (12, 80),
    "organization.role": (24, 120),
    "flow.text": (14, 120),
    "flow.detail": (28, 180),
    "flow.link_label": (8, 40),
    "smartart.title": (14, 80),
    "smartart.note": (36, 160),
    "smartart.center": (16, 80),
    "schedule.name": (16, 100),
    "schedule.group": (12, 60),
    "schedule.owner": (12, 60),
    "sequence.participant": (14, 80),
    "sequence.message": (24, 120),
    "sequence.note": (32, 160),
    "timeline.date": (12, 40),
    "timeline.title": (14, 100),
    "timeline.description": (32, 160),
}


def add_issue(items: list[dict[str, Any]], level: str, path: str, message: str) -> None:
    items.append({"level": level, "path": path, "message": message})


def inspect_text(items: list[dict[str, Any]], value: Any, path: str, rule: str, required: bool = False) -> None:
    if value is None:
        if required:
            add_issue(items, "error", path, "文字字段不能为空")
        return
    if not isinstance(value, str):
        add_issue(items, "error", path, "文字字段必须是字符串")
        return
    if not value.strip():
        add_issue(items, "error", path, "文字字段不能是空字符串")
        return
    recommended, hard = LIMITS[rule]
    length = len(value)
    if length > hard:
        add_issue(items, "error", path, f"长度 {length} 超过接口上限 {hard}")
    elif length > recommended:
        add_issue(items, "warning", path, f"长度 {length} 偏长，建议压缩到 {recommended} 字符以内")


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def check_keys(items: list[dict[str, Any]], value: Any, allowed: set[str], path: str) -> None:
    if not isinstance(value, dict):
        return
    for key in value:
        if key not in allowed:
            add_issue(items, "error", f"{path}/{key}", "字段不在当前 V2 契约允许范围内")


def check_object(items: list[dict[str, Any]], value: Any, path: str, label: str) -> bool:
    if not isinstance(value, dict) or isinstance(value, list):
        add_issue(items, "error", path, f"{label}必须是对象")
        return False
    return True


def check_list(items: list[dict[str, Any]], value: Any, path: str, label: str, minimum: int = 0, maximum: int | None = None) -> bool:
    if not isinstance(value, list):
        add_issue(items, "error", path, f"{label}必须是数组")
        return False
    if len(value) < minimum:
        add_issue(items, "error", path, f"{label}至少需要 {minimum} 项")
    if maximum is not None and len(value) > maximum:
        add_issue(items, "error", path, f"{label}不能超过 {maximum} 项")
    return True


def check_common(items: list[dict[str, Any]], request: dict[str, Any], kind: str) -> None:
    allowed = {"kind", "variant", "title", "subtitle", "theme", "page", "rasterScale", "data"}
    kind_fields = {
        "chart": {"unit"},
        "organization": {"direction"},
        "flow": {"direction", "layoutPolicy"},
        "smartart": {"direction", "center"},
        "schedule": {"startDate", "unit", "showTimeScale"},
        "sequence": set(),
        "timeline": set(),
    }
    check_keys(items, request, allowed | kind_fields[kind], "$")
    inspect_text(items, request.get("title"), "/title", "title")
    inspect_text(items, request.get("subtitle"), "/subtitle", "subtitle")

    if "theme" in request:
        theme = request.get("theme")
        if not isinstance(theme, str) or not theme.strip():
            add_issue(items, "error", "/theme", "theme 省略即可，不能传 null 或空字符串")
        elif theme not in THEMES:
            add_issue(items, "error", "/theme", f"未知色系 {theme!r}，先用 get_themes.py 查询线上列表")
    if "page" in request and request["page"] not in PAGES:
        add_issue(items, "error", "/page", "page 必须是 a4-portrait 或 a4-landscape")
    if "rasterScale" in request:
        scale = request["rasterScale"]
        if not isinstance(scale, int) or isinstance(scale, bool) or not 1 <= scale <= 3:
            add_issue(items, "error", "/rasterScale", "rasterScale 必须是 1 到 3 的整数")
    if kind in VARIANTS and request.get("variant") not in VARIANTS[kind]:
        add_issue(items, "error", "/variant", f"{kind} 的 variant 不在当前 V2 支持范围内")


def check_chart(items: list[dict[str, Any]], request: dict[str, Any]) -> None:
    data = request.get("data")
    if not check_list(items, data, "/data", "图表数据", 1, 24000):
        return
    if "unit" in request:
        inspect_text(items, request["unit"], "/unit", "chart.series")
        if isinstance(request["unit"], str) and len(request["unit"]) > 20:
            add_issue(items, "error", "/unit", "unit 不能超过 20 个字符")

    variant = request.get("variant")
    has_series: bool | None = None
    labels: set[str] = set()
    series: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    for index, row in enumerate(data):
        path = f"/data/{index}"
        if not check_object(items, row, path, "图表行"):
            continue
        check_keys(items, row, {"label", "series", "value"}, path)
        inspect_text(items, row.get("label"), f"{path}/label", "chart.label", True)
        if "series" in row:
            inspect_text(items, row.get("series"), f"{path}/series", "chart.series", True)
        current_has_series = row.get("series") is not None
        if has_series is None:
            has_series = current_has_series
        elif has_series != current_has_series:
            add_issue(items, "error", path, "图表数据不能混用有 series 和无 series 的行")
        value = row.get("value")
        if not is_number(value):
            add_issue(items, "error", f"{path}/value", "value 必须是有限数字")
        label = row.get("label") if isinstance(row.get("label"), str) else None
        series_name = row.get("series") if isinstance(row.get("series"), str) else "__single__"
        if label:
            labels.add(label)
            series.add(series_name)
            pair = (label, series_name)
            if pair in pairs:
                add_issue(items, "error", path, "同一 label 和 series 不能重复")
            pairs.add(pair)
        if variant == "matrix" and not current_has_series:
            add_issue(items, "error", f"{path}/series", "matrix 必须为每行提供 series")
        if variant in {"pie", "funnel", "radar"} and is_number(value) and value < 0:
            add_issue(items, "error", f"{path}/value", f"{variant} 不允许负数")
    if len(labels) > (12 if variant == "matrix" else 200):
        add_issue(items, "error", "/data", "图表分类数量超过当前契约限制")
    if len(series) > 12:
        add_issue(items, "error", "/data", "图表系列数量不能超过 12")
    if variant == "matrix" and labels and series and len(pairs) != len(labels) * len(series):
        add_issue(items, "error", "/data", "matrix 必须补齐每个 label 与 series 的组合")


def check_organization(items: list[dict[str, Any]], request: dict[str, Any]) -> None:
    if "direction" in request and request["direction"] not in {"vertical", "horizontal"}:
        add_issue(items, "error", "/direction", "direction 必须是 vertical 或 horizontal")

    def visit(node: Any, path: str, depth: int, count: list[int]) -> None:
        if not check_object(items, node, path, "组织节点"):
            return
        check_keys(items, node, {"name", "role", "headcount", "children"}, path)
        count[0] += 1
        if count[0] > 200:
            add_issue(items, "error", path, "组织节点不能超过 200 个")
        if depth > 12:
            add_issue(items, "error", path, "组织层级不能超过 12 层")
        inspect_text(items, node.get("name"), f"{path}/name", "organization.name", True)
        inspect_text(items, node.get("role"), f"{path}/role", "organization.role")
        if "headcount" in node:
            value = node["headcount"]
            if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 1_000_000:
                add_issue(items, "error", f"{path}/headcount", "headcount 必须是 0 到 1000000 的整数")
        children = node.get("children", [])
        if not check_list(items, children, f"{path}/children", "children", 0, 200):
            return
        for index, child in enumerate(children):
            visit(child, f"{path}/children/{index}", depth + 1, count)

    visit(request.get("data"), "/data", 0, [0])


def check_flow(items: list[dict[str, Any]], request: dict[str, Any]) -> None:
    if "direction" in request and request["direction"] not in {"vertical", "horizontal"}:
        add_issue(items, "error", "/direction", "direction 必须是 vertical 或 horizontal")
    if "layoutPolicy" in request:
        policy = request["layoutPolicy"]
        if not check_object(items, policy, "/layoutPolicy", "layoutPolicy"):
            return
        check_keys(items, policy, {"usage", "canvas", "preserveDirection"}, "/layoutPolicy")
        if policy.get("usage") != "standalone-image" or policy.get("canvas") != "adaptive" or policy.get("preserveDirection") is not True:
            add_issue(items, "error", "/layoutPolicy", "独立自适应画布必须使用固定的 standalone-image/adaptive/true 组合")
        if "page" in request:
            add_issue(items, "error", "/page", "flow.graph 使用 layoutPolicy 时不能同时传 page")

    variant = request.get("variant")
    data = request.get("data")
    if variant == "sequence":
        if not check_list(items, data, "/data", "线性流程步骤", 2, 80):
            return
        for index, step in enumerate(data):
            path = f"/data/{index}"
            if isinstance(step, str):
                inspect_text(items, step, path, "flow.text", True)
            elif check_object(items, step, path, "流程步骤"):
                check_keys(items, step, {"text", "detail", "shape"}, path)
                inspect_text(items, step.get("text"), f"{path}/text", "flow.text", True)
                inspect_text(items, step.get("detail"), f"{path}/detail", "flow.detail")
                if "shape" in step and step["shape"] not in FLOW_SHAPES:
                    add_issue(items, "error", f"{path}/shape", "未知流程节点形状")
        return

    if not check_object(items, data, "/data", "流程图数据"):
        return
    check_keys(items, data, {"nodes", "links"}, "/data")
    nodes = data.get("nodes")
    links = data.get("links")
    if not check_list(items, nodes, "/data/nodes", "流程节点", 1, 80):
        nodes = []
    if not check_list(items, links, "/data/links", "流程连线", 1, 160):
        links = []
    refs: set[str] = set()
    for index, node in enumerate(nodes):
        path = f"/data/nodes/{index}"
        if not check_object(items, node, path, "流程节点"):
            continue
        check_keys(items, node, {"ref", "text", "detail", "shape"}, path)
        inspect_text(items, node.get("ref"), f"{path}/ref", "flow.text", True)
        inspect_text(items, node.get("text"), f"{path}/text", "flow.text", True)
        inspect_text(items, node.get("detail"), f"{path}/detail", "flow.detail")
        ref = node.get("ref") if isinstance(node.get("ref"), str) else None
        if ref:
            if ref in refs:
                add_issue(items, "error", f"{path}/ref", "流程节点 ref 必须唯一")
            refs.add(ref)
        if "shape" in node and node["shape"] not in FLOW_SHAPES:
            add_issue(items, "error", f"{path}/shape", "未知流程节点形状")
    for index, link in enumerate(links):
        path = f"/data/links/{index}"
        if not check_object(items, link, path, "流程连线"):
            continue
        check_keys(items, link, {"from", "to", "label", "relation"}, path)
        for field in ("from", "to"):
            inspect_text(items, link.get(field), f"{path}/{field}", "flow.text", True)
            if isinstance(link.get(field), str) and link[field] not in refs:
                add_issue(items, "error", f"{path}/{field}", "连线端点必须引用已有节点 ref")
        inspect_text(items, link.get("label"), f"{path}/label", "flow.link_label")
        if "relation" in link and link["relation"] not in {"main", "feedback"}:
            add_issue(items, "error", f"{path}/relation", "relation 必须是 main 或 feedback")


def check_smartart(items: list[dict[str, Any]], request: dict[str, Any]) -> None:
    variant = request.get("variant")
    if "direction" in request and request["direction"] not in {"vertical", "horizontal"}:
        add_issue(items, "error", "/direction", "direction 必须是 vertical 或 horizontal")
    if "center" in request:
        inspect_text(items, request["center"], "/center", "smartart.center", True)
    if request.get("center") is not None and variant not in {"cycle", "radial", "petal-radial", "relationship"}:
        add_issue(items, "error", "/center", "center 只适用于 cycle、radial、petal-radial、relationship")

    data = request.get("data")
    if variant == "comparison":
        if not check_object(items, data, "/data", "comparison 数据"):
            return
        check_keys(items, data, {"columns", "rows"}, "/data")
        columns = data.get("columns")
        rows = data.get("rows")
        if check_list(items, columns, "/data/columns", "comparison columns", 2, 2):
            for index, value in enumerate(columns):
                inspect_text(items, value, f"/data/columns/{index}", "smartart.title", True)
        if check_list(items, rows, "/data/rows", "comparison rows", 2, 5):
            for index, row in enumerate(rows):
                path = f"/data/rows/{index}"
                if not check_object(items, row, path, "comparison 行"):
                    continue
                check_keys(items, row, {"label", "values"}, path)
                inspect_text(items, row.get("label"), f"{path}/label", "smartart.title", True)
                values = row.get("values")
                if check_list(items, values, f"{path}/values", "comparison values", 2, 2):
                    for value_index, value in enumerate(values):
                        inspect_text(items, value, f"{path}/values/{value_index}", "smartart.note", True)
        return

    if not check_list(items, data, "/data", "SmartArt 数据", 2, 6):
        return
    if variant == "petal-radial" and len(data) != 6:
        add_issue(items, "error", "/data", "petal-radial 必须正好提供 6 项")
    for index, item in enumerate(data):
        path = f"/data/{index}"
        if isinstance(item, str):
            inspect_text(items, item, path, "smartart.title", True)
            continue
        if not check_object(items, item, path, "SmartArt 项"):
            continue
        check_keys(items, item, {"title", "note", "icon"}, path)
        inspect_text(items, item.get("title"), f"{path}/title", "smartart.title", True)
        inspect_text(items, item.get("note"), f"{path}/note", "smartart.note")
        if "icon" in item and item["icon"] not in SMARTART_ICONS:
            add_issue(items, "error", f"{path}/icon", "未知 SmartArt 图标")


def check_schedule(items: list[dict[str, Any]], request: dict[str, Any]) -> None:
    if "startDate" in request:
        value = request["startDate"]
        if not isinstance(value, str) or len(value) != 10 or value[4] != "-" or value[7] != "-":
            add_issue(items, "error", "/startDate", "startDate 必须是 YYYY-MM-DD")
    if "unit" in request and request["unit"] not in {"day", "week", "stage"}:
        add_issue(items, "error", "/unit", "unit 必须是 day、week 或 stage")
    if "showTimeScale" in request and not isinstance(request["showTimeScale"], bool):
        add_issue(items, "error", "/showTimeScale", "showTimeScale 必须是布尔值")
    data = request.get("data")
    if not check_list(items, data, "/data", "排期任务", 1, 30):
        return
    refs: set[str] = set()
    tasks: list[tuple[str, Any, str]] = []
    for index, task in enumerate(data):
        path = f"/data/{index}"
        if not check_object(items, task, path, "排期任务"):
            continue
        check_keys(items, task, {"ref", "name", "duration", "predecessors", "start", "group", "owner", "milestone"}, path)
        inspect_text(items, task.get("ref"), f"{path}/ref", "schedule.name", True)
        inspect_text(items, task.get("name"), f"{path}/name", "schedule.name", True)
        ref = task.get("ref") if isinstance(task.get("ref"), str) else None
        if ref:
            if ref in refs:
                add_issue(items, "error", f"{path}/ref", "任务 ref 必须唯一")
            refs.add(ref)
        duration = task.get("duration")
        if not isinstance(duration, int) or isinstance(duration, bool) or not 1 <= duration <= 10000:
            add_issue(items, "error", f"{path}/duration", "duration 必须是 1 到 10000 的整数")
        if "start" in task and (not isinstance(task["start"], int) or isinstance(task["start"], bool) or not 0 <= task["start"] <= 1_000_000):
            add_issue(items, "error", f"{path}/start", "start 必须是 0 到 1000000 的整数")
        inspect_text(items, task.get("group"), f"{path}/group", "schedule.group")
        inspect_text(items, task.get("owner"), f"{path}/owner", "schedule.owner")
        if "milestone" in task and not isinstance(task["milestone"], bool):
            add_issue(items, "error", f"{path}/milestone", "milestone 必须是布尔值")
        predecessors = task.get("predecessors", [])
        if check_list(items, predecessors, f"{path}/predecessors", "predecessors", 0, 30):
            seen: set[str] = set()
            for predecessor_index, predecessor in enumerate(predecessors):
                if not isinstance(predecessor, str) or not predecessor.strip():
                    add_issue(items, "error", f"{path}/predecessors/{predecessor_index}", "前置任务 ref 必须是非空字符串")
                elif predecessor in seen:
                    add_issue(items, "error", f"{path}/predecessors/{predecessor_index}", "前置任务不能重复")
                seen.add(predecessor)
            tasks.append((ref or "", predecessors, path))
    for ref, predecessors, path in tasks:
        for predecessor in predecessors:
            if predecessor not in refs:
                add_issue(items, "error", f"{path}/predecessors", f"未知前置任务 ref: {predecessor}")
            if predecessor == ref:
                add_issue(items, "error", f"{path}/predecessors", "任务不能依赖自身")
    explicit_starts = ["start" in task for task in data if isinstance(task, dict)]
    if any(explicit_starts):
        if request.get("variant") != "gantt":
            add_issue(items, "error", "/data", "start 只适用于 schedule.gantt")
        if not all(explicit_starts):
            add_issue(items, "error", "/data", "排期不能混用有 start 和无 start 的任务")
        if any(isinstance(task, dict) and task.get("predecessors") for task in data):
            add_issue(items, "error", "/data", "显式 start 模式不能同时提供 predecessors")


def check_sequence(items: list[dict[str, Any]], request: dict[str, Any]) -> None:
    data = request.get("data")
    if not check_object(items, data, "/data", "时序图数据"):
        return
    check_keys(items, data, {"participants", "messages", "notes"}, "/data")
    participants = data.get("participants")
    messages = data.get("messages")
    notes = data.get("notes", [])
    if not check_list(items, participants, "/data/participants", "参与方", 2, 6):
        participants = []
    if not check_list(items, messages, "/data/messages", "消息", 1, 12):
        messages = []
    if not check_list(items, notes, "/data/notes", "备注", 0, 4):
        notes = []
    refs: set[str] = set()
    for index, participant in enumerate(participants):
        path = f"/data/participants/{index}"
        if isinstance(participant, str):
            inspect_text(items, participant, path, "sequence.participant", True)
            ref = participant.strip()
        elif check_object(items, participant, path, "参与方"):
            check_keys(items, participant, {"ref", "name"}, path)
            inspect_text(items, participant.get("ref"), f"{path}/ref", "sequence.participant", True)
            inspect_text(items, participant.get("name"), f"{path}/name", "sequence.participant", True)
            ref = participant.get("ref") if isinstance(participant.get("ref"), str) else ""
        else:
            ref = ""
        if ref:
            if ref in refs:
                add_issue(items, "error", f"{path}/ref", "参与方 ref 必须唯一")
            refs.add(ref)
    for index, message in enumerate(messages):
        path = f"/data/messages/{index}"
        if not check_object(items, message, path, "消息"):
            continue
        check_keys(items, message, {"from", "to", "message", "kind"}, path)
        for field in ("from", "to"):
            inspect_text(items, message.get(field), f"{path}/{field}", "sequence.participant", True)
            if isinstance(message.get(field), str) and message[field] not in refs:
                add_issue(items, "error", f"{path}/{field}", "消息端点必须引用已有参与方 ref")
        inspect_text(items, message.get("message"), f"{path}/message", "sequence.message", True)
        if "kind" in message and message["kind"] not in {"call", "return"}:
            add_issue(items, "error", f"{path}/kind", "消息 kind 必须是 call 或 return")
    for index, note in enumerate(notes):
        path = f"/data/notes/{index}"
        if not check_object(items, note, path, "备注"):
            continue
        check_keys(items, note, {"participant", "text"}, path)
        inspect_text(items, note.get("participant"), f"{path}/participant", "sequence.participant", True)
        inspect_text(items, note.get("text"), f"{path}/text", "sequence.note", True)
        if isinstance(note.get("participant"), str) and note["participant"] not in refs:
            add_issue(items, "error", f"{path}/participant", "备注 participant 必须引用已有参与方 ref")


def check_timeline(items: list[dict[str, Any]], request: dict[str, Any]) -> None:
    data = request.get("data")
    if not check_list(items, data, "/data", "时间轴事件", 2, 8):
        return
    refs: set[str] = set()
    for index, item in enumerate(data):
        path = f"/data/{index}"
        if not check_object(items, item, path, "时间轴事件"):
            continue
        check_keys(items, item, {"ref", "date", "title", "description", "position", "icon"}, path)
        for field, rule in (("ref", "timeline.title"), ("date", "timeline.date"), ("title", "timeline.title")):
            inspect_text(items, item.get(field), f"{path}/{field}", rule, True)
        inspect_text(items, item.get("description"), f"{path}/description", "timeline.description")
        ref = item.get("ref") if isinstance(item.get("ref"), str) else None
        if ref:
            if ref in refs:
                add_issue(items, "error", f"{path}/ref", "时间轴 ref 必须唯一")
            refs.add(ref)
        if "position" in item and item["position"] not in {"top", "bottom"}:
            add_issue(items, "error", f"{path}/position", "position 必须是 top 或 bottom")
        if "icon" in item and item["icon"] not in TIMELINE_ICONS:
            add_issue(items, "error", f"{path}/icon", "未知时间轴图标")


def lint(request: Any) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    if not isinstance(request, dict):
        add_issue(issues, "error", "$", "请求必须是 JSON 对象")
        return {"valid": False, "contractRequired": True, "errors": 1, "warnings": 0, "issues": issues}

    kind = request.get("kind")
    if kind not in KINDS:
        add_issue(issues, "error", "/kind", "kind 不属于 V2 支持范围")
        return {"valid": False, "contractRequired": True, "errors": 1, "warnings": 0, "issues": issues}

    check_common(issues, request, kind)
    if kind not in {"organization", "sequence"} and not isinstance(request.get("variant"), str):
        add_issue(issues, "error", "/variant", "该 kind 必须提供 variant")
    if "data" not in request:
        add_issue(issues, "error", "/data", "请求必须提供 data")
    elif kind == "chart":
        check_chart(issues, request)
    elif kind == "organization":
        check_organization(issues, request)
    elif kind == "flow":
        check_flow(issues, request)
    elif kind == "smartart":
        check_smartart(issues, request)
    elif kind == "schedule":
        check_schedule(issues, request)
    elif kind == "sequence":
        check_sequence(issues, request)
    elif kind == "timeline":
        check_timeline(issues, request)

    errors = sum(issue["level"] == "error" for issue in issues)
    warnings = sum(issue["level"] == "warning" for issue in issues)
    return {
        "valid": errors == 0,
        "contractRequired": True,
        "errors": errors,
        "warnings": warnings,
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="检查图形请求结构、引用关系和节点文字长度")
    parser.add_argument("request", nargs="?", default="-", help="JSON 请求文件，或使用 - 从 stdin 读取")
    parser.add_argument("--strict", action="store_true", help="将文字长度 warning 也作为失败")
    parser.add_argument("--output", help="将检查结果写入 JSON 文件")
    args = parser.parse_args()
    try:
        result = lint(read_json_input(args.request))
        write_json(result, args.output)
        return 1 if not result["valid"] or (args.strict and result.get("warnings", 0) > 0) else 0
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f"lint_render_request.py: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
