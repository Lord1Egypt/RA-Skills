#!/usr/bin/env python3
"""
Agent Optimization Script
分析评估记录并生成优化计划
"""

import os
import sys
import json
import argparse
from datetime import datetime
from config import get_self_improvement_dir, load_json, save_json


def optimize_agent(agent_id: str) -> dict:
    """
    分析评估数据并生成优化计划
    """
    si_dir = get_self_improvement_dir()
    eval_path = os.path.join(si_dir, "evaluations.json")
    
    if not os.path.exists(eval_path):
        print("⚠️  No evaluations found. Run evaluate-task.py first.")
        return None
    
    eval_data = load_json(eval_path)
    evaluations = eval_data.get("evaluations", [])
    
    # 筛选当前 Agent 的评估
    agent_evals = [e for e in evaluations if e.get("agentId") == agent_id]
    
    if not agent_evals:
        print(f"⚠️  No evaluations for agent: {agent_id}")
        return None
    
    # 按时间排序，取最近10条
    agent_evals.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    recent_evals = agent_evals[:10]
    
    # 计算平均分
    avg_score = sum(e["score"] for e in recent_evals) / len(recent_evals)
    avg_score = round(avg_score, 2)
    
    print(f"\n=== Agent Optimization ===")
    print(f"Agent: {agent_id}")
    print()
    print("Recent Performance:")
    
    # 颜色输出
    if avg_score >= 80:
        score_color = "green"
    elif avg_score >= 70:
        score_color = "yellow"
    else:
        score_color = "red"
    
    print(f"  Average Score: {avg_score}/100")
    print(f"  Evaluated Tasks: {len(recent_evals)}")
    print()
    
    # 识别改进点
    low_scores = [e for e in recent_evals if e["score"] < 70]
    
    if low_scores:
        print("Areas for Improvement:")
        for eval_item in low_scores:
            print(f"  - Task: {eval_item.get('taskType')}")
            print(f"    Score: {eval_item['score']}")
            print(f"    Time: {eval_item.get('timestamp', 'N/A')}")
        
        # 生成优化计划
        optimization_plan = {
            "planId": f"opt-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "agent": agent_id,
            "generatedAt": datetime.now().isoformat(),
            "currentScore": avg_score,
            "targetScore": min(90, round(avg_score + 10, 2)),
            "actions": []
        }
        
        # 添加优化动作
        for eval_item in low_scores:
            optimization_plan["actions"].append({
                "action": f"Review and improve {eval_item.get('taskType')} workflow",
                "status": "pending",
                "priority": "high",
                "relatedTask": eval_item.get("taskId")
            })
        
        # 添加通用优化建议
        if avg_score < 70:
            optimization_plan["actions"].append({
                "action": "Review recent lessons-learned.json for patterns",
                "status": "pending",
                "priority": "medium"
            })
            optimization_plan["actions"].append({
                "action": "Consider updating skills or tools",
                "status": "pending",
                "priority": "medium"
            })
        
        # 保存优化计划
        plan_path = os.path.join(si_dir, "optimization-plan.json")
        save_json(plan_path, optimization_plan)
        
        print()
        print(f"✅ Optimization plan generated")
        print(f"   Target Score: {optimization_plan['targetScore']}")
        print(f"   Actions: {len(optimization_plan['actions'])}")
        
        return optimization_plan
    else:
        print("✅ Performance is good, no immediate optimization needed")
        
        # 如果分数在 80-89 之间，提供主动优化建议
        if 80 <= avg_score < 90:
            print()
            print("💡 Suggestion for excellence:")
            print("   Review best practices in evaluations.json to reach >90")
        
        return {"status": "good", "score": avg_score}


def main():
    parser = argparse.ArgumentParser(description="Agent 优化分析")
    parser.add_argument("--agent-id", "-a", required=True, help="Agent ID")
    
    args = parser.parse_args()
    
    return optimize_agent(args.agent_id)


if __name__ == "__main__":
    main()
