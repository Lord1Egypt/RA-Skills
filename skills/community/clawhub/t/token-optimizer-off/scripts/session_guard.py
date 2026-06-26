#!/usr/bin/env python3
"""
session_guard.py - 会话健康度自动判断
Agent 每次回复前调用此脚本，自动判断是否需要新开会话或压缩记忆。

判断逻辑：
  1. 估算当前上下文 token 量
  2. 检测任务类型切换（跨任务污染）
  3. 检测无关内容比例
  4. 输出：继续 / 压缩 / 新开会话

用法:
  python3 session_guard.py check --task STOCK --rounds 15
  python3 session_guard.py check --task STOCK --rounds 15 --context-size 80000
"""
import os, sys, json, argparse
from datetime import datetime

# 配置：支持环境变量覆盖
MEMORY_DIR = os.path.expanduser(os.getenv('TOKEN_OPTIMIZER_MEMORY_DIR', '~/.openclaw/memory'))
SESSIONS_DIR = os.path.join(MEMORY_DIR, 'sessions')
STATE_FILE = os.path.join(SESSIONS_DIR, '.session_state.json')

# ============================================================
# 阈值配置
# ============================================================
THRESHOLDS = {
    'warn_tokens':    40000,   # 超过此值：建议压缩
    'critical_tokens':70000,   # 超过此值：强烈建议新开会话
    'max_rounds':     25,      # 超过此轮数：建议新开会话
    'task_switch_limit': 2,    # 单会话内任务类型切换超过此次：建议新开
    'budget_target':  8500,    # 新会话目标token上限
}

# 任务类型关键词映射（用于自动识别）
TASK_KEYWORDS = {
    'STOCK':  ['股票','行情','持仓','止损','止盈','均线','大盘','A股','买入','卖出','涨跌'],
    'DEPLOY': ['部署','安装','服务','systemd','报错','依赖','pip','venv','启动','重启'],
    'CODE':   ['代码','函数','类','模块','bug','调试','编写','实现','脚本'],
    'QUERY':  ['天气','新闻','彩票','查询','搜索','今天','现在'],
    'REMIND': ['提醒','定时','分钟后','明天','待会'],
}


def detect_task_type(text: str) -> str:
    """根据关键词自动识别任务类型"""
    scores = {t: 0 for t in TASK_KEYWORDS}
    for task, keywords in TASK_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[task] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 'QUERY'


