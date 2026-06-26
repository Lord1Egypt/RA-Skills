#!/usr/bin/env python3
"""
memory_sync.py - GitHub 跨设备记忆同步工具

功能:
  - push: 将本地修改推送到 GitHub
  - pull: 从 GitHub 拉取最新记忆
  - status: 查看同步状态
  - auto: 自动同步（pull → 操作 → push）

用法:
  python scripts/memory_sync.py pull [--uid UID]
  python scripts/memory_sync.py push [--uid UID] [--message MSG]
  python scripts/memory_sync.py status
  python scripts/memory_sync.py auto --uid UID

环境变量:
  MEMORY_USER_ID    当前用户ID（可替代 --uid 参数）
  MEMORY_REPO_DIR   记忆仓库目录（默认当前目录）
  GITHUB_TOKEN      GitHub Personal Access Token（可选，用于 HTTPS 认证）
"""

import os
import re
import sys
import shutil
import argparse
import subprocess
from datetime import datetime
from pathlib import Path


# ──────────────────────────────────────────
# Git 基础工具
# ──────────────────────────────────────────

def _find_git() -> str:
    """查找 git 可执行文件路径，兼容 Windows/macOS/Linux。"""
    import shutil
    git_path = shutil.which("git")
    if git_path:
        return git_path
    # Windows 常见安装位置
    windows_candidates = [
        r"C:\Program Files\Git\bin\git.exe",
        r"C:\Program Files (x86)\Git\bin\git.exe",
    ]
    for candidate in windows_candidates:
        if os.path.isfile(candidate):
            return candidate
    raise FileNotFoundError("未找到 git 可执行文件，请先安装: https://git-scm.com")


_GIT_EXE = None  # 懒初始化


def run_git(args, cwd, check=True, capture=True):
    """执行 git 命令，返回 (returncode, stdout, stderr)。
    
    跨平台要点：
    - 使用 shutil.which 查找 git，避免 Windows PATH 缺失
    - 固定 encoding=utf-8，解决 Windows 默认 gbk 乱码
    - errors='replace' 防止无效字节崩溃
    - creationflags=0x08000000 (CREATE_NO_WINDOW) 仅 Windows 有效，防止弹出黑框
    """
    global _GIT_EXE
    if _GIT_EXE is None:
        _GIT_EXE = _find_git()

    env = os.environ.copy()
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        env["GIT_TERMINAL_PROMPT"] = "0"
        # Windows 下设置 GIT_ASKPASS 防止弹出 credential 弹窗
        env["GIT_ASKPASS"] = "echo"

    # Windows 下隐藏控制台窗口
    creation_flags = 0
    if sys.platform == "win32":
        creation_flags = 0x08000000  # CREATE_NO_WINDOW

    result = subprocess.run(
        [_GIT_EXE] + args,
        cwd=str(cwd),      # 确保 Path 对象也能传入
        capture_output=capture,
        text=True,
        encoding="utf-8",
        errors="replace",  # 防止 Windows 上非 UTF-8 字节崩溃
        env=env,
        creationflags=creation_flags,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} 失败:\nfrom typing import List, Dict, Optional, Union, Any, Tuple\n{result.stderr}")
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def is_git_repo(path):
    """检查目录是否是 git 仓库"""
    return os.path.exists(os.path.join(path, ".git"))


def get_current_branch(repo_dir):
    _, out, _ = run_git(["branch", "--show-current"], repo_dir)
    return out.strip()


def has_uncommitted_changes(repo_dir):
    _, out, _ = run_git(["status", "--porcelain"], repo_dir)
    return bool(out.strip())


def get_remote_url(repo_dir):
    rc, out, _ = run_git(["remote", "get-url", "origin"], repo_dir, check=False)
    return out.strip() if rc == 0 else None


# ──────────────────────────────────────────
# 冲突处理
# ──────────────────────────────────────────

