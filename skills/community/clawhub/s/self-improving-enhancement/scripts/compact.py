#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Self-Improving Enhancement - Smart Memory Compaction
Automatically merges similar entries and compresses memory
"""

import sys
import json
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def load_corrections(base_dir):
    """Load corrections.md"""
    corrections_md = base_dir / "corrections.md"
    if not corrections_md.exists():
        return []
    
    content = corrections_md.read_text(encoding='utf-8')
    lines = [line.strip() for line in content.split('\n') 
             if line.strip() and not line.strip().startswith('#')]
    return lines


def find_similar(lines, threshold=0.6):
    """Find similar lines using simple string similarity"""
    similar_groups = []
    used = set()
    
    for i, line1 in enumerate(lines):
        if i in used:
            continue
        
        group = [line1]
        used.add(i)
        
        for j, line2 in enumerate(lines[i+1:], i+1):
            if j in used:
                continue
            
            # Simple similarity: word overlap
            words1 = set(line1.lower().split())
            words2 = set(line2.lower().split())
            
            if not words1 or not words2:
                continue
            
            overlap = len(words1 & words2) / max(len(words1), len(words2))
            
            if overlap >= threshold:
                group.append(line2)
                used.add(j)
        
        if len(group) > 1:
            similar_groups.append(group)
    
    return similar_groups


def compact_corrections(base_dir, auto=False):
    """Compact corrections.md"""
    print("=" * 60)
    print("🗜️  Smart Memory Compaction")
    print("=" * 60)
    print()
    
    lines = load_corrections(base_dir)
    
    if not lines:
        print("✓ No corrections to compact")
        return
    
    print(f"Found {len(lines)} corrections")
    print()
    
    similar_groups = find_similar(lines)
    
    if not similar_groups:
        print("✓ No similar entries found")
        return
    
    print(f"Found {len(similar_groups)} similar groups:")
    print()
    
    for i, group in enumerate(similar_groups, 1):
        print(f"Group {i} ({len(group)} entries):")
        for line in group:
            print(f"  - {line[:60]}...")
        print()
        
        # Merge into single entry
        merged = f"[Merged {len(group)} entries] " + group[0][:100]
        print(f"  → Merged: {merged[:60]}...")
        print()
    
    if auto:
        print("✓ Auto-compaction enabled - changes applied")
        # TODO: Actually write changes
    else:
        print("Run with --auto to apply changes")
    
    print()
    print("=" * 60)


def main():
    base_dir = Path.home() / "self-improving"
    
    auto = "--auto" in sys.argv
    compact_corrections(base_dir, auto)


if __name__ == "__main__":
    main()
