#!/usr/bin/env python3
"""BP Audit Data Query CLI — fetch BP data for audit via Open-API.

Usage:
    python3 bp_api.py <action> [options]

Actions:
    get_all_periods           List all BP periods
    get_group_tree            Get group tree for a period
    get_task_tree             Get task tree for a group
    get_goal_detail           Get objective detail with KRs and actions
    get_key_result_detail     Get key result detail with actions
    get_action_detail         Get action detail
    add_key_result            Add a child key result under a goal
    add_action                Add a child action under a key result
    search_task               Search tasks by name
    search_group              Search groups by name

Options:
    --format json|md          Output format (default: json). "md" produces
                              compact Markdown that significantly reduces token
                              consumption when used with LLMs.

Environment:
    BP_OPEN_API_APP_KEY       Authentication key (required)
    BP_OPEN_API_BASE_URL      API base URL (optional, has default)
"""

import argparse
import json
import os
import re
import sys

import requests

BASE_URL = os.environ.get(
    "BP_OPEN_API_BASE_URL",
    "https://sg-al-cwork-web.mediportal.com.cn/open-api",
)
APP_KEY = os.environ.get("BP_OPEN_API_APP_KEY", "")

TIMEOUT = 30


# ─── HTTP helper ─────────────────────────────────────────────────

def _request(method, path, *, params=None, json_body=None):
    if not APP_KEY:
        return {"error": "BP_OPEN_API_APP_KEY is not configured. Set it as an environment variable."}

    url = f"{BASE_URL}{path}"
    headers = {"appKey": APP_KEY}

    try:
        if method == "GET":
            resp = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
        else:
            headers["Content-Type"] = "application/json"
            resp = requests.post(url, params=params, json=json_body, headers=headers, timeout=TIMEOUT)

        resp.raise_for_status()
        data = resp.json()

        if data.get("resultCode") != 1:
            return {"error": data.get("resultMsg", "Unknown API error"), "resultCode": data.get("resultCode")}

        return {"success": True, "data": data.get("data")}

    except requests.HTTPError as e:
        return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}


# ─── JSON slim helpers (existing) ────────────────────────────────

def _slim_group_tree(node):
    if node is None:
        return None
    if isinstance(node, list):
        return [_slim_group_tree(n) for n in node]
    keep = {k: node[k] for k in ("id", "name", "type", "employeeId", "levelNumber", "weight") if k in node}
    children = node.get("children")
    if children:
        keep["children"] = [_slim_group_tree(c) for c in children]
    return keep


def _slim_task_tree(node):
    if node is None:
        return None
    if isinstance(node, list):
        return [_slim_task_tree(n) for n in node]
    essential = ("id", "name", "fullLevelNumber", "type", "ruleType",
                 "planStartDate", "planEndDate", "statusDesc", "weight")
    keep = {k: node[k] for k in essential if k in node}
    children = node.get("children")
    if children:
        keep["children"] = [_slim_task_tree(c) for c in children]
    return keep


# ─── Markdown formatting helpers ─────────────────────────────────

def _strip_html(text):
    """Remove HTML tags and collapse whitespace."""
    if not text:
        return ""
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _fmt_users(task_users):
    """Format taskUsers list into compact string: '承接人:张三,李四; 协办人:王五'."""
    if not task_users:
        return "无"
    parts = []
    for u in task_users:
        role = u.get("role", "?")
        names = ",".join(e.get("name", "?") for e in (u.get("empList") or []))
        if names:
            parts.append(f"{role}:{names}")
    return "; ".join(parts) if parts else "无"


def _fmt_depts(task_depts):
    """Format taskDepts list into compact string."""
    if not task_depts:
        return ""
    parts = []
    for d in task_depts:
        names = ",".join(dp.get("name", "?") for dp in (d.get("deptList") or []))
        if names:
            parts.append(names)
    return "; ".join(parts)


