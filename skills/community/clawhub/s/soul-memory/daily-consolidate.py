#!/usr/bin/env python3
"""
Soul Memory 每日整合腳本 v1.1
功能：將當日 memory/YYYY-MM-DD.md 內容整合到 soul_memory.md
執行時間：每日 23:59 HKT (香港時間 UTC+8)
時區：HKT (UTC+8)
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

# 香港時區 (UTC+8)
HK_TZ = timezone(timedelta(hours=8))

def get_hk_datetime():
    """獲取香港時間"""
    return datetime.now(HK_TZ)

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
SOUL_MEMORY_FILE = WORKSPACE / "soul-memory" / "soul_memory.md"

def get_today_md():
    """獲取今日的記憶文件路徑（使用香港時間）"""
    today = get_hk_datetime().strftime('%Y-%m-%d')
    return MEMORY_DIR / f"{today}.md"

def get_yesterday_md():
    """獲取昨日的記憶文件路徑（使用香港時間）"""
    yesterday = (get_hk_datetime() - timedelta(days=1)).strftime('%Y-%m-%d')
    return MEMORY_DIR / f"{yesterday}.md"

def read_md_file(path):
    """讀取 md 文件內容"""
    if not path.exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def append_to_soul_memory(content, date_str):
    """追加內容到 soul_memory.md"""
    # 確保文件存在
    SOUL_MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # 讀取現有內容（如有）
    existing = ""
    if SOUL_MEMORY_FILE.exists():
        with open(SOUL_MEMORY_FILE, 'r', encoding='utf-8') as f:
            existing = f.read()
    
    # 檢查是否已包含今日內容（避免重複）
    if f"## {date_str}" in existing:
        print(f"⏭️  {date_str} 已存在於 soul_memory.md，跳過")
        return False
    
    # 追加新內容
    header = f"\n\n{'='*60}\n"
    header += f"## {date_str} - 每日記憶歸檔\n"
    header += f"{'='*60}\n\n"
    
    with open(SOUL_MEMORY_FILE, 'a', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
        f.write("\n")
    
    return True

def main():
    hk_now = get_hk_datetime()
    print(f"🧠 Soul Memory 每日整合開始... ({hk_now.strftime('%Y-%m-%d %H:%M:%S')} HKT)")
    
    # 優先處理今日文件
    today_path = get_today_md()
    today_content = read_md_file(today_path)
    
    if today_content:
        date_str = hk_now.strftime('%Y-%m-%d')
        if append_to_soul_memory(today_content, date_str):
            print(f"✅ 今日記憶已整合：{today_path}")
        else:
            print(f"⏭️  今日記憶已存在，跳過")
    else:
        print(f"⚠️  今日文件不存在：{today_path}")
        
        # 嘗試昨日文件
        yesterday_path = get_yesterday_md()
        yesterday_content = read_md_file(yesterday_path)
        
        if yesterday_content:
            date_str = (get_hk_datetime() - timedelta(days=1)).strftime('%Y-%m-%d')
            if append_to_soul_memory(yesterday_content, date_str):
                print(f"✅ 昨日記憶已整合：{yesterday_path}")
            else:
                print(f"⏭️  昨日記憶已存在，跳過")
        else:
            print(f"⚠️  昨日文件也不存在：{yesterday_path}")
    
    print("🧠 Soul Memory 每日整合完成")

if __name__ == "__main__":
    main()
