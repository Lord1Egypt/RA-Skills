#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票监控 Skill 安装脚本
- 检查并安装依赖（akshare）
- 注册 launchd 定时任务（macOS）或 cron（Linux）
- 生成默认配置文件（如果不存在）
"""

import os
import sys
import subprocess
import platform

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SKILL_DIR, 'config.yaml')
PLIST_PATH = os.path.join(os.path.expanduser('~'), 'Library/LaunchAgents/com.openclaw.stock-monitor.plist')


def run(cmd, check=True, timeout=30):
    """执行 shell 命令"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if check and result.returncode != 0:
        print(f"[ERROR] Command failed: {cmd}")
        print(f"STDERR: {result.stderr}")
    return result


def check_akshare():
    """检查 akshare 是否安装"""
    try:
        import akshare
        print(f"✅ akshare 已安装 ({akshare.__version__})")
        return True
    except ImportError:
        print("⏳ 正在安装 akshare...")
        result = run(f"{sys.executable} -m pip install akshare --quiet", timeout=120)
        if result.returncode == 0:
            print("✅ akshare 安装成功")
            return True
        else:
            print(f"❌ akshare 安装失败: {result.stderr}")
            return False


def create_config():
    """生成默认配置文件（如果不存在）"""
    if os.path.exists(CONFIG_PATH):
        print(f"✅ 配置文件已存在: {CONFIG_PATH}")
        return

    default_config = """# 股票监控配置
# 修改此文件以定制您的股票池

stocks:
  # 示例：添加您想监控的股票
  # - code: "000001"
  #   name: "平安银行"
  #   market: "sz"
  #   emoji: "🏦"
  #   position:
  #     cost: 12.50
  #     quantity: 1000

push:
  channel: "console"   # console | feishu | telegram
  times:
    - "09:15"
    - "10:30"
    - "13:00"
    - "14:50"

  feishu:
    chat_id: ""

  telegram:
    chat_id: ""
    bot_token: ""

advanced:
  history_days: 60
"""

    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        f.write(default_config)
    print(f"✅ 配置文件已创建: {CONFIG_PATH}")
    print("   请编辑 config.yaml 添加您的股票")


def register_launchd():
    """注册 macOS launchd 定时任务"""
    if platform.system() != 'Darwin':
        print("⏭️ 非 macOS 系统，跳过 launchd 注册")
        return

    # 确保 LaunchAgents 目录存在
    launch_agents_dir = os.path.expanduser('~/Library/LaunchAgents')
    os.makedirs(launch_agents_dir, exist_ok=True)

    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.stock-monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{SKILL_DIR}/stock_monitor.py</string>
        <string>morning</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <dict><key>Hour</key><integer>9</integer><key>Minute</key><integer>15</integer></dict>
        <dict><key>Hour</key><integer>10</integer><key>Minute</key><integer>30</integer></dict>
        <dict><key>Hour</key><integer>13</integer><key>Minute</key><integer>0</integer></dict>
        <dict><key>Hour</key><integer>14</integer><key>Minute</key><integer>50</integer></dict>
    </array>
    <key>RunAtLoad</key>
    <false/>
    <key>StandardOutPath</key>
    <string>{SKILL_DIR}/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>{SKILL_DIR}/logs/launchd.err</string>
</dict>
</plist>
"""

    with open(PLIST_PATH, 'w', encoding='utf-8') as f:
        f.write(plist_content)

    # 加载任务
    run(f"launchctl load {PLIST_PATH}", check=False)
    print(f"✅ launchd 定时任务已注册")
    print(f"   推送时间: 09:15 / 10:30 / 13:00 / 14:50")


def register_cron():
    """注册 Linux cron 定时任务"""
    if platform.system() == 'Darwin':
        return  # macOS 用 launchd

    cron_cmd = (
        f"cd {SKILL_DIR} && {sys.executable} stock_monitor.py morning"
    )
    cron_line = (
        "15 9 * * * " + cron_cmd + " >> " + SKILL_DIR + "/logs/cron.log 2>&1\n"
        "30 10 * * * " + cron_cmd + " >> " + SKILL_DIR + "/logs/cron.log 2>&1\n"
        "0 13 * * * " + cron_cmd + " >> " + SKILL_DIR + "/logs/cron.log 2>&1\n"
        "50 14 * * * " + cron_cmd + " >> " + SKILL_DIR + "/logs/cron.log 2>&1\n"
    )

    try:
        result = run(f'(crontab -l 2>/dev/null | grep -v stock_monitor.py; echo "{cron_line}") | crontab -', timeout=5)
        if result.returncode == 0:
            print("✅ cron 定时任务已注册")
        else:
            print(f"⚠️ cron 注册可能失败: {result.stderr}")
    except Exception as e:
        print(f"⚠️ cron 注册失败: {e}")


def main():
    print("=" * 40)
    print("📈 股票监控 Skill 安装程序")
    print("=" * 40)
    print()

    # 1. 检查/安装依赖
    print("[1/4] 检查 Python 依赖...")
    check_akshare()
    print()

    # 2. 创建配置文件
    print("[2/4] 初始化配置文件...")
    os.makedirs(os.path.join(SKILL_DIR, 'logs'), exist_ok=True)
    create_config()
    print()

    # 3. 注册定时任务
    print("[3/4] 注册定时推送任务...")
    if platform.system() == 'Darwin':
        register_launchd()
    else:
        register_cron()
    print()

    # 4. 验证
    print("[4/4] 验证安装...")
    result = run(f'{sys.executable} {SKILL_DIR}/stock_monitor.py --help 2>&1', check=False)
    if result.returncode == 0 or 'generate_report' in result.stdout or 'Usage:' in result.stdout:
        print("✅ 验证通过")
    else:
        # 实际运行一次测试
        test_result = run(f'{sys.executable} {SKILL_DIR}/stock_monitor.py 2>&1', check=False, timeout=30)
        if '股票参考' in test_result.stdout or 'config.yaml' in test_result.stderr:
            print("✅ 验证通过")
        else:
            print(f"⚠️ 验证警告: {test_result.stderr[:200]}")

    print()
    print("=" * 40)
    print("🎉 安装完成！")
    print()
    print("下一步:")
    print(f"  1. 编辑 config.yaml 添加您的股票")
    print(f"  2. 运行  {sys.executable} {SKILL_DIR}/stock_monitor.py  测试输出")
    print()
    if platform.system() == 'Darwin':
        print("定时任务已通过 launchd 管理:")
        print(f"  launchctl list | grep stock-monitor  # 查看状态")
        print(f"  launchctl unload {PLIST_PATH}  # 停止")
        print(f"  launchctl load {PLIST_PATH}     # 启动")


if __name__ == '__main__':
    main()