def _fmt_align_list(items, label):
    """Format upwardTaskList / downTaskList into markdown lines."""
    if not items:
        return f"- {label}：无\n"
    lines = [f"- {label}（{len(items)}项）：\n"]
    for t in items:
        group_name = ""
        gi = t.get("groupInfo")
        if gi:
            group_name = f"[{gi.get('name', '?')}]"
        lines.append(f"  - {t.get('name', '?')} {group_name}（id:{t.get('id', '?')}）\n")
    return "".join(lines)


def _md_create_result(data, item_type):
    if isinstance(data, dict):
        task_id = data.get("taskId") or data.get("id") or "?"
        parent_id = data.get("parentTaskId") or data.get("parentId")
    else:
        task_id = data
        parent_id = None
    lines = [f"# 新增{item_type}成功\n\n"]
    lines.append(f"- 新任务 ID：{task_id}\n")
    if parent_id:
        lines.append(f"- 父任务 ID：{parent_id}\n")
    return "".join(lines)


# ─── Per-action Markdown formatters ──────────────────────────────

def _md_periods(data):
    lines = ["# BP 周期列表\n\n"]
    lines.append("| 名称 | ID | 状态 |\n|------|-----|------|\n")
    for p in (data or []):
        st = "启用" if p.get("status") == 1 else "停用"
        lines.append(f"| {p.get('name', '?')} | {p.get('id', '?')} | {st} |\n")
    return "".join(lines)


def _md_group_tree(data, indent=0):
    if not data:
        return "（空）\n"
    if isinstance(data, list):
        return "".join(_md_group_tree(n, indent) for n in data)
    prefix = "  " * indent
    typ = "组织" if data.get("type") == "org" else "个人"
    line = f"{prefix}- **{data.get('name', '?')}** ({typ}, {data.get('levelNumber', '?')}, id:{data.get('id', '?')})\n"
    children = data.get("children")
    if children:
        line += "".join(_md_group_tree(c, indent + 1) for c in children)
    return line


def _md_task_tree(data, indent=0):
    if not data:
        return "（空）\n"
    if isinstance(data, list):
        return "".join(_md_task_tree(n, indent) for n in data)
    prefix = "  " * indent
    line = f"{prefix}- **{data.get('name', '?')}** [{data.get('type', '?')}] ({data.get('fullLevelNumber', '?')}, {data.get('statusDesc', '?')}, id:{data.get('id', '?')})\n"
    children = data.get("children")
    if children:
        line += "".join(_md_task_tree(c, indent + 1) for c in children)
    return line


def _md_action(a, heading_level=4):
    """Format a single action (KI)."""
    h = "#" * heading_level
    lines = [f"{h} 举措 {a.get('fullLevelNumber', '?')}：{_strip_html(a.get('name', '?'))}\n\n"]
    lines.append(f"- 状态：{a.get('statusDesc', '?')} | 周期：{a.get('reportCycle', '?')} | 时间：{a.get('planDateRange', '?')}\n")
    lines.append(f"- 人员：{_fmt_users(a.get('taskUsers'))}\n")
    depts = _fmt_depts(a.get("taskDepts"))
    if depts:
        lines.append(f"- 部门：{depts}\n")
    lines.append(_fmt_align_list(a.get("upwardTaskList"), "向上对齐"))
    lines.append(_fmt_align_list(a.get("downTaskList"), "向下承接"))
    return "".join(lines)


def _md_key_result(kr, heading_level=3, include_actions=True):
    """Format a single KR (with optional actions)."""
    h = "#" * heading_level
    lines = [f"{h} KR {kr.get('fullLevelNumber', '?')}：{_strip_html(kr.get('name', '?'))}\n\n"]
    lines.append(f"- 状态：{kr.get('statusDesc', '?')} | 周期：{kr.get('reportCycle', '?')} | 时间：{kr.get('planDateRange', '?')}\n")
    lines.append(f"- 人员：{_fmt_users(kr.get('taskUsers'))}\n")
    depts = _fmt_depts(kr.get("taskDepts"))
    if depts:
        lines.append(f"- 部门：{depts}\n")
    ms = _strip_html(kr.get("measureStandard", ""))
    if ms:
        lines.append(f"- **衡量标准**：{ms}\n")
    lines.append(_fmt_align_list(kr.get("upwardTaskList"), "向上对齐"))
    lines.append(_fmt_align_list(kr.get("downTaskList"), "向下承接"))
    if include_actions and kr.get("actions"):
        lines.append("\n")
        for a in kr["actions"]:
            lines.append(_md_action(a, heading_level + 1))
            lines.append("\n")
    return "".join(lines)


