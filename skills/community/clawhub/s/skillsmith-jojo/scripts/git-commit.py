#!/usr/bin/env python3
"""
Git 智能提交脚本
自动生成规范的 commit message
"""

import subprocess
import sys
import re
from pathlib import Path

def run_git(args):
    result = subprocess.run(['git'] + args, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def get_changed_files():
    stdout, _, _ = run_git(['diff', '--cached', '--name-only'])
    if not stdout:
        stdout, _, _ = run_git(['diff', '--name-only'])
    return stdout.split('\n') if stdout else []

def analyze_change_type(files):
    types = {'feat': [], 'fix': [], 'docs': [], 'style': [], 'chore': []}
    for f in files:
        if not f: continue
        if 'test' in f.lower(): types['test'].append(f)
        elif f.endswith('.md'): types['docs'].append(f)
        elif 'fix' in f.lower(): types['fix'].append(f)
        elif f.endswith(('.py', '.js', '.ts')): types['feat'].append(f)
        else: types['chore'].append(f)
    for t, files in types.items():
        if files: return t, files
    return 'chore', files

def generate_commit_message(change_type, files, custom_msg=None):
    if custom_msg: return f"{change_type}: {custom_msg}"
    type_desc = {'feat': 'add', 'fix': 'fix', 'docs': 'update docs', 'chore': 'update'}
    file_names = [Path(f).name for f in files[:3] if f]
    file_desc = ', '.join(file_names) if file_names else 'update'
    return f"{change_type}: {type_desc.get(change_type, 'update')} {file_desc}"

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Git 智能提交')
    parser.add_argument('--all', '-a', action='store_true', help='自动 add 所有文件')
    parser.add_argument('--message', '-m', help='自定义 commit message')
    args = parser.parse_args()

    _, _, code = run_git(['rev-parse', '--git-dir'])
    if code != 0:
        print("❌ 错误：当前目录不是 git 仓库"); sys.exit(1)

    if args.all:
        run_git(['add', '-A'])
        print("✓ 已添加所有文件")

    files = get_changed_files()
    if not files or files == ['']:
        print("⚠️ 没有待提交的改动"); sys.exit(0)

    change_type, _ = analyze_change_type(files)
    message = generate_commit_message(change_type, files, args.message)

    print(f"📝 生成的 commit message: {message}")
    stdout, stderr, code = run_git(['commit', '-m', message])

    if code == 0:
        print("✓ 提交成功")
        stdout, _, _ = run_git(['log', '-1', '--oneline'])
        print(f"   {stdout}")
    else:
        print(f"❌ 提交失败: {stderr}"); sys.exit(1)

if __name__ == '__main__':
    main()
