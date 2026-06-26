#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub & Gitee 自动发布脚本
"""
import os
import sys
import json
import subprocess
import io

# Fix encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    import requests
except ImportError:
    print("请安装 requests: pip install requests")
    sys.exit(1)

GITHUB_API = "https://api.github.com"
GITEE_API = "https://gitee.com/api/v5"
REPO_NAME = "sen-dev-patterns"
DESCRIPTION = "Personal development patterns: UI styles, code modules, algorithms, pitfalls - CodeBuddy Skill"

def find_github_token():
    """查找GitHub token"""
    # 1. 环境变量
    for var in ['GITHUB_TOKEN', 'GH_TOKEN', 'GITHUB_PERSONAL_ACCESS_TOKEN']:
        token = os.getenv(var)
        if token:
            print(f"[+] Found token in env: {var[:10]}...")
            return token

    # 2. VSCode扩展
    paths = [
        os.path.expandvars(r"%APPDATA%\Code\User\globalStorage\github-auth-token"),
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    token = data.get('token') or data.get('github_token')
                    if token:
                        print(f"[+] Found token in VSCode state")
                        return token
            except Exception as e:
                print(f"[!] Error reading {path}: {e}")

    # 3. Git credential
    try:
        result = subprocess.run(
            ['git', 'credential', 'fill'],
            input='protocol=https\nhost=github.com\n\n',
            capture_output=True, text=True, encoding='utf-8',
            timeout=5
        )
        for line in result.stdout.split('\n'):
            if line.startswith('password='):
                return line[9:]
    except:
        pass

    return None

def get_github_user(token):
    """获取GitHub用户信息"""
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
    resp = requests.get(f'{GITHUB_API}/user', headers=headers)
    if resp.status_code == 200:
        return resp.json()
    return None

def create_github_repo(token, repo_name, description):
    """创建GitHub仓库"""
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
    data = {'name': repo_name, 'description': description, 'private': False, 'auto_init': False}

    # 检查是否存在
    resp = requests.get(f'{GITHUB_API}/repos/sinadook/{repo_name}', headers=headers)
    if resp.status_code == 200:
        print(f"[*] GitHub repo already exists: {repo_name}")
        return True

    # 创建
    resp = requests.post(f'{GITHUB_API}/user/repos', headers=headers, json=data)
    if resp.status_code == 201:
        print(f"[+] GitHub repo created: {repo_name}")
        return True

    try:
        error = resp.json()
        if 'already exists' in str(error).lower():
            print(f"[*] GitHub repo already exists: {repo_name}")
            return True
    except:
        pass

    print(f"[!] GitHub API error: {resp.status_code} - {resp.text[:200]}")
    return False

def push_to_github():
    """推送到GitHub"""
    print("\n=== Publishing to GitHub ===")

    token = find_github_token()
    if not token:
        print("[!] No GitHub token found")
        print("\n请在浏览器中创建Personal Access Token:")
        print("  1. 访问 https://github.com/settings/tokens")
        print("  2. 点击 'Generate new token (classic)'")
        print("  3. 勾选 'repo' 权限")
        print("  4. 复制token并设置环境变量:")
        print("     Windows: set GITHUB_TOKEN=your_token_here")
        print("     然后重新运行此脚本")
        return False

    user = get_github_user(token)
    if not user:
        print("[!] Invalid token - cannot authenticate")
        return False

    username = user.get('login')
    print(f"[+] Authenticated as: {username}")

    if not create_github_repo(token, REPO_NAME, DESCRIPTION):
        return False

    # 推送
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_dir)

    # 设置远程
    remote_url = f'https://{username}:{token}@github.com/{username}/{REPO_NAME}.git'

    # 添加远程（更新如果存在）
    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
    if result.returncode == 0:
        subprocess.run(['git', 'remote', 'set-url', 'origin', remote_url], check=True)
        print(f"[*] Updated origin URL")
    else:
        subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
        print(f"[*] Added origin URL")

    # 推送
    result = subprocess.run(['git', 'push', '-u', 'origin', 'master'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode == 0:
        print(f"\n[+] GitHub publish SUCCESS!")
        print(f"    URL: https://github.com/{username}/{REPO_NAME}")
        return True
    else:
        print(f"\n[!] GitHub push failed")
        return False

def create_gitee_repo(repo_name, description):
    """创建Gitee仓库"""
    token = os.getenv('GITEE_TOKEN')
    if not token:
        print("[!] No Gitee token (set GITEE_TOKEN env)")
        return False

    data = {
        'access_token': token,
        'name': repo_name,
        'description': description,
        'private': False,
        'auto_init': False
    }

    resp = requests.post(f'{GITEE_API}/user/repos', data=data)
    if resp.status_code == 201 or 'already exists' in resp.text.lower():
        print(f"[+] Gitee repo ready: gitee.com/sinadook/{repo_name}")
        return True

    print(f"[!] Gitee error: {resp.status_code} - {resp.text[:200]}")
    return False

def main():
    print("=" * 50)
    print("  Sen-Dev-Patterns Skill Publisher")
    print("=" * 50)

    success = push_to_github()

    print("\n" + "=" * 50)
    if success:
        print("SUCCESS! Skill published to GitHub.")
        print("Now you can submit to ClawHub using the GitHub URL.")
    else:
        print("GitHub publish failed. Please provide a GitHub token.")
        print("\nQuick setup:")
        print("1. Visit: https://github.com/settings/tokens")
        print("2. Create token with 'repo' scope")
        print("3. Run: set GITHUB_TOKEN=your_token")
        print("4. Re-run this script")
    print("=" * 50)

if __name__ == "__main__":
    main()
