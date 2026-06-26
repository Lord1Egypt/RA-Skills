#!/usr/bin/env python3
"""
team-weekly 工作日志管理模块

提供工作日志的增删查改功能，支持自然语言输入解析。
"""

import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from utils import (
    check_subscription,
    create_base_parser,
    ensure_data_dir,
    generate_id,
    get_worklog_file,
    load_json_file,
    now_str,
    output_error,
    output_success,
    parse_date,
    read_input_data,
    save_json_file,
    today_str,
)
from team_store import get_member_by_name, _load_team


# ============================================================
# 工作分类
# ============================================================

VALID_CATEGORIES = ["开发", "设计", "测试", "会议", "其他"]


# ============================================================
# 工作日志数据操作
# ============================================================

def _load_worklogs() -> List[Dict[str, Any]]:
    """加载所有工作日志。"""
    data = load_json_file(get_worklog_file())
    if data is None:
        return []
    if isinstance(data, list):
        return data
    return data.get("logs", [])


def _save_worklogs(logs: List[Dict[str, Any]]) -> None:
    """保存工作日志。"""
    ensure_data_dir()
    save_json_file(get_worklog_file(), logs)


def parse_natural_input(text: str) -> Dict[str, Any]:
    """解析自然语言工作日志输入。

    支持的输入格式示例：
    - "张三今天完成了官网首页设计，耗时6小时"
    - "李四 完成用户模块开发 8h 项目:商城"
    - "王五 设计LOGO 3小时 设计"

    Args:
        text: 自然语言输入文本。

    Returns:
        解析后的字典，包含 member_name, task_description, hours, project, category 等。
    """
    result: Dict[str, Any] = {
        "member_name": None,
        "task_description": None,
        "hours": None,
        "project": None,
        "category": "其他",
        "date": today_str(),
    }

    # 提取成员姓名（假设在句首，中文名2-4字或英文名）
    name_match = re.match(r'^([a-zA-Z\u4e00-\u9fff]{1,10})\s*', text)
    if name_match:
        result["member_name"] = name_match.group(1)

    # 提取工时
    hours_patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:小时|hours?|hrs?|h)',
        r'耗时\s*(\d+(?:\.\d+)?)',
    ]
    for pattern in hours_patterns:
        hours_match = re.search(pattern, text, re.IGNORECASE)
        if hours_match:
            result["hours"] = float(hours_match.group(1))
            break

    # 提取项目名
    project_match = re.search(r'项目[:：]\s*([^\s,，。]+)', text)
    if project_match:
        result["project"] = project_match.group(1)

    # 提取分类
    for cat in VALID_CATEGORIES:
        if cat in text:
            result["category"] = cat
            break

    # 提取日期
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    if date_match:
        result["date"] = date_match.group(1)
    elif "今天" in text:
        result["date"] = today_str()
    elif "昨天" in text:
        from datetime import timedelta
        yesterday = datetime.now() - timedelta(days=1)
        result["date"] = yesterday.strftime("%Y-%m-%d")

    # 提取任务描述（去除已解析的部分，取主要内容）
    desc = text
    # 移除成员名
    if result["member_name"]:
        desc = desc.replace(result["member_name"], "", 1)
    # 移除工时信息
    for pattern in hours_patterns:
        desc = re.sub(pattern, "", desc, flags=re.IGNORECASE)
    # 移除项目信息
    desc = re.sub(r'项目[:：]\s*[^\s,，。]+', '', desc)
    # 移除日期和时间词
    desc = re.sub(r'\d{4}-\d{2}-\d{2}', '', desc)
    desc = re.sub(r'(今天|昨天|耗时)', '', desc)
    # 清理
    desc = re.sub(r'[,，。\s]+', ' ', desc).strip()
    desc = re.sub(r'^(完成了?|做了?)\s*', '', desc).strip()
    if desc:
        result["task_description"] = desc

    return result


