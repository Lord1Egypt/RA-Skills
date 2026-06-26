#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate complete Xiaohongshu posts with multiple pages.

Usage:
    uv run gen_post.py --title "标题" --content "内容" [--output ./dir]
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def get_api_key() -> str | None:
    """Get API key from environment."""
    return os.environ.get("GEMINI_API_KEY")


def get_style_prompt(style: str) -> str:
    """Get style-specific prompt additions."""
    styles = {
        "dreamy": "soft pastel gradient background from light purple to blue, ethereal atmosphere, floating light particles, dreamy aesthetic, neural network constellation patterns",
        "tech": "dark background with neon blue and purple accents, futuristic tech patterns, circuit board elements, modern digital aesthetic",
        "minimal": "clean white background with subtle gray accents, minimalist design, simple elegant composition, lots of white space",
        "warm": "warm orange to pink gradient, cozy inviting atmosphere, soft bokeh lights, warm aesthetic"
    }
    return styles.get(style, styles["dreamy"])


def parse_content(content: str) -> list[dict]:
    """Parse content into page sections."""
    pages = []
    
    # Split by Chinese sentence endings or explicit separators
    # Look for patterns like: 我是谁。 xxx。 xxx。
    sentences = re.split(r'(?<=[。！？.!?])\s*', content.strip())
    
    current_page = {"lines": [], "type": "content"}
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Check for explicit section markers
        if any(sentence.startswith(marker) for marker in ["我是谁", "我是"]):
            if current_page["lines"]:
                pages.append(current_page)
            current_page = {"lines": [sentence], "type": "opening", "title": "我是谁"}
        
        elif re.match(r'^\d+[.．、]\s*', sentence) or "计划" in sentence[:10]:
            # Checklist items - collect them
            if current_page["type"] != "checklist":
                if current_page["lines"]:
                    pages.append(current_page)
                current_page = {"lines": [], "type": "checklist", "title": "计划清单"}
            current_page["lines"].append(sentence)
        
        elif any(kw in sentence for kw in ["感谢", "关注", "一起成长", "一起进化"]) and len(sentence) < 30:
            # Ending page
            if current_page["lines"]:
                pages.append(current_page)
            current_page = {"lines": [sentence], "type": "ending", "title": "感谢关注"}
        
        elif len(sentence) < 30 and ("是" in sentence or "的" in sentence):
            # Short impactful sentence = quote
            if current_page["lines"]:
                pages.append(current_page)
            current_page = {"lines": [sentence], "type": "quote"}
        
        else:
            current_page["lines"].append(sentence)
        
        # Check if current page is getting too long
        if len("".join(current_page["lines"])) > 80 and current_page["type"] == "content":
            pages.append(current_page)
            current_page = {"lines": [], "type": "content"}
    
    # Add the last page
    if current_page["lines"]:
        pages.append(current_page)
    
    # Convert to final format
    result = []
    for page in pages:
        text = "".join(page["lines"])
        
        if page["type"] == "opening":
            result.append({
                "type": "opening",
                "title": page.get("title", "我是谁"),
                "text": text
            })
        
        elif page["type"] == "quote":
            result.append({
                "type": "quote",
                "text": text
            })
        
        elif page["type"] == "checklist":
            items = []
            for line in page["lines"]:
                # Extract item text after number
                match = re.match(r'^\d+[.．、]\s*(.+)', line)
                if match:
                    items.append(match.group(1))
                elif line.strip():
                    items.append(line.strip())
            if items:
                result.append({
                    "type": "checklist",
                    "title": page.get("title", "计划清单"),
                    "items": items[:5]
                })
        
        elif page["type"] == "ending":
            result.append({
                "type": "ending",
                "title": page.get("title", "感谢关注"),
                "text": "一起成长，一起进化",
                "subtitle": "点击关注，见证成长之旅"
            })
        
        else:  # content
            # Check if it's a reflection
            if any(kw in text for kw in ["反思", "明白", "意识到", "感悟"]):
                result.append({
                    "type": "reflection",
                    "title": "我的反思",
                    "text": text
                })
            else:
                result.append({
                    "type": "content",
                    "title": "",
                    "text": text
                })
    
    return result


def generate_cover_prompt(title: str, subtitle: str | None, date: str, style: str) -> str:
    """Generate cover page prompt."""
    style_desc = get_style_prompt(style)
    prompt = f"""Xiaohongshu style cover design, {style_desc},
main title '{title}' in elegant Chinese calligraphy font at center,
minimalist and clean aesthetic, professional social media cover,
3:4 vertical format, high quality typography, decorative constellation network patterns"""
    
    if subtitle:
        prompt += f", subtitle '{subtitle}' below the main title"
    if date:
        prompt += f", date '{date}' at bottom of the image"
    
    prompt += ", inspiring mood, dreamy atmosphere, professional graphic design"
    return prompt


