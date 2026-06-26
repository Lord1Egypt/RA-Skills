#!/usr/bin/env python3
"""
EPUB Processor for Reading Assistant Skill
Parses an .epub file → extracts chapters → outputs JSON manifest + chapter text files.

Usage:
    python process_epub.py <epub_path> <output_dir>

Output:
    <output_dir>/manifest.json   — book metadata + chapter list
    <output_dir>/chapters/       — one .txt per chapter
"""

import sys
import os
import json
import re
import hashlib
from pathlib import Path

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


def clean_text(html_content):
    """Extract and clean text from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style tags
    for tag in soup(['script', 'style']):
        tag.decompose()

    # Get text with newlines preserved
    text = soup.get_text(separator='\n')

    # Clean up excessive whitespace
    lines = [line.strip() for line in text.splitlines()]
    text = '\n'.join(line for line in lines if line)

    return text


def extract_chapter_title(text, index, toc_titles=None):
    """Try to extract a chapter title from the text or TOC."""
    if toc_titles and index < len(toc_titles):
        return toc_titles[index]

    # Try first line as title
    first_line = text.split('\n')[0].strip()
    if len(first_line) < 100 and first_line:
        return first_line

    return f"Chapter {index + 1}"


def parse_epub(epub_path, output_dir):
    """Parse epub and output structured chapter files."""
    book = epub.read_epub(epub_path)

    # --- Metadata ---
    def get_meta(field):
        val = book.get_metadata('DC', field)
        return val[0][0] if val else ''

    title = get_meta('title')
    author = get_meta('creator')
    language = get_meta('language')
    description = get_meta('description')

    # --- TOC titles ---
    toc_titles = []
    for item in book.toc:
        if isinstance(item, epub.Link):
            toc_titles.append(item.title)
        elif isinstance(item, tuple):
            section, links = item
            toc_titles.append(section.title)
            for link in links:
                toc_titles.append(link.title)

    # --- Extract chapters ---
    chapters = []
    chapter_dir = Path(output_dir) / 'chapters'
    chapter_dir.mkdir(parents=True, exist_ok=True)

    ch_index = 0
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        content = item.get_content()
        text = clean_text(content)

        # Skip very short content (cover pages, blank pages, etc.)
        if len(text) < 100:
            continue

        ch_title = extract_chapter_title(text, ch_index, toc_titles)
        ch_filename = f"ch_{ch_index:03d}.txt"
        ch_path = chapter_dir / ch_filename

        # Write chapter text
        ch_path.write_text(text, encoding='utf-8')

        chapters.append({
            'index': ch_index,
            'title': ch_title,
            'filename': ch_filename,
            'char_count': len(text),
            'word_estimate': len(text),  # For CJK, char ≈ word
            'reading_time_min': max(1, round(len(text) / 500)),  # ~500 CJK chars/min
        })

        ch_index += 1

    # --- Book ID (hash of title + author) ---
    book_id = hashlib.md5(f"{title}:{author}".encode()).hexdigest()[:12]

    # --- Manifest ---
    manifest = {
        'book_id': book_id,
        'title': title,
        'author': author,
        'language': language,
        'description': clean_text(description.encode()) if description else '',
        'total_chapters': len(chapters),
        'total_chars': sum(ch['char_count'] for ch in chapters),
        'total_reading_time_min': sum(ch['reading_time_min'] for ch in chapters),
        'chapters': chapters,
    }

    manifest_path = Path(output_dir) / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

    print(json.dumps({
        'status': 'success',
        'book_id': book_id,
        'title': title,
        'author': author,
        'total_chapters': len(chapters),
        'total_chars': manifest['total_chars'],
        'manifest_path': str(manifest_path),
        'chapters_dir': str(chapter_dir),
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python process_epub.py <epub_path> <output_dir>")
        sys.exit(1)

    epub_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(epub_path):
        print(f"Error: File not found: {epub_path}")
        sys.exit(1)

    parse_epub(epub_path, output_dir)
