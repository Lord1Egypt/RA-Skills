import os
import shutil
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from enum import Enum

class SyncStrategy(Enum):
    REBASE = "rebase"
    MERGE = "merge"
    FORCE = "force"

def validate_git_repo(repo_path: Path) -> Dict:
    """验证路径是否是有效的 Git 仓库"""
    if not repo_path.exists():
        return {"valid": False, "error": f"路径不存在: {repo_path}"}
    
    if not repo_path.is_dir():
        return {"valid": False, "error": f"不是目录: {repo_path}"}
    
    git_dir = repo_path / ".git"
    if not git_dir.exists():
        return {"valid": False, "error": f"不是 Git 仓库（缺少 .git 目录）: {repo_path}"}
    
    return {"valid": True, "error": None}

def get_repo_remote_url(repo_path: Path, remote_name: str = "origin") -> Optional[str]:
    """获取指定仓库的远程地址"""
    original_dir = os.getcwd()
    try:
        os.chdir(repo_path)
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return None
    finally:
        os.chdir(original_dir)

def get_current_branch(repo_path: Path) -> str:
    """获取仓库当前分支"""
    original_dir = os.getcwd()
    try:
        os.chdir(repo_path)
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip() or "main"
    except:
        return "main"
    finally:
        os.chdir(original_dir)

