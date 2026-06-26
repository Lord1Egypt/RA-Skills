#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""
Generate a professional design documentation HTML file for client delivery.

This script creates a comprehensive design specification document with the same
format and content dimensions as the reference test.html document. It includes
6 major sections with professional styling and comprehensive coverage.

NEW: Auto-extraction from HTML files! The script can now automatically extract
page structure, content summaries, colors, images, and CTAs from the generated HTML.

Usage:
    python generate_design_doc.py --project-name "Coffee Shop" --output "design-doc.html"

Auto-extract from HTML (Recommended):
    python generate_design_doc.py \
        --project-name "Coffee Shop" \
        --output "design-doc.html" \
        --html-file "index.html"

Advanced Usage:
    python generate_design_doc.py \
        --project-name "E-commerce Website" \
        --output "design-doc.html" \
        --html-file "index.html" \
        --design-concept "现代简约风格" \
        --author "设计团队"
"""

import argparse
import sys
import re
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser
from typing import List, Dict, Optional


def validate_output_path(filename: str) -> None:
    """Validate output filename to prevent path traversal attacks."""
    path = Path(filename)
    if '..' in path.parts:
        raise ValueError(f"Invalid filename '{filename}': Path traversal (..) is not allowed.")
    if path.is_absolute():
        raise ValueError(f"Invalid filename '{filename}': Absolute paths are not allowed.")
    filename_str = str(filename)
    if '//' in filename_str or '\\\\' in filename_str:
        raise ValueError(f"Invalid filename '{filename}': Contains invalid path separators.")


class SectionExtractor(HTMLParser):
    """HTML parser to extract page sections and their content based on headings."""

    def __init__(self):
        super().__init__()
        self.sections = []
        self.headings = []  # Store (tag, title, position)
        self.current_heading = None
        self.current_content = []
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header'}
        self.in_skip_tag = False
        self.current_skip_tag = None

    def handle_starttag(self, tag, attrs):
        # Skip certain tags
        if tag in self.skip_tags:
            self.in_skip_tag = True
            self.current_skip_tag = tag
            return

        # Capture headings (h1-h3) as section titles
        if tag in ['h1', 'h2', 'h3']:
            # Save previous section if exists
            if self.current_heading and self.current_content:
                content_summary = self._summarize_content(self.current_content)
                self.sections.append({
                    'name': self.current_heading['title'],
                    'content': content_summary
                })
            self.current_heading = {'tag': tag, 'title': ''}
            self.current_content = []

    def handle_endtag(self, tag):
        if self.in_skip_tag and tag == self.current_skip_tag:
            self.in_skip_tag = False
            self.current_skip_tag = None

        # Save section when encountering a new heading or end
        if tag in ['h1', 'h2', 'h3'] and self.current_heading:
            if self.current_heading['title']:  # Only save if title was captured
                pass  # Content will be saved when next heading starts

    def handle_data(self, data):
        if self.in_skip_tag:
            return

        text = data.strip()

        # Capture heading title
        if self.current_heading and not self.current_heading['title']:
            self.current_heading['title'] = text
        elif text and len(text) > 1:  # Capture section content
            # Ignore very short text and common noise
            if len(text) > 2 and not text.startswith(('&', '<')):
                self.current_content.append(text)

    def _summarize_content(self, content_list: List[str]) -> str:
        """Create a meaningful summary from content text."""
        if not content_list:
            return "该版块包含相关内容和信息展示。"

        # Filter out very short items
        meaningful_content = [c for c in content_list if len(c) > 5]

        if not meaningful_content:
            return "该版块包含相关内容和信息展示。"

        # Take first few meaningful sentences
        summary_parts = []
        total_chars = 0
        max_chars = 150  # Limit summary length

        for content in meaningful_content:
            if total_chars + len(content) > max_chars:
                break
            summary_parts.append(content)
            total_chars += len(content)

        if summary_parts:
            summary = ' '.join(summary_parts)
            # Add ellipsis if content was truncated
            if len(summary_parts) < len(meaningful_content):
                summary += '...'
            return summary

        return "该版块包含相关内容和信息展示。"

    def close(self):
        """Save the last section when parsing is complete."""
        super().close()
        if self.current_heading and self.current_heading['title'] and self.current_content:
            content_summary = self._summarize_content(self.current_content)
            self.sections.append({
                'name': self.current_heading['title'],
                'content': content_summary
            })

    def get_sections(self) -> List[Dict[str, str]]:
        """Return extracted sections."""
        return self.sections


def extract_sections_from_html(html_file: str) -> List[Dict[str, str]]:
    """Extract page sections and their content from HTML file.

    Args:
        html_file: Path to the HTML file

    Returns:
        List of dictionaries with 'name' and 'content' keys
    """
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        parser = SectionExtractor()
        parser.feed(html_content)
        parser.close()  # Important: call close() to save the last section

        sections = parser.get_sections()

        # If no sections found, try to extract from headings using regex
        if not sections:
            sections = extract_sections_from_headings(html_content)

        return sections

    except Exception as e:
        print(f"Warning: Could not extract sections from HTML: {e}", file=sys.stderr)
        return []


def extract_sections_from_headings(html_content: str) -> List[Dict[str, str]]:
    """Extract sections based on heading tags (h1-h3) with content summaries."""
    sections = []

    # Remove script and style tags
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    # Find all heading tags with their position and content
    heading_pattern = r'<h([1-3])[^>]*>(.*?)</h\1>'
    headings = list(re.finditer(heading_pattern, html_content, re.DOTALL | re.IGNORECASE))

    for i, match in enumerate(headings):
        level = match.group(1)
        title_html = match.group(2)

        # Clean up title (remove HTML tags)
        title_clean = re.sub(r'<[^>]+>', '', title_html).strip()
        if not title_clean:
            continue

        # Find content after this heading until next heading
        start_pos = match.end()
        if i + 1 < len(headings):
            end_pos = headings[i + 1].start()
        else:
            end_pos = len(html_content)

        # Extract content between this heading and next
        content_between = html_content[start_pos:end_pos]

        # Remove all HTML tags to get text content
        text_content = re.sub(r'<[^>]+>', ' ', content_between)
        text_content = re.sub(r'\s+', ' ', text_content).strip()

        # Get meaningful summary
        if text_content:
            # Take first few sentences
            sentences = [s.strip() for s in text_content.split('.') if s.strip()]
            summary = '. '.join(sentences[:3])  # Take up to 3 sentences
            if len(summary) > 150:
                summary = summary[:147] + '...'
        else:
            summary = f"该{level}级标题版块包含相关内容展示。"

        sections.append({
            'name': title_clean,
            'content': summary
        })

    return sections


def extract_colors_from_html(html_file: str) -> Dict[str, str]:
    """Extract color scheme from HTML/CSS file.

    Args:
        html_file: Path to the HTML file

    Returns:
        Dictionary with color keys (primary, secondary, accent, bg)
    """
    colors = {
        'primary': '#0a2540',
        'secondary': '#1e3a5f',
        'accent': '#ff6b2c',
        'bg': '#ffffff'  # Fixed white background
    }

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract CSS variables (excluding bg/background)
        css_var_pattern = r'--(?:primary|secondary|accent)[\s]*:[\s]*([#][0-9a-fA-F]{3,8})'
        matches = re.findall(css_var_pattern, content)

        if matches:
            if len(matches) > 0:
                colors['primary'] = matches[0]
            if len(matches) > 1:
                colors['secondary'] = matches[1]
            if len(matches) > 2:
                colors['accent'] = matches[2]

        # If no CSS vars found, try to extract from inline styles
        if not matches or len(matches) < 3:
            # Look for common color patterns
            color_pattern = r'#[0-9a-fA-F]{6}'
            all_colors = re.findall(color_pattern, content)
            if all_colors:
                # Use first few unique colors
                unique_colors = list(dict.fromkeys(all_colors))[:3]
                if len(unique_colors) > 0:
                    colors['primary'] = unique_colors[0]
                if len(unique_colors) > 1:
                    colors['secondary'] = unique_colors[1]
                if len(unique_colors) > 2:
                    colors['accent'] = unique_colors[2]

    except Exception as e:
        print(f"Warning: Could not extract colors from HTML: {e}", file=sys.stderr)

    return colors


def extract_images_from_html(html_file: str) -> List[Dict[str, str]]:
    """Extract image information from HTML file.

    Args:
        html_file: Path to the HTML file

    Returns:
        List of dictionaries with image info
    """
    images = []

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract img tags
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        img_matches = re.findall(img_pattern, content, re.IGNORECASE)

        for src in img_matches:
            # Extract filename from path
            filename = src.split('/')[-1]

            # Determine resolution based on filename
            resolution = '1K'
            if '4k' in filename.lower() or 'large' in filename.lower():
                resolution = '4K'
            elif '2k' in filename.lower() or 'medium' in filename.lower():
                resolution = '2K'

            images.append({
                'filename': filename,
                'resolution': resolution,
                'purpose': '页面图片'
            })

        # Extract background images from CSS
        bg_img_pattern = r'background-image:\s*url\(["\']?([^"\')]+)["\']?\)'
        bg_matches = re.findall(bg_img_pattern, content, re.IGNORECASE)

        for src in bg_matches:
            filename = src.split('/')[-1]
            images.append({
                'filename': filename,
                'resolution': '2K',
                'purpose': '背景图片'
            })

    except Exception as e:
        print(f"Warning: Could not extract images from HTML: {e}", file=sys.stderr)

    return images


def count_ctas_from_html(html_file: str) -> int:
    """Count CTA buttons in HTML file.

    Args:
        html_file: Path to the HTML file

    Returns:
        Number of CTA buttons found
    """
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count buttons and links with CTA-related classes or text
        cta_count = 0

        # Count button tags
        buttons = re.findall(r'<button[^>]*>', content, re.IGNORECASE)
        cta_count += len(buttons)

        # Count anchor tags with common CTA classes
        cta_links = re.findall(r'<a[^>]*class=["\'][^"\']*(?:btn|button|cta)[^"\']*["\'][^>]*>', content, re.IGNORECASE)
        cta_count += len(cta_links)

        # Count links with CTA-related text
        cta_text_pattern = r'<a[^>]*>(?:立即|点击|马上|了解更多|联系我们|注册|登录|购买|预订)[^<]*</a>'
        cta_text_matches = re.findall(cta_text_pattern, content, re.IGNORECASE)
        cta_count += len(cta_text_matches)

        return cta_count

    except Exception as e:
        print(f"Warning: Could not count CTAs from HTML: {e}", file=sys.stderr)
        return 0


def create_design_doc(
    project_name: str,
    design_concept: str = "",
    target_audience: str = "",
    primary_color: str = "#0a2540",
    secondary_color: str = "#1e3a5f",
    accent_color: str = "#ff6b2c",
    bg_color: str = "#f7fafc",
    typography: str = "",
    design_goals: str = "",
    page_sections: str = "",
    image_list: str = "",
    cta_count: str = "",
    tech_stack: str = "",
    features: str = "",
    css_file: str = "",
    author: str = "Web Design Studio",
    project_type: str = "website",
    version: str = "1.0",
    html_file: Optional[str] = None
) -> str:
    """Generate professional HTML design documentation.

    Args:
        html_file: Optional path to HTML file for auto-extraction of content
    """
    # Auto-extract from HTML if provided
    if html_file:
        print(f"📖 Analyzing HTML file: {html_file}")

        # Extract sections
        extracted_sections = extract_sections_from_html(html_file)
        if extracted_sections and not page_sections:
            page_sections = ','.join([s['name'] for s in extracted_sections[:10]])
            print(f"✓ Extracted {len(extracted_sections)} sections")

        # Extract colors
        extracted_colors = extract_colors_from_html(html_file)
        if not any([primary_color == "#0a2540", secondary_color == "#1e3a5f",
                   accent_color == "#ff6b2c", bg_color == "#f7fafc"]):
            # User provided custom colors, don't override
            pass
        else:
            primary_color = extracted_colors['primary']
            secondary_color = extracted_colors['secondary']
            accent_color = extracted_colors['accent']
            bg_color = extracted_colors['bg']
            print(f"✓ Extracted color scheme")

        # Extract images
        extracted_images = extract_images_from_html(html_file)
        if extracted_images and not image_list:
            image_list = ','.join([f"{img['filename']}|{img['resolution']}|{img['purpose']}"
                                   for img in extracted_images])
            print(f"✓ Extracted {len(extracted_images)} images")

        # Count CTAs
        if not cta_count:
            cta_num = count_ctas_from_html(html_file)
            if cta_num > 0:
                cta_count = str(cta_num)
                print(f"✓ Found {cta_num} CTA buttons")

    # Get current date
    now = datetime.now()
    current_date = now.strftime("%Y年%m月%d日")
    current_year = now.year

    # Parse page sections
    sections_list = []
    if page_sections:
        sections_list = [(i + 1, s.strip()) for i, s in enumerate(page_sections.split(',')) if s.strip()]

    # Parse image list
    images = []
    if image_list:
        for img in image_list.split(','):
            img = img.strip()
            if '|' in img:
                parts = img.split('|')
                if len(parts) >= 2:
                    images.append({
                        'filename': parts[0].strip(),
                        'resolution': parts[1].strip(),
                        'purpose': parts[2].strip() if len(parts) > 2 else ""
                    })

    # Build HTML - using string concatenation for better compatibility
    html_parts = []

    # HTML header
    html_parts.append('<!DOCTYPE html>')
    html_parts.append('<html lang="zh-CN">')
    html_parts.append('<head>')
    html_parts.append('    <meta charset="UTF-8">')
    html_parts.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_parts.append(f'    <title>{project_name} - 设计说明文档</title>')
    html_parts.append('    <style>')
    html_parts.append('        :root {')
    html_parts.append(f'            --primary: {primary_color};')
    html_parts.append(f'            --secondary: {secondary_color};')
    html_parts.append(f'            --accent: {accent_color};')
    html_parts.append('            --text: #1a1a1a;')
    html_parts.append('            --text-light: #4a5568;')
    html_parts.append(f'            --bg: {bg_color};')
    html_parts.append('            --white: #ffffff;')
    html_parts.append('            --border: #e2e8f0;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        * {')
    html_parts.append('            margin: 0;')
    html_parts.append('            padding: 0;')
    html_parts.append('            box-sizing: border-box;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        body {')
    html_parts.append('            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif;')
    html_parts.append('            line-height: 1.8;')
    html_parts.append('            color: var(--text);')
    html_parts.append('            background: var(--bg);')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        /* Header */')
    html_parts.append('        .doc-header {')
    html_parts.append(f'            background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);')
    html_parts.append('            color: var(--white);')
    html_parts.append('            padding: 100px 0 80px;')
    html_parts.append('            position: relative;')
    html_parts.append('            overflow: hidden;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .doc-header::before {')
    html_parts.append('            content: "";')
    html_parts.append('            position: absolute;')
    html_parts.append('            top: 0; left: 0; right: 0; bottom: 0;')
    html_parts.append('            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);')
    html_parts.append('            opacity: 0.5;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .header-content {')
    html_parts.append('            max-width: 1200px;')
    html_parts.append('            margin: 0 auto;')
    html_parts.append('            padding: 0 40px;')
    html_parts.append('            position: relative;')
    html_parts.append('            z-index: 1;')
    html_parts.append('            text-align: center;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .doc-badge {')
    html_parts.append('            display: inline-block;')
    html_parts.append('            background: rgba(255,255,255,0.2);')
    html_parts.append('            padding: 8px 20px;')
    html_parts.append('            border-radius: 20px;')
    html_parts.append('            font-size: 14px;')
    html_parts.append('            font-weight: 600;')
    html_parts.append('            margin-bottom: 24px;')
    html_parts.append('            letter-spacing: 1px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .doc-header h1 {')
    html_parts.append('            font-size: 52px;')
    html_parts.append('            font-weight: 800;')
    html_parts.append('            line-height: 1.2;')
    html_parts.append('            margin-bottom: 24px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .doc-header .subtitle {')
    html_parts.append('            font-size: 22px;')
    html_parts.append('            opacity: 0.9;')
    html_parts.append('            margin-bottom: 40px;')
    html_parts.append('            font-weight: 300;')
    html_parts.append('            color: #fff;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .doc-meta {')
    html_parts.append('            display: flex;')
    html_parts.append('            gap: 40px;')
    html_parts.append('            flex-wrap: wrap;')
    html_parts.append('            opacity: 0.85;')
    html_parts.append('            font-size: 15px;')
    html_parts.append('            justify-content: center;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .doc-meta-item {')
    html_parts.append('            display: flex;')
    html_parts.append('            align-items: center;')
    html_parts.append('            gap: 8px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        /* Navigation */')
    html_parts.append('        .sticky-nav {')
    html_parts.append('            background: var(--white);')
    html_parts.append('            border-bottom: 1px solid var(--border);')
    html_parts.append('            position: sticky;')
    html_parts.append('            top: 0;')
    html_parts.append('            z-index: 1000;')
    html_parts.append('            box-shadow: 0 2px 8px rgba(0,0,0,0.06);')
    html_parts.append('            display: flex;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .nav-content {')
    html_parts.append('            max-width: 1200px;')
    html_parts.append('            margin: 0 auto;')
    html_parts.append('            padding: 0 40px;')
    html_parts.append('            display: flex;')
    html_parts.append('            gap: 8px;')
    html_parts.append('            overflow-x: auto;')
    html_parts.append('            scrollbar-width: none;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .nav-content::-webkit-scrollbar {')
    html_parts.append('            display: none;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .nav-link {')
    html_parts.append('            padding: 20px 24px;')
    html_parts.append('            color: var(--text-light);')
    html_parts.append('            text-decoration: none;')
    html_parts.append('            font-weight: 500;')
    html_parts.append('            font-size: 14px;')
    html_parts.append('            white-space: nowrap;')
    html_parts.append('            border-bottom: 3px solid transparent;')
    html_parts.append('            transition: all 0.3s;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .nav-link:hover {')
    html_parts.append(f'            color: {primary_color};')
    html_parts.append(f'            border-bottom-color: {accent_color};')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        /* Content */')
    html_parts.append('        .content {')
    html_parts.append('            max-width: 1200px;')
    html_parts.append('            margin: 0 auto;')
    html_parts.append('            padding: 80px 40px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .section {')
    html_parts.append('            margin-bottom: 100px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .section-number {')
    html_parts.append('            display: inline-block;')
    html_parts.append('            width: 48px;')
    html_parts.append('            height: 48px;')
    html_parts.append(f'            background: linear-gradient(135deg, {accent_color} 0%, #e55a1f 100%);')
    html_parts.append('            color: var(--white);')
    html_parts.append('            border-radius: 12px;')
    html_parts.append('            font-size: 24px;')
    html_parts.append('            font-weight: 700;')
    html_parts.append('            display: flex;')
    html_parts.append('            align-items: center;')
    html_parts.append('            justify-content: center;')
    html_parts.append('            margin-bottom: 24px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .section-title {')
    html_parts.append('            font-size: 38px;')
    html_parts.append('            font-weight: 700;')
    html_parts.append(f'            color: {primary_color};')
    html_parts.append('            margin-bottom: 32px;')
    html_parts.append('            line-height: 1.3;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .subsection-title {')
    html_parts.append('            font-size: 26px;')
    html_parts.append('            font-weight: 600;')
    html_parts.append(f'            color: {secondary_color};')
    html_parts.append('            margin-top: 48px;')
    html_parts.append('            margin-bottom: 20px;')
    html_parts.append('            padding-left: 16px;')
    html_parts.append(f'            border-left: 4px solid {accent_color};')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        p {')
    html_parts.append('            margin-bottom: 16px;')
    html_parts.append('            color: var(--text-light);')
    html_parts.append('            font-size: 16px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .info-box {')
    html_parts.append(f'            background: linear-gradient(135deg, rgba(10,37,64,0.05) 0%, rgba(30,58,95,0.03) 100%);')
    html_parts.append(f'            border-left: 4px solid {accent_color};')
    html_parts.append('            padding: 24px;')
    html_parts.append('            border-radius: 0 12px 12px 0;')
    html_parts.append('            margin: 32px 0;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .info-box h4 {')
    html_parts.append(f'            color: {primary_color};')
    html_parts.append('            margin-bottom: 12px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .features-grid {')
    html_parts.append('            display: grid;')
    html_parts.append('            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));')
    html_parts.append('            gap: 24px;')
    html_parts.append('            margin: 32px 0;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .feature-card {')
    html_parts.append('            background: var(--white);')
    html_parts.append('            padding: 28px;')
    html_parts.append('            border-radius: 12px;')
    html_parts.append('            border: 1px solid var(--border);')
    html_parts.append('            transition: all 0.3s;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .feature-card:hover {')
    html_parts.append('            box-shadow: 0 8px 24px rgba(0,0,0,0.08);')
    html_parts.append('            transform: translateY(-2px);')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .feature-icon {')
    html_parts.append('            width: 56px;')
    html_parts.append('            height: 56px;')
    html_parts.append('            background: linear-gradient(135deg, rgba(255,107,44,0.1) 0%, rgba(255,107,44,0.05) 100%);')
    html_parts.append('            border-radius: 12px;')
    html_parts.append('            display: flex;')
    html_parts.append('            align-items: center;')
    html_parts.append('            justify-content: center;')
    html_parts.append('            font-size: 28px;')
    html_parts.append('            margin-bottom: 16px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .feature-card h4 {')
    html_parts.append(f'            color: {primary_color};')
    html_parts.append('            margin-bottom: 12px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .color-palette {')
    html_parts.append('            display: grid;')
    html_parts.append('            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));')
    html_parts.append('            gap: 20px;')
    html_parts.append('            margin: 32px 0;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .color-card {')
    html_parts.append('            border-radius: 12px;')
    html_parts.append('            overflow: hidden;')
    html_parts.append('            box-shadow: 0 4px 12px rgba(0,0,0,0.08);')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .color-sample {')
    html_parts.append('            height: 120px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .color-info {')
    html_parts.append('            background: var(--white);')
    html_parts.append('            padding: 20px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .color-info h4 {')
    html_parts.append(f'            color: {primary_color};')
    html_parts.append('            margin-bottom: 8px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .color-info p {')
    html_parts.append('            font-size: 14px;')
    html_parts.append('            margin: 4px 0;')
    html_parts.append('            color: var(--text-light);')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .page-structure {')
    html_parts.append('            background: var(--white);')
    html_parts.append('            border-radius: 16px;')
    html_parts.append('            padding: 40px;')
    html_parts.append('            margin: 32px 0;')
    html_parts.append('            border: 1px solid var(--border);')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .structure-item {')
    html_parts.append('            display: flex;')
    html_parts.append('            gap: 20px;')
    html_parts.append('            padding: 24px 0;')
    html_parts.append('            border-bottom: 1px solid var(--border);')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .structure-item:last-child {')
    html_parts.append('            border-bottom: none;')
    html_parts.append('            padding-bottom: 0;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .structure-item:first-child {')
    html_parts.append('            padding-top: 0;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .structure-number {')
    html_parts.append('            width: 40px;')
    html_parts.append('            height: 40px;')
    html_parts.append(f'            background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);')
    html_parts.append('            color: var(--white);')
    html_parts.append('            border-radius: 10px;')
    html_parts.append('            display: flex;')
    html_parts.append('            align-items: center;')
    html_parts.append('            justify-content: center;')
    html_parts.append('            font-weight: 700;')
    html_parts.append('            flex-shrink: 0;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .structure-content h4 {')
    html_parts.append(f'            color: {primary_color};')
    html_parts.append('            margin-bottom: 8px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .structure-content .tag {')
    html_parts.append('            display: inline-block;')
    html_parts.append('            background: rgba(255,107,44,0.1);')
    html_parts.append(f'            color: {accent_color};')
    html_parts.append('            padding: 4px 12px;')
    html_parts.append('            border-radius: 6px;')
    html_parts.append('            font-size: 12px;')
    html_parts.append('            font-weight: 600;')
    html_parts.append('            margin-bottom: 12px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .data-table {')
    html_parts.append('            width: 100%;')
    html_parts.append('            border-collapse: collapse;')
    html_parts.append('            background: var(--white);')
    html_parts.append('            border-radius: 12px;')
    html_parts.append('            overflow: hidden;')
    html_parts.append('            box-shadow: 0 4px 12px rgba(0,0,0,0.05);')
    html_parts.append('            margin: 32px 0;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .data-table th {')
    html_parts.append(f'            background: {primary_color};')
    html_parts.append('            color: var(--white);')
    html_parts.append('            padding: 16px 20px;')
    html_parts.append('            text-align: left;')
    html_parts.append('            font-weight: 600;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .data-table td {')
    html_parts.append('            padding: 16px 20px;')
    html_parts.append('            border-bottom: 1px solid var(--border);')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .data-table tr:last-child td {')
    html_parts.append('            border-bottom: none;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .data-table tr:hover {')
    html_parts.append('            background: var(--bg);')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .checklist {')
    html_parts.append('            list-style: none;')
    html_parts.append('            padding: 0;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .checklist li {')
    html_parts.append('            display: flex;')
    html_parts.append('            align-items: flex-start;')
    html_parts.append('            gap: 12px;')
    html_parts.append('            padding: 16px 0;')
    html_parts.append('            border-bottom: 1px solid var(--border);')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .checklist li:last-child {')
    html_parts.append('            border-bottom: none;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .checklist li::before {')
    html_parts.append('            content: "✓";')
    html_parts.append('            width: 28px;')
    html_parts.append('            height: 28px;')
    html_parts.append('            background: #10b981;')
    html_parts.append('            color: var(--white);')
    html_parts.append('            border-radius: 50%;')
    html_parts.append('            display: flex;')
    html_parts.append('            align-items: center;')
    html_parts.append('            justify-content: center;')
    html_parts.append('            font-weight: 700;')
    html_parts.append('            flex-shrink: 0;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .checklist li.pending::before {')
    html_parts.append('            content: "⏳";')
    html_parts.append(f'            background: {accent_color};')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .doc-footer {')
    html_parts.append(f'            background: {primary_color};')
    html_parts.append('            color: var(--white);')
    html_parts.append('            padding: 60px 40px;')
    html_parts.append('            text-align: center;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .footer-content {')
    html_parts.append('            max-width: 1200px;')
    html_parts.append('            margin: 0 auto;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .footer-logo {')
    html_parts.append('            font-size: 24px;')
    html_parts.append('            font-weight: 700;')
    html_parts.append('            margin-bottom: 16px;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        .footer-info {')
    html_parts.append('            opacity: 0.8;')
    html_parts.append('            font-size: 14px;')
    html_parts.append('            color: #fff;')
    html_parts.append('        }')
    html_parts.append('')
    html_parts.append('        @media (max-width: 768px) {')
    html_parts.append('            .doc-header h1 { font-size: 36px; }')
    html_parts.append('            .section-title { font-size: 28px; }')
    html_parts.append('            .content { padding: 40px 20px; }')
    html_parts.append('        }')
    html_parts.append('    </style>')
    html_parts.append('</head>')
    html_parts.append('<body>')
    html_parts.append('    <!-- Header -->')
    html_parts.append('    <header class="doc-header">')
    html_parts.append('        <div class="header-content">')
    html_parts.append(f'            <span class="doc-badge">设计文档 V{version}</span>')
    html_parts.append(f'            <h1>{project_name}<br>设计说明文档</h1>')
    html_parts.append(f'            <p class="subtitle">专业{project_type}设计 · 高质量交付标准</p>')
    html_parts.append('            <div class="doc-meta">')
    html_parts.append('                <div class="doc-meta-item">')
    html_parts.append('                    <span>📅</span>')
    html_parts.append(f'                    <span>{current_date}</span>')
    html_parts.append('                </div>')
    html_parts.append('                <div class="doc-meta-item">')
    html_parts.append('                    <span>👨‍💻</span>')
    html_parts.append(f'                    <span>{author}</span>')
    html_parts.append('                </div>')
    html_parts.append('                <div class="doc-meta-item">')
    html_parts.append('                    <span>📄</span>')
    html_parts.append('                    <span>设计交付文档</span>')
    html_parts.append('                </div>')
    html_parts.append('            </div>')
    html_parts.append('        </div>')
    html_parts.append('    </header>')

    # Navigation
    html_parts.append('    <!-- Navigation -->')
    html_parts.append('    <nav class="sticky-nav">')
    html_parts.append('        <div class="nav-content">')
    html_parts.append('            <a href="#overview" class="nav-link">设计概述</a>')
    html_parts.append('            <a href="#visual" class="nav-link">视觉设计</a>')
    html_parts.append('            <a href="#structure" class="nav-link">页面结构</a>')
    html_parts.append('            <a href="#ux" class="nav-link">用户体验</a>')
    html_parts.append('            <a href="#tech" class="nav-link">技术实现</a>')
    html_parts.append('            <a href="#deliver" class="nav-link">交付清单</a>')
    html_parts.append('        </div>')
    html_parts.append('    </nav>')

    # Main Content
    html_parts.append('    <!-- Content -->')
    html_parts.append('    <main class="content">')

    # Section 1: Overview
    html_parts.append('        <!-- Section 1 -->')
    html_parts.append('        <section class="section" id="overview">')
    html_parts.append('            <div class="section-number">01</div>')
    html_parts.append('            <h2 class="section-title">设计概述</h2>')
    html_parts.append('            <div class="info-box">')
    html_parts.append('                <h4>核心理念</h4>')
    concept = design_concept if design_concept else "本设计旨在创造独特而难忘的用户体验，通过精心策划的视觉语言和交互流程，传达品牌核心价值。"
    html_parts.append(f'                <p>{concept}</p>')
    html_parts.append('            </div>')
    html_parts.append('            <h3 class="subsection-title">设计目标</h3>')
    html_parts.append('            <div class="features-grid">')
    html_parts.append('                <div class="feature-card">')
    html_parts.append('                    <div class="feature-icon">🎯</div>')
    html_parts.append('                    <h4>建立品牌认知</h4>')
    html_parts.append('                    <p>通过独特的视觉设计风格，建立专业的品牌形象</p>')
    html_parts.append('                </div>')
    html_parts.append('                <div class="feature-card">')
    html_parts.append('                    <div class="feature-icon">📈</div>')
    html_parts.append('                    <h4>促进业务转化</h4>')
    html_parts.append('                    <p>优化用户旅程，设置合理的转化路径</p>')
    html_parts.append('                </div>')
    html_parts.append('                <div class="feature-card">')
    html_parts.append('                    <div class="feature-icon">💎</div>')
    html_parts.append('                    <h4>传递核心价值</h4>')
    html_parts.append('                    <p>清晰展示产品/服务的核心优势</p>')
    html_parts.append('                </div>')
    html_parts.append('                <div class="feature-card">')
    html_parts.append('                    <div class="feature-icon">⚡</div>')
    html_parts.append('                    <h4>提升用户体验</h4>')
    html_parts.append('                    <p>流畅的交互设计、响应式布局</p>')
    html_parts.append('                </div>')
    html_parts.append('            </div>')
    html_parts.append('            <h3 class="subsection-title">目标受众</h3>')
    audience = target_audience if target_audience else "本设计针对目标用户群体进行深度定制，充分考虑用户需求和行为习惯。"
    html_parts.append(f'            <p>{audience}</p>')
    html_parts.append('        </section>')

    # Section 2: Visual Design
    html_parts.append('        <!-- Section 2 -->')
    html_parts.append('        <section class="section" id="visual">')
    html_parts.append('            <div class="section-number">02</div>')
    html_parts.append('            <h2 class="section-title">视觉设计策略</h2>')
    html_parts.append('            <h3 class="subsection-title">色彩系统</h3>')
    html_parts.append('            <div class="color-palette">')
    html_parts.append(f'                <div class="color-card">')
    html_parts.append(f'                    <div class="color-sample" style="background: {primary_color};"></div>')
    html_parts.append('                    <div class="color-info">')
    html_parts.append('                        <h4>主色调</h4>')
    html_parts.append(f'                        <p><strong>主色 {primary_color}</strong></p>')
    html_parts.append('                        <p>品牌主色，传递专业感</p>')
    html_parts.append('                    </div>')
    html_parts.append('                </div>')
    html_parts.append(f'                <div class="color-card">')
    html_parts.append(f'                    <div class="color-sample" style="background: {secondary_color};"></div>')
    html_parts.append('                    <div class="color-info">')
    html_parts.append('                        <h4>辅助色</h4>')
    html_parts.append(f'                        <p><strong>辅助色 {secondary_color}</strong></p>')
    html_parts.append('                        <p>用于层次和深度</p>')
    html_parts.append('                    </div>')
    html_parts.append('                </div>')
    html_parts.append(f'                <div class="color-card">')
    html_parts.append(f'                    <div class="color-sample" style="background: {accent_color};"></div>')
    html_parts.append('                    <div class="color-info">')
    html_parts.append('                        <h4>强调色</h4>')
    html_parts.append(f'                        <p><strong>强调色 {accent_color}</strong></p>')
    html_parts.append('                        <p>用于CTA按钮和行动引导</p>')
    html_parts.append('                    </div>')
    html_parts.append('                </div>')
    html_parts.append(f'                <div class="color-card">')
    html_parts.append(f'                    <div class="color-sample" style="background: {bg_color};"></div>')
    html_parts.append('                    <div class="color-info">')
    html_parts.append('                        <h4>背景色</h4>')
    html_parts.append(f'                        <p><strong>背景色 {bg_color}</strong></p>')
    html_parts.append('                        <p>用于背景和分隔</p>')
    html_parts.append('                    </div>')
    html_parts.append('                </div>')
    html_parts.append('            </div>')
    html_parts.append('            <h3 class="subsection-title">字体设计</h3>')
    typo = typography if typography else "使用系统字体栈或精选Web字体，确保快速加载。"
    html_parts.append(f'            <p>{typo}</p>')
    html_parts.append('        </section>')

    # Section 3: Page Structure
    html_parts.append('        <!-- Section 3 -->')
    html_parts.append('        <section class="section" id="structure">')
    html_parts.append('            <div class="section-number">03</div>')
    html_parts.append('            <h2 class="section-title">页面结构设计</h2>')
    html_parts.append(f'            <p>本设计采用现代化的页面布局，共{len(sections_list) if sections_list else "多个"}功能区块。</p>')
    html_parts.append('            <div class="page-structure">')

    # Get extracted sections with content for better descriptions
    extracted_sections = []
    if html_file:
        extracted_sections = extract_sections_from_html(html_file)

    if sections_list:
        for num, section in sections_list:
            # Find matching extracted section for content
            section_content = "该区块展示相关内容，提供清晰的信息架构。"
            if extracted_sections:
                for extracted in extracted_sections:
                    if section.lower() in extracted['name'].lower() or extracted['name'].lower() in section.lower():
                        section_content = extracted['content']
                        break

            html_parts.append(f'                <div class="structure-item">')
            html_parts.append(f'                    <div class="structure-number">{num}</div>')
            html_parts.append(f'                    <div class="structure-content">')
            html_parts.append(f'                        <span class="tag">Section</span>')
            html_parts.append(f'                        <h4>{section}</h4>')
            html_parts.append(f'                        <p>{section_content}</p>')
            html_parts.append(f'                    </div>')
            html_parts.append(f'                </div>')
    else:
        html_parts.append('                <div class="structure-item">')
        html_parts.append('                    <div class="structure-number">1</div>')
        html_parts.append('                    <div class="structure-content">')
        html_parts.append('                        <span class="tag">Sticky Header</span>')
        html_parts.append('                        <h4>顶部导航区</h4>')
        html_parts.append('                        <p>固定顶部导航栏，包含品牌标识和主要链接。</p>')
        html_parts.append('                    </div>')
        html_parts.append('                </div>')
        html_parts.append('                <div class="structure-item">')
        html_parts.append('                    <div class="structure-number">2</div>')
        html_parts.append('                    <div class="structure-content">')
        html_parts.append('                        <span class="tag">Hero Section</span>')
        html_parts.append('                        <h4>首屏展示区</h4>')
        html_parts.append('                        <p>全屏高度的首屏区域，创造强烈的第一印象。</p>')
        html_parts.append('                    </div>')
        html_parts.append('                </div>')

    html_parts.append('                <div class="structure-item">')
    html_parts.append('                    <div class="structure-number">' + str(len(sections_list) + 2 if sections_list else 3) + '</div>')
    html_parts.append('                    <div class="structure-content">')
    html_parts.append('                        <span class="tag">Footer</span>')
    html_parts.append('                        <h4>页脚区</h4>')
    html_parts.append('                        <p>包含版权信息和链接导航。</p>')
    html_parts.append('                    </div>')
    html_parts.append('                </div>')
    html_parts.append('            </div>')
    html_parts.append('        </section>')

    # Section 4: UX
    html_parts.append('        <!-- Section 4 -->')
    html_parts.append('        <section class="section" id="ux">')
    html_parts.append('            <div class="section-number">04</div>')
    html_parts.append('            <h2 class="section-title">用户体验设计</h2>')
    html_parts.append('            <h3 class="subsection-title">交互设计</h3>')
    html_parts.append('            <div class="features-grid">')
    html_parts.append('                <div class="feature-card"><div class="feature-icon">🔄</div><h4>平滑滚动</h4><p>锚点链接平滑滚动</p></div>')
    html_parts.append('                <div class="feature-card"><div class="feature-icon">✨</div><h4>滚动动画</h4><p>元素进入视口时的动画</p></div>')
    html_parts.append('                <div class="feature-card"><div class="feature-icon">👆</div><h4>悬停效果</h4><p>丰富的悬停反馈</p></div>')
    html_parts.append('                <div class="feature-card"><div class="feature-icon">📝</div><h4>表单验证</h4><p>实时验证和反馈</p></div>')
    html_parts.append('            </div>')
    html_parts.append('            <h3 class="subsection-title">响应式设计</h3>')
    html_parts.append('            <table class="data-table">')
    html_parts.append('                <thead><tr><th>设备类型</th><th>屏幕宽度</th><th>布局特点</th></tr></thead>')
    html_parts.append('                <tbody>')
    html_parts.append('                    <tr><td><strong>桌面端</strong></td><td>&gt; 992px</td><td>多栏布局</td></tr>')
    html_parts.append('                    <tr><td><strong>平板端</strong></td><td>768px - 992px</td><td>自适应网格</td></tr>')
    html_parts.append('                    <tr><td><strong>移动端</strong></td><td>&lt; 768px</td><td>单栏堆叠</td></tr>')
    html_parts.append('                </tbody>')
    html_parts.append('            </table>')
    html_parts.append('        </section>')

    # Section 5: Technical
    html_parts.append('        <!-- Section 5 -->')
    html_parts.append('        <section class="section" id="tech">')
    html_parts.append('            <div class="section-number">05</div>')
    html_parts.append('            <h2 class="section-title">技术实现</h2>')
    html_parts.append('            <h3 class="subsection-title">技术栈</h3>')
    tech_info = tech_stack if tech_stack else "HTML5, CSS3, JavaScript, 响应式设计"
    html_parts.append(f'            <p>{tech_info}</p>')
    html_parts.append('            <h3 class="subsection-title">代码特点</h3>')
    html_parts.append('            <div class="features-grid">')
    html_parts.append('                <div class="feature-card"><div class="feature-icon">⚡</div><h4>轻量级</h4><p>无框架依赖</p></div>')
    html_parts.append('                <div class="feature-card"><div class="feature-icon">🔧</div><h4>易维护</h4><p>代码结构清晰</p></div>')
    html_parts.append('                <div class="feature-card"><div class="feature-icon">📦</div><h4>可扩展</h4><p>模块化命名</p></div>')
    html_parts.append('                <div class="feature-card"><div class="feature-icon">🌐</div><h4>SEO友好</h4><p>语义化标签</p></div>')
    html_parts.append('            </div>')
    html_parts.append('        </section>')

    # Section 6: Deliverables
    html_parts.append('        <!-- Section 6 -->')
    html_parts.append('        <section class="section" id="deliver">')
    html_parts.append('            <div class="section-number">06</div>')
    html_parts.append('            <h2 class="section-title">交付清单</h2>')
    html_parts.append('            <h3 class="subsection-title">已交付内容</h3>')
    html_parts.append('            <ul class="checklist">')
    html_parts.append(f'                <li>完整HTML页面文件</li>')
    html_parts.append(f'                <li>{f"{len(images)}张高质量图片" if images else "所有需要的图片资源"}</li>')
    html_parts.append(f'                <li>响应式CSS样式</li>')
    html_parts.append(f'                <li>交互JavaScript代码</li>')
    html_parts.append(f'                <li>设计说明文档（本文件）</li>')
    html_parts.append('            </ul>')

    if images:
        html_parts.append('            <h3 class="subsection-title">图片资源清单</h3>')
        html_parts.append('            <table class="data-table">')
        html_parts.append('                <thead><tr><th>文件名</th><th>分辨率</th><th>用途</th></tr></thead>')
        html_parts.append('                <tbody>')
        for img in images:
            html_parts.append(f'                    <tr><td>{img["filename"]}</td><td>{img["resolution"]}</td><td>{img["purpose"]}</td></tr>')
        html_parts.append('                </tbody>')
        html_parts.append('            </table>')

    html_parts.append('            <h3 class="subsection-title">建议后续工作</h3>')
    html_parts.append('            <ul class="checklist">')
    html_parts.append('                <li class="pending">表单后端对接</li>')
    html_parts.append('                <li class="pending">域名与服务器部署</li>')
    html_parts.append('                <li class="pending">SSL证书配置</li>')
    html_parts.append('                <li class="pending">图片优化（WebP、CDN）</li>')
    html_parts.append('            </ul>')
    html_parts.append('            <h3 class="subsection-title">设计亮点总结</h3>')
    html_parts.append('            <div class="features-grid">')
    html_parts.append('                <div class="feature-card"><div class="feature-icon">🖥️</div><h4>专业视觉设计</h4><p>独特的视觉风格</p></div>')
    cta_info = f'{cta_count}+个询盘入口' if cta_count else '多转化入口'
    html_parts.append(f'                <div class="feature-card"><div class="feature-icon">🎯</div><h4>{cta_info}</h4><p>合理设置的CTA</p></div>')
    html_parts.append('                <div class="feature-card"><div class="feature-icon">📱</div><h4>全平台适配</h4><p>完美适配各种设备</p></div>')
    html_parts.append('                <div class="feature-card"><div class="feature-icon">⚡</div><h4>轻量级技术</h4><p>加载快速易维护</p></div>')
    html_parts.append('            </div>')
    html_parts.append('        </section>')

    html_parts.append('    </main>')

    # Footer
    html_parts.append('    <!-- Footer -->')
    html_parts.append('    <footer class="doc-footer">')
    html_parts.append('        <div class="footer-content">')
    html_parts.append(f'            <div class="footer-logo">{project_name}</div>')
    html_parts.append('            <p class="footer-info">')
    html_parts.append(f'                文档版本：v{version} | 最后更新：{current_date}<br>')
    html_parts.append(f'                设计单位：{author}')
    html_parts.append('            </p>')
    html_parts.append('        </div>')
    html_parts.append('    </footer>')

    # Script
    html_parts.append('    <script>')
    html_parts.append('        document.querySelectorAll(\'a[href^="#"]\').forEach(anchor => {')
    html_parts.append('            anchor.addEventListener("click", function (e) {')
    html_parts.append('                e.preventDefault();')
    html_parts.append('                const target = document.querySelector(this.getAttribute("href"));')
    html_parts.append('                if (target) {')
    html_parts.append('                    const headerOffset = 70;')
    html_parts.append('                    const elementPosition = target.getBoundingClientRect().top;')
    html_parts.append('                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;')
    html_parts.append('                    window.scrollTo({')
    html_parts.append('                        top: offsetPosition,')
    html_parts.append('                        behavior: "smooth"')
    html_parts.append('                    });')
    html_parts.append('                }')
    html_parts.append('            });')
    html_parts.append('        });')
    html_parts.append('    </script>')

    html_parts.append('</body>')
    html_parts.append('</html>')

    return '\n'.join(html_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Generate professional design documentation HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--project-name", "-p", required=True, help="Project name")
    parser.add_argument("--output", "-o", required=True, help="Output HTML filename")
    parser.add_argument("--html-file", "-H", help="HTML file to auto-extract content from")
    parser.add_argument("--design-concept", "-d", help="Design concept")
    parser.add_argument("--target-audience", "-a", help="Target audience")
    parser.add_argument("--primary-color", default="#0a2540", help="Primary color")
    parser.add_argument("--secondary-color", default="#1e3a5f", help="Secondary color")
    parser.add_argument("--accent-color", default="#ff6b2c", help="Accent color")
    parser.add_argument("--bg-color", default="#f7fafc", help="Background color")
    parser.add_argument("--typography", "-t", help="Typography")
    parser.add_argument("--design-goals", "-g", help="Design goals")
    parser.add_argument("--page-sections", "-s", help="Page sections")
    parser.add_argument("--image-list", help="Image list")
    parser.add_argument("--cta-count", help="CTA count")
    parser.add_argument("--tech-stack", help="Tech stack")
    parser.add_argument("--features", "-f", help="Features")
    parser.add_argument("--css-file", help="CSS file path")
    parser.add_argument("--author", default="Web Design Studio", help="Author")
    parser.add_argument("--project-type", default="website", help="Project type")
    parser.add_argument("--version", default="1.0", help="Version")

    args = parser.parse_args()

    try:
        validate_output_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    if not output_path.suffix:
        output_path = output_path.with_suffix('.html')

    html_content = create_design_doc(
        project_name=args.project_name,
        design_concept=args.design_concept or "",
        target_audience=args.target_audience or "",
        primary_color=args.primary_color,
        secondary_color=args.secondary_color,
        accent_color=args.accent_color,
        bg_color=args.bg_color,
        typography=args.typography or "",
        design_goals=args.design_goals or "",
        page_sections=args.page_sections or "",
        image_list=args.image_list or "",
        cta_count=args.cta_count or "",
        tech_stack=args.tech_stack or "",
        features=args.features or "",
        css_file=args.css_file or "",
        author=args.author,
        project_type=args.project_type,
        version=args.version,
        html_file=args.html_file
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Design documentation generated: {output_path}")
    print(f"📄 Open in browser: file://{output_path.resolve()}")


if __name__ == "__main__":
    main()
