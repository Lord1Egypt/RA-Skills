#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gitee (码云) 发布脚本
国内用户可直接访问
"""
import os
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    import requests
except ImportError:
    print("请安装 requests: pip install requests")
    sys.exit(1)

GITEE_API = "https://gitee.com/api/v5"
REPO_NAME = "sen-dev-patterns"
DESCRIPTION = "个人开发提效Skill - UI规范、算法库、踩坑记录、Web开发规范"

def main():
    print("=" * 50)
    print("  Gitee (码云) 发布脚本")
    print("=" * 50)

    token = os.getenv('GITEE_TOKEN')
    if not token:
        print("\n[!] 未找到Gitee Token")
        print("\n请按以下步骤操作:")
        print("1. 访问 https://gitee.com/oauth/applications")
        print("2. 点击 '创建应用'")
        print("3. 填写应用信息，勾选 'projects' 权限")
        print("4. 获取 Access Token")
        print("5. 设置环境变量: set GITEE_TOKEN=your_token")
        print("6. 重新运行此脚本")
        print("\n或者手动创建仓库:")
        print("1. 访问 https://gitee.com/new")
        print("2. 创建名为 'sen-dev-patterns' 的仓库")
        print("3. 运行命令推送:")
        print("   git remote add gitee https://gitee.com/the13ai/sen-dev-patterns.git")
        print("   git push -u gitee master")
        return

    # 检查仓库是否存在
    resp = requests.get(f'{GITEE_API}/repos/the13ai/{REPO_NAME}', params={'access_token': token})
    if resp.status_code == 200:
        print(f"[*] Gitee仓库已存在: {REPO_NAME}")
    else:
        # 创建仓库
        data = {
            'access_token': token,
            'name': REPO_NAME,
            'description': DESCRIPTION,
            'private': False,
            'auto_init': False,
            'has_issues': True,
            'has_wiki': True
        }
        resp = requests.post(f'{GITEE_API}/user/repos', data=data)
        if resp.status_code == 201:
            print(f"[+] Gitee仓库创建成功: {REPO_NAME}")
        else:
            print(f"[!] Gitee创建失败: {resp.status_code}")
            print(f"    {resp.text[:200]}")

    # 推送
    import subprocess
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_dir)

    remote_url = f'https://the13ai:{token}@gitee.com/the13ai/{REPO_NAME}.git'

    result = subprocess.run(['git', 'remote', 'get-url', 'gitee'], capture_output=True, text=True)
    if result.returncode == 0:
        subprocess.run(['git', 'remote', 'set-url', 'gitee', remote_url], check=True)
    else:
        subprocess.run(['git', 'remote', 'add', 'gitee', remote_url], check=True)

    result = subprocess.run(['git', 'push', '-u', 'gitee', 'master'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"\n[+] Gitee发布成功!")
        print(f"    URL: https://gitee.com/the13ai/{REPO_NAME}")
    else:
        print(f"\n[!] Gitee推送失败")
        print(result.stderr)

if __name__ == "__main__":
    main()
