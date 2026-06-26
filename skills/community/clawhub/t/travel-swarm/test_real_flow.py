#!/usr/bin/env python3.8
"""真实测试：苏格拉底追问 + 蜂群审核"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/travel_swarm')

import asyncio
from dotenv import load_dotenv
load_dotenv('/home/admin/.openclaw/workspace/travel_swarm/.env')

from backend.agents.travel_swarm_engine import TravelSwarmEngine

async def test():
    engine = TravelSwarmEngine()
    
    print("=" * 60)
    print("【真实测试】苏格拉底追问 + 蜂群审核")
    print("=" * 60)
    
    # 第一轮：用户输入
    user_input = "我想去重庆玩2天，预算2000元，两个人，喜欢吃火锅和看夜景，住解放碑附近。"
    print(f"\n用户输入: {user_input}")
    
    # 第一轮追问
    response1 = await engine.process_user_message(user_input)
    print(f"\n系统回应:\n{response1}")
    
    # 第二轮：回答追问
    user_answer2 = "老火锅，南山一棵树看夜景"
    print(f"\n用户回答: {user_answer2}")
    
    response2 = await engine.process_user_message(user_answer2)
    print(f"\n系统回应:\n{response2}")
    
    # 第三轮：继续追问
    user_answer3 = "预算严格控制，不超过2000"
    print(f"\n用户回答: {user_answer3}")
    
    response3 = await engine.process_user_message(user_answer3)
    print(f"\n系统回应:\n{response3}")
    
    print("\n" + "=" * 60)
    print("【测试完成】")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test())