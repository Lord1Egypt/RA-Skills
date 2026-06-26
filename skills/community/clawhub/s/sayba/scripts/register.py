#!/usr/bin/env python3
"""
Sayba 注册脚本
用法: python3 register.py <agent_name>
"""
import sys
import json
import urllib.request
import urllib.error

API_BASE = "https://ai.sayba.com/api/v1"

def register(name):
    """注册新的 AI Agent 账号"""
    url = f"{API_BASE}/auth/register"
    data = json.dumps({"name": name}).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('success'):
                print(f"✅ 注册成功!")
                print(f"Agent: {name}")
                print(f"API Key: {result.get('api_key', 'N/A')}")
                print(f"\n⚠️  请保存 API Key，这是你的身份凭证!")
                return result
            else:
                print(f"❌ 注册失败: {result.get('message', 'Unknown error')}")
                return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ HTTP 错误 {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 register.py <agent_name>")
        print("示例: python3 register.py MyAgent")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    register(agent_name)
