#!/usr/bin/env python3
"""
团队协作高级模式 - 真正切换模型
通过 OpenClaw sessions_spawn API 调用不同模型
v1.2.0 - 新增法律顾问、艺术专家、市场分析专家
"""

import json
import os
import sys
from datetime import datetime

# 模型配置（8人团队）
ROLES = {
    # 核心团队
    "product_manager": {
        "name": "产品经理",
        "model": "bailian/qwen-plus",
        "type": "core",
        "description": "需求分析、功能设计、优先级排序"
    },
    "developer": {
        "name": "程序员",
        "model": "bailian/glm-5",
        "type": "core",
        "description": "代码开发、功能实现、技术方案"
    },
    "designer": {
        "name": "设计师",
        "model": "bailian/qwen3.5-plus",
        "type": "core",
        "description": "UI设计、视觉优化、交互方案"
    },
    "tester": {
        "name": "测试工程师",
        "model": "deepseek-coder",
        "type": "core",
        "description": "功能测试、Bug定位、测试报告"
    },
    "reviewer": {
        "name": "代码审查员",
        "model": "bailian/qwen-max",
        "type": "core",
        "description": "代码审查、性能优化、安全检查"
    },
    # 专业顾问
    "legal_advisor": {
        "name": "法律顾问",
        "model": "bailian/qwen-max",
        "type": "advisor",
        "description": "合规审查、风险防控、知识产权"
    },
    "art_expert": {
        "name": "艺术专家",
        "model": "bailian/qwen3.5-plus",
        "type": "advisor",
        "description": "创意指导、审美把控、艺术风格"
    },
    "market_analyst": {
        "name": "市场分析专家",
        "model": "bailian/qwen-plus",
        "type": "advisor",
        "description": "市场调研、竞品分析、商业策略"
    }
}

def print_spawn_instruction(role_key, task, previous_output=None):
    """打印 spawn 调用指令"""
    role = ROLES[role_key]
    role_type = "【核心】" if role["type"] == "core" else "【顾问】"
    
    print(f"""
{'='*50}
{role_type} 阶段：{role['name']}
{'='*50}

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
    if len(sys.argv) < 2:
        print("=" * 50)
        print("团队协作高级模式 - 模型切换 v1.2.0")
        print("=" * 50)
        print("\n用法：python team-workflow.py <项目需求> [--full|--core|--minimal]")
        print("\n选项：")
        print("  --full     全员协作（8人，含顾问）")
        print("  --core     核心团队（5人，默认）")
        print("  --minimal  最小团队（产品+开发）")
        print("\n这会生成各阶段的 spawn 调用指令")
        sys.exit(1)
    
    # 解析参数
    args = sys.argv[1:]
    mode = "core"  # 默认核心团队
    
    if "--full" in args:
        mode = "full"
        args.remove("--full")
    elif "--minimal" in args:
        mode = "minimal"
        args.remove("--minimal")
    
    task = " ".join(args)
    
    print("=" * 50)
    print("团队协作高级模式 - 模型切换 v1.2.0")
    print("=" * 50)
    print(f"\n项目：{task}")
    print(f"模式：{mode}")
    print()
    
    # 根据模式定义工作流
    if mode == "full":
        # 全员协作
        workflow = [
            ("product_manager", "分析需求，输出需求文档和功能列表"),
            ("market_analyst", "市场调研，竞品分析，商业建议（基于需求文档）"),
            ("developer", "根据需求文档，实现核心代码"),
            ("designer", "根据需求和代码，设计UI方案"),
            ("art_expert", "创意指导，视觉风格建议（基于设计方案）"),
            ("legal_advisor", "合规审查，风险提示，法律建议"),
            ("tester", "功能测试，Bug定位，输出测试报告"),
            ("reviewer", "代码审查，性能优化建议，质量评分")
        ]
        team_size = 8
    elif mode == "minimal":
        # 最小团队
        workflow = [
            ("product_manager", "分析需求，输出需求文档"),
            ("developer", "根据需求文档，实现代码")
        ]
        team_size = 2
    else:
        # 核心团队（默认）
        workflow = [
            ("product_manager", "分析需求，输出需求文档"),
            ("developer", "根据需求文档，实现代码"),
            ("designer", "根据需求和代码，设计UI"),
            ("tester", "测试代码，输出测试报告"),
            ("reviewer", "审查代码，输出审查报告")
        ]
        team_size = 5
    
    print(f"团队规模：{team_size} 人")
    print("-" * 50)
    
    for i, (role_key, role_task) in enumerate(workflow, 1):
        role = ROLES[role_key]
        role_type = "核心" if role["type"] == "core" else "顾问"
        print(f"\n[{i}/{len(workflow)}] {role['name']} ({role_type})")
        print(f"    任务：{role_task}")
        print(f"    模型：{role['model']}")
        print("-" * 50)
    
    print("\n" + "=" * 50)
    print("调用说明")
    print("=" * 50)
    print("""
在对话中，按照上述顺序依次调用各角色：

1. 以产品经理身份开始需求分析
2. 完成后，切换到下一角色继续
3. 最后汇总所有角色的输出

触发方式：
- "用团队协作高级模式"
- "切换模型协作"
""")

if __name__ == "__main__":
    main()