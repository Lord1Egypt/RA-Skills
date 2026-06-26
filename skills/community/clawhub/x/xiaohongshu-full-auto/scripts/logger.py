#!/usr/bin/env python3
"""
发布日志记录
"""

import json
import os
import time
from typing import Dict


LOG_FILE = os.path.join(os.path.dirname(__file__), '../../published.jsonl')


def log_published(record: Dict) -> None:
    """记录一条发布记录"""
    # 确保目录存在
    log_dir = os.path.dirname(LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def get_published_history(limit: int = 100) -> list:
    """获取发布历史"""
    if not os.path.exists(LOG_FILE):
        return []
    
    history = []
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                history.append(json.loads(line))
    
    return history[-limit:]
