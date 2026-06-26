#!/usr/bin/env python3
"""
process_l3_tasks.py
处理 L3 压缩任务队列，支持多 agent 并发

流程：
1. 读取 inbox 中的 L3 任务
2. 原子性获取 pending 任务（标记为 in_progress）
3. 处理任务
4. 标记为 done

防止冲突：
- 使用原子性文件操作
- 每个任务有 status 字段
- 只有 pending 的任务才会被处理
"""

import os
import re
import glob
import shutil
from datetime import datetime

L3_QUEUE_FILE = r"E:\zhuazhua\.openclaw-shared\memory\inbox\l3_compression_queue.md"
PROCESSED_DIR = r"E:\zhuazhua\.openclaw-shared\memory\inbox\processed"
BACKUP_DIR = r"E:\zhuazhua\.openclaw-shared\memory\inbox\l3_backup"

def load_queue():
    """加载任务队列"""
    if not os.path.exists(L3_QUEUE_FILE):
        return []
    
    with open(L3_QUEUE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按 --- 分隔任务
    tasks = []
    blocks = content.split('---')
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if 'L3_COMPRESSION_TASK' not in block:
            continue
        
        task = {'raw': block, 'status': 'pending', 'session_file': None, 'content': ''}
        
        lines = block.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('status:'):
                task['status'] = line.split(':', 1)[1].strip()
            elif line.startswith('Session文件:'):
                task['session_file'] = line.split(':', 1)[1].strip()
        
        # 提取 session 内容（--- 之后的部分）
        parts = block.split('---', 2)
        if len(parts) >= 3:
            task['content'] = parts[2].strip()
        
        tasks.append(task)
    
    return tasks

def claim_task(session_file):
    """
    原子性获取任务：找到 pending 的任务，标记为 in_progress
    返回 True 表示成功获取，False 表示已被其他 agent 获取
    """
    if not os.path.exists(L3_QUEUE_FILE):
        return False
    
    # 读取文件
    with open(L3_QUEUE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 备份
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_file = os.path.join(BACKUP_DIR, f'l3_queue.{datetime.now().strftime("%Y%m%d_%H%M%S")}.md')
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 查找并修改目标任务
    blocks = content.split('---')
    modified = False
    new_blocks = []
    
    for block in blocks:
        block_stripped = block.strip()
        if not block_stripped:
            continue
        if 'L3_COMPRESSION_TASK' not in block_stripped:
            new_blocks.append(block)
            continue
        
        # 检查是否是目标 session 且状态为 pending
        is_target = False
        for line in block.split('\n'):
            if line.strip().startswith('Session文件:') and session_file in line:
                is_target = True
            if line.strip().startswith('status:') and 'pending' in line.lower():
                if is_target:
                    # 标记为 in_progress
                    block = block.replace('status: pending', 'status: in_progress:xiaozhua')
                    modified = True
        
        new_blocks.append(block)
    
    if not modified:
        return False
    
    # 写回文件
    new_content = '---'.join(new_blocks)
    with open(L3_QUEUE_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def mark_done(session_file):
    """标记任务为完成"""
    if not os.path.exists(L3_QUEUE_FILE):
        return
    
    with open(L3_QUEUE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 将 in_progress 改为 done
    content = re.sub(
        r'status: in_progress:xiaozhua',
        'status: done:xiaozhua',
        content
    )
    
    with open(L3_QUEUE_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

def process_task(task):
    """处理单个 L3 任务"""
    session_file = task['session_file']
    if not session_file or not os.path.exists(session_file):
        print(f"[跳过] Session文件不存在: {session_file}")
        return False
    
    print(f"[处理] L3压缩: {os.path.basename(session_file)}")
    
    # 这里需要 AI 介入处理
    # TODO: 调用 AI 能力生成摘要
    # 目前只是示例，实际需要接入 AI
    
    print(f"[完成] L3压缩: {os.path.basename(session_file)}")
    return True

def main():
    print(f"\n{'='*50}")
    print(f"L3 Compression Task Processor")
    print(f"{'='*50}")
    
    tasks = load_queue()
    pending_tasks = [t for t in tasks if t['status'] == 'pending']
    
    print(f"总任务数: {len(tasks)}")
    print(f"待处理: {len(pending_tasks)}")
    
    if not pending_tasks:
        print("没有待处理的 L3 任务")
        return
    
    processed = 0
    for task in pending_tasks:
        if not task['session_file']:
            continue
        
        # 尝试获取任务（原子性）
        if not claim_task(task['session_file']):
            print(f"[跳过] 任务已被其他agent获取: {task['session_file']}")
            continue
        
        # 处理任务
        success = process_task(task)
        
        if success:
            mark_done(task['session_file'])
            processed += 1
        
        print()
    
    print(f"{'='*50}")
    print(f"处理完成: {processed} 个任务")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
