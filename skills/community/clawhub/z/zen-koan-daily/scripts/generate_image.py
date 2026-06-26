#!/usr/bin/env python3
"""
Generate Zen ink wash painting for koan
Uses Google Gemini imagen-3.0-generate-001
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def get_image_prompt(koan):
    """Generate image prompt from koan data"""
    
    # Base zen ink wash style
    style = """Chinese zen ink wash painting (禅宗水墨画), 
minimalist composition, vast empty space (留白), 
subtle gradations of black ink on rice paper,
sparse brushstrokes, meditative atmosphere,
traditional Chinese calligraphy style,
serene and contemplative mood,
monochrome with occasional touches of subtle color"""
    
    # Extract theme elements
    elements = koan.get('visual_elements', [])
    mood = koan.get('mood', 'serene')
    
    # Compose scene description
    if 'dog' in elements:
        scene = "small dog silhouette in vast empty landscape, bamboo in mist"
    elif 'void' in elements or 'sky' in elements:
        scene = "vast empty sky, single tea cup on simple wooden table"
    elif 'mountain' in elements:
        scene = "distant misty mountain peak, single pine tree"
    else:
        scene = "bamboo grove in morning mist, plum blossom branch"
    
    # Full prompt
    prompt = f"{style},\n{scene},\n{mood} atmosphere,\nZen Buddhist aesthetic,\nChinese monk contemplating"
    
    return prompt

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate Zen ink wash image')
    parser.add_argument('--koan-file', help='Path to koan JSON file')
    parser.add_argument('--koan-json', help='Koan JSON string')
    parser.add_argument('--output', help='Output image path')
    parser.add_argument('--prompt-only', action='store_true', help='Only print prompt')
    
    args = parser.parse_args()
    
    # Load koan
    if args.koan_json:
        koan = json.loads(args.koan_json)
    elif args.koan_file:
        with open(args.koan_file, 'r', encoding='utf-8') as f:
            koan = json.load(f)
    else:
        print("Error: Provide --koan-file or --koan-json", file=sys.stderr)
        sys.exit(1)
    
    # Generate prompt
    prompt = get_image_prompt(koan)
    
    if args.prompt_only:
        print(prompt)
        return
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_dir = Path.home() / ".openclaw" / "media" / "outbound" / "zen-koan"
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = output_dir / f"koan-{koan['id']}-{timestamp}.png"
    
    # Print command for exec tool
    print(f"# Run this command via exec tool:")
    print(f"uv run ~/clawd/skills/yumfu/scripts/generate_image.py \\")
    print(f'  --prompt "{prompt}" \\')
    print(f"  --filename {output_path} \\")
    print(f"  --resolution 2K")
    
    print(f"\n# Output will be: {output_path}", file=sys.stderr)

if __name__ == '__main__':
    main()
