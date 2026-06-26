#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Self-Improving Enhancement - Weekly Review
Generates weekly learning reports and suggests actions
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def load_stats(base_dir):
    """Load heartbeat state"""
    heartbeat_json = base_dir / "heartbeat-state.json"
    if not heartbeat_json.exists():
        return {}
    
    with open(heartbeat_json, 'r', encoding='utf-8') as f:
        return json.load(f)


def count_lines(file_path):
    """Count non-empty lines"""
    if not file_path.exists():
        return 0
    with open(file_path, 'r', encoding='utf-8') as f:
        return sum(1 for line in f if line.strip())


def generate_review(base_dir):
    """Generate weekly review"""
    print("=" * 60)
    print("📈 Weekly Learning Review")
    print("=" * 60)
    print()
    
    # Load stats
    stats = load_stats(base_dir)
    
    # Count memory files
    memory_lines = count_lines(base_dir / "memory.md")
    corrections_lines = count_lines(base_dir / "corrections.md")
    
    # Count project files
    projects_dir = base_dir / "projects"
    project_count = len(list(projects_dir.glob("*.md"))) if projects_dir.exists() else 0
    
    # Count domain files
    domains_dir = base_dir / "domains"
    domain_count = len(list(domains_dir.glob("*.md"))) if domains_dir.exists() else 0
    
    # Count archive files
    archive_dir = base_dir / "archive"
    archive_count = len(list(archive_dir.glob("*.md"))) if archive_dir.exists() else 0
    
    print(f"Week of {datetime.now().strftime('%Y-%m-%d')}")
    print()
    
    print("📊 Memory Statistics:")
    print()
    print(f"  HOT Memory:    {memory_lines} entries")
    print(f"  Corrections:   {corrections_lines} entries")
    print(f"  Projects:      {project_count} files")
    print(f"  Domains:       {domain_count} files")
    print(f"  Archived:      {archive_count} files")
    print()
    
    total = memory_lines + corrections_lines
    print(f"  Total:         {total} entries")
    print()
    
    # Activity summary
    print("📝 Activity Summary:")
    print()
    
    last_review = stats.get("lastReview")
    if last_review:
        print(f"  Last review:   {last_review}")
    else:
        print(f"  Last review:   First review")
    
    total_corrections = stats.get("totalCorrections", 0)
    print(f"  Total corrections logged: {total_corrections}")
    
    total_promotions = stats.get("totalPromotions", 0)
    print(f"  Total promotions to HOT:  {total_promotions}")
    print()
    
    # Recommendations
    print("💡 Recommendations:")
    print()
    
    if corrections_lines > 20:
        print("  ⚠️  Many corrections - consider running compact.py")
    
    if memory_lines > 80:
        print("  ⚠️  HOT memory is large - consider archiving unused entries")
    
    if corrections_lines > 0 and corrections_lines <= 20:
        print("  ✓ Good progress - keep collecting corrections")
    
    if memory_lines > 0 and memory_lines <= 80:
        print("  ✓ HOT memory size is healthy")
    
    print()
    
    # Suggested actions
    print("🎯 Suggested Actions:")
    print()
    
    actions = []
    
    if corrections_lines >= 5:
        actions.append("Run compact.py to merge similar entries")
    
    if memory_lines >= 50:
        actions.append("Review HOT memory and archive unused entries")
    
    if project_count == 0 and corrections_lines > 10:
        actions.append("Consider organizing by project (projects/)")
    
    if domain_count == 0 and corrections_lines > 10:
        actions.append("Consider organizing by domain (domains/)")
    
    if not actions:
        actions.append("Continue normal usage - no action needed")
    
    for i, action in enumerate(actions, 1):
        print(f"  {i}. {action}")
    
    print()
    print("=" * 60)
    
    # Update stats
    stats["lastReview"] = datetime.now().isoformat()
    
    heartbeat_json = base_dir / "heartbeat-state.json"
    with open(heartbeat_json, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print()
    print("✓ Review state updated")


def main():
    base_dir = Path.home() / "self-improving"
    
    weekly = "--weekly" in sys.argv
    generate_review(base_dir)


if __name__ == "__main__":
    main()
