#!/usr/bin/env python3
"""
Soul Memory Heartbeat Auto-Save Trigger
v3.5.10 - 檢查上次 heartbeat 到現在的消息，避免遺漏
"""

import sys
import os
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timedelta, timezone

# ========== 配置 ==========
# 時區配置：香港時間 (UTC+8)
HK_TZ = timezone(timedelta(hours=8))

def get_hk_datetime():
    """獲取香港時間"""
    return datetime.now(HK_TZ)

SOUL_MEMORY_PATH = os.environ.get('SOUL_MEMORY_PATH', os.path.dirname(__file__))
sys.path.insert(0, SOUL_MEMORY_PATH)

from core import SoulMemorySystem

# OpenClaw session 路徑
SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
SESSIONS_JSON = SESSIONS_DIR / "sessions.json"

# 去重記錄文件
DEDUP_FILE = Path.home() / ".openclaw" / "workspace" / "soul-memory" / "dedup_hashes.json"

# Heartbeat 狀態文件（記錄上次執行時間）
HEARTBEAT_STATE_FILE = Path.home() / ".openclaw" / "workspace" / "soul-memory" / "heartbeat_state.json"

def get_heartbeat_state():
    """讀取上次 heartbeat 執行時間"""
    if not HEARTBEAT_STATE_FILE.exists():
        return None
    try:
        with open(HEARTBEAT_STATE_FILE, 'r') as f:
            data = json.load(f)
        return data.get('last_check_time')
    except:
        return None

def save_heartbeat_state():
    """保存當前 heartbeat 執行時間"""
    try:
        HEARTBEAT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HEARTBEAT_STATE_FILE, 'w') as f:
            json.dump({
                'last_check_time': datetime.now().isoformat()
            }, f)
    except Exception as e:
        print(f"⚠️ 無法保存 heartbeat 狀態：{e}")

def get_active_session_id():
    """獲取當前 active session 的 ID（排除 cron/HEARTBEAT session）v3.5.8"""
    try:
        with open(SESSIONS_JSON, 'r', encoding='utf-8') as f:
            sessions = json.load(f)
        
        # 找到最近更新的 session（排除 cron）
        best_session = None
        best_time = 0
        
        for key, data in sessions.items():
            if isinstance(data, dict) and 'updatedAt' in data:
                # v3.5.7: 排除 cron session 和 HEARTBEAT session (agent:main:main)
                if "cron" in key.lower() or key == "agent:main:main":
                    continue
                session_id = data.get('sessionId', key)
                if data['updatedAt'] > best_time:
                    best_time = data['updatedAt']
                    best_session = session_id
        
        return best_session
    except Exception as e:
        print(f"⚠️ 無法讀取 sessions.json: {e}")
        return None

def read_session_messages(session_id, last_check_time=None, hours=3):
    """讀取 session 對話內容（上次 heartbeat 到現在；若無狀態則 fallback 最近 N 小時）"""
    session_file = SESSIONS_DIR / f"{session_id}.jsonl"
    
    if not session_file.exists():
        print(f"⚠️ Session 檔案不存在: {session_file}")
        return []
    
    messages = []
    if last_check_time:
        try:
            cutoff_time = datetime.fromisoformat(last_check_time)
            print(f"📅 檢查時間範圍: {cutoff_time.strftime('%Y-%m-%d %H:%M:%S')} → 現在")
        except Exception:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            print(f"⚠️ heartbeat_state 無效，fallback 檢查最近 {hours} 小時")
    else:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        print(f"📅 無 heartbeat_state，fallback 檢查最近 {hours} 小時")
    
    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                
                try:
                    entry = json.loads(line)
                    
                    # 只處理消息類型
                    if entry.get('type') != 'message':
                        continue
                    
                    # 解析時間戳
                    timestamp_str = entry.get('timestamp', '')
                    if not timestamp_str:
                        continue
                    
                    try:
                        msg_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        msg_time = msg_time.replace(tzinfo=None)
                    except:
                        continue
                    
                    # 只處理最近的消息
                    if msg_time < cutoff_time:
                        continue
                    
                    # 提取消息內容
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