def load_state() -> dict:
    """加载会话状态"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding='utf-8') as f:
            return json.load(f)
    return {
        'session_start': datetime.now().isoformat(),
        'rounds': 0,
        'task_history': [],
        'task_switches': 0,
        'peak_tokens': 0,
        'last_task': '',
    }


def save_state(state: dict):
    """保存会话状态"""
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def reset_state():
    """重置会话状态（新开会话时调用）"""
    state = {
        'session_start': datetime.now().isoformat(),
        'rounds': 0,
        'task_history': [],
        'task_switches': 0,
        'peak_tokens': 0,
        'last_task': '',
    }
    save_state(state)
    return state


def check(task_type: str = None, rounds: int = None,
          context_size: int = None, message: str = '') -> dict:
    """
    核心判断逻辑
    返回: {
      'action': 'continue' | 'compress' | 'new_session',
      'reason': str,
      'load_files': [文件列表],
      'warning': str
    }
    """
    state = load_state()

    # 自动识别任务类型
    if not task_type and message:
        task_type = detect_task_type(message)
    task_type = (task_type or 'QUERY').upper()

    # 更新状态
    if rounds is not None:
        state['rounds'] = rounds
    else:
        state['rounds'] += 1

    if context_size:
        state['peak_tokens'] = max(state['peak_tokens'], context_size)

    # 检测任务切换
    if state['last_task'] and state['last_task'] != task_type:
        state['task_switches'] += 1
    if task_type not in state['task_history']:
        state['task_history'].append(task_type)
    state['last_task'] = task_type

    save_state(state)

    # ---- 判断逻辑 ----
    action = 'continue'
    reason = ''
    warning = ''

    # 1. context_size 超过强制阈值
    if context_size and context_size >= THRESHOLDS['critical_tokens']:
        action = 'new_session'
        reason = f'上下文已达{context_size:,} tokens（阈值{THRESHOLDS["critical_tokens"]:,}），强烈建议新开会话'

    # 2. 轮数超限
    elif state['rounds'] >= THRESHOLDS['max_rounds']:
        action = 'new_session'
        reason = f'会话已进行{state["rounds"]}轮（阈值{THRESHOLDS["max_rounds"]}轮），建议新开会话'

    # 3. 任务类型切换过多（上下文污染）
    elif state['task_switches'] >= THRESHOLDS['task_switch_limit']:
        action = 'new_session'
        reason = f'任务类型切换{state["task_switches"]}次（{" → ".join(state["task_history"])}），上下文已污染，建议新开会话'

    # 4. context_size 超过警告阈值
    elif context_size and context_size >= THRESHOLDS['warn_tokens']:
        action = 'compress'
        reason = f'上下文已达{context_size:,} tokens（阈值{THRESHOLDS["warn_tokens"]:,}），建议压缩记忆'

    # 5. 正常继续
    else:
        action = 'continue'
        reason = f'会话健康（第{state["rounds"]}轮，任务:{task_type}）'

    # 计算应加载的文件
    load_files = _get_load_files(task_type, action)

    result = {
        'action': action,
        'reason': reason,
        'task_type': task_type,
        'rounds': state['rounds'],
        'task_switches': state['task_switches'],
        'load_files': load_files,
        'warning': warning,
    }

    _print_result(result)
    return result


def _get_load_files(task_type: str, action: str) -> list:
    """根据任务类型和动作，返回应加载的最小文件集"""
    # 新开会话只加载最精简的内容
    if action == 'new_session':
        files = []
        index = os.path.join(MEMORY_DIR, 'index', 'INDEX.md')
        latest = os.path.join(SESSIONS_DIR, 'latest-summary.md')
        if os.path.exists(index):  files.append(index)
        if os.path.exists(latest): files.append(latest)
        return files

    # 正常加载：INDEX + latest + 任务专属
    task_memory = {
        'STOCK':  os.path.join(MEMORY_DIR, 'stock', 'service.md'),
        'DEPLOY': os.path.join(MEMORY_DIR, 'ops-experience.md'),
    }
    files = []
    for f in [
        os.path.join(MEMORY_DIR, 'index', 'INDEX.md'),
        os.path.join(SESSIONS_DIR, 'latest-summary.md'),
        task_memory.get(task_type, ''),
    ]:
        if f and os.path.exists(f):
            files.append(f)
    return files


def _print_result(result: dict):
    icons = {'continue': '✅', 'compress': '⚠️', 'new_session': '🔄'}
    icon = icons.get(result['action'], '❓')
    print(f'\n{icon} [{result["action"].upper()}] {result["reason"]}')
    print(f'   任务类型: {result["task_type"]} | 轮数: {result["rounds"]} | 任务切换: {result["task_switches"]}次')
    print(f'   应加载文件({len(result["load_files"])}个):')
    for f in result['load_files']:
        size = os.path.getsize(f) if os.path.exists(f) else 0
        print(f'     - {os.path.basename(f)} ({size}字节)')

    if result['action'] == 'new_session':
        print(f'\n   💡 操作步骤:')
        print(f'      1. python3 compress_session.py   # 先压缩当前会话')
        print(f'      2. 开启新会话窗口')
        print(f'      3. 新会话只需加载上方{len(result["load_files"])}个文件（约{THRESHOLDS["budget_target"]}tokens以内）')
    elif result['action'] == 'compress':
        print(f'\n   💡 运行: python3 compress_session.py')


def main():
    parser = argparse.ArgumentParser(description='会话健康度自动判断')
    sub = parser.add_subparsers(dest='cmd')

    # check 命令
    p_check = sub.add_parser('check', help='检查会话状态')
    p_check.add_argument('--task', help='任务类型 STOCK/DEPLOY/CODE/QUERY/REMIND')
    p_check.add_argument('--rounds', type=int, help='当前会话轮数')
    p_check.add_argument('--context-size', type=int, help='当前上下文token数')
    p_check.add_argument('--message', default='', help='当前消息（用于自动识别任务类型）')

    # reset 命令
    sub.add_parser('reset', help='重置会话状态（新开会话后调用）')

    # status 命令
    sub.add_parser('status', help='查看当前会话状态')

    args = parser.parse_args()

    if args.cmd == 'check':
        check(
            task_type=args.task,
            rounds=args.rounds,
            context_size=args.context_size,
            message=args.message
        )
    elif args.cmd == 'reset':
        reset_state()
        print('✅ 会话状态已重置')
    elif args.cmd == 'status':
        state = load_state()
        print(json.dumps(state, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
