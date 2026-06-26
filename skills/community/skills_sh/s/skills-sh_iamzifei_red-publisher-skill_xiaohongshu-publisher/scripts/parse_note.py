#!/usr/bin/env python3
"""
Parse Markdown or text content for Xiaohongshu (小红书) note publishing.

Extracts:
- Title (from first H1/H2 or first line)
- Content (body text, without images)
- Images (list of image paths)
- Tags (from #hashtag format)

Usage:
    python parse_note.py <file> [--output json]
    python parse_note.py --title "标题" --content "内容" --images "img1.jpg,img2.jpg"

Output (JSON):
{
    "title": "Note Title",
    "content": "Note content text...",
    "images": ["/path/to/img1.jpg", "/path/to/img2.jpg"],
    "tags": ["tag1", "tag2"]
}
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def extract_title(text: str) -> tuple[str, str]:
    """Extract title from first H1, H2, or first non-empty line.

    Returns:
        (title, text_without_title_line)
    """
    lines = text.strip().split('\n')
    title = ""
    title_line_idx = None

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        # H1 - use as title and remove
        if stripped.startswith('# '):
            title = stripped[2:].strip()
            title_line_idx = idx
            break
        # H2 - use as title and remove
        if stripped.startswith('## '):
            title = stripped[3:].strip()
            title_line_idx = idx
            break
        # First non-empty, non-image line
        if not stripped.startswith('!['):
            title = stripped[:50]  # Xiaohongshu title is short
            title_line_idx = idx
            break

    # Remove title line from text
    if title_line_idx is not None:
        lines.pop(title_line_idx)
        text = '\n'.join(lines)

    return title, text


def extract_images(text: str, base_path: Path) -> tuple[list[str], str]:
    """Extract image paths and return text without image references.

    Returns:
        (image_paths, text_without_images)
    """
    images = []

    # Find all markdown images
    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

    def process_image(match):
        img_path = match.group(2)

        # Skip URLs, only process local files
        if img_path.startswith(('http://', 'https://')):
            return ''

        # Resolve relative paths
        if not os.path.isabs(img_path):
            full_path = str(base_path / img_path)
        else:
            full_path = img_path

        # Only add if file exists
        if os.path.exists(full_path):
            images.append(full_path)
        else:
            print(f"Warning: Image not found: {full_path}", file=sys.stderr)

        return ''  # Remove from text

    clean_text = img_pattern.sub(process_image, text)

    return images, clean_text


def extract_tags(text: str) -> tuple[list[str], str]:
    """Extract hashtags from text.

    Returns:
        (tags, text_without_tags)
    """
    tags = []

    # Find all hashtags (Chinese and English)
    # Match #tag or #标签 format, but not ## headers
    tag_pattern = re.compile(r'(?<!#)#([^\s#]+)')

    matches = tag_pattern.findall(text)
    for tag in matches:
        if tag and tag not in tags:
            tags.append(tag)

    # Remove tag markers from text (keep the tag word itself)
    clean_text = tag_pattern.sub(r'\1', text)

    return tags, clean_text


def clean_content(text: str) -> str:
    """Clean up content text for Xiaohongshu.

    - Remove markdown formatting
    - Collapse multiple newlines
    - Trim whitespace
    """
    # Remove H2/H3 markers but keep text
    text = re.sub(r'^#{2,}\s*', '', text, flags=re.MULTILINE)

    # Remove bold/italic markers
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)

    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # Remove blockquote markers
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)

    # Remove list markers
    text = re.sub(r'^[-*]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)

    # Collapse multiple newlines to double
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Trim
    text = text.strip()

    return text


def parse_file(filepath: str) -> dict:
    """Parse a file and return structured data."""
    path = Path(filepath)
    base_path = path.parent

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title first
    title, content = extract_title(content)

    # Extract images
    images, content = extract_images(content, base_path)

    # Extract tags
    tags, content = extract_tags(content)

    # Clean content
    content = clean_content(content)

    return {
        "title": title,
        "content": content,
        "images": images,
        "tags": tags[:5],  # Xiaohongshu recommends max 5 tags
        "source_file": str(path.absolute())
    }


def parse_args_content(title: str, content: str, images_str: str, tags_str: str) -> dict:
    """Parse content from command line arguments."""
    images = []
    if images_str:
        for img in images_str.split(','):
            img = img.strip()
            if os.path.exists(img):
                images.append(os.path.abspath(img))
            else:
                print(f"Warning: Image not found: {img}", file=sys.stderr)

    tags = []
    if tags_str:
        tags = [t.strip() for t in tags_str.split(',') if t.strip()]

    return {
        "title": title or "",
        "content": content or "",
        "images": images,
        "tags": tags[:5]
    }


def main():
    parser = argparse.ArgumentParser(description='Parse content for Xiaohongshu notes')
    parser.add_argument('file', nargs='?', help='Markdown/text file to parse')
    parser.add_argument('--title', '-t', help='Note title')
    parser.add_argument('--content', '-c', help='Note content')
    parser.add_argument('--images', '-i', help='Comma-separated image paths')
    parser.add_argument('--tags', help='Comma-separated tags')
    parser.add_argument('--output', choices=['json'], default='json',
                       help='Output format (default: json)')

    args = parser.parse_args()

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        result = parse_file(args.file)
    elif args.title or args.content or args.images:
        result = parse_args_content(args.title, args.content, args.images, args.tags)
    else:
        print("Error: Provide either a file or --title/--content/--images", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
