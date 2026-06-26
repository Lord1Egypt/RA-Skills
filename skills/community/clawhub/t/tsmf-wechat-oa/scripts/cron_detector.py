#!/usr/bin/env python3
"""
Cron Job 检测模块
用于判断是否有公众号写作的定时任务
"""

import os
import subprocess
from pathlib import Path


def has_wechat_cron_job() -> bool:
    """
    检测是否有公众号写作的定时任务
    
    检测方式（按优先级）：
    1. 检查 crontab 中是否有 wechat/write_article 相关任务
    2. 检查环境变量 WECHAT_AUTO_MODE
    3. 检查配置文件 ~/.wechat_cron_config
    4. 检查 systemd timer
    
    Returns:
        bool: True 表示有定时任务，False 表示没有
    """
    
    # 方法1：检查 crontab
    try:
        result = subprocess.run(
            ['crontab', '-l'], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            cron_content = result.stdout.lower()
            keywords = ['wechat', 'write_article', '公众号', '写作']
            if any(kw in cron_content for kw in keywords):
                return True
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        pass
    
    # 方法2：检查环境变量
    if os.getenv('WECHAT_AUTO_MODE', '').lower() == 'true':
        return True
    
    # 方法3：检查配置文件
    config_paths = [
        Path.home() / '.wechat_cron_config',
        Path.home() / '.config' / 'wechat' / 'cron.conf',
        Path('/etc/wechat/cron.conf'),
    ]
    for config_path in config_paths:
        if config_path.exists():
            return True
    
    # 方法4：检查 systemd timer
    try:
        result = subprocess.run(
            ['systemctl', 'list-timers', '--all'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            timer_content = result.stdout.lower()
            if 'wechat' in timer_content or 'write' in timer_content:
                return True
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        pass
    
    return False


def get_writing_mode() -> str:
    """
    根据 cron_job 检测获取写作模式
    
    Returns:
        str: 'auto' 表示自动模式，'guided' 表示指定主题模式
    """
    if has_wechat_cron_job():
        return 'auto'
    return 'guided'


def get_mode_description() -> str:
    """获取当前模式的描述"""
    mode = get_writing_mode()
    if mode == 'auto':
        return "自动模式（检测到定时任务）"
    return "指定主题模式（未检测到定时任务）"


if __name__ == "__main__":
    # 测试
    print(f"Cron Job 检测: {has_wechat_cron_job()}")
    print(f"写作模式: {get_writing_mode()}")
    print(f"模式描述: {get_mode_description()}")
