#!/usr/bin/env python3
"""
记忆压缩器 - 压缩和归档旧记忆

用法:
    # 压缩30天前的记忆
    python memory_compressor.py compress --older-than 30d --output archive.md
    
    # 生成记忆摘要
    python memory_compressor.py summarize --days 7
    
    # 清理过期记忆
    python memory_compressor.py clean --older-than 90d --dry-run
"""

import argparse
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict


class MemoryCompressor:
    """记忆压缩器"""
    
    def __init__(self, base_dir: str = "/root/.openclaw/workspace"):
        self.base_dir = Path(base_dir)
        self.memory_dir = self.base_dir / "memory"
        self.archive_dir = self.base_dir / "memory_archive"
        self.archive_dir.mkdir(exist_ok=True)
    
    def compress_old_memories(self, days: int, output_file: str = None) -> str:
        """
        压缩旧记忆
        
        Args:
            days: 压缩N天前的记忆
            output_file: 输出文件路径
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # 收集旧记忆
        old_memories = []
        files_to_archive = []
        
        for memory_file in self.memory_dir.glob("*.md"):
            try:
                file_date = datetime.strptime(memory_file.stem, "%Y-%m-%d")
                if file_date < cutoff_date:
                    content = memory_file.read_text(encoding='utf-8')
                    memories = self._parse_memories(content, memory_file.stem)
                    old_memories.extend(memories)
                    files_to_archive.append(memory_file)
            except:
                continue
        
        if not old_memories:
            return "没有需要压缩的旧记忆"
        
        # 按分类和重要性分组
        compressed = self._compress_by_category(old_memories)
        
        # 生成归档内容
        archive_content = self._generate_archive(compressed, days)
        
        # 保存归档文件
        if not output_file:
            output_file = f"archive_{cutoff_date.strftime('%Y%m%d')}_{datetime.now().strftime('%Y%m%d')}.md"
        
        output_path = self.archive_dir / output_file
        output_path.write_text(archive_content, encoding='utf-8')
        
        # 移动原文件到归档目录
        archive_subdir = self.archive_dir / f"raw_{cutoff_date.strftime('%Y%m%d')}"
        archive_subdir.mkdir(exist_ok=True)
        
        for file in files_to_archive:
            file.rename(archive_subdir / file.name)
        
        return f"已压缩 {len(old_memories)} 条记忆到 {output_path}"
    
    def _parse_memories(self, content: str, date_str: str) -> List[Dict]:
        """解析记忆"""
        memories = []
        
        pattern = r'### (\d{2}:\d{2}:\d{2}) \[重要性:(\d+)/10\]\n- \*\*内容\*\*: (.+?)\n- \*\*分类\*\*: (.+?)\n- \*\*标签\*\*: (.+?)\n'
        
        for match in re.finditer(pattern, content, re.DOTALL):
            memories.append({
                "date": date_str,
                "time": match.group(1),
                "importance": int(match.group(2)),
                "content": match.group(3).strip(),
                "category": match.group(4).strip(),
                "tags": [t.strip() for t in match.group(5).split(',') if t.strip() != '无']
            })
        
        return memories
    
    def _compress_by_category(self, memories: List[Dict]) -> Dict:
        """按分类压缩记忆"""
        compressed = defaultdict(lambda: {"high": [], "medium": [], "low": []})
        
        for memory in memories:
            category = memory.get('category', 'general')
            importance = memory.get('importance', 5)
            
            if importance >= 8:
                level = "high"
            elif importance >= 5:
                level = "medium"
            else:
                level = "low"
            
            compressed[category][level].append(memory)
        
        return dict(compressed)
    
    def _generate_archive(self, compressed: Dict, days: int) -> str:
        """生成归档内容"""
        lines = [
            f"# 记忆归档 ({days}天前)",
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## 摘要",
            ""
        ]
        
        # 按分类生成摘要
        for category, levels in sorted(compressed.items()):
            total = sum(len(mems) for mems in levels.values())
            if total == 0:
                continue
            
            lines.append(f"### {category}")
            lines.append(f"总计: {total} 条记忆")
            lines.append("")
            
            # 重要记忆（详细保留）
            if levels['high']:
                lines.append("**重要记忆**:")
                for m in levels['high']:
                    lines.append(f"- [{m['date']}] {m['content']}")
                lines.append("")
            
            # 中等记忆（摘要）
            if levels['medium']:
                lines.append(f"**一般记忆**: {len(levels['medium'])} 条")
                # 按日期分组摘要
                by_date = defaultdict(list)
                for m in levels['medium']:
                    by_date[m['date']].append(m)
                
                for date, mems in sorted(by_date.items()):
                    topics = set()
                    for m in mems:
                        # 提取前10个字作为主题
                        topic = m['content'][:10] + "..."
                        topics.add(topic)
                    lines.append(f"  - {date}: {len(mems)} 条 ({', '.join(list(topics)[:3])})")
                lines.append("")
            
            # 低重要性记忆（仅统计）
            if levels['low']:
                lines.append(f"**次要记忆**: {len(levels['low'])} 条 (已归档，详情见原始文件)")
                lines.append("")
        
        return '\n'.join(lines)
    
    def summarize_period(self, days: int) -> str:
        """生成时间段摘要"""
        memories = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            memory_file = self.memory_dir / f"{date_str}.md"
            
            if memory_file.exists():
                content = memory_file.read_text(encoding='utf-8')
                day_memories = self._parse_memories(content, date_str)
                memories.extend(day_memories)
        
        if not memories:
            return f"最近{days}天没有记忆记录"
        
        # 生成摘要
        summary_lines = [
            f"# 记忆摘要 (最近{days}天)",
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"记忆总数: {len(memories)} 条",
            "",
            "## 分类统计",
            ""
        ]
        
        # 按分类统计
        by_category = defaultdict(list)
        for m in memories:
            by_category[m['category']].append(m)
        
        for category, mems in sorted(by_category.items(), key=lambda x: -len(x[1])):
            summary_lines.append(f"- **{category}**: {len(mems)} 条")
        
        summary_lines.extend(["", "## 重要记忆", ""])
        
        # 列出高重要性记忆
        important = [m for m in memories if m['importance'] >= 8]
        if important:
            for m in sorted(important, key=lambda x: x['date'], reverse=True)[:10]:
                summary_lines.append(f"- [{m['date']}] {m['content'][:80]}...")
        else:
            summary_lines.append("无")
        
        summary_lines.extend(["", "## 标签云", ""])
        
        # 统计标签
        tag_counts = defaultdict(int)
        for m in memories:
            for tag in m.get('tags', []):
                tag_counts[tag] += 1
        
        top_tags = sorted(tag_counts.items(), key=lambda x: -x[1])[:10]
        for tag, count in top_tags:
            summary_lines.append(f"- {tag}: {count} 次")
        
        return '\n'.join(summary_lines)
    
    def clean_old_memories(self, days: int, dry_run: bool = True) -> str:
        """清理过期记忆"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        files_to_remove = []
        
        for memory_file in self.memory_dir.glob("*.md"):
            try:
                file_date = datetime.strptime(memory_file.stem, "%Y-%m-%d")
                if file_date < cutoff_date:
                    files_to_remove.append(memory_file)
            except:
                continue
        
        if dry_run:
            return f"[模拟运行] 将删除 {len(files_to_remove)} 个文件 (来自{days}天前)"
        else:
            # 实际删除前，先压缩备份
            self.compress_old_memories(days)
            
            for file in files_to_remove:
                file.unlink()
            
            return f"已清理 {len(files_to_remove)} 个过期记忆文件"


def main():
    parser = argparse.ArgumentParser(description='记忆压缩器')
    parser.add_argument('action', choices=['compress', 'summarize', 'clean'],
                       help='操作类型')
    parser.add_argument('--older-than', type=str, help='处理N天前的 (如 30d)')
    parser.add_argument('--days', type=int, help='天数')
    parser.add_argument('--output', type=str, help='输出文件')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行')
    
    args = parser.parse_args()
    
    compressor = MemoryCompressor()
    
    if args.action == 'compress':
        if not args.older_than:
            print("[X] 请提供 --older-than (如 30d)")
            return
        
        days = int(args.older_than.rstrip('d'))
        result = compressor.compress_old_memories(days, args.output)
        print(result)
    
    elif args.action == 'summarize':
        if not args.days:
            print("[X] 请提供 --days")
            return
        
        summary = compressor.summarize_period(args.days)
        print(summary)
    
    elif args.action == 'clean':
        if not args.older_than:
            print("[X] 请提供 --older-than")
            return
        
        days = int(args.older_than.rstrip('d'))
        result = compressor.clean_old_memories(days, args.dry_run)
        print(result)


if __name__ == '__main__':
    main()
