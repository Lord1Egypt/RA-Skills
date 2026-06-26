#!/usr/bin/env python3
"""
收集技能执行后的用户反馈（简化版）
用法: python3 collect-feedback.py --skill SKILL_NAME [--score SCORE] [--comment COMMENT]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tracking import is_tracked


def get_feedback_dir(skill_name: str) -> Path:
    """获取技能的反馈存储目录"""
    base_dir = Path.home() / ".openclaw/workspace/.skill-polisher/feedback"
    skill_dir = base_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    return skill_dir


def collect_interactive(skill_name: str) -> dict:
    """交互式收集用户反馈"""
    print(f"\n{'='*50}")
    print(f"📊 {skill_name} 执行反馈")
    print(f"{'='*50}\n")
    
    # 评分
    while True:
        try:
            score = input("请对本次执行评分 (0-10): ").strip()
            score = int(score)
            if 0 <= score <= 10:
                break
            print("请输入 0-10 之间的数字")
        except ValueError:
            print("请输入数字")
    
    # 问题/建议
    comment = input("遇到的问题或建议 (可选): ").strip() or None
    
    return {
        "skill": skill_name,
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(),
        "score": score,
        "comment": comment
    }


def save_feedback(feedback: dict) -> Path:
    """保存反馈到文件"""
    skill_name = feedback["skill"]
    feedback_dir = get_feedback_dir(skill_name)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}.json"
    filepath = feedback_dir / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(feedback, f, ensure_ascii=False, indent=2)
    
    return filepath


def print_result(feedback: dict):
    """打印反馈结果"""
    score = feedback["score"]
    
    print(f"\n✅ 反馈已保存")
    print(f"📈 评分: {score}/10")
    
    if score >= 8:
        print("🎉 感谢好评！")
    elif score >= 6:
        print("📝 收到反馈，会持续改进")
    else:
        print("⚠️  检测到较低评分，将优先优化")


def main():
    parser = argparse.ArgumentParser(description="收集技能执行反馈（仅追踪列表中的技能）")
    parser.add_argument("--skill", required=True, help="技能名称")
    parser.add_argument("--score", type=int, help="评分 (0-10)")
    parser.add_argument("--comment", help="问题或建议")
    parser.add_argument("--force", "-f", action="store_true", help="强制记录（不在追踪列表时也记录）")
    
    args = parser.parse_args()
    
    # 检查是否在追踪列表中
    if not is_tracked(args.skill) and not args.force:
        print(f"\n⚠️  {args.skill} 不在追踪列表中")
        print(f"   使用 tracking.py --add {args.skill} 添加到追踪列表")
        print(f"   或使用 --force 强制记录")
        sys.exit(1)
    
    # 如果提供了参数，使用非交互模式
    if args.score is not None:
        if not 0 <= args.score <= 10:
            print("错误: 评分必须在 0-10 之间")
            sys.exit(1)
        feedback = {
            "skill": args.skill,
            "timestamp": datetime.now(timezone.utc).astimezone().isoformat(),
            "score": args.score,
            "comment": args.comment
        }
    else:
        # 交互式收集
        feedback = collect_interactive(args.skill)
    
    # 保存
    filepath = save_feedback(feedback)
    
    # 输出结果
    print_result(feedback)
    print(f"💾 保存位置: {filepath}")


if __name__ == "__main__":
    main()
