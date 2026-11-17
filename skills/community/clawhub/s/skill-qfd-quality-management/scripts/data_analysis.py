#!/usr/bin/env python3
"""
QFD历史数据分析工具
支持：需求优先级分析、技术可行性评估、迭代优化建议
"""

import argparse
import json
import csv
import sys
from typing import Dict, List, Any, Tuple
from collections import defaultdict


def load_history_data(csv_file: str) -> List[Dict[str, Any]]:
    """加载历史项目数据"""
    data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def load_current_requirements(json_file: str) -> Dict[str, Any]:
    """加载当前需求数据"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_priority_adjustments(history: List[Dict], current: Dict) -> List[Dict[str, Any]]:
    """分析需求优先级调整建议"""
    # 统计历史项目中各类需求的平均权重和完成情况
    category_stats = defaultdict(lambda: {"weights": [], "satisfaction": [], "count": 0})
    
    for project in history:
        category = project.get("category", "功能")
        weight = float(project.get("initial_weight", 3))
        satisfaction = float(project.get("final_satisfaction", 3))
        
        category_stats[category]["weights"].append(weight)
        category_stats[category]["satisfaction"].append(satisfaction)
        category_stats[category]["count"] += 1
    
    # 计算调整系数
    adjustments = []
    for cat, stats in category_stats.items():
        if stats["count"] > 0:
            avg_weight = sum(stats["weights"]) / len(stats["weights"])
            avg_satisfaction = sum(stats["satisfaction"]) / len(stats["satisfaction"])
            
            # 满意度低于初始权重，说明预期过高，需下调
            if avg_satisfaction < avg_weight - 0.5:
                adjustment = -0.5
                reason = f"{cat}类需求历史满意度({avg_satisfaction:.1f})低于预期，建议适当下调"
            elif avg_satisfaction > avg_weight + 0.5:
                adjustment = 0.3
                reason = f"{cat}类需求历史满意度({avg_satisfaction:.1f})高于预期，可以适当提高"
            else:
                adjustment = 0
                reason = f"{cat}类需求历史表现符合预期"
            
            adjustments.append({
                "category": cat,
                "historical_avg_weight": round(avg_weight, 2),
                "historical_avg_satisfaction": round(avg_satisfaction, 2),
                "suggested_adjustment": adjustment,
                "reason": reason
            })
    
    return adjustments


def analyze_technical_feasibility(history: List[Dict], current: Dict) -> List[Dict[str, Any]]:
    """分析技术实现可行性"""
    # 统计各技术指标的实现难度和成功率
    tech_stats = defaultdict(lambda: {"difficulty": [], "success": [], "count": 0})
    
    for project in history:
        tech_id = project.get("technical_requirement_id", "")
        difficulty = float(project.get("difficulty_rating", 3))
        success = 1 if project.get("implementation_status", "").lower() in ["success", "成功", "completed", "完成"] else 0
        
        if tech_id:
            tech_stats[tech_id]["difficulty"].append(difficulty)
            tech_stats[tech_id]["success"].append(success)
            tech_stats[tech_id]["count"] += 1
    
    # 分析当前技术指标
    feasibility = []
    current_tech_ids = {tr["id"] for tr in current.get("technical_requirements", [])}
    
    for tech_id, stats in tech_stats.items():
        if stats["count"] > 0:
            avg_difficulty = sum(stats["difficulty"]) / len(stats["difficulty"])
            success_rate = sum(stats["success"]) / len(stats["success"])
            
            # 评估可行性
            if tech_id in current_tech_ids:
                if success_rate >= 0.8 and avg_difficulty <= 3:
                    level = "高"
                    suggestion = "技术成熟，可以作为核心指标"
                elif success_rate >= 0.5:
                    level = "中"
                    suggestion = "需要关注实现风险，建议准备备选方案"
                else:
                    level = "低"
                    suggestion = "历史成功率较低，需要谨慎评估或寻找替代方案"
                
                feasibility.append({
                    "technical_requirement_id": tech_id,
                    "historical_difficulty": round(avg_difficulty, 2),
                    "historical_success_rate": round(success_rate * 100, 1),
                    "feasibility_level": level,
                    "suggestion": suggestion,
                    "data_points": stats["count"]
                })
    
    return feasibility


def calculate_confidence_scores(history: List[Dict], current: Dict) -> Dict[str, Any]:
    """计算分析结果的可信度"""
    num_projects = len(history)
    unique_categories = len(set(p.get("category", "") for p in history if p.get("category")))
    
    # 基于数据量评估可信度
    if num_projects >= 10:
        data_confidence = "高"
        data_confidence_score = 0.9
    elif num_projects >= 5:
        data_confidence = "中"
        data_confidence_score = 0.7
    elif num_projects >= 3:
        data_confidence = "低"
        data_confidence_score = 0.5
    else:
        data_confidence = "极低"
        data_confidence_score = 0.3
    
    return {
        "total_projects": num_projects,
        "unique_categories": unique_categories,
        "confidence_level": data_confidence,
        "confidence_score": data_confidence_score,
        "recommendation": "数据量充足，分析结果可靠" if num_projects >= 5 else "建议积累更多历史数据以提高分析准确性"
    }


def generate_optimization_report(history: List[Dict], current: Dict) -> Dict[str, Any]:
    """生成优化建议报告"""
    priority_adjustments = analyze_priority_adjustments(history, current)
    feasibility = analyze_technical_feasibility(history, current)
    confidence = calculate_confidence_scores(history, current)
    
    # 综合建议
    suggestions = []
    
    # 优先级建议
    high_priority_adjust = [a for a in priority_adjustments if a["suggested_adjustment"] > 0]
    if high_priority_adjust:
        suggestions.append({
            "type": "优先级上调",
            "items": [a["category"] for a in high_priority_adjust],
            "action": "建议适当提高权重"
        })
    
    low_priority_adjust = [a for a in priority_adjustments if a["suggested_adjustment"] < 0]
    if low_priority_adjust:
        suggestions.append({
            "type": "优先级下调",
            "items": [a["category"] for a in low_priority_adjust],
            "action": "建议适当降低权重"
        })
    
    # 可行性建议
    low_feasibility = [f for f in feasibility if f["feasibility_level"] == "低"]
    if low_feasibility:
        suggestions.append({
            "type": "技术风险",
            "items": [f["technical_requirement_id"] for f in low_feasibility],
            "action": "需要进一步评估或准备替代方案"
        })
    
    # 总体评价
    if confidence["confidence_score"] >= 0.7 and len(low_feasibility) == 0:
        overall_status = "推荐执行"
        overall_note = "历史数据支持度高，技术风险低"
    elif confidence["confidence_score"] >= 0.5:
        overall_status = "谨慎推进"
        overall_note = "建议结合专家判断确认分析结果"
    else:
        overall_status = "建议延期"
        overall_note = "历史数据不足，建议先进行小规模试点验证"
    
    report = {
        "summary": {
            "overall_status": overall_status,
            "overall_note": overall_note,
            "confidence": confidence
        },
        "priority_adjustments": priority_adjustments,
        "technical_feasibility": feasibility,
        "optimization_suggestions": suggestions
    }
    
    return report


def main():
    parser = argparse.ArgumentParser(description="QFD历史数据分析工具")
    parser.add_argument("--history", type=str, required=True, help="历史项目数据CSV文件路径")
    parser.add_argument("--current", type=str, required=True, help="当前需求JSON文件路径")
    parser.add_argument("--output", type=str, help="输出文件路径（可选，默认stdout）")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="输出格式")
    
    args = parser.parse_args()
    
    try:
        history = load_history_data(args.history)
        current = load_current_requirements(args.current)
        
        report = generate_optimization_report(history, current)
        
        if args.format == "markdown":
            md = ["# QFD优化建议报告\n"]
            md.append(f"**总体状态**: {report['summary']['overall_status']}")
            md.append(f"**说明**: {report['summary']['overall_note']}\n")
            
            md.append("## 可信度评估\n")
            conf = report['summary']['confidence']
            md.append(f"- 分析项目数: {conf['total_projects']}")
            md.append(f"- 涉及类别: {conf['unique_categories']}")
            md.append(f"- 可信度: {conf['confidence_level']} ({conf['confidence_score']*100:.0f}%)")
            md.append(f"- 建议: {conf['recommendation']}\n")
            
            if report['priority_adjustments']:
                md.append("## 优先级调整建议\n")
                md.append("| 类别 | 历史权重 | 历史满意度 | 建议调整 | 原因 |")
                md.append("|---|---|---|---|---|")
                for adj in report['priority_adjustments']:
                    sign = "+" if adj["suggested_adjustment"] > 0 else ("-" if adj["suggested_adjustment"] < 0 else "0")
                    md.append(f"| {adj['category']} | {adj['historical_avg_weight']} | {adj['historical_avg_satisfaction']} | {sign}{abs(adj['suggested_adjustment'])} | {adj['reason']} |")
                md.append("")
            
            if report['technical_feasibility']:
                md.append("## 技术可行性评估\n")
                md.append("| 技术指标 | 历史难度 | 成功率 | 可行性 | 建议 |")
                md.append("|---|---|---|---|---|")
                for f in report['technical_feasibility']:
                    md.append(f"| {f['technical_requirement_id']} | {f['historical_difficulty']} | {f['historical_success_rate']}% | {f['feasibility_level']} | {f['suggestion']} |")
                md.append("")
            
            if report['optimization_suggestions']:
                md.append("## 综合优化建议\n")
                for s in report['optimization_suggestions']:
                    md.append(f"**{s['type']}**: {', '.join(s['items'])} - {s['action']}")
                md.append("")
            
            output = "\n".join(md)
        else:
            output = json.dumps(report, ensure_ascii=False, indent=2)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"分析报告已保存: {args.output}")
        else:
            print(output)
    
    except FileNotFoundError as e:
        print(f"错误: 文件不存在 - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
