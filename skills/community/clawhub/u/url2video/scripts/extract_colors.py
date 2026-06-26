#!/usr/bin/env python3
"""Extract dominant colors from a website for video branding."""

import sys
import re
import urllib.request
from collections import Counter
from urllib.parse import urlparse

def extract_colors(url):
    """Extract hex and rgb colors from website CSS/HTML."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        sys.exit(1)

    # Extract hex colors
    hex_colors = re.findall(r'#[0-9a-fA-F]{3,8}\b', html)

    # Extract rgb/rgba
    rgb_colors = re.findall(r'rgba?\([^)]+\)', html)

    # Count frequency
    all_colors = [c.lower() for c in hex_colors]
    color_counts = Counter(all_colors)

    # Filter out common non-colors and normalize
    filtered = {}
    for color, count in color_counts.most_common(30):
        # Skip grayscale and transparent
        if color in ('#000', '#000000', '#fff', '#ffffff', '#transparent'):
            continue
        # Expand shorthand hex
        if len(color) == 4:
            color = '#' + ''.join([c*2 for c in color[1:]])
        filtered[color] = count

    return filtered, rgb_colors[:10]

def suggest_palette(colors):
    """Suggest brand palette from extracted colors."""
    sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)

    palette = {
        'primary': sorted_colors[0][0] if len(sorted_colors) > 0 else '#ff6b35',
        'secondary': sorted_colors[1][0] if len(sorted_colors) > 1 else '#2ec4b6',
        'background': '#1a1a2e',  # Default dark
        'text': '#ffffff',
        'textMuted': '#999999',
    }

    return palette

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_colors.py <website_url>")
        sys.exit(1)

    url = sys.argv[1]
    if not url.startswith('http'):
        url = 'https://' + url

    print(f"Extracting colors from {url}...\n")

    colors, rgb_colors = extract_colors(url)

    print("Top colors found:")
    for color, count in colors.most_common(10):
        print(f"  {color}: {count} occurrences")

    print("\nRGB colors found:")
    for rgb in rgb_colors[:5]:
        print(f"  {rgb}")

    palette = suggest_palette(colors)
    print("\nSuggested palette:")
    for key, value in palette.items():
        print(f"  {key}: {value}")

    print("\n--- TypeScript const ---")
    print("const COLORS = {")
    for key, value in palette.items():
        print(f"  {key}: '{value}',")
    print("};")

if __name__ == '__main__':
    main()