def resolve_conflict(filepath, uid):
    """
    处理 git merge 冲突文件：
    - 私人记忆：保留 HEAD（当前设备最新），旧版保存为 .conflict.bak
    - 公共记忆：两版本追加到文件末尾，标记待人工合并
    """
    if not os.path.exists(filepath):
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "<<<<<<< HEAD" not in content:
        return  # 无冲突

    is_shared = "shared/" in filepath.replace("\\", "/")

    if is_shared:
        # 公共记忆：追加冲突内容，标记待处理
        resolved = re.sub(
            r"<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> .+?\n",
            lambda m: (
                m.group(1) + "\n\n"
                f"<!-- [CONFLICT - 需人工合并 - {datetime.now().strftime('%Y-%m-%d %H:%M')}]\n"
                f"冲突版本:\n{m.group(2)}\n-->\n\n"
            ),
            content,
            flags=re.DOTALL,
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(resolved)
        print(f"  ⚠️  公共记忆冲突已标记（需人工合并）: {os.path.basename(filepath)}")
    else:
        # 私人记忆：保留 HEAD 版本，备份旧版
        bak_path = filepath + f".conflict.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
        shutil.copy2(filepath, bak_path)

        resolved = re.sub(
            r"<<<<<<< HEAD\n(.*?)\n=======\n.*?\n>>>>>>> .+?\n",
            r"\1\n",
            content,
            flags=re.DOTALL,
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(resolved)
        print(f"  🔄 私人记忆冲突已解决（保留本地版本），备份: {os.path.basename(bak_path)}")


def find_conflict_files(repo_dir):
    """查找所有有冲突的文件"""
    _, out, _ = run_git(["diff", "--name-only", "--diff-filter=U"], repo_dir, check=False)
    return [os.path.join(repo_dir, f) for f in out.splitlines() if f]


# ──────────────────────────────────────────
# 核心同步操作
# ──────────────────────────────────────────

def do_pull(repo_dir, uid=None, use_merge=False):
    """
    从远程拉取最新记忆。

    策略:
    - use_merge=False (默认): git rebase origin/main（历史线性整洁）
      → 冲突时自动处理（私人保留HEAD，公共标记待合并），然后 --continue
    - use_merge=True: git merge origin/main（保留所有分支历史）
      → 冲突时同样自动处理
    """
    strategy = "merge" if use_merge else "rebase"
    print(f"⬇️  拉取远程记忆（策略: {strategy}）...")

    # git fetch（总是先拉）
    run_git(["fetch", "origin"], repo_dir)

    if use_merge:
        # merge 策略
        rc, out, err = run_git(["merge", "origin/main", "--no-edit"], repo_dir, check=False)
        cmd_desc = "merge"
    else:
        # rebase 策略（默认）
        rc, out, err = run_git(["rebase", "origin/main"], repo_dir, check=False)
        cmd_desc = "rebase"

    if rc != 0:
        err_lower = err.lower()
        if "conflict" in err_lower or "CONFLICT" in err:
            print("  ⚠️  发现冲突，正在自动处理...")
            conflict_files = find_conflict_files(repo_dir)
            for fpath in conflict_files:
                resolve_conflict(fpath, uid)

            # 标记冲突已解决
            run_git(["add", "-A"], repo_dir)

            if use_merge:
                # merge 冲突：完成 merge
                run_git(["commit", "--no-edit"], repo_dir, check=False)
            else:
                # rebase 冲突：继续 rebase
                run_git(["rebase", "--continue"], repo_dir, check=False)

            print(f"  ✅ {cmd_desc} 冲突已处理并解决")
        else:
            print(f"  ❌ {cmd_desc} 失败: {err}")
            if not use_merge:
                print("  💡 提示: 可尝试 --merge 策略（保留分支历史）")
            run_git(["rebase", "--abort"], repo_dir, check=False)
            return False

    # 汇报新内容
    _, log, _ = run_git(
        ["log", "HEAD@{1}..HEAD", "--oneline", "--no-walk=unsorted"],
        repo_dir, check=False
    )
    if log:
        print(f"  📥 拉取到新提交:\n    " + "\n    ".join(log.splitlines()))
    else:
        print("  ✅ 已是最新，无新内容")

    return True


def do_push(repo_dir, uid=None, message=None, scope=None):
    """将本地记忆推送到远程"""
    if not has_uncommitted_changes(repo_dir):
        print("  ℹ️  无本地改动，跳过推送")
        return True

    # 生成 commit 消息
    if not message:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        if scope == "shared":
            message = f"memory(shared): 更新公共记忆 {now}"
        elif uid:
            message = f"memory({uid}): 同步记忆 {now}"
        else:
            message = f"memory: 同步 {now}"

    # git add
    run_git(["add", "-A"], repo_dir)

    # git commit
    run_git(["commit", "-m", message], repo_dir)
    print(f"  📝 已提交: {message}")

    # git push
    rc, _, err = run_git(["push", "origin", "main"], repo_dir, check=False)
    if rc != 0:
        if "rejected" in err or "failed to push" in err:
            print("  ⚠️  推送被拒绝（远程有新内容），尝试先 pull...")
            do_pull(repo_dir, uid)
            run_git(["push", "origin", "main"], repo_dir)
            print("  ✅ 推送成功")
        else:
            print(f"  ❌ 推送失败: {err}")
            return False
    else:
        print("  ✅ 推送成功")

    return True


def do_status(repo_dir):
    """显示同步状态"""
    print(f"\n📊 记忆同步状态")
    print(f"📁 仓库: {repo_dir}")

    remote = get_remote_url(repo_dir)
    branch = get_current_branch(repo_dir)
    # 脱敏 remote URL（不暴露 token）
    safe_remote = remote
    if remote:
        import re as _re
        safe_remote = _re.sub(r"(https://)[^@]+(@)", r"\1***\2", remote)
        if "@" not in remote:
            safe_remote = remote
    print(f"🔗 远程: {safe_remote or '未配置'}")
    print(f"🌿 分支: {branch}")

    # 本地改动
    _, status_out, _ = run_git(["status", "--short"], repo_dir, check=False)
    if status_out:
        print(f"\n📝 未提交的改动:")
        for line in status_out.splitlines():
            print(f"   {line}")
    else:
        print("\n  ✅ 工作区干净，无未提交改动")

    # 与远程对比
    run_git(["fetch", "origin"], repo_dir, check=False)
    _, ahead, _ = run_git(
        ["rev-list", "--count", "HEAD..origin/main"], repo_dir, check=False
    )
    _, behind, _ = run_git(
        ["rev-list", "--count", "origin/main..HEAD"], repo_dir, check=False
    )

    ahead = ahead.strip() or "0"
    behind = behind.strip() or "0"

    if ahead != "0":
        print(f"\n  ⬇️  远程有 {ahead} 个新提交未拉取")
    if behind != "0":
        print(f"\n  ⬆️  本地有 {behind} 个提交未推送")
    if ahead == "0" and behind == "0":
        print("  🔄 与远程保持同步")

    # 最近提交
    _, log, _ = run_git(
        ["log", "--oneline", "-5"], repo_dir, check=False
    )
    if log:
        print(f"\n📜 最近提交:")
        for line in log.splitlines():
            print(f"   {line}")


def do_auto_sync(repo_dir, uid, message=None, use_merge=False):
    """自动同步：pull → （外部写入操作） → push"""
    print(f"\n🔄 自动同步模式（用户: {uid}，策略: {'merge' if use_merge else 'rebase'}）")

    # 1. Pull
    success = do_pull(repo_dir, uid, use_merge=use_merge)
    if not success:
        print("❌ Pull 失败，终止同步")
        return False

    # 2. 检查是否有未提交内容
    if has_uncommitted_changes(repo_dir):
        do_push(repo_dir, uid, message)
    else:
        print("  ℹ️  无需推送")

    return True


# ──────────────────────────────────────────
# 仓库初始化（克隆）
# ──────────────────────────────────────────

def clone_or_init(repo_url, target_dir, token=None):
    """克隆或初始化 GitHub 仓库"""
    if os.path.exists(target_dir) and is_git_repo(target_dir):
        print(f"✅ 仓库已存在: {target_dir}")
        return target_dir

    if repo_url:
        # 注入 token 到 URL（HTTPS clone 时不可避免）
        if token and "github.com" in repo_url and "https://" in repo_url:
            repo_url = repo_url.replace("https://", f"https://{token}@")
            # 打印时脱敏
            print(f"⬇️  克隆仓库: {repo_url.replace(token, '***')}")
        else:
            print(f"⬇️  克隆仓库: {repo_url}")
        os.makedirs(os.path.dirname(target_dir) or ".", exist_ok=True)
        subprocess.run(["git", "clone", repo_url, target_dir], check=True)
        print(f"✅ 克隆完成: {target_dir}")
    else:
        # 本地初始化
        os.makedirs(target_dir, exist_ok=True)
        subprocess.run(["git", "init"], cwd=target_dir, check=True)
        print(f"✅ 本地仓库初始化: {target_dir}")

    return target_dir


# ──────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="GitHub 跨设备记忆同步工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "action",
        choices=["pull", "push", "status", "auto"],
        help="操作类型",
    )
    parser.add_argument("--uid", help="用户ID（覆盖环境变量 MEMORY_USER_ID）")
    parser.add_argument("--repo-dir", default=".", help="记忆仓库本地目录")
    parser.add_argument("--message", "-m", help="自定义 commit 消息")
    parser.add_argument("--scope", choices=["private", "shared", "all"], default="all", help="同步范围")
    parser.add_argument("--merge", action="store_true",
                        help="使用 merge 策略代替 rebase（适合多人频繁协作）")
    args = parser.parse_args()

    uid = args.uid or os.environ.get("MEMORY_USER_ID", "")
    repo_dir = os.path.abspath(
        args.repo_dir or os.environ.get("MEMORY_REPO_DIR", ".")
    )

    if not is_git_repo(repo_dir):
        print(f"❌ 不是 git 仓库: {repo_dir}")
        print("   请先运行: python scripts/memory_init.py --repo-url ...")
        sys.exit(1)

    if args.action == "pull":
        do_pull(repo_dir, uid, use_merge=args.merge)

    elif args.action == "push":
        do_push(repo_dir, uid, args.message, args.scope)

    elif args.action == "status":
        do_status(repo_dir)

    elif args.action == "auto":
        if not uid:
            print("❌ 自动同步需要指定用户ID（--uid 或 MEMORY_USER_ID 环境变量）")
            sys.exit(1)
        do_auto_sync(repo_dir, uid, args.message, use_merge=args.merge)


if __name__ == "__main__":
    main()
