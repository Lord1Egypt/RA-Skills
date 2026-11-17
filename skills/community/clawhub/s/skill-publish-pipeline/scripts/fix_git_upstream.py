#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复 git 无法创建 refs/remotes/<remote>/ 嵌套目录的问题。

背景（本机实测，git 2.55.0.windows.5）：
  新建仓库后 push 成功、`git ls-remote` 能看到远程分支，但
  `git branch -vv` 显示 `[origin/main: gone]`；`git fetch` 和 `git update-ref`
  都报告成功却完全不落盘，`refs/remotes/` 始终是空目录
  （无 packed-refs、非 reftable、目录权限正常、全新 clone 无此问题）。
  根因是 git 创建嵌套 ref 目录那一步静默失败。

本脚本绕开 git，直接手写 loose ref 文件，然后建立 upstream 追踪。

用法（请在 PowerShell 通道运行——github.com 在 Bash 沙箱内不可达）：
    python fix_git_upstream.py <repo_path> [remote] [branch]

    repo_path   仓库本地路径（含 .git）
    remote      远程名，默认 origin
    branch      分支名，默认 main

退出码：0 成功 / 1 失败

注：所有输出刻意使用 ASCII，避免 PowerShell 5.1 控制台代码页导致的乱码。
"""
import os
import subprocess
import sys


def git(args, cwd):
    """统一入口：内部固定加 'git'，避免调用处漏写。"""
    p = subprocess.run(["git"] + args, capture_output=True, cwd=cwd)
    return (
        p.returncode,
        p.stdout.decode("utf-8", "replace").strip(),
        p.stderr.decode("utf-8", "replace").strip(),
    )


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    repo = os.path.abspath(sys.argv[1])
    remote = sys.argv[2] if len(sys.argv) > 2 else "origin"
    branch = sys.argv[3] if len(sys.argv) > 3 else "main"

    if not os.path.isdir(os.path.join(repo, ".git")):
        print("ERROR: not a git repository (no .git): %s" % repo)
        return 1

    print("repo   : %s" % repo)
    print("remote : %s" % remote)
    print("branch : %s" % branch)
    print()

    # 1) Read remote SHA (also verifies connectivity)
    rc, out, err = git(["ls-remote", remote, "refs/heads/" + branch], repo)
    if rc != 0 or not out:
        print("ERROR: cannot read refs/heads/%s from remote" % branch)
        print("       rc=%s err=%s" % (rc, err[:200]))
        print("       HINT: github.com is unreachable inside the Bash sandbox.")
        print("             Run this under PowerShell (system proxy applies there).")
        return 1
    sha = out.split()[0]
    print("remote SHA: %s" % sha)

    # 2) Hand-write the loose ref (bypasses git's failing mkdir)
    ref_dir = os.path.join(repo, ".git", "refs", "remotes", remote)
    os.makedirs(ref_dir, exist_ok=True)
    ref_file = os.path.join(ref_dir, branch)
    with open(ref_file, "w", encoding="ascii") as f:
        f.write(sha + "\n")
    print("wrote     : %s" % ref_file)

    # 3) Set upstream tracking
    rc, out, err = git(["branch", "--set-upstream-to=%s/%s" % (remote, branch), branch], repo)
    print("set-upstream: rc=%s %s%s" % (rc, out, err[:160]))

    # 4) Verify
    print()
    print("=== verify ===")
    checks = (
        ["for-each-ref", "--format=%(refname) %(objectname:short)", "refs/remotes/"],
        ["status", "-sb"],
        ["branch", "-vv"],
    )
    bad = 0
    for args in checks:
        rc, out, err = git(args, repo)
        print("$ git %s" % " ".join(args))
        print("  " + (out.replace("\n", "\n  ") if out else err[:160]))
        if rc != 0:
            bad += 1

    rc, out, _ = git(["status", "-sb"], repo)
    if "gone" in out or bad:
        print()
        print("WARN: still shows [gone], or a command failed. Fix incomplete.")
        return 1

    print()
    print("OK. 'git push' works now.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
