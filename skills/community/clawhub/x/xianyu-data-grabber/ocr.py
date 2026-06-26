#!/usr/bin/env python3
"""
闲鱼数据 OCR 识别脚本
使用 Tesseract 识别截图中的文字
"""

import sys
from PIL import Image
import pytesseract
import re

def extract_products(text):
    """从 OCR 结果中提取商品信息"""
    products = []
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    for line in lines:
        # 提取包含价格、想要、包邮等关键信息的行
        if any(x in line for x in ['¥', '想要', '包邮', '自动发货', '人超要', '人起要']):
            # 清理多余字符
            line = re.sub(r'\s+', ' ', line)
            if len(line) > 5 and len(line) < 200:
                products.append(line)
    
    return products

def main():
    if len(sys.argv) < 2:
        print("用法：python3 ocr.py <截图路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    try:
        # 打开图片
        img = Image.open(image_path)
        
        # OCR 识别
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        
        # 提取商品信息
        products = extract_products(text)
        
        # 输出结果
        for p in products:
            print(p)
        
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
