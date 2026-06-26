#!/usr/bin/env python3
"""
基于健康报告生成打磨建议
用法: python3 polish-suggest.py [--skill SKILL_NAME] [--auto]
"""

import argparse
import json
import sys
from pathlib import Path
import importlib.util

# 动态导入 health-report 的函数
spec = importlib.util.spec_from_file_location("health_report", 
    Path(__file__).parent / "health-report.py")
health_report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(health_report)
calculate_health_score = health_report.calculate_health_score
get_all_skills = health_report.get_all_skills


def analyze_skill(skill_name: str) -> dict:
    """分析技能，生成改进建议"""
    report = calculate_health_score(skill_name)
    
    if report["level"] == "unknown":
        return {
            "skill": skill_name,
            "priority": "low",
            "reason": "暂无使用数据，无法评估",
            "suggestions": ["开始使用该技能以收集反馈数据"]
        }
    
    suggestions = []
    priority = "low"
    
    metrics = report["metrics"]
    issues = report["issues"]
    
    # 根据问题生成建议
    if metrics["recent_avg"] and metrics["recent_avg"] < 6:
        suggestions.append({
            "type": "quality",
            "issue": "完成度评分偏低",
            "action": "检查 SKILL.md 中的 Quick Start 是否清晰，示例是否可运行",
            "reference": "best-practices.md#quick-start"
        })
        priority = "high"
    
    if metrics["success_rate"] and metrics["success_rate"] < 70:
        suggestions.append({
            "type": "reliability",
            "issue": "成功率偏低",
            "action": "检查脚本错误处理，添加更多边界情况处理",
            "reference": "pitfalls.md#error-handling"
        })
        priority = "high"
    
    if metrics["usage_count"] < 3:
        suggestions.append({
            "type": "adoption",
            "issue": "使用频率低",
            "action": "检查技能描述是否清晰，考虑增加使用场景说明",
            "reference": "best-practices.md#description"
        })
        priority = "medium"
    
    # 检查是否有具体的问题反馈
    feedbacks = load_recent_feedback(skill_name)
    common_issues = extract_common_issues(feedbacks)
    
    for issue in common_issues:
        suggestions.append({
            "type": "user_feedback",
            "issue": issue["description"],
            "action": f"用户反馈: {issue['count']} 次提到",
            "reference": None
        })
        if issue["count"] >= 2:
            priority = "high"
    
    # 如果没有具体问题，给出通用建议
    if not suggestions:
        if report["overall"] >= 80:
            suggestions.append({
                "type": "maintenance",
                "issue": "技能状态良好",
                "action": "可作为最佳实践案例，考虑提取可复用模式",
                "reference": "best-practices.md"
            })
        else:
            suggestions.append({
                "type": "general",
                "issue": "综合评分有提升空间",
                "action": "对照 quality-standards.md 进行全面检查",
                "reference": "quality-standards.md"
            })
    
    return {
        "skill": skill_name,
        "health": report["overall"],
        "level": report["level"],
        "priority": priority,
        "suggestions": suggestions
    }


def load_recent_feedback(skill_name: str, limit: int = 10):
    """加载近期反馈"""
    import json
    from datetime import datetime, timedelta
    
    feedback_dir = Path.home() / ".openclaw/workspace/.skill-polisher/feedback" / skill_name
    if not feedback_dir.exists():
        return []
    
    feedbacks = []
    for file in sorted(feedback_dir.glob("*.json"), reverse=True)[:limit]:
        try:
            with open(file, "r", encoding="utf-8") as f:
                feedbacks.append(json.load(f))
        except Exception:
            continue
    
    return feedbacks


def extract_common_issues(feedbacks: list) -> list:
    """提取常见问题模式"""
    issues = []
    issue_counts = {}
    
    for fb in feedbacks:
        if fb.get("issues"):
            key = fb["issues"].lower().strip()
            issue_counts[key] = issue_counts.get(key, 0) + 1
    
    for issue, count in issue_counts.items():
        if count >= 1:
            issues.append({
                "description": issue[:50] + "..." if len(issue) > 50 else issue,
                "count": count
            })
    
    return sorted(issues, key=lambda x: x["count"], reverse=True)[:3]


def print_suggestion(analysis: dict):
    """打印建议"""
    skill = analysis["skill"]
    health = analysis["health"]
    priority = analysis["priority"]
    
    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
    
    print(f"\n{priority_emoji} {skill} (健康度: {health}/100)")
    print(f"   优先级: {priority.upper()}")
    
    for i, sug in enumerate(analysis["suggestions"], 1):
        print(f"\n   {i}. [{sug['type']}] {sug['issue']}")
        print(f"      建议: {sug['action']}")
        if sug.get("reference"):
            print(f"      参考: {sug['reference']}")


def generate_polish_plan(auto_select: bool = False) -> list:
    """生成打磨计划"""
    skills = get_all_skills()
    analyses = []
    
    for skill in skills:
        analysis = analyze_skill(skill)
        analyses.append(analysis)
    
    # 按优先级排序
    priority_order = {"high": 0, "medium": 1, "low": 2}
    analyses.sort(key=lambda x: (priority_order.get(x["priority"], 3), -x["health"]))
    
    if auto_select:
        # 自动选择高优先级的技能
        return [a for a in analyses if a["priority"] == "high"]
    
    return analyses


def main():
    parser = argparse.ArgumentParser(description="生成技能打磨建议")
    parser.add_argument("--skill", help="指定技能名称")
    parser.add_argument("--auto", action="store_true", help="自动模式，只显示需要处理的")
    parser.add_argument("--plan", action="store_true", help="生成完整打磨计划")
    
    args = parser.parse_args()
    
    if args.skill:
        analysis = analyze_skill(args.skill)
        print_suggestion(analysis)
    elif args.plan or args.auto:
        analyses = generate_polish_plan(auto_select=args.auto)
        
        print(f"\n{'='*60}")
        print(f"🔧 Skill Polisher 打磨计划")
        print(f"{'='*60}")
        
        if not analyses:
            print("\n✅ 所有技能状态良好，暂无需要打磨的")
            return
        
        high_count = sum(1 for a in analyses if a["priority"] == "high")
        if high_count > 0:
            print(f"\n🔴 高优先级 ({high_count} 个):")
            for analysis in analyses:
                if analysis["priority"] == "high":
                    print_suggestion(analysis)
        
        if not args.auto:
            medium_count = sum(1 for a in analyses if a["priority"] == "medium")
            if medium_count > 0:
                print(f"\n🟡 中优先级 ({medium_count} 个):")
                for analysis in analyses:
                    if analysis["priority"] == "medium":
                        print_suggestion(analysis)
        
        print(f"\n{'='*60}")
        print(f"💡 建议已输出，请手动决定是否采纳")
        print(f"{'='*60}")
    else:
        # 默认显示所有技能的建议
        analyses = generate_polish_plan()
        for analysis in analyses:
            print_suggestion(analysis)


if __name__ == "__main__":
    main()
