#!/usr/bin/env python3
"""
Token 消耗记录工具
记录每次对话的 token 消耗到数据文件
"""

import json
import sys
import os
from datetime import datetime

# 数据文件路径
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
DATA_FILE = os.path.join(DATA_DIR, 'token_log.json')


def ensure_data_file():
    """确保数据文件存在"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)


def load_data():
    """加载数据文件"""
    ensure_data_file()
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}


def save_data(data):
    """保存数据到文件"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def log_token(input_tokens, output_tokens):
    """记录 token 消耗"""
    data = load_data()
    
    today = datetime.now().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%H:%M')
    
    total = input_tokens + output_tokens
    
    if today not in data:
        data[today] = {
            "date": today,
            "input": 0,
            "output": 0,
            "total": 0,
            "sessions": []
        }
    
    # 累加今日数据
    data[today]["input"] += input_tokens
    data[today]["output"] += output_tokens
    data[today]["total"] += total
    
    # 记录本次会话
    data[today]["sessions"].append({
        "time": now,
        "input": input_tokens,
        "output": output_tokens
    })
    
    save_data(data)
    
    print(f"✅ 已记录 {today} {now} 的 token 消耗")
    print(f"   输入：{input_tokens:,} tokens")
    print(f"   输出：{output_tokens:,} tokens")
    print(f"   总计：{total:,} tokens")
    print(f"   今日累计：{data[today]['total']:,} tokens")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python3 log_token.py <输入tokens> <输出tokens>")
        print("示例: python3 log_token.py 1200 800")
        sys.exit(1)
    
    try:
        input_tokens = int(sys.argv[1])
        output_tokens = int(sys.argv[2])
        log_token(input_tokens, output_tokens)
    except ValueError:
        print("❌ 错误：请输入有效的数字")
        sys.exit(1)
