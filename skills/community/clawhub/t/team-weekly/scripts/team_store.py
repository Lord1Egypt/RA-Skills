#!/usr/bin/env python3
"""
team-weekly 团队与成员管理模块

提供团队创建、成员增删改查等功能，数据以 JSON 格式存储在本地。
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from utils import (
    check_subscription,
    create_base_parser,
    ensure_data_dir,
    generate_id,
    get_team_file,
    load_json_file,
    now_str,
    output_error,
    output_success,
    read_input_data,
    save_json_file,
)


# ============================================================
# 团队数据操作
# ============================================================

def _load_team() -> Optional[Dict[str, Any]]:
    """加载团队数据。"""
    return load_json_file(get_team_file())


def _save_team(team: Dict[str, Any]) -> None:
    """保存团队数据。"""
    save_json_file(get_team_file(), team)


def init_team(data: Dict[str, Any]) -> Dict[str, Any]:
    """初始化团队。

    Args:
        data: 包含以下字段的字典：
            - name (str): 团队名称（必填）
            - members (list, optional): 初始成员列表

    Returns:
        创建后的团队数据。

    Raises:
        ValueError: 缺少必填字段时抛出。
    """
    name = data.get("name")
    if not name:
        raise ValueError("请提供团队名称（name 字段）")

    ensure_data_dir()

    # 检查是否已存在团队
    existing = _load_team()
    if existing:
        raise ValueError(
            f"团队已存在: {existing['name']}。"
            f"如需重新创建，请先删除现有团队数据。"
        )

    sub = check_subscription()

    team = {
        "id": generate_id(),
        "name": name,
        "members": [],
        "created_at": now_str(),
        "updated_at": now_str(),
        "subscription_tier": sub["tier"],
    }

    # 如果提供了初始成员列表，逐个添加
    initial_members = data.get("members", [])
    for member_data in initial_members:
        if isinstance(member_data, str):
            member_data = {"name": member_data}
        _add_member_to_team(team, member_data, sub)

    _save_team(team)
    return team


def _add_member_to_team(
    team: Dict[str, Any],
    member_data: Dict[str, Any],
    sub: Dict[str, Any],
) -> Dict[str, Any]:
    """向团队添加成员（内部方法）。

    Args:
        team: 团队数据。
        member_data: 成员数据，包含 name, role, projects 等。
        sub: 订阅信息。

    Returns:
        新添加的成员数据。

    Raises:
        ValueError: 超出人数限制或缺少必填字段时抛出。
    """
    max_members = sub["max_members"]
    current_count = len(team["members"])

    if current_count >= max_members:
        raise ValueError(
            f"团队成员已达上限（{max_members}人）。"
            f"当前订阅等级为{sub['tier']}，"
            + (
                "如需更多成员请升级至付费版（¥69/月）。"
                if sub["tier"] == "free"
                else "已达付费版最大成员数。"
            )
        )

    name = member_data.get("name")
    if not name:
        raise ValueError("请提供成员姓名（name 字段）")

    # 检查重名
    for m in team["members"]:
        if m["name"] == name:
            raise ValueError(f"成员 {name!r} 已存在")

    member = {
        "id": generate_id(),
        "name": name,
        "role": member_data.get("role", "成员"),
        "projects": member_data.get("projects", []),
        "created_at": now_str(),
    }

    team["members"].append(member)
    team["updated_at"] = now_str()
    return member


def add_member(data: Dict[str, Any]) -> Dict[str, Any]:
    """添加团队成员。

    Args:
        data: 包含以下字段的字典：
            - name (str): 成员姓名（必填）
            - role (str, optional): 角色，默认"成员"
            - projects (list, optional): 参与的项目列表

    Returns:
        新添加的成员数据。
    """
    team = _load_team()
    if not team:
        raise ValueError("团队尚未初始化，请先执行 init 操作")

    sub = check_subscription()
    member = _add_member_to_team(team, data, sub)
    _save_team(team)
    return member


def remove_member(data: Dict[str, Any]) -> Dict[str, Any]:
    """移除团队成员。

    Args:
        data: 包含以下字段的字典：
            - name (str) 或 id (str): 成员姓名或 ID（二选一）

    Returns:
        被移除的成员数据。
    """
    team = _load_team()
    if not team:
        raise ValueError("团队尚未初始化，请先执行 init 操作")

    member_name = data.get("name")
    member_id = data.get("id")

    if not member_name and not member_id:
        raise ValueError("请提供成员姓名（name）或 ID（id）")

    removed = None
    new_members = []
    for m in team["members"]:
        if (member_name and m["name"] == member_name) or \
           (member_id and m["id"] == member_id):
            removed = m
        else:
            new_members.append(m)

    if not removed:
        identifier = member_name or member_id
        raise ValueError(f"未找到成员: {identifier}")

    team["members"] = new_members
    team["updated_at"] = now_str()
    _save_team(team)
    return removed


def list_members() -> Dict[str, Any]:
    """列出所有团队成员。

    Returns:
        包含团队信息和成员列表的字典。
    """
    team = _load_team()
    if not team:
        raise ValueError("团队尚未初始化，请先执行 init 操作")

    sub = check_subscription()
    return {
        "team_name": team["name"],
        "team_id": team["id"],
        "subscription_tier": sub["tier"],
        "max_members": sub["max_members"],
        "current_count": len(team["members"]),
        "members": team["members"],
    }


def get_team() -> Dict[str, Any]:
    """获取完整的团队信息。

    Returns:
        团队完整数据。
    """
    team = _load_team()
    if not team:
        raise ValueError("团队尚未初始化，请先执行 init 操作")
    return team


def get_member_by_name(name: str) -> Optional[Dict[str, Any]]:
    """通过姓名查找成员。

    Args:
        name: 成员姓名。

    Returns:
        成员数据，未找到返回 None。
    """
    team = _load_team()
    if not team:
        return None
    for m in team["members"]:
        if m["name"] == name:
            return m
    return None


# ============================================================
# 命令行入口
# ============================================================

def main() -> None:
    """命令行入口函数。"""
    parser = create_base_parser("团队与成员管理工具")
    args, _ = parser.parse_known_args()

    try:
        action = args.action

        if action == "init":
            data = read_input_data(args)
            result = init_team(data)
            output_success(result)

        elif action == "add-member":
            data = read_input_data(args)
            result = add_member(data)
            output_success(result)

        elif action == "remove-member":
            data = read_input_data(args)
            result = remove_member(data)
            output_success(result)

        elif action == "list":
            result = list_members()
            output_success(result)

        elif action == "get-team":
            result = get_team()
            output_success(result)

        else:
            output_error(f"未知操作: {action}", "UNKNOWN_ACTION")

    except (ValueError, PermissionError) as e:
        output_error(str(e), type(e).__name__.upper())
    except Exception as e:
        output_error(f"内部错误: {e}", "INTERNAL_ERROR")


if __name__ == "__main__":
    # 将脚本目录加入 sys.path，确保可以导入同目录模块
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
