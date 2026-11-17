"""
Virsical 工单管理模块。

提供工单参数查询、项目位置查询、工单创建等功能。
"""

import json
import sys
from typing import Optional

from .virsical_client import VirsicalClient


def _filter_none(obj):
    """递归过滤字典中的 None 值。"""
    if isinstance(obj, dict):
        return {k: _filter_none(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [_filter_none(item) for item in obj]
    return obj


def get_requirement_params() -> dict:
    """获取工单创建参数。

    包括项目列表、工单类型、优先级选项等。

    Returns:
        工单参数数据（字段: project, requirementType, priority）
    """
    client = VirsicalClient()
    return client.get("/vsk/fm-service/api/requirement/paramsPacking")


def get_requirement_locations(project_id: str) -> list:
    """获取项目空间位置列表。

    Args:
        project_id: 项目 ID

    Returns:
        位置列表 [{id, pathName}, ...]
    """
    client = VirsicalClient()
    result = client.get("/vsk/fm-service/api/projectSpace/id", query={"projectId": project_id})

    data = result.get("data", result.get("result", result))
    if isinstance(data, dict):
        data = data.get("records", data.get("list", []))

    return _extract_locations(data)


def _extract_locations(nodes: list) -> list:
    """递归提取位置树中的 id 和 pathName。

    Args:
        nodes: 位置节点列表

    Returns:
        扁平化的位置列表
    """
    result = []
    for node in nodes:
        result.append({
            "id": node.get("id", ""),
            "pathName": node.get("pathName", ""),
            "name": node.get("name", ""),
        })
        children = node.get("children", [])
        if children:
            result.extend(_extract_locations(children))
    return result


def create_requirement(
    project_id: str,
    content: str,
    requirement_type_id: str,
    priority: str = "medium",
    location_ids: Optional[list] = None,
) -> dict:
    """创建工单。

    Args:
        project_id: 项目 ID（字符串）
        content: 工单内容描述
        requirement_type_id: 工单类型 ID（字符串）
        priority: 优先级，支持整数 ID（从 get_requirement_params() 动态获取）
                  或字符串别名（"high"/"medium"/"low"）
                  别名映射："high"→"紧急", "medium"→"普通", "low"→"预约"
        location_ids: 位置 ID 列表

    Returns:
        创建结果
    """
    # 先检查是否有必要的参数配置
    params = get_requirement_params()
    data = params.get("data", {})
    projects = data.get("project", [])
    types = data.get("requirementType", [])
    priorities = data.get("priority", [])

    if not projects:
        return {
            "success": False,
            "message": "暂无可用项目，请先在威思客系统中配置项目信息",
        }
    if not types:
        return {
            "success": False,
            "message": "暂无可用工单类型，请先在威思客系统中配置工单类型",
        }

    client = VirsicalClient()

    # 优先级：支持数字 ID 直接传入，也支持字符串别名，最终转为字符串
    if isinstance(priority, int) or (isinstance(priority, str) and priority.isdigit()):
        priority_id = str(priority)
    else:
        priority_name_map = {
            "high": "紧急",
            "medium": "普通",
            "low": "预约",
        }
        target_priority_name = priority_name_map.get(str(priority), "普通")
        priority_id = None
        for p in priorities:
            if p.get("priorityName") == target_priority_name:
                priority_id = str(p.get("id", ""))
                break
        if priority_id is None and priorities:
            priority_id = str(priorities[0].get("id", ""))
    
    body = {
        "projectId": project_id,
        "requirementContent": content,
        "requirementTypeId": requirement_type_id,
        "priority": priority_id,
        "entranceSource": "ai",
    }

    # 注意：requirementLocations 在测试环境会导致 400，暂不传
    result = client.post("/vsk/fm-service/api/requirement/create/v2", body=body)

    code = result.get("code", result.get("status", -1))
    if code == 0 or code == "0" or result.get("success"):
        # 反查项目名、类型名、优先级名，便于上层呈现
        project_name = ""
        for p in projects:
            if str(p.get("id", "")) == str(project_id):
                project_name = p.get("projectName", p.get("name", ""))
                break

        type_name = ""
        for t in types:
            if str(t.get("id", "")) == str(requirement_type_id):
                type_name = t.get("name", "")
                break

        priority_name = ""
        for p in priorities:
            if str(p.get("id", "")) == str(priority_id):
                priority_name = p.get("priorityName", "")
                break

        response_data = result.get("data", result)
        if isinstance(response_data, dict):
            requirement_no = response_data.get("requirementNo") or response_data.get("id", "")
        else:
            requirement_no = str(response_data) if response_data else ""
        return {
            "success": True,
            "message": "工单创建成功",
            "data": {
                "id": response_data.get("id", response_data) if isinstance(response_data, dict) else response_data,
                "requirementNo": requirement_no,
                "projectName": project_name,
                "typeName": type_name,
                "priorityName": priority_name,
                "content": content,
            },
        }
    else:
        msg = result.get("msg", result.get("message", f"创建失败 (code: {code})"))
        return {
            "success": False,
            "message": msg,
        }


def format_params(params: dict) -> str:
    """格式化工单参数为可读文本。

    Args:
        params: get_requirement_params 的返回结果

    Returns:
        格式化的参数文本
    """
    lines = []
    data = params.get("data", params)

    # 项目列表
    projects = data.get("project", [])
    if projects:
        lines.append("## 可选项目")
        for proj in projects:
            name = proj.get("projectName", proj.get("name", ""))
            pid = proj.get("id", "")
            lines.append(f"- {name} (ID: {pid})")
    else:
        lines.append("⚠️  **暂无可用项目**")
        lines.append("   请先在威思客系统中配置项目信息")

    # 工单类型（按项目分组）
    types = data.get("requirementType", [])
    if types:
        lines.append("\n## 工单类型")
        for t in types:
            name = t.get("name", "")
            tid = t.get("id", "")
            pid = t.get("projectId", "")
            lines.append(f"- {name} (ID: {tid}, 项目: {pid})")
    else:
        lines.append("\n⚠️  **暂无可用工单类型**")
        lines.append("   请先在威思客系统中配置工单类型")

    # 优先级
    priorities = data.get("priority", [])
    if priorities:
        lines.append("\n## 优先级")
        for p in priorities:
            lines.append(f"- {p.get('priorityName', '')} (ID: {p.get('id', '')})")

    return "\n".join(lines) if lines else "暂无参数数据"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python requirement.py params")
        print("  python requirement.py locations <project_id>")
        print("  python requirement.py create <project_id> <content> <type_id> [priority]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "params":
        result = get_requirement_params()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif action == "locations":
        if len(sys.argv) < 3:
            print("Error: project_id required")
            sys.exit(1)
        result = get_requirement_locations(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif action == "create":
        if len(sys.argv) < 5:
            print("Error: project_id, content, type_id required")
            sys.exit(1)
        priority = sys.argv[5] if len(sys.argv) > 5 else "medium"
        result = create_requirement(
            project_id=sys.argv[2],
            content=sys.argv[3],
            requirement_type_id=sys.argv[4],
            priority=priority,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
