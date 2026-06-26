#!/usr/bin/env python3
"""
图片 OCR 识别工具
使用方式: python ocr_images.py --image 图片路径
"""

import argparse
import sys
from typing import List

from cnocr import CnOcr


def ocr_recognize(image_path: str) -> List[str]:
    """
    使用 cnocr 识别图片中的文字

    参数:
        image_path: 图片文件路径

    返回:
        list: 识别出的文字列表，每行是一个元素
    """
    cn_ocr = CnOcr()
    result = cn_ocr.ocr(image_path)

    text_lines = []
    for line in result:
        if isinstance(line, str):
            text_lines.append(line)
        elif isinstance(line, dict):
            text_lines.append(line.get('text', ''))
        else:
            try:
                line_text = ''.join([item['text'] for item in line])
                text_lines.append(line_text)
            except:
                text_lines.append(str(line))

    return text_lines


def main():
    parser = argparse.ArgumentParser(description='图片 OCR 识别工具')
    parser.add_argument('--image', '-i', required=True, help='图片文件路径')
    
    args = parser.parse_args()
    
    image_path = args.image
    
    print(f"正在识别图片: {image_path}")
    
    try:
        text_lines = ocr_recognize(image_path)
        
        if not text_lines:
            print("OCR 未能识别出任何文字")
            sys.exit(1)
        
        print(f"\n识别结果（共 {len(text_lines)} 行）：")
        print("-" * 40)
        for i, line in enumerate(text_lines, 1):
            print(f"{i}: {line}")
        print("-" * 40)
        
        # 输出 JSON 格式便于后续处理
        import json
        result = {
            "image": image_path,
            "lines": text_lines,
            "line_count": len(text_lines)
        }
        print("\nJSON 输出:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
