#!/usr/bin/env python3
"""
FMEA 表格管理器
支持创建项目、添加分析项、RPN计算、预防措施跟踪与导出
"""

import argparse
import json
import os
import sys
import csv
from datetime import datetime
from pathlib import Path

# 数据存储目录
DATA_DIR = Path("fmea_output")
DATA_DIR.mkdir(exist_ok=True)


def get_project_file(project_name):
    """获取项目数据文件路径"""
    safe_name = "".join(c for c in project_name if c.isalnum() or c in "-_").strip()
    return DATA_DIR / f"{safe_name}_fmea.json"


def create_project(project_name):
    """创建新FMEA项目"""
    project_file = get_project_file(project_name)
    
    if project_file.exists():
        return {"status": "exists", "message": f"项目 '{project_name}' 已存在"}
    
    project = {
        "project_name": project_name,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "items": [],
        "summary": {
            "total_items": 0,
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "low_risk_count": 0
        }
    }
    
    with open(project_file, "w", encoding="utf-8") as f:
        json.dump(project, f, ensure_ascii=False, indent=2)
    
    return {"status": "success", "message": f"项目 '{project_name}' 创建成功", "file": str(project_file)}


def load_project(project_name):
    """加载项目数据"""
    project_file = get_project_file(project_name)
    
    if not project_file.exists():
        return None
    
    with open(project_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_project(project):
    """保存项目数据"""
    project["updated_at"] = datetime.now().isoformat()
    project_file = get_project_file(project["project_name"])
    
    with open(project_file, "w", encoding="utf-8") as f:
        json.dump(project, f, ensure_ascii=False, indent=2)


def calculate_rpn(severity, occurrence, detection):
    """计算RPN及风险等级"""
    rpn = severity * occurrence * detection
    
    if rpn <= 20:
        level = "低"
    elif rpn <= 60:
        level = "中"
    elif rpn <= 100:
        level = "高"
    elif rpn <= 200:
        level = "很高"
    else:
        level = "极高"
    
    return rpn, level


def add_item(project_name, item_data):
    """添加FMEA分析项"""
    project = load_project(project_name)
    if project is None:
        return {"status": "error", "message": f"项目 '{project_name}' 不存在"}
    
    severity = item_data["severity"]
    occurrence = item_data["occurrence"]
    detection = item_data["detection"]
    rpn, risk_level = calculate_rpn(severity, occurrence, detection)
    
    item = {
        "id": len(project["items"]) + 1,
        "item_number": item_data.get("item_number", ""),
        "system_subsystem": item_data.get("system_subsystem", ""),
        "function": item_data.get("function", ""),
        "potential_failure_mode": item_data.get("failure_mode", ""),
        "potential_effect": item_data.get("effect", ""),
        "severity": severity,
        "potential_cause": item_data.get("cause", ""),
        "occurrence": occurrence,
        "current_prevention": item_data.get("prevention", ""),
        "detection": detection,
        "rpn": rpn,
        "risk_level": risk_level,
        "recommended_actions": item_data.get("actions", ""),
        "responsibility": item_data.get("responsibility", ""),
        "target_date": item_data.get("target_date", ""),
        "actions_taken": item_data.get("actions_taken", ""),
        "closure_date": item_data.get("closure_date", ""),
        "revised_severity": None,
        "revised_occurrence": None,
        "revised_detection": None,
        "revised_rpn": None,
        "status": "open",
        "created_at": datetime.now().isoformat()
    }
    
    project["items"].append(item)
    update_summary(project)
    save_project(project)
    
    return {
        "status": "success",
        "message": f"分析项已添加，RPN={rpn}，风险等级={risk_level}",
        "item_id": item["id"],
        "rpn": rpn,
        "risk_level": risk_level
    }


def update_summary(project):
    """更新项目摘要统计"""
    items = project.get("items", [])
    
    high_risk = sum(1 for i in items if i.get("risk_level") in ["高", "很高", "极高"])
    medium_risk = sum(1 for i in items if i.get("risk_level") == "中")
    low_risk = sum(1 for i in items if i.get("risk_level") == "低")
    
    project["summary"] = {
        "total_items": len(items),
        "high_risk_count": high_risk,
        "medium_risk_count": medium_risk,
        "low_risk_count": low_risk
    }


def list_items(project_name):
    """列出项目所有分析项"""
    project = load_project(project_name)
    if project is None:
        return {"status": "error", "message": f"项目 '{project_name}' 不存在"}
    
    items_summary = []
    for item in project["items"]:
        items_summary.append({
            "id": item["id"],
            "item_number": item["item_number"],
            "system_subsystem": item["system_subsystem"],
            "function": item["function"],
            "failure_mode": item["potential_failure_mode"],
            "severity": item["severity"],
            "occurrence": item["occurrence"],
            "detection": item["detection"],
            "rpn": item["rpn"],
            "risk_level": item["risk_level"],
            "status": item["status"]
        })
    
    return {
        "status": "success",
        "project": project["project_name"],
        "summary": project["summary"],
        "items": items_summary
    }


def update_item(project_name, item_id, update_data):
    """更新分析项"""
    project = load_project(project_name)
    if project is None:
        return {"status": "error", "message": f"项目 '{project_name}' 不存在"}
    
    item = next((i for i in project["items"] if i["id"] == item_id), None)
    if item is None:
        return {"status": "error", "message": f"分析项 {item_id} 不存在"}
    
    # 更新字段
    for key, value in update_data.items():
        if key in ["severity", "occurrence", "detection"]:
            item[key] = value
            # 重新计算RPN
            rpn, level = calculate_rpn(
                item["severity"], item["occurrence"], item["detection"]
            )
            item["rpn"] = rpn
            item["risk_level"] = level
        elif key in ["recommended_actions", "actions_taken", "responsibility", 
                     "target_date", "closure_date", "status"]:
            item[key] = value
    
    # 如果有闭环日期，更新修订后的RPN
    if item.get("revised_severity") and item.get("revised_occurrence") and item.get("revised_detection"):
        rpn, _ = calculate_rpn(
            item["revised_severity"], 
            item["revised_occurrence"], 
            item["revised_detection"]
        )
        item["revised_rpn"] = rpn
    
    update_summary(project)
    save_project(project)
    
    return {"status": "success", "message": f"分析项 {item_id} 已更新", "item": item}


def recommend_actions(severity, occurrence, detection):
    """根据评分推荐预防措施"""
    rpn, risk_level = calculate_rpn(severity, occurrence, detection)
    
    recommendations = []
    
    # 严重度相关（后果导向）
    if severity >= 8:
        recommendations.extend([
            "评估是否可以改变设计消除失效模式",
            "考虑冗余设计或备份方案",
            "审查设计余量是否足够",
            "与客户沟通确认可接受的风险水平"
        ])
    elif severity >= 6:
        recommendations.extend([
            "增加保护电路或安全装置",
            "考虑故障检测与报警机制"
        ])
    
    # 发生度相关（原因导向）
    if occurrence >= 8:
        recommendations.extend([
            "分析根本原因（5Why/鱼骨图）",
            "重新设计以消除失效机理",
            "选择更可靠的材料或工艺",
            "改善工作环境条件"
        ])
    elif occurrence >= 6:
        recommendations.extend([
            "加强进料检验",
            "优化工艺参数控制",
            "增加过程监控"
        ])
    
    # 探测度相关（探测能力导向）
    if detection >= 8:
        recommendations.extend([
            "改进检测方法或设备",
            "增加在线检测点",
            "实施统计过程控制(SPC)",
            "考虑采用更敏感的传感器"
        ])
    elif detection >= 6:
        recommendations.extend([
            "增加检测频次",
            "改进取样方案",
            "引入自动化检测"
        ])
    
    # 通用建议
    recommendations.extend([
        "制定纠正措施计划",
        "指定责任人并设置完成期限",
        "验证措施有效性",
        "更新FMEA记录"
    ])
    
    # 去重
    recommendations = list(dict.fromkeys(recommendations))
    
    return {
        "current_rpn": rpn,
        "risk_level": risk_level,
        "recommendations": recommendations
    }


def export_project(project_name, format_type="csv"):
    """导出项目数据"""
    project = load_project(project_name)
    if project is None:
        return {"status": "error", "message": f"项目 '{project_name}' 不存在"}
    
    if format_type == "csv":
        export_file = DATA_DIR / f"{project_name}_export.csv"
        
        fieldnames = [
            "id", "item_number", "system_subsystem", "function",
            "potential_failure_mode", "potential_effect", "severity",
            "potential_cause", "occurrence", "current_prevention",
            "detection", "rpn", "risk_level", "recommended_actions",
            "responsibility", "target_date", "actions_taken",
            "closure_date", "status"
        ]
        
        with open(export_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for item in project["items"]:
                writer.writerow(item)
        
        return {"status": "success", "file": str(export_file)}
    
    elif format_type == "json":
        export_file = DATA_DIR / f"{project_name}_export.json"
        with open(export_file, "w", encoding="utf-8") as f:
            json.dump(project, f, ensure_ascii=False, indent=2)
        return {"status": "success", "file": str(export_file)}
    
    return {"status": "error", "message": f"不支持的导出格式: {format_type}"}


def get_high_risk_items(project_name):
    """获取高风险项清单"""
    project = load_project(project_name)
    if project is None:
        return {"status": "error", "message": f"项目 '{project_name}' 不存在"}
    
    high_risk = [i for i in project["items"] 
                 if i.get("risk_level") in ["高", "很高", "极高"]]
    
    # 按RPN排序
    high_risk.sort(key=lambda x: x.get("rpn", 0), reverse=True)
    
    return {
        "status": "success",
        "project": project_name,
        "high_risk_count": len(high_risk),
        "high_risk_items": [{
            "id": i["id"],
            "item_number": i["item_number"],
            "failure_mode": i["potential_failure_mode"],
            "rpn": i["rpn"],
            "risk_level": i["risk_level"],
            "recommended_actions": i["recommended_actions"]
        } for i in high_risk]
    }


def main():
    parser = argparse.ArgumentParser(description="FMEA表格管理器")
    parser.add_argument("--action", 
                        choices=["create", "add", "list", "update", "recommend", 
                                "export", "high-risk", "help"],
                        default="help", help="操作类型")
    parser.add_argument("--project", help="项目名称")
    parser.add_argument("--item-id", type=int, help="分析项ID")
    
    # 分析项参数
    parser.add_argument("--item-number", help="项目编号")
    parser.add_argument("--system-subsystem", help="系统/子系统")
    parser.add_argument("--function", help="功能描述")
    parser.add_argument("--failure-mode", help="潜在失效模式")
    parser.add_argument("--effect", help="潜在影响")
    parser.add_argument("--severity", type=int, choices=range(1, 11), help="严重度(1-10)")
    parser.add_argument("--cause", help="潜在原因")
    parser.add_argument("--occurrence", type=int, choices=range(1, 11), help="发生度(1-10)")
    parser.add_argument("--prevention", help="当前预防措施")
    parser.add_argument("--detection", type=int, choices=range(1, 11), help="探测度(1-10)")
    parser.add_argument("--actions", help="建议措施")
    parser.add_argument("--responsibility", help="责任人")
    parser.add_argument("--target-date", help="目标日期")
    parser.add_argument("--actions-taken", help="已采取措施")
    parser.add_argument("--closure-date", help="闭环日期")
    parser.add_argument("--status", choices=["open", "in-progress", "closed"], help="状态")
    parser.add_argument("--format", choices=["csv", "json"], default="csv", help="导出格式")
    
    args = parser.parse_args()
    
    result = None
    
    if args.action == "help":
        help_text = """
FMEA 表格管理器使用说明

命令格式:
  python scripts/fmea_tracker.py --action <操作> [参数...]

操作类型:
  create     - 创建新项目
  add        - 添加分析项
  list       - 列出所有分析项
  update     - 更新分析项
  recommend  - 获取措施建议
  export     - 导出数据
  high-risk  - 获取高风险项

示例:
  # 创建项目
  python scripts/fmea_tracker.py --action create --project "电机驱动系统"

  # 添加分析项
  python scripts/fmea_tracker.py --action add --project "电机驱动系统" \\
    --item-number "A1" --function "提供持续动力" --failure-mode "转速下降" \\
    --severity 8 --occurrence 5 --detection 3

  # 列出项目
  python scripts/fmea_tracker.py --action list --project "电机驱动系统"

  # 获取建议
  python scripts/fmea_tracker.py --action recommend --severity 8 --occurrence 5 --detection 3

  # 导出CSV
  python scripts/fmea_tracker.py --action export --project "电机驱动系统" --format csv
        """
        print(help_text)
        return
    
    elif args.action == "create":
        if not args.project:
            result = {"status": "error", "message": "需要 --project 参数"}
        else:
            result = create_project(args.project)
    
    elif args.action == "add":
        if not args.project:
            result = {"status": "error", "message": "需要 --project 参数"}
        elif not all([args.severity, args.occurrence, args.detection]):
            result = {"status": "error", "message": "需要 --severity, --occurrence, --detection 参数"}
        else:
            item_data = {
                "item_number": args.item_number or "",
                "system_subsystem": args.system_subsystem or "",
                "function": args.function or "",
                "failure_mode": args.failure_mode or "",
                "effect": args.effect or "",
                "severity": args.severity,
                "cause": args.cause or "",
                "occurrence": args.occurrence,
                "prevention": args.prevention or "",
                "detection": args.detection,
                "actions": args.actions or "",
                "responsibility": args.responsibility or "",
                "target_date": args.target_date or "",
                "actions_taken": args.actions_taken or ""
            }
            result = add_item(args.project, item_data)
    
    elif args.action == "list":
        if not args.project:
            result = {"status": "error", "message": "需要 --project 参数"}
        else:
            result = list_items(args.project)
    
    elif args.action == "update":
        if not args.project or not args.item_id:
            result = {"status": "error", "message": "需要 --project 和 --item-id 参数"}
        else:
            update_data = {}
            if args.severity: update_data["severity"] = args.severity
            if args.occurrence: update_data["occurrence"] = args.occurrence
            if args.detection: update_data["detection"] = args.detection
            if args.actions: update_data["actions_taken"] = args.actions
            if args.responsibility: update_data["responsibility"] = args.responsibility
            if args.target_date: update_data["target_date"] = args.target_date
            if args.closure_date: update_data["closure_date"] = args.closure_date
            if args.status: update_data["status"] = args.status
            
            result = update_item(args.project, args.item_id, update_data)
    
    elif args.action == "recommend":
        if not all([args.severity, args.occurrence, args.detection]):
            result = {"status": "error", "message": "需要 --severity, --occurrence, --detection 参数"}
        else:
            result = recommend_actions(args.severity, args.occurrence, args.detection)
    
    elif args.action == "export":
        if not args.project:
            result = {"status": "error", "message": "需要 --project 参数"}
        else:
            result = export_project(args.project, args.format)
    
    elif args.action == "high-risk":
        if not args.project:
            result = {"status": "error", "message": "需要 --project 参数"}
        else:
            result = get_high_risk_items(args.project)
    
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
