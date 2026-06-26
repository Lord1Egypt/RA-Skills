#!/usr/bin/env python3.8
"""
真实验证：MCP高德API客户端
"""

import asyncio
import os
import sys

# 添加路径
sys.path.insert(0, '/home/admin/.openclaw/workspace/travel_swarm')

from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("【真实验证】MCP高德API客户端")
print("=" * 60)

# 直接导入amap_client
import importlib.util
spec = importlib.util.spec_from_file_location("amap_client", 
    "/home/admin/.openclaw/workspace/travel_swarm/backend/mcp/amap_client.py")
amap_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(amap_module)

AMAP_KEY = "a8b1798825bfafb84c26bb5d76279cdc"

async def test_mcp():
    client = amap_module.AmapMCPClient(AMAP_KEY)
    
    print("\n【1】地理编码测试")
    try:
        loc = await client.geocode("北京市故宫")
        print("故宫坐标:", loc)
    except Exception as e:
        print("错误:", str(e)[:200])
    
    print("\n【2】天气查询测试")
    try:
        weather = await client.weather("北京")
        if "lives" in weather:
            w = weather["lives"][0]
            print(f"北京天气: {w['weather']} {w['temperature']}°C")
        else:
            print("返回:", weather)
    except Exception as e:
        print("错误:", str(e)[:200])
    
    print("\n【3】POI搜索测试")
    try:
        pois = await client.search_poi("火锅", "重庆", limit=5)
        print(f"找到 {len(pois)} 家火锅店:")
        for i, p in enumerate(pois[:3], 1):
            print(f"  {i}. {p['name']} - {p.get('address', '无地址')}")
    except Exception as e:
        print("错误:", str(e)[:200])
    
    print("\n【4】酒店搜索测试")
    try:
        hotels = await client.search_poi("酒店", "重庆", types="150700", limit=5)
        print(f"找到 {len(hotels)} 家酒店:")
        for i, h in enumerate(hotels[:3], 1):
            name = h.get('name', '未知')
            addr = h.get('address', '无地址')
            rating = h.get('biz_ext', {}).get('rating', '无评分')
            print(f"  {i}. {name} | 评分:{rating} | {addr}")
    except Exception as e:
        print("错误:", str(e)[:200])
    
    print("\n【5】路线规划测试")
    try:
        route = await client.route_plan("重庆解放碑", "重庆洪崖洞", mode="driving", city="重庆")
        if "route" in route:
            paths = route["route"]["paths"][0]
            dist = paths.get("distance", "未知")
            time = paths.get("duration", "未知")
            print(f"解放碑→洪崖洞: {dist}米, {time}秒")
        else:
            print("返回:", str(route)[:300])
    except Exception as e:
        print("错误:", str(e)[:200])

print("\n开始执行...")
asyncio.run(test_mcp())
print("\n" + "=" * 60)
print("【验证完成】")
print("=" * 60)