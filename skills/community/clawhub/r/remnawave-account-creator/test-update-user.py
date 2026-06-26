#!/usr/bin/env python3
"""
Remnawave API 用户更新测试脚本
测试不同的 API 端点和参数组合
"""

import requests
import json
import os

# 配置
API_BASE = "https://8.212.8.43"
TOKEN = os.environ.get('REMNAWAVE_API_TOKEN')
if not TOKEN:
    with open(os.path.expanduser('~/.openclaw/workspace/.env'), 'r') as f:
        for line in f:
            if line.startswith('REMNAWAVE_API_TOKEN='):
                TOKEN = line.split('=')[1].strip()
                break

HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

# 测试用户
USER_UUID = "5ce517c7-4fe6-4850-ab21-67dbf1e03b52"
USERNAME = "iven_pc"
SQUAD_UUIDS = ["0a19fbb7-1fea-4862-b1b2-603994b3709a", "1f85b65c-c604-4ef7-9a05-7ab0a86a3194"]

def test_endpoint(method, endpoint, data=None, desc=""):
    """测试 API 端点"""
    url = f"{API_BASE}{endpoint}"
    print(f"\n{'='*60}")
    print(f"测试：{desc}")
    print(f"端点：{method} {endpoint}")
    print(f"{'='*60}")
    
    try:
        if method == 'GET':
            resp = requests.get(url, headers=HEADERS, verify=False)
        elif method == 'PUT':
            resp = requests.put(url, json=data, headers=HEADERS, verify=False)
        elif method == 'PATCH':
            resp = requests.patch(url, json=data, headers=HEADERS, verify=False)
        elif method == 'POST':
            resp = requests.post(url, json=data, headers=HEADERS, verify=False)
        
        print(f"状态码：{resp.status_code}")
        try:
            print(f"响应：{json.dumps(resp.json(), indent=2, ensure_ascii=False)}")
        except:
            print(f"响应：{resp.text[:500]}")
        
        return resp.status_code, resp.json()
    except Exception as e:
        print(f"错误：{e}")
        return None, None

def main():
    print("🔍 Remnawave API 用户更新端点测试")
    print(f"测试用户：{USERNAME} ({USER_UUID})")
    
    # 测试 1: GET 用户信息
    test_endpoint('GET', f'/api/users/by-username/{USERNAME}', desc="获取用户信息")
    
    # 测试 2: PUT /api/users/{uuid} - 只传分组
    test_endpoint('PUT', f'/api/users/{USER_UUID}', 
                  data={'activeInternalSquads': SQUAD_UUIDS},
                  desc="PUT /api/users/{uuid} - 只传分组")
    
    # 测试 3: PUT /api/users/{uuid} - 传完整数据
    test_endpoint('PUT', f'/api/users/{USER_UUID}', 
                  data={
                      'username': USERNAME,
                      'email': 'iven@codeforce.tech',
                      'hwidDeviceLimit': 1,
                      'trafficLimitBytes': 107374182400,
                      'trafficLimitStrategy': 'WEEK',
                      'expireAt': '2027-03-11T09:16:57.322Z',
                      'activeInternalSquads': SQUAD_UUIDS
                  },
                  desc="PUT /api/users/{uuid} - 传完整数据")
    
    # 测试 4: PATCH /api/users/{uuid}
    test_endpoint('PATCH', f'/api/users/{USER_UUID}', 
                  data={'activeInternalSquads': SQUAD_UUIDS},
                  desc="PATCH /api/users/{uuid}")
    
    # 测试 5: PUT /api/users/{username}
    test_endpoint('PUT', f'/api/users/{USERNAME}', 
                  data={'activeInternalSquads': SQUAD_UUIDS},
                  desc="PUT /api/users/{username}")
    
    # 测试 6: PATCH /api/users/{username}
    test_endpoint('PATCH', f'/api/users/{USERNAME}', 
                  data={'activeInternalSquads': SQUAD_UUIDS},
                  desc="PATCH /api/users/{username}")
    
    # 测试 7: POST /api/users/{uuid}/squads
    test_endpoint('POST', f'/api/users/{USER_UUID}/squads', 
                  data={'squadUuids': SQUAD_UUIDS},
                  desc="POST /api/users/{uuid}/squads")
    
    # 测试 8: PUT /api/users/{uuid}/squads
    test_endpoint('PUT', f'/api/users/{USER_UUID}/squads', 
                  data={'squadUuids': SQUAD_UUIDS},
                  desc="PUT /api/users/{uuid}/squads")
    
    # 测试 9: GET /api/internal-squads
    test_endpoint('GET', '/api/internal-squads', desc="获取内部组列表")

if __name__ == '__main__':
    main()
