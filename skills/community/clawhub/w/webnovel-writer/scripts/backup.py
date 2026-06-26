#!/usr/bin/env python3
"""Novel Writer 数据备份"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

def backup_novel(novel_dir: str, output_dir: str = None):
    """备份小说数据文件（不备份正文，只备份结构化数据）"""
    src = Path(novel_dir).resolve()
    if not src.exists():
        print(f"❌ 目录不存在: {src}")
        return False

    data_files = []
    for pattern in ["character_states.json", "foreshadowing.json", "设定词典.md",
                    "追踪表.md", "检查清单.md", "大纲.md", "设定集.md"]:
        p = src / pattern
        if p.exists():
            data_files.append(p)

    # 也扫描 数据/ 子目录
    data_sub = src / "数据"
    if data_sub.exists():
        data_files.extend(data_sub.glob("*.json"))
        data_files.extend(data_sub.glob("*.md"))

    if not data_files:
        print(f"⚠️  未找到数据文件: {src}")
        return False

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = src.name
    if output_dir:
        dest = Path(output_dir) / f"{name}_backup_{ts}"
    else:
        dest = src / "backups" / f"backup_{ts}"
    dest.mkdir(parents=True, exist_ok=True)

    for f in data_files:
        rel = f.relative_to(src)
        d = dest / rel.parent
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, d / f.name)

    print(f"✅ 已备份 {len(data_files)} 个文件 → {dest}")
    return True

def main():
    if len(sys.argv) < 2:
        print("📖 Novel Writer 数据备份")
        print("用法: backup <小说目录> [输出目录]")
        sys.exit(0)

    backup_novel(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

if __name__ == "__main__":
    main()
