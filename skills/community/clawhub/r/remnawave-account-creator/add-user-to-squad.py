#!/usr/bin/env python3
"""
使用 Python 调用 Remnawave API 添加用户到分组
"""
import requests
import json
import os

# 读取配置
ENV_FILE = os.path.expanduser('~/.openclaw/workspace/.env')
with open(ENV_FILE) as f:
    for line in f:
        if line.startswith('REMNAWAVE_API_TOKEN='):
            API_TOKEN = line.split('=', 1)[1].strip()
            break

API_BASE = 'https://8.212.8.43'
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

# 目标用户和分组
USERNAME = 'iven_pc'
NEW_SQUAD_UUID = '0a19fbb7-1fea-4862-b1b2-603994b3709a'
EXISTING_SQUAD_UUID = '071aee4a-1234-4c38-8f24-807c5992d9cc'

def main():
    print(f'🔍 查找用户：{USERNAME}...\n')
    
    # 获取用户信息
    resp = requests.get(f'{API_BASE}/api/users/by-username/{USERNAME}', headers=HEADERS, verify=False)
    user_data = resp.json().get('response', {})
    
    if not user_data.get('uuid'):
        print('❌ 用户不存在')
        return
    
    user_uuid = user_data['uuid']
    current_squads = user_data.get('activeInternalSquads', [])
    
    print(f'✅ 找到用户：{user_data["username"]}')
    print(f'   UUID: {user_uuid}')
    print(f'   当前分组：{[s["name"] for s in current_squads]}')
    print()
    
    # 检查是否已在新分组
    current_uuids = [s['uuid'] for s in current_squads]
    if NEW_SQUAD_UUID in current_uuids:
        print('✅ 用户已在 Access Gateway 分组中')
        return
    
    # 添加新分组
    new_squads = current_uuids + [NEW_SQUAD_UUID]
    
    print(f'➕ 准备添加分组：Access Gateway')
    print(f'   添加后分组：{len(new_squads)} 个')
    print()
    
    # 尝试多种 API 端点
    endpoints = [
        ('PUT', f'/api/users/{user_uuid}'),
        ('PUT', f'/api/users/by-username/{USERNAME}'),
        ('PATCH', f'/api/users/{user_uuid}'),
        ('PATCH', f'/api/users/by-username/{USERNAME}'),
        ('POST', f'/api/users/{user_uuid}/squads'),
    ]
    
    for method, endpoint in endpoints:
        print(f'📡 尝试 {method} {endpoint}...')
        
        if method == 'PUT':
            resp = requests.put(f'{API_BASE}{endpoint}', headers=HEADERS, verify=False,
                              json={'activeInternalSquads': new_squads})
        elif method == 'PATCH':
            resp = requests.patch(f'{API_BASE}{endpoint}', headers=HEADERS, verify=False,
                                json={'activeInternalSquads': new_squads})
        elif method == 'POST':
            resp = requests.post(f'{API_BASE}{endpoint}', headers=HEADERS, verify=False,
                               json={'squadUuids': [NEW_SQUAD_UUID], 'operation': 'add'})
        
        print(f'   状态码：{resp.status_code}')
        
        if resp.status_code == 200:
            print('✅ 分组添加成功!')
            # 验证
            resp = requests.get(f'{API_BASE}/api/users/by-username/{USERNAME}', headers=HEADERS, verify=False)
            updated = resp.json().get('response', {})
            print(f'   新分组列表：{[s["name"] for s in updated.get("activeInternalSquads", [])]}')
            return
        else:
            print(f'   响应：{resp.text[:200]}')
    
    print('\n❌ 所有 API 端点都失败')

if __name__ == '__main__':
    main()
