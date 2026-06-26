#!/usr/bin/env python3
"""
TravelMaster V8 API测试
"""
import requests
import json

BASE_URL = "http://localhost:7860"

def test_health():
    """测试健康检查"""
    resp = requests.get(f"{BASE_URL}/health")
    data = resp.json()
    
    assert data["status"] == "ok"
    assert data["version"] == "V8-MultiMCP"
    print("✅ 健康检查通过")
    return data

def test_travel_api():
    """测试旅行规划API"""
    resp = requests.post(
        f"{BASE_URL}/api/travel",
        json={"message": "五一去香港"}
    )
    data = resp.json()
    
    assert "reply" in data
    assert "progress" in data
    print("✅ 旅行规划API通过")
    return data

def test_select_plan():
    """测试方案选择API"""
    resp = requests.post(
        f"{BASE_URL}/api/select_plan",
        json={"plan": "A"}
    )
    data = resp.json()
    
    assert "html_report" in data
    print("✅ 方案选择API通过")
    return data

if __name__ == "__main__":
    print("=== TravelMaster V8 API测试 ===")
    
    health = test_health()
    print(f"版本: {health['version']}")
    print(f"功能: {health['features']}")
    
    travel = test_travel_api()
    print(f"进度: {travel['progress']}%")
    
    plan = test_select_plan()
    print(f"HTML长度: {len(plan['html_report'])}字符")
    
    print("\n✅ 所有测试通过")