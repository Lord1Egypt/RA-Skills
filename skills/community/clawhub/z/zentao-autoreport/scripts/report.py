#!/usr/bin/env python3
#
# zentao-autoreport - 自动记录一条工时
# Usage: python report.py <task_id> <consumed> "<work_desc>" [date]
#

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "zentao" / ".env"

def load_config():
    """加载配置文件"""
    if not CONFIG_PATH.exists():
        print(f"ERROR: Config file {CONFIG_PATH} not found")
        sys.exit(1)

    config = {}
    with open(CONFIG_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config

def relogin(zentao_url, account, password):
    """重新登录获取最新的 zentaosid"""
    import http.cookiejar
    import urllib.request

    cookie_jar = http.cookiejar.LWPCookieJar()

    # 获取登录页面
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    opener.open(f"{zentao_url}user-login.html")

    # 执行登录
    login_data = f"account={account}&password={password}&remember=on".encode()
    req = urllib.request.Request(
        f"{zentao_url}index.php?m=user&f=login&t=json",
        data=login_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    opener.open(req)

    # 提取 zentaosid
    zentaosid = None
    for cookie in cookie_jar:
        if cookie.name == 'zentaosid':
            zentaosid = cookie.value

    if not zentaosid:
        print("ERROR: Failed to get zentaosid")
        sys.exit(1)

    return zentaosid

def get_task_info(task_id, zentao_url, token):
    """获取任务信息"""
    import urllib.request

    req = urllib.request.Request(f"{zentao_url}api.php/v1/tasks/{task_id}")
    req.add_header('Token', token)

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
    return data

def format_number(value):
    """格式化数字，去掉多余的 0"""
    formatted = f"{value:.1f}"
    if formatted.endswith('.0'):
        return formatted[:-2]
    return formatted

def record_workhour(task_id, consumed, left, work_desc, date, zentao_url, zentaosid):
    """调用 recordworkhour 接口记录工时"""
    import http.cookiejar
    import urllib.request
    import urllib.parse

    # 设置 cookie
    cookie_jar = http.cookiejar.CookieJar()
    cookie = http.cookiejar.Cookie(
        version=0, name='zentaosid', value=zentaosid,
        port=None, port_specified=False,
        domain=zentao_url.split('/')[2], domain_specified=True, domain_initial_dot=False,
        path='/', path_specified=True,
        secure=False, expires=None, discard=True,
        comment=None, comment_url=None, rest={}
    )
    cookie_jar.set_cookie(cookie)

    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    opener.addheaders = [
        ('X-Requested-With', 'XMLHttpRequest'),
    ]

    # 构建 multipart 表单
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="date[0]"\r\n\r\n{date}\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="consumed[0]"\r\n\r\n{consumed}\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="left[0]"\r\n\r\n{left}\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="work[0]"\r\n\r\n{work_desc}\r\n'
        f'--{boundary}--\r\n'
    ).encode()

    url = f"{zentao_url}index.php?m=task&f=recordworkhour&taskID={task_id}"
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

    response = opener.open(req)
    return response.read().decode()

def main():
    if len(sys.argv) < 4:
        print(f'Usage: {sys.argv[0]} <task_id> <consumed> "<work_desc>" [date]')
        sys.exit(1)

    task_id = sys.argv[1]
    consumed = float(sys.argv[2])
    work_desc = sys.argv[3]
    date = sys.argv[4] if len(sys.argv) > 4 else datetime.now().strftime('%Y-%m-%d')

    # 加载配置
    config = load_config()
    zentao_url = config.get('ZENTAO_URL', '')
    zentao_account = config.get('ZENTAO_ACCOUNT', '')
    zentao_password = config.get('ZENTAO_PASSWORD', '')
    zentao_token = config.get('ZENTAO_TOKEN', '')

    if not zentao_url:
        print("ERROR: ZENTAO_URL not found in config")
        sys.exit(1)

    # 确保 URL 以 / 结尾
    if not zentao_url.endswith('/'):
        zentao_url += '/'

    # 重新登录获取最新 zentaosid
    print(">>> Re-login to get fresh zentaosid...")
    zentaosid = relogin(zentao_url, zentao_account, zentao_password)
    print(f">>> Got fresh zentaosid: {zentaosid}")

    # 获取任务信息
    print(f">>> Getting task info for {task_id}...")
    task_info = get_task_info(task_id, zentao_url, zentao_token)

    current_left = float(task_info.get('left', 0))
    current_consumed = float(task_info.get('consumed', 0))

    new_left = current_left - consumed
    new_consumed = current_consumed + consumed

    print(f">>> Current: consumed={format_number(current_consumed)}, left={format_number(current_left)}")
    print(f">>> New: consumed={format_number(new_consumed)}, left={format_number(new_left)}")

    # 记录工时
    print(f">>> Recording... date={date}, consumed={consumed}, left={format_number(new_left)}")

    response = record_workhour(
        task_id, consumed, format_number(new_left), work_desc, date,
        zentao_url, zentaosid
    )

    print(f">>> Response: {response}")

    # 检查结果
    try:
        result = json.loads(response)
        if result.get('result') == 'success':
            print(f"✅ SUCCESS: Recorded successfully!")
            print(f"RESULT: task={task_id}, consumed={consumed}, date={date}, work=\"{work_desc}\"")
            print(f"UPDATED: consumed={format_number(new_consumed)}, left={format_number(new_left)}")
            sys.exit(0)
        else:
            print(f"❌ FAILED: {response}")
            sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ FAILED: Invalid JSON response: {response}")
        sys.exit(1)

if __name__ == '__main__':
    main()
