#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image OCR Reader - Extract text from images using RapidOCR
Usage: python read_image.py <image_path>
"""

import sys
import os
import json
from pathlib import Path

def extract_text(image_path: str) -> dict:
    """
    Extract text from an image using RapidOCR.
    """
    try:
        from rapidocr import RapidOCR
        
        # Initialize OCR
        ocr = RapidOCR()
        
        # Run OCR
        result = ocr(image_path)
        
        # Extract text
        lines = []
        all_text = []
        
        if result and result.boxes is not None:
            for i, (box, text, confidence) in enumerate(zip(result.boxes, result.txts, result.scores)):
                lines.append({
                    "text": text,
                    "confidence": round(float(confidence), 4),
                    "box": box.tolist() if hasattr(box, 'tolist') else list(box)
                })
                all_text.append(text)
        
        return {
            "success": True,
            "text": "\n".join(all_text),
            "lines": lines,
            "line_count": len(lines),
            "error": None
        }
        
    except ImportError as e:
        return {
            "success": False,
            "text": "",
            "lines": [],
            "line_count": 0,
            "error": f"RapidOCR not installed. Run: pip install rapidocr. Error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "text": "",
            "lines": [],
            "line_count": 0,
            "error": str(e)
        }


def get_image_info(image_path: str) -> dict:
    """Get basic image information."""
    try:
        from PIL import Image
        img = Image.open(image_path)
        return {
            "success": True,
            "format": img.format,
            "size": list(img.size),
            "width": img.width,
            "height": img.height,
            "mode": img.mode
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: python read_image.py <image_path>"
        }, ensure_ascii=False))
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(json.dumps({
            "success": False,
            "error": f"Image file not found: {image_path}"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # Get image info
    info = get_image_info(image_path)
    
    # Extract text
    result = extract_text(image_path)
    result["image_info"] = info
    
    # Output as JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
