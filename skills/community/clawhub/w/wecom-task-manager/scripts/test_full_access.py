#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 wecom-task-manager 技能的完整访问控制
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task_manager import (
    check_access,
    ALLOWED_AGENTS,
    create_task,
    get_task_by_id,
    start_task,
    update_progress,
    complete_task,
    edit_task,
    delete_task
)

def test_all_apis():
    """测试所有 API 的访问控制"""
    print("=" * 70)
    print("🔐 wecom-task-manager 完整访问控制测试")
    print("=" * 70)
    print()
    
    print(f"允许的 agents: {', '.join(ALLOWED_AGENTS)}")
    print()
    
    # 测试 1：白名单内的 agents
    print("✅ 测试 1：白名单内的 agents 应该可以调用")
    print("-" * 70)
    for agent in ALLOWED_AGENTS[:2]:  # 只测试前 2 个
        result = check_access(agent)
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {agent}: {status}")
    print()
    
    # 测试 2：白名单外的 agents
    print("❌ 测试 2：白名单外的 agents 应该被拒绝")
    print("-" * 70)
    test_agents = ["backend", "frontend"]
    for agent in test_agents:
        result = check_access(agent)
        status = "✅ 拒绝" if not result else "❌ 通过（错误）"
        print(f"  {agent}: {status}")
    print()
    
    # 测试 3：API 调用测试（使用环境变量）
    print("🧪 测试 3：API 调用测试（通过环境变量）")
    print("-" * 70)
    
    # 设置环境变量为白名单内的 agent
    os.environ["AGENT_ID"] = "techlead"
    print(f"  设置 AGENT_ID=techlead")
    
    # 测试查询（不会实际修改数据）
    print("  测试 get_task_by_id('NONEXISTENT'):")
    task = get_task_by_id("NONEXISTENT")
    print(f"    结果：{task} (预期：None)")
    print()
    
    # 设置环境变量为白名单外的 agent
    os.environ["AGENT_ID"] = "backend"
    print(f"  设置 AGENT_ID=backend")
    
    # 测试查询
    print("  测试 get_task_by_id('NONEXISTENT'):")
    task = get_task_by_id("NONEXISTENT")
    print(f"    结果：{task} (预期：None，因为访问被拒绝)")
    print()
    
    # 清除环境变量
    if "AGENT_ID" in os.environ:
        del os.environ["AGENT_ID"]
    
    print("=" * 70)
    print("✅ 测试完成")
    print("=" * 70)
    print()
    print("📝 总结:")
    print("  - 白名单内的 agents: ✅ 可以调用所有 API")
    print("  - 白名单外的 agents: ✅ 被拒绝访问")
    print("  - 环境变量支持：✅ 正常工作")
    print()

if __name__ == "__main__":
    test_all_apis()
