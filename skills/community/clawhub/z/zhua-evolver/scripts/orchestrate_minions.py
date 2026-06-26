#!/usr/bin/env python3
"""
小弟调度脚本 - 调度6个小弟协同进化
作者：码爪
"""

import argparse

MINIONS = {
    "探爪": {"emoji": "🔍", "role": "搜索新技能、调研技术趋势"},
    "码爪": {"emoji": "💻", "role": "编写进化脚本、自动化工具"},
    "魂爪": {"emoji": "👻", "role": "更新SOUL.md、身份进化"},
    "话爪": {"emoji": "💬", "role": "记录进化日志、对外宣传"},
    "守爪": {"emoji": "🛡️", "role": "监控进化安全、防止回滚"},
    "影爪": {"emoji": "📸", "role": "生成进化可视化、头像更新"}
}

def orchestrate(task):
    """调度小弟执行任务"""
    
    print(f"🐾 调度小弟执行任务: {task}")
    print()
    
    # 根据任务类型分配小弟
    if "搜索" in task or "调研" in task:
        assign_minion("探爪", task)
    elif "编写" in task or "代码" in task:
        assign_minion("码爪", task)
    elif "身份" in task or "SOUL" in task:
        assign_minion("魂爪", task)
    elif "记录" in task or "日志" in task:
        assign_minion("话爪", task)
    elif "安全" in task or "监控" in task:
        assign_minion("守爪", task)
    elif "可视化" in task or "图像" in task:
        assign_minion("影爪", task)
    else:
        # 默认调度所有小弟
        print("🎯 全员出动！")
        for name, info in MINIONS.items():
            assign_minion(name, task)

def assign_minion(name, task):
    """分配任务给小弟"""
    info = MINIONS[name]
    print(f"{info['emoji']} {name}: {info['role']}")
    print(f"   任务: {task}")
    print(f"   状态: 已分配")
    print()

def main():
    parser = argparse.ArgumentParser(description="调度小弟协同进化")
    parser.add_argument("--task", type=str, required=True, help="任务描述")
    
    args = parser.parse_args()
    orchestrate(args.task)

if __name__ == "__main__":
    main()
