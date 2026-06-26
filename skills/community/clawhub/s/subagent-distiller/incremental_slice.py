#!/usr/bin/env python3
"""
incremental_slice.py - 增量切片器 v3.0

核心改进：
- 不再全量扫描所有 jsonl
- 使用 cursor 记录上次处理位置
- 只读取新增行
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

# 路径配置
WORKSPACE = Path("/home/aqukin/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills/subagent-distiller"
CHUNKS_DIR = SKILL_DIR / "chunks"
CURSORS_DIR = SKILL_DIR / "cursors"
SESSIONS_DIR = Path("/home/aqukin/.openclaw/agents/main/sessions")

def ensure_dirs():
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    CURSORS_DIR.mkdir(parents=True, exist_ok=True)

def get_cursor_path(session_file):
    """获取 cursor 文件路径"""
    # 处理 .jsonl.reset.2026-03-05... 等变体
    base_name = session_file.name.split('.jsonl')[0]
    return CURSORS_DIR / f"{base_name}.cursor"

def read_cursor(cursor_path):
    """读取 cursor（上次处理到的行号）"""
    if cursor_path.exists():
        try:
            with open(cursor_path, 'r') as f:
                data = json.load(f)
                return data.get('line', 0), data.get('mtime', 0)
        except:
            return 0, 0
    return 0, 0

def write_cursor(cursor_path, line, mtime):
    """写入 cursor"""
    with open(cursor_path, 'w') as f:
        json.dump({'line': line, 'mtime': mtime, 'updated': datetime.now().isoformat()}, f)

def get_session_files():
    """获取所有会话文件（包括 .jsonl, .reset.*, .deleted.*）"""
    files = []
    if SESSIONS_DIR.exists():
        for f in SESSIONS_DIR.glob('*.jsonl'):
            files.append(f)
        for f in SESSIONS_DIR.glob('*.jsonl.reset.*'):
            files.append(f)
        for f in SESSIONS_DIR.glob('*.jsonl.deleted.*'):
            files.append(f)
    return sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)

def count_lines(filepath):
    """计算文件总行数"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except:
        return 0

def get_file_mtime(filepath):
    """获取文件修改时间"""
    try:
        return filepath.stat().st_mtime
    except:
        return 0

def read_new_lines(filepath, start_line, end_line):
    """读取指定行范围的内容"""
    lines = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                if i >= start_line and i < end_line:
                    lines.append(line)
                if i >= end_line:
                    break
    except Exception as e:
        print(f"  读取文件失败 {filepath}: {e}")
    return lines

def create_slice(session_file, start_line, end_line, content_lines):
    """创建切片文件"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    slice_name = f"slice_{session_file.stem}_{start_line}_{end_line}_{timestamp}.json"
    slice_path = CHUNKS_DIR / slice_name
    
    # 组装切片内容
    content = ''.join(content_lines)
    
    slice_data = {
        'source': str(session_file),
        'source_name': session_file.name,
        'start_line': start_line,
        'end_line': end_line,
        'timestamp': timestamp,
        'content': content,
        'line_count': len(content_lines)
    }
    
    with open(slice_path, 'w', encoding='utf-8') as f:
        json.dump(slice_data, f, indent=2, ensure_ascii=False)
    
    return slice_path

def should_process_file(session_file):
    """判断是否应该处理该文件"""
    # 跳过系统文件
    if session_file.name.startswith('.'):
        return False
    
    # 检查文件大小（跳过空文件）
    try:
        if session_file.stat().st_size == 0:
            return False
    except:
        return False
    
    return True

def main():
    print("🌙 增量切片器 v3.0")
    print("=" * 50)
    
    ensure_dirs()
    
    session_files = get_session_files()
    if not session_files:
        print("没有找到会话文件")
        return
    
    print(f"发现 {len(session_files)} 个会话文件")
    print()
    
    total_new_lines = 0
    total_slices = 0
    processed_files = []
    
    for session_file in session_files:
        if not should_process_file(session_file):
            continue
        
        print(f"📄 {session_file.name}")
        
        # 读取 cursor
        cursor_path = get_cursor_path(session_file)
        last_line, last_mtime = read_cursor(cursor_path)
        current_mtime = get_file_mtime(session_file)
        
        # 检查文件是否被修改过
        if current_mtime == last_mtime and last_line > 0:
            print(f"   ⏭️  文件未修改，上次处理到第 {last_line} 行")
            continue
        
        # 计算当前总行数
        total_lines = count_lines(session_file)
        
        if total_lines == 0:
            print(f"   ⚠️  空文件或无法读取")
            continue
        
        if total_lines <= last_line:
            print(f"   ✅ 无新增内容（总 {total_lines} 行，已处理 {last_line} 行）")
            # 更新 mtime，避免重复检查
            write_cursor(cursor_path, last_line, current_mtime)
            continue
        
        new_lines = total_lines - last_line
        print(f"   🆕 发现 {new_lines} 行新内容（总 {total_lines} 行，已处理 {last_line} 行）")
        
        # 读取新增行
        content_lines = read_new_lines(session_file, last_line, total_lines)
        
        if not content_lines:
            print(f"   ⚠️  读取新内容失败")
            continue
        
        # 创建切片（每 50 行一个切片，可根据需要调整）
        SLICE_SIZE = 50
        for i in range(0, len(content_lines), SLICE_SIZE):
            chunk_lines = content_lines[i:i+SLICE_SIZE]
            slice_start = last_line + i
            slice_end = slice_start + len(chunk_lines)
            
            slice_path = create_slice(session_file, slice_start, slice_end, chunk_lines)
            total_slices += 1
            print(f"   ✂️  创建切片: {slice_path.name} ({len(chunk_lines)} 行)")
        
        # 更新 cursor
        write_cursor(cursor_path, total_lines, current_mtime)
        
        total_new_lines += new_lines
        processed_files.append({
            'file': session_file.name,
            'new_lines': new_lines,
            'slices': (new_lines + SLICE_SIZE - 1) // SLICE_SIZE
        })
        print()
    
    # 输出总结
    print("=" * 50)
    print(f"✅ 增量切片完成")
    print(f"   新内容行数: {total_new_lines}")
    print(f"   生成切片数: {total_slices}")
    print(f"   处理文件数: {len(processed_files)}")
    print()
    
    if processed_files:
        print("详细报告:")
        for pf in processed_files:
            print(f"   {pf['file']}: +{pf['new_lines']} 行 → {pf['slices']} 个切片")
    
    # 保存摘要
    summary = {
        'timestamp': datetime.now().isoformat(),
        'total_new_lines': total_new_lines,
        'total_slices': total_slices,
        'processed_files': processed_files
    }
    
    summary_path = SKILL_DIR / 'slice_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n摘要已保存到: {summary_path}")
    
    # 如果有新切片，提示下一步
    if total_slices > 0:
        print("\n🚀 下一步: 运行 realtime_distill.py 进行实时结构化提取")

if __name__ == '__main__':
    main()