#!/usr/bin/env python3
"""Text cleaning and normalization tool."""

import sys
import re
import argparse

def clean_text(text):
    """Clean and normalize text."""
    # Remove BOM
    text = text.lstrip('\ufeff')
    
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove extra blank lines (more than 2 consecutive)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove trailing whitespace
    text = '\n'.join(line.rstrip() for line in text.split('\n'))
    
    # Remove leading whitespace from each line
    text = '\n'.join(line.lstrip() for line in text.split('\n'))
    
    # Normalize multiple spaces to single space
    text = re.sub(r' +', ' ', text)
    
    # Remove zero-width characters
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)
    
    return text.strip()

def remove_extra_spaces(text):
    """Remove extra spaces while preserving paragraph structure."""
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Replace multiple spaces with single space
        line = re.sub(r' +', ' ', line)
        cleaned_lines.append(line.strip())
    return '\n'.join(cleaned_lines)

def normalize_unicode(text):
    """Normalize unicode characters."""
    import unicodedata
    return unicodedata.normalize('NFC', text)

def main():
    parser = argparse.ArgumentParser(description='Clean and normalize text')
    parser.add_argument('--input', '-i', required=True, help='Input file')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    parser.add_argument('--extra-spaces', action='store_true', help='Remove extra spaces only')
    parser.add_argument('--normalize-unicode', action='store_true', help='Normalize unicode')
    
    args = parser.parse_args()
    
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    if args.extra_spaces:
        result = remove_extra_spaces(text)
    elif args.normalize_unicode:
        result = normalize_unicode(text)
    else:
        result = clean_text(text)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Cleaned text saved to: {args.output}")
    else:
        print(result)

if __name__ == '__main__':
    main()
