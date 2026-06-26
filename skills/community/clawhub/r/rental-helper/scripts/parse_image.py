#!/usr/bin/env python3
"""
从图片识别房源信息（OCR）
用法: python parse_image.py --image path/to/image.jpg

支持识别图片中的文字信息，提取：
- 小区名称
- 租金
- 户型
- 面积
- 联系方式
- 其他描述
"""

import json
import os
import argparse
import re
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/rental-data")
DATA_FILE = os.path.join(DATA_DIR, "listings.json")

def ensure_data_dir():
    """确保数据目录存在"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_listings():
    """加载现有房源列表"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_listings(listings):
    """保存房源列表"""
    ensure_data_dir()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)

def extract_info_from_text(text):
    """从文本中提取房源信息"""
    info = {}
    
    lines = text.split('\n')
    
    # 尝试提取租金
    price_patterns = [
        r'(\d{3,5})\s*元/?月',
        r'租金[:：]?\s*(\d{3,5})',
        r'价格[:：]?\s*(\d{3,5})',
        r'¥(\d{3,5})',
        r'(\d{3,5})\s*/月',
    ]
    for pattern in price_patterns:
        match = re.search(pattern, text)
        if match:
            price = int(match.group(1))
            if 500 <= price <= 50000:
                info["rent"] = price
                break
    
    # 尝试提取户型
    room_patterns = [
        r'(\d+)室(\d+)厅',
        r'(\d+)房(\d+)厅',
        r'(单间|一室一厅|两室一厅|三室一厅|两室两厅|三室两厅)',
    ]
    for pattern in room_patterns:
        match = re.search(pattern, text)
        if match:
            if match.lastindex == 2:
                info["room_type"] = f"{match.group(1)}室{match.group(2)}厅"
            else:
                info["room_type"] = match.group(1)
            break
    
    # 尝试提取面积
    area_match = re.search(r'(\d+\.?\d*)\s*㎡', text)
    if area_match:
        info["area"] = float(area_match.group(1))
    
    # 尝试提取联系方式
    phone_match = re.search(r'1[3-9]\d{9}', text)
    if phone_match:
        info["contact"] = phone_match.group(0)
    
    # 尝试提取小区名称（通常是第一行非空内容）
    for line in lines:
        line = line.strip()
        if line and len(line) > 2 and len(line) < 30:
            # 排除纯数字和常见干扰词
            if not re.match(r'^\d+$', line) and not any(word in line for word in ['元', '月', '室', '厅', '㎡']):
                info["name"] = line
                break
    
    # 提取其他描述（可能是优点）
    descriptions = []
    for line in lines:
        line = line.strip()
        if len(line) > 5 and len(line) < 100:
            if any(word in line for word in ['地铁', '公交', '附近', '配套', '装修', '家具', '家电', '采光', '通风']):
                descriptions.append(line)
    if descriptions:
        info["pros"] = '；'.join(descriptions[:3])  # 最多取3条
    
    # 提取交通信息
    transport_patterns = [
        r'(距[\d\u4e00-\u9fa5]+地铁[\d\u4e00-\u9fa5]*站[\d\u4e00-\u9fa5]*\d+米)',
        r'(步行\d+分钟到[\d\u4e00-\u9fa5]+)',
        r'(地铁[\d\u4e00-\u9fa5]*线[\d\u4e00-\u9fa5]*站)',
    ]
    for pattern in transport_patterns:
        match = re.search(pattern, text)
        if match:
            info["transport"] = match.group(1)
            break
    
    return info

def parse_image(args):
    """解析图片"""
    if not os.path.exists(args.image):
        print(f"图片不存在: {args.image}")
        return
    
    # 尝试使用OCR
    text = ""
    
    # 方法1: 使用 pytesseract
    try:
        from PIL import Image
        import pytesseract
        image = Image.open(args.image)
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        print("✅ 使用 Tesseract OCR 识别成功")
    except ImportError:
        print("⚠️ 未安装 pytesseract，尝试其他方法...")
    except Exception as e:
        print(f"⚠️ Tesseract 识别失败: {e}")
    
    # 方法2: 使用 easyocr
    if not text:
        try:
            import easyocr
            reader = easyocr.Reader(['ch_sim', 'en'])
            result = reader.readtext(args.image)
            text = '\n'.join([item[1] for item in result])
            print("✅ 使用 EasyOCR 识别成功")
        except ImportError:
            print("⚠️ 未安装 easyocr")
        except Exception as e:
            print(f"⚠️ EasyOCR 识别失败: {e}")
    
    if not text:
        print("\n❌ OCR 识别失败，请确保已安装OCR工具：")
        print("   方案1: pip install pytesseract pillow")
        print("      并安装 Tesseract: brew install tesseract tesseract-lang")
        print("   方案2: pip install easyocr")
        return
    
    # 显示识别的原始文本
    print("\n📝 识别的文本内容：")
    print("-" * 40)
    print(text[:500] if len(text) > 500 else text)
    if len(text) > 500:
        print("... (已截断)")
    print("-" * 40)
    
    # 提取信息
    info = extract_info_from_text(text)
    
    if not info:
        print("\n⚠️ 未能从图片中提取到房源信息")
        return
    
    # 显示提取结果
    print("\n📋 提取的房源信息：")
    print("-" * 40)
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # 保存到数据库
    listings = load_listings()
    new_id = f"L{len(listings) + 1:03d}"
    
    listing = {
        "id": new_id,
        "name": info.get("name", "未命名房源"),
        "rent": info.get("rent", 0),
        "room_type": info.get("room_type", ""),
        "area": info.get("area", 0),
        "transport": info.get("transport", ""),
        "contact": info.get("contact", ""),
        "pros": info.get("pros", ""),
        "status": "待考虑",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    listings.append(listing)
    save_listings(listings)
    
    print(f"\n✅ 已保存为房源 {new_id}")
    print("提示：请补充完善其他信息（地址、交通详情、联系方式等）")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从图片识别房源信息")
    parser.add_argument("--image", required=True, help="图片路径")
    
    args = parser.parse_args()
    parse_image(args)
