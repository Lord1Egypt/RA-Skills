#!/usr/bin/env python3
"""
status.py - Token使用状态检查
显示当前记忆文件大小、预估token消耗、压缩建议
用法: python3 status.py
"""
import os
from datetime import datetime

MEMORY_DIR   = os.path.expanduser('~/.openclaw/memory')
SESSIONS_DIR = os.path.join(MEMORY_DIR, 'sessions')

# token预算上限
BUDGET = {
    '系统提示':     2000,
    'INDEX.md':    500,
    'latest-summary': 1500,
    '任务专属记忆': 1000,
    '近5轮对话':   3000,
    '当前消息':     500,
}
TOTAL_BUDGET = sum(BUDGET.values())


def estimate_tokens(filepath: str) -> int:
    """估算文件token数（中文约1.5字符/token，英文约4字符/token）"""
    if not os.path.exists(filepath):
        return 0
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        text = f.read()
    # 简单估算：中文字符*0.7 + 其他字符*0.25
    cn = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    other = len(text) - cn
    return int(cn * 0.7 + other * 0.25)


def main():
    print('\n' + '='*55)
    print('  📊 Token-Optimizer 状态报告')
    print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('='*55)

    # 扫描记忆文件
    memory_files = []
    for root, dirs, files in os.walk(MEMORY_DIR):
        for f in files:
            if f.endswith('.md'):
                path = os.path.join(root, f)
                size = os.path.getsize(path)
                tokens = estimate_tokens(path)
                memory_files.append((path.replace(MEMORY_DIR+'/', ''), size, tokens))

    memory_files.sort(key=lambda x: x[2], reverse=True)

    print('\n📁 记忆文件 Token 消耗：')
    total_memory_tokens = 0
    for name, size, tokens in memory_files:
        bar = '█' * min(int(tokens/100), 30)
        print(f'  {name:<40} {tokens:>5} tokens  {bar}')
        total_memory_tokens += tokens

    # 预算分析
    print('\n💰 Token 预算分析：')
    for item, budget in BUDGET.items():
        print(f'  {item:<16} 预算: {budget:>5} tokens')
    print(f'  {"─"*35}')
    print(f'  {"总预算上限":<16}       {TOTAL_BUDGET:>5} tokens')

    # latest-summary 实际大小
    latest = os.path.join(SESSIONS_DIR, 'latest-summary.md')
    latest_tokens = estimate_tokens(latest)
    print(f'\n📌 latest-summary.md 实际: {latest_tokens} tokens', end='')
    if latest_tokens > 1500:
        print(f'  ⚠️  超出预算，建议压缩！')
    else:
        print(f'  ✅ 正常')

    # 压缩建议
    print('\n💡 建议：')
    if latest_tokens > 1500:
        print('  ⚠️  运行: python3 compress_session.py')
    else:
        print('  ✅ 当前记忆文件大小正常')

    sessions = [f for f in os.listdir(SESSIONS_DIR)
                if f.endswith('-summary.md') and f != 'latest-summary.md'] \
               if os.path.exists(SESSIONS_DIR) else []
    if len(sessions) > 7:
        print(f'  ⚠️  历史摘要文件过多({len(sessions)}个)，建议清理30天前的归档')

    print(f'\n  目标: 新会话输入token ≤ {TOTAL_BUDGET:,}')
    print('='*55 + '\n')


if __name__ == '__main__':
    main()
