#!/usr/bin/env python3
"""
Soul Memory Heartbeat Cleanup Script
每3小時自動執行，作為保底清理（主流程以前置過濾為主）
Compatible with Soul Memory v3.3.1
"""

import re
import os
from pathlib import Path
from datetime import datetime

# Memory 目錄
MEMORY_DIR = Path("/root/.openclaw/workspace/memory")

def clean_heartbeat_reports():
    """清理所有記憶文件中的 Heartbeat 報告"""
    if not MEMORY_DIR.exists():
        print(f"❌ Memory 目錄不存在: {MEMORY_DIR}")
        return
    
    # 獲取所有 .md 文件
    md_files = sorted(MEMORY_DIR.glob("*.md"))
    total_cleaned = 0
    files_modified = 0
    
    # Heartbeat 報告的正則表達式模式（多種格式）
    patterns = [
        # 匹配 "## [N] 14:22-23:46 - Heartbeat 系統運作摘要" 格式
        r'##\s+\[N\]\s+.*?Heartbeat\s+.*?\n###.*?\n.*?---\s*\n',
        # 匹配包含 Heartbeat 的條目
        r'##\s+\[.*?\]\s+.*?Heartbeat.*?\n.*?---\s*\n',
        # 匹配完整 Heartbeat 區塊
        r'🔥\s+\[.*?\].*?Heartbeat.*?\*Source:.*?\*\s*\n',
        # 匹配 "🩺 Heartbeat 報告" 區塊
        r'\d+\.\s+🔥.*?Heartbeat.*?\*Source:.*?\*\s*\n'
    ]
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            cleaned_count = 0
            
            # 應用所有清理模式
            for pattern in patterns:
                matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)
                cleaned_count += len(matches)
                content = re.sub(pattern, '', content, flags=re.DOTALL | re.MULTILINE)
            
            # 清理多餘的空行
            content = re.sub(r'\n{3,}', '\n\n', content)
            
            # 如果內容有變化，寫回文件
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_modified += 1
                total_cleaned += cleaned_count
                print(f"✅ 清理: {md_file.name} ({cleaned_count} 條 Heartbeat)")
                
        except Exception as e:
            print(f"❌ 錯誤處理 {md_file}: {e}")
    
    print(f"\n📊 清理總結 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}):")
    print(f"   處理文件: {len(md_files)}")
    print(f"   修改文件: {files_modified}")
    print(f"   移除 Heartbeat: {total_cleaned} 條")
    print(f"🏛️ Heartbeat 清理完成！")
    
    return total_cleaned

if __name__ == "__main__":
    clean_heartbeat_reports()
