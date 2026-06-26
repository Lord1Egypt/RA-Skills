#!/usr/bin/env python3
"""
Cross-Agent Learning Synchronization
跨 Agent 同步学习成果
"""

import os
import sys
import json
import glob
import shutil
import argparse
from config import get_workspace, get_shared_context_dir, DEFAULT_OPENCLAW_DIR, load_json


def sync_learning() -> dict:
    """
    同步学习成果到其他 Agent
    """
    # 读取共享知识
    shared_dir = get_shared_context_dir()
    shared_path = os.path.join(shared_dir, "collective-wisdom.json")
    
    if not os.path.exists(shared_path):
        print("No shared knowledge found. Run learn-lesson.py first.")
        return None
    
    shared_data = load_json(shared_path)
    lessons = shared_data.get("lessons", [])
    lesson_count = len(lessons)
    
    if lesson_count == 0:
        print("No lessons to sync")
        return None
    
    print("\n=== Syncing Learning Across Agents ===")
    print()
    print(f"Source: {get_workspace()}")
    print(f"Lessons to sync: {lesson_count}")
    print()
    
    # 获取所有 agent 工作区
    workspaces = [d for d in glob.glob(os.path.join(DEFAULT_OPENCLAW_DIR, "workspace-*")) 
                  if os.path.isdir(d)]
    
    synced_count = 0
    skipped_count = 0
    source_workspace = get_workspace()
    
    for ws in workspaces:
        # 跳过源目录
        if ws == source_workspace:
            skipped_count += 1
            continue
        
        # 创建目标目录
        target_dir = os.path.join(ws, "shared-context", "self-improvement")
        os.makedirs(target_dir, exist_ok=True)
        
        # 复制共享知识
        target_path = os.path.join(target_dir, "collective-wisdom.json")
        shutil.copy2(shared_path, target_path)
        synced_count += 1
        
        ws_name = os.path.basename(ws)
        print(f"Synced to: {ws_name}")
    
    print()
    print("=== Sync Summary ===")
    print(f"Synced to: {synced_count} agents")
    print(f"Skipped: {skipped_count} (source)")
    print(f"Total lessons: {lesson_count}")
    print()
    print("All agents now have access to shared knowledge")
    print()
    
    return {
        "synced_count": synced_count,
        "skipped_count": skipped_count,
        "lesson_count": lesson_count
    }


def main():
    parser = argparse.ArgumentParser(description="跨 Agent 学习同步")
    # 无需参数，全局同步
    args = parser.parse_args()
    
    return sync_learning()


if __name__ == "__main__":
    main()
