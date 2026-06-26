#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音监听助手 - OpenClaw 技能接口
可通过 OpenClaw 调用此技能
"""

import subprocess
import sys
import os

# 获取技能目录
skill_dir = os.path.dirname(os.path.abspath(__file__))

# 智能唤醒模式脚本
script_path = os.path.join(skill_dir, 'voice_input_baidu_smart.py')

def start():
    """启动语音监听"""
    print("=" * 60)
    print("语音监听助手 - 正在启动...")
    print("=" * 60)
    print(f"脚本: {script_path}")
    print(f"唤醒词: 小龙虾")
    print(f"停止词: 停止")
    print(f"")
    print("使用说明:")
    print("1. 程序启动后进入待机模式")
    print("2. 说: '小龙虾' 激活")
    print("3. 说: '停止' 暂停")
    print(f"")
    print("=" * 60)
    print(f"")

    # 启动语音监听
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except KeyboardInterrupt:
        print("\n\n语音监听已停止")
    except Exception as e:
        print(f"\n\n启动失败: {e}")
        return False

    return True

if __name__ == "__main__":
    success = start()
    if not success:
        sys.exit(1)