#!/usr/bin/env python3
"""
完成问题排查流程
- 应用或丢弃隔离环境的变更
- 归档解决方案
- 返回主线
"""
import os
import sys
import json
import datetime
import subprocess

TROUBLE_DIR = ".trouble-shooting"
ACTIVE_FILE = f"{TROUBLE_DIR}/active.json"
ARCHIVE_DIR = f"{TROUBLE_DIR}/archive"

def load_snapshot():
    if not os.path.exists(ACTIVE_FILE):
        return None
    with open(ACTIVE_FILE, 'r') as f:
        return json.load(f)

def archive_solution(snapshot, solution, action):
    """归档解决方案"""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    archive = {
        **snapshot,
        "solved_at": datetime.datetime.now().isoformat(),
        "solution": solution,
        "action": action  # 'applied' or 'discarded'
    }

    archive_file = f"{ARCHIVE_DIR}/{snapshot['id']}.json"
    with open(archive_file, 'w') as f:
        json.dump(archive, f, indent=2, ensure_ascii=False)

    return archive_file

def apply_worktree_changes(snapshot):
    """将 worktree 的变更应用到主线"""
    worktree_path = f"../{os.path.basename(os.getcwd())}-trouble-{snapshot['id']}"

    if not os.path.exists(worktree_path):
        return {"success": False, "error": "Worktree not found"}

    try:
        # 切换到原分支
        subprocess.run(
            ["git", "checkout", snapshot['branch']],
            capture_output=True, check=True
        )

        # 从 worktree 分支 cherry-pick 或合并变更
        result = subprocess.run(
            ["git", "merge", f"trouble/{snapshot['id']}", "--no-edit"],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            # 合并失败，尝试 cherry-pick
            return {"success": False, "error": "Merge failed, manual resolution needed"}

        # 清理 worktree
        subprocess.run(
            ["git", "worktree", "remove", "-f", worktree_path],
            capture_output=True, check=True
        )

        # 删除临时分支
        subprocess.run(
            ["git", "branch", "-D", f"trouble/{snapshot['id']}"],
            capture_output=True
        )

        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def discard_worktree(snapshot):
    """丢弃 worktree 的变更"""
    worktree_path = f"../{os.path.basename(os.getcwd())}-trouble-{snapshot['id']}"

    try:
        # 清理 worktree
        if os.path.exists(worktree_path):
            subprocess.run(
                ["git", "worktree", "remove", "-f", worktree_path],
                capture_output=True, check=True
            )

        # 删除临时分支
        subprocess.run(
            ["git", "branch", "-D", f"trouble/{snapshot['id']}"],
            capture_output=True
        )

        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def remove_active_file():
    if os.path.exists(ACTIVE_FILE):
        os.remove(ACTIVE_FILE)

def main():
    if len(sys.argv) < 2:
        print("Usage: finish_troubleshoot.py <action> [solution]")
        print("  action: apply | discard")
        sys.exit(1)

    action = sys.argv[1]  # 'apply' or 'discard'
    solution = sys.argv[2] if len(sys.argv) > 2 else "Fixed"

    # 加载快照
    snapshot = load_snapshot()
    if not snapshot:
        print(json.dumps({"error": "No active troubleshooting session"}))
        sys.exit(1)

    # 处理 worktree 变更
    if snapshot.get("mode") == "worktree":
        if action == "apply":
            result = apply_worktree_changes(snapshot)
        else:
            result = discard_worktree(snapshot)
    else:
        result = {"success": True, "mode": "subagent"}

    # 归档
    archive_file = archive_solution(snapshot, solution, action)

    # 清理 active file
    remove_active_file()

    # 输出结果
    output = {
        "issue_id": snapshot['id'],
        "title": snapshot['title'],
        "action": action,
        "solution": solution,
        "archive_file": archive_file,
        "cleanup": result
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))

    # 输出用户友好的信息
    if action == "apply":
        print(f"\n✅ 变更已应用到主线")
    else:
        print(f"\n🗑️  变更已丢弃")

    print(f"✅ 问题已归档 (#{snapshot['id']})")
    print(f"🎯 回到主线上下文")

if __name__ == "__main__":
    main()
