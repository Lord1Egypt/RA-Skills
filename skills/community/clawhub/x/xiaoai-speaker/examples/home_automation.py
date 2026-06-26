#!/usr/bin/env python3
"""
智能家居联动示例
结合传感器数据，自动语音播报
"""
import asyncio
import os
import sys
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from speak import speak

async def door_open_alert():
    """门打开提醒"""
    await speak("前门已打开，欢迎回家！")

async def temperature_alert():
    """温度提醒"""
    temp = random.randint(20, 35)  # 模拟温度
    if temp > 30:
        await speak(f"当前室温{temp}度，建议开启空调！")
    else:
        await speak(f"当前室温{temp}度，温度适宜。")

async def delivery_alert():
    """快递提醒"""
    await speak("有快递到了，请查收！")

if __name__ == '__main__':
    if not os.getenv('MI_USER') or not os.getenv('MI_PASS'):
        print("❌ 请先设置 MI_USER 和 MI_PASS 环境变量")
        sys.exit(1)
    
    # 模拟场景
    asyncio.run(delivery_alert())