def identify_important_content(messages):
    """識別重要內容（超寬鬆模式 v3.4.0 - 強制記錄技術操作）v3.5.12"""
    important = []
    
    # v3.5.12: 只處理用戶消息，不保存助手回應
    messages = [msg for msg in messages if msg.get('role') == 'user']
    
    # 強制記錄關鍵詞（必須記錄 [C] Critical）
    force_record_keywords = [
        # 安裝/部署
        '安裝', 'install', 'npm install', 'pip install', 'apt install', 'yarn add',
        '部署', 'deploy', 'setup', '配置', 'config', 'configure',
        # 參數修改
        '參數', 'parameter', '修改', 'change', 'update', '設定', 'setting',
        'API Key', 'Token', '密鑰', 'key', 'secret', 'password',
        'provider', '模型', 'model', 'baseUrl', 'endpoint',
        # 開發程式
        '開發', 'develop', '編程', 'programming', '代碼', 'code',
        '創建', 'create', '新增', 'add', '刪除', 'delete', 'remove',
        '修改', 'modify', 'edit', '更新', 'update',
        '測試', 'test', 'debug', '調試', '運行', 'run',
        'git', 'commit', 'push', 'pull', 'clone', 'branch',
        '文件', 'file', '目錄', 'directory', '路徑', 'path',
        'skill', '技能', 'clawhub', 'plugin',
        # 系統操作
        '重啟', 'restart', '啟動', 'start', '停止', 'stop',
        '服務', 'service', '進程', 'process', '端口', 'port',
        # OpenClaw 特定
        'openclaw', 'gateway', 'agent', 'session',
    ]
    
    # 用戶指令關鍵詞（用戶主動要求 = 重要）
    user_intent_keywords = [
        '記住', '保存', '備忘', '提醒', '重要',
        '做', '執行', '完成', '檢查', '查看',
    ]
    
    for msg in messages:
        content = msg['content']
        
        # 排除內容（最小化排除）
        # 1. 太短（降低閾值到 20 字）
        if len(content) < 20:
            continue
        
        # 2. 系統指令（僅排除 HEARTBEAT.md 相關）
        if 'HEARTBEAT.md' in content or 'Read HEARTBEAT.md' in content:
            continue
        
        # 識別重要內容
        importance_score = 0
        priority = 'I'  # 默認 Important（從 Normal 提升）
        is_force_record = False
        
        # 檢查強制記錄關鍵詞
        for keyword in force_record_keywords:
            if keyword.lower() in content.lower():
                importance_score += 3
                priority = 'C'
                is_force_record = True
                break
        
        # 長文本內容（降低閾值 > 50 字）
        if len(content) > 50:
            importance_score += 1
        if len(content) > 100:
            importance_score += 1
        
        # 檢查用戶意圖關鍵詞
        for keyword in user_intent_keywords:
            if keyword in content:
                importance_score += 2
                break
        
        # 用戶消息（用戶說的話更重要）
        if msg['role'] == 'user':
            importance_score += 1
        
        # v3.4.0: 只要 importance_score >= 1 就記錄（從 2 降低到 1）
        # 或者是強制記錄類型
        if importance_score >= 1 or is_force_record:
            important.append({
                'time': msg['time'],
                'content': content,
                'priority': priority,
                'score': importance_score
            })
    
    return important

def should_skip_content(content):
    """前置過濾：跳過 Heartbeat 模板化/系統性內容"""
    skip_patterns = [
        r'Heartbeat 報告',
        r'來源[：:]\s*Session 對話回顧',
        r'分析消息數',
        r'識別重要內容',
        r'保存位置',
        r'今日總計.*條記憶',
        r'System v\d+\.\d+\.\d+\s*運作分析報告'
    ]
    return any(re.search(p, content, re.IGNORECASE) for p in skip_patterns)

