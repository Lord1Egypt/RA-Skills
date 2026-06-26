#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Self-Improving Enhancement - Memory Visualization
Creates visual charts of memory usage and learning trends
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def count_lines(file_path):
    """Count non-empty lines"""
    if not file_path.exists():
        return 0
    with open(file_path, 'r', encoding='utf-8') as f:
        return sum(1 for line in f if line.strip())


def visualize(base_dir):
    """Create visual memory stats"""
    print("=" * 60)
    print("📊 Self-Improving Enhancement - Memory Visualization")
    print("=" * 60)
    print()
    
    # Count memory files
    memory_lines = count_lines(base_dir / "memory.md")
    corrections_lines = count_lines(base_dir / "corrections.md")
    
    # Count project files
    projects_dir = base_dir / "projects"
    project_files = list(projects_dir.glob("*.md")) if projects_dir.exists() else []
    project_lines = sum(count_lines(f) for f in project_files)
    
    # Count domain files
    domains_dir = base_dir / "domains"
    domain_files = list(domains_dir.glob("*.md")) if domains_dir.exists() else []
    domain_lines = sum(count_lines(f) for f in domain_files)
    
    # Count archive files
    archive_dir = base_dir / "archive"
    archive_files = list(archive_dir.glob("*.md")) if archive_dir.exists() else []
    archive_lines = sum(count_lines(f) for f in archive_files)
    
    # Calculate totals
    total = memory_lines + corrections_lines + project_lines + domain_lines + archive_lines
    
    # Visual bars
    def bar(value, max_value, width=30):
        if max_value == 0:
            return ""
        filled = int((value / max_value) * width)
        return "█" * filled + "░" * (width - filled)
    
    max_lines = max(memory_lines, corrections_lines, project_lines, domain_lines, archive_lines, 1)
    
    print("Memory Distribution:")
    print()
    
    print(f"  HOT (memory.md)")
    print(f"  {bar(memory_lines, max_lines)} {memory_lines} entries")
    print()
    
    print(f"  Corrections")
    print(f"  {bar(corrections_lines, max_lines)} {corrections_lines} entries")
    print()
    
    print(f"  WARM (projects/)")
    print(f"  {bar(project_lines, max_lines)} {project_lines} entries ({len(project_files)} files)")
    print()
    
    print(f"  WARM (domains/)")
    print(f"  {bar(domain_lines, max_lines)} {domain_lines} entries ({len(domain_files)} files)")
    print()
    
    print(f"  COLD (archive/)")
    print(f"  {bar(archive_lines, max_lines)} {archive_lines} entries ({len(archive_files)} files)")
    print()
    
    print("-" * 60)
    print(f"  TOTAL: {total} entries")
    print()
    
    # Usage efficiency
    print("Usage Efficiency:")
    print()
    
    if total > 0:
        hot_pct = (memory_lines / total) * 100
        warm_pct = ((project_lines + domain_lines) / total) * 100
        cold_pct = (archive_lines / total) * 100
        corrections_pct = (corrections_lines / total) * 100
        
        print(f"  HOT (active):     {hot_pct:5.1f}%  ████████████████████")
        print(f"  Corrections:      {corrections_pct:5.1f}%  ████████████████████")
        print(f"  WARM (learning):  {warm_pct:5.1f}%  ████████████████████")
        print(f"  COLD (archived):  {cold_pct:5.1f}%  ████████████████████")
    
    print()
    
    # Health score
    print("Memory Health:")
    print()
    
    health_score = 100
    
    if memory_lines > 100:
        health_score -= 20
        print("  ⚠️  HOT memory exceeds 100 lines")
    
    if corrections_lines > 50:
        health_score -= 10
        print("  ⚠️  Many unprocessed corrections")
    
    if archive_lines == 0 and total > 50:
        health_score -= 5
        print("  ℹ️  No archived entries (consider archiving old items)")
    
    if health_score >= 90:
        print(f"  ✓ Health Score: {health_score}/100 (Excellent)")
    elif health_score >= 70:
        print(f"  ✓ Health Score: {health_score}/100 (Good)")
    else:
        print(f"  ⚠️  Health Score: {health_score}/100 (Needs attention)")
    
    print()
    print("=" * 60)


def main():
    base_dir = Path.home() / "self-improving"
    visualize(base_dir)


if __name__ == "__main__":
    main()
