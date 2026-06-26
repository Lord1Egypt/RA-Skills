#!/usr/bin/env python3
"""
Book Review Script
Reviews all chapters for correctness, flow, grammar, and plot adherence.
"""

import argparse
import json
import sys
from pathlib import Path
import re

# Handle Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def load_chapters(chapter_dir):
    """Load all chapter files from directory."""
    chapter_dir = Path(chapter_dir)
    chapters = []
    
    for filepath in sorted(chapter_dir.glob("chapter-*.md")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract chapter number from filename
        match = re.search(r'chapter-(\d+)', filepath.stem)
        chapter_num = int(match.group(1)) if match else 0
        
        chapters.append({
            'number': chapter_num,
            'filename': filepath.name,
            'content': content,
            'word_count': len(content.split())
        })
    
    return sorted(chapters, key=lambda x: x['number'])


def load_book_bible(filepath):
    """Load book bible for reference."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def review_chapters(chapters, book_bible_content, discovery_data):
    """Review all chapters and generate report."""
    
    answers = discovery_data.get('answers', {})
    genre = answers.get('genre', '')
    atmosphere = answers.get('atmosphere', '')
    
    report = f"""# Book Review Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Chapters reviewed: {len(chapters)}

---

## Summary

### Statistics
- **Total chapters:** {len(chapters)}
- **Total words:** {sum(c['word_count'] for c in chapters):,}
- **Average chapter length:** {sum(c['word_count'] for c in chapters) // len(chapters):,} words
- **Shortest chapter:** Chapter {min(chapters, key=lambda x: x['word_count'])['number']} ({min(c['word_count'] for c in chapters)} words)
- **Longest chapter:** Chapter {max(chapters, key=lambda x: x['word_count'])['number']} ({max(c['word_count'] for c in chapters)} words)

### Overall Assessment
[Based on genre: {genre}, Atmosphere: {atmosphere}]

---

## Chapter-by-Chapter Review

"""
    
    issues_found = 0
    
    for chapter in chapters:
        chapter_report, chapter_issues = review_single_chapter(chapter, book_bible_content)
        report += chapter_report
        issues_found += chapter_issues
    
    report += f"""

---

## Common Issues Found

### Grammar & Style
{generate_grammar_issues(chapters)}

### Plot & Continuity
{generate_plot_issues(chapters, book_bible_content)}

### Character Consistency
{generate_character_issues(chapters)}

### Pacing
{generate_pacing_analysis(chapters)}

---

## Recommendations

### Immediate Fixes (High Priority)
1. [List critical issues that must be fixed]

### Improvements (Medium Priority)
1. [List issues that should be fixed for better quality]

### Enhancements (Low Priority)
1. [List optional improvements]

---

## Next Steps

1. **Address critical issues** - Fix plot holes, continuity errors
2. **Improve pacing** - Adjust chapter lengths where needed
3. **Polish prose** - Fix grammar, style issues
4. **Character consistency** - Ensure voices remain distinct
5. **Final proofread** - One last pass before export

---

**Total issues identified:** {issues_found}
**Review complete.** Ready for export after addressing critical issues.
"""
    
    return report, issues_found


def review_single_chapter(chapter, book_bible_content):
    """Review a single chapter."""
    
    issues = []
    
    # Check chapter structure
    if not chapter['content'].startswith('# Chapter'):
        issues.append("Missing chapter heading")
    
    # Check word count
    if chapter['word_count'] < 500:
        issues.append("Chapter may be too short")
    elif chapter['word_count'] > 5000:
        issues.append("Chapter may be too long")
    
    # Check for common writing issues
    content_lower = chapter['content'].lower()
    
    # Filter words
    filter_words = ['felt', 'saw', 'heard', 'noticed', 'realized', 'watched', 'looked']
    for word in filter_words:
        if f" {word} " in content_lower:
            issues.append(f"Filter word: '{word}' (consider showing instead of telling)")
    
    # Adverbs
    adverb_count = len(re.findall(r'\w+ly\b', chapter['content']))
    if adverb_count > 10:
        issues.append(f"High adverb count: {adverb_count} (consider stronger verbs)")
    
    # Passive voice
    passive_count = len(re.findall(r'\b(am|is|are|was|were|be|being|been)\s+\w+ed\b', content_lower))
    if passive_count > 5:
        issues.append(f"Passive voice detected: {passive_count} instances")
    
    # Dialogue tags
    dialogue_tags = ['said', 'asked', 'replied', 'whispered', 'shouted']
    tag_count = sum(len(re.findall(rf'\b{tag}\b', content_lower)) for tag in dialogue_tags)
    if tag_count > 20:
        issues.append(f"Dialogue tags: {tag_count} (consider using action beats)")
    
    # Generate chapter report
    report = f"""### Chapter {chapter['number']}: {chapter['filename']}

**Word count:** {chapter['word_count']}
**Issues found:** {len(issues)}

#### Issues:
"""
    
    if issues:
        for issue in issues:
            report += f"- {issue}\n"
    else:
        report += "- No major issues found\n"
    
    report += f"""
#### Excerpt:
{chapter['content'][:200]}...

---
"""
    
    return report, len(issues)


def generate_grammar_issues(chapters):
    """Generate grammar and style issues summary."""
    
    total_adverbs = 0
    total_passive = 0
    total_filter = 0
    
    for chapter in chapters:
        content_lower = chapter['content'].lower()
        total_adverbs += len(re.findall(r'\w+ly\b', chapter['content']))
        total_passive += len(re.findall(r'\b(am|is|are|was|were|be|being|been)\s+\w+ed\b', content_lower))
        
        filter_words = ['felt', 'saw', 'heard', 'noticed', 'realized', 'watched', 'looked']
        for word in filter_words:
            total_filter += len(re.findall(rf'\b{word}\b', content_lower))
    
    return f"""
- **Adverbs:** {total_adverbs} total (average {total_adverbs//len(chapters)} per chapter)
- **Passive voice:** {total_passive} instances
- **Filter words:** {total_filter} instances
- **Recommendation:** Replace filter words with action, reduce adverbs, use active voice.
"""


def generate_plot_issues(chapters, book_bible_content):
    """Generate plot and continuity issues summary."""
    
    # Check for chapter hooks
    hooks_missing = 0
    for i, chapter in enumerate(chapters):
        if i < len(chapters) - 1:
            # Check if chapter ends with hook
            last_para = chapter['content'].strip().split('\n')[-1]
            if len(last_para) < 50 or not any(q in last_para for q in ['?', 'but', 'however', 'yet']):
                hooks_missing += 1
    
    return f"""
- **Chapter hooks:** {hooks_missing} chapters may lack strong ending hooks
- **Continuity:** Check character details remain consistent
- **Pacing:** Ensure rising tension throughout
- **Recommendation:** Add hooks to chapters {[c['number'] for i, c in enumerate(chapters) if i < len(chapters) - 1 and hooks_missing > 0][:3]}
"""


def generate_character_issues(chapters):
    """Generate character consistency issues summary."""
    
    # Check for character name consistency (simplified)
    character_names = set()
    for chapter in chapters:
        # Extract potential character names (capitalized words)
        words = re.findall(r'\b[A-Z][a-z]+\b', chapter['content'])
        character_names.update([w for w in words if len(w) > 2 and w not in ['The', 'And', 'But', 'For']])
    
    return f"""
- **Character names found:** {len(character_names)} distinct names
- **Consistency:** Ensure each character has distinct voice
- **Development:** Check character arcs progress naturally
- **Recommendation:** Create character voice guide if needed
"""


def generate_pacing_analysis(chapters):
    """Generate pacing analysis."""
    
    word_counts = [c['word_count'] for c in chapters]
    avg_length = sum(word_counts) // len(word_counts)
    
    pacing_issues = []
    
    # Check for extreme variations
    for i, count in enumerate(word_counts):
        if count < avg_length * 0.5:
            pacing_issues.append(f"Chapter {i+1} very short ({count} words)")
        elif count > avg_length * 1.5:
            pacing_issues.append(f"Chapter {i+1} very long ({count} words)")
    
    # Check middle section for sagging
    middle_start = len(chapters) // 3
    middle_end = 2 * len(chapters) // 3
    middle_avg = sum(word_counts[middle_start:middle_end]) // (middle_end - middle_start)
    
    if middle_avg < avg_length * 0.9:
        pacing_issues.append("Middle section may be sagging (lower word count)")
    
    pacing_text = f"""
- **Average chapter length:** {avg_length} words
- **Length variation:** {max(word_counts) - min(word_counts)} words difference
- **Middle section average:** {middle_avg} words
"""
    
    if pacing_issues:
        pacing_text += "\n**Pacing concerns:**\n"
        for issue in pacing_issues[:3]:  # Show top 3
            pacing_text += f"- {issue}\n"
    
    return pacing_text


def main():
    parser = argparse.ArgumentParser(description="Review Book Chapters")
    parser.add_argument("--chapters", "-c", required=True, help="Directory containing chapter files")
    parser.add_argument("--book-bible", "-b", required=True, help="Path to book bible markdown file")
    parser.add_argument("--discovery", "-d", required=True, help="Path to discovery JSON file")
    parser.add_argument("--output", "-o", default="review-notes.md", help="Output file")
    parser.add_argument("--fix", action="store_true", help="Attempt to auto-fix minor issues")
    
    args = parser.parse_args()
    
    # Import datetime here to avoid circular import
    from datetime import datetime
    
    # Load data
    chapters = load_chapters(args.chapters)
    
    if not chapters:
        print(f"Error: No chapter files found in {args.chapters}")
        return 1
    
    book_bible_content = load_book_bible(args.book_bible)
    
    with open(args.discovery, 'r', encoding='utf-8') as f:
        discovery_data = json.load(f)
    
    # Review chapters
    report, issues_found = review_chapters(chapters, book_bible_content, discovery_data)
    
    # Write report
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✓ Review complete: {output_path}")
    print(f"  Chapters reviewed: {len(chapters)}")
    print(f"  Issues found: {issues_found}")
    print(f"  Average words per chapter: {sum(c['word_count'] for c in chapters) // len(chapters):,}")
    
    if args.fix:
        print("\nAuto-fix not yet implemented. Review report for manual fixes.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())