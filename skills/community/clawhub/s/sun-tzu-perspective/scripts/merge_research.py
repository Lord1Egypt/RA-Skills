#!/usr/bin/env python3
# 调研结果合并脚本
# 自动扫描 references/research/ 目录，统计调研质量

import os
import re
from pathlib import Path

def count_sources(file_path):
    """统计文件中的引用数量"""
    if not os.path.exists(file_path):
        return 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单统计URL引用数量
    urls = re.findall(r'https?://[^\s]+', content)
    return len(set(urls))

def analyze_research(skill_dir):
    research_dir = Path(skill_dir) / "references" / "research"
    
    if not research_dir.exists():
        print(f"错误: {research_dir} 不存在")
        return
    
    files = sorted(research_dir.glob("*.md"))
    
    print("\n" + "="*80)
    print("调研质量摘要")
    print("="*80)
    print(f"{'Agent':<20} {'来源数量':<12} {'文件大小':<12} {'关键发现'}")
    print("-"*80)
    
    total_sources = 0
    for file in files:
        stat = os.stat(file)
        sources = count_sources(file)
        total_sources += sources
        print(f"{file.stem:<20} {sources:<12} {stat.st_size:<12} {'[已生成']}")
    
    print("-"*80)
    print(f"{'总计':<20} {total_sources:<12}")
    print("="*80 + "\n")

if __name__ == "__main__":
    analyze_research(".")
