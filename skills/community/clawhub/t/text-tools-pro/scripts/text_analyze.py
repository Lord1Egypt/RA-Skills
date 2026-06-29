#!/usr/bin/env python3
"""Text analysis and statistics tool."""

import sys
import re
import argparse

def analyze_text(text):
    """Analyze text and return statistics."""
    stats = {}
    
    # Basic counts
    stats['total_chars'] = len(text)
    stats['total_chars_no_spaces'] = len(text.replace(' ', '').replace('\n', ''))
    
    # Word count (split by whitespace and punctuation)
    words = re.findall(r'\b\w+\b', text)
    stats['word_count'] = len(words)
    
    # Line count
    lines = text.split('\n')
    stats['line_count'] = len(lines)
    stats['non_empty_lines'] = len([l for l in lines if l.strip()])
    
    # Paragraph count (separated by blank lines)
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    stats['paragraph_count'] = len(paragraphs)
    
    # Reading time estimate (average 200 words per minute)
    stats['reading_time_min'] = round(stats['word_count'] / 200, 1)
    
    # Sentence count (rough estimate)
    sentences = re.split(r'[.!?。！？]+', text)
    stats['sentence_count'] = len([s for s in sentences if s.strip()])
    
    # Average word length
    if words:
        stats['avg_word_length'] = round(sum(len(w) for w in words) / len(words), 1)
    else:
        stats['avg_word_length'] = 0
    
    # Unique words
    stats['unique_words'] = len(set(w.lower() for w in words))
    
    return stats

def main():
    parser = argparse.ArgumentParser(description='Analyze text statistics')
    parser.add_argument('--input', '-i', required=True, help='Input file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    stats = analyze_text(text)
    
    if args.json:
        import json
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print(f"Text Analysis Results")
        print(f"====================")
        print(f"Total Characters:        {stats['total_chars']:,}")
        print(f"Characters (no spaces):  {stats['total_chars_no_spaces']:,}")
        print(f"Word Count:              {stats['word_count']:,}")
        print(f"Unique Words:            {stats['unique_words']:,}")
        print(f"Sentences:               {stats['sentence_count']:,}")
        print(f"Paragraphs:              {stats['paragraph_count']:,}")
        print(f"Lines:                   {stats['line_count']:,}")
        print(f"Non-empty Lines:         {stats['non_empty_lines']:,}")
        print(f"Average Word Length:     {stats['avg_word_length']}")
        print(f"Estimated Reading Time:  {stats['reading_time_min']} minutes")

if __name__ == '__main__':
    main()