def _md_goal_detail(data):
    """Format goal detail (with KRs and actions)."""
    lines = [f"# 目标 {data.get('fullLevelNumber', '?')}：{_strip_html(data.get('name', '?'))}\n\n"]
    lines.append(f"- 路径：{data.get('path', '?')}\n")
    lines.append(f"- 状态：{data.get('statusDesc', '?')} | 周期：{data.get('reportCycle', '?')} | 时间：{data.get('planDateRange', '?')}\n")
    lines.append(f"- 人员：{_fmt_users(data.get('taskUsers'))}\n")
    depts = _fmt_depts(data.get("taskDepts"))
    if depts:
        lines.append(f"- 部门：{depts}\n")
    lines.append(_fmt_align_list(data.get("upwardTaskList"), "向上对齐"))
    lines.append(_fmt_align_list(data.get("downTaskList"), "向下承接"))
    krs = data.get("keyResults") or []
    if krs:
        lines.append(f"\n## 关键成果（{len(krs)}条）\n\n")
        for kr in krs:
            lines.append(_md_key_result(kr))
            lines.append("\n")
    return "".join(lines)


def _md_kr_detail(data):
    """Format standalone KR detail (with actions)."""
    return _md_key_result(data, heading_level=2)


def _md_action_detail(data):
    """Format standalone action detail."""
    return _md_action(data, heading_level=2)


def _md_search_task(data):
    if not data:
        return "搜索结果：无匹配\n"
    lines = [f"# 任务搜索结果（{len(data)}条）\n\n"]
    lines.append("| 名称 | 类型 | 分组 | 编号 | ID |\n|------|------|------|------|----|\n")
    for t in data:
        group_name = t.get("groupName", "?")
        lines.append(
            f"| {t.get('name', '?')} | {t.get('type', '?')} "
            f"| {group_name} | {t.get('fullLevelNumber', '?')} "
            f"| {t.get('id', '?')} |\n"
        )
    return "".join(lines)


def _md_search_group(data):
    if not data:
        return "搜索结果：无匹配\n"
    lines = [f"# 分组搜索结果（{len(data)}条）\n\n"]
    lines.append("| 名称 | 类型 | 层级编码 | ID |\n|------|------|---------|----|\n")
    for g in data:
        typ = "组织" if g.get("type") == "org" else "个人"
        lines.append(
            f"| {g.get('name', '?')} | {typ} "
            f"| {g.get('levelNumber', '?')} "
            f"| {g.get('id', '?')} |\n"
        )
    return "".join(lines)


MD_FORMATTERS = {
    "get_all_periods": _md_periods,
    "get_group_tree": lambda d: f"# 分组树\n\n{_md_group_tree(d)}",
    "get_task_tree": lambda d: f"# 任务树\n\n{_md_task_tree(d)}",
    "get_goal_detail": _md_goal_detail,
    "get_key_result_detail": _md_kr_detail,
    "get_action_detail": _md_action_detail,
    "add_key_result": lambda d: _md_create_result(d, "关键成果"),
    "add_action": lambda d: _md_create_result(d, "关键举措"),
    "search_task": _md_search_task,
    "search_group": _md_search_group,
}


# ─── Action implementations ──────────────────────────────────────

def get_all_periods(args):
    params = {}
    if args.name:
        params["name"] = args.name
    return _request("GET", "/bp/period/getAllPeriod", params=params or None)


def get_group_tree(args):
    if not args.period_id:
        return {"error": "period_id is required for get_group_tree"}
    params = {"periodId": args.period_id}
    if getattr(args, "only_personal", False):
        params["onlyPersonal"] = "true"
    result = _request("GET", "/bp/group/getTree", params=params)
    if result.get("success") and result.get("data"):
        result["data"] = _slim_group_tree(result["data"])
    return result