def summarize_content(content, max_len=400):
    """超長內容摘要化：1 行摘要 + 最多 3 條要點"""
    if len(content) <= max_len:
        return content

    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
    summary_line = lines[0][:80]

    bullets = []
    for ln in lines[1:]:
        if len(bullets) >= 3:
            break
        if ln.startswith(('-', '•', '*')) or '：' in ln or ':' in ln:
            bullets.append(ln[:120])

    if not bullets:
        chunks = re.split(r'[。.!?！？；;]', content)
        bullets = [c.strip()[:120] for c in chunks if c.strip()][:3]

    out = [f"摘要：{summary_line}"]
    out.extend([f"- {b}" for b in bullets])
    out.append(f"(原文長度：{len(content)} 字，已摘要)")
    return "\n".join(out)

def get_daily_output_file(base_date=None, max_lines=500, max_bytes=50*1024):
    """按行數/檔案大小滾動 daily file：YYYY-MM-DD[-b|-c].md"""
    if base_date is None:
        base_date = datetime.now().strftime('%Y-%m-%d')

    daily_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    daily_dir.mkdir(parents=True, exist_ok=True)

    suffixes = [''] + [f'-{chr(c)}' for c in range(ord('b'), ord('z')+1)]
    for s in suffixes:
        candidate = daily_dir / f"{base_date}{s}.md"
        if not candidate.exists():
            return candidate

        try:
            txt = candidate.read_text(encoding='utf-8')
            line_count = txt.count('\n') + 1
            size = candidate.stat().st_size
            if line_count <= max_lines and size <= max_bytes:
                return candidate
        except Exception:
            return candidate

    return daily_dir / f"{base_date}-overflow.md"

