#!/usr/bin/env python3
"""
text-compressor.py — compress text files while preserving readability.
Usage: python compress.py <input_file> [output_file] [--level 1-9]
"""

import sys
import argparse
import re
from pathlib import Path


def compress_text(content: str, level: int = 1) -> str:
    """Apply text compression heuristics."""
    
    # Level 1: Clean whitespace
    lines = content.splitlines()
    
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in lines]
    
    # Remove consecutive empty lines (preserve max 1)
    cleaned = []
    prev_empty = False
    for line in lines:
        if line:
            cleaned.append(line)
            prev_empty = False
        elif not prev_empty:
            cleaned.append('')
            prev_empty = True
    
    result = '\n'.join(cleaned)
    
    if level >= 2:
        # Level 2: Shorten common phrases (single-space preserved)
        replacements = [
            (r'\bthat is\b', "that's"),
            (r'\bthat the\b', "th'"),
            (r'\bfor the\b', "4th"),
            (r'\bwith the\b', "w/th"),
            (r'\bto the\b', "2th"),
            (r'\band the\b', "n'th"),
            (r'\bin the\b', "in th'"),
            (r'\byou are\b', "ur"),
            (r'\bwe are\b', "we're"),
            (r'\bthey are\b', "they're"),
            (r'\bit is\b', "it's"),
            (r'\bthis is\b', "this's"),
            (r'\bis not\b', "isn't"),
            (r'\bare not\b', "aren't"),
            (r'\bdo not\b', "don't"),
            (r'\bdoes not\b', "doesn't"),
            (r'\bcan not\b', "can't"),
            (r'\bwill not\b', "won't"),
            (r'\bshould not\b', "shouldn't"),
            (r'\bhave not\b', "haven't"),
            (r'\bhas not\b', "hasn't"),
            (r'\bhad not\b', "hadn't"),
            (r'\bI am\b', "I'm"),
            (r'\byou are\b', "you're"),
            (r'\bwe are\b', "we're"),
            (r'\bthey are\b', "they're"),
            (r'\bit will\b', "it'll"),
            (r'\bthat will\b', "that'll"),
            (r'\bthere will\b', "there'll"),
            (r'\bhere is\b', "here's"),
            (r'\bthere is\b', "there's"),
            (r'\bwhat is\b', "what's"),
            (r'\bwho is\b', "who's"),
        ]
        for pattern, replacement in replacements:
            result = re.sub(pattern, replacement, result)
    
    if level >= 3:
        # Level 3: Aggressive abbreviations
        aggressive = [
            (r'\bbecause\b', "bc"),
            (r'\bthrough\b', "thru"),
            (r'\bwithout\b', "w/o"),
            (r'\bwithin\b', "w/in"),
            (r'\bwhether\b', "weth"),
            (r'\bleast\b', "lst"),
            (r'\bmight\b', "mght"),
            (r'\bthought\b', "thot"),
            (r'\bwhich\b', "whch"),
            (r'\bwhere\b', "whre"),
            (r'\bwould\b', "wd"),
            (r'\bcould\b', "cld"),
            (r'\bshould\b', "shd"),
            (r'\babout\b', "abt"),
            (r'\bagain\b', "ag n"),
            (r'\bafter\b', "aft"),
            (r'\balso\b', "als"),
            (r'\bbefore\b', "bef"),
            (r'\bbetween\b', "btn"),
            (r'\bgoing\b', "goin"),
            (r'\bknew\b', "nju"),
            (r'\blittle\b', "lil"),
            (r'\bmany\b', "mny"),
            (r'\bnever\b', "nvr"),
            (r'\bonly\b', "onli"),
            (r'\bother\b', "othr"),
            (r'\breally\b', "rly"),
            (r'\bshould\b', "shld"),
            (r'\bsomeone\b', "sm1"),
            (r'\bsomething\b', "smth"),
            (r'\btoday\b', "tdy"),
            (r'\btomorrow\b', "tmrw"),
            (r'\byesterday\b', "yest"),
            (r'\blevel\b', "lvl"),
            (r'\bpassword\b', "pwd"),
            (r'\busername\b', "usr"),
            (r'\bnumber\b', "num"),
            (r'\breceive\b', "rcv"),
            (r'\breceived\b', "rcvd"),
            (r'\bplease\b', "pls"),
            (r'\bthank you\b', "thx"),
            (r'\bthanks\b', "thx"),
        ]
        for pattern, replacement in aggressive:
            result = re.sub(pattern, replacement, result)
    
    return result


def decompress_text(content: str, level: int = 1) -> str:
    """Reverse compression - restore original text."""
    # This is approximate - can't fully restore originals
    replacements = [
        ("bc", "because"),
        ("thru", "through"),
        ("w/o", "without"),
        ("w/in", "within"),
        ("ur", "you are"),
        ("I'm", "I am"),
        ("you're", "you are"),
        ("we're", "we are"),
        ("they're", "they are"),
        ("it's", "it is"),
        ("that's", "that is"),
        ("isn't", "is not"),
        ("aren't", "are not"),
        ("don't", "do not"),
        ("doesn't", "does not"),
        ("can't", "can not"),
        ("won't", "will not"),
        ("shouldn't", "should not"),
        ("haven't", "have not"),
        ("hasn't", "has not"),
        ("hadn't", "had not"),
        ("it'll", "it will"),
        ("that'll", "that will"),
        ("there'll", "there will"),
        ("here's", "here is"),
        ("there's", "there is"),
        ("what's", "what is"),
        ("who's", "who is"),
    ]
    for abbr, full in replacements:
        result = content.replace(abbr, full)
    
    # Normalize whitespace
    result = re.sub(r' +', ' ', result)
    return result


def main():
    parser = argparse.ArgumentParser(description='Compress text files')
    parser.add_argument('input', help='Input file path')
    parser.add_argument('output', nargs='?', help='Output file path (default: input + .compressed)')
    parser.add_argument('--level', type=int, default=1, choices=[1, 2, 3], help='Compression level 1-3')
    parser.add_argument('--decompress', action='store_true', help='Decompress instead')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)
    
    content = input_path.read_text(encoding='utf-8')
    
    if args.decompress:
        result = decompress_text(content, args.level)
    else:
        result = compress_text(content, args.level)
    
    if args.output:
        output_path = Path(args.output)
    else:
        suffix = '.compressed' if not args.decompress else '.restored'
        output_path = input_path.with_suffix(input_path.suffix + suffix)
    
    output_path.write_text(result, encoding='utf-8')
    
    orig_size = len(content.encode('utf-8'))
    new_size = len(result.encode('utf-8'))
    ratio = (1 - new_size / orig_size) * 100 if orig_size > 0 else 0
    
    print(f"Done: {orig_size} -> {new_size} bytes ({ratio:.1f}% reduction)")
    print(f"Output: {output_path}")


if __name__ == '__main__':
    main()