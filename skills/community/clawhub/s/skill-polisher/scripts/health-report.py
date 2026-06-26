#!/usr/bin/env python3
"""
生成技能健康报告（仅追踪列表中的技能）
用法: python3 health-report.py [SKILL_NAME] [--output FORMAT]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

# 导入追踪列表
sys.path.insert(0, str(Path(__file__).parent))
from tracking import get_tracked_skills, is_tracked


def get_polisher_dir() -> Path:
    """获取 polisher 数据目录"""
    return Path.home() / ".openclaw/workspace/.skill-polisher"


def get_tracked_skills_list() -> List[str]:
    """获取追踪列表中的技能"""
    return get_tracked_skills()


def load_feedback(skill_name: str, days: int = 30) -> List[dict]:
    """加载技能的近期反馈"""
    feedback_dir = get_polisher_dir() / "feedback" / skill_name
    if not feedback_dir.exists():
        return []
    
    feedbacks = []
    cutoff = datetime.now(timezone.utc).astimezone() - timedelta(days=days)
    
    for file in feedback_dir.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                feedback_time = datetime.fromisoformat(data["timestamp"])
                # 如果反馈时间没有时区，假设为本地时区
                if feedback_time.tzinfo is None:
                    feedback_time = feedback_time.replace(tzinfo=timezone.utc).astimezone()
                if feedback_time >= cutoff:
                    feedbacks.append(data)
        except Exception:
            continue
    
    return sorted(feedbacks, key=lambda x: x["timestamp"], reverse=True)


def calculate_health_score(skill_name: str) -> dict:
    """计算技能健康度"""
    feedbacks = load_feedback(skill_name, days=30)
    
    if not feedbacks:
        return {
            "skill": skill_name,
            "overall": None,
            "level": "unknown",
            "metrics": {
                "recent_avg": None,
                "usage_count": 0,
                "success_rate": None,
                "feedback_count": 0
            },
            "issues": ["暂无反馈数据"]
        }
    
    # 计算各项指标（简化版：直接使用 score 字段）
    scores = []
    low_scores = 0
    
    for fb in feedbacks:
        # 兼容新旧格式
        if "score" in fb:
            score = fb["score"]
        else:
            # 旧格式：计算综合得分
            s = fb.get("scores", {})
            completion = s.get("completion", 0)
            usability = s.get("usability") or completion
            quality = s.get("quality") or completion
            score = completion * 0.4 + usability * 0.25 + quality * 0.25 + 10 * 0.1
        
        scores.append(score)
        if score < 6:
            low_scores += 1
    
    recent_avg = sum(scores) / len(scores) if scores else 0
    usage_count = len(feedbacks)
    success_rate = (len([s for s in scores if s >= 6]) / len(scores) * 100) if scores else 0
    
    # 计算最终健康度（映射到 0-100 分制）
    # 近期平均分(40%) + 使用频率(20%) + 成功率(30%) + 反馈丰富度(10%)
    freq_score = min(usage_count / 10 * 10, 10)  # 10次使用得满分
    
    overall = (
        recent_avg * 10 * 0.4 +      # 近期平均分映射到 0-100
        freq_score * 10 * 0.2 +       # 使用频率
        success_rate * 0.3 +          # 成功率
        min(len(feedbacks) / 5 * 10, 10) * 10 * 0.1  # 反馈丰富度
    )
    
    # 确定等级
    if overall >= 80:
        level = "excellent"
        level_emoji = "🟢"
    elif overall >= 60:
        level = "good"
        level_emoji = "🟡"
    elif overall >= 40:
        level = "warning"
        level_emoji = "🟠"
    else:
        level = "critical"
        level_emoji = "🔴"
    
    # 识别问题
    issues = []
    if recent_avg < 6:
        issues.append(f"近期平均分较低 ({recent_avg:.1f})")
    if success_rate < 70:
        issues.append(f"成功率偏低 ({success_rate:.1f}%)")
    if usage_count < 3:
        issues.append("使用频率较低，数据不足")
    
    return {
        "skill": skill_name,
        "overall": round(overall, 1),
        "level": level,
        "level_emoji": level_emoji,
        "metrics": {
            "recent_avg": round(recent_avg, 1),
            "usage_count": usage_count,
            "success_rate": round(success_rate, 1),
            "feedback_count": len(feedbacks),
            "low_score_count": low_scores
        },
        "issues": issues if issues else ["暂无明显问题"]
    }


def print_report(report: dict, detailed: bool = False):
    """打印报告"""
    skill = report["skill"]
    overall = report["overall"]
    level = report["level"]
    emoji = report.get("level_emoji", "⚪")
    
    print(f"\n{emoji} {skill}")
    print(f"   健康度: {overall if overall else 'N/A'}/100 [{level}]")
    
    if detailed:
        metrics = report["metrics"]
        print(f"   近期均分: {metrics['recent_avg'] if metrics['recent_avg'] else 'N/A'}")
        print(f"   使用次数: {metrics['usage_count']}")
        print(f"   成功率: {metrics['success_rate']}%")
        print(f"   问题: {', '.join(report['issues'])}")


def generate_full_report(output_format: str = "text"):
    """生成完整报告（仅追踪列表中的技能）"""
    skills = get_tracked_skills_list()
    
    if not skills:
        print("\n📭 追踪列表为空")
        print("   使用 tracking.py --add <skill-name> 添加技能到追踪列表")
        return
    
    reports = []
    for skill in skills:
        report = calculate_health_score(skill)
        reports.append(report)
    
    # 按健康度排序
    reports.sort(key=lambda x: x["overall"] if x["overall"] else 0, reverse=True)
    
    if output_format == "json":
        print(json.dumps(reports, ensure_ascii=False, indent=2))
        return
    
    # 文本格式
    print(f"\n{'='*60}")
    print(f"📊 Skill Polisher 健康报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    
    # 汇总
    excellent = sum(1 for r in reports if r["level"] == "excellent")
    good = sum(1 for r in reports if r["level"] == "good")
    warning = sum(1 for r in reports if r["level"] == "warning")
    critical = sum(1 for r in reports if r["level"] == "critical")
    unknown = sum(1 for r in reports if r["level"] == "unknown")
    
    print(f"\n📈 汇总:")
    print(f"   🟢 优秀: {excellent}  🟡 良好: {good}  🟠 需关注: {warning}  🔴 需重构: {critical}  ⚪ 无数据: {unknown}")
    
    # 需要关注的技能
    need_attention = [r for r in reports if r["level"] in ("warning", "critical")]
    if need_attention:
        print(f"\n⚠️  需要关注的技能:")
        for r in need_attention:
            print(f"   - {r['skill']}: {r['overall']}/100 - {r['issues'][0]}")
    
    # 详细列表
    print(f"\n📋 详细评分:")
    for report in reports:
        print_report(report, detailed=False)
    
    print(f"\n{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="生成技能健康报告（仅追踪列表中的技能）")
    parser.add_argument("skill", nargs="?", help="指定技能名称（默认全部）")
    parser.add_argument("--output", "-o", choices=["text", "json"], default="text", help="输出格式")
    parser.add_argument("--detailed", "-d", action="store_true", help="显示详细信息")
    
    args = parser.parse_args()
    
    if args.skill:
        # 检查是否在追踪列表中
        if not is_tracked(args.skill):
            print(f"\n⚠️  {args.skill} 不在追踪列表中")
            print(f"   使用 tracking.py --add {args.skill} 添加到追踪列表")
            return
        
        report = calculate_health_score(args.skill)
        if args.output == "json":
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print_report(report, detailed=args.detailed)
    else:
        generate_full_report(output_format=args.output)


if __name__ == "__main__":
    main()
