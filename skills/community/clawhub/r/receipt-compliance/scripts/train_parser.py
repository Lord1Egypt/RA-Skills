#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火车票 OCR 专用解析器
识别火车票上的关键字段并输出统一数据结构
"""

import re
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from unified_invoice import UnifiedInvoice, VAT_DEDUCTION_RATES


# === 火车票正则匹配模式 ===
TRAIN_PATTERNS = {
    'train_number': r'[GDC]\d{1,4}',
    'date': r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)',
    'time': r'(\d{1,2}:\d{2})',
    'station': r'[\u4e00-\u9fa5]{2,10}站?',
    'seat_class': r'(二等座|一等座|商务座|硬座|软座|硬卧|软卧)',
    'car_number': r'\d{1,3}车\d{1,3}[ABCDF]?',
    'price': r'[¥￥]?(\d+\.\d{1,2})元?',
    'passenger': r'姓名[:：]\s*([\u4e00-\u9fa5]{2,4})',
    'id_number': r'\d{17}[\dXx]|\d{15}',
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


def extract_train_info(ocr_text: str) -> Dict[str, Any]:
    """从 OCR 文本中提取火车票信息"""
    info = {
        'invoice_type': 'traditional',
        'receipt_type': 'train_ticket',
        'source_format': 'image',
        'extracted_at': datetime.now().isoformat(),
    }
    
    # 提取车次号
    train_match = re.search(TRAIN_PATTERNS['train_number'], ocr_text)
    if train_match:
        info['transport_number'] = train_match.group(0)
    
    # 提取日期
    date_matches = re.findall(TRAIN_PATTERNS['date'], ocr_text)
    if date_matches:
        info['travel_date'] = normalize_date(date_matches[0])
    
    # 提取站点（简单启发：日期后面通常是站点）
    stations = re.findall(r'([\u4e00-\u9fa5]{2,6})站?', ocr_text)
    if len(stations) >= 2:
        info['departure_station'] = stations[0]
        info['arrival_station'] = stations[-1]
    elif len(stations) == 1:
        info['departure_station'] = stations[0]
    
    # 提取价格
    prices = re.findall(r'[¥￥](\d+\.\d{1,2})', ocr_text)
    if not prices:
        prices = re.findall(r'(\d+\.\d{1,2})元', ocr_text)
    if prices:
        # 火车票通常有多个金额（票价、保险等），取最大值作为票价
        amounts = [float(p) for p in prices]
        info['total'] = max(amounts)
    
    # 提取座位等级
    seat_match = re.search(TRAIN_PATTERNS['seat_class'], ocr_text)
    if seat_match:
        info['seat_class'] = seat_match.group(0)
    
    # 提取乘客姓名
    passenger_match = re.search(TRAIN_PATTERNS['passenger'], ocr_text)
    if passenger_match:
        info['passenger_name'] = passenger_match.group(1)
    
    # 计算可抵扣进项税额（火车票 9%）
    if info.get('total'):
        rate = VAT_DEDUCTION_RATES['train_ticket']
        info['vat_deduction_rate'] = rate
        info['vat_deduction_amount'] = round(info['total'] * rate, 2)
    
    # 费用分类
    info['expense_category'] = '差旅费'
    
    return info


def parse_train_ticket(ocr_text: str) -> UnifiedInvoice:
    """
    解析火车票 OCR 文本，返回统一数据结构
    """
    info = extract_train_info(ocr_text)
    invoice = UnifiedInvoice(**info)
    invoice.raw_text = ocr_text
    return invoice


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python train_parser.py <path_to_train_ticket_image>")
        sys.exit(1)
    
    # 读取文件并尝试OCR
    file_path = sys.argv[1]
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(file_path)
        ocr_text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        
        invoice = parse_train_ticket(ocr_text)
        print(invoice.to_json())
    except ImportError:
        print("请先安装 pytesseract: pip install pytesseract", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"解析失败: {e}", file=sys.stderr)
        sys.exit(1)
