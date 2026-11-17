#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定额发票 OCR 专用解析器
识别定额发票上的关键字段并输出统一数据结构
"""

import re
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from unified_invoice import UnifiedInvoice, VAT_DEDUCTION_RATES


# === 定额发票正则匹配模式 ===
FIXED_PATTERNS = {
    'invoice_code': r'发票代码[:：]\s*(\d{10,12})',
    'invoice_number': r'发票号码[:：]\s*(\d{8,20})',
    'amount': r'(?:金额|合计)[:：]\s*[¥￥]?(\d+\.\d{1,2})元?',
    'amount2': r'[¥￥](\d+\.\d{1,2})元',
    'payer': r'(?:付款方|购买方)[:：]\s*([\u4e00-\u9fa5A-Za-z0-9（）()]+)',
    'payee': r'(?:收款方|销售方)[:：]\s*([\u4e00-\u9fa5A-Za-z0-9（）()]+)',
    'date': r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)',
    'seal': r'(?:印章|专用章|财务章)',
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


def extract_fixed_invoice_info(ocr_text: str) -> Dict[str, Any]:
    """从 OCR 文本中提取定额发票信息"""
    info = {
        'invoice_type': 'traditional',
        'receipt_type': 'fixed_invoice',
        'source_format': 'image',
        'extracted_at': datetime.now().isoformat(),
    }
    
    # 提取发票代码
    code_match = re.search(FIXED_PATTERNS['invoice_code'], ocr_text)
    if code_match:
        info['invoice_code'] = code_match.group(1)
        info['fixed_invoice_code'] = code_match.group(1)
    
    # 提取发票号码
    number_match = re.search(FIXED_PATTERNS['invoice_number'], ocr_text)
    if number_match:
        info['invoice_number'] = number_match.group(1)
    
    # 提取金额
    amount_match = re.search(FIXED_PATTERNS['amount'], ocr_text)
    if amount_match:
        info['total'] = float(amount_match.group(1))
    else:
        # 尝试直接匹配 ¥xx.xx 元
        amounts = re.findall(r'[¥￥](\d+\.\d{1,2})', ocr_text)
        if amounts:
            info['total'] = float(amounts[0])
    
    # 提取日期
    date_matches = re.findall(FIXED_PATTERNS['date'], ocr_text)
    if date_matches:
        info['billing_date'] = normalize_date(date_matches[0])
    
    # 提取付款方/购买方
    payer_match = re.search(FIXED_PATTERNS['payer'], ocr_text)
    if payer_match:
        info['buyer_name'] = payer_match.group(1).strip()
    
    # 提取收款方/销售方
    payee_match = re.search(FIXED_PATTERNS['payee'], ocr_text)
    if payee_match:
        info['seller_name'] = payee_match.group(1).strip()
    
    # 定额发票不可抵扣进项税
    info['vat_deduction_rate'] = VAT_DEDUCTION_RATES['fixed_invoice']
    info['vat_deduction_amount'] = 0.0
    
    # 费用分类（根据金额和关键词推断）
    amount = info.get('total', 0) or 0
    if amount <= 100:
        info['expense_category'] = '办公费'
    elif amount <= 500:
        info['expense_category'] = '其他费用'
    else:
        info['expense_category'] = '大额费用'
    
    return info


def parse_fixed_invoice(ocr_text: str) -> UnifiedInvoice:
    """解析定额发票 OCR 文本，返回统一数据结构"""
    info = extract_fixed_invoice_info(ocr_text)
    invoice = UnifiedInvoice(**info)
    invoice.raw_text = ocr_text
    return invoice


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python fixed_parser.py <path_to_fixed_invoice_image>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(file_path)
        ocr_text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        
        invoice = parse_fixed_invoice(ocr_text)
        print(invoice.to_json())
    except ImportError:
        print("请先安装 pytesseract: pip install pytesseract", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"解析失败: {e}", file=sys.stderr)
        sys.exit(1)
