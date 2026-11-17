#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
出租车票 OCR 专用解析器
识别出租车票上的关键字段并输出统一数据结构
"""

import re
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from unified_invoice import UnifiedInvoice, VAT_DEDUCTION_RATES


# === 出租车票正则匹配模式 ===
TAXI_PATTERNS = {
    'license_plate': r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤川青藏琼宁][A-Z][A-Z0-9]{4,5}',
    'date': r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)',
    'time': r'(\d{1,2}:\d{2})',
    'on_time': r'上车时间[:：]\s*(\d{1,2}:\d{2})',
    'off_time': r'下车时间[:：]\s*(\d{1,2}:\d{2})',
    'mileage': r'(\d+\.\d{1,2})公里',
    'mileage2': r'里程[:：]\s*(\d+\.\d{1,2})',
    'price': r'[¥￥]?(\d+\.\d{1,2})元?',
    'company': r'[\u4e00-\u9fa5]{2,10}出租车公司',
    'invoice_number': r'\d{8,12}',
}


def normalize_date(date_str: str) -> str:
    """标准化日期格式"""
    if not date_str:
        return None
    date_str = date_str.replace('年', '-').replace('月', '-').replace('日', '').replace('/', '-')
    parts = date_str.split('-')
    if len(parts) == 3:
        return f"{parts[0]}-{int(parts[1]):02d}-{int(parts[2]):02d}"
    return date_str


def extract_taxi_info(ocr_text: str) -> Dict[str, Any]:
    """从 OCR 文本中提取出租车票信息"""
    info = {
        'invoice_type': 'traditional',
        'receipt_type': 'taxi_receipt',
        'source_format': 'image',
        'extracted_at': datetime.now().isoformat(),
    }
    
    # 提取车牌号
    plate_match = re.search(TAXI_PATTERNS['license_plate'], ocr_text)
    if plate_match:
        info['taxi_license_plate'] = plate_match.group(0)
    
    # 提取日期
    date_matches = re.findall(TAXI_PATTERNS['date'], ocr_text)
    if date_matches:
        info['billing_date'] = normalize_date(date_matches[0])
    
    # 提取上车时间
    on_time_match = re.search(TAXI_PATTERNS['on_time'], ocr_text)
    if on_time_match:
        info['pickup_time'] = on_time_match.group(1)
    
    # 提取下车时间
    off_time_match = re.search(TAXI_PATTERNS['off_time'], ocr_text)
    if off_time_match:
        info['dropoff_time'] = off_time_match.group(1)
    
    # 提取里程
    mileage_match = re.search(TAXI_PATTERNS['mileage'], ocr_text)
    if mileage_match:
        info['taxi_mileage'] = float(mileage_match.group(1))
    else:
        mileage_match = re.search(TAXI_PATTERNS['mileage2'], ocr_text)
        if mileage_match:
            info['taxi_mileage'] = float(mileage_match.group(1))
    
    # 提取金额
    prices = re.findall(r'[¥￥](\d+\.\d{1,2})', ocr_text)
    if not prices:
        prices = re.findall(r'(\d+\.\d{1,2})元', ocr_text)
    if prices:
        amounts = [float(p) for p in prices]
        info['total'] = max(amounts)
    
    # 提取出租车公司
    company_match = re.search(TAXI_PATTERNS['company'], ocr_text)
    if company_match:
        info['seller_name'] = company_match.group(0)
    
    # 提取发票号码
    inv_match = re.search(TAXI_PATTERNS['invoice_number'], ocr_text)
    if inv_match:
        info['invoice_number'] = inv_match.group(0)
    
    # 计算机票可抵扣进项税额（电子普票 3%）
    if info.get('total'):
        rate = VAT_DEDUCTION_RATES['taxi_receipt']
        info['vat_deduction_rate'] = rate
        info['vat_deduction_amount'] = round(info['total'] * rate, 2)
    
    # 费用分类
    info['expense_category'] = '差旅费'
    
    return info


def parse_taxi_receipt(ocr_text: str) -> UnifiedInvoice:
    """解析出租车票 OCR 文本，返回统一数据结构"""
    info = extract_taxi_info(ocr_text)
    invoice = UnifiedInvoice(**info)
    invoice.raw_text = ocr_text
    return invoice


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python taxi_parser.py <path_to_taxi_receipt_image>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(file_path)
        ocr_text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        
        invoice = parse_taxi_receipt(ocr_text)
        print(invoice.to_json())
    except ImportError:
        print("请先安装 pytesseract: pip install pytesseract", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"解析失败: {e}", file=sys.stderr)
        sys.exit(1)
