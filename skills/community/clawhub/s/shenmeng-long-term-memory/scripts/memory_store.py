#!/usr/bin/env python3
"""
记忆存储器 - 存储和管理长期记忆

用法:
    # 添加记忆
    python memory_store.py add \
      --content "用户喜欢喝咖啡不加糖" \
      --category "user_preference" \
      --tags "饮食,偏好" \
      --importance 7
    
    # 批量导入
    python memory_store.py import --file memories.json
    
    # 查看今日记忆
    python memory_store.py today
    
    # 查看重要记忆
    python memory_store.py list --importance-above 8
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import re


class MemoryStore:
    """记忆存储器"""
    
    def __init__(self, base_dir: str = "/root/.openclaw/workspace"):
        self.base_dir = Path(base_dir)
        self.memory_dir = self.base_dir / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        
        self.core_memory_file = self.base_dir / "MEMORY.md"
        self.user_file = self.base_dir / "USER.md"
    
    def _get_today_file(self) -> Path:
        """获取今日记忆文件"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.memory_dir / f"{today}.md"
    
    def _get_memory_file(self, date_str: str) -> Path:
        """获取指定日期的记忆文件"""
        return self.memory_dir / f"{date_str}.md"
    
    def add_memory(self, content: str, category: str = "general", 
                   tags: List[str] = None, importance: int = 5,
                   source: str = "manual") -> Dict:
        """
        添加记忆
        
        Args:
            content: 记忆内容
            category: 分类 (user_preference, decision, event, task, etc.)
            tags: 标签列表
            importance: 重要性 (1-10)
            source: 来源 (manual, auto, extraction)
        """
        memory = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "category": category,
            "tags": tags or [],
            "importance": importance,
            "source": source
        }
        
        # 存储到日常记忆文件
        self._append_to_daily(memory)
        
        # 如果重要性高，同时更新核心记忆
        if importance >= 8:
            self._update_core_memory(memory)
        
        return memory
    
    def _append_to_daily(self, memory: Dict):
        """追加到日常记忆文件"""
        file_path = self._get_today_file()
        
        # 创建文件头（如果是新文件）
        if not file_path.exists():
            header = f"""# Memory Log - {datetime.now().strftime("%Y-%m-%d")}

## Key Events

"""
            file_path.write_text(header, encoding='utf-8')
        
        # 格式化记忆条目
        tags_str = ", ".join(memory['tags']) if memory['tags'] else "无"
        entry = f"""### {memory['timestamp'][11:19]} [重要性:{memory['importance']}/10]
- **内容**: {memory['content']}
- **分类**: {memory['category']}
- **标签**: {tags_str}
- **来源**: {memory['source']}

"""
        
        # 追加到文件
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(entry)
    
    def _update_core_memory(self, memory: Dict):
        """更新核心记忆文件"""
        if not self.core_memory_file.exists():
            # 创建基础结构
            content = """# MEMORY.md - 长期记忆

## 用户偏好

## 重要事件

## 决策记录

## 经验教训

"""
            self.core_memory_file.write_text(content, encoding='utf-8')
        
        # 根据分类决定存储位置
        category_map = {
            "user_preference": "## 用户偏好",
            "decision": "## 决策记录",
            "event": "## 重要事件",
            "lesson": "## 经验教训"
        }
        
        section = category_map.get(memory['category'], "## 其他")
        
        # 读取现有内容
        content = self.core_memory_file.read_text(encoding='utf-8')
        
        # 在对应section下添加
        if section in content:
            lines = content.split('\n')
            new_lines = []
            inserted = False
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                if line.startswith(section) and not inserted:
                    # 在该section下添加记忆
                    new_lines.append(f"- {memory['content']} ({memory['timestamp'][:10]})")
                    inserted = True
            
            if inserted:
                self.core_memory_file.write_text('\n'.join(new_lines), encoding='utf-8')
    
    def import_memories(self, file_path: str) -> List[Dict]:
        """批量导入记忆"""
        path = Path(file_path)
        
        if not path.exists():
            return [{"error": f"文件不存在: {file_path}"}]
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = []
        for item in data:
            memory = self.add_memory(
                content=item.get('content', ''),
                category=item.get('category', 'general'),
                tags=item.get('tags', []),
                importance=item.get('importance', 5),
                source=item.get('source', 'import')
            )
            results.append(memory)
        
        return results
    
    def list_memories(self, date: str = None, importance_above: int = None,
                      category: str = None, tag: str = None) -> List[Dict]:
        """列出记忆"""
        memories = []
        
        # 确定要搜索的文件
        if date:
            files = [self._get_memory_file(date)]
        else:
            files = sorted(self.memory_dir.glob("*.md"), reverse=True)
        
        for file_path in files:
            if not file_path.exists():
                continue
            
            content = file_path.read_text(encoding='utf-8')
            file_memories = self._parse_memories(content)
            
            # 应用过滤
            for memory in file_memories:
                if importance_above and memory.get('importance', 0) < importance_above:
                    continue
                if category and memory.get('category') != category:
                    continue
                if tag and tag not in memory.get('tags', []):
                    continue
                
                memories.append(memory)
        
        return memories
    
    def _parse_memories(self, content: str) -> List[Dict]:
        """解析记忆文件内容"""
        memories = []
        
        # 简单解析 - 根据格式提取
        pattern = r'### (\d{2}:\d{2}:\d{2}) \[重要性:(\d+)/10\]\n- \*\*内容\*\*: (.+?)\n- \*\*分类\*\*: (.+?)\n- \*\*标签\*\*: (.+?)\n'
        
        for match in re.finditer(pattern, content, re.DOTALL):
            memories.append({
                "timestamp": match.group(1),
                "importance": int(match.group(2)),
                "content": match.group(3).strip(),
                "category": match.group(4).strip(),
                "tags": [t.strip() for t in match.group(5).split(',') if t.strip() != '无']
            })
        
        return memories
    
    def get_today_summary(self) -> str:
        """获取今日记忆摘要"""
        today_file = self._get_today_file()
        
        if not today_file.exists():
            return "今日暂无记忆记录"
        
        content = today_file.read_text(encoding='utf-8')
        memories = self._parse_memories(content)
        
        if not memories:
            return "今日暂无记忆记录"
        
        # 生成摘要
        lines = [f"今日记忆 ({len(memories)} 条):", ""]
        
        for m in memories:
            importance_marker = "🔴" if m['importance'] >= 8 else "🟡" if m['importance'] >= 5 else "🟢"
            lines.append(f"{importance_marker} [{m['category']}] {m['content'][:50]}...")
        
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='记忆存储器')
    parser.add_argument('action', choices=['add', 'import', 'list', 'today'], 
                       help='操作类型')
    parser.add_argument('--content', type=str, help='记忆内容')
    parser.add_argument('--category', type=str, default='general', help='分类')
    parser.add_argument('--tags', type=str, help='标签（逗号分隔）')
    parser.add_argument('--importance', type=int, default=5, help='重要性 (1-10)')
    parser.add_argument('--file', type=str, help='导入文件路径')
    parser.add_argument('--date', type=str, help='日期 (YYYY-MM-DD)')
    parser.add_argument('--importance-above', type=int, help='重要性阈值')
    
    args = parser.parse_args()
    
    store = MemoryStore()
    
    if args.action == 'add':
        if not args.content:
            print("[X] 请提供 --content")
            return
        
        tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
        memory = store.add_memory(
            content=args.content,
            category=args.category,
            tags=tags,
            importance=args.importance
        )
        print(f"[OK] 记忆已存储")
        print(f"  内容: {memory['content'][:50]}...")
        print(f"  重要性: {memory['importance']}/10")
    
    elif args.action == 'import':
        if not args.file:
            print("[X] 请提供 --file")
            return
        
        results = store.import_memories(args.file)
        print(f"[OK] 已导入 {len(results)} 条记忆")
    
    elif args.action == 'list':
        memories = store.list_memories(
            date=args.date,
            importance_above=args.importance_above,
            category=args.category
        )
        print(f"[*] 找到 {len(memories)} 条记忆")
        for m in memories[:20]:  # 只显示前20条
            print(f"  [{m['importance']}/10] {m['content'][:60]}...")
    
    elif args.action == 'today':
        summary = store.get_today_summary()
        print(summary)


if __name__ == '__main__':
    main()
