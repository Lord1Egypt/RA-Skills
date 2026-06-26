#!/usr/bin/env python3
"""
new_session.py - 新会话初始化
输出本次会话应加载的记忆清单，帮助 Agent 按需加载，避免全量加载
用法:
  python3 new_session.py init              # 初始化记忆目录结构
  python3 new_session.py load STOCK        # 输出 STOCK 任务应加载的文件清单
  python3 new_session.py load DEPLOY       # 输出 DEPLOY 任务应加载的文件清单
"""
import os, sys, json
from datetime import datetime

MEMORY_DIR   = os.path.expanduser('~/.openclaw/memory')
SESSIONS_DIR = os.path.join(MEMORY_DIR, 'sessions')
INDEX_FILE   = os.path.join(MEMORY_DIR, 'index', 'INDEX.md')
LATEST_FILE  = os.path.join(SESSIONS_DIR, 'latest-summary.md')

# 任务类型 → 额外加载的记忆文件
TASK_MEMORY_MAP = {
    'STOCK':  [os.path.join(MEMORY_DIR, 'stock', 'service.md')],
    'DEPLOY': [os.path.join(MEMORY_DIR, 'ops-experience.md')],
    'CODE':   [],
    'QUERY':  [],
    'REMIND': [],
}

# 目录模板
DIR_TEMPLATE = {
    'index':    ['INDEX.md', 'RULES.md'],
    'sessions': ['SESSION-RULES.md'],
    'stock':    [],
    'ops':      [],
}


def cmd_init():
    """初始化记忆目录结构"""
    for d in DIR_TEMPLATE:
        path = os.path.join(MEMORY_DIR, d)
        os.makedirs(path, exist_ok=True)
        print(f'[创建] {path}')

    # 生成默认 INDEX.md（如不存在）
    if not os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(f'# 记忆索引 - 初始化于 {datetime.now().strftime("%Y-%m-%d")}\n\n')
            f.write('## 新会话加载顺序\n')
            f.write('1. INDEX.md（本文件）\n')
            f.write('2. sessions/latest-summary.md\n')
            f.write('3. 任务专属记忆（按TaskID）\n')
            f.write('4. 近5轮对话（滑动窗口）\n\n')
            f.write('## 任务类型\n')
            for k in TASK_MEMORY_MAP:
                f.write(f'- {k}-*\n')
        print(f'[创建] {INDEX_FILE}')

    # 生成空的 latest-summary.md（如不存在）
    if not os.path.exists(LATEST_FILE):
        with open(LATEST_FILE, 'w', encoding='utf-8') as f:
            f.write(f'# 会话摘要 - {datetime.now().strftime("%Y-%m-%d")}\n\n（暂无历史摘要）\n')
        print(f'[创建] {LATEST_FILE}')

    print('\n[完成] 记忆目录初始化成功')
    print(f'目录: {MEMORY_DIR}')


def cmd_load(task_type: str):
    """输出指定任务类型应加载的文件清单"""
    task_type = task_type.upper()
    files = []

    # 必读文件
    for f in [INDEX_FILE, LATEST_FILE]:
        if os.path.exists(f):
            files.append(f)

    # 任务专属记忆
    for f in TASK_MEMORY_MAP.get(task_type, []):
        if os.path.exists(f):
            files.append(f)

    # 输出清单
    total_size = sum(os.path.getsize(f) for f in files)
    est_tokens = int(total_size * 0.6)  # 粗估：1字节≈0.6token

    print(f'\n=== {task_type} 任务加载清单 ===')
    for f in files:
        size = os.path.getsize(f)
        print(f'  ✅ {f} ({size}字节)')
    print(f'\n预估token消耗: ~{est_tokens} tokens')
    print(f'（不含系统提示~2000 + 近5轮对话~3000）')

    # 输出JSON供程序调用
    result = {
        'task_type': task_type,
        'files': files,
        'total_bytes': total_size,
        'est_tokens': est_tokens
    }
    print(f'\nJSON: {json.dumps(result, ensure_ascii=False)}')
    return result


def main():
    if len(sys.argv) < 2:
        print('用法:')
        print('  python3 new_session.py init')
        print('  python3 new_session.py load STOCK|DEPLOY|CODE|QUERY|REMIND')
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == 'init':
        cmd_init()
    elif cmd == 'load':
        task = sys.argv[2] if len(sys.argv) > 2 else 'QUERY'
        cmd_load(task)
    else:
        print(f'[错误] 未知命令: {cmd}')
        sys.exit(1)


if __name__ == '__main__':
    main()
