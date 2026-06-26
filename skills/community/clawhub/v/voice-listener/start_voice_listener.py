#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音监听启动器 - 可通过OpenClaw技能系统调用
"""

import subprocess
import sys
import os

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 智能唤醒模式脚本
script_path = os.path.join(current_dir, 'voice_input_baidu_smart.py')

print(f"正在启动语音监听...")
print(f"脚本路径: {script_path}")
print(f"唤醒词: 小龙虾")
print(f"停止词: 停止")
print(f"按 Ctrl+C 可以停止程序")
print(f"=" * 60)

# 启动语音监听
try:
    subprocess.run([sys.executable, script_path])
except KeyboardInterrupt:
    print("\n\n语音监听已停止")
except Exception as e:
    print(f"\n\n启动失败: {e}")
    print("请检查:")
    print("1. Python环境是否正确")
    print("2. 依赖库是否已安装")
    print("3. baidu_config.json 配置是否正确")