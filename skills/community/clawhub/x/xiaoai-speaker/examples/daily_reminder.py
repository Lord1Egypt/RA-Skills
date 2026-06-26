#!/usr/bin/env python3
"""
生活提醒示例
定时播报生活相关提醒
"""
import asyncio
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from speak import speak

async def morning_reminder():
    """早上提醒"""
    await speak("早上好！记得喝一杯温水，开启美好的一天！")

async def lunch_reminder():
    """午餐提醒"""
    await speak("午饭时间到了，记得按时吃饭哦！")

async def dinner_reminder():
    """晚餐提醒"""
    await speak("晚饭时间到，该准备吃饭啦！")

async def sleep_reminder():
    """睡觉提醒"""
    await speak("已经晚上11点了，早点休息，不要熬夜！")

async def medicine_reminder():
    """吃药提醒"""
    await speak("该吃药了，记得按时服用！")

async def water_reminder():
    """喝水提醒"""
    await speak("工作这么久，起来活动一下，喝杯水吧！")

if __name__ == '__main__':
    if not os.getenv('MI_USER') or not os.getenv('MI_PASS'):
        print("❌ 请先设置 MI_USER 和 MI_PASS 环境变量")
        sys.exit(1)
    
    # 根据当前时间选择提醒类型
    hour = datetime.now().hour
    
    if 6 <= hour < 9:
        asyncio.run(morning_reminder())
    elif 11 <= hour < 13:
        asyncio.run(lunch_reminder())
    elif 17 <= hour < 19:
        asyncio.run(dinner_reminder())
    elif 22 <= hour or hour < 6:
        asyncio.run(sleep_reminder())
    else:
        asyncio.run(water_reminder())
