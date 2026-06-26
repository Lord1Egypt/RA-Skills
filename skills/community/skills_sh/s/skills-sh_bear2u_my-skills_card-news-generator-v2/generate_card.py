#!/usr/bin/env python3
"""
Card News Generator
Creates beautiful social media card images with Korean text support
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import sys


def resize_and_crop(img, target_width, target_height):
    """
    Resize and crop image to fit target dimensions while maintaining aspect ratio
    Centers the crop
    """
    # Get current dimensions
    width, height = img.size

    # Calculate aspect ratios
    target_ratio = target_width / target_height
    current_ratio = width / height

    if current_ratio > target_ratio:
        # Image is wider than target - crop width
        new_height = target_height
        new_width = int(new_height * current_ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Crop center
        left = (new_width - target_width) // 2
        img = img.crop((left, 0, left + target_width, target_height))
    else:
        # Image is taller than target - crop height
        new_width = target_width
        new_height = int(new_width / current_ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Crop center
        top = (new_height - target_height) // 2
        img = img.crop((0, top, target_width, top + target_height))

    return img


def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width"""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]
        
        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # Word is too long, force it
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines


def create_card_news(
    title,
    content,
    output_path,
    bg_color="#F5F3EE",
    text_color="#1A1A1A",
    width=600,
    height=600,
    title_size=48,
    content_size=28,
    number=None,
    bg_image_path=None,
    overlay_opacity=0.5
):
    """
    Generate a card news image with vertically centered content

    Args:
        title: Main title text
        content: Body content text
        output_path: Path to save the image
        bg_color: Background color (hex)
        text_color: Text color (hex)
        width: Image width in pixels (default 600)
        height: Image height in pixels (default 600)
        title_size: Title font size (default 48)
        content_size: Content font size (default 28)
        number: Optional number badge (e.g., 1, 2, 3)
        bg_image_path: Optional path to background image
        overlay_opacity: Opacity of dark overlay when using background image (0.0-1.0, default 0.5)
    """

    # Create image with background
    if bg_image_path and os.path.exists(bg_image_path):
        # Load and resize background image
        try:
            bg_img = Image.open(bg_image_path)
            # Convert to RGB if necessary
            if bg_img.mode != 'RGB':
                bg_img = bg_img.convert('RGB')
            # Resize to fit canvas (crop center if aspect ratio differs)
            bg_img = resize_and_crop(bg_img, width, height)
            img = bg_img

            # Add dark overlay for better text visibility
            overlay = Image.new('RGB', (width, height), (0, 0, 0))
            img = Image.blend(img, overlay, overlay_opacity)

            # Use white text on background images
            if text_color == "#1A1A1A":  # Default dark color
                text_color = "#FFFFFF"

        except Exception as e:
            print(f"Warning: Could not load background image {bg_image_path}: {e}", file=sys.stderr)
            print("Falling back to solid color background", file=sys.stderr)
            img = Image.new('RGB', (width, height), bg_color)
    else:
        # Create image with background color
        img = Image.new('RGB', (width, height), bg_color)

    draw = ImageDraw.Draw(img)
    
    # Padding
    padding = 40
    max_text_width = width - (padding * 2)
    
    # Try to load fonts (fallback to default if not available)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", title_size)
    except:
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansKR-Bold.ttf", title_size)
        except:
            print("Warning: Korean font not found, using default font", file=sys.stderr)
            title_font = ImageFont.load_default()
    
    try:
        content_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", content_size)
    except:
        try:
            content_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansKR-Regular.ttf", content_size)
        except:
            content_font = ImageFont.load_default()
    
    try:
        number_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", 60)
    except:
        try:
            number_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansKR-Bold.ttf", 60)
        except:
            number_font = ImageFont.load_default()
    
    # Calculate total content height first
    number_height = 0
    if number is not None:
        number_text = str(number)
        bbox = draw.textbbox((0, 0), number_text, font=number_font)
        number_height = bbox[3] - bbox[1] + 40  # height + spacing
    
    # Wrap and measure title
    title_lines = []
    for line in title.split('\n'):
        wrapped = wrap_text(line, title_font, max_text_width, draw)
        title_lines.extend(wrapped)
    
    title_height = 0
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        title_height += bbox[3] - bbox[1] + 10
    
    # Wrap and measure content
    content_lines = []
    for line in content.split('\n'):
        wrapped = wrap_text(line, content_font, max_text_width, draw)
        content_lines.extend(wrapped)
    
    content_height = 0
    for line in content_lines:
        bbox = draw.textbbox((0, 0), line, font=content_font)
        content_height += bbox[3] - bbox[1] + 8
    
    # Calculate total height and starting Y position for vertical centering
    spacing_between = 30
    total_content_height = number_height + title_height + spacing_between + content_height
    start_y = (height - total_content_height) // 2
    
    current_y = start_y
    
    # Draw number badge if provided
    if number is not None:
        number_text = str(number)
        bbox = draw.textbbox((0, 0), number_text, font=number_font)
        number_width = bbox[2] - bbox[0]
        number_x = (width - number_width) // 2
        draw.text((number_x, current_y), number_text, fill=text_color, font=number_font)
        current_y += bbox[3] - bbox[1] + 40
    
    # Draw title
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        
        x = (width - line_width) // 2
        draw.text((x, current_y), line, fill=text_color, font=title_font)
        current_y += line_height + 10
    
    current_y += spacing_between  # Space between title and content
    
    # Draw content
    for line in content_lines:
        bbox = draw.textbbox((0, 0), line, font=content_font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        
        x = (width - line_width) // 2
        draw.text((x, current_y), line, fill=text_color, font=content_font)
        current_y += line_height + 8
    
    # Save image
    img.save(output_path, 'PNG', quality=95)
    print(f"Card news generated successfully: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate card news images with Korean text support'
    )
    
    # Required arguments
    parser.add_argument('--title', required=True, help='Main title text')
    parser.add_argument('--content', required=True, help='Body content text')
    parser.add_argument('--output', required=True, help='Output file path')
    
    # Optional arguments
    parser.add_argument('--bg-color', default='#F5F3EE', help='Background color (hex)')
    parser.add_argument('--text-color', default='#1A1A1A', help='Text color (hex)')
    parser.add_argument('--width', type=int, default=600, help='Image width (default: 600)')
    parser.add_argument('--height', type=int, default=600, help='Image height (default: 600)')
    parser.add_argument('--title-size', type=int, default=48, help='Title font size (default: 48)')
    parser.add_argument('--content-size', type=int, default=28, help='Content font size (default: 28)')
    parser.add_argument('--number', type=int, help='Optional number badge')
    parser.add_argument('--bg-image', help='Path to background image')
    parser.add_argument('--overlay-opacity', type=float, default=0.5, help='Opacity of dark overlay (0.0-1.0, default: 0.5)')
    
    args = parser.parse_args()

    create_card_news(
        title=args.title,
        content=args.content,
        output_path=args.output,
        bg_color=args.bg_color,
        text_color=args.text_color,
        width=args.width,
        height=args.height,
        title_size=args.title_size,
        content_size=args.content_size,
        number=args.number,
        bg_image_path=args.bg_image,
        overlay_opacity=args.overlay_opacity
    )


if __name__ == '__main__':
    main()
