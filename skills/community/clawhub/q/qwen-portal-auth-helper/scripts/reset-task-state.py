#!/usr/bin/env python3
"""
重置 OpenClaw cron 任务状态
当 qwen-portal OAuth 认证成功后，任务可能仍保持错误状态
此脚本重置 consecutiveErrors 和 lastError 字段
"""

import json
import os
import sys

def reset_task_state(task_id):
    """重置指定任务的状态"""
    config_path = os.path.expanduser("~/.openclaw/cron/jobs.json")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ 配置文件未找到: {config_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析错误: {e}")
        return False
    
    modified = False
    for job in data['jobs']:
        if job['id'] == task_id:
            print(f"🔧 重置任务: {job.get('name', 'Unnamed')} ({task_id})")
            
            # 保存原始状态用于日志
            old_errors = job['state'].get('consecutiveErrors', 0)
            old_status = job['state'].get('lastStatus', 'unknown')
            old_error = job['state'].get('lastError', '')
            
            # 重置状态
            job['state']['consecutiveErrors'] = 0
            job['state']['lastStatus'] = 'pending'
            job['state']['lastError'] = ''
            
            print(f"   连续错误: {old_errors} → 0")
            print(f"   状态: {old_status} → pending")
            if old_error:
                print(f"   清除错误: {old_error[:80]}...")
            
            modified = True
            break
    
    if not modified:
        print(f"❌ 未找到任务 ID: {task_id}")
        print("可用任务:")
        for job in data['jobs'][:5]:  # 显示前5个任务
            print(f"  - {job['id']}: {job.get('name', 'Unnamed')}")
        return False
    
    # 保存修改
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✅ 任务状态已重置")
        return True
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("使用: reset-task-state.py <task-id>")
        print("示例: reset-task-state.py 71628635-03e3-414b-865b-e427af4e804f")
        print("\n获取任务ID:")
        print("  openclaw cron list | grep qwen-portal")
        sys.exit(1)
    
    task_id = sys.argv[1]
    success = reset_task_state(task_id)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
