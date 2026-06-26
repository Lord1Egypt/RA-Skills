#!/bin/bash
# 浑水美债雷达 - 每日自动运行脚本

cd ~/workspace/agent/skills/us-treasury-radar

# 运行 Python 脚本
python3 radar.py

# 可选：保存到日志文件
# python3 radar.py >> ~/workspace/agent/logs/debt_radar.log 2>&1
