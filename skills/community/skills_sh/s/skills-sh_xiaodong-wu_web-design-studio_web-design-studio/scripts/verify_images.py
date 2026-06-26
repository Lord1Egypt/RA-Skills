#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""
Verify that all images referenced in HTML files exist and are accessible.

This script scans HTML files for image references and validates that
the corresponding image files exist. It helps catch missing images,
incorrect paths, or broken references before deployment.

Usage:
    python verify_images.py [--html-dir .] [--images-dir images]
"""

import argparse
import re
import sys
from pathlib import Path


def extract_image_references(html_file: Path) -> list[str]:
    """
    Extract all image references from an HTML file.

    Args:
        html_file: Path to the HTML file

    Returns:
        List of image paths found in the HTML
    """
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all <img> src attributes
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        images = re.findall(img_pattern, content, re.IGNORECASE)

        # Find all background-image in style attributes
        bg_pattern = r'background-image:\s*url\(["\']?([^"\')]+)["\']?\)'
        bg_images = re.findall(bg_pattern, content, re.IGNORECASE)

        return images + bg_images
    except Exception as e:
        print(f"⚠️  Error reading {html_file}: {e}", file=sys.stderr)
        return []


def verify_image_path(image_ref: str, html_file: Path, images_dir: Path) -> dict:
    """
    Verify if an image reference points to an existing file.

    Args:
        image_ref: Image path from HTML (e.g., "images/photo.png")
        html_file: Path to the HTML file containing the reference
        images_dir: Expected images directory

    Returns:
        Dictionary with verification results
    """
    result = {
        'ref': image_ref,
        'exists': False,
        'path': None,
        'issue': None
    }

    # Skip external URLs and data URLs
    if image_ref.startswith(('http://', 'https://', 'data:')):
        result['exists'] = True
        result['issue'] = 'external'
        return result

    # Try different path resolutions
    possible_paths = [
        # Relative to HTML file
        html_file.parent / image_ref,
        # Relative to images directory
        images_dir / Path(image_ref).name,
        # In project root
        Path.cwd() / image_ref,
        Path.cwd() / 'images' / Path(image_ref).name,
    ]

    for path in possible_paths:
        if path.exists() and path.is_file():
            result['exists'] = True
            result['path'] = path
            return result

    # Check if it's a common issue
    if not image_ref.startswith('images/'):
        result['issue'] = 'path_mismatch'
    else:
        result['issue'] = 'not_found'

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Verify image references in HTML files"
    )
    parser.add_argument(
        "--html-dir",
        default=".",
        help="Directory containing HTML files (default: current directory)"
    )
    parser.add_argument(
        "--images-dir",
        default="images",
        help="Expected images directory (default: images/)"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to fix common path issues (adds 'images/' prefix if needed)"
    )

    args = parser.parse_args()

    html_dir = Path(args.html_dir)
    images_dir = Path(args.images_dir)

    if not html_dir.exists():
        print(f"❌ Error: HTML directory '{html_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Find all HTML files
    html_files = list(html_dir.glob("*.html")) + list(html_dir.glob("*.htm"))

    if not html_files:
        print(f"⚠️  No HTML files found in '{html_dir}'")
        sys.exit(0)

    print(f"🔍 Scanning {len(html_files)} HTML file(s)...\n")

    all_valid = True
    total_images = 0
    missing_images = []

    for html_file in html_files:
        print(f"📄 Checking: {html_file.name}")

        image_refs = extract_image_references(html_file)
        total_images += len(image_refs)

        if not image_refs:
            print("   ℹ️  No image references found\n")
            continue

        file_valid = True
        file_results = []

        for ref in image_refs:
            result = verify_image_path(ref, html_file, images_dir)
            file_results.append(result)

            if not result['exists']:
                file_valid = False
                all_valid = False
                missing_images.append({
                    'html_file': html_file,
                    'ref': ref,
                    'issue': result['issue']
                })

        # Display results for this file
        if file_valid:
            print(f"   ✅ All {len(image_refs)} image(s) valid\n")
        else:
            print(f"   ❌ Found issues:\n")
            for result in file_results:
                if not result['exists']:
                    issue_desc = {
                        'not_found': 'File not found',
                        'path_mismatch': 'Possible path mismatch (missing images/ prefix?)'
                    }.get(result['issue'], 'Unknown issue')

                    print(f"      ❌ {result['ref']}")
                    print(f"         Issue: {issue_desc}")

            print()

    # Summary
    print("=" * 60)
    print("📊 Summary")
    print("=" * 60)
    print(f"HTML files scanned: {len(html_files)}")
    print(f"Total image references: {total_images}")
    print(f"Missing images: {len(missing_images)}")

    if missing_images:
        print("\n❌ Missing Image Details:")
        print("-" * 60)

        for item in missing_images:
            print(f"\n📄 {item['html_file'].name}")
            print(f"   🔗 {item['ref']}")

            # Suggest fixes
            if item['issue'] == 'path_mismatch':
                suggested = f"images/{Path(item['ref']).name}"
                print(f"   💡 Suggestion: Try using '{suggested}'")
            else:
                print(f"   💡 Action: Generate or add this image to the images/ directory")

        print("\n" + "=" * 60)
        print("💡 Tips to fix:")
        print("  1. Generate missing images using generate_image.py")
        print("  2. Ensure images are saved in the 'images/' directory")
        print("  3. Update HTML to use 'images/filename.png' format")
        print("  4. Run this script again to verify")
        print("=" * 60)

        sys.exit(1)
    else:
        print("\n✅ All images verified successfully!")
        print("🎉 Your page is ready to deploy!")
        sys.exit(0)


if __name__ == "__main__":
    main()
