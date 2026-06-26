#!/usr/bin/env python3
"""
Project Status Checker
Shows current status of story writing project.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Handle Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def check_project_status(project_dir="."):
    """Check status of story writing project."""
    
    project_dir = Path(project_dir)
    
    status = {
        'stage': 0,
        'stage_name': 'Not Started',
        'files': {},
        'progress': {},
        'next_step': 'Start discovery process'
    }
    
    # Check for discovery file
    discovery_files = list(project_dir.glob("discovery*.json"))
    if discovery_files:
        status['files']['discovery'] = discovery_files[0].name
        status['stage'] = 1
        status['stage_name'] = 'Discovery Complete'
        status['next_step'] = 'Generate story bible'
    
    # Check for story bible
    story_bible_files = list(project_dir.glob("story-bible*.md"))
    if story_bible_files:
        status['files']['story_bible'] = story_bible_files[0].name
        status['stage'] = 2
        status['stage_name'] = 'Story Bible Complete'
        status['next_step'] = 'Generate book bible'
    
    # Check for book bible
    book_bible_files = list(project_dir.glob("book-bible*.md"))
    if book_bible_files:
        status['files']['book_bible'] = book_bible_files[0].name
        status['stage'] = 3
        status['stage_name'] = 'Book Bible Complete'
        status['next_step'] = 'Start drafting chapters'
    
    # Check for chapters
    chapter_dir = project_dir / "chapters"
    if chapter_dir.exists():
        chapter_files = list(chapter_dir.glob("chapter-*.md"))
        if chapter_files:
            status['files']['chapters'] = len(chapter_files)
            status['stage'] = 4
            status['stage_name'] = 'Drafting in Progress'
            
            # Calculate progress
            total_chapters = 0
            total_words = 0
            
            # Try to get target from discovery
            if discovery_files:
                with open(discovery_files[0], 'r', encoding='utf-8') as f:
                    discovery_data = json.load(f)
                    answers = discovery_data.get('answers', {})
                    
                    # Parse chapter count
                    import re
                    chapters_raw = answers.get('scope_chapters', '24 chapters')
                    chapter_match = re.search(r'(\d+)', chapters_raw)
                    total_chapters = int(chapter_match.group(1)) if chapter_match else 24
                    
                    # Parse word count
                    words_raw = answers.get('scope_words', '80,000 words')
                    word_match = re.search(r'([\d,]+)', words_raw)
                    target_words = int(word_match.group(1).replace(',', '')) if word_match else 80000
            
            # Count actual words
            for chapter_file in chapter_files:
                with open(chapter_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    total_words += len(content.split())
            
            status['progress'] = {
                'chapters_completed': len(chapter_files),
                'total_chapters': total_chapters,
                'words_written': total_words,
                'target_words': target_words if 'target_words' in locals() else 0,
                'chapter_percent': (len(chapter_files) / total_chapters * 100) if total_chapters > 0 else 0,
                'word_percent': (total_words / target_words * 100) if 'target_words' in locals() and target_words > 0 else 0
            }
            
            if len(chapter_files) >= total_chapters:
                status['stage'] = 5
                status['stage_name'] = 'Drafting Complete'
                status['next_step'] = 'Review book quality'
    
    # Check for review notes
    review_files = list(project_dir.glob("review-notes*.md"))
    if review_files:
        status['files']['review'] = review_files[0].name
        status['stage'] = 6
        status['stage_name'] = 'Review Complete'
        status['next_step'] = 'Export to HTML'
    
    # Check for export
    export_dir = project_dir / "export"
    if export_dir.exists():
        html_files = list(export_dir.glob("*.html"))
        if html_files:
            status['files']['export'] = html_files[0].name
            status['stage'] = 7
            status['stage_name'] = 'Export Complete'
            status['next_step'] = 'Project complete!'
    
    return status


def print_status(status, verbose=False):
    """Print formatted status report."""
    
    stages = [
        "0. Not Started",
        "1. Discovery Complete",
        "2. Story Bible Complete", 
        "3. Book Bible Complete",
        "4. Drafting in Progress",
        "5. Drafting Complete",
        "6. Review Complete",
        "7. Export Complete"
    ]
    
    print("\n" + "="*60)
    print("📊 STORY PROJECT STATUS")
    print("="*60)
    
    print(f"\nCurrent Stage: {status['stage_name']}")
    print(f"Stage: {status['stage']}/7")
    
    # Show stage progress
    print("\n" + "─"*60)
    print("Pipeline Progress:")
    for i, stage in enumerate(stages):
        marker = "✓" if i <= status['stage'] else "○"
        current = "←" if i == status['stage'] else " "
        print(f"  {marker} {current} {stage}")
    
    # Show files
    if status['files']:
        print("\n" + "─"*60)
        print("Project Files:")
        for file_type, file_info in status['files'].items():
            if file_type == 'chapters':
                print(f"  📁 chapters/ ({file_info} files)")
            else:
                print(f"  📄 {file_info}")
    
    # Show progress if drafting
    if status['progress']:
        print("\n" + "─"*60)
        print("Writing Progress:")
        
        prog = status['progress']
        
        if prog['total_chapters'] > 0:
            chapter_pct = prog['chapter_percent']
            print(f"  Chapters: {prog['chapters_completed']}/{prog['total_chapters']} ({chapter_pct:.1f}%)")
            
            # Progress bar for chapters
            bar_length = 30
            filled = int(bar_length * chapter_pct / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"  [{bar}]")
        
        if prog['target_words'] > 0:
            word_pct = prog['word_percent']
            print(f"  Words: {prog['words_written']:,}/{prog['target_words']:,} ({word_pct:.1f}%)")
            
            # Progress bar for words
            bar_length = 30
            filled = int(bar_length * word_pct / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"  [{bar}]")
            
            # On track?
            if prog['chapters_completed'] > 0 and prog['total_chapters'] > 0:
                expected_words = (prog['chapters_completed'] / prog['total_chapters']) * prog['target_words']
                variance = prog['words_written'] - expected_words
                if variance > 0:
                    print(f"  📈 Ahead by {variance:,} words")
                elif variance < 0:
                    print(f"  📉 Behind by {abs(variance):,} words")
                else:
                    print(f"  📊 Exactly on target")
    
    print("\n" + "─"*60)
    print(f"Next Step: {status['next_step']}")
    print("="*60 + "\n")
    
    # Show commands for next step
    print("Suggested Commands:")
    
    if status['stage'] == 0:
        print("  python scripts/discovery.py")
    elif status['stage'] == 1:
        print(f"  python scripts/story-bible-generator.py --discovery {status['files']['discovery']}")
    elif status['stage'] == 2:
        print(f"  python scripts/book-bible-generator.py --story-bible {status['files']['story_bible']} --discovery {status['files']['discovery']}")
    elif status['stage'] == 3:
        print(f"  python scripts/draft-chapter.py --book-bible {status['files']['book_bible']} --discovery {status['files']['discovery']} --chapter 1")
    elif status['stage'] == 4:
        next_chapter = status['progress']['chapters_completed'] + 1
        print(f"  python scripts/draft-chapter.py --book-bible {status['files']['book_bible']} --discovery {status['files']['discovery']} --chapter {next_chapter}")
    elif status['stage'] == 5:
        print(f"  python scripts/review-book.py --chapters chapters/ --book-bible {status['files']['book_bible']} --discovery {status['files']['discovery']}")
    elif status['stage'] == 6:
        print(f"  python scripts/export-html.py --chapters chapters/ --discovery {status['files']['discovery']}")
    elif status['stage'] == 7:
        print(f"  Project complete! View at: export/{status['files']['export']}")


def main():
    parser = argparse.ArgumentParser(description="Check Story Project Status")
    parser.add_argument("--project-dir", "-p", default=".", help="Project directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Check status
    status = check_project_status(args.project_dir)
    
    if args.json:
        import json as json_module
        print(json_module.dumps(status, indent=2))
    else:
        print_status(status, args.verbose)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())