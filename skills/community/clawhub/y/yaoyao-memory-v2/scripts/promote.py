#!/usr/bin/env python3
"""
龙虾记忆系统 - 记忆升级脚本
将中期记忆（memory/*.md）升级为长期记忆（MEMORY.md）
"""

import argparse
import os
import re
from datetime import datetime, timedelta
from pathlib import Path


def find_memory_files(memory_dir: str, days: int = 7) -> list:
    """查找指定天数内的记忆文件"""
    memory_path = Path(memory_dir)
    if not memory_path.exists():
        return []
    
    cutoff = datetime.now() - timedelta(days=days)
    files = []
    
    for f in memory_path.glob("*.md"):
        if f.name == "heartbeat-state.json":
            continue
        # 从文件名提取日期 YYYY-MM-DD.md
        match = re.match(r"(\d{4}-\d{2}-\d{2})\.md", f.name)
        if match:
            file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
            if file_date >= cutoff:
                files.append(f)
    
    return sorted(files)


def extract_important_content(file_path: Path) -> list:
    """从记忆文件中提取重要内容"""
    content = file_path.read_text(encoding="utf-8")
    important_items = []
    seen_blocks = set()  # 避免重复提取
    
    # 优先级：决策 > 错误 > 用户 > 重要
    patterns = [
        (r"#决策\b", "decision"),
        (r"#错误\b", "error"),
        (r"#用户\b", "user"),
        (r"#重要\b", "important"),
    ]
    
    lines = content.split("\n")
    for i, line in enumerate(lines):
        # 按优先级匹配，一行只归入一个分类
        for pattern, tag_type in patterns:
            if re.search(pattern, line):
                # 提取该行及后续相关内容
                block_lines = [line]
                j = i + 1
                while j < len(lines) and lines[j].strip() and not lines[j].startswith("#"):
                    block_lines.append(lines[j])
                    j += 1
                
                block_content = "\n".join(block_lines)
                block_hash = hash(block_content)
                
                # 避免重复
                if block_hash not in seen_blocks:
                    seen_blocks.add(block_hash)
                    important_items.append({
                        "type": tag_type,
                        "content": block_content,
                        "source": file_path.name
                    })
                break  # 匹配到一个标签后跳出，避免重复
    
    return important_items


def categorize_content(items: list) -> dict:
    """按类型分类内容"""
    categories = {
        "decision": [],
        "error": [],
        "user": [],
        "important": [],
    }
    
    for item in items:
        cat = item["type"]
        if cat in categories:
            categories[cat].append(item)
    
    return categories


def format_for_memory_md(items: list, category: str) -> str:
    """格式化为 MEMORY.md 格式"""
    if not items:
        return ""
    
    category_names = {
        "decision": "重要决策记录",
        "error": "错误与教训",
        "user": "用户档案",
        "important": "核心知识沉淀",
    }
    
    lines = [f"\n### [{datetime.now().strftime('%Y-%m-%d')}] {category_names.get(category, category)}\n"]
    
    for item in items:
        lines.append(f"- **来源**: {item['source']}")
        lines.append(f"- **内容**: {item['content']}")
        lines.append("")
    
    return "\n".join(lines)


def promote_to_memory_md(memory_md_path: str, items: list, category: str) -> bool:
    """将内容升级到 MEMORY.md"""
    if not items:
        return False
    
    memory_md = Path(memory_md_path)
    if not memory_md.exists():
        print(f"MEMORY.md 不存在: {memory_md_path}")
        return False
    
    content = memory_md.read_text(encoding="utf-8")
    new_section = format_for_memory_md(items, category)
    
    # 找到对应章节插入
    section_markers = {
        "decision": "## 🎯 重要决策记录",
        "error": "## ⚠️ 错误与教训",
        "user": "## 👤 用户档案",
        "important": "## 📚 核心知识沉淀",
    }
    
    marker = section_markers.get(category)
    if marker and marker in content:
        # 在章节末尾插入
        parts = content.split(marker)
        if len(parts) >= 2:
            # 找到下一个 ## 标记
            next_section = parts[1].find("\n## ")
            if next_section == -1:
                # 没有下一章节，追加到末尾
                parts[1] += new_section
            else:
                # 在下一章节前插入
                parts[1] = parts[1][:next_section] + new_section + parts[1][next_section:]
            content = marker.join(parts)
    
    memory_md.write_text(content, encoding="utf-8")
    return True


def mark_as_promoted(file_path: Path, items: list):
    """在原文件标记已升级"""
    content = file_path.read_text(encoding="utf-8")
    
    for item in items:
        # 在内容后添加升级标记
        old_content = item["content"]
        if old_content in content:
            content = content.replace(
                old_content,
                f"{old_content}\n[已升级到 MEMORY.md - {datetime.now().strftime('%Y-%m-%d')}]"
            )
    
    file_path.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="升级中期记忆到长期记忆")
    parser.add_argument("--workspace", default="~/.openclaw/workspace", help="工作空间路径")
    parser.add_argument("--days", type=int, default=7, help="检查最近N天的记忆")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不执行")
    args = parser.parse_args()
    
    workspace = Path(args.workspace).expanduser()
    memory_dir = workspace / "memory"
    memory_md = workspace / "MEMORY.md"
    
    print(f"🔍 扫描最近 {args.days} 天的记忆文件...")
    files = find_memory_files(memory_dir, args.days)
    print(f"   找到 {len(files)} 个文件")
    
    all_items = []
    for f in files:
        items = extract_important_content(f)
        if items:
            print(f"   📄 {f.name}: {len(items)} 条待升级")
            all_items.extend(items)
    
    if not all_items:
        print("✅ 没有需要升级的内容")
        return
    
    categories = categorize_content(all_items)
    
    print("\n📊 升级统计:")
    for cat, items in categories.items():
        if items:
            print(f"   {cat}: {len(items)} 条")
    
    if args.dry_run:
        print("\n[DRY RUN] 预览完成，未执行升级")
        return
    
    print("\n🚀 执行升级...")
    for cat, items in categories.items():
        if items and promote_to_memory_md(memory_md, items, cat):
            print(f"   ✅ {cat}: 已写入 MEMORY.md")
            # 标记原文件
            for item in items:
                source_file = memory_dir / item["source"]
                if source_file.exists():
                    mark_as_promoted(source_file, [item])
    
    print("✅ 升级完成")


if __name__ == "__main__":
    main()
