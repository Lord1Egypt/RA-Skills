#!/usr/bin/env python3
"""
SlonAide API 测试脚本
用于快速测试 API 连接和功能
"""

import sys
import json
import requests
from datetime import datetime

def test_api_connection(api_key):
    """测试 API 连接"""
    base_url = "https://api.aidenote.cn"
    
    print("=" * 60)
    print("SlonAide API 连接测试")
    print("=" * 60)
    
    # 1. 测试认证
    print("\n1. 测试认证...")
    token_url = f"{base_url}/api/UserapikeyMstr/GetToken/{api_key}"
    
    try:
        response = requests.post(token_url, headers={'Content-Type': 'application/json'}, timeout=10)
        data = response.json()
        
        if data.get("code") == 200:
            token = data["result"]["token"]
            user_id = data["result"]["userId"]
            print(f"✅ 认证成功")
            print(f"   用户ID: {user_id}")
            print(f"   令牌: {token[:20]}...")
        else:
            print(f"❌ 认证失败: {data.get('message', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 认证请求失败: {e}")
        return False
    
    # 2. 测试获取列表
    print("\n2. 测试获取笔记列表...")
    list_url = f"{base_url}/api/audiofileMstr/audiofileseleUserAllList"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'order': 'descending',
        'orderField': 'createTime',
        'page': 1,
        'pageSize': 3
    }
    
    try:
        response = requests.post(list_url, headers=headers, json=payload, timeout=10)
        data = response.json()
        
        if data.get("code") == 200:
            result = data["result"]
            total = result.get("total", 0)
            records = result.get("records", result.get("items", []))
            
            print(f"✅ 获取列表成功")
            print(f"   总记录数: {total}")
            print(f"   当前页记录数: {len(records)}")
            
            if records:
                print(f"\n   最新记录:")
                for i, record in enumerate(records[:3], 1):
                    title = record.get('audiofileTitle', record.get('audiofileFileName', '未命名'))
                    file_id = record.get('id', '未知ID')
                    print(f"   {i}. {title}")
                    print(f"      ID: {file_id}")
        else:
            print(f"❌ 获取列表失败: {data.get('message', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 获取列表请求失败: {e}")
        return False
    
    # 3. 测试获取详情（如果有记录）
    if records:
        print("\n3. 测试获取笔记详情...")
        first_record = records[0]
        file_id = first_record.get('id')
        
        if file_id:
            detail_url = f"{base_url}/api/audiofileMstr/GetAudioFileDetail/{file_id}"
            
            try:
                response = requests.get(detail_url, headers=headers, timeout=10)
                data = response.json()
                
                if data.get("code") == 200:
                    detail = data["result"]
                    transcript = detail.get('transcriptText', '')
                    summary = detail.get('aiSummary', '')
                    
                    print(f"✅ 获取详情成功")
                    if transcript:
                        print(f"   转写文本长度: {len(transcript)} 字符")
                    if summary:
                        print(f"   AI 总结: {summary[:100]}...")
                else:
                    print(f"⚠️ 获取详情失败: {data.get('message', '未知错误')}")
            except Exception as e:
                print(f"⚠️ 获取详情请求失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    return True

def main():
    if len(sys.argv) < 2:
        print("使用方法: python test_api.py <API_KEY>")
        print("示例: python test_api.py sk-xxx...")
        sys.exit(1)
    
    api_key = sys.argv[1]
    
    # 验证 API Key 格式
    if not api_key.startswith('sk-'):
        print("⚠️ 警告: API Key 格式可能不正确，应以 'sk-' 开头")
    
    success = test_api_connection(api_key)
    
    if success:
        print("\n✅ 所有测试通过！API 连接正常。")
        print("\n下一步:")
        print("1. 在 OpenClaw 中配置此 API Key")
        print("2. 使用 'slonaide_test_connection' 测试插件")
        print("3. 开始使用 SlonAide 技能")
    else:
        print("\n❌ 测试失败，请检查:")
        print("1. API Key 是否正确")
        print("2. 网络连接是否正常")
        print("3. SlonAide 服务是否可用")
        sys.exit(1)

if __name__ == "__main__":
    main()