def git_pull(repo_path: Path, strategy: SyncStrategy = SyncStrategy.REBASE) -> Dict:
    """在指定仓库执行 git pull"""
    original_dir = os.getcwd()
    try:
        os.chdir(repo_path)
        
        # 获取当前分支
        branch = get_current_branch(repo_path)
        
        if strategy == SyncStrategy.REBASE:
            cmd = ["git", "pull", "--rebase", "origin", branch]
        elif strategy == SyncStrategy.MERGE:
            cmd = ["git", "pull", "origin", branch]
        else:  # force 策略跳过 pull
            return {"success": True, "message": "Force strategy: skip pull", "skipped": True}
        
        print(f"  执行: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return {"success": True, "message": "Pull successful", "conflict": False}
        else:
            # 检查冲突
            if "conflict" in result.stderr.lower():
                # 中止合并
                subprocess.run(["git", "rebase", "--abort"], check=False, capture_output=True)
                subprocess.run(["git", "merge", "--abort"], check=False, capture_output=True)
                return {"success": False, "message": "Merge conflict", "conflict": True}
            return {"success": False, "message": result.stderr, "conflict": False}
    
    except Exception as e:
        return {"success": False, "message": str(e), "conflict": False}
    finally:
        os.chdir(original_dir)

def sync_workspace_to_git(
    target_repo_path: str,
    branch: str = None,
    commit_msg: str = None,
    exclude_patterns: List[str] = None,
    pull_before_push: bool = True,
    strategy: str = "rebase"
) -> Dict:
    """
    将 .openclaw/workspace/ 同步到指定的本地 Git 仓库
    
    Args:
        target_repo_path: 目标 Git 仓库的本地路径（必需）
        branch: 目标分支，默认自动检测
        commit_msg: 自定义提交信息
        exclude_patterns: 额外排除的文件/目录列表
        pull_before_push: 是否先执行 git pull
        strategy: 合并策略 rebase/merge/force
    
    Returns:
        操作结果字典
    """
    
    # 配置
    SOURCE_DIR = Path.home() / ".openclaw" / "workspace"
    TARGET_DIR = Path(target_repo_path).expanduser().resolve()
    DEFAULT_EXCLUDES = {"skills", ".git", "__pycache__", ".DS_Store", "node_modules", ".clawhub"}
    
    if exclude_patterns:
        DEFAULT_EXCLUDES.update(exclude_patterns)
    
    # 解析策略
    try:
        sync_strategy = SyncStrategy(strategy.lower())
    except ValueError:
        sync_strategy = SyncStrategy.REBASE
    
    print(f"{'=' * 50}")
    print(f"🚀 Workspace Git Sync")
    print(f"{'=' * 50}")
    
    # 步骤 1: 验证源目录
    print(f"\n📂 步骤 1/6: 检查源目录...")
    if not SOURCE_DIR.exists():
        error_msg = f"源目录不存在: {SOURCE_DIR}"
        print(f"❌ {error_msg}")
        return {"status": "error", "message": error_msg}
    print(f"✅ 源目录: {SOURCE_DIR.absolute()}")
    
    # 步骤 2: 验证目标仓库
    print(f"\n📁 步骤 2/6: 检查目标仓库...")
    validation = validate_git_repo(TARGET_DIR)
    if not validation["valid"]:
        print(f"❌ {validation['error']}")
        return {"status": "error", "message": validation['error']}
    print(f"✅ 目标仓库: {TARGET_DIR}")
    
    # 获取远程信息
    remote_url = get_repo_remote_url(TARGET_DIR)
    if remote_url:
        print(f"🌐 远程地址: {remote_url}")
    
    # 确定分支
    if not branch:
        branch = get_current_branch(TARGET_DIR)
    print(f"🌿 目标分支: {branch}")
    
    # 生成提交信息
    if not commit_msg:
        commit_msg = f"Sync from workspace - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    original_dir = os.getcwd()
    deleted_count = 0
    
    try:
        # 步骤 3: 执行 git pull
        if pull_before_push and sync_strategy != SyncStrategy.FORCE:
            print(f"\n🔄 步骤 3/6: 同步远程变更 (git pull --{sync_strategy.value})...")
            pull_result = git_pull(TARGET_DIR, sync_strategy)
            
            if not pull_result["success"]:
                if pull_result.get("conflict"):
                    error_msg = "检测到合并冲突，请手动解决后重试"
                    print(f"❌ {error_msg}")
                    return {"status": "error", "message": error_msg, "conflict": True}
                else:
                    print(f"⚠️  Pull 失败: {pull_result['message']}")
                    print(f"    继续执行...")
            else:
                if pull_result.get("skipped"):
                    print(f"⏭️  跳过 pull (force 模式)")
                else:
                    print(f"✅ 同步完成")
        else:
            print(f"\n⏭️  步骤 3/6: 跳过 git pull")
        
        # 步骤 4: 清理目标目录（保留 .git）
        print(f"\n🧹 步骤 4/6: 清理目标目录...")
        for item in TARGET_DIR.iterdir():
            if item.name == ".git":
                continue
            if item.name in DEFAULT_EXCLUDES:
                continue
            
            try:
                if item.is_file():
                    item.unlink()
                    deleted_count += 1
                elif item.is_dir():
                    shutil.rmtree(item)
                    deleted_count += 1
            except Exception as e:
                print(f"⚠️  无法删除 {item.name}: {e}")
        
        print(f"✅ 清理完成，删除 {deleted_count} 个项目")
        
        # 步骤 5: 复制文件
        print(f"\n📋 步骤 5/6: 复制文件...")
        copied_count = 0
        skipped_items = []
        
        for item in SOURCE_DIR.iterdir():
            # 检查排除列表
            if item.name in DEFAULT_EXCLUDES:
                skipped_items.append(item.name)
                continue
            
            dest = TARGET_DIR / item.name
            
            try:
                if item.is_file():
                    shutil.copy2(item, dest)
                    copied_count += 1
                    print(f"📄 {item.name}")
                elif item.is_dir():
                    # 复制目录，应用排除规则
                    def ignore_func(dir, contents):
                        return [c for c in contents if c in DEFAULT_EXCLUDES]
                    
                    shutil.copytree(item, dest, ignore=ignore_func)
                    copied_count += 1
                    print(f"📁 {item.name}/")
            except Exception as e:
                print(f"⚠️  复制失败 {item.name}: {e}")
        
        if skipped_items:
            print(f"⏭️  跳过: {', '.join(skipped_items)}")
        print(f"✅ 复制完成，共 {copied_count} 个项目")
        
        # 步骤 6: Git 提交与推送
        print(f"\n🚀 步骤 6/6: 提交与推送...")
        os.chdir(TARGET_DIR)
        
        # 配置 git 用户信息（如未配置）
        subprocess.run(["git", "config", "user.email", "kimi-agent@moonshot.cn"], 
                      check=False, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Kimi Agent"], 
                      check=False, capture_output=True)
        
        # 检查是否有变更
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        
        if not status_result.stdout.strip():
            print(f"ℹ️  没有文件变更，无需提交")
            return {
                "status": "success",
                "message": "No changes to commit",
                "copied": copied_count,
                "target": str(TARGET_DIR),
                "branch": branch
            }
        
        # git add
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
        
        # git commit
        commit_result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            capture_output=True,
            text=True,
            check=True
        )
        
        # 提取 commit hash
        commit_hash = ""
        match = re.search(r"\[.*? ([a-f0-9]+)\]", commit_result.stdout)
        if match:
            commit_hash = match.group(1)[:7]
        
        # git push
        if sync_strategy == SyncStrategy.FORCE:
            print(f"⚠️  使用强制推送 (--force-with-lease)")
            push_cmd = ["git", "push", "--force-with-lease", "origin", branch]
        else:
            push_cmd = ["git", "push", "origin", branch]
        
        subprocess.run(push_cmd, check=True, capture_output=True)
        
        print(f"✅ 提交: {commit_hash}")
        print(f"✅ 推送到 origin/{branch}")
        
        return {
            "status": "success",
            "message": "Sync completed successfully",
            "copied": copied_count,
            "deleted": deleted_count,
            "commit": commit_msg,
            "commit_hash": commit_hash,
            "target": str(TARGET_DIR),
            "remote": remote_url,
            "branch": branch,
            "skipped": skipped_items
        }
    
    except subprocess.CalledProcessError as e:
        error_msg = f"Git 操作失败: {e.stderr if e.stderr else str(e)}"
        print(f"❌ {error_msg}")
        return {"status": "error", "message": error_msg, "target": str(TARGET_DIR)}
    
    except Exception as e:
        error_msg = f"同步失败: {str(e)}"
        print(f"❌ {error_msg}")
        return {"status": "error", "message": error_msg, "target": str(TARGET_DIR)}
    
    finally:
        os.chdir(original_dir)
        print(f"\n{'=' * 50}")
        print(f"✨ 同步完成")
        print(f"{'=' * 50}")


# 便捷函数
def quick_sync(target_path: str, message: str = None):
    """快速同步到指定路径"""
    return sync_workspace_to_git(
        target_repo_path=target_path,
        commit_msg=message
    )

def force_sync(target_path: str, message: str = None):
    """强制同步（覆盖远程）"""
    return sync_workspace_to_git(
        target_repo_path=target_path,
        commit_msg=message,
        strategy="force",
        pull_before_push=False
    )


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 sync_workspace.py <目标仓库路径> [提交信息]")
        print("示例: python3 sync_workspace.py ~/projects/backup-repo")
        sys.exit(1)
    
    target = sys.argv[1]
    message = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = sync_workspace_to_git(target, commit_msg=message)
    print(f"\n结果: {result['status']}")
    if result['status'] == 'error':
        print(f"错误: {result['message']}")
        sys.exit(1)
