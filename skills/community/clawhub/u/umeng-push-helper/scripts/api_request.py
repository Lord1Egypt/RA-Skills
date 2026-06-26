#!/usr/bin/env python3
"""
友盟推送后台 API 请求工具
Usage: 
  python api_request.py get_msg_content <msg_id>    - 查询消息详情
  python api_request.py send_test <params>          - 发送测试推送
  python api_request.py custom <url> [method]       - 自定义请求
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.error


def get_cookie():
    """加载保存的 Cookie"""
    script_dir = Path(__file__).parent
    cookie_path = script_dir / 'cookie.json'
    
    if not cookie_path.exists():
        raise Exception("未登录，请先运行 save_cookie.py 保存 Cookie")
    
    with open(cookie_path, 'r', encoding='utf-8') as f:
        cookie_data = json.load(f)
    
    return cookie_data.get('cookie', '')


def extract_ctoken(cookie):
    """从 Cookie 字符串中提取 ctoken 值"""
    for item in cookie.split(';'):
        item = item.strip()
        if item.startswith('ctoken='):
            return item.split('=', 1)[1]
    return None


def make_request(url, method='GET', data=None):
    """发起 HTTP 请求"""
    cookie = get_cookie()
    
    # 提取 ctoken 用于 x-csrf-token 头
    ctoken = extract_ctoken(cookie)
    
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'x-csrf-token': ctoken if ctoken else ""
    }
    
    if data:
        headers['Content-Type'] = 'application/json;charset=UTF-8'
        data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return {
                'success': True,
                'status_code': response.status,
                'data': json.loads(response.read().decode('utf-8'))
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        
        # 检查是否是 401 未授权
        if e.code == 401:
            return {
                'success': False,
                'error': 'UNAUTHORIZED',
                'message': 'Cookie 已过期或无效，请重新登录',
                'status_code': e.code
            }
        
        return {
            'success': False,
            'error': 'HTTP_ERROR',
            'message': f'HTTP {e.code}: {error_body}',
            'status_code': e.code
        }
    except urllib.error.URLError as e:
        return {
            'success': False,
            'error': 'NETWORK_ERROR',
            'message': f'网络错误：{e.reason}'
        }
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'error': 'PARSE_ERROR',
            'message': f'响应解析失败：{e}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': 'UNKNOWN_ERROR',
            'message': str(e)
        }


def get_msg_content(msg_id):
    """查询消息详情"""
    # 注意：这里使用的是 test-tool MCP 服务的接口
    # 如果需要直接调用友盟 API，需要替换为实际的 API 地址
    print(f"📡 正在查询消息：{msg_id}")
    
    # 由于友盟后台 API 可能需要特定的 endpoint，这里提供一个示例
    # 实际使用时需要根据友盟 API 文档调整
    url = "https://upush.umeng.com/api/send/detail"  # 示例 URL，需要替换为实际 API
    
    result = make_request(url, 'POST', {'msg_id': msg_id})
    
    if result['success']:
        print("✅ 查询成功")
        print(json.dumps(result['data'], indent=2, ensure_ascii=False))
    else:
        print(f"❌ 查询失败：{result['message']}")
        
        if result.get('error') == 'UNAUTHORIZED':
            print("\n💡 Cookie 可能已过期，请重新登录:")
            print("   1. 访问 https://upush.umeng.com")
            print("   2. 重新获取 Cookie")
            print("   3. 运行：python save_cookie.py \"新 Cookie\"")
    
    return result


def custom_request(url, method='GET'):
    """自定义 API 请求"""
    print(f"📡 发起 {method} 请求：{url}")
    
    result = make_request(url, method)
    
    if result['success']:
        print("✅ 请求成功")
        print(f"状态码：{result['status_code']}")
        print("\n响应内容:")
        print(json.dumps(result['data'], indent=2, ensure_ascii=False))
    else:
        print(f"❌ 请求失败：{result['message']}")
    
    return result


def print_usage():
    """打印使用说明"""
    print("""
📦 友盟推送 API 请求工具

使用方法:
  python api_request.py get_msg_content <msg_id>     - 查询消息详情
  python api_request.py custom <url> [method]        - 自定义请求
  python api_request.py help                         - 显示此帮助

示例:
  python api_request.py get_msg_content uluzms2177451692046001
  python api_request.py custom https://upush.umeng.com/api/stats GET
  python api_request.py custom https://upush.umeng.com/api/send POST

""")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'help':
        print_usage()
        sys.exit(0)
    
    elif command == 'get_msg_content':
        if len(sys.argv) < 3:
            print("❌ 缺少 msg_id 参数")
            print("用法：python api_request.py get_msg_content <msg_id>")
            sys.exit(1)
        
        msg_id = sys.argv[2]
        result = get_msg_content(msg_id)
        sys.exit(0 if result['success'] else 1)
    
    elif command == 'custom':
        if len(sys.argv) < 3:
            print("❌ 缺少 URL 参数")
            print("用法：python api_request.py custom <url> [method]")
            sys.exit(1)
        
        url = sys.argv[2]
        method = sys.argv[3] if len(sys.argv) > 3 else 'GET'
        result = custom_request(url, method.upper())
        sys.exit(0 if result['success'] else 1)
    
    else:
        print(f"❌ 未知命令：{command}")
        print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
