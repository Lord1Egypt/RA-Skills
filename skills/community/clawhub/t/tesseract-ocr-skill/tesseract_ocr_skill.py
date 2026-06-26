#!/usr/bin/env python3
"""
Tesseract OCR Skill for OpenClaw
专门用于处理中医教材截图的OCR技能
"""

import argparse
import json
import sys
from pathlib import Path

# 添加脚本路径到系统路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from .scripts.tesseract_ocr import main as tesseract_main

def cli_main():
    parser = argparse.ArgumentParser(description='Tesseract OCR Skill for TCM Materials')
    parser.add_argument('image_path', help='Path to the image file')
    parser.add_argument('--lang', choices=['chi_sim', 'eng', 'chi_sim+eng'], 
                       default='chi_sim+eng', help='Recognition language')
    parser.add_argument('--format', choices=['text', 'structured', 'question_answer'], 
                       default='text', help='Output format')
    parser.add_argument('--output', '-o', help='Output file path')
    
    args = parser.parse_args()
    
    params = {
        "image_path": args.image_path,
        "language": args.lang,
        "output_format": args.format
    }
    
    result = tesseract_main(params)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Result saved to {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    cli_main()