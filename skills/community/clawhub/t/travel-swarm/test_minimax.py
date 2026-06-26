#!/usr/bin/env python3.8
"""测试MiniMax TokenPlan API"""

import asyncio
import os
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/travel_swarm')

from dotenv import load_dotenv
load_dotenv()

from backend.utils.minimax_client import minimax_client

async def test():
    print("=" * 60)
    print("【MiniMax TokenPlan API测试】")
    print("=" * 60)
    
    key = os.getenv("MINIMAX_API_KEY")
    print(f"API Key: {key[:20]}...")
    
    models = ["MiniMax-M2.5", "MiniMax-M2.7", "MiniMax-M2.7-highspeed"]
    
    for model in models:
        print(f"\n【测试】{model}")
        try:
            result = await minimax_client.call("请用一句话介绍重庆火锅", model)
            print(f"返回: {result[:100]}...")
            print(f"✅ {model} 成功")
        except Exception as e:
            print(f"❌ {model} 失败: {str(e)[:200]}")
    
    print("\n" + "=" * 60)
    print("【蜂群模型测试】")
    print("=" * 60)
    
    from backend.agents.review_swarm import ReviewSwarm
    
    swarm = ReviewSwarm()
    print(f"蜂女王模型: {swarm.queen.model}")
    print(f"时间蜂模型: {swarm.workers[0].model_type}")
    print(f"预算蜂模型: {swarm.workers[1].model_type}")
    print(f"体验蜂模型: {swarm.workers[2].model_type}")
    
    # 测试蜂群审核
    test_plan = {
        "destination": "重庆",
        "days": 2,
        "budget": 2000,
        "schedule": "Day1: 解放碑→火锅→洪崖洞"
    }
    
    print("\n开始蜂群审核...")
    result = await swarm.review_plan(test_plan)
    print(f"审核结果: {result['approved']}")
    print(f"详情: {result['summary']}")

if __name__ == "__main__":
    asyncio.run(test())