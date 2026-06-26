#!/usr/bin/env python3
"""
Copy image to system clipboard for Xiaohongshu (小红书) note publishing.

Supports:
- Image files (jpg, png, gif, webp) - copies as image data
- Optional image compression before copying

Usage:
    # Copy image to clipboard
    python copy_to_clipboard.py /path/to/image.jpg

    # Copy image with compression (quality 0-100)
    python copy_to_clipboard.py /path/to/image.jpg --quality 80

macOS Requirements:
    pip install Pillow pyobjc-framework-Cocoa
"""

import argparse
import io
import os
import sys
from pathlib import Path


def compress_image(image_path: str, quality: int = 85, max_size: tuple = (2000, 2000)) -> bytes:
    """Compress image and return as bytes."""
    from PIL import Image

    img = Image.open(image_path)

    # Convert to RGB if necessary (for JPEG)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Resize if too large
    img.thumbnail(max_size, Image.Resampling.LANCZOS)

    # Save to bytes
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=quality, optimize=True)
    return buffer.getvalue()


def copy_image_to_clipboard_macos(image_path: str, quality: int = None) -> bool:
    """Copy image to macOS clipboard using AppKit."""
    try:
        from AppKit import NSPasteboard, NSPasteboardTypePNG, NSPasteboardTypeTIFF
        from Foundation import NSData

        # Compress if quality specified, otherwise use original
        if quality:
            image_data = compress_image(image_path, quality)
        else:
            with open(image_path, 'rb') as f:
                image_data = f.read()

        # Create NSData from image bytes
        ns_data = NSData.dataWithBytes_length_(image_data, len(image_data))

        # Get pasteboard and clear it
        pasteboard = NSPasteboard.generalPasteboard()
        pasteboard.clearContents()

        # Determine type based on file extension
        ext = Path(image_path).suffix.lower()
        if ext in ('.png',):
            pasteboard.setData_forType_(ns_data, NSPasteboardTypePNG)
        else:
            # For JPEG and others, use TIFF (more compatible)
            from PIL import Image
            img = Image.open(io.BytesIO(image_data))
            tiff_buffer = io.BytesIO()
            img.save(tiff_buffer, format='TIFF')
            tiff_data = NSData.dataWithBytes_length_(tiff_buffer.getvalue(), len(tiff_buffer.getvalue()))
            pasteboard.setData_forType_(tiff_data, NSPasteboardTypeTIFF)

        return True

    except ImportError as e:
        print(f"Error: Missing dependency: {e}", file=sys.stderr)
        print("Install with: pip install Pillow pyobjc-framework-Cocoa", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error copying image: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description='Copy image to clipboard for Xiaohongshu')
    parser.add_argument('path', help='Path to image file')
    parser.add_argument('--quality', '-q', type=int, default=None,
                       help='JPEG quality (1-100), enables compression')
    parser.add_argument('--max-width', type=int, default=2000,
                       help='Max width for resize')
    parser.add_argument('--max-height', type=int, default=2000,
                       help='Max height for resize')

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: Image not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    success = copy_image_to_clipboard_macos(args.path, args.quality)
    if success:
        print(f"Image copied to clipboard: {args.path}")
        if args.quality:
            print(f"  (compressed with quality={args.quality})")
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
