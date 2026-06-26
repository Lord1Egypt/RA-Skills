#!/usr/bin/env python3
"""
百度千帆 Coding Plan 用量查询工具
自动检测 cookie 状态，失效时自动登录
"""

import json
import subprocess
import sys
import os
import re
import time
from datetime import datetime

AUTH_FILE = os.path.expanduser("~/.baidu-qianfan-auth.json")
API_URL = "https://console.bce.baidu.com/api/qianfan/charge/codingPlan/quota"
LOGIN_URL = "https://console.bce.baidu.com/qianfan/resource/subscribe"

# 颜色定义
CYAN = '\033[0;36m'
BLUE = '\033[0;34m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
NC = '\033[0m'

def run_browser(args):
    """运行 agent-browser 命令"""
    result = subprocess.run(
        ['agent-browser'] + args,
        capture_output=True,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def open_page(url):
    """打开页面"""
    stdout, stderr, code = run_browser(['open', url])
    return code == 0

def get_url():
    """获取当前 URL"""
    stdout, stderr, code = run_browser(['get', 'url'])
    return stdout if code == 0 else None

def get_snapshot():
    """获取页面快照"""
    stdout, stderr, code = run_browser(['snapshot', '-i'])
    return stdout if code == 0 else None

def eval_js(js_code):
    """执行 JavaScript"""
    stdout, stderr, code = run_browser(['eval', js_code])
    return stdout if code == 0 else None

def click_element(ref):
    """点击元素"""
    stdout, stderr, code = run_browser(['click', ref])
    return code == 0

def fill_input(ref, text):
    """填充输入框"""
    stdout, stderr, code = run_browser(['fill', ref, text])
    return code == 0

def close_browser():
    """关闭浏览器"""
    run_browser(['close'])

def save_auth():
    """保存登录状态"""
    stdout, stderr, code = run_browser(['state', 'save', AUTH_FILE])
    return code == 0

def parse_snapshot(snapshot):
    """解析快照，提取元素引用"""
    elements = {}
    for line in snapshot.split('\n'):
        # 匹配类似: textbox "手机号" [ref=e3]
        match = re.search(r'(\w+(?:\s+\w+)*)\s+"([^"]+)"\s+\[ref=(e\d+)\]', line)
        if match:
            elem_type, text, ref = match.groups()
            elements[text] = ref
            elements[f"{elem_type}:{text}"] = ref
        # 匹配按钮: button "登录/注册" [ref=e9]
        match = re.search(r'button\s+"([^"]+)"\s+\[ref=(e\d+)\]', line)
        if match:
            text, ref = match.groups()
            elements[text] = ref
    return elements

def build_cookie_string(cookies):
    """构建 cookie 字符串"""
    parts = []
    for c in cookies:
        if 'baidu.com' in c.get('domain', ''):
            parts.append(f"{c['name']}={c['value']}")
    return '; '.join(parts)

def query_with_curl(cookies):
    """使用 curl 查询 API"""
    cookie_str = build_cookie_string(cookies)
    
    cmd = [
        'curl', '-s', '-L', API_URL,
        '-H', f'Cookie: {cookie_str}',
        '-H', 'Referer: https://console.bce.baidu.com/qianfan/resource/subscribe',
        '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        '--max-time', '10'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None

def check_cookie_valid():
    """检查 cookie 是否有效"""
    if not os.path.exists(AUTH_FILE):
        return False, "未找到 cookie 文件"
    
    try:
        with open(AUTH_FILE, 'r') as f:
            data = json.load(f)
        cookies = data.get('cookies', [])
        
        if not cookies:
            return False, "cookie 文件为空"
        
        # 尝试查询 API
        result = query_with_curl(cookies)
        
        if not result:
            return False, "API 请求失败"
        
        try:
            data = json.loads(result)
            if data.get('success'):
                return True, data['result']['quota']
            else:
                return False, f"API 返回错误: {data.get('message', '未知错误')}"
        except json.JSONDecodeError:
            return False, "响应解析失败，cookie 可能已过期"
            
    except (json.JSONDecodeError, IOError) as e:
        return False, f"读取 cookie 失败: {e}"

def login(phone):
    """登录百度账号"""
    print(f"{BLUE}正在打开登录页面...{NC}")
    
    # 打开订阅页面（会重定向到登录页）
    open_page(LOGIN_URL)
    time.sleep(3)
    
    # 获取登录页面元素
    snapshot = get_snapshot()
    elements = parse_snapshot(snapshot)
    
    # 检查是否已经登录
    url = get_url()
    if url and 'qianfan' in url and 'login' not in url:
        print(f"{GREEN}✓ 已经登录{NC}")
        save_auth()
        return True
    
    # 填写手机号
    if '手机号' in elements:
        fill_input(elements['手机号'], phone)
        print(f"{BLUE}已填写手机号{NC}")
    else:
        print(f"{RED}未找到手机号输入框{NC}")
        return False
    
    # 发送验证码
    if '发送验证码' in elements:
        click_element(elements['发送验证码'])
        print(f"{YELLOW}验证码已发送到 {phone}{NC}")
    else:
        print(f"{RED}未找到发送验证码按钮{NC}")
        return False
    
    # 获取验证码输入
    code = input(f"{YELLOW}请输入验证码: {NC}").strip()
    
    if not code:
        print(f"{RED}验证码不能为空{NC}")
        return False
    
    # 重新获取快照
    snapshot = get_snapshot()
    elements = parse_snapshot(snapshot)
    
    # 填写验证码
    if '短信验证码' in elements:
        fill_input(elements['短信验证码'], code)
    else:
        print(f"{RED}未找到验证码输入框{NC}")
        return False
    
    # 勾选协议
    if '我已阅读并同意' in elements:
        from subprocess import run
        run(['agent-browser', 'check', elements['我已阅读并同意']], capture_output=True)
    
    # 点击登录
    snapshot = get_snapshot()
    elements = parse_snapshot(snapshot)
    
    if '登录/注册' in elements:
        click_element(elements['登录/注册'])
        print(f"{BLUE}正在登录...{NC}")
    else:
        print(f"{RED}未找到登录按钮{NC}")
        return False
    
    # 等待登录完成
    time.sleep(5)
    
    # 检查是否需要二次验证
    url = get_url()
    if url and ('verify' in url or 'login' in url):
        print(f"{YELLOW}需要进行二次验证{NC}")
        snapshot = get_snapshot()
        elements = parse_snapshot(snapshot)
        
        if '发送验证码' in elements:
            click_element(elements['发送验证码'])
            code = input(f"{YELLOW}请输入二次验证码: {NC}").strip()
            
            snapshot = get_snapshot()
            elements = parse_snapshot(snapshot)
            
            if '验证码' in elements:
                fill_input(elements['验证码'], code)
            
            if '确定' in elements:
                click_element(elements['确定'])
            
            time.sleep(3)
    
    # 检查登录结果
    url = get_url()
    if url and 'qianfan' in url and 'login' not in url:
        print(f"{GREEN}✓ 登录成功{NC}")
        save_auth()
        return True
    else:
        print(f"{RED}登录失败{NC}")
        return False

def format_time(t):
    """格式化时间"""
    try:
        dt = datetime.fromisoformat(t.replace('+08:00', ''))
        return dt.strftime('%m月%d日 %H:%M')
    except:
        return t

def display_quota(quota):
    """显示用量"""
    print(f"\n{CYAN}╔══════════════════════════════════════════════════════════╗{NC}")
    print(f"{CYAN}║          📊 百度千帆 · Coding Plan 用量详情              ║{NC}")
    print(f"{CYAN}╚══════════════════════════════════════════════════════════╝{NC}\n")
    
    for label, key in [('⏱️  5小时周期', 'fiveHour'), ('📅 本周用量', 'week'), ('📆 本月用量', 'month')]:
        q = quota.get(key, {})
        used, limit = q.get('used', 0), q.get('limit', 0)
        remaining = limit - used if limit else 0
        pct = used / limit * 100 if limit else 0
        reset = format_time(q.get('resetAt', '未知'))
        
        if pct < 50:
            color = GREEN
        elif pct < 80:
            color = YELLOW
        else:
            color = RED
        
        print(f"{BLUE}{label}:{NC}")
        print(f"   已用: {used} / {limit} ({color}{pct:.1f}%{NC})")
        print(f"   剩余: {remaining}")
        print(f"   重置: {reset}")
        print()
    
    print(f"{CYAN}══════════════════════════════════════════════════════════{NC}")

def main():
    # 检查 cookie 是否有效
    print(f"{BLUE}🔍 检查登录状态...{NC}")
    is_valid, result = check_cookie_valid()
    
    if is_valid:
        print(f"{GREEN}✓ Cookie 有效，直接查询用量{NC}")
        display_quota(result)
        close_browser()
        return 0
    
    # Cookie 无效，需要登录
    print(f"{YELLOW}⚠ {result}{NC}")
    print(f"{YELLOW}需要重新登录{NC}\n")
    
    # 获取手机号
    phone = os.environ.get('QIANFAN_PHONE', '')
    if not phone:
        phone = input(f"{BLUE}请输入手机号: {NC}").strip()
    
    if not phone:
        print(f"{RED}手机号不能为空{NC}")
        return 1
    
    try:
        # 登录
        if login(phone):
            # 重新查询
            is_valid, result = check_cookie_valid()
            if is_valid:
                display_quota(result)
                return 0
            else:
                print(f"{RED}查询失败: {result}{NC}")
                return 1
        else:
            return 1
    finally:
        close_browser()

if __name__ == '__main__':
    sys.exit(main())