def add_worklog(data: Dict[str, Any]) -> Dict[str, Any]:
    """添加工作日志。

    Args:
        data: 包含以下字段的字典：
            - member_name (str): 成员姓名（必填）
            - task_description (str): 任务描述（必填）
            - date (str, optional): 日期，默认今天
            - hours (float, optional): 工时
            - project (str, optional): 项目名称
            - category (str, optional): 分类，默认"其他"
            - natural_input (str, optional): 自然语言输入，优先解析

    Returns:
        创建的工作日志记录。
    """
    # 如果有自然语言输入，先解析
    natural_input = data.get("natural_input")
    if natural_input:
        parsed = parse_natural_input(natural_input)
        # 解析结果作为默认值，显式传入的字段优先
        for key, value in parsed.items():
            if value is not None and key not in data:
                data[key] = value

    member_name = data.get("member_name")
    task_description = data.get("task_description")

    if not member_name:
        raise ValueError("请提供成员姓名（member_name 字段）")
    if not task_description:
        raise ValueError("请提供任务描述（task_description 字段）")

    # 验证成员是否存在
    team = _load_team()
    if team:
        member = get_member_by_name(member_name)
        if not member:
            raise ValueError(
                f"成员 {member_name!r} 不存在。"
                f"请先使用 add-member 添加成员。"
            )
        member_id = member["id"]
    else:
        member_id = generate_id()

    # 校验分类
    category = data.get("category", "其他")
    if category not in VALID_CATEGORIES:
        category = "其他"

    # 校验日期
    date = data.get("date", today_str())
    parse_date(date)  # 验证格式

    log_entry = {
        "id": generate_id(),
        "member_id": member_id,
        "member_name": member_name,
        "date": date,
        "task_description": task_description,
        "project": data.get("project", ""),
        "hours": float(data.get("hours", 0)),
        "category": category,
        "created_at": now_str(),
    }

    logs = _load_worklogs()
    logs.append(log_entry)
    _save_worklogs(logs)

    return log_entry


