#!/usr/bin/env python3
"""
Task Evaluation Script
评估任务执行并记录结果
"""

import os
import sys
import json
import argparse
from datetime import datetime
from config import get_self_improvement_dir, load_json, save_json


def evaluate_task(agent_id: str, task_id: str, task_type: str,
                  completion: int, efficiency: int, quality: int, satisfaction: int) -> dict:
    """
    评估任务执行
    
    评分公式: 总分 = 完成度(30%) + 效率(20%) + 质量(30%) + 满意度(20%)
    """
    # 计算总分
    total_score = (completion * 0.3) + (efficiency * 0.2) + (quality * 0.3) + (satisfaction * 0.2)
    total_score = round(total_score, 2)
    
    # 创建评估记录
    evaluation = {
        "timestamp": datetime.now().isoformat(),
        "agentId": agent_id,
        "taskId": task_id,
        "taskType": task_type,
        "score": total_score,
        "metrics": {
            "completion": completion,
            "efficiency": efficiency,
            "quality": quality,
            "satisfaction": satisfaction
        }
    }
    
    # 保存到文件
    si_dir = get_self_improvement_dir()
    eval_path = os.path.join(si_dir, "evaluations.json")
    
    eval_data = load_json(eval_path, {"evaluations": []})
    eval_data["evaluations"].append(evaluation)
    save_json(eval_path, eval_data)
    
    return evaluation


def main():
    parser = argparse.ArgumentParser(description="评估任务执行")
    parser.add_argument("--agent-id", "-a", required=True, help="Agent ID")
    parser.add_argument("--task-id", "-t", required=True, help="任务 ID")
    parser.add_argument("--task-type", required=True, help="任务类型")
    parser.add_argument("--completion", "-c", type=int, required=True, help="完成度 (0-100)")
    parser.add_argument("--efficiency", "-e", type=int, required=True, help="效率 (0-100)")
    parser.add_argument("--quality", "-q", type=int, required=True, help="质量 (0-100)")
    parser.add_argument("--satisfaction", "-s", type=int, required=True, help="满意度 (0-100)")
    
    args = parser.parse_args()
    
    result = evaluate_task(
        args.agent_id,
        args.task_id,
        args.task_type,
        args.completion,
        args.efficiency,
        args.quality,
        args.satisfaction
    )
    
    print("\n=== Task Evaluation ===")
    print(f"Agent: {args.agent_id}")
    print(f"Task: {args.task_type} ({args.task_id})")
    print(f"Score: {result['score']}/100")
    print()
    
    # 如果分数低于 70，提示触发优化
    if result['score'] < 70:
        print("Score below 70, consider running optimize-agent.py")
    
    return result


if __name__ == "__main__":
    main()
