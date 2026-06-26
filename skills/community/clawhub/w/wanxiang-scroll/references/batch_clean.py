#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
万象绘卷原始草稿内容清洗脚本
规则：
1. 去除行首 "- " 多余前缀
2. 去除 > 注释/ID 元信息头
3. 英文直引号→中文弯引号
4. 多余空行压缩为最多两个换行
5. 代码块(YAML)内容不处理
"""

import re
import os
import sys
import glob

BASE_DIR = r"D:\openclaw\.openclaw\workspace\skills\wanxiang-scroll\references"

# 需要清洗的目录（不含原始草稿和ch11）
TARGET_DIRS = [
    "ch01-核心系统", "ch02-文风系统", "ch03-互动故事",
    "ch04-剧情管理", "ch05-创作引擎", "ch06-网文创作",
    "ch07-质量控制", "ch08-辅助工具", "ch09-角色设定",
    "ch10-拆书融合", "ch12-李诞七步", "ch13-人生模拟",
]

# 排除的文件（非原始草稿，已经是干净格式）
EXCLUDE_PREFIXES = ["01-world-building", "02-world-rules", "03-interaction-reference",
                     "01-style-library", "02-style-details", "03-style-details",
                     "04-style-details", "05-style-details",
                     "01-quick-start", "02-core-mechanics",
                     "01-plot-control", "01-apex-engine", "02-direct-telling",
                     "01-workflow", "02-content-generation", "03-platform-adaptation",
                     "04-zhihu-guide", "05-novel-outline-reference",
                     "01-quality-standard", "02-editor-techniques", "03-ai-trace-removal",
                     "01-character-tools", "02-novel-tools", "03-advanced-techniques",
                     "04-bomb-theory", "01-personality-system", "02-output-guidelines",
                     "03-quality-control", "04-creative-tools",
                     "01-workflow-guide", "02-templates", "03-quality-and-rules",
                     "cognitive-bias-demo",
                     "01-world-gen", "02-character", "03-event-system",
                     "04-action", "05-time-system", "06-legacy", "07-novel-gen"]


def is_excluded(filename):
    for prefix in EXCLUDE_PREFIXES:
        if filename.startswith(prefix):
            return True
    return False


def clean_text(text):
    """清洗文本内容"""
    result = []
    in_code_block = False
    
    for line in text.split('\n'):
        # 跟踪代码块状态
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue
        
        if in_code_block:
            result.append(line)
            continue
        
        # 规则2：去除 > 注释/ID 元信息头
        stripped = line.strip()
        if stripped.startswith('> 注释') or stripped.startswith('> ID:'):
            continue
        # 也去除 # 文风配置 重复标题（文件里已有标题）
        # 不去除，保留
        
        # 规则1：去除行首 "- " 前缀
        if re.match(r'^- (.+)$', stripped):
            line = '  ' + stripped[2:]  # 缩进保留层级感
        
        # 规则3：英文直引号→中文弯引号
        if '"' in line and not in_code_block:
            new_line = []
            open_q = True
            for ch in line:
                if ch == '"':
                    new_line.append('\u201c' if open_q else '\u201d')
                    open_q = not open_q
                else:
                    new_line.append(ch)
            line = ''.join(new_line)
        
        result.append(line)
    
    text = '\n'.join(result)
    
    # 规则4：多余空行压缩（3个以上换行→2个）
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    # 清理开头多余空行
    text = text.lstrip('\n')
    
    return text


def process_file(filepath):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    original_len = len(text)
    cleaned = clean_text(text)
    
    if len(cleaned) != original_len:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        return original_len, len(cleaned)
    
    return original_len, original_len


def main():
    total_files = 0
    changed_files = 0
    
    for dirname in TARGET_DIRS:
        dirpath = os.path.join(BASE_DIR, dirname)
        if not os.path.exists(dirpath):
            continue
        
        for filename in sorted(os.listdir(dirpath)):
            if not filename.endswith('.md'):
                continue
            if filename == 'index.md':
                continue
            if is_excluded(filename):
                continue
            
            filepath = os.path.join(dirpath, filename)
            try:
                orig, new = process_file(filepath)
                total_files += 1
                if orig != new:
                    changed_files += 1
                    print(f"[FIX] {dirname}/{filename} {orig}->{new} bytes")
                else:
                    print(f"[OK]  {dirname}/{filename} no change")
            except Exception as e:
                print(f"[ERR] {dirname}/{filename}: {e}")
    
    print(f"\nTotal: {total_files} files, {changed_files} changed")


if __name__ == "__main__":
    main()
