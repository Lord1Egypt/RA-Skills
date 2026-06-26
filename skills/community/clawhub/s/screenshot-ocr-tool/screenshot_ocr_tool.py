#!/usr/bin/env python3
# screenshot_ocr_tool.py - Screen Capture OCR Tool for TCM Exam Questions

import argparse
import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from scripts.screenshot_ocr import main

def cli_main():
    parser = argparse.ArgumentParser(description='Screen Capture OCR Tool for TCM Exam Questions')
    parser.add_argument('image_path', help='Path to the screenshot image')
    parser.add_argument('--format', choices=['text', 'structured', 'question_answer'], 
                       default='text', help='Output format')
    parser.add_argument('--output', '-o', help='Output file path')
    
    args = parser.parse_args()
    
    params = {
        "image_path": args.image_path,
        "output_format": args.format
    }
    
    result = main(params)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Result saved to {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    cli_main()