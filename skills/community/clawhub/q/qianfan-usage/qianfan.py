#!/usr/bin/env python3
"""
百度千帆 Coding Plan 用量快速查询
直接使用保存的 cookie，无需登录
"""

import json
import subprocess
import sys
import os

AUTH_FILE = os.path.expanduser("~/.baidu-qianfan-auth.json")
API_URL = "https://console.bce.baidu.com/api/qianfan/charge/codingPlan/quota"

def load_cookies():
    """加载保存的 cookies"""
    if not os.path.exists(AUTH_FILE):
        return None
    
    with open(AUTH_FILE, 'r') as f:
        data = json.load(f)
    return data.get('cookies', [])

def build_cookie_string(cookies):
    """构建 cookie 字符串"""
    parts = []
    for c in cookies:
        if 'baidu.com' in c.get('domain', ''):
            parts.append(f"{c['name']}={c['value']}")
    return '; '.join(parts)

def query():
    """查询用量"""
    cookies = load_cookies()
    if not cookies:
        return None, "未找到 cookie，请先登录"
    
    cmd = [
        'curl', '-s', '-L', API_URL,
        '-H', f'Cookie: {build_cookie_string(cookies)}',
        '-H', 'Referer: https://console.bce.baidu.com/qianfan/resource/subscribe',
        '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        return None, result.stderr
    
    try:
        data = json.loads(result.stdout)
        if not data.get('success'):
            return None, data.get('message', '查询失败')
        return data['result']['quota'], None
    except (json.JSONDecodeError, KeyError) as e:
        return None, f"解析失败: {e}"

def format_time(t):
    """格式化时间"""
    return t.replace('T', ' ').replace('+08:00', '')[:16]

def main():
    quota, error = query()
    
    if error:
        print(f"❌ {error}")
        return 1
    
    print("=" * 50)
    print("📊 千帆 Coding Plan 用量")
    print("=" * 50)
    
    for name, key in [('5小时', 'fiveHour'), ('本周', 'week'), ('本月', 'month')]:
        q = quota.get(key, {})
        used, limit = q.get('used', 0), q.get('limit', 0)
        pct = used / limit * 100 if limit else 0
        reset = format_time(q.get('resetAt', '未知'))
        print(f"\n⏱️ {name}: {used}/{limit} ({pct:.1f}%)")
        print(f"   剩余: {limit - used} | 重置: {reset}")
    
    print("\n" + "=" * 50)
    return 0

if __name__ == '__main__':
    sys.exit(main())
