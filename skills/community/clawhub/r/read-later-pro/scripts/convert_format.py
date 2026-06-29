#!/usr/bin/env python3
"""
Convert article between different formats: Markdown, PDF, EPUB, HTML.
"""

import sys
import json
import os
import re
from datetime import datetime

def markdown_to_html(markdown_content, title="Article"):
    """Convert Markdown to HTML."""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px 20px; line-height: 1.6; color: #333; }}
        h1 {{ color: #222; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        h2 {{ color: #444; margin-top: 30px; }}
        p {{ margin: 15px 0; }}
        a {{ color: #0066cc; }}
        img {{ max-width: 100%; height: auto; }}
        blockquote {{ border-left: 4px solid #ddd; margin: 0; padding-left: 20px; color: #666; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
        pre {{ background: #f4f4f4; padding: 15px; overflow-x: auto; border-radius: 5px; }}
    </style>
</head>
<body>
"""
    
    # Simple markdown to HTML conversion
    content = markdown_content
    
    # Headers
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    
    # Bold and italic
    content = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', content)
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
    
    # Links
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
    
    # Code blocks
    content = re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', content, flags=re.DOTALL)
    content = re.sub(r'`(.+?)`', r'<code>\1</code>', content)
    
    # Blockquotes
    content = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', content, flags=re.MULTILINE)
    
    # Paragraphs
    paragraphs = content.split('\n\n')
    html_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<') and not p.startswith('```'):
            p = f'<p>{p}</p>'
        html_paragraphs.append(p)
    
    html += '\n'.join(html_paragraphs)
    html += '\n</body>\n</html>'
    
    return html

def markdown_to_epub(markdown_content, title="Article", author=""):
    """Create a simple EPUB structure."""
    # EPUB is a ZIP file with specific structure
    # For simplicity, we'll create the content file that would go inside
    html_content = markdown_to_html(markdown_content, title)
    
    # Remove DOCTYPE and html tags for EPUB content
    html_content = re.sub(r'<!DOCTYPE[^>]*>', '', html_content)
    html_content = re.sub(r'<html[^>]*>', '<html xmlns="http://www.w3.org/1999/xhtml">', html_content)
    
    return html_content

def create_markdown(metadata, content):
    """Create formatted Markdown from metadata and content."""
    md = f"""# {metadata.get('title', 'Untitled')}

**Source:** [{metadata.get('url', 'Unknown')}]({metadata.get('url', '#')})  
"""
    if metadata.get('author'):
        md += f"**Author:** {metadata['author']}  \n"
    
    md += f"**Saved:** {metadata.get('date', datetime.now().isoformat())}  \n"
    md += f"**Word Count:** {metadata.get('word_count', 0)}  \n\n"
    md += "---\n\n"
    md += content
    
    return md

def main():
    if len(sys.argv) < 4:
        print("Usage: convert_format.py <input_file> <output_format> <output_file>", file=sys.stderr)
        print("Formats: markdown, html, epub", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_format = sys.argv[2].lower()
    output_file = sys.argv[3]
    
    # Read input
    with open(input_file, 'r', encoding='utf-8') as f:
        if input_file.endswith('.json'):
            data = json.load(f)
            content = data.get('content', '')
            metadata = data
        else:
            content = f.read()
            metadata = {'title': 'Article', 'url': '', 'date': datetime.now().isoformat()}
    
    # Convert
    if output_format == 'markdown' or output_format == 'md':
        output = create_markdown(metadata, content)
    elif output_format == 'html':
        output = markdown_to_html(content, metadata.get('title', 'Article'))
    elif output_format == 'epub':
        output = markdown_to_epub(content, metadata.get('title', 'Article'), metadata.get('author', ''))
    else:
        print(f"Unsupported format: {output_format}", file=sys.stderr)
        sys.exit(1)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"Converted to {output_format}: {output_file}")

if __name__ == '__main__':
    main()
