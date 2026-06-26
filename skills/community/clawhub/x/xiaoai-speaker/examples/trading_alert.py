#!/usr/bin/env python3
"""
量化交易提醒示例
当股价达到条件时，小爱音箱自动播报
"""
import asyncio
import os
import sys

# 添加脚本路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from speak import speak

async def check_price_and_alert():
    """检查股价并播报"""
    # 这里接入你的数据源
    stock_name = "贵州茅台"
    price = 1500.00
    signal = "买入信号"
    
    message = f"{signal}触发！{stock_name}当前价格{price}元"
    
    # 播报
    result = await speak(message)
    
    if result:
        print(f"✅ 已播报: {message}")
    else:
        print(f"❌ 播报失败")

if __name__ == '__main__':
    # 确保设置了环境变量
    if not os.getenv('MI_USER') or not os.getenv('MI_PASS'):
        print("❌ 请先设置 MI_USER 和 MI_PASS 环境变量")
        sys.exit(1)
    
    asyncio.run(check_price_and_alert())
