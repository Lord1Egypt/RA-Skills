#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Todo Tracker - 待办事项管理
功能：生成待办列表、标记完成、查看进度、验证完成
"""

import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

# 数据存储路径
TODO_STORAGE_PATH = Path.home() / ".openclaw" / "workspace" / "todo-current.json"
MEMORY_PATH = Path.home() / ".openclaw" / "workspace" / "MEMORY.md"

def load_todo_list():
    """读取当前待办列表"""
    try:
        if TODO_STORAGE_PATH.exists():
            with open(TODO_STORAGE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"❌ 读取待办列表失败：{e}")
    return None

def save_todo_list(todo_list):
    """保存待办列表"""
    try:
        TODO_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(TODO_STORAGE_PATH, 'w', encoding='utf-8') as f:
            json.dump(todo_list, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ 保存待办列表失败：{e}")
        return False

def append_to_memory(todo_list):
    """写入 MEMORY.md"""
    try:
        if not MEMORY_PATH.exists():
            return
        
        entry = f"""
## 待办任务 [{todo_list['id']}]
- 创建时间：{todo_list['createdAt']}
- 任务：{todo_list['title']}
- 状态：{len([i for i in todo_list['items'] if i['status'] == 'completed'])}/{len(todo_list['items'])} 已完成

"""
        with open(MEMORY_PATH, 'a', encoding='utf-8') as f:
            f.write(entry)
    except Exception as e:
        print(f"⚠️ 写入 MEMORY.md 失败：{e}")

def generate_todo_list(task_description, items=None):
    """生成待办列表"""
    # 检查是否有未完成的待办
    existing = load_todo_list()
    if existing and any(item['status'] == 'pending' for item in existing.get('items', [])):
        # 如果有未完成的，追加新任务而不是拒绝
        print(f"⚠️ 已有未完成的待办列表，将追加新任务")
        print_progress(existing)
    
    # 如果没有传入 items，使用默认拆解
    if not items:
        items = [
            {'id': str(uuid.uuid4())[:8], 'description': f'步骤 1: {task_description}', 'status': 'pending', 'createdAt': datetime.now().isoformat()},
        ]
    
    todo_list = {
        'id': f'todo_{datetime.now().strftime("%Y%m%d%H%M%S")}',
        'title': task_description[:50],
        'createdAt': datetime.now().isoformat(),
        'items': items
    }
    
    if save_todo_list(todo_list):
        append_to_memory(todo_list)
        return {
            'success': True,
            'message': f'✅ 已生成待办列表，共 {len(items)} 项任务',
            'data': todo_list
        }
    else:
        return {
            'success': False,
            'message': '❌ 保存待办列表失败',
            'data': None
        }

def mark_completed(todo_id):
    """标记待办完成"""
    todo_list = load_todo_list()
    if not todo_list:
        return {
            'success': False,
            'message': '❌ 没有进行中的待办列表',
            'data': None
        }
    
    item = next((i for i in todo_list['items'] if i['id'] == todo_id), None)
    if not item:
        return {
            'success': False,
            'message': f'❌ 未找到 ID 为 {todo_id} 的待办项',
            'data': None
        }
    
    if item['status'] == 'completed':
        return {
            'success': False,
            'message': f'⚠️ 待办项 "{item["description"]}" 已经是完成状态',
            'data': None
        }
    
    item['status'] = 'completed'
    item['completedAt'] = datetime.now().isoformat()
    
    if save_todo_list(todo_list):
        completed_count = len([i for i in todo_list['items'] if i['status'] == 'completed'])
        total_count = len(todo_list['items'])
        return {
            'success': True,
            'message': f'✅ 已完成：{item["description"]}（{completed_count}/{total_count}）',
            'data': {
                'completedItem': item,
                'progress': {'completed': completed_count, 'total': total_count}
            }
        }
    else:
        return {
            'success': False,
            'message': '❌ 保存失败',
            'data': None
        }

def print_progress(todo_list):
    """打印进度"""
    if not todo_list:
        return
    
    pending = [i for i in todo_list['items'] if i['status'] == 'pending']
    completed = [i for i in todo_list['items'] if i['status'] == 'completed']
    
    print(f"\n📋 **待办列表：{todo_list['title']}**")
    print(f"进度：{len(completed)}/{len(todo_list['items'])} 已完成\n")
    
    if completed:
        print("✅ 已完成：")
        for item in completed:
            print(f"  - {item['description']}")
    
    if pending:
        print("\n⏳ 待完成：")
        for item in pending:
            print(f"  - [{item['id']}] {item['description']}")
    print()

def show_progress():
    """查看进度"""
    todo_list = load_todo_list()
    if not todo_list:
        return {
            'success': False,
            'message': '❌ 没有进行中的待办列表',
            'data': None
        }
    
    pending = [i for i in todo_list['items'] if i['status'] == 'pending']
    completed = [i for i in todo_list['items'] if i['status'] == 'completed']
    
    progress_text = f"📋 **待办列表：{todo_list['title']}**\n"
    progress_text += f"进度：{len(completed)}/{len(todo_list['items'])} 已完成\n\n"
    
    if completed:
        progress_text += "✅ 已完成：\n"
        for item in completed:
            progress_text += f"  - {item['description']}\n"
    
    if pending:
        progress_text += "\n⏳ 待完成：\n"
        for item in pending:
            progress_text += f"  - [{item['id']}] {item['description']}\n"
    
    # 打印进度
    print_progress(todo_list)
    
    return {
        'success': True,
        'message': progress_text,
        'data': {
            'title': todo_list['title'],
            'total': len(todo_list['items']),
            'completed': len(completed),
            'pending': len(pending),
            'pendingItems': pending,
            'completedItems': completed
        }
    }

def verify_completion():
    """验证完成情况"""
    todo_list = load_todo_list()
    if not todo_list:
        return {
            'success': False,
            'message': '❌ 没有进行中的待办列表',
            'data': None,
            'allCompleted': False
        }
    
    pending = [i for i in todo_list['items'] if i['status'] == 'pending']
    
    if not pending:
        return {
            'success': True,
            'message': '🎉 所有待办项已完成！任务执行完毕。',
            'data': todo_list,
            'allCompleted': True
        }
    else:
        pending_desc = '\n'.join([f"  - [{i['id']}] {i['description']}" for i in pending])
        return {
            'success': True,
            'message': f'⚠️ 还有 {len(pending)} 项待办未完成：\n{pending_desc}\n\n请继续执行或确认是否跳过。',
            'data': {
                'pendingCount': len(pending),
                'pendingItems': pending
            },
            'allCompleted': False
        }

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法：python3 todo_tracker.py <action> [params]")
        print("动作：generate-todo-list, mark-completed, show-progress, verify-completion")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == 'generate-todo-list':
        task_desc = sys.argv[2] if len(sys.argv) > 2 else "未命名任务"
        result = generate_todo_list(task_desc)
        # 生成后立即显示进度
        if result['success']:
            todo_list = load_todo_list()
            if todo_list:
                print_progress(todo_list)
    elif action == 'mark-completed':
        todo_id = sys.argv[2] if len(sys.argv) > 2 else ""
        result = mark_completed(todo_id)
        # 标记后立即显示进度
        if result['success']:
            todo_list = load_todo_list()
            if todo_list:
                print_progress(todo_list)
    elif action == 'show-progress':
        result = show_progress()
    elif action == 'verify-completion':
        result = verify_completion()
    else:
        print(f"❌ 不支持的动作：{action}")
        sys.exit(1)
    
    if not (action in ['generate-todo-list', 'mark-completed'] and result['success']):
        # 避免重复打印（generate 和 mark 已经打印了进度）
        print(result['message'])
        if result.get('data'):
            print(json.dumps(result['data'], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
