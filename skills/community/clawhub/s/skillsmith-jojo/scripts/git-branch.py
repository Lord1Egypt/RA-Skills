#!/usr/bin/env python3
"""
Git 分支管理脚本
规范分支命名和操作
"""

import subprocess
import sys
import re

def run_git(args):
    result = subprocess.run(['git'] + args, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def validate_branch_name(branch_type, name):
    clean_name = name.lower().replace(' ', '-')
    clean_name = re.sub(r'[^a-z0-9\-]', '', clean_name)
    valid_types = ['feature', 'fix', 'hotfix', 'docs', 'refactor', 'test']
    if branch_type not in valid_types:
        print(f"❌ 无效的分支类型: {branch_type}"); return None
    return f"{branch_type}/{clean_name}"

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Git 分支管理')
    subparsers = parser.add_subparsers(dest='command')
    
    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('type', choices=['feature', 'fix', 'hotfix'])
    create_parser.add_argument('name')
    
    switch_parser = subparsers.add_parser('switch')
    switch_parser.add_argument('branch')
    
    list_parser = subparsers.add_parser('list')
    
    args = parser.parse_args()

    _, _, code = run_git(['rev-parse', '--git-dir'])
    if code != 0:
        print("❌ 错误：当前目录不是 git 仓库"); sys.exit(1)

    if args.command == 'create':
        branch = validate_branch_name(args.type, args.name)
        if branch:
            _, stderr, code = run_git(['checkout', '-b', branch])
            if code == 0: print(f"✓ 创建并切换到分支: {branch}")
            else: print(f"❌ 创建失败: {stderr}")
    
    elif args.command == 'switch':
        _, stderr, code = run_git(['checkout', args.branch])
        if code == 0: print(f"✓ 切换到分支: {args.branch}")
        else: print(f"❌ 切换失败: {stderr}")
    
    elif args.command == 'list':
        stdout, _, _ = run_git(['branch', '-a'])
        print("\n📋 分支列表:")
        for line in stdout.split('\n'):
            print(f"   {line.strip()}")

if __name__ == '__main__':
    main()
