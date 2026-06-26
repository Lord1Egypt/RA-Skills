#!/usr/bin/env python3
"""
save_shared_state.py
将当前 agent session 状态保存到共享内存

用法:
  python scripts/save_shared_state.py --task "正在处理X任务" --status "进行中"
  python scripts/save_shared_state.py --decision "决定做Y" --note "原因Z"
  python scripts/save_shared_state.py --checkpoint  # 定期保存
"""

import os
import sys
import json
import argparse
from datetime import datetime

SHARED_STATE_FILE = r"E:\zhuazhua\.openclaw-shared\memory\shared_state.md"
BACKUP_DIR = r"E:\zhuazhua\.openclaw-shared\memory\backups"

def load_current_state():
    """加载现有 shared state"""
    if not os.path.exists(SHARED_STATE_FILE):
        return {
            "last_updated": None,
            "decisions": [],
            "tasks": [],
            "sessions": {},
            "sync_log": []
        }
    
    # 简单解析：提取 date: 和 last_updated 行
    with open(SHARED_STATE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    state = {
        "last_updated": None,
        "decisions": [],
        "tasks": [],
        "sessions": {},
        "sync_log": []
    }
    
    # 提取最后更新时间
    for line in content.split('\n'):
        if line.startswith('## 最后更新时间'):
            parts = line.split(':', 1)
            if len(parts) > 1:
                state['last_updated'] = parts[1].strip()
    
    return state

def save_state(state):
    """保存 state 到 shared_state.md"""
    os.makedirs(os.path.dirname(SHARED_STATE_FILE), exist_ok=True)
    
    lines = [
        "---",
        "date: 2026-04-04",
        "type: shared-state",
        "version: 1.0",
        "---",
        "",
        "# 共享状态 (Shared State)",
        "",
        "> 所有常驻 agent 共享的状态。每次新 session 启动时读取。",
        "",
        f"## 最后更新时间",
        f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}",
        "",
        "## 重要决策记录",
        "",
        "| 时间 | 决策 | 影响 |",
        "|------|------|------|",
    ]
    
    for d in state.get('decisions', [])[-5:]:  # 只保留最近5条
        lines.append(f"| {d.get('time','')} | {d.get('decision','')} | {d.get('impact','')} |")
    
    lines.extend([
        "",
        "## 待办事项",
        "",
        "| 事项 | 优先级 | 状态 | 来源 |",
        "|------|--------|------|------|",
    ])
    
    for t in state.get('tasks', [])[-10:]:  # 只保留最近10条
        lines.append(f"| {t.get('name','')} | {t.get('priority','')} | {t.get('status','')} | {t.get('source','')} |")
    
    lines.extend([
        "",
        "## Session 存活状态",
        "",
        "| Session | 最后活跃 | 状态 |",
        "|--------|---------|------|",
    ])
    
    for sid, sinfo in state.get('sessions', {}).items():
        lines.append(f"| {sid} | {sinfo.get('last_active','')} | {sinfo.get('status','')} |")
    
    lines.extend([
        "",
        "## 最近同步记录",
        "",
        "| 时间 | 操作 | 操作者 |",
        "|------|------|--------|",
    ])
    
    for log in state.get('sync_log', [])[-10:]:  # 只保留最近10条
        lines.append(f"| {log.get('time','')} | {log.get('action','')} | {log.get('agent','')} |")
    
    with open(SHARED_STATE_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    # 备份
    os.makedirs(BACKUP_DIR, exist_ok=True)
    import shutil
    backup_file = os.path.join(BACKUP_DIR, f"shared_state.{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    shutil.copy2(SHARED_STATE_FILE, backup_file)
    
    return True

def add_decision(state, decision, impact=""):
    """添加决策记录"""
    state['decisions'].append({
        'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'decision': decision,
        'impact': impact
    })
    # 只保留最近20条
    state['decisions'] = state['decisions'][-20:]

def add_task(state, name, priority="P2", source="小爪"):
    """添加待办事项"""
    state['tasks'].append({
        'name': name,
        'priority': priority,
        'status': 'pending',
        'source': source
    })

def update_session(state, session_id, status="活跃"):
    """更新 session 状态"""
    state['sessions'][session_id] = {
        'last_active': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'status': status
    }

def add_sync_log(state, action, agent="小爪"):
    """添加同步记录"""
    state['sync_log'].append({
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'action': action,
        'agent': agent
    })
    # 只保留最近50条
    state['sync_log'] = state['sync_log'][-50:]

def main():
    parser = argparse.ArgumentParser(description="保存共享状态")
    parser.add_argument('--task', help='添加/更新任务')
    parser.add_argument('--priority', default='P2', help='任务优先级')
    parser.add_argument('--decision', help='记录决策')
    parser.add_argument('--impact', default='', help='决策影响')
    parser.add_argument('--note', default='', help='备注')
    parser.add_argument('--checkpoint', action='store_true', help='定期保存检查点')
    parser.add_argument('--session', default='main', help='Session ID')
    parser.add_argument('--session-status', default='活跃', help='Session 状态')
    
    args = parser.parse_args()
    
    state = load_current_state()
    
    if args.checkpoint:
        add_sync_log(state, 'checkpoint保存', '小爪')
    elif args.decision:
        add_decision(state, args.decision, args.impact)
        add_sync_log(state, f'记录决策: {args.decision}', '小爪')
    elif args.task:
        add_task(state, args.task, args.priority)
        add_sync_log(state, f'添加任务: {args.task}', '小爪')
    
    update_session(state, args.session, args.session_status)
    save_state(state)
    
    print(f"[OK] 状态已保存到 shared_state.md")

if __name__ == "__main__":
    main()
