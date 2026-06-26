#!/usr/bin/env python3
"""
增强版 OCR 识别脚本
- 图像预处理（二值化、去噪、对比度增强）
- 多 PSM 模式识别
- 结构化数据提取
- 错误校正
"""

import sys
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import re
import json

def preprocess_image(image_path):
    """图像预处理"""
    # 用 OpenCV 读取
    img_cv = cv2.imread(image_path)
    
    # 转换为灰度图
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # 去噪
    denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
    
    # 二值化（自适应阈值）
    binary = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
    
    # 对比度增强
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(binary)
    
    # 保存临时文件
    temp_path = image_path.replace('.png', '_processed.png')
    cv2.imwrite(temp_path, enhanced)
    
    return temp_path

def ocr_multiple_modes(image_path):
    """多 PSM 模式识别"""
    results = []
    
    # PSM 模式：3=自动，6=统一块，11=稀疏文本，12=稀疏文本+行
    for psm in [3, 6, 11, 12]:
        try:
            custom_config = f'--oem 3 --psm {psm} -c preserve_interword_spaces=1'
            text = pytesseract.image_to_string(
                Image.open(image_path),
                lang='chi_sim+eng',
                config=custom_config
            )
            results.append({
                'psm': psm,
                'text': text,
                'lines': [l.strip() for l in text.split('\n') if l.strip()]
            })
        except Exception as e:
            print(f"PSM {psm} 失败：{e}", file=sys.stderr)
    
    return results

def extract_product_info(lines):
    """从 OCR 结果中提取结构化商品信息"""
    products = []
    
    for line in lines:
        # 清理多余空格
        line = re.sub(r'\s+', ' ', line)
        
        # 跳过太短或太长的行
        if len(line) < 5 or len(line) > 200:
            continue
        
        # 跳过明显不是商品的行
        skip_words = ['闲鱼', '搜索', '登录', '注册', '综合', '排序', '筛选', '猜你喜欢']
        if any(word in line for word in skip_words):
            continue
        
        # 提取价格（多种格式：¥10, ￥10, 10 元）
        price = None
        price_match = re.search(r'[¥￥](\d+\.?\d*)', line)
        if price_match:
            price = price_match.group(1)
        else:
            # 尝试匹配 "10 元" 格式
            yuan_match = re.search(r'(\d+\.?\d*)\s*元', line)
            if yuan_match:
                price = yuan_match.group(1)
        
        # 提取想要人数（多种格式：628 人想要，628 人超要，628 人起要）
        wants = None
        wants_match = re.search(r'(\d+)\s*人\s*(想要 | 超要 | 起要)', line)
        if wants_match:
            wants = wants_match.group(1)
        
        # 提取卖家信息
        seller_match = re.search(r'(信用 [优秀 | 极好 | 良好])', line)
        seller = seller_match.group(1) if seller_match else None
        
        # 提取标签
        tags = []
        if '包邮' in line:
            tags.append('包邮')
        if '自动发货' in line or '24h' in line.lower():
            tags.append('自动发货')
        if '验货宝' in line:
            tags.append('验货宝')
        if '鱼小铺' in line:
            tags.append('鱼小铺')
        
        # 只保留包含关键信息的行
        if price or wants or tags:
            products.append({
                'raw': line,
                'price': price,
                'wants': wants,
                'seller': seller,
                'tags': tags
            })
    
    return products

def merge_results(results):
    """合并多个 PSM 模式的结果，去重"""
    all_products = []
    seen = set()
    
    for result in results:
        products = extract_product_info(result['lines'])
        for p in products:
            # 去重（基于原始文本）
            key = p['raw'][:50]
            if key not in seen:
                seen.add(key)
                all_products.append(p)
    
    return all_products

def main():
    if len(sys.argv) < 2:
        print("用法：python3 ocr-enhanced.py <截图路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    try:
        # 图像预处理
        processed_path = preprocess_image(image_path)
        
        # 多模式 OCR
        results = ocr_multiple_modes(processed_path)
        
        # 合并结果
        products = merge_results(results)
        
        # 只输出纯 JSON（无其他日志）
        output = {
            'image': image_path,
            'products': products,
            'count': len(products)
        }
        
        # 只输出 JSON，其他日志走 stderr
        print(json.dumps(output, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(json.dumps({'error': str(e), 'count': 0}), file=sys.stdout)
        sys.exit(0)  # 不退出，返回空结果

if __name__ == '__main__':
    main()
