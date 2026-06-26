#!/usr/bin/env python3.8
"""真实测试 - 获取完整错误堆栈"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/travel_swarm')

import asyncio
from dotenv import load_dotenv
load_dotenv('/home/admin/.openclaw/workspace/travel_swarm/.env')

from backend.agents.travel_swarm_engine import TravelSwarmEngine

print("=" * 60)
print("【真实引擎测试 - 完整错误堆栈】")
print("=" * 60)

async def test():
    engine = TravelSwarmEngine()
    
    user_input = "我想去重庆玩2天，预算2000，两个人，喜欢火锅和夜景"
    print(f"\n用户输入: {user_input}")
    
    try:
        response = await engine.process_user_message(user_input)
        print(f"\n成功响应: {response[:200]}")
    except Exception as e:
        print(f"\n❌ 错误类型: {type(e).__name__}")
        print(f"❌ 错误信息: {str(e)}")
        print("\n完整错误堆栈:")
        import traceback
        traceback.print_exc()

asyncio.run(test())