#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Novel to EPUB Converter
Converts markdown chapter files to a professionally formatted EPUB ebook.

Usage:
    python3 create_epub.py [options]

Options:
    --title TITLE       Book title (default: auto-detect from task_plan.md or directory)
    --author AUTHOR     Author name (default: "Claude AI")
    --path PATH         Directory containing chapter files (default: current directory)
    --output OUTPUT     Output filename (default: [title].epub)
    --subtitle SUBTITLE Book subtitle/tagline
    --description DESC  Book description for metadata

Example:
    python3 create_epub.py --title "凤鸣九霄" --author "Claude AI" --subtitle "穿越·宫廷·玄幻·爱情"
"""

import os
import re
import argparse
import glob
from ebooklib import epub


def parse_args():
    parser = argparse.ArgumentParser(description='Convert markdown chapters to EPUB')
    parser.add_argument('--title', type=str, help='Book title')
    parser.add_argument('--author', type=str, default='Claude AI', help='Author name')
    parser.add_argument('--path', type=str, default='.', help='Chapter directory')
    parser.add_argument('--output', type=str, help='Output filename')
    parser.add_argument('--subtitle', type=str, default='', help='Book subtitle')
    parser.add_argument('--description', type=str, default='', help='Book description')
    return parser.parse_args()


def detect_title_from_plan(path):
    """Try to detect book title from task_plan.md"""
    plan_file = os.path.join(path, 'task_plan.md')
    if os.path.exists(plan_file):
        with open(plan_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for "# Writing Plan: XXX" or "# 写作计划：XXX"
            match = re.search(r'^#\s*(?:Writing Plan|写作计划)[：:]\s*[《]?(.+?)[》]?\s*$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
    return None


def find_chapter_files(path):
    """Find and sort chapter markdown files"""
    patterns = [
        os.path.join(path, '[0-9][0-9]_*.md'),
        os.path.join(path, '第*章*.md'),
        os.path.join(path, 'chapter_*.md'),
    ]

    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))

    # Remove duplicates and sort
    files = sorted(set(files))

    # Filter out non-chapter files
    excluded = ['task_plan.md', 'README.md', 'plan.md']
    files = [f for f in files if os.path.basename(f).lower() not in [e.lower() for e in excluded]]

    return files


def extract_chapter_title(filepath):
    """Extract chapter title from filename or file content"""
    filename = os.path.basename(filepath)

    # Try to get title from filename: "01_标题.md" -> "第一章 标题"
    match = re.match(r'(\d+)_(.+)\.md', filename)
    if match:
        num = int(match.group(1))
        title = match.group(2)
        chinese_nums = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
                       '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十']
        if num < len(chinese_nums):
            return f"第{chinese_nums[num]}章 {title}"
        return f"第{num}章 {title}"

    # Try to extract from file content
    with open(filepath, 'r', encoding='utf-8') as f:
        first_lines = f.read(500)
        match = re.search(r'^#\s+(.+)$', first_lines, re.MULTILINE)
        if match:
            return match.group(1).strip()

    return filename.replace('.md', '')


def md_to_html(md_content):
    """Convert Markdown to HTML with Chinese novel formatting"""
    html = md_content

    # Process headings
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # Process blockquotes (poetry/lyrics)
    def replace_blockquote(match):
        content = match.group(1)
        lines = content.strip().split('\n')
        formatted_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith('> '):
                line = line[2:]
            elif line.startswith('>'):
                line = line[1:]
            if line:
                formatted_lines.append(f'<p class="quote-line">{line}</p>')
        return '<blockquote class="poetry">' + '\n'.join(formatted_lines) + '</blockquote>'

    html = re.sub(r'((?:^>.*\n?)+)', replace_blockquote, html, flags=re.MULTILINE)

    # Process formatting
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Process horizontal rules
    html = re.sub(r'^---+$', r'<hr/>', html, flags=re.MULTILINE)

    # Process paragraphs
    paragraphs = html.split('\n\n')
    processed = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if any(p.startswith(tag) for tag in ['<h', '<blockquote', '<hr', '<p']):
            processed.append(p)
        else:
            p = p.replace('\n', '<br/>')
            processed.append(f'<p>{p}</p>')

    return '\n'.join(processed)


def get_css_style():
    """Return CSS for Chinese novel typography"""
    return '''
@namespace epub "http://www.idpf.org/2007/ops";

body {
    font-family: "Songti SC", "SimSun", "Noto Serif CJK SC", serif;
    line-height: 1.8;
    padding: 20px;
    text-align: justify;
}

h1 {
    font-size: 1.8em;
    text-align: center;
    margin: 40px 0 30px 0;
    color: #333;
    font-weight: bold;
}

h2 {
    font-size: 1.4em;
    margin: 30px 0 20px 0;
    color: #444;
}

h3 {
    font-size: 1.2em;
    margin: 20px 0 15px 0;
    color: #555;
}

p {
    text-indent: 2em;
    margin: 0.8em 0;
}

blockquote.poetry {
    border-left: 3px solid #c9a959;
    padding-left: 15px;
    margin: 25px 0;
    background: #faf8f0;
    padding: 15px 15px 15px 20px;
}

blockquote.poetry p.quote-line {
    font-style: italic;
    color: #666;
    text-indent: 0;
    margin: 5px 0;
}

hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 30px auto;
    width: 60%;
}

.cover-title {
    font-size: 2.5em;
    text-align: center;
    margin-top: 30%;
    color: #333;
}

.cover-subtitle {
    font-size: 1.2em;
    text-align: center;
    color: #666;
    margin-top: 20px;
}

.cover-author {
    font-size: 1em;
    text-align: center;
    color: #888;
    margin-top: 50px;
}

.chapter-end {
    text-align: center;
    margin: 40px 0;
    color: #888;
}
'''


def create_cover_page(title, subtitle, author, css_item):
    """Create cover page HTML"""
    content = f'''
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="style/novel.css"/>
</head>
<body>
    <div style="text-align: center; padding-top: 100px;">
        <h1 class="cover-title">{title}</h1>
        <p class="cover-subtitle">{subtitle}</p>
        <hr style="width: 200px; margin: 50px auto;"/>
        <p class="cover-author">作者：{author}</p>
    </div>
</body>
</html>
'''
    cover = epub.EpubHtml(title='封面', file_name='cover.xhtml', lang='zh')
    cover.content = content
    cover.add_item(css_item)
    return cover


def create_epub(args):
    """Main function to create EPUB"""
    path = os.path.abspath(args.path)

    # Detect title
    title = args.title or detect_title_from_plan(path) or os.path.basename(path)
    author = args.author
    subtitle = args.subtitle
    description = args.description

    print(f"📚 Creating EPUB: {title}")
    print(f"   Author: {author}")
    print(f"   Path: {path}")

    # Find chapter files
    chapter_files = find_chapter_files(path)
    if not chapter_files:
        print("❌ No chapter files found!")
        print("   Looking for patterns: XX_title.md, 第X章.md, chapter_X.md")
        return None

    print(f"   Found {len(chapter_files)} chapters")

    # Create book
    book = epub.EpubBook()
    book.set_identifier(f'{title.replace(" ", "-")}-{hash(title) % 10000:04d}')
    book.set_title(title)
    book.set_language('zh')
    book.add_author(author)

    if description:
        book.add_metadata('DC', 'description', description)

    # Add CSS
    css = epub.EpubItem(
        uid="style_novel",
        file_name="style/novel.css",
        media_type="text/css",
        content=get_css_style()
    )
    book.add_item(css)

    # Create cover
    cover = create_cover_page(title, subtitle, author, css)
    book.add_item(cover)

    # Process chapters
    epub_chapters = [cover]
    toc_items = [epub.Link('cover.xhtml', '封面', 'cover')]

    for filepath in chapter_files:
        chapter_title = extract_chapter_title(filepath)
        filename = os.path.basename(filepath).replace('.md', '.xhtml')

        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()

        html_content = md_to_html(md_content)

        chapter = epub.EpubHtml(
            title=chapter_title,
            file_name=filename,
            lang='zh'
        )
        chapter.content = f'''
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{chapter_title}</title>
    <link rel="stylesheet" type="text/css" href="style/novel.css"/>
</head>
<body>
    {html_content}
</body>
</html>
'''
        chapter.add_item(css)
        book.add_item(chapter)
        epub_chapters.append(chapter)
        toc_items.append(epub.Link(filename, chapter_title, filename.replace('.xhtml', '')))
        print(f"   ✓ {chapter_title}")

    # Set TOC and spine
    book.toc = tuple(toc_items)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + epub_chapters

    # Write EPUB
    output_name = args.output or f'{title}.epub'
    output_path = os.path.join(path, output_name)
    epub.write_epub(output_path, book, {})

    print(f"\n✅ EPUB created successfully!")
    print(f"📖 Output: {output_path}")

    return output_path


if __name__ == '__main__':
    args = parse_args()
    create_epub(args)
