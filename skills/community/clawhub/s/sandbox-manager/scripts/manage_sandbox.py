#!/usr/bin/env python3.9
"""
沙箱连接和管理工具
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def connect_sandbox(sandbox_id):
    """连接已有沙箱"""
    from e2b_code_interpreter import Sandbox

    print(f"🔌 正在连接沙箱: {sandbox_id}")

    sbx = Sandbox(sandbox_id=sandbox_id)

    info = sbx.get_info()
    print(f"\n✅ 连接成功!")
    print(f"  沙箱ID: {sbx.sandbox_id}")
    print(f"  模板: {info.template_id}")
    print(f"  过期时间: {info.end_at}")

    return sbx

def get_sandbox_info(sandbox_id):
    """获取沙箱信息"""
    from e2b_code_interpreter import Sandbox

    sbx = Sandbox(sandbox_id=sandbox_id)
    return sbx.get_info()

def list_sandbox_files(sandbox_id, path="."):
    """列出沙箱文件"""
    from e2b_code_interpreter import Sandbox

    sbx = Sandbox(sandbox_id=sandbox_id)
    files = sbx.files.list(path=path, depth=2)

    print(f"\n📁 沙箱文件列表 ({sandbox_id}):")
    print("="*60)
    for f in files:
        print(f"  {f.path}")

    return files

def exec_in_sandbox(sandbox_id, command):
    """在沙箱中执行命令"""
    from e2b_code_interpreter import Sandbox

    sbx = Sandbox(sandbox_id=sandbox_id)

    print(f"\n⚙️  执行命令: {command}")
    print("="*60)

    result = sbx.commands.run(command)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"[stderr] {result.stderr}", file=sys.stderr)

    print(f"\n退出码: {result.exit_code}")

    return result

def kill_sandbox(sandbox_id):
    """销毁沙箱"""
    from e2b_code_interpreter import Sandbox

    print(f"🗑️  正在销毁沙箱: {sandbox_id}")

    sbx = Sandbox(sandbox_id=sandbox_id)
    sbx.kill()

    print("✅ 沙箱已销毁")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='沙箱管理工具')
    parser.add_argument('action', choices=['connect', 'info', 'files', 'exec', 'kill'])
    parser.add_argument('--sandbox-id', '-s', required=True, help='沙箱ID')
    parser.add_argument('--path', '-p', default='.', help='文件路径(用于 files 命令)')
    parser.add_argument('--command', '-c', help='要执行的命令(用于 exec 命令)')

    args = parser.parse_args()

    load_dotenv(os.path.expanduser('~/.env'))

    if args.action == 'connect':
        sbx = connect_sandbox(args.sandbox_id)
    elif args.action == 'info':
        info = get_sandbox_info(args.sandbox_id)
        print(info)
    elif args.action == 'files':
        list_sandbox_files(args.sandbox_id, args.path)
    elif args.action == 'exec':
        if not args.command:
            print("❌ exec 命令需要 --command 参数")
            sys.exit(1)
        exec_in_sandbox(args.sandbox_id, args.command)
    elif args.action == 'kill':
        kill_sandbox(args.sandbox_id)