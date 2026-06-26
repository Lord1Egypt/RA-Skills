#!/usr/bin/env python3
"""
context_guard.py - Context PTL 防御截断

参考 Claude Code 的防御截断机制：
- PTL (Prompt Token Limit) 防御截断
- 自动保留 20% 最新分组
- Compact 压缩后状态重组

用途：
    - 防止重要上下文被截断
    - 智能保留最新信息
    - Compact 模式压缩重组
"""

import json
import re
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path

# 默认配置
DEFAULT_WINDOW = 200000  # 200k token
DEFAULT_BUFFER = 13000    # 13k 预触发缓冲
DEFAULT_RESERVE = 0.2    # 保留 20% 最新分组


class ContextGroup:
    """上下文分组"""
    
    def __init__(self, content: str, group_type: str = "default", priority: int = 0):
        self.content = content
        self.group_type = group_type  # file, plan, skill, mcp, memory
        self.priority = priority      # 0-100, 越高越重要
        self.size = len(content)
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "type": self.group_type,
            "priority": self.priority,
            "size": self.size,
        }


class ContextGuard:
    """
    Context PTL 防御截断
    
    策略：
    1. 将上下文分成多个分组
    2. 计算总大小
    3. 如果超过窗口，触发截断
    4. 优先保留高优先级和最新分组
    5. 保留最新 20% 的分组
    """
    
    def __init__(
        self,
        window: int = DEFAULT_WINDOW,
        buffer: int = DEFAULT_BUFFER,
        reserve_ratio: float = DEFAULT_RESERVE,
    ):
        self.window = window
        self.buffer = buffer
        self.reserve_ratio = reserve_ratio
        self.effective_limit = window - buffer
    
    def estimate_tokens(self, text: str) -> int:
        """估算 token 数（简单估计：中文约 2 字符 ≈ 1 token）"""
        # 粗略估算
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        other_chars = len(text) - chinese_chars
        return int(chinese_chars / 2 + other_chars / 4)
    
    def parse_context(self, text: str) -> List[ContextGroup]:
        """
        解析上下文为分组
        支持的分组标记：
        - @file: 文件内容
        - @plan: 计划
        - @skill: 技能
        - @memory: 记忆
        - @mcp: MCP 工具
        """
        groups = []
        
        # 按标记分割
        pattern = r'(@\w+):([\s\S]*?)(?=(?:@\w+):|$)'
        matches = re.findall(pattern, text)
        
        # 默认分组类型优先级
        type_priority = {
            "memory": 80,   # 记忆高优先级
            "file": 60,    # 文件中等
            "plan": 70,    # 计划中等偏高
            "skill": 50,   # 技能中等
            "mcp": 40,     # MCP 工具较低
            "default": 30,
        }
        
        if matches:
            for group_type, content in matches:
                group_type = group_type[1:]  # 去掉 @
                priority = type_priority.get(group_type, 30)
                groups.append(ContextGroup(content.strip(), group_type, priority))
        else:
            # 无标记，整个作为默认分组
            groups.append(ContextGroup(text, "default", 30))
        
        return groups
    
    def truncate(
        self,
        groups: List[ContextGroup],
        max_tokens: int,
    ) -> List[ContextGroup]:
        """
        截断分组，保留重要和最新的
        """
        # 按优先级和位置排序
        # 位置用负索引（越后面越大）
        for i, g in enumerate(groups):
            g.position = len(groups) - i  # 位置分数，越新越高
        
        # 计算总分并排序
        for g in groups:
            g.score = g.priority * 10 + g.position
        
        # 按分数降序排序
        sorted_groups = sorted(groups, key=lambda x: x.score, reverse=True)
        
        result = []
        total_tokens = 0
        
        # 计算最新分组的数量（保留 20% 最新）
        latest_count = max(1, int(len(groups) * self.reserve_ratio))
        latest_groups = set(groups[-latest_count:])
        
        for g in sorted_groups:
            g_tokens = self.estimate_tokens(g.content)
            
            # 强制保留最新分组
            if g in latest_groups:
                result.append(g)
                total_tokens += g_tokens
                continue
            
            # 非最新分组，检查容量
            if total_tokens + g_tokens <= max_tokens:
                result.append(g)
                total_tokens += g_tokens
        
        # 按原始顺序重组
        result.sort(key=lambda x: x.position)
        
        return result
    
    def compact(self, text: str) -> str:
        """
        Compact 压缩：合并低优先级分组，保留核心
        """
        groups = self.parse_context(text)
        
        if not groups:
            return text
        
        # 计算总 token
        total_tokens = sum(self.estimate_tokens(g.content) for g in groups)
        
        if total_tokens <= self.effective_limit:
            return text
        
        # 截断
        truncated_groups = self.truncate(groups, self.effective_limit)
        
        # 重组
        result_parts = []
        for g in truncated_groups:
            marker = f"@{g.group_type}:"
            result_parts.append(f"{marker}\n{g.content}")
        
        return "\n\n".join(result_parts)
    
    def get_stats(self, text: str) -> dict:
        """
        获取上下文统计
        """
        groups = self.parse_context(text)
        total_tokens = sum(self.estimate_tokens(g.content) for g in groups)
        
        return {
            "total_chars": len(text),
            "total_tokens_estimate": total_tokens,
            "window": self.window,
            "buffer": self.buffer,
            "effective_limit": self.effective_limit,
            "usage_ratio": total_tokens / self.effective_limit if self.effective_limit > 0 else 0,
            "group_count": len(groups),
            "groups": [
                {
                    "type": g.group_type,
                    "priority": g.priority,
                    "size": g.size,
                    "tokens": self.estimate_tokens(g.content),
                }
                for g in groups
            ],
            "needs_truncation": total_tokens > self.effective_limit,
        }