def generate_page_prompt(page: dict, style: str) -> str:
    """Generate prompt for a content page."""
    style_desc = get_style_prompt(style)
    page_type = page["type"]
    
    base_constraints = "NO phone frame NO mobile interface NO device mockup NO smartphone mockup, text directly on gradient background"
    
    if page_type == "opening":
        return f"""Xiaohongshu style content page, {style_desc},
page title '{page['title']}' at top in elegant Chinese font,
body text '{page['text']}' in clean readable Chinese typography,
{base_constraints}, minimalist design, professional social media layout, 3:4 vertical format"""
    
    elif page_type == "quote":
        return f"""Xiaohongshu style quote card, {style_desc},
quote text '{page['text']}' in large elegant Chinese calligraphy centered,
{base_constraints}, quotation mark decorations, inspirational mood, 3:4 vertical format"""
    
    elif page_type == "reflection":
        return f"""Xiaohongshu reflection page, watercolor aesthetic, {style_desc},
title '{page['title']}' at top, reflection text '{page['text']}' in elegant typography,
{base_constraints}, decorative botanical elements, thoughtful mood, 3:4 vertical format"""
    
    elif page_type == "checklist":
        items_text = ", ".join([f"{i+1}. {item}" for i, item in enumerate(page['items'])])
        return f"""Xiaohongshu checklist page, {style_desc},
title '{page['title']}' at top, items '{items_text}' with checkmark icons,
{base_constraints}, clean modern layout, colorful accents, 3:4 vertical format"""
    
    elif page_type == "ending":
        subtitle = page.get('subtitle', '')
        return f"""Xiaohongshu ending page, {style_desc},
title '{page['title']}' in elegant font, message '{page['text']}',
{base_constraints}, growth visualization element, subtitle '{subtitle}' at bottom,
professional design, 3:4 vertical format, inspiring closing mood"""
    
    else:  # content
        title = page.get('title', '')
        text = page['text']
        if title:
            return f"""Xiaohongshu content page, {style_desc},
title '{title}' at top, body text '{text}' in readable typography,
{base_constraints}, clean layout, professional design, 3:4 vertical format"""
        else:
            return f"""Xiaohongshu content page, {style_desc},
main text '{text}' prominently displayed in elegant Chinese typography,
{base_constraints}, professional social media design, 3:4 vertical format"""


def generate_image(client, prompt: str, output_path: Path) -> bool:
    """Generate a single image using Gemini API."""
    from google.genai import types
    from PIL import Image as PILImage
    from io import BytesIO
    
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(image_size="2K")
            )
        )
        
        for part in response.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    import base64
                    image_data = base64.b64decode(image_data)
                
                image = PILImage.open(BytesIO(image_data))
                
                # Ensure RGB mode
                if image.mode == 'RGBA':
                    rgb_image = PILImage.new('RGB', image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[3])
                    rgb_image.save(str(output_path), 'PNG')
                elif image.mode == 'RGB':
                    image.save(str(output_path), 'PNG')
                else:
                    image.convert('RGB').save(str(output_path), 'PNG')
                return True
        
        return False
        
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate complete Xiaohongshu posts with multiple pages"
    )
    parser.add_argument(
        "--title", "-t",
        required=True,
        help="Post title"
    )
    parser.add_argument(
        "--content", "-c",
        required=True,
        help="Main content text"
    )
    parser.add_argument(
        "--subtitle", "-s",
        help="Subtitle for cover"
    )
    parser.add_argument(
        "--date", "-d",
        default=datetime.now().strftime("%Y.%m.%d"),
        help="Date string (default: today)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output directory (default: auto-generated)"
    )
    parser.add_argument(
        "--style", "-st",
        choices=["dreamy", "tech", "minimal", "warm"],
        default="dreamy",
        help="Visual style"
    )
    parser.add_argument(
        "--max-pages", "-m",
        type=int,
        default=10,
        help="Maximum number of pages (default: 10)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key()
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    # Import here
    from google import genai
    
    client = genai.Client(api_key=api_key)

    # Setup output directory
    if args.output:
        output_dir = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d")
        clean_title = "".join(c for c in args.title if c.isalnum() or c in "_-")[:15]
        output_dir = Path(f"xhs-post-{timestamp}-{clean_title}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")

    # Parse content into pages
    pages = parse_content(args.content)
    total_pages = min(len(pages) + 1, args.max_pages)  # +1 for cover
    
    print(f"\nGenerating {total_pages} pages...")
    print("-" * 40)

    # Generate cover
    print("Generating cover...")
    cover_prompt = generate_cover_prompt(args.title, args.subtitle, args.date, args.style)
    cover_path = output_dir / "01-cover.png"
    if generate_image(client, cover_prompt, cover_path):
        print(f"✅ 01-cover.png")
    else:
        print(f"❌ Failed to generate cover")

    # Generate content pages
    for i, page in enumerate(pages[:args.max_pages-1], start=2):
        page_type = page["type"]
        print(f"Generating page {i} ({page_type})...")
        
        prompt = generate_page_prompt(page, args.style)
        output_path = output_dir / f"{i:02d}-{page_type}.png"
        
        if generate_image(client, prompt, output_path):
            print(f"✅ {output_path.name}")
        else:
            print(f"❌ Failed to generate page {i}")

    print("-" * 40)
    print(f"\n✅ Complete! Generated {total_pages} pages in {output_dir}")
    print(f"\nFiles:")
    for f in sorted(output_dir.glob("*.png")):
        size = f.stat().st_size / 1024  # KB
        print(f"  • {f.name} ({size:.1f} KB)")


if __name__ == "__main__":
    main()
