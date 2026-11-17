#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通行费票据 OCR 专用解析器
识别高速/桥闸通行费票据并输出统一数据结构
支持计算可抵扣进项税额（高速3%，桥闸5%）
"""

import re
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from unified_invoice import UnifiedInvoice, VAT_DEDUCTION_RATES


# === 通行费票据正则匹配模式 ===
TOLL_PATTERNS = {
    'entry_station': r'入口[:：]\s*([\u4e00-\u9fa5A-Za-z0-9]+)',
    'exit_station': r'出口[:：]\s*([\u4e00-\u9fa5A-Za-z0-9]+)',
    'date': r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)',
    'time': r'(\d{1,2}:\d{2}:\d{2})',
    'amount': r'[¥￥]?(\d+\.\d{1,2})元?',
    'vehicle_type': r'(客车|货车|专项作业车)',
    'weight': r'(\d+\.\d{1,2})吨',
    'invoice_code': r'发票代码[:：]\s*(\d{10,12})',
    'invoice_number': r'发票号码[:：]\s*(\d{8,20})',
    'toll_type': r'(高速公路|一级公路|桥闸)',
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


def extract_toll_info(ocr_text: str) -> Dict[str, Any]:
    """从 OCR 文本中提取通行费票据信息"""
    info = {
        'invoice_type': 'traditional',
        'receipt_type': 'toll_receipt',
        'source_format': 'image',
        'extracted_at': datetime.now().isoformat(),
    }
    
    # 提取入口站
    entry_match = re.search(TOLL_PATTERNS['entry_station'], ocr_text)
    if entry_match:
        info['departure_station'] = entry_match.group(1)
    
    # 提取出口站
    exit_match = re.search(TOLL_PATTERNS['exit_station'], ocr_text)
    if exit_match:
        info['arrival_station'] = exit_match.group(1)
    
    # 提取日期
    date_matches = re.findall(TOLL_PATTERNS['date'], ocr_text)
    if date_matches:
        info['billing_date'] = normalize_date(date_matches[0])
    
    # 提取金额
    amounts = re.findall(r'[¥￥](\d+\.\d{1,2})', ocr_text)
    if not amounts:
        amounts = re.findall(r'(\d+\.\d{1,2})元', ocr_text)
    if amounts:
        info['total'] = float(amounts[0])
    
    # 提取车辆类型
    vehicle_match = re.search(TOLL_PATTERNS['vehicle_type'], ocr_text)
    if vehicle_match:
        info['vehicle_type'] = vehicle_match.group(0)
    
    # 提取通行费类型（高速/桥闸）
    toll_type_match = re.search(TOLL_PATTERNS['toll_type'], ocr_text)
    if toll_type_match:
        info['toll_road_type'] = toll_type_match.group(0)
    
    # 提取发票代码
    code_match = re.search(TOLL_PATTERNS['invoice_code'], ocr_text)
    if code_match:
        info['invoice_code'] = code_match.group(1)
    
    # 提取发票号码
    number_match = re.search(TOLL_PATTERNS['invoice_number'], ocr_text)
    if number_match:
        info['invoice_number'] = number_match.group(1)
    
    # 计算可抵扣进项税额
    toll_type = info.get('toll_road_type', '')
    if info.get('total'):
        if '高速' in toll_type or '一级' in toll_type:
            rate = VAT_DEDUCTION_RATES['toll_receipt_highway']
        elif '桥闸' in toll_type:
            rate = VAT_DEDUCTION_RATES['toll_receipt_bridge']
        else:
            rate = VAT_DEDUCTION_RATES['toll_receipt_highway']  # 默认高速
        
        info['vat_deduction_rate'] = rate
        info['vat_deduction_amount'] = round(info['total'] * rate, 2)
    
    # 费用分类
    info['expense_category'] = '通行费'
    
    return info


def parse_toll_receipt(ocr_text: str) -> UnifiedInvoice:
    """解析通行费票据 OCR 文本，返回统一数据结构"""
    info = extract_toll_info(ocr_text)
    invoice = UnifiedInvoice(**info)
    invoice.raw_text = ocr_text
    return invoice


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python toll_parser.py <path_to_toll_receipt_image>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(file_path)
        ocr_text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        
        invoice = parse_toll_receipt(ocr_text)
        print(invoice.to_json())
    except ImportError:
        print("请先安装 pytesseract: pip install pytesseract", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"解析失败: {e}", file=sys.stderr)
        sys.exit(1)