def cmd_compact(args: list):
    """Compact 模式：压缩上下文"""
    if not args:
        print("Usage: context_guard.py compact <file>")
        return
    
    file_path = Path(args[0])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    guard = ContextGuard()
    
    # 显示统计
    stats = guard.get_stats(text)
    print("\n📊 Context Stats:")
    print(f"  Total chars: {stats['total_chars']}")
    print(f"  Token estimate: {stats['total_tokens_estimate']}")
    print(f"  Window: {stats['window']}")
    print(f"  Usage: {stats['usage_ratio']*100:.1f}%")
    print(f"  Groups: {stats['group_count']}")
    print()
    
    if stats['needs_truncation']:
        print("⚠️  Needs truncation, compacting...")
        compacted = guard.compact(text)
        
        # 输出
        output_file = file_path.with_suffix('.compact.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(compacted)
        
        print(f"✅ Compacted → {output_file}")
        print(f"   Original: {len(text)} chars")
        print(f"   Compacted: {len(compacted)} chars")
        print(f"   Reduced: {(1-len(compacted)/len(text))*100:.1f}%")
    else:
        print("✅ No truncation needed")


def cmd_stats(args: list):
    """显示统计信息"""
    if not args:
        print("Usage: context_guard.py stats <file>")
        return
    
    file_path = Path(args[0])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    guard = ContextGuard()
    stats = guard.get_stats(text)
    
    print("\n📊 Context Stats:")
    print(f"  Total chars: {stats['total_chars']:,}")
    print(f"  Token estimate: ~{stats['total_tokens_estimate']:,}")
    print(f"  Window limit: {stats['window']:,}")
    print(f"  Buffer: {stats['buffer']:,}")
    print(f"  Effective limit: {stats['effective_limit']:,}")
    print(f"  Usage: {stats['usage_ratio']*100:.1f}%")
    print(f"  Groups: {stats['group_count']}")
    
    print("\n📦 Groups:")
    for g in stats['groups']:
        print(f"  [{g['type']:10}] {g['tokens']:5} tokens, priority={g['priority']}")
    
    print()
    if stats['needs_truncation']:
        print("⚠️  WARNING: Context exceeds effective limit!")
    else:
        print("✅ OK")


def cmd_split(args: list):
    """分割长文本为多个 chunk"""
    if len(args) < 2:
        print("Usage: context_guard.py split <file> <chunk-size>")
        return
    
    file_path = Path(args[0])
    chunk_size = int(args[1])
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    guard = ContextGuard()
    groups = guard.parse_context(text)
    
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for g in groups:
        g_tokens = guard.estimate_tokens(g.content)
        
        if current_tokens + g_tokens > chunk_size and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_tokens = 0
        
        current_chunk.append(g)
        current_tokens += g_tokens
    
    if current_chunk:
        chunks.append(current_chunk)
    
    # 输出
    output_dir = file_path.parent / f"{file_path.stem}_chunks"
    output_dir.mkdir(exist_ok=True)
    
    for i, chunk in enumerate(chunks):
        content = "\n\n".join(f"@{g.group_type}:\n{g.content}" for g in chunk)
        output_file = output_dir / f"chunk_{i+1:03d}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  chunk_{i+1:03d}.md: {guard.estimate_tokens(content)} tokens")
    
    print(f"\n✅ Split into {len(chunks)} chunks → {output_dir}")


def main():
    if len(sys.argv) < 2:
        print("Usage: context_guard.py <command> [args]")
        print("\nCommands:")
        print("  stats <file>        - 显示上下文统计")
        print("  compact <file>      - Compact 压缩模式")
        print("  split <file> <n>   - 分割为 n tokens 的 chunk")
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    commands = {
        "stats": cmd_stats,
        "compact": cmd_compact,
        "split": cmd_split,
    }
    
    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
