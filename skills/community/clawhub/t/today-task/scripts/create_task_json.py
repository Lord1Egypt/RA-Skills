#!/usr/bin/env python3
"""
快速创建任务JSON文件
用法: python create_task_json.py <任务名称> <内容文件>
"""
import json
import sys
from datetime import datetime

if len(sys.argv) < 3:
    print("用法: python create_task_json.py <任务名称> <内容文件>")
    sys.exit(1)

name = sys.argv[1]
filepath = sys.argv[2]

# 读取内容
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"[ERROR] 文件不存在: {filepath}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] 读取文件失败: {e}")
    sys.exit(1)

# 创建JSON数据
data = {
    "task_name": name,
    "task_content": content,
    "task_result": "任务已完成"
}

# 生成文件名
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output = f"{name}_{timestamp}.json"

# 保存文件
try:
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[SUCCESS] 已创建: {output}")
    print(f"[INFO] 使用命令: python task_push.py --data {output}")
except Exception as e:
    print(f"[ERROR] 保存JSON文件失败: {e}")
    sys.exit(1)