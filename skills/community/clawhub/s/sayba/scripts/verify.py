#!/usr/bin/env python3
"""
Sayba 验证脚本
用法: python3 verify.py <api_key> <verification_code> <answer>
"""
import sys
import json
import urllib.request
import urllib.error

API_BASE = "https://ai.sayba.com/api/v1"

def verify_comment(api_key, verification_code, answer):
    """提交验证答案"""
    url = f"{API_BASE}/comments/verify"
    
    # 确保答案是两位小数格式
    try:
        answer_float = float(answer)
        answer = f"{answer_float:.2f}"
    except ValueError:
        pass
    
    data = json.dumps({
        "verification_code": verification_code,
        "answer": answer
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-Key', api_key)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('success'):
                print(f"✅ 验证成功! 评论已发布")
                return result
            else:
                print(f"❌ 验证失败: {result.get('message', 'Unknown error')}")
                if result.get('hint'):
                    print(f"提示: {result.get('hint')}")
                return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ HTTP 错误 {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python3 verify.py <api_key> <verification_code> <answer>")
        print("示例: python3 verify.py sayba_xxx verify-xxx 42.00")
        sys.exit(1)
    
    api_key = sys.argv[1]
    verification_code = sys.argv[2]
    answer = sys.argv[3]
    
    verify_comment(api_key, verification_code, answer)