def get_task_tree(args):
    if not args.group_id:
        return {"error": "group_id is required for get_task_tree"}
    result = _request("GET", "/bp/task/v2/getSimpleTree", params={"groupId": args.group_id})
    if result.get("success") and result.get("data"):
        result["data"] = _slim_task_tree(result["data"])
    return result


def get_goal_detail(args):
    if not args.task_id:
        return {"error": "task_id is required for get_goal_detail"}
    return _request("GET", "/bp/task/v2/getGoalAndKeyResult", params={"id": args.task_id})


def get_key_result_detail(args):
    if not args.task_id:
        return {"error": "task_id is required for get_key_result_detail"}
    return _request("GET", "/bp/task/v2/getKeyResult", params={"id": args.task_id})


def get_action_detail(args):
    if not args.task_id:
        return {"error": "task_id is required for get_action_detail"}
    return _request("GET", "/bp/task/v2/getAction", params={"id": args.task_id})


def search_task(args):
    if not args.group_id:
        return {"error": "group_id is required for search_task"}
    if not args.name:
        return {"error": "name is required for search_task"}
    return _request("GET", "/bp/task/v2/searchByName", params={"groupId": args.group_id, "name": args.name})


def search_group(args):
    if not args.period_id:
        return {"error": "period_id is required for search_group"}
    if not args.name:
        return {"error": "name is required for search_group"}
    return _request("GET", "/bp/group/searchByName", params={"periodId": args.period_id, "name": args.name})


def _parse_json_object(value, option_name):
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        return {"error": f"{option_name} must be valid JSON: {exc}"}
    if not isinstance(parsed, dict):
        return {"error": f"{option_name} must be a JSON object"}
    return {"success": True, "data": parsed}


def _parse_json_list(value, option_name):
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        return {"error": f"{option_name} must be valid JSON: {exc}"}
    if not isinstance(parsed, list):
        return {"error": f"{option_name} must be a JSON array"}
    return {"success": True, "data": parsed}


def _parse_id_list(raw_value):
    if not raw_value:
        return None
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def _build_task_payload(args, parent_field, *, scalar_fields, list_fields):
    payload = {}

    if args.body_json:
        parsed = _parse_json_object(args.body_json, "--body_json")
        if parsed.get("error"):
            return parsed
        payload.update(parsed["data"])

    parent_value = getattr(args, parent_field)
    if parent_value:
        payload[parent_field] = parent_value

    for field in scalar_fields:
        value = getattr(args, field)
        if value:
            api_field = "".join(
                word.capitalize() if index else word
                for index, word in enumerate(field.split("_"))
            )
            payload[api_field] = value

    for field in list_fields:
        value = getattr(args, field)
        if value:
            api_field = "".join(
                word.capitalize() if index else word
                for index, word in enumerate(field.split("_"))
            )
            payload[api_field] = _parse_id_list(value)

    if args.weight is not None:
        payload["weight"] = args.weight

    if args.upload_sp_file_dtos:
        parsed = _parse_json_list(args.upload_sp_file_dtos, "--upload_sp_file_dtos")
        if parsed.get("error"):
            return parsed
        payload["uploadSpFileDTOS"] = parsed["data"]

    return {"success": True, "data": payload}


def add_key_result(args):
    payload_result = _build_task_payload(
        args,
        "goal_id",
        scalar_fields=(
            "name",
            "rule_type",
            "required_index",
            "plan_start_date",
            "plan_end_date",
            "description",
            "measure_standard",
            "action_plan",
        ),
        list_fields=(
            "owner_ids",
            "owner_dept_ids",
            "collaborator_ids",
            "copy_to_ids",
            "supervisor_ids",
            "observer_ids",
            "upward_task_id_list",
        ),
    )
    if payload_result.get("error"):
        return payload_result

    payload = payload_result["data"]
    if not payload.get("goal_id") and not payload.get("goalId"):
        return {"error": "goal_id is required for add_key_result"}
    if not payload.get("name"):
        return {"error": "name is required for add_key_result"}

    if "goal_id" in payload:
        payload["goalId"] = payload.pop("goal_id")

    result = _request("POST", "/bp/task/v2/addKeyResult", json_body=payload)
    if result.get("success"):
        result["data"] = {"taskId": result["data"], "parentTaskId": payload.get("goalId")}
    return result


