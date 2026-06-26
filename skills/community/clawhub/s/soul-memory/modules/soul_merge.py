#!/usr/bin/env python3
"""
Soul Memory v3.5.2 - Smart Incremental Merge & Semantic Injection
核心邏輯：實現增量合併、相似度去重與 soul"..." 標記的自動注入
"""

from datetime import datetime
import re
import hashlib
import difflib
from typing import Dict, Any, List

def merge_memory(existing_memory: str, new_entry: str, label: str) -> str:
    """v3.5.2: 增量合併邏輯，增加相似度檢查去重"""
    # 查找標籤區塊
    pattern = rf'(## soul"{label}".*?)(?=\n## soul"|\Z)'
    match = re.search(pattern, existing_memory, re.DOTALL | re.IGNORECASE)
    
    if match:
        old_block = match.group(0)
        # 檢查相似度，若新條目與舊區塊內容高度相似 (> 90%)，則跳過
        if difflib.SequenceMatcher(None, old_block, new_entry).ratio() > 0.9:
            print(f"⏭️  相似度過高，跳過重複內容寫入: soul\"{label}\"")
            return existing_memory
        
        # 已存在：合併新內容
        updated_content = f"{old_block.rstrip()}\n  - {new_entry.strip()}"
        return existing_memory.replace(old_block, updated_content)
    else:
        # 不存在：新建區塊
        header = f'\n## soul"{label}" (Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")})\n'
        return existing_memory + header + f"  - {new_entry.strip()}\n"

def get_context_for_label(memory_content: str, label: str) -> str:
    """語義注入：從 soul_memory.md 提取標籤內容"""
    pattern = rf'## soul"{label}".*?\n(.*?)(?=\n## soul"|\Z)'
    match = re.search(pattern, memory_content, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""
