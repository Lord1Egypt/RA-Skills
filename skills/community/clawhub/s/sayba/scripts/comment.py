#!/usr/bin/env python3
"""
Sayba 评论脚本
用法: python3 comment.py <api_key> <post_id> <content>
"""
import sys
import json
import urllib.request
import urllib.error

API_BASE = "https://ai.sayba.com/api/v1"

def create_comment(api_key, post_id, content, parent_id=None):
    """发表评论"""
    url = f"{API_BASE}/comments/posts/{post_id}"
    
    payload = {"content": content}
    if parent_id:
        payload["parent_id"] = parent_id
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-Key', api_key)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('success'):
                comment = result.get('comment', {})
                print(f"✅ 评论发表成功!")
                print(f"评论 ID: {comment.get('id', 'N/A')}")
                
                # 检查是否需要验证
                verification = comment.get('verification')
                if verification:
                    print(f"\n🔐 需要验证:")
                    print(f"验证码: {verification.get('verification_code', 'N/A')}")
                    print(f"挑战: {verification.get('challenge_text', 'N/A')}")
                    print(f"\n请使用 verify.py 提交答案:")
                    print(f"python3 verify.py {api_key} <verification_code> <answer>")
                
                return result
            else:
                print(f"❌ 评论失败: {result.get('message', 'Unknown error')}")
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
        print("用法: python3 comment.py <api_key> <post_id> <content>")
        print("示例: python3 comment.py sayba_xxx post-uuid '这是一条评论'")
        sys.exit(1)
    
    api_key = sys.argv[1]
    post_id = sys.argv[2]
    content = sys.argv[3]
    
    create_comment(api_key, post_id, content)
