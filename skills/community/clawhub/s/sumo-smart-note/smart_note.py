"""
Sumo Smart Note - 智能筆記同步工具
當老爺說「記下來」時，自動同步到 SumoNoteBook

用法:
    python smart_note.py "要記錄的內容" [--title "標題"]
"""

import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime

# ============================================================================
# 設定
# ============================================================================

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', 'C:/Users/rayray/.openclaw/workspace'))
SUMO_SHARED = Path("C:/butler_sumo/library/SumoNoteBook/raw/shared")

# ============================================================================
# 工具函數
# ============================================================================

def get_file_hash(content: str) -> str:
    """計算內容的 MD5 hash"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()[:8]

def get_workspace_name() -> str:
    """從 workspace 路徑取得蘇茉名稱"""
    basename = WORKSPACE.name
    if basename.startswith("workspace"):
        return basename.replace("workspace", "").replace("_", "").capitalize()
    return "Main"

def save_to_workspace(title: str, content: str, tags: list = None) -> Path:
    """保存到 workspace memory"""
    today = datetime.now().strftime("%Y-%m-%d")
    memory_dir = WORKSPACE / "memory"
    memory_dir.mkdir(exist_ok=True)
    
    # 建立檔案
    filename = f"{today}_development_log.md"
    filepath = memory_dir / filename
    
    # 如果檔案已存在，追加內容
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            existing = f.read()
        
        # 檢查是否已有相同內容（根據 hash）
        content_hash = get_file_hash(content)
        if content_hash in existing:
            print(f"[SKIP] Content already exists in {filename}")
            return filepath
        
        new_content = existing + "\n\n---\n\n" + content
    else:
        new_content = content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"[OK] Saved to workspace: {filepath}")
    return filepath

def save_to_sumonotebook(title: str, content: str, tags: list = None) -> Path:
    """同步到 SumoNoteBook raw/shared"""
    SUMO_SHARED.mkdir(parents=True, exist_ok=True)
    
    # 產生檔名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    workspace_name = get_workspace_name()
    
    # 淨化標題（去除非法字元，使用英文或拼音）
    safe_title = "".join(c if c.isalnum() or c in ' -_' else '_' for c in title)
    safe_title = safe_title.strip().replace(' ', '_')[:30]
    if not safe_title or safe_title == '_':
        safe_title = "note"
    
    filename = f"{timestamp}__{workspace_name}__{safe_title}.md"
    filepath = SUMO_SHARED / filename
    
    # 加入標題和標籤
    full_content = f"""# {title}

> 時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 來源：{get_workspace_name()}

---

{content}

---

## 標籤
{tags if tags else '#development #sumo家族'}
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"[OK] Synced to SumoNoteBook: {filepath}")
    return filepath

def extract_concepts(content: str) -> list:
    """從內容中提取概念關鍵詞"""
    # 簡單的關鍵詞提取
    keywords = []
    important_markers = ['###', '##', '**', '- ', '1.', '2.', '3.']
    
    for line in content.split('\n'):
        for marker in important_markers:
            if marker in line:
                # 清理並加入關鍵詞
                word = line.replace(marker, '').strip()
                word = word.replace('**', '').strip()
                if len(word) > 2 and len(word) < 30:
                    keywords.append(word)
    
    return list(set(keywords))[:5]  # 最多5個

# ============================================================================
# 主程式
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    content = sys.argv[1]
    
    # 解析參數
    title = "開發記錄"
    tags = []
    
    for arg in sys.argv[2:]:
        if arg.startswith('--title'):
            title = arg.split(' ', 1)[1] if ' ' in arg else "開發記錄"
        elif arg.startswith('--tags'):
            tags = arg.split(' ', 1)[1].split(',') if ' ' in arg else []
    
    # 如果沒有提供標題，從內容中提取
    if title == "開發記錄" and len(content) > 10:
        lines = content.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#'):
                title = line.strip()[:50]
                break
    
    print("=" * 60)
    print("[SMART NOTE] 智能筆記")
    print("=" * 60)
    print()
    print(f"Title: {title}")
    print(f"Content length: {len(content)} chars")
    print()
    
    # 儲存到 workspace
    workspace_path = save_to_workspace(title, content, tags)
    
    # 同步到 SumoNoteBook
    sumonotebook_path = save_to_sumonotebook(title, content, tags)
    
    print()
    print("=" * 60)
    print("[COMPLETE] 筆記已同步！")
    print("=" * 60)
    print()
    print(f"Workspace: {workspace_path}")
    print(f"SumoNoteBook: {sumonotebook_path}")

if __name__ == '__main__':
    exit(main())