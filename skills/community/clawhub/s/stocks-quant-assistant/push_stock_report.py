#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时推送入口（供 launchd/cron 调用）
根据当前北京时间自动判断推送时段
"""
import os
import sys
import time
import hashlib
from datetime import datetime

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

from stock_monitor import check_and_install, load_config, generate_report, push_report

# ============================================================
# 兜底保护机制：在调用LLM之前就拦截，防止无谓消耗tokens
# ============================================================

PUSH_STATE_FILE = os.path.join(SKILL_DIR, '.push_state')
LAST_REPORT_FILE = os.path.join(SKILL_DIR, '.last_report')

def load_push_state():
    """加载推送状态"""
    try:
        if os.path.exists(PUSH_STATE_FILE):
            with open(PUSH_STATE_FILE, 'r') as f:
                import json
                return json.load(f)
    except Exception:
        pass
    return {'last_push_time': 0, 'last_report_hash': '', 'push_count': 0, 'window_start': time.time(), 'last_content_hash': ''}

def save_push_state(state):
    """保存推送状态"""
    try:
        with open(PUSH_STATE_FILE, 'w') as f:
            import json
            json.dump(state, f)
    except Exception:
        pass

def check_before_llm_call():
    """
    在调用LLM之前检查是否需要生成报告
    返回 (should_generate, reason)
    - True: 需要调用LLM生成报告
    - False: 跳过，不需要调用LLM
    """
    state = load_push_state()
    current_time = time.time()
    
    # 1. 检查时间是否在推送窗口内（配置的时间点前后5分钟）
    config = load_config()
    push_times = config.get('push', {}).get('times', [])
    current_time_str = datetime.now().strftime('%H:%M')
    
    in_time_window = False
    for t in push_times:
        # 解析配置的时间
        try:
            h, m = map(int, t.split(':'))
            target_time = current_time - (current_time % 86400) + h * 3600 + m * 60
            # 检查是否在目标时间的前后5分钟内
            if abs(current_time - target_time) < 300:
                in_time_window = True
                break
        except Exception:
            pass
    
    if not in_time_window:
        return False, f"当前时间 {current_time_str} 不在推送窗口内"
    
    # 2. 检查1小时内推送次数
    window = 3600
    if current_time - state['window_start'] > window:
        state['push_count'] = 0
        state['window_start'] = current_time
    
    if state.get('push_count', 0) >= 5:
        return False, f"1小时内推送次数已达 {state['push_count']} 次，触发保护"
    
    # 3. 检查距离上次推送时间
    time_since_last = current_time - state.get('last_push_time', 0)
    if time_since_last < 300:  # 5分钟内不推送
        return False, f"距离上次推送仅 {time_since_last:.0f} 秒，拒绝重复推送"
    
    # 4. 检查上次报告内容哈希（如果内容相似，大概率也会被拦截）
    last_content_hash = state.get('last_content_hash', '')
    if last_content_hash:
        # 这里我们不拒绝生成，只是记录，供后面对比
        pass
    
    return True, "通过检查，准备生成报告"

def should_push_anyway():
    """强制推送检查（用于手动触发或特殊情况下覆盖保护）"""
    state = load_push_state()
    current_time = time.time()
    # 如果距离上次推送超过30分钟，忽略重复检查
    if current_time - state['last_push_time'] > 1800:
        return True
    return False

def auto_mode():
    """根据当前北京时间自动选择推送时段"""
    hour = datetime.now().hour
    if hour < 10:
        return 'morning'    # 09:15 -> 开盘前
    elif hour < 12:
        return 'noon'       # 10:00 -> 早盘
    elif hour < 14:
        return 'afternoon'  # 13:00 -> 午后
    else:
        return 'evening'    # 14:50 -> 尾盘

def main():
    check_and_install()  # 幂等：已安装则立即返回
    
    # 优先用命令行参数（手动测试时指定），否则自动判断
    mode = sys.argv[1] if len(sys.argv) > 1 else auto_mode()
    config = load_config()
    
    # ============================================================
    # 核心保护：在调用LLM之前检查
    # ============================================================
    if len(sys.argv) == 1:
        should_generate, reason = check_before_llm_call()
        print(f"[INFO] {reason}", file=sys.stderr)
        if not should_generate:
            return
    
    # 只有通过检查才调用LLM生成报告
    report = generate_report(config, mode)
    
    # 如果报告包含异常关键词，且不是手动触发，进一步检查
    if len(sys.argv) == 1 and ('获取失败' in report or '数据异常' in report):
        if not should_push_anyway():
            print(f"[WARN] 数据获取异常，跳过本次推送", file=sys.stderr)
            return
    
    # 最后保护：对比上次推送的内容
    state = load_push_state()
    content_hash = hashlib.md5(report.encode('utf-8')).hexdigest()
    
    if len(sys.argv) == 1:
        if content_hash == state.get('last_content_hash', ''):
            print(f"[WARN] 推送内容与上次相同，跳过", file=sys.stderr)
            return
    
    # 推送
    push_report(report, config)
    
    # 更新状态
    state['last_push_time'] = time.time()
    state['last_content_hash'] = content_hash
    state['push_count'] = state.get('push_count', 0) + 1
    save_push_state(state)

if __name__ == '__main__':
    main()
