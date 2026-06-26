#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票定时推送脚本
用法: python notify_job.py --codes 600016,000725 --app-id xxx --app-secret xxx --receive-id xxx
"""

import sys
import os
import argparse
import json

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetcher import StockFetcher, send_feishu_private
from trader import StockTrader


def main():
    parser = argparse.ArgumentParser(description='股票定时推送')
    parser.add_argument('--codes', required=True, help='股票代码，用逗号分隔')
    parser.add_argument('--app-id', required=True, help='飞书应用 App ID')
    parser.add_argument('--app-secret', required=True, help='飞书应用 App Secret')
    parser.add_argument('--receive-id', required=True, help='接收者 ID')
    
    args = parser.parse_args()
    
    codes = [c.strip() for c in args.codes.split(',') if c.strip()]
    fetcher = StockFetcher()
    trader = StockTrader()
    
    messages = []
    
    for code in codes:
        # 获取行情
        result = fetcher.get_quote(code)
        
        # 获取持仓
        position = trader.get_position(code)
        
        # 生成卡片
        message = fetcher.format_table(result, position)
        messages.append(message)
    
    # 分别发送每只股票的卡片
    success_count = 0
    for message in messages:
        success = send_feishu_private(message, args.app_id, args.app_secret, args.receive_id, is_card=True)
        if success:
            success_count += 1
    
    if success_count == len(messages):
        print("✅ 已发送")
        return 0
    else:
        print("❌ 发送失败")
        return 1


if __name__ == '__main__':
    sys.exit(main())
