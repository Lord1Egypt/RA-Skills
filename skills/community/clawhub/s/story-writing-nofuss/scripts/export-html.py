#!/usr/bin/env python3
"""
HTML Book Export
Exports chapters as formatted HTML book.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Handle Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def load_chapters(chapter_dir):
    """Load all chapter files from directory."""
    chapter_dir = Path(chapter_dir)
    chapters = []
    
    import re
    
    for filepath in sorted(chapter_dir.glob("chapter-*.md")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract chapter number and title
        match = re.search(r'# Chapter (\d+)(?::\s*(.+))?', content)
        chapter_num = int(match.group(1)) if match else 0
        chapter_title = match.group(2).strip() if match and match.group(2) else f"Chapter {chapter_num}"
        
        # Remove markdown headers, convert to HTML
        html_content = markdown_to_html(content)
        
        chapters.append({
            'number': chapter_num,
            'title': chapter_title,
            'filename': filepath.name,
            'content': html_content,
            'raw_content': content
        })
    
    return sorted(chapters, key=lambda x: x['number'])


def markdown_to_html(markdown):
    """Convert markdown to HTML (simplified)."""
    
    # Remove chapter header
    lines = markdown.split('\n')
    html_lines = []
    
    for line in lines:
        # Skip chapter header (already handled)
        if line.startswith('# Chapter'):
            continue
        
        # Convert headers
        if line.startswith('## '):
            html_lines.append(f'<h3>{line[3:]}</h3>')
        elif line.startswith('### '):
            html_lines.append(f'<h4>{line[4:]}</h4>')
        elif line.startswith('#### '):
            html_lines.append(f'<h5>{line[5:]}</h5>')
        
        # Convert emphasis
        elif '**' in line or '__' in line:
            # Simple bold conversion
            line = line.replace('**', '<strong>').replace('__', '<strong>')
            # Need to close tags properly in real implementation
            html_lines.append(f'<p>{line}</p>')
        
        # Convert italics
        elif '*' in line or '_' in line:
            line = line.replace('*', '<em>').replace('_', '<em>')
            html_lines.append(f'<p>{line}</p>')
        
        # Empty line
        elif line.strip() == '':
            html_lines.append('<p>&nbsp;</p>')
        
        # Regular paragraph
        else:
            html_lines.append(f'<p>{line}</p>')
    
    return '\n'.join(html_lines)


def generate_html_book(chapters, discovery_data, output_path):
    """Generate complete HTML book."""
    
    answers = discovery_data.get('answers', {})
    
    # Get book title from discovery or default
    book_title = answers.get('book_title', 'My Novel')
    author_name = answers.get('author_name', 'Author')
    genre = answers.get('genre', 'Fiction')
    
    # Generate table of contents
    toc_items = []
    for chapter in chapters:
        toc_items.append(f'<li><a href="#chapter-{chapter["number"]}">{chapter["title"]}</a></li>')
    
    toc_html = '\n'.join(toc_items)
    
    # Generate chapter HTML
    chapter_html = []
    for chapter in chapters:
        chapter_html.append(f'''
        <div class="chapter" id="chapter-{chapter["number"]}">
            <h2>{chapter["title"]}</h2>
            {chapter["content"]}
        </div>
        ''')
    
    chapters_html = '\n'.join(chapter_html)
    
    # Complete HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book_title}</title>
    <style>
        /* Book Styling */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Georgia, 'Times New Roman', Times, serif;
            line-height: 1.6;
            color: #333;
            background-color: #f9f9f9;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .title-page {{
            text-align: center;
            padding: 40vh 20px;
            page-break-after: always;
        }}
        
        .title-page h1 {{
            font-size: 3em;
            margin-bottom: 20px;
            color: #222;
        }}
        
        .title-page h2 {{
            font-size: 1.5em;
            font-weight: normal;
            color: #666;
            margin-bottom: 40px;
        }}
        
        .title-page .author {{
            font-size: 1.2em;
            color: #444;
        }}
        
        .toc {{
            page-break-after: always;
            padding: 40px 20px;
        }}
        
        .toc h2 {{
            text-align: center;
            margin-bottom: 30px;
            font-size: 2em;
        }}
        
        .toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        
        .toc li {{
            margin-bottom: 10px;
            padding: 5px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .toc a {{
            text-decoration: none;
            color: #333;
            display: block;
            padding: 5px 10px;
            transition: background-color 0.3s;
        }}
        
        .toc a:hover {{
            background-color: #f0f0f0;
        }}
        
        .chapter {{
            page-break-before: always;
            padding: 40px 20px;
        }}
        
        .chapter h2 {{
            text-align: center;
            margin-bottom: 40px;
            font-size: 2em;
            color: #222;
            border-bottom: 2px solid #ddd;
            padding-bottom: 10px;
        }}
        
        .chapter p {{
            margin-bottom: 1.5em;
            text-align: justify;
            font-size: 1.1em;
        }}
        
        .chapter h3 {{
            margin: 30px 0 15px 0;
            color: #444;
            font-size: 1.5em;
        }}
        
        .chapter h4 {{
            margin: 25px 0 10px 0;
            color: #555;
            font-size: 1.3em;
        }}
        
        .chapter strong {{
            font-weight: bold;
        }}
        
        .chapter em {{
            font-style: italic;
        }}
        
        /* Print styles */
        @media print {{
            body {{
                background-color: white;
                padding: 0;
            }}
            
            .title-page {{
                padding: 35vh 20px;
            }}
            
            .toc, .chapter {{
                padding: 20px;
            }}
            
            .toc a::after {{
                content: leader(".") target-counter(attr(href), page);
            }}
        }}
        
        /* Page breaks for print */
        @media print {{
            .title-page, .toc, .chapter {{
                page-break-inside: avoid;
            }}
            
            .chapter h2 {{
                page-break-after: avoid;
            }}
            
            .chapter p {{
                orphans: 3;
                widows: 3;
            }}
        }}
    </style>
</head>
<body>
    <!-- Title Page -->
    <div class="title-page">
        <h1>{book_title}</h1>
        <h2>{genre}</h2>
        <div class="author">by {author_name}</div>
    </div>
    
    <!-- Table of Contents -->
    <div class="toc">
        <h2>Table of Contents</h2>
        <ul>
            {toc_html}
        </ul>
    </div>
    
    <!-- Chapters -->
    {chapters_html}
    
    <!-- End of Book -->
    <div class="chapter">
        <h2>The End</h2>
        <p style="text-align: center; font-style: italic; margin-top: 100px;">
            Thank you for reading.
        </p>
    </div>
    
    <script>
        // Add chapter numbers to TOC in print
        if (window.matchMedia('print').matches) {{
            document.addEventListener('DOMContentLoaded', function() {{
                var chapters = document.querySelectorAll('.chapter');
                var tocLinks = document.querySelectorAll('.toc a');
                
                for (var i = 0; i < chapters.length; i++) {{
                    if (tocLinks[i]) {{
                        // In a real implementation, you would add page numbers
                        // This is simplified for the example
                    }}
                }}
            }});
        }}
        
        // Smooth scrolling for TOC links
        document.addEventListener('DOMContentLoaded', function() {{
            var tocLinks = document.querySelectorAll('.toc a');
            
            tocLinks.forEach(function(link) {{
                link.addEventListener('click', function(e) {{
                    e.preventDefault();
                    var targetId = this.getAttribute('href');
                    var targetElement = document.querySelector(targetId);
                    
                    if (targetElement) {{
                        window.scrollTo({{
                            top: targetElement.offsetTop - 20,
                            behavior: 'smooth'
                        }});
                    }}
                }});
            }});
        }});
    </script>
</body>
</html>'''
    
    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return html


def main():
    parser = argparse.ArgumentParser(description="Export Book as HTML")
    parser.add_argument("--chapters", "-c", required=True, help="Directory containing chapter files")
    parser.add_argument("--discovery", "-d", required=True, help="Path to discovery JSON file")
    parser.add_argument("--output", "-o", default="export/book.html", help="Output HTML file")
    parser.add_argument("--title", "-t", help="Book title (overrides discovery)")
    parser.add_argument("--author", "-a", help="Author name (overrides discovery)")
    
    args = parser.parse_args()
    
    # Load data
    chapters = load_chapters(args.chapters)
    
    if not chapters:
        print(f"Error: No chapter files found in {args.chapters}")
        return 1
    
    with open(args.discovery, 'r', encoding='utf-8') as f:
        discovery_data = json.load(f)
    
    # Override title/author if provided
    if args.title:
        discovery_data['answers']['book_title'] = args.title
    if args.author:
        discovery_data['answers']['author_name'] = args.author
    
    # Ensure book_title exists
    if 'book_title' not in discovery_data['answers']:
        discovery_data['answers']['book_title'] = "My Novel"
    if 'author_name' not in discovery_data['answers']:
        discovery_data['answers']['author_name'] = "Author"
    
    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate HTML book
    html_content = generate_html_book(chapters, discovery_data, output_path)
    
    print(f"\n✓ HTML Book exported: {output_path}")
    print(f"  Chapters included: {len(chapters)}")
    print(f"  Title: {discovery_data['answers']['book_title']}")
    print(f"  Author: {discovery_data['answers']['author_name']}")
    print(f"\nFile size: {len(html_content) // 1024} KB")
    print("\nTo view: Open the HTML file in any web browser.")
    print("To print: Use browser's print function (Ctrl+P).")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())