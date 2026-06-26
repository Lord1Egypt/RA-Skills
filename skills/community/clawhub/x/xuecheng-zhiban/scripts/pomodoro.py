#!/usr/bin/env python3
"""
学程智伴 - 番茄钟工具
简单的番茄钟计时器，支持自定义时长和休息
"""

import time
import sys

def pomodoro(work_minutes=25, break_minutes=5, cycles=1):
    """
    番茄钟计时器
    
    参数:
        work_minutes: 工作时长（分钟）
        break_minutes: 休息时长（分钟）
        cycles: 循环次数
    """
    print(f"\n🍅 番茄钟开始！\n")
    print(f"📝 专注时长：{work_minutes}分钟")
    print(f"☕ 休息时长：{break_minutes}分钟")
    print(f"🔄 计划循环：{cycles}次\n")
    print("准备好了吗？咱们开始！🚀\n")
    
    for cycle in range(1, cycles + 1):
        print(f"{'='*40}")
        print(f"📍 第 {cycle}/{cycles} 轮")
        print(f"{'='*40}\n")
        
        # 工作时段
        print(f"💪 专注时间！{work_minutes}分钟倒计时开始...")
        countdown(work_minutes * 60, "专注中")
        print("\n✅ 完成！太棒了！🎉\n")
        
        # 如果不是最后一轮，休息
        if cycle < cycles:
            print(f"☕ 休息时间！{break_minutes}分钟放松一下~")
            countdown(break_minutes * 60, "休息中")
            print("\n🎯 休息结束，准备下一轮！\n")
    
    print(f"{'='*40}")
    print("🌟 所有番茄钟完成！你今天超棒的！")
    print(f"{'='*40}\n")

def countdown(seconds, label=""):
    """倒计时显示"""
    start = time.time()
    while True:
        elapsed = time.time() - start
        remaining = seconds - elapsed
        if remaining <= 0:
            break
        
        mins = int(remaining // 60)
        secs = int(remaining % 60)
        
        # 简单的进度条
        progress = elapsed / seconds
        bar_length = 20
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        sys.stdout.write(f"\r{label} [{bar}] {mins:02d}:{secs:02d} ")
        sys.stdout.flush()
        time.sleep(1)
    
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()

def quick_timer(minutes, task_name="任务"):
    """快速计时器"""
    print(f"\n⏱️ 快速计时：{minutes}分钟 - {task_name}")
    print("开始！💪\n")
    countdown(minutes * 60, task_name)
    print("✅ 时间到！任务完成！🎉\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="学程智伴 - 番茄钟工具")
    parser.add_argument("--work", type=int, default=25, help="工作时长（分钟）")
    parser.add_argument("--break", type=int, default=5, help="休息时长（分钟）")
    parser.add_argument("--cycles", type=int, default=1, help="循环次数")
    parser.add_argument("--quick", type=int, help="快速计时（分钟）")
    parser.add_argument("--task", type=str, default="任务", help="任务名称")
    
    args = parser.parse_args()
    
    try:
        if args.quick:
            quick_timer(args.quick, args.task)
        else:
            pomodoro(args.work, args.__dict__["break"], args.cycles)
    except KeyboardInterrupt:
        print("\n\n⏸️ 计时暂停。需要继续时随时叫我！👋\n")
