#!/usr/bin/env python3
"""
Helper script for formatting YouTube subtitles for summarization.
"""

import sys
import textwrap

def clean_subtitles(text):
    """
    Clean up common artifacts in auto-generated subtitles.
    Removes extra spaces, fixes common punctuation issues.
    """
    # Remove multiple newlines
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    cleaned = ' '.join(lines)
    
    # Fix multiple spaces
    while '  ' in cleaned:
        cleaned = cleaned.replace('  ', ' ')
    
    return cleaned

def chunk_text(text, max_chunk_size=2000):
    """
    Split long text into chunks for models with context limits.
    """
    paragraphs = textwrap.wrap(text, max_chunk_size, break_long_words=False)
    return paragraphs

def format_for_summarization(text, video_url=None, video_title=None):
    """
    Format subtitle text ready for AI summarization.
    """
    cleaned = clean_subtitles(text)
    chunks = chunk_text(cleaned)
    
    output = []
    if video_title:
        output.append(f"Video: {video_title}")
    if video_url:
        output.append(f"URL: {video_url}")
    output.append("")
    output.append("Full Transcript:")
    output.append("---")
    
    for i, chunk in enumerate(chunks):
        if len(chunks) > 1:
            output.append(f"\n[Part {i+1}/{len(chunks)}]\n")
        output.append(chunk)
    
    output.append("\n---")
    
    return "\n".join(output)

def main():
    if len(sys.argv) < 2:
        print("Usage: python summarize.py <input-text-file>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    cleaned = clean_subtitles(text)
    formatted = format_for_summarization(cleaned)
    print(formatted)

if __name__ == "__main__":
    main()
