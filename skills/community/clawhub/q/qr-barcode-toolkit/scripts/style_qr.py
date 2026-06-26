#!/usr/bin/env python3
"""
qr-code-toolkit/scripts/style_qr.py
二维码美化工具 - 添加logo、改变颜色、样式
"""

import argparse
import os

import qrcode
from PIL import Image


def add_logo(qr_path: str, logo_path: str, output_path: str, logo_ratio: float = 0.25):
    """Add a logo to the center of a QR code"""
    
    qr_img = Image.open(qr_path).convert('RGBA')
    logo_img = Image.open(logo_path).convert('RGBA')
    
    # Calculate logo size
    qr_width, qr_height = qr_img.size
    logo_size = int(min(qr_width, qr_height) * logo_ratio)
    
    # Resize logo
    logo_img = logo_img.resize((logo_size, logo_size))
    
    # Create a white background for the logo area
    logo_bg = Image.new('RGBA', (logo_size + 10, logo_size + 10), (255, 255, 255, 255))
    
    # Calculate position
    pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
    
    # Paste logo background first
    bg_pos = ((qr_width - logo_size - 10) // 2, (qr_height - logo_size - 10) // 2)
    qr_img.paste(logo_bg, bg_pos, logo_bg)
    
    # Paste logo
    qr_img.paste(logo_img, pos, logo_img)
    
    qr_img.save(output_path)
    print(f"Styled QR with logo: {output_path}")
    
    return output_path


def change_colors(qr_path: str, output_path: str, fg_color: str = '#000000',
                  bg_color: str = '#FFFFFF', gradient: bool = False):
    """Change QR code colors"""
    
    img = Image.open(qr_path).convert('RGBA')
    
    # Create new image with target colors
    new_img = Image.new('RGBA', img.size, bg_color)
    
    # Replace black pixels with foreground color
    pixels = img.load()
    new_pixels = new_img.load()
    
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if r < 128 and g < 128 and b < 128:
                new_pixels[x, y] = fg_color
    
    new_img.save(output_path)
    print(f"Recolored QR: {output_path}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Style QR code')
    parser.add_argument('input', help='Input QR code image')
    parser.add_argument('--output', '-o', required=True, help='Output path')
    parser.add_argument('--logo', '-l', help='Logo image to add')
    parser.add_argument('--logo-ratio', type=float, default=0.25,
                        help='Logo size ratio to QR code')
    parser.add_argument('--fg-color', help='Foreground color (hex)')
    parser.add_argument('--bg-color', help='Background color (hex)')
    args = parser.parse_args()
    
    if args.logo:
        add_logo(args.input, args.logo, args.output, args.logo_ratio)
    elif args.fg_color or args.bg_color:
        change_colors(args.input, args.output,
                     args.fg_color or '#000000',
                     args.bg_color or '#FFFFFF')
    else:
        print("Error: specify --logo or --fg-color/--bg-color")


if __name__ == '__main__':
    main()
