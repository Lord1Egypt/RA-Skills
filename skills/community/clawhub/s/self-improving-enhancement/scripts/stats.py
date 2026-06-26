#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Self-Improving Enhancement - 记忆统计工具
显示记忆使用情况和统计数据
"""

import sys
import json
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def count_lines(file_path):
    """计算文件行数（非空行）"""
    if not file_path.exists():
        return 0
    with open(file_path, 'r', encoding='utf-8') as f:
        return sum(1 for line in f if line.strip() and not line.strip().startswith('#'))


def show_stats():
    """显示记忆统计"""
    base_dir = Path.home() / "self-improving"
    
    print("=" * 60)
    print("📊 Self-Improving Enhancement 记忆统计")
    print("=" * 60)
    print()
    
    # HOT 记忆
    memory_md = base_dir / "memory.md"
    memory_lines = count_lines(memory_md)
    print(f"HOT 记忆：{memory_lines} 行")
    
    # WARM 记忆
    projects_dir = base_dir / "projects"
    domains_dir = base_dir / "domains"
    
    project_files = list(projects_dir.glob("*.md")) if projects_dir.exists() else []
    domain_files = list(domains_dir.glob("*.md")) if domains_dir.exists() else []
    
    project_lines = sum(count_lines(f) for f in project_files)
    domain_lines = sum(count_lines(f) for f in domain_files)
    
    print(f"WARM 记忆：{project_lines + domain_lines} 行")
    print(f"  - 项目记忆：{len(project_files)} 个文件，{project_lines} 行")
    print(f"  - 领域记忆：{len(domain_files)} 个文件，{domain_lines} 行")
    
    # COLD 记忆
    archive_dir = base_dir / "archive"
    archive_files = list(archive_dir.glob("*.md")) if archive_dir.exists() else []
    archive_lines = sum(count_lines(f) for f in archive_files)
    
    print(f"COLD 记忆：{archive_lines} 行 ({len(archive_files)} 个文件)")
    
    # 纠正记录
    corrections_md = base_dir / "corrections.md"
    corrections_lines = count_lines(corrections_md)
    print(f"纠正记录：{corrections_lines} 行")
    
    # 总计
    total_lines = memory_lines + project_lines + domain_lines + archive_lines + corrections_lines
    print()
    print(f"总计：{total_lines} 行")
    print("=" * 60)


if __name__ == "__main__":
    show_stats()
