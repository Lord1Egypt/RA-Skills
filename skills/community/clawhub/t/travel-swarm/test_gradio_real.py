#!/usr/bin/env python3.8
"""真实Gradio对话测试"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/travel_swarm')

import requests
import json

url = "http://localhost:7860/api/predict"

data = {
    "data": ["我想去重庆玩2天，预算2000元，两个人，喜欢火锅和夜景", []],
    "event_data": None,
    "fn_index": 0
}

print("=" * 60)
print("【真实Gradio对话测试】")
print("=" * 60)
print(f"请求URL: {url}")
print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")

try:
    resp = requests.post(url, json=data, timeout=30)
    print(f"\n状态码: {resp.status_code}")
    print(f"\n返回内容:")
    print(resp.text[:500])
    
    if resp.status_code == 200:
        result = resp.json()
        print(f"\n解析结果: {json.dumps(result, ensure_ascii=False, indent=2)[:300]}")
    else:
        print(f"\n错误响应: {resp.text}")
        
except Exception as e:
    print(f"\n请求失败: {str(e)}")

print("\n" + "=" * 60)