def list_worklogs(data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """查询工作日志列表。

    Args:
        data: 可选过滤条件字典：
            - member_name (str, optional): 按成员筛选
            - date (str, optional): 按日期筛选
            - date_from (str, optional): 起始日期
            - date_to (str, optional): 结束日期
            - project (str, optional): 按项目筛选
            - category (str, optional): 按分类筛选

    Returns:
        包含日志列表和统计信息的字典。
    """
    logs = _load_worklogs()

    if data:
        # 按成员筛选
        member_name = data.get("member_name")
        if member_name:
            logs = [l for l in logs if l["member_name"] == member_name]

        # 按日期筛选
        date = data.get("date")
        if date:
            logs = [l for l in logs if l["date"] == date]

        # 按日期范围筛选
        date_from = data.get("date_from")
        date_to = data.get("date_to")
        if date_from:
            logs = [l for l in logs if l["date"] >= date_from]
        if date_to:
            logs = [l for l in logs if l["date"] <= date_to]

        # 按项目筛选
        project = data.get("project")
        if project:
            logs = [l for l in logs if l.get("project") == project]

        # 按分类筛选
        category = data.get("category")
        if category:
            logs = [l for l in logs if l.get("category") == category]

    # 按日期倒序排列
    logs.sort(key=lambda x: x["date"], reverse=True)

    total_hours = sum(l.get("hours", 0) for l in logs)

    return {
        "total_count": len(logs),
        "total_hours": total_hours,
        "logs": logs,
    }


def query_worklogs(data: Dict[str, Any]) -> Dict[str, Any]:
    """高级查询工作日志，支持按周/月聚合。

    Args:
        data: 查询条件字典：
            - week (str, optional): 周标识，如 "2024-W03" 或 "this" 或 "last"
            - month (str, optional): 月标识，如 "2024-01" 或 "this" 或 "last"
            - member_name (str, optional): 按成员筛选
            - project (str, optional): 按项目筛选
            - group_by (str, optional): 分组方式 (member/project/category/date)

    Returns:
        查询结果和聚合统计。
    """
    from datetime import timedelta
    import calendar

    logs = _load_worklogs()
    now = datetime.now()

    # 解析周
    week = data.get("week")
    if week:
        if week == "this":
            monday = now - timedelta(days=now.weekday())
            sunday = monday + timedelta(days=6)
        elif week == "last":
            monday = now - timedelta(days=now.weekday() + 7)
            sunday = monday + timedelta(days=6)
        else:
            # 解析 YYYY-WNN 格式
            try:
                parts = week.split("-W")
                year = int(parts[0])
                week_num = int(parts[1])
                # ISO 周一
                jan1 = datetime(year, 1, 1)
                start_of_week1 = jan1 - timedelta(days=jan1.isoweekday() - 1)
                monday = start_of_week1 + timedelta(weeks=week_num - 1)
                sunday = monday + timedelta(days=6)
            except (ValueError, IndexError):
                raise ValueError(f"无效的周标识: {week!r}，请使用 YYYY-WNN 格式")

        date_from = monday.strftime("%Y-%m-%d")
        date_to = sunday.strftime("%Y-%m-%d")
        logs = [l for l in logs if date_from <= l["date"] <= date_to]

    # 解析月
    month = data.get("month")
    if month:
        if month == "this":
            year, mon = now.year, now.month
        elif month == "last":
            if now.month == 1:
                year, mon = now.year - 1, 12
            else:
                year, mon = now.year, now.month - 1
        else:
            try:
                parts = month.split("-")
                year, mon = int(parts[0]), int(parts[1])
            except (ValueError, IndexError):
                raise ValueError(f"无效的月标识: {month!r}，请使用 YYYY-MM 格式")

        _, last_day = calendar.monthrange(year, mon)
        date_from = f"{year:04d}-{mon:02d}-01"
        date_to = f"{year:04d}-{mon:02d}-{last_day:02d}"
        logs = [l for l in logs if date_from <= l["date"] <= date_to]

    # 按成员筛选
    member_name = data.get("member_name")
    if member_name:
        logs = [l for l in logs if l["member_name"] == member_name]

    # 按项目筛选
    project = data.get("project")
    if project:
        logs = [l for l in logs if l.get("project") == project]

    # 分组聚合
    group_by = data.get("group_by")
    groups: Dict[str, Any] = {}

    if group_by:
        for log in logs:
            if group_by == "member":
                key = log["member_name"]
            elif group_by == "project":
                key = log.get("project", "未分类")
            elif group_by == "category":
                key = log.get("category", "其他")
            elif group_by == "date":
                key = log["date"]
            else:
                key = "全部"

            if key not in groups:
                groups[key] = {"count": 0, "hours": 0, "logs": []}
            groups[key]["count"] += 1
            groups[key]["hours"] += log.get("hours", 0)
            groups[key]["logs"].append(log)

    total_hours = sum(l.get("hours", 0) for l in logs)

    result = {
        "total_count": len(logs),
        "total_hours": total_hours,
        "logs": logs,
    }

    if groups:
        # 返回摘要（不含具体日志以减少体积）
        result["groups"] = {
            k: {"count": v["count"], "hours": v["hours"]}
            for k, v in groups.items()
        }

    return result


def delete_worklog(data: Dict[str, Any]) -> Dict[str, Any]:
    """删除工作日志。

    Args:
        data: 包含以下字段的字典：
            - id (str): 日志 ID（必填）

    Returns:
        被删除的日志记录。
    """
    log_id = data.get("id")
    if not log_id:
        raise ValueError("请提供日志 ID（id 字段）")

    logs = _load_worklogs()
    removed = None
    new_logs = []

    for log in logs:
        if log["id"] == log_id:
            removed = log
        else:
            new_logs.append(log)

    if not removed:
        raise ValueError(f"未找到日志: {log_id}")

    _save_worklogs(new_logs)
    return removed


# ============================================================
# 命令行入口
# ============================================================

def main() -> None:
    """命令行入口函数。"""
    parser = create_base_parser("工作日志管理工具")
    args, _ = parser.parse_known_args()

    try:
        action = args.action

        if action == "add":
            data = read_input_data(args)
            result = add_worklog(data)
            output_success(result)

        elif action == "list":
            try:
                data = read_input_data(args)
            except ValueError:
                data = None
            result = list_worklogs(data)
            output_success(result)

        elif action == "query":
            data = read_input_data(args)
            result = query_worklogs(data)
            output_success(result)

        elif action == "delete":
            data = read_input_data(args)
            result = delete_worklog(data)
            output_success(result)

        else:
            output_error(f"未知操作: {action}", "UNKNOWN_ACTION")

    except (ValueError, PermissionError) as e:
        output_error(str(e), type(e).__name__.upper())
    except Exception as e:
        output_error(f"内部错误: {e}", "INTERNAL_ERROR")


if __name__ == "__main__":
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
