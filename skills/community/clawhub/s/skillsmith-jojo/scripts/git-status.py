#!/usr/bin/env python3
"""
Git 仓库状态可视化脚本
"""

import subprocess
import sys

def run_git(args):
    result = subprocess.run(['git'] + args, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def main():
    _, _, code = run_git(['rev-parse', '--git-dir'])
    if code != 0:
        print("❌ 错误：当前目录不是 git 仓库"); sys.exit(1)

    print("=" * 50)
    print("📦 Git 仓库状态")
    print("=" * 50)

    # 分支信息
    stdout, _, _ = run_git(['branch', '--show-current'])
    print(f"\n🌿 当前分支: {stdout or '(无)'}")

    # 提交状态
    stdout, _, _ = run_git(['rev-parse', '--abbrev-ref', '@{upstream}'])
    if stdout:
        stdout, _, _ = run_git(['rev-list', '--left-right', '--count', 'HEAD...@{upstream}'])
        if stdout:
            ahead, behind = stdout.split('\t')
            if int(ahead) > 0: print(f"   ⬆️  领先远程 {ahead} 个提交")
            if int(behind) > 0: print(f"   ⬇️  落后远程 {behind} 个提交")
            if ahead == '0' and behind == '0': print("   ✅ 与远程同步")
    else:
        print("   ⚠️  没有上游分支")

    # 文件状态
    stdout, _, _ = run_git(['status', '--porcelain'])
    staged = modified = untracked = 0
    if stdout:
        for line in stdout.split('\n'):
            if not line: continue
            if line[1] in 'ADM': staged += 1
            elif line[0] in ' M': modified += 1
            elif line.startswith('??'): untracked += 1

    print(f"\n📁 文件状态:")
    if staged > 0: print(f"   🟢 已暂存: {staged} 个文件")
    if modified > 0: print(f"   🟡 已修改: {modified} 个文件")
    if untracked > 0: print(f"   ⚪ 未跟踪: {untracked} 个文件")
    if staged == 0 and modified == 0 and untracked == 0: print("   ✅ 工作区干净")

    # 最后一次提交
    stdout, _, _ = run_git(['log', '-1', '--format=%h %s'])
    print(f"\n📝 最后一次提交: {stdout or '(无)'}")

    print("\n" + "=" * 50)

if __name__ == '__main__':
    main()
