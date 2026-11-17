#!/usr/bin/env python3
"""历史周报管理器 - 读取归档历史、提取追踪数据、自动归档新周报"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def read_history(weeks: int = 4, history_dir: str = "./weekly_reports/history") -> dict:
    """读取最近N周的历史周报"""
    result = {
        "status": "success",
        "weeks_read": 0,
        "data": {
            "unresolved_issues": [],
            "in_progress_items": [],
            "last_week_metrics": {}
        }
    }

    history_path = Path(history_dir)
    if not history_path.exists():
        return {"status": "success", "data": result["data"], "message": "无历史数据"}

    # 收集所有历史文件
    history_files = []
    for f in history_path.glob("*.md"):
        # 提取周次信息
        match = re.search(r'(\d{4})-W(\d{2,})', f.stem)
        if match:
            year, week = int(match.group(1)), int(match.group(2))
            history_files.append((year, week, f))

    # 按时间排序，取最近N个
    history_files.sort(key=lambda x: (x[0], x[1]), reverse=True)
    recent_files = history_files[:weeks]

    for year, week, file_path in recent_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            week_id = f"{year}-W{week:02d}"
            
            # 提取未解决问题
            in_issues = False
            for line in content.split('\n'):
                if '## 异常与问题' in line or '## 问题' in line:
                    in_issues = True
                elif line.startswith('## ') and in_issues:
                    in_issues = False
                elif in_issues and line.strip() and not line.startswith('#'):
                    if any(kw in line for kw in ['- [ ]', '- [ ] 待', '[进行中]', '持续']):
                        result["data"]["unresolved_issues"].append({
                            "week": week_id,
                            "description": line.strip().lstrip('- *').strip()
                        })
            
            # 提取进行中项目
            in_progress = False
            for line in content.split('\n'):
                if '## 完成事项' in line or '## 进行中' in line:
                    in_progress = True
                elif line.startswith('## ') and in_progress:
                    in_progress = False
                elif in_progress and line.strip() and not line.startswith('#'):
                    if any(kw in line for kw in ['[进行中]', '[持续]', '进行中']):
                        result["data"]["in_progress_items"].append({
                            "week": week_id,
                            "description": line.strip().lstrip('- *').strip()
                        })

            # 提取最新指标（仅最近1周）
            if result["weeks_read"] == 0:
                for line in content.split('\n'):
                    for keyword in ["产量", "良率", "OEE", "交付率"]:
                        if keyword in line:
                            parts = line.split(':')
                            if len(parts) >= 2:
                                result["data"]["last_week_metrics"][keyword] = parts[1].strip().split()[0]

            result["weeks_read"] += 1
        except Exception as e:
            continue

    # 去重
    seen_issues = set()
    result["data"]["unresolved_issues"] = [
        item for item in result["data"]["unresolved_issues"]
        if item["description"] not in seen_issues and not seen_issues.add(item["description"])
    ]
    
    seen_items = set()
    result["data"]["in_progress_items"] = [
        item for item in result["data"]["in_progress_items"]
        if item["description"] not in seen_items and not seen_items.add(item["description"])
    ]

    return result


def archive_report(file_path: str, history_dir: str = "./weekly_reports/history") -> dict:
    """归档周报文件到历史目录"""
    source = Path(file_path)
    if not source.exists():
        return {"status": "error", "message": f"文件不存在: {file_path}"}

    # 提取周次
    match = re.search(r'(\d{4})-W(\d{2,})', source.stem)
    if match:
        week_id = f"{match.group(1)}-W{int(match.group(2)):02d}"
    else:
        week_id = datetime.now().strftime("%Y-W%V")

    # 创建历史目录
    history_path = Path(history_dir)
    history_path.mkdir(parents=True, exist_ok=True)

    # 复制文件
    dest = history_path / f"{week_id}.md"
    dest.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    return {"status": "success", "archived_to": str(dest), "week_id": week_id}


def validate_data(data: dict) -> dict:
    """校验数据完整性，返回缺失项列表"""
    missing = []
    
    # 检查最低门槛
    metrics = data.get("production_metrics", [])
    completed = data.get("completed_items", [])
    plan = data.get("next_week_plan", [])
    
    if not metrics or len(metrics) == 0:
        missing.append("核心指标（产量/良率/OEE/交付率等）")
    
    if not completed or len(completed) == 0:
        missing.append("本周完成事项")
    
    if not plan or len(plan) == 0:
        missing.append("下周计划")
    
    return {
        "valid": len(missing) == 0,
        "missing": missing
    }


def main():
    parser = argparse.ArgumentParser(description="历史周报管理")
    subparsers = parser.add_subparsers(dest="action", help="操作类型")

    # 读取历史
    read_parser = subparsers.add_parser("read", help="读取历史数据")
    read_parser.add_argument("--weeks", type=int, default=4, help="读取周数")
    read_parser.add_argument("--dir", default="./weekly_reports/history", help="历史目录")

    # 归档
    archive_parser = subparsers.add_parser("archive", help="归档周报")
    archive_parser.add_argument("--file", required=True, help="周报文件路径")
    archive_parser.add_argument("--dir", default="./weekly_reports/history", help="历史目录")

    # 校验
    validate_parser = subparsers.add_parser("validate", help="校验数据完整性")
    validate_parser.add_argument("--data", required=True, help="JSON数据字符串")

    args = parser.parse_args()

    if args.action == "read":
        result = read_history(args.weeks, args.dir)
    elif args.action == "archive":
        result = archive_report(args.file, args.dir)
    elif args.action == "validate":
        data = json.loads(args.data)
        result = validate_data(data)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