def add_action(args):
    payload_result = _build_task_payload(
        args,
        "key_result_id",
        scalar_fields=(
            "name",
            "rule_type",
            "required_index",
            "plan_start_date",
            "plan_end_date",
            "description",
            "measure_standard",
        ),
        list_fields=(
            "owner_ids",
            "upward_task_id_list",
        ),
    )
    if payload_result.get("error"):
        return payload_result

    payload = payload_result["data"]
    if not payload.get("key_result_id") and not payload.get("keyResultId"):
        return {"error": "key_result_id is required for add_action"}
    if not payload.get("name"):
        return {"error": "name is required for add_action"}

    if "key_result_id" in payload:
        payload["keyResultId"] = payload.pop("key_result_id")

    result = _request("POST", "/bp/task/v2/addAction", json_body=payload)
    if result.get("success"):
        result["data"] = {"taskId": result["data"], "parentTaskId": payload.get("keyResultId")}
    return result


# ─── CLI entry point ─────────────────────────────────────────────

ACTION_MAP = {
    "get_all_periods": get_all_periods,
    "get_group_tree": get_group_tree,
    "get_task_tree": get_task_tree,
    "get_goal_detail": get_goal_detail,
    "get_key_result_detail": get_key_result_detail,
    "get_action_detail": get_action_detail,
    "add_key_result": add_key_result,
    "add_action": add_action,
    "search_task": search_task,
    "search_group": search_group,
}


def main():
    parser = argparse.ArgumentParser(
        description="BP Audit Data Query — fetch BP data for audit via Open-API",
    )
    parser.add_argument("action", choices=ACTION_MAP.keys(), help="The query action to perform")
    parser.add_argument("--period_id", help="Period ID")
    parser.add_argument("--name", help="Name keyword (for search/filter)")
    parser.add_argument("--group_id", help="Group ID")
    parser.add_argument("--task_id", help="Task ID (for detail queries)")
    parser.add_argument("--goal_id", help="Goal ID (for add_key_result)")
    parser.add_argument("--key_result_id", help="Key result ID (for add_action)")
    parser.add_argument("--rule_type", help="Report cycle type")
    parser.add_argument("--required_index", help="Required report index for the cycle")
    parser.add_argument("--plan_start_date", help="Planned start date in yyyy-MM-dd")
    parser.add_argument("--plan_end_date", help="Planned end date in yyyy-MM-dd")
    parser.add_argument("--owner_ids", help="Comma-separated owner employee IDs")
    parser.add_argument("--owner_dept_ids", help="Comma-separated owner department IDs")
    parser.add_argument("--collaborator_ids", help="Comma-separated collaborator employee IDs")
    parser.add_argument("--copy_to_ids", help="Comma-separated copy-to employee IDs")
    parser.add_argument("--supervisor_ids", help="Comma-separated supervisor employee IDs")
    parser.add_argument("--observer_ids", help="Comma-separated observer employee IDs")
    parser.add_argument("--upward_task_id_list", help="Comma-separated upward task IDs")
    parser.add_argument("--weight", type=float, help="Task weight")
    parser.add_argument("--description", help="Task description")
    parser.add_argument("--measure_standard", help="Measure standard")
    parser.add_argument("--action_plan", help="Action plan")
    parser.add_argument("--upload_sp_file_dtos", help="JSON array for uploadSpFileDTOS")
    parser.add_argument("--body_json", help="Raw JSON object merged into POST body")
    parser.add_argument("--only_personal", action="store_true", help="Only personal groups (for get_group_tree)")
    parser.add_argument("--format", choices=["json", "md"], default="json",
                        help="Output format: json (default) or md (compact Markdown, saves tokens)")

    args = parser.parse_args()
    result = ACTION_MAP[args.action](args)

    if result.get("error"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    if args.format == "md":
        formatter = MD_FORMATTERS.get(args.action)
        if formatter and result.get("data") is not None:
            print(formatter(result["data"]))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
