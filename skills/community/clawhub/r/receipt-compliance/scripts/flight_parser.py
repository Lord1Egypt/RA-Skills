#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞机行程单 OCR 专用解析器
识别飞机行程单上的关键字段并输出统一数据结构
"""

import re
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from unified_invoice import UnifiedInvoice, VAT_DEDUCTION_RATES


# === 飞机行程单正则匹配模式 ===
FLIGHT_PATTERNS = {
    'flight_number': r'[A-Z]{2}\d{3,4}',
    'date': r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)',
    'time': r'(\d{1,2}:\d{2})',
    'airport': r'[\u4e00-\u9fa5]{2,8}机场?',
    'route': r'([\u4e00-\u9fa5]{2,6})[-—→]([\u4e00-\u9fa5]{2,6})',
    'passenger': r'乘客[:：]\s*([\u4e00-\u9fa5]{2,4})',
    'seat_class': r'(经济舱|商务舱|头等舱)',
    'price': r'[¥￥]?(\d+\.\d{1,2})元?',
    'fuel_surcharge': r'燃油附加费[:：]\s*[¥￥]?(\d+\.\d{1,2})',
    'airport_fee': r'民航发展基金[:：]\s*[¥￥]?(\d+\.\d{1,2})',
    'ticket_number': r'[A-Z0-9]{10,14}',
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


def extract_flight_info(ocr_text: str) -> Dict[str, Any]:
    """从 OCR 文本中提取飞机行程单信息"""
    info = {
        'invoice_type': 'traditional',
        'receipt_type': 'flight_itinerary',
        'source_format': 'image',
        'extracted_at': datetime.now().isoformat(),
    }
    
    # 提取航班号（两个大写字母+3-4位数字）
    flight_match = re.search(FLIGHT_PATTERNS['flight_number'], ocr_text)
    if flight_match:
        info['transport_number'] = flight_match.group(0)
    
    # 提取日期
    date_matches = re.findall(FLIGHT_PATTERNS['date'], ocr_text)
    if date_matches:
        info['travel_date'] = normalize_date(date_matches[0])
    
    # 提取机场（简单启发）
    airports = re.findall(r'([\u4e00-\u9fa5]{2,6})机场', ocr_text)
    if len(airports) >= 2:
        info['departure_station'] = airports[0]
        info['arrival_station'] = airports[-1]
    elif len(airports) == 1:
        info['departure_station'] = airports[0]
    
    # 提取票价
    prices = re.findall(r'[¥￥](\d+\.\d{1,2})', ocr_text)
    if not prices:
        prices = re.findall(r'(\d+\.\d{1,2})元', ocr_text)
    if prices:
        amounts = [float(p) for p in prices]
        info['total'] = max(amounts)
    
    # 提取燃油附加费
    fuel_match = re.search(FLIGHT_PATTERNS['fuel_surcharge'], ocr_text)
    if fuel_match:
        info['fuel_surcharge'] = float(fuel_match.group(1))
    
    # 提取民航发展基金
    airport_fee_match = re.search(FLIGHT_PATTERNS['airport_fee'], ocr_text)
    if airport_fee_match:
        info['airport_construction_fee'] = float(airport_fee_match.group(1))
    
    # 提取座位等级
    seat_match = re.search(FLIGHT_PATTERNS['seat_class'], ocr_text)
    if seat_match:
        info['seat_class'] = seat_match.group(0)
    
    # 提取乘客姓名
    passenger_match = re.search(FLIGHT_PATTERNS['passenger'], ocr_text)
    if passenger_match:
        info['passenger_name'] = passenger_match.group(1)
    
    # 计算机票可抵扣进项税额（9%，不含民航发展基金）
    if info.get('total'):
        rate = VAT_DEDUCTION_RATES['flight_itinerary']
        info['vat_deduction_rate'] = rate
        # 机票票价（不含民航发展基金）的9%
        ticket_amount = info['total'] - (info.get('airport_construction_fee', 0) or 0)
        info['vat_deduction_amount'] = round(ticket_amount * rate, 2)
    
    # 费用分类
    info['expense_category'] = '差旅费'
    
    return info


def parse_flight_itinerary(ocr_text: str) -> UnifiedInvoice:
    """解析飞机行程单 OCR 文本，返回统一数据结构"""
    info = extract_flight_info(ocr_text)
    invoice = UnifiedInvoice(**info)
    invoice.raw_text = ocr_text
    return invoice


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python flight_parser.py <path_to_flight_itinerary_image>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(file_path)
        ocr_text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        
        invoice = parse_flight_itinerary(ocr_text)
        print(invoice.to_json())
    except ImportError:
        print("请先安装 pytesseract: pip install pytesseract", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"解析失败: {e}", file=sys.stderr)
        sys.exit(1)
