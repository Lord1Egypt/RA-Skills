#!/usr/bin/env python3
"""
百度千帆 Coding Plan 用量查询工具
使用保存的 cookie 直接查询 API，避免重复登录
"""

import json
import subprocess
import sys
import os
from datetime import datetime

AUTH_FILE = os.path.expanduser("~/.baidu-qianfan-auth.json")
API_URL = "https://console.bce.baidu.com/api/qianfan/charge/codingPlan/quota"

# 颜色定义
CYAN = '\033[0;36m'
BLUE = '\033[0;34m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
NC = '\033[0m'

def load_cookies():
    """从状态文件加载 cookies"""
    if not os.path.exists(AUTH_FILE):
        return []
    
    try:
        with open(AUTH_FILE, 'r') as f:
            data = json.load(f)
        return data.get('cookies', [])
    except (json.JSONDecodeError, IOError) as e:
        print(f"{RED}读取 cookie 文件失败: {e}{NC}")
        return []

def build_cookie_string(cookies):
    """构建 cookie 字符串 - 只包含相关域名的 cookie"""
    cookie_parts = []
    relevant_domains = ['console.bce.baidu.com', 'bce.baidu.com', 'baidu.com']
    
    for cookie in cookies:
        name = cookie.get('name', '')
        value = cookie.get('value', '')
        domain = cookie.get('domain', '')
        
        if name and value:
            # 只包含与百度智能云相关的 cookie
            for d in relevant_domains:
                if d in domain:
                    cookie_parts.append(f"{name}={value}")
                    break
    
    return '; '.join(cookie_parts)

def query_quota():
    """查询用量"""
    cookies = load_cookies()
    
    if not cookies:
        return None, "未找到保存的 cookie，请先运行登录脚本"
    
    cookie_str = build_cookie_string(cookies)
    
    if not cookie_str:
        return None, "无法构建有效的 cookie 字符串"
    
    # 使用 curl 查询 API
    cmd = [
        'curl', '-s', '-L',
        API_URL,
        '-H', 'Accept: application/json, text/plain, */*',
        '-H', 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8',
        '-H', 'Referer: https://console.bce.baidu.com/qianfan/resource/subscribe',
        '-H', f'Cookie: {cookie_str}',
        '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        '-H', 'X-Requested-With: XMLHttpRequest',
        '--connect-timeout', '10',
        '--max-time', '30'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        return None, f"请求失败: {result.stderr}"
    
    return result.stdout, None

def format_reset_time(reset_at):
    """格式化重置时间"""
    try:
        # 处理 ISO 格式时间
        dt = datetime.fromisoformat(reset_at.replace('+08:00', ''))
        return dt.strftime('%m月%d日 %H:%M')
    except:
        return reset_at

def parse_quota(data):
    """解析 API 响应"""
    try:
        if not data:
            return None, "空响应"
        
        result = json.loads(data)
        
        if not result.get('success'):
            error_msg = result.get('message', '未知错误')
            return None, f"API 返回错误: {error_msg}"
        
        quota = result.get('result', {}).get('quota', {})
        
        if not quota:
            return None, "响应中未找到 quota 数据"
        
        return quota, None
        
    except json.JSONDecodeError as e:
        return None, f"JSON 解析失败: {e}, 原始数据: {data[:200]}"

def display_quota(quota):
    """显示用量信息"""
    print(f"\n{CYAN}╔══════════════════════════════════════════════════════════╗{NC}")
    print(f"{CYAN}║          📊 百度千帆 · Coding Plan 用量详情              ║{NC}")
    print(f"{CYAN}╚══════════════════════════════════════════════════════════╝{NC}\n")
    
    # 定义周期
    periods = [
        ('⏱️  5小时周期', 'fiveHour'),
        ('📅 本周用量', 'week'),
        ('📆 本月用量', 'month')
    ]
    
    for label, key in periods:
        data = quota.get(key, {})
        used = data.get('used', 0)
        limit = data.get('limit', 0)
        reset_at = data.get('resetAt', '未知')
        
        remaining = limit - used if limit > 0 else 0
        percent = (used / limit * 100) if limit > 0 else 0
        reset_time = format_reset_time(reset_at)
        
        # 根据使用率选择颜色
        if percent < 50:
            color = GREEN
            status = "充足"
        elif percent < 80:
            color = YELLOW
            status = "注意"
        else:
            color = RED
            status = "警告"
        
        print(f"{BLUE}{label}:{NC}")
        print(f"   已用: {used} / {limit} ({color}{percent:.1f}%{NC})")
        print(f"   剩余: {remaining}")
        print(f"   重置: {reset_time}")
        print(f"   状态: {color}{status}{NC}")
        print()
    
    print(f"{CYAN}══════════════════════════════════════════════════════════{NC}")
    
    # 总体建议
    five_hour = quota.get('fiveHour', {})
    five_hour_percent = (five_hour.get('used', 0) / five_hour.get('limit', 1)) * 100
    
    print(f"\n{BLUE}💡 使用建议：{NC}")
    if five_hour_percent > 80:
        print(f"   {RED}• 5小时用量较高 ({five_hour_percent:.1f}%)，建议稍后再用{NC}")
    elif five_hour_percent > 50:
        print(f"   {YELLOW}• 5小时用量中等 ({five_hour_percent:.1f}%)，可继续使用{NC}")
    else:
        print(f"   {GREEN}• 用量正常 ({five_hour_percent:.1f}%)，可以继续使用{NC}")
    
    month = quota.get('month', {})
    month_percent = (month.get('used', 0) / month.get('limit', 1)) * 100
    print(f"   • 月度额度剩余 {(100-month_percent):.1f}%")

def main():
    print(f"{BLUE}🔍 正在查询千帆 Coding Plan 用量...{NC}")
    
    # 检查 cookie 文件
    if not os.path.exists(AUTH_FILE):
        print(f"{RED}❌ 未找到 cookie 文件: {AUTH_FILE}{NC}")
        print(f"{YELLOW}💡 请先运行登录脚本获取 cookie{NC}")
        return 1
    
    # 查询用量
    print(f"{BLUE}📊 正在请求 API...{NC}")
    result, error = query_quota()
    
    if error:
        print(f"{RED}❌ {error}{NC}")
        return 1
    
    # 解析响应
    quota, error = parse_quota(result)
    
    if error:
        print(f"{RED}❌ {error}{NC}")
        
        # 检查是否是登录过期
        if '未登录' in error or 'login' in result.lower():
            print(f"{YELLOW}💡 Cookie 可能已过期，需要重新登录{NC}")
        return 1
    
    # 显示结果
    display_quota(quota)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
