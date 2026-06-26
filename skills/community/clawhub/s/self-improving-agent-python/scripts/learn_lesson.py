#!/usr/bin/env python3
"""
Lesson Learning Script
记录经验教训并同步到共享知识库
"""

import os
import sys
import json
import argparse
from datetime import datetime
from config import get_self_improvement_dir, get_shared_context_dir, load_json, save_json


def learn_lesson(agent_id: str, lesson: str, impact: str, category: str) -> dict:
    """
    记录经验教训
    
    Args:
        agent_id: Agent ID
        lesson: 学到的经验
        impact: 影响程度 (high/medium/low)
        category: 类别 (quality/efficiency/tools/knowledge)
    """
    # 创建经验记录
    lesson_record = {
        "id": f"lesson-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "agent": agent_id,
        "lesson": lesson,
        "impact": impact,
        "category": category,
        "applied": False
    }
    
    # 保存到本地经验库
    si_dir = get_self_improvement_dir()
    lessons_path = os.path.join(si_dir, "lessons-learned.json")
    
    lessons_data = load_json(lessons_path, {"lessons": []})
    lessons_data["lessons"].append(lesson_record)
    save_json(lessons_path, lessons_data)
    
    # 同步到共享知识库
    shared_dir = get_shared_context_dir()
    shared_path = os.path.join(shared_dir, "collective-wisdom.json")
    
    shared_data = load_json(shared_path, {"lessons": []})
    if "lessons" not in shared_data:
        shared_data["lessons"] = []
    shared_data["lessons"].append(lesson_record)
    save_json(shared_path, shared_data)
    
    return lesson_record


def main():
    parser = argparse.ArgumentParser(description="记录经验教训")
    parser.add_argument("--agent-id", "-a", required=True, help="Agent ID")
    parser.add_argument("--lesson", "-l", required=True, help="学到的经验")
    parser.add_argument("--impact", "-i", required=True, choices=["high", "medium", "low"], 
                       help="影响程度")
    parser.add_argument("--category", "-c", required=True, 
                       choices=["quality", "efficiency", "tools", "knowledge"],
                       help="类别")
    
    args = parser.parse_args()
    
    result = learn_lesson(args.agent_id, args.lesson, args.impact, args.category)
    
    print("\n=== Lesson Learned ===")
    print(f"Agent: {args.agent_id}")
    print(f"Category: {args.category}")
    print(f"Lesson: {args.lesson}")
    print()
    print("Lesson recorded and shared")
    print()
    
    return result


if __name__ == "__main__":
    main()
