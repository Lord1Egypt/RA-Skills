#!/usr/bin/env python3
#
# zentao-autoreport - 获取所有任务并匹配用户描述
# Usage: python match-tasks.py "<user_description>"
#

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

CONFIG_PATH = Path.home() / ".config" / "zentao" / ".env"

def load_config():
    """加载配置文件"""
    if not CONFIG_PATH.exists():
        print(f"ERROR: Config {CONFIG_PATH} not found")
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

def get_all_tasks(zentao_url, zentaosid):
    """获取当前用户所有任务"""
    import http.cookiejar
    import urllib.request

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

    url = f"{zentao_url}index.php?m=my&f=task&t=json&onlybody=yes"

    with opener.open(url) as response:
        data = json.loads(response.read().decode())

    return data.get('data', {}).get('tasks', [])

def match_tasks(user_desc, tasks):
    """智能匹配用户描述到任务"""
    desc_lower = user_desc.lower()

    matches = []
    for task in tasks:
        task_name = task.get('name', '').lower()
        task_id = task.get('id')

        # 简单的关键词匹配
        score = 0
        desc_words = re.split(r'[\s,，.。]+', desc_lower)
        for word in desc_words:
            if len(word) > 1 and word in task_name:
                score += 1

        if score > 0:
            matches.append((task, score))

    # 按匹配度排序
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches

def format_tasks_table(tasks):
    """格式化任务列表为表格"""
    lines = []
    lines.append(f'# Found {len(tasks)} tasks:')
    lines.append('')
    lines.append('| Task ID | Task Name | Consumed | Left |')
    lines.append('|---------|-----------|----------|------|')

    for t in tasks:
        tid = t.get('id')
        name = t.get('name', '').replace('|', '\\|')
        consumed = t.get('consumed', '0')
        left = t.get('left', '0')
        lines.append(f'| {tid} | {name} | {consumed}h | {left}h |')

    lines.append('')
    lines.append('## Full task list JSON:')
    lines.append('```')
    for t in tasks:
        lines.append(f'- {t.get("id")}: {t.get("name")}')
    lines.append('```')

    return '\n'.join(lines)

def main():
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} "<user_description>"')
        sys.exit(1)

    user_desc = sys.argv[1]

    # 加载配置
    config = load_config()
    zentao_url = config.get('ZENTAO_URL', '')
    zentao_account = config.get('ZENTAO_ACCOUNT', '')
    zentao_password = config.get('ZENTAO_PASSWORD', '')

    if not zentao_url:
        print("ERROR: ZENTAO_URL not found in config")
        sys.exit(1)

    # 确保 URL 以 / 结尾
    if not zentao_url.endswith('/'):
        zentao_url += '/'

    # 优先从配置获取 ZENTAO_SID，如果没有则尝试从 cookies 文件读取
    zentaosid = config.get('ZENTAO_SID', '')

    if not zentaosid:
        cookie_file = Path('/tmp/cookies.txt')
        if cookie_file.exists():
            with open(cookie_file) as f:
                for line in f:
                    if 'zentaosid' in line:
                        parts = line.strip().split()
                        if len(parts) >= 7:
                            zentaosid = parts[6]

    # 如果还是没有 zentaosid，尝试重新登录获取
    if not zentaosid:
        if zentao_account and zentao_password:
            print(">>> No zentaosid found, re-login...")
            zentaosid = relogin(zentao_url, zentao_account, zentao_password)
            print(f">>> Got fresh zentaosid: {zentaosid}")
        else:
            print("ERROR: zentaosid not found and no account/password for re-login.")
            sys.exit(1)

    # 获取所有任务
    print(">>> Fetching all tasks...")
    tasks = get_all_tasks(zentao_url, zentaosid)

    # 打印任务列表
    print(format_tasks_table(tasks))

    # 匹配任务
    if len(sys.argv) > 2 and sys.argv[2] == '--match':
        print("\n>>> Matching tasks...")
        matches = match_tasks(user_desc, tasks)
        if matches:
            print(f"\n# Matched {len(matches)} tasks:")
            for task, score in matches:
                print(f"- Task {task.get('id')}: {task.get('name')} (score: {score})")
        else:
            print("\n# No matching tasks found")

if __name__ == '__main__':
    main()