def save_to_daily_file(content, priority):
    """保存到 daily file（使用香港時間）"""
    hk_now = get_hk_datetime()
    today = hk_now.strftime('%Y-%m-%d')
    daily_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    daily_file = daily_dir / f"{today}.md"
    
    # 確保目錄存在
    daily_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成內容
    timestamp = hk_now.strftime('%H:%M')
    header = "\n\n" + "-" * 50 + "\n"
    header += f"## [{priority}] {timestamp} - Heartbeat 自動提取\n"
    header += f"**來源**：Session 對話回顧\n"
    header += f"**時區**：HKT (UTC+8)\n\n"
    
    # 追加到檔案
    with open(daily_file, 'a', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
        f.write('\n')
    
    return str(daily_file)

def normalize_for_dedup(content):
    """內容正規化（v3.5.5 放寬）：只移除固定模板欄位，保留時間戳和 emoji"""
    normalized = content
    # v3.5.5: 不移除時間戳（保留內容差異）
    # normalized = re.sub(r'\b\d{1,2}:\d{2}(:\d{2})?\b', '', normalized)  # 已停用
    # normalized = re.sub(r'\b\d{4}-\d{2}-\d{2}\b', '', normalized)  # 已停用
    # v3.5.5: 不移除 emoji 標頭
    # normalized = re.sub(r'^[\s🔥⭐✅📊🩺💾📈⚠️🎯🏛️✨-]+', '', normalized)  # 已停用
    # 只移除固定模板欄位（這些是系統生成的固定內容）
    for pat in [
        r'來源[：:].*',
        r'時區[：:].*',
        r'分析消息數[：:].*',
        r'識別重要內容[：:].*',
        r'保存位置[：:].*',
        r'今日總計.*條記憶',
        r'Heartbeat 時間[：:].*',
        r'Heartbeat 記憶檢查.*'
    ]:
        normalized = re.sub(pat, '', normalized)
    # 壓縮空白
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized

def get_content_hash(content):
    """計算內容哈希（用於去重）"""
    normalized = normalize_for_dedup(content)
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()

def get_saved_hashes(today_date=None):
    """獲取已保存的內容哈希（使用香港時間）"""
    if today_date is None:
        today_date = get_hk_datetime().strftime('%Y-%m-%d')

    if not DEDUP_FILE.exists():
        return {}

    try:
        with open(DEDUP_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 返回今天的哈希集合
        return data.get(today_date, set())
    except Exception as e:
        print(f"⚠️ 讀取去重記錄失敗: {e}")
        return set()

def save_hash(today_date, content_hash):
    """記錄新的內容哈希"""
    try:
        # 讀取現有記錄
        if DEDUP_FILE.exists():
            with open(DEDUP_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}

        # 更新今天的哈希集合
        if today_date not in data:
            data[today_date] = []

        if content_hash not in data[today_date]:
            data[today_date].append(content_hash)

        # 保存
        with open(DEDUP_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"⚠️ 保存去重記錄失敗: {e}")

def check_daily_memory():
    """檢查今日記憶檔案（使用香港時間）"""
    today = get_hk_datetime().strftime('%Y-%m-%d')
    daily_file = Path.home() / ".openclaw" / "workspace" / "memory" / f"{today}.md"
    
    if daily_file.exists():
        with open(daily_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 計算各類標記數量
        auto_save_count = content.count('[Auto-Save]')
        heartbeat_extract_count = content.count('## [I]') + content.count('## [C]') - content.count('[Auto-Save]')
        
        return auto_save_count, heartbeat_extract_count
    
    return 0, 0

def main():
    """Heartbeat 檢查點"""
    print(f"🧠 初始化 Soul Memory System v3.5.3...")
    system = SoulMemorySystem()
    system.initialize()
    print(f"✅ 記憶系統就緒")

    # 步驟 1：檢查現有記憶
    auto_save_count, heartbeat_extract_count = check_daily_memory()

    hk_now = get_hk_datetime()
    print(f"\n🩺 Heartbeat 記憶檢查 ({hk_now.strftime('%Y-%m-%d %H:%M:%S')} HKT/UTC+8)")
    print(f"- [Auto-Save] 條目：{auto_save_count} 條")
    print(f"- [Heartbeat 提取] 條目：{heartbeat_extract_count} 條")

    # 步驟 2：主動提取對話（新功能 v3.2.0）
    print(f"\n🔍 開始主動提取對話...")

    session_id = get_active_session_id()
    if not session_id:
        print("⚠️ 無法獲取 session ID，跳過對話提取")
    else:
        print(f"📋 當前 Session: {session_id[:8]}...")

        # 讀取上次 heartbeat 到現在的對話；首次無狀態時 fallback 最近 3 小時
        last_check_time = get_heartbeat_state()
        messages = read_session_messages(session_id, last_check_time=last_check_time, hours=3)
        print(f"📝 找到 {len(messages)} 條 recent 消息")
        save_heartbeat_state()

        # 識別重要內容
        important = identify_important_content(messages)
        print(f"⭐ 識別出 {len(important)} 條重要內容")

        # 去重：獲取已保存的哈希（使用香港時間）
        today = get_hk_datetime().strftime('%Y-%m-%d')
        saved_hashes = get_saved_hashes(today)
        print(f"🔒 已有 {len(saved_hashes)} 條今日記憶")

        # 保存重要內容（跳過重複）
        saved_count = 0
        skipped_count = 0

        for item in important:
            content_hash = get_content_hash(item['content'])

            # 檢查是否已經保存過
            if content_hash in saved_hashes:
                skipped_count += 1
                print(f"  ⏭️  跳過重複 [{item['priority']}] - {len(item['content'])} 字")
                continue

            # 保存新內容
            daily_file = save_to_daily_file(item['content'], item['priority'])
            save_hash(today, content_hash)  # 記錄哈希
            saved_count += 1
            print(f"  ✅ 保存 [{item['priority']}] {saved_count}/{len(important)} - {len(item['content'])} 字")

        if saved_count > 0:
            print(f"💾 已保存 {saved_count} 條新記憶至 {daily_file}")
        if skipped_count > 0:
            print(f"🔄 跳過 {skipped_count} 條重複記憶")

    # 最終報告
    print(f"\n📊 最終狀態:")
    new_auto_save, new_heartbeat = check_daily_memory()

    if new_auto_save > auto_save_count or new_heartbeat > heartbeat_extract_count:
        print(f"✅ 新增記憶已保存")
        print(f"   - Auto-Save: {new_auto_save - auto_save_count} 條")
        print(f"   - Heartbeat 提取: {new_heartbeat - heartbeat_extract_count} 條")
        print(f"   ↳ 保存至 memory/{datetime.now().strftime('%Y-%m-%d')}.md")
    else:
        print("❌ 無新記憶需要保存")

if __name__ == '__main__':
    main()
