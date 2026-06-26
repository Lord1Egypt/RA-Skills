#!/usr/bin/env python3
"""
团队协作高级模式 - 真正切换模型
通过 OpenClaw sessions_spawn API 调用不同模型
"""

import json
import os
from datetime import datetime

# 模型配置
ROLES = {
    "product_manager": {
        "name": "产品经理",
        "model": "bailian/qwen-plus"
    },
    "developer": {
        "name": "程序员",
        "model": "bailian/glm-5"
    },
    "designer": {
        "name": "设计师",
        "model": "bailian/qwen3.5-plus"
    },
    "tester": {
        "name": "测试工程师",
        "model": "deepseek-coder"
    },
    "reviewer": {
        "name": "代码审查员",
        "model": "bailian/qwen-max"
    }
}

def print_spawn_instruction(role_key, task):
    """打印 spawn 调用指令"""
    role = ROLES[role_key]
    print(f"""
## 阶段：{role['name']}

使用 sessions_spawn 调用：
- agentId: "{role['model']}"
- task: "{task}"
- mode: "run"

示例代码：
sessions_spawn(
    agentId="{role['model']}",
    task="[具体任务描述]",
    mode="run"
)
""")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python team-workflow.py <项目需求>")
        print("\n这会生成各阶段的 spawn 调用指令")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    
    print("=" * 50)
    print("团队协作高级模式 - 模型切换")
    print("=" * 50)
    print(f"\n项目：{task}\n")
    
    workflow = [
        ("product_manager", "分析需求，输出需求文档"),
        ("developer", "根据需求文档，实现代码"),
        ("designer", "根据需求和代码，设计UI"),
        ("tester", "测试代码，输出测试报告"),
        ("reviewer", "审查代码，输出审查报告")
    ]
    
    for role_key, role_task in workflow:
        print_spawn_instruction(role_key, role_task)
        print("-" * 50)

if __name__ == "__main__":
    main()