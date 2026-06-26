#!/usr/bin/env python3
"""
PDF to Images Converter
Converts each page of a PDF to individual image files.
"""

import sys
import os
from pathlib import Path

try:
    from pdf2image import convert_from_path
except ImportError:
    print("Error: pdf2image is not installed.")
    print("Please install it with: pip install pdf2image")
    print("Also requires poppler-utils: sudo apt-get install poppler-utils")
    sys.exit(1)


def pdf_to_images(pdf_path, output_dir=None, dpi=200):
    """
    Convert PDF to images, one per page.

    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save images (default: same as PDF)
        dpi (int): Image resolution (default: 200)

    Returns:
        list: List of image file paths
    """
    try:
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            print(f"Error: File not found: {pdf_path}")
            return []

        # Set output directory
        if output_dir is None:
            output_dir = pdf_path.parent / f"{pdf_path.stem}_pages"
        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"Converting PDF to images...")
        print(f"PDF: {pdf_path}")
        print(f"Output: {output_dir}")

        # Convert PDF to images
        images = convert_from_path(str(pdf_path), dpi=dpi)

        image_paths = []
        for i, image in enumerate(images, start=1):
            image_path = output_dir / f"page_{i:03d}.png"
            image.save(str(image_path), "PNG")
            image_paths.append(str(image_path))
            print(f"  Page {i}/{len(images)}: {image_path.name}")

        print(f"\nTotal pages converted: {len(images)}")
        print(f"Images saved to: {output_dir}")

        return image_paths

    except Exception as e:
        print(f"Error converting PDF: {str(e)}")
        return []


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_images.py <pdf_path> [output_dir] [dpi]")
        print("\nExample:")
        print("  python pdf_to_images.py document.pdf")
        print("  python pdf_to_images.py document.pdf ./images 300")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 200

    image_paths = pdf_to_images(pdf_path, output_dir, dpi)

    if image_paths:
        print("\nImage paths (for Claude):")
        for path in image_paths:
            print(f"  {path}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
