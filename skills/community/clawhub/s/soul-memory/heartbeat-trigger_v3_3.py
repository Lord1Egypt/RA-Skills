#!/usr/bin/env python3
"""
Soul Memory Heartbeat Auto-Save Trigger v3.3
核心改進：
1. 分層關鍵詞字典（通用 Schema）
2. 語意相似度去重（雙層機制）
3. 多標籤索引系統
4. 優先級動態調整
5. 使用通用術語（無硬編碼用戶字眼）
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime, timedelta

SOUL_MEMORY_PATH = os.environ.get('SOUL_MEMORY_PATH', os.path.dirname(__file__))
sys.path.insert(0, SOUL_MEMORY_PATH)

# ============================================
# 導入核心模組
# ============================================
from core import SoulMemorySystem
from keyword_mapping_v3_3 import classify_content, get_priority_from_tags, KEYWORD_MAPPING
from semantic_dedup_v3_3 import PersistentDedup
from tag_index_v3_3 import TagIndex, update_tag_index

# ============================================
# 路徑配置
# ============================================
SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
SESSIONS_JSON = SESSIONS_DIR / "sessions.json"

# 去重記錄和標籤索引（v3.3）
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "soul-memory" / "data"
DEDUP_FILE = DATA_DIR / "dedup.json"
TAG_INDEX_FILE = DATA_DIR / "tag_index.json"

# ============================================
# Session 數據讀取
# ============================================

def get_active_session_id() -> str:
    """獲取當前 active session 的 ID"""
    try:
        with open(SESSIONS_JSON, 'r', encoding='utf-8') as f:
            sessions = json.load(f)
        
        best_session = None
        best_time = 0
        
        for key, data in sessions.items():
            if isinstance(data, dict) and 'updatedAt' in data:
                if data['updatedAt'] > best_time:
                    best_time = data['updatedAt']
                    best_session = data.get('sessionId', key)
        
        return best_session
    except Exception as e:
        print(f"⚠️ 無法讀取 sessions.json: {e}")
        return None


def read_session_messages(session_id: str, hours: int = 1) -> list:
    """讀取 session 對話內容（最近 N 小時）"""
    session_file = SESSIONS_DIR / f"{session_id}.jsonl"
    
    if not session_file.exists():
        print(f"⚠️ Session 檔案不存在: {session_file}")
        return []
    
    messages = []
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                
                try:
                    entry = json.loads(line)
                    
                    if entry.get('type') != 'message':
                        continue
                    
                    timestamp_str = entry.get('timestamp', '')
                    if not timestamp_str:
                        continue
                    
                    try:
                        msg_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        msg_time = msg_time.replace(tzinfo=None)
                    except:
                        continue
                    
                    if msg_time < cutoff_time:
                        continue
                    
                    message = entry.get('message', {})
                    role = message.get('role', '')
                    content = message.get('content', [])
                    
                    # 提取文本內容
                    text_content = ''
                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get('type') == 'text':
                                text_content += item.get('text', '')
                    
                    if text_content.strip():
                        messages.append({
                            'time': msg_time,
                            'role': role,
                            'content': text_content.strip()
                        })
                        
                except json.JSONDecodeError:
                    continue
                    
    except Exception as e:
        print(f"⚠️ 讀取 session 檔案錯誤: {e}")
    
    return messages


# ============================================
# 內容識別（v3.3 改進）
# ============================================

def identify_important_content(messages: list) -> list:
    """
    識別重要內容（v3.3 - 使用分層關鍵詞）
    
    Args:
        messages: 消息列表
    
    Returns:
        list: 重要內容列表 [{time, content, priority, tags}, ...]
    """
    important = []
    
    for msg in messages:
        content = msg['content']
        
        # 排除規則（v3.3 基礎）
        if len(content) < 30:
            continue
        
        if 'HEARTBEAT.md' in content or 'Read HEARTBEAT.md' in content:
            continue
        
        # v3.3: 使用分層關鍵詞字典
        tags = classify_content(content)
        priority = get_priority_from_tags(tags)
        
        # 長內容提升優先級
        if len(content) > 200 and priority == 'I':
            priority = 'C'
        
        # AI 回應且重要
        if msg['role'] == 'assistant' and (tags or len(content) > 100):
            important.append({
                'time': msg['time'],
                'content': content,
                'priority': priority,
                'tags': tags
            })
    
    return important


# ============================================
# 保存到 Daily File（v3.3 支持標籤）
# ============================================

def save_to_daily_file(content: str, priority: str, tags: list = None) -> str:
    """
    保存到 daily file（支持標籤）
    
    Args:
        content: 內容
        priority: 優先級 [C/I/N]
        tags: [(tag, weight), ...]
    
    Returns:
        str: daily file 路徑
    """
    today = datetime.now().strftime('%Y-%m-%d')
    daily_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    daily_file = daily_dir / f"{today}.md"
    
    daily_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%H:%M')
    header = "\n\n" + "-" * 50 + "\n"
    
    # v3.3: 添加標籤行
    if tags:
        tag_str = ', '.join([f"{t[0]}({t[1]})" for t in tags[:3]])  # 只顯示前 3 個
        header += f"**標籤**: {tag_str}\n"
    
    header += f"## [{priority}] {timestamp} - Heartbeat 自動提取\n"
    header += f"**來源**：Session 對話回顧\n"
    header += f"**時區**：UTC\n\n"
    
    with open(daily_file, 'a', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
        f.write('\n')
    
    return str(daily_file)


# ============================================
# Daily File 統計
# ============================================

def check_daily_memory() -> tuple:
    """檢查今日記憶檔案"""
    today = datetime.now().strftime('%Y-%m-%d')
    daily_file = Path.home() / ".openclaw" / "workspace" / "memory" / f"{today}.md"
    
    if daily_file.exists():
        with open(daily_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 計算各類標記數量
        auto_save_count = content.count('[Auto-Save]')
        heartbeat_extract = content.count('## [C]') + content.count('## [I]') - auto_save_count
        
        return auto_save_count, heartbeat_extract
    
    return 0, 0


# ============================================
# 主函數
# ============================================

def main():
    """Heartbeat 檢查點（v3.3）"""
    print(f"🧠 初始化 Soul Memory System v3.3...")
    system = SoulMemorySystem()
    system.initialize()
    print(f"✅ 記憶系統就緒")
    
    # v3.3: 初始化新組件
    print(f"🔧 初始化去重系統...")
    dedup = PersistentDedup(str(DEDUP_FILE), threshold=0.85, category_based=True)
    
    print(f"🏷️  初始化標籤索引...")
    tag_idx = TagIndex(str(TAG_INDEX_FILE))
    
    # 檢查現有記憶
    auto_save_count, heartbeat_extract_count = check_daily_memory()
    
    print(f"\n🩺 Heartbeat 記憶檢查 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC)")
    print(f"- [Auto-Save] 條目：{auto_save_count} 條")
    print(f"- [Heartbeat 提取] 條目：{heartbeat_extract_count} 條")
    
    # 主動提取對話
    print(f"\n🔍 開始主動提取對話...")
    
    session_id = get_active_session_id()
    if not session_id:
        print("⚠️ 無法獲取 session ID，跳過對話提取")
        print(f"\n📊 最終狀態: ❌ 無新記憶需要保存")
        return
    
    print(f"📋 當前 Session: {session_id[:8]}...")
    
    # 讀取最近 1 小時的對話
    messages = read_session_messages(session_id, hours=1)
    print(f"📝 找到 {len(messages)} 條 recent 消息")
    
    # 識別重要內容
    important = identify_important_content(messages)
    print(f"⭐ 識別出 {len(important)} 條重要內容")
    
    # 統計去重統計
    saved_count = 0
    skipped_exact = 0
    skipped_similar = 0
    
    for item in important:
        # v3.3: 獲取分類
        tags = item['tags']
        if tags:
            category = tags[0][0]  # 使用第一個標籤作為分類
        else:
            category = 'General'
        
        # v3.3: 雙層去重檢查
        is_dup, dedup_type = dedup.is_duplicate(item['content'], category)
        
        if is_dup:
            if dedup_type == 'exact':
                skipped_exact += 1
                print(f"  📦 跳過完全相同 [{item['priority']}] - {len(item['content'])} 字")
            else:
                skipped_similar += 1
                print(f"  🔄 跳過語意相似 [{item['priority']}/{category}] - {len(item['content'])} 字")
            continue
        
        # v3.3: 保存內容 + 標籤
        daily_file = save_to_daily_file(item['content'], item['priority'], tags)
        
        # 保存到去重系統
        dedup.save(item['content'], category)
        
        # v3.3: 更新標籤索引
        update_tag_index(
            item['content'],
            item['priority'],
            tags,
            daily_file,
            tag_idx
        )
        
        saved_count += 1
        tag_display = ', '.join([t[0] for t in tags[:2]]) if tags else '無'
        print(f"  ✅ 保存 [{item['priority']}] {saved_count}/{len(important)} - {len(item['content'])} 字 (標籤: {tag_display})")
    
    # 最終報告
    print(f"\n📊 最終狀態:")
    new_auto_save, new_heartbeat = check_daily_memory()
    
    if new_auto_save > auto_save_count or new_heartbeat > heartbeat_extract_count:
        print(f"✅ 新增記憶已保存")
        print(f"   - 新增: {saved_count} 條")
        print(f"   - 跳過完全相同: {skipped_exact} 條")
        print(f"   - 跳過語意相似: {skipped_similar} 條")
        print(f"   ↳ 保存至 memory/{datetime.now().strftime('%Y-%m-%d')}.md")
        
        # v3.3: 顯示標籤統計
        tag_stats = tag_idx.get_stats()
        print(f"\n🏷️  標籤索引統計:")
        print(f"   - 總標籤數: {tag_stats['total_tags']}")
        print(f"   - 總索引條目: {tag_stats['total_entries']}")
        
        if tag_stats['top_tags']:
            print(f"\n   熱門標籤:")
            for tag, count in tag_stats['top_tags'][:3]:
                print(f"   - {tag}: {count}")
    else:
        print("❌ 無新記憶需要保存")


if __name__ == '__main__':
    main()
