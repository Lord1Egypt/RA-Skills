#!/usr/bin/env python3
"""
Zen Koan Daily - Main generation script
Generates daily koan lecture with image and audio
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Paths
SKILL_DIR = Path(__file__).parent.parent
KOANS_FILE = SKILL_DIR / "references" / "koans.json"
PROGRESS_FILE = SKILL_DIR / "references" / "progress.json"
OUTPUT_DIR = Path.home() / ".openclaw" / "media" / "outbound" / "zen-koan"

def load_koans():
    """Load koan database"""
    with open(KOANS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)['koans']

def load_progress():
    """Load progress tracker"""
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_progress(progress):
    """Save progress tracker"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def get_next_koan(koans, progress):
    """Get next koan in sequence (循环)"""
    total = len(koans)
    last_id = progress.get('last_koan_id', 0)
    
    # Find next koan (循环到第一则如果已完成所有)
    next_id = (last_id % total) + 1
    
    # Find koan by ID
    for koan in koans:
        if koan['id'] == next_id:
            return koan
    
    # Fallback to first koan
    return koans[0]

def format_lecture(koan, lang='zh', personal_insight=None):
    """Format koan lecture text"""
    if lang == 'zh':
        lecture = f"""🎋 每日禅宗公案 | Daily Zen Koan

━━━━━━━━━━━━━━━━━

**{koan['title_zh']}**
*{koan['collection']} 第{koan.get('case_number', '—')}则*

━━━━━━━━━━━━━━━━━

📜 **原文**

{koan['text_zh']}

━━━━━━━━━━━━━━━━━

📖 **背景**

{koan['background_zh']}

━━━━━━━━━━━━━━━━━

💡 **白话解读**

{koan['interpretation_zh']}

━━━━━━━━━━━━━━━━━

🌏 **现代启示**

{koan['modern_insight_zh']}
"""
        
        # Add personal insight if provided
        if personal_insight:
            lecture += f"""

━━━━━━━━━━━━━━━━━

🧘 **为你而讲**

{personal_insight}
"""
    
    else:  # English
        lecture = f"""🎋 Daily Zen Koan | 每日禅宗公案

━━━━━━━━━━━━━━━━━

**{koan['title_en']}**
*{koan['collection_en']}{' Case ' + str(koan['case_number']) if koan.get('case_number') else ''}*

━━━━━━━━━━━━━━━━━

📜 **The Koan**

{koan['text_en']}

━━━━━━━━━━━━━━━━━

📖 **Background**

{koan['background_en']}

━━━━━━━━━━━━━━━━━

💡 **Interpretation**

{koan['interpretation_en']}

━━━━━━━━━━━━━━━━━

🌏 **Modern Insight**

{koan['modern_insight_en']}
"""
        
        # Add personal insight if provided
        if personal_insight:
            lecture += f"""

━━━━━━━━━━━━━━━━━

🧘 **For You Today**

{personal_insight}
"""
    
    return lecture

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate daily Zen koan')
    parser.add_argument('--next', action='store_true', help='Get next koan in sequence')
    parser.add_argument('--id', type=int, help='Get specific koan by ID')
    parser.add_argument('--lang', choices=['zh', 'en', 'both'], default='zh', help='Language')
    parser.add_argument('--personal', type=str, help='Personal insight based on recent context')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    # Load data
    koans = load_koans()
    progress = load_progress()
    
    # Select koan
    if args.id:
        koan = next((k for k in koans if k['id'] == args.id), koans[0])
    elif args.next:
        koan = get_next_koan(koans, progress)
    else:
        koan = get_next_koan(koans, progress)
    
    # Output
    if args.format == 'json':
        print(json.dumps(koan, indent=2, ensure_ascii=False))
    else:
        if args.lang == 'both':
            print(format_lecture(koan, 'zh', args.personal))
            print("\n" + "="*50 + "\n")
            print(format_lecture(koan, 'en', args.personal))
        else:
            print(format_lecture(koan, args.lang, args.personal))
    
    # Update progress if --next
    if args.next:
        progress['last_koan_id'] = koan['id']
        progress['last_date'] = datetime.now().isoformat()
        if koan['id'] not in progress['completed_koans']:
            progress['completed_koans'].append(koan['id'])
        save_progress(progress)
        
        # Print metadata to stderr for scripting
        print(f"\n[Progress: {len(progress['completed_koans'])}/{len(koans)} koans completed]", 
              file=sys.stderr)

if __name__ == '__main__':
    main()
