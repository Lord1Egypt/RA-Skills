"""
sync.py - Micro Sync：同步关键信息到热层 MEMORY.md
运行方式: python sync.py
"""
import sys
from pathlib import Path
from datetime import datetime

SKILL_ROOT = Path(r"C:\Users\12084\Desktop\阿巴阿巴工作区\另一个我")
STORAGE_DIR = SKILL_ROOT / "storage" / "cold" / "另一个我"
MEMORY_FILE = Path(r"C:\Users\12084\.openclaw\workspace\MEMORY.md")

def extract_key_changes():
    """从冷层文件提取关键变化"""
    changes = []
    
    # 读取 wechat-profile
    profile_file = STORAGE_DIR / "wechat-profile.md"
    if profile_file.exists():
        content = profile_file.read_text(encoding='utf-8')
        # 提取最新动态
        lines = content.split('\n')
        for line in lines:
            if '最后活跃' in line or '未读' in line:
                changes.append(line.strip())
    
    return changes[:10]

def update_memory():
    """更新热层 MEMORY.md"""
    if not MEMORY_FILE.exists():
        print(f"  ⚠️ MEMORY.md 不存在，跳过")
        return
    
    changes = extract_key_changes()
    
    # 读取现有 MEMORY.md
    content = MEMORY_FILE.read_text(encoding='utf-8')
    
    # 添加微信同步标记
    sync_marker = f"""
---

## 微信画像同步 ({datetime.now().strftime('%Y-%m-%d')})

### 最新动态
"""
    for change in changes:
        sync_marker += f"- {change}\n"
    
    # 检查是否已有同步区块
    if '## 微信画像同步' in content:
        # 替换旧的
        import re
        pattern = r'\n---\n\n## 微信画像同步.*?(?=\n---|\Z)'
        content = re.sub(pattern, sync_marker, content, flags=re.DOTALL)
    else:
        content += sync_marker
    
    MEMORY_FILE.write_text(content, encoding='utf-8')
    print(f"  ✅ 已同步到 MEMORY.md")

def main():
    print("=" * 50)
    print("Micro Sync - 同步到热层")
    print("=" * 50)
    
    if not STORAGE_DIR.exists():
        print("  ❌ 冷层数据不存在，请先运行 main.py")
        return
    
    print("\n[1/2] 提取关键变化...")
    changes = extract_key_changes()
    for c in changes[:5]:
        print(f"  - {c[:80]}")
    
    print("\n[2/2] 更新热层 MEMORY.md...")
    update_memory()
    
    print(f"\n✅ Micro Sync 完成")

if __name__ == "__main__":
    main()
