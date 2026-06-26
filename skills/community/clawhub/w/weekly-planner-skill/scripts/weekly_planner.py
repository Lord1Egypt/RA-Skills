#!/usr/bin/env python3
"""
周记录整理脚本
功能：增删改查记录、查询今日/本周/按类别、导出周报
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from dateutil import parser
from pathlib import Path


# 数据存储目录
DATA_DIR = "./weekly-plans"


def get_week_file_path(year, week):
    """获取周数据文件路径"""
    return os.path.join(DATA_DIR, f"week-{year}-W{week:02d}.json")


def ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)


def get_week_start_end(year, week):
    """
    计算指定年份和周次的开始和结束日期
    使用ISO周次标准（周一为每周第一天）
    """
    # 找到该年的第一个周一
    jan1 = datetime(year, 1, 1)
    if jan1.weekday() != 0:
        days_to_monday = (0 - jan1.weekday()) % 7
        first_monday = jan1 + timedelta(days=days_to_monday)
    else:
        first_monday = jan1

    week_start = first_monday + timedelta(weeks=week - 1)
    week_end = week_start + timedelta(days=6)

    return week_start.strftime("%Y-%m-%d"), week_end.strftime("%Y-%m-%d")


def create_week_data(year, week):
    """创建新的周数据结构"""
    start_date, end_date = get_week_start_end(year, week)
    return {
        "year": year,
        "week": week,
        "start_date": start_date,
        "end_date": end_date,
        "plans": [],
        "completions": [],
        "reflections": []
    }


def load_week_data(year, week):
    """加载周数据，如果不存在则创建"""
    ensure_data_dir()
    file_path = get_week_file_path(year, week)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return create_week_data(year, week)


def save_week_data(year, week, data):
    """保存周数据到文件"""
    ensure_data_dir()
    file_path = get_week_file_path(year, week)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return file_path


def get_next_task_id(data):
    """获取下一个任务ID（跳过已删除的）"""
    used_ids = [p["id"] for p in data["plans"] if not p.get("deleted", False)]
    if not used_ids:
        return 1
    return max(used_ids) + 1


def add_plan(year, week, task, category, date, priority="medium"):
    """
    添加周计划任务
    参数：
        year: 年份
        week: 周次
        task: 任务描述
        category: 任务类别（work/study/health/other）
        date: 分配日期（YYYY-MM-DD格式）
        priority: 优先级（high/medium/low）
    """
    data = load_week_data(year, week)

    task_id = get_next_task_id(data)

    # 验证日期
    start_date = data["start_date"]
    end_date = data["end_date"]
    if date < start_date or date > end_date:
        print(f"警告：日期 {date} 不在周范围内（{start_date} 至 {end_date}）")

    plan = {
        "id": task_id,
        "task": task,
        "category": category,
        "assigned_date": date,
        "status": "pending",
        "priority": priority,
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "updated_at": None,
        "deleted": False
    }

    data["plans"].append(plan)
    file_path = save_week_data(year, week, data)

    return {
        "success": True,
        "task_id": task_id,
        "file": file_path,
        "message": f"任务已添加：ID={task_id}, 任务={task}, 日期={date}"
    }


def update_plan(year, week, task_id, field, value):
    """
    更新计划任务
    参数：
        year: 年份
        week: 周次
        task_id: 任务ID
        field: 要更新的字段（task/category/date/priority）
        value: 新值
    """
    data = load_week_data(year, week)

    task = None
    for p in data["plans"]:
        if p["id"] == task_id and not p.get("deleted", False):
            task = p
            break

    if not task:
        return {
            "success": False,
            "message": f"未找到任务ID {task_id}"
        }

    valid_fields = ["task", "category", "date", "priority"]
    if field not in valid_fields:
        return {
            "success": False,
            "message": f"无效的字段 {field}，可选：{', '.join(valid_fields)}"
        }

    # 特殊验证
    if field == "date":
        start_date = data["start_date"]
        end_date = data["end_date"]
        if value < start_date or value > end_date:
            return {
                "success": False,
                "message": f"日期 {value} 不在周范围内（{start_date} 至 {end_date}）"
            }

    task[field] = value
    task["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    file_path = save_week_data(year, week, data)

    return {
        "success": True,
        "task_id": task_id,
        "field": field,
        "new_value": value,
        "file": file_path,
        "message": f"任务已更新：ID={task_id}, {field}={value}"
    }


def delete_plan(year, week, task_id):
    """
    删除计划任务（软删除）
    参数：
        year: 年份
        week: 周次
        task_id: 任务ID
    """
    data = load_week_data(year, week)

    task = None
    for p in data["plans"]:
        if p["id"] == task_id and not p.get("deleted", False):
            task = p
            break

    if not task:
        return {
            "success": False,
            "message": f"未找到任务ID {task_id}"
        }

    # 软删除
    task["deleted"] = True
    task["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # 删除关联的完成记录
    data["completions"] = [c for c in data["completions"] if c["task_id"] != task_id]

    file_path = save_week_data(year, week, data)

    return {
        "success": True,
        "task_id": task_id,
        "file": file_path,
        "message": f"任务已删除：ID={task_id}"
    }


def add_completion(year, week, task_id, notes="", progress=100):
    """
    记录任务完成
    参数：
        year: 年份
        week: 周次
        task_id: 任务ID
        notes: 完成备注
        progress: 完成进度（0-100）
    """
    data = load_week_data(year, week)

    task = None
    for p in data["plans"]:
        if p["id"] == task_id and not p.get("deleted", False):
            task = p
            break

    if not task:
        return {
            "success": False,
            "message": f"未找到任务ID {task_id}"
        }

    task["status"] = "completed"
    task["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    completion = {
        "task_id": task_id,
        "task": task["task"],
        "category": task["category"],
        "assigned_date": task["assigned_date"],
        "completed_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "notes": notes,
        "progress": progress
    }

    data["completions"].append(completion)
    file_path = save_week_data(year, week, data)

    return {
        "success": True,
        "task_id": task_id,
        "task": task["task"],
        "file": file_path,
        "message": f"任务完成已记录：{task['task']}"
    }


def undo_completion(year, week, task_id):
    """
    撤销任务完成
    参数：
        year: 年份
        week: 周次
        task_id: 任务ID
    """
    data = load_week_data(year, week)

    task = None
    for p in data["plans"]:
        if p["id"] == task_id and not p.get("deleted", False):
            task = p
            break

    if not task:
        return {
            "success": False,
            "message": f"未找到任务ID {task_id}"
        }

    task["status"] = "pending"
    task["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # 删除完成记录
    original_count = len(data["completions"])
    data["completions"] = [c for c in data["completions"] if c["task_id"] != task_id]

    if len(data["completions"]) == original_count:
        return {
            "success": False,
            "message": f"任务ID {task_id} 没有完成记录"
        }

    file_path = save_week_data(year, week, data)

    return {
        "success": True,
        "task_id": task_id,
        "file": file_path,
        "message": f"任务完成已撤销：{task['task']}"
    }


def change_date(year, week, task_id, new_date):
    """
    调整任务日期
    参数：
        year: 年份
        week: 周次
        task_id: 任务ID
        new_date: 新日期（YYYY-MM-DD格式）
    """
    return update_plan(year, week, task_id, "date", new_date)


def add_reflection(year, week, date, content):
    """
    记录反思内容
    参数：
        year: 年份
        week: 周次
        date: 日期（YYYY-MM-DD格式）
        content: 反思内容
    """
    data = load_week_data(year, week)

    # 查找是否已存在该日期的反思
    existing_reflection = None
    for r in data["reflections"]:
        if r["date"] == date:
            existing_reflection = r
            break

    if existing_reflection:
        existing_reflection["content"] += f"\n{content}"
        existing_reflection["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    else:
        reflection = {
            "date": date,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }
        data["reflections"].append(reflection)

    file_path = save_week_data(year, week, data)

    return {
        "success": True,
        "date": date,
        "file": file_path,
        "message": f"反思已记录：{date}"
    }


def query_today(year, week, date):
    """
    查询今日情况
    参数：
        year: 年份
        week: 周次
        date: 日期（YYYY-MM-DD格式）
    """
    data = load_week_data(year, week)

    # 筛选今日数据
    today_plans = [p for p in data["plans"] if p["assigned_date"] == date and not p.get("deleted", False)]
    today_completions = [c for c in data["completions"] if c["assigned_date"] == date]
    today_reflection = None
    for r in data["reflections"]:
        if r["date"] == date:
            today_reflection = r
            break

    # 统计
    total = len(today_plans)
    completed = len([p for p in today_plans if p["status"] == "completed"])
    completion_rate = (completed / total * 100) if total > 0 else 0

    return {
        "success": True,
        "date": date,
        "summary": {
            "total_plans": total,
            "completed": completed,
            "completion_rate": round(completion_rate, 2)
        },
        "plans": today_plans,
        "completions": today_completions,
        "reflection": today_reflection
    }


def query_week(year, week):
    """
    查询本周整体情况
    参数：
        year: 年份
        week: 周次
    """
    data = load_week_data(year, week)

    # 按日期分组
    daily_data = {}
    current_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        daily_data[date_str] = {
            "plans": [p for p in data["plans"] if p["assigned_date"] == date_str and not p.get("deleted", False)],
            "completions": [c for c in data["completions"] if c["assigned_date"] == date_str],
            "reflections": [r for r in data["reflections"] if r["date"] == date_str]
        }
        current_date += timedelta(days=1)

    # 统计
    active_plans = [p for p in data["plans"] if not p.get("deleted", False)]
    total = len(active_plans)
    completed = len([p for p in active_plans if p["status"] == "completed"])

    return {
        "success": True,
        "year": year,
        "week": week,
        "start_date": data["start_date"],
        "end_date": data["end_date"],
        "summary": {
            "total_plans": total,
            "completed": completed,
            "completion_rate": round((completed / total * 100) if total > 0 else 0, 2)
        },
        "daily_data": daily_data,
        "reflections": data["reflections"]
    }


def query_by_category(year, week, category):
    """
    按类别查询
    参数：
        year: 年份
        week: 周次
        category: 类别（work/study/health/other）
    """
    data = load_week_data(year, week)

    # 筛选类别数据
    category_plans = [p for p in data["plans"] if p["category"] == category and not p.get("deleted", False)]
    category_completions = [c for c in data["completions"] if c["category"] == category]

    # 统计
    total = len(category_plans)
    completed = len([p for p in category_plans if p["status"] == "completed"])

    return {
        "success": True,
        "category": category,
        "summary": {
            "total": total,
            "completed": completed,
            "completion_rate": round((completed / total * 100) if total > 0 else 0, 2)
        },
        "plans": category_plans,
        "completions": category_completions
    }


def get_week_data(year, week):
    """获取周数据（原始数据）"""
    data = load_week_data(year, week)
    file_path = get_week_file_path(year, week)

    return {
        "success": True,
        "file": file_path,
        "data": data
    }


def export_week_report(year, week):
    """
    导出周报数据
    参数：
        year: 年份
        week: 周次
    """
    data = load_week_data(year, week)

    active_plans = [p for p in data["plans"] if not p.get("deleted", False)]
    total_plans = len(active_plans)
    completed_tasks = [c for c in data["completions"]]
    completed_count = len(completed_tasks)
    completion_rate = (completed_count / total_plans * 100) if total_plans > 0 else 0

    # 按类别统计
    category_stats = {}
    for plan in active_plans:
        cat = plan["category"]
        if cat not in category_stats:
            category_stats[cat] = {"total": 0, "completed": 0}
        category_stats[cat]["total"] += 1

    for comp in data["completions"]:
        cat = comp["category"]
        if cat in category_stats:
            category_stats[cat]["completed"] += 1

    # 按日期统计
    daily_stats = {}
    current_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        daily_stats[date_str] = {
            "plans": [p for p in active_plans if p["assigned_date"] == date_str],
            "completions": [c for c in data["completions"] if c["assigned_date"] == date_str],
            "reflection": next((r for r in data["reflections"] if r["date"] == date_str), None)
        }
        current_date += timedelta(days=1)

    return {
        "success": True,
        "summary": {
            "year": year,
            "week": week,
            "start_date": data["start_date"],
            "end_date": data["end_date"],
            "total_plans": total_plans,
            "completed_count": completed_count,
            "completion_rate": round(completion_rate, 2)
        },
        "category_stats": category_stats,
        "daily_stats": daily_stats,
        "plans": active_plans,
        "completions": completed_tasks,
        "reflections": data["reflections"]
    }


def generate_daily_report(year, week, date):
    """
    生成工作日报
    参数：
        year: 年份
        week: 周次
        date: 日期（YYYY-MM-DD格式）
    """
    # 获取当日数据
    today_data = query_today(year, week, date)

    if not today_data["success"]:
        return {
            "success": False,
            "message": "获取今日数据失败"
        }

    # 计算星期
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekdays[date_obj.weekday()]

    # 判断是否为工作日
    is_weekday = date_obj.weekday() < 5  # 0-4为工作日

    # 按优先级分组任务
    high_priority = [p for p in today_data["plans"] if p["priority"] == "high"]
    medium_priority = [p for p in today_data["plans"] if p["priority"] == "medium"]
    low_priority = [p for p in today_data["plans"] if p["priority"] == "low"]

    # 统计完成情况
    high_completed = len([p for p in high_priority if p["status"] == "completed"])
    medium_completed = len([p for p in medium_priority if p["status"] == "completed"])
    low_completed = len([p for p in low_priority if p["status"] == "completed"])

    return {
        "success": True,
        "report_info": {
            "date": date,
            "weekday": weekday,
            "is_weekday": is_weekday,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "summary": today_data["summary"],
        "priority_breakdown": {
            "high": {
                "total": len(high_priority),
                "completed": high_completed
            },
            "medium": {
                "total": len(medium_priority),
                "completed": medium_completed
            },
            "low": {
                "total": len(low_priority),
                "completed": low_completed
            }
        },
        "plans": today_data["plans"],
        "completions": today_data["completions"],
        "reflection": today_data["reflection"]
    }


def main():
    parser = argparse.ArgumentParser(description="周记录整理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # add_plan 命令
    add_parser = subparsers.add_parser("add_plan", help="添加计划任务")
    add_parser.add_argument("--year", type=int, required=True, help="年份")
    add_parser.add_argument("--week", type=int, required=True, help="周次")
    add_parser.add_argument("--task", type=str, required=True, help="任务描述")
    add_parser.add_argument("--category", type=str, required=True, help="任务类别")
    add_parser.add_argument("--date", type=str, required=True, help="分配日期(YYYY-MM-DD)")
    add_parser.add_argument("--priority", type=str, default="medium", help="优先级")

    # update_plan 命令
    update_parser = subparsers.add_parser("update_plan", help="更新计划任务")
    update_parser.add_argument("--year", type=int, required=True, help="年份")
    update_parser.add_argument("--week", type=int, required=True, help="周次")
    update_parser.add_argument("--task_id", type=int, required=True, help="任务ID")
    update_parser.add_argument("--field", type=str, required=True, help="要更新的字段")
    update_parser.add_argument("--value", type=str, required=True, help="新值")

    # delete_plan 命令
    delete_parser = subparsers.add_parser("delete_plan", help="删除计划任务")
    delete_parser.add_argument("--year", type=int, required=True, help="年份")
    delete_parser.add_argument("--week", type=int, required=True, help="周次")
    delete_parser.add_argument("--task_id", type=int, required=True, help="任务ID")

    # add_completion 命令
    complete_parser = subparsers.add_parser("add_completion", help="记录任务完成")
    complete_parser.add_argument("--year", type=int, required=True, help="年份")
    complete_parser.add_argument("--week", type=int, required=True, help="周次")
    complete_parser.add_argument("--task_id", type=int, required=True, help="任务ID")
    complete_parser.add_argument("--notes", type=str, default="", help="完成备注")
    complete_parser.add_argument("--progress", type=int, default=100, help="完成进度")

    # undo_completion 命令
    undo_parser = subparsers.add_parser("undo_completion", help="撤销任务完成")
    undo_parser.add_argument("--year", type=int, required=True, help="年份")
    undo_parser.add_argument("--week", type=int, required=True, help="周次")
    undo_parser.add_argument("--task_id", type=int, required=True, help="任务ID")

    # change_date 命令
    change_parser = subparsers.add_parser("change_date", help="调整任务日期")
    change_parser.add_argument("--year", type=int, required=True, help="年份")
    change_parser.add_argument("--week", type=int, required=True, help="周次")
    change_parser.add_argument("--task_id", type=int, required=True, help="任务ID")
    change_parser.add_argument("--new_date", type=str, required=True, help="新日期(YYYY-MM-DD)")

    # add_reflection 命令
    reflection_parser = subparsers.add_parser("add_reflection", help="记录反思")
    reflection_parser.add_argument("--year", type=int, required=True, help="年份")
    reflection_parser.add_argument("--week", type=int, required=True, help="周次")
    reflection_parser.add_argument("--date", type=str, required=True, help="日期(YYYY-MM-DD)")
    reflection_parser.add_argument("--content", type=str, required=True, help="反思内容")

    # query_today 命令
    query_today_parser = subparsers.add_parser("query_today", help="查询今日情况")
    query_today_parser.add_argument("--year", type=int, required=True, help="年份")
    query_today_parser.add_argument("--week", type=int, required=True, help="周次")
    query_today_parser.add_argument("--date", type=str, required=True, help="日期(YYYY-MM-DD)")

    # query_week 命令
    query_week_parser = subparsers.add_parser("query_week", help="查询本周情况")
    query_week_parser.add_argument("--year", type=int, required=True, help="年份")
    query_week_parser.add_argument("--week", type=int, required=True, help="周次")

    # query_by_category 命令
    query_cat_parser = subparsers.add_parser("query_by_category", help="按类别查询")
    query_cat_parser.add_argument("--year", type=int, required=True, help="年份")
    query_cat_parser.add_argument("--week", type=int, required=True, help="周次")
    query_cat_parser.add_argument("--category", type=str, required=True, help="类别")

    # get_week_data 命令
    get_parser = subparsers.add_parser("get_week_data", help="获取周数据")
    get_parser.add_argument("--year", type=int, required=True, help="年份")
    get_parser.add_argument("--week", type=int, required=True, help="周次")

    # export_week_report 命令
    export_parser = subparsers.add_parser("export_week_report", help="导出周报")
    export_parser.add_argument("--year", type=int, required=True, help="年份")
    export_parser.add_argument("--week", type=int, required=True, help="周次")

    # generate_daily_report 命令
    daily_report_parser = subparsers.add_parser("generate_daily_report", help="生成工作日报")
    daily_report_parser.add_argument("--year", type=int, required=True, help="年份")
    daily_report_parser.add_argument("--week", type=int, required=True, help="周次")
    daily_report_parser.add_argument("--date", type=str, required=True, help="日期(YYYY-MM-DD)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 执行对应命令
    if args.command == "add_plan":
        result = add_plan(args.year, args.week, args.task, args.category, args.date, args.priority)
    elif args.command == "update_plan":
        result = update_plan(args.year, args.week, args.task_id, args.field, args.value)
    elif args.command == "delete_plan":
        result = delete_plan(args.year, args.week, args.task_id)
    elif args.command == "add_completion":
        result = add_completion(args.year, args.week, args.task_id, args.notes, args.progress)
    elif args.command == "undo_completion":
        result = undo_completion(args.year, args.week, args.task_id)
    elif args.command == "change_date":
        result = change_date(args.year, args.week, args.task_id, args.new_date)
    elif args.command == "add_reflection":
        result = add_reflection(args.year, args.week, args.date, args.content)
    elif args.command == "query_today":
        result = query_today(args.year, args.week, args.date)
    elif args.command == "query_week":
        result = query_week(args.year, args.week)
    elif args.command == "query_by_category":
        result = query_by_category(args.year, args.week, args.category)
    elif args.command == "get_week_data":
        result = get_week_data(args.year, args.week)
    elif args.command == "export_week_report":
        result = export_week_report(args.year, args.week)
    elif args.command == "generate_daily_report":
        result = generate_daily_report(args.year, args.week, args.date)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
