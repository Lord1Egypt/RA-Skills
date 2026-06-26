#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR 辅助模块
支持 pytesseract 和 easyocr
"""

import sys
from PIL import Image

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def ocr_with_pytesseract(image_path):
    """
    使用 pytesseract 进行 OCR
    需要先安装：
    - pip install pytesseract
    - 下载安装 Tesseract-OCR 引擎：https://github.com/UB-Mannheim/tesseract/wiki
    """
    try:
        import pytesseract
        
        # 设置 Tesseract 路径（Windows）
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        return text.strip()
    except ImportError:
        print("❌ pytesseract 未安装")
        print("   运行：pip install pytesseract")
        print("   并安装 Tesseract-OCR 引擎")
        return None
    except Exception as e:
        print(f"❌ OCR 失败：{e}")
        return None

def ocr_with_easyocr(image_path):
    """
    使用 EasyOCR 进行 OCR
    需要先安装：pip install easyocr
    """
    try:
        import easyocr
        
        reader = easyocr.Reader(['ch_sim', 'en'])
        result = reader.readtext(image_path)
        
        # 提取文字
        texts = [item[1] for item in result]
        return '\n'.join(texts)
    except ImportError:
        print("❌ easyocr 未安装")
        print("   运行：pip install easyocr")
        return None
    except Exception as e:
        print(f"❌ OCR 失败：{e}")
        return None

def auto_select_ocr(image_path):
    """
    自动选择可用的 OCR 引擎
    """
    # 优先尝试 pytesseract
    text = ocr_with_pytesseract(image_path)
    if text:
        return text
    
    # 备选 easyocr
    text = ocr_with_easyocr(image_path)
    if text:
        return text
    
    return "[OCR 失败，请安装 pytesseract 或 easyocr]"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python ocr_helper.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    text = auto_select_ocr(image_path)
    print(text)
