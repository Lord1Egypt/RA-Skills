#!/usr/bin/env python3
"""
Session 交接脚本
在新 session 启动时，自动加载旧 session 的摘要
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path


def get_workspace_root():
    """获取 workspace 根目录"""
    # 从当前脚本路径推断
    script_dir = Path(__file__).parent
    return script_dir.parent


def get_recent_memory_files(days=2):
    """获取最近 N 天的记忆文件"""
    workspace = get_workspace_root()
    memory_dir = workspace / "memory"
    
    if not memory_dir.exists():
        return []
    
    files = []
    today = datetime.now()
    
    for i in range(days):
        date = today - timedelta(days=i)
        filename = date.strftime("%Y-%m-%d.md")
        filepath = memory_dir / filename
        
        if filepath.exists():
            files.append(filepath)
    
    return files


def extract_session_summary(memory_file):
    """从记忆文件中提取 session 摘要"""
    try:
        content = memory_file.read_text(encoding='utf-8')
        
        # 查找最近的 session 摘要
        lines = content.split('\n')
        summary_lines = []
        in_summary = False
        
        for line in lines:
            if '【Session 摘要】' in line or '【会话摘要】' in line:
                in_summary = True
                summary_lines = [line]
            elif in_summary:
                if line.startswith('【') or line.startswith('##'):
                    break
                summary_lines.append(line)
        
        if summary_lines:
            return '\n'.join(summary_lines)
        
        # 如果没有找到摘要，返回最后 20 行
        return '\n'.join(lines[-20:])
    
    except Exception as e:
        print(f"读取记忆文件失败: {e}")
        return None


def generate_handoff_context(channel=None):
    """
    生成 session 交接上下文
    
    Args:
        channel: 频道名称（可选）
    
    Returns:
        str: 交接上下文文本
    """
    memory_files = get_recent_memory_files(days=2)
    
    if not memory_files:
        return "没有找到最近的记忆文件。"
    
    context_parts = ["# Session 交接上下文\n"]
    
    for memory_file in memory_files:
        date = memory_file.stem
        context_parts.append(f"\n## {date} 的记忆摘要\n")
        
        summary = extract_session_summary(memory_file)
        if summary:
            context_parts.append(summary)
        else:
            context_parts.append("（无摘要）")
    
    # 如果指定了频道，添加频道相关的记忆
    if channel:
        context_parts.append(f"\n## {channel} 频道相关记忆\n")
        context_parts.append(f"（从记忆文件中筛选 channel={channel} 的条目）")
    
    return '\n'.join(context_parts)


def save_handoff_context(context, output_file=None):
    """
    保存交接上下文到文件
    
    Args:
        context: 交接上下文文本
        output_file: 输出文件路径（可选）
    """
    if output_file is None:
        workspace = get_workspace_root()
        output_file = workspace / "memory" / "session_handoff.md"
    
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(context, encoding='utf-8')
    
    print(f"✅ 交接上下文已保存到: {output_file}")


def compress_current_session():
    """
    压缩当前 session 的内容
    
    这个函数应该在检测到 [NEW_SESSION] 标记时调用
    """
    workspace = get_workspace_root()
    memory_dir = workspace / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    memory_file = memory_dir / f"{today}.md"
    
    # 生成 session 摘要
    summary = f"""
【Session 摘要】切换新会话前的压缩
时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
触发原因：检测到 [NEW_SESSION] 标记
关键信息：
- （这里应该由 LLM 生成当前 session 的关键信息摘要）
- （包括：完成的任务、做出的决策、遇到的问题、待办事项）
检索标签：#session #压缩 #交接
<!-- meta: importance=8 access=0 created={today} last_accessed={today} channel=auto -->
"""
    
    # 追加到记忆文件
    with open(memory_file, 'a', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"✅ Session 摘要已写入: {memory_file}")
    
    return summary


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "compress":
            # 压缩当前 session
            compress_current_session()
        
        elif command == "handoff":
            # 生成交接上下文
            channel = sys.argv[2] if len(sys.argv) > 2 else None
            context = generate_handoff_context(channel)
            save_handoff_context(context)
            print(context)
        
        else:
            print(f"未知命令: {command}")
            print("用法: python session_handoff.py [compress|handoff] [channel]")
    
    else:
        # 默认：生成交接上下文
        context = generate_handoff_context()
        print(context)
