#!/usr/bin/env python3
"""
定时通知示例
开盘提醒、收盘总结等
"""
import asyncio
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from speak import speak

async def market_open_alert():
    """开盘提醒"""
    await speak("A股开盘了，请注意量化信号！")

async def market_close_summary():
    """收盘总结"""
    await speak("今日收盘，请查看今日收益情况。")

async def lunch_reminder():
    """午餐提醒"""
    await speak("午饭时间到了，记得吃饭休息！")

if __name__ == '__main__':
    if not os.getenv('MI_USER') or not os.getenv('MI_PASS'):
        print("❌ 请先设置 MI_USER 和 MI_PASS 环境变量")
        sys.exit(1)
    
    # 根据时间选择播报内容
    hour = datetime.now().hour
    
    if hour == 9:
        asyncio.run(market_open_alert())
    elif hour == 15:
        asyncio.run(market_close_summary())
    elif hour == 12:
        asyncio.run(lunch_reminder())
    else:
        asyncio.run(speak("这是一条定时测试消息"))
