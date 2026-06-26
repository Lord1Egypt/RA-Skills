#!/usr/bin/env python3
"""
启动问题排查流程 - 上下文隔离模式
- 自动保存当前上下文作为"主线"
- 创建隔离环境（worktree/subagent）
- 在隔离环境中解决问题
"""
import os
import sys
import json
import datetime
import subprocess
import hashlib

TROUBLE_DIR = ".trouble-shooting"
ACTIVE_FILE = f"{TROUBLE_DIR}/active.json"

def ensure_dir():
    os.makedirs(f"{TROUBLE_DIR}/archive", exist_ok=True)

def save_snapshot(issue_id, title, mode):
    """保存当前主线上下文快照"""
    snapshot = {
        "id": issue_id,
        "title": title,
        "mode": mode,  # 'worktree' or 'subagent'
        "timestamp": datetime.datetime.now().isoformat(),
        "branch": get_current_branch(),
        "cwd": os.getcwd()
    }
    ensure_dir()
    with open(ACTIVE_FILE, 'w') as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    return snapshot

def get_current_branch():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except:
        return "unknown"

def generate_issue_id():
    """生成简短的问题 ID"""
    timestamp = datetime.datetime.now().strftime("%m%d%H%M")
    rand = hashlib.md5(os.urandom(8)).hexdigest()[:4]
    return f"{timestamp}-{rand}"

def create_worktree(issue_id):
    """创建 git worktree 进行物理隔离"""
    worktree_path = f"../{os.path.basename(os.getcwd())}-trouble-{issue_id}"
    try:
        subprocess.run(
            ["git", "worktree", "add", "-b", f"trouble/{issue_id}", worktree_path],
            capture_output=True, check=True
        )
        return worktree_path
    except subprocess.CalledProcessError:
        # 分支可能已存在，尝试直接添加
        try:
            subprocess.run(
                ["git", "worktree", "add", worktree_path, f"trouble/{issue_id}"],
                capture_output=True, check=True
            )
            return worktree_path
        except:
            return None
    except Exception:
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: start_troubleshoot.py <title> [mode]")
        print("  mode: worktree (default) | subagent")
        sys.exit(1)

    title = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "worktree"
    issue_id = generate_issue_id()

    # 保存主线快照（主线就是当前所有上下文，不需要用户告知）
    snapshot = save_snapshot(issue_id, title, mode)

    result = {
        "issue_id": issue_id,
        "title": title,
        "mode": mode,
        "timestamp": snapshot["timestamp"],
        "snapshot_file": ACTIVE_FILE
    }

    if mode == "worktree":
        worktree_path = create_worktree(issue_id)
        result["worktree_path"] = worktree_path

        if worktree_path:
            result["message"] = f"Worktree created at {worktree_path}"
            result["next_step"] = f"cd {worktree_path}"
        else:
            result["mode"] = "subagent"
            result["message"] = "Worktree failed, fallback to subagent mode"

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
