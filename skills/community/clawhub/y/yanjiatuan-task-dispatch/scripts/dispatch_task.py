#!/usr/bin/env python3
"""研家团 · 团队任务调度脚本"""
import json, sys, argparse
from datetime import datetime

def dispatch(task_desc, stocks):
    stocks_list = [s.strip() for s in stocks.split(",")] if stocks else []
    task_id = f"T{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"
    
    result = {
        "task_id": task_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "task": task_desc,
        "stocks": stocks_list,
        "dispatch": {
            "yanmu": {"assigned": [f"基本面分析：{s}" for s in stocks_list], "status": "pending"},
            "yanlin": {"assigned": [f"产业策略分析" if not stocks_list else f"产业策略：{stocks_list[0]}所处赛道"], "status": "pending"},
            "yanji": {"assigned": [f"技术面分析：{s}" for s in stocks_list], "status": "pending"},
            "yansheng": {"assigned": [f"舆情分析：{s}" for s in stocks_list], "status": "pending"},
            "yandun": {"assigned": [f"风险评估：{s}" for s in stocks_list], "status": "pending"}
        },
        "workflow": "各角色并行分析 → 汇总输出 → 冲突修正 → 研策合成报告 → 审核交付",
        "next_step": "分派各角色执行分析任务"
    }
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="研家团任务调度")
    parser.add_argument("--task", default="自选股综合投研分析", help="投研需求描述")
    parser.add_argument("--stocks", default="", help="标的列表，逗号分隔")
    parser.add_argument("--output", choices=["json", "text"], default="text")
    args = parser.parse_args()
    result = dispatch(args.task, args.stocks)
    if args.output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"📋 任务ID: {result['task_id']}")
        print(f"📝 任务: {result['task']}")
        print(f"📊 标的: {', '.join(result['stocks']) if result['stocks'] else '待指定'}")
        print(f"\n👥 分派情况:")
        for agent, info in result['dispatch'].items():
            print(f"  {agent}: {', '.join(info['assigned'])} [{info['status']}]")
        print(f"\n📌 下一步: {result['next_step']}")
