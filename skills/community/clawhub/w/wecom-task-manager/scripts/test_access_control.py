#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 wecom-task-manager 技能的访问控制
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task_manager import check_access, ALLOWED_AGENTS

def test_access_control():
    """测试访问控制"""
    print("=" * 60)
    print("🔐 wecom-task-manager 访问控制测试")
    print("=" * 60)
    print()
    
    print(f"允许的 agents: {', '.join(ALLOWED_AGENTS)}")
    print(f"访问控制开关：{'✅ 启用' if check_access.__globals__['ACCESS_CONTROL_ENABLED'] else '❌ 禁用'}")
    print()
    
    # 测试白名单内的 agents
    print("✅ 测试白名单内的 agents:")
    for agent in ALLOWED_AGENTS:
        result = check_access(agent)
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {agent}: {status}")
    print()
    
    # 测试白名单外的 agents
    print("❌ 测试白名单外的 agents:")
    test_agents = ["backend", "frontend", "copywriter", "unknown_agent"]
    for agent in test_agents:
        result = check_access(agent)
        status = "✅ 通过" if result else "❌ 拒绝"
        print(f"  {agent}: {status}")
    print()
    
    # 测试空 agent_id
    print("⚠️ 测试空 agent_id:")
    result = check_access("")
    status = "✅ 通过" if result else "❌ 拒绝"
    print(f"  空 ID: {status}")
    print()
    
    print("=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_access_control()
