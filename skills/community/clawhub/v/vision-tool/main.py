#!/usr/bin/env python3
"""
Vision Tool - Main skill script
Image recognition using Ollama + qwen3.5:4b
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add scripts directory to path
SKILL_DIR = Path(__file__).parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from vision_core import VisionAnalyzer
except ImportError:
    print("Error: Could not import vision_core.py")
    print(f"Make sure it's in {SCRIPTS_DIR}")
    sys.exit(1)

def analyze_image(image_path, prompt="Describe this image"):
    """
    Analyze an image and return results
    """
    analyzer = VisionAnalyzer()
    return analyzer.analyze_image(image_path, prompt)

def main():
    parser = argparse.ArgumentParser(description="Vision Tool - Image Recognition Skill")
    parser.add_argument("image", help="Path to image file")
    parser.add_argument("--prompt", default="Describe this image", help="Analysis prompt")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    # Check if image exists
    if not os.path.exists(args.image):
        print(f"Error: Image not found: {args.image}")
        sys.exit(1)
    
    # Analyze image
    result = analyze_image(args.image, args.prompt)
    
    # Output result
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
        
        print(f"✅ Analysis successful ({result['time_elapsed']})")
        print(f"📋 Source: {result['source']}")
        print(f"📊 Stats: {result['stats']['prompt_tokens']}↑ {result['stats']['output_tokens']}↓ tokens")
        
        print("\n" + "="*60)
        print("📝 Analysis Result:")
        print("="*60)
        print(result['analysis'])
        print("="*60)

if __name__ == "__main__":
    main()