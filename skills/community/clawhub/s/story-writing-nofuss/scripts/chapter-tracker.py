#!/usr/bin/env python3
"""
Chapter and word count tracker for story writing.
Calculates per-chapter targets and tracks progress.
"""

import argparse
import json
import sys
from pathlib import Path

# Handle Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def calculate_targets(total_chapters: int, total_words: int) -> dict:
    """Calculate per-chapter word count targets."""
    avg_per_chapter = total_words / total_chapters
    return {
        "total_chapters": total_chapters,
        "total_words_target": total_words,
        "avg_words_per_chapter": round(avg_per_chapter),
        "act_breakdown": {
            "act1_chapters": max(1, round(total_chapters * 0.25)),
            "act2_chapters": max(1, round(total_chapters * 0.50)),
            "act3_chapters": max(1, round(total_chapters * 0.25)),
        }
    }


def track_progress(total_chapters: int, total_words: int, 
                   completed: int, written: int) -> dict:
    """Track writing progress and calculate remaining targets."""
    targets = calculate_targets(total_chapters, total_words)
    
    remaining_chapters = total_chapters - completed
    remaining_words = total_words - written
    
    if remaining_chapters > 0:
        needed_avg = remaining_words / remaining_chapters
    else:
        needed_avg = 0
    
    chapter_pct = (completed / total_chapters) * 100
    word_pct = (written / total_words) * 100
    on_track = word_pct >= chapter_pct
    
    return {
        **targets,
        "chapters_completed": completed,
        "chapters_remaining": remaining_chapters,
        "words_written": written,
        "words_remaining": remaining_words,
        "needed_avg_per_chapter": round(needed_avg),
        "chapter_progress_pct": round(chapter_pct, 1),
        "word_progress_pct": round(word_pct, 1),
        "on_track": on_track,
        "variance": round(word_pct - chapter_pct, 1)
    }


def print_report(progress: dict, is_tracking: bool = False):
    """Print a formatted progress report."""
    print("\n" + "=" * 50)
    print("📖 STORY PROGRESS REPORT")
    print("=" * 50)
    print(f"\nTarget: {progress['total_chapters']} chapters, {progress['total_words_target']:,} words")
    print(f"Average per chapter: {progress['avg_words_per_chapter']:,} words")
    
    if is_tracking:
        print(f"\n✅ Completed: {progress['chapters_completed']}/{progress['total_chapters']} chapters ({progress['chapter_progress_pct']}%)")
        print(f"📝 Written: {progress['words_written']:,}/{progress['total_words_target']:,} words ({progress['word_progress_pct']}%)")
        
        if progress['on_track']:
            print(f"\n✓ On track! (+{progress['variance']}% variance)")
        else:
            print(f"\n⚠ Behind target ({progress['variance']}% variance)")
        
        print(f"\nRemaining: {progress['chapters_remaining']} chapters, {progress['words_remaining']:,} words")
        print(f"Needed average: {progress['needed_avg_per_chapter']:,} words/chapter")
    else:
        print(f"\n📊 Planning mode - use --completed and --written to track progress")
    
    print(f"\n--- Three-Act Breakdown ---")
    acts = progress['act_breakdown']
    print(f"Act 1 (Setup): ~{acts['act1_chapters']} chapters")
    print(f"Act 2 (Confrontation): ~{acts['act2_chapters']} chapters")
    print(f"Act 3 (Resolution): ~{acts['act3_chapters']} chapters")
    print("=" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Track story writing progress")
    parser.add_argument("--chapters", type=int, required=True, help="Total chapters planned")
    parser.add_argument("--target", type=int, required=True, help="Total word count target")
    parser.add_argument("--completed", type=int, default=0, help="Chapters completed")
    parser.add_argument("--written", type=int, default=0, help="Words written so far")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    is_tracking = args.completed > 0 or args.written > 0
    
    if is_tracking:
        report = track_progress(args.chapters, args.target, args.completed, args.written)
    else:
        report = calculate_targets(args.chapters, args.target)
    
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report, is_tracking)


if __name__ == "__main__":
    main()
