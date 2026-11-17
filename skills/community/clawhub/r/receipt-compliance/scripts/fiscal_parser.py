#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财政票据 OCR 专用解析器
识别非税收入票据、罚没票据等财政票据并输出统一数据结构
"""

import re
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from unified_invoice import UnifiedInvoice, VAT_DEDUCTION_RATES


# === 财政票据正则匹配模式 ===
FISCAL_PATTERNS = {
    'payer': r'(?:缴款人|付款人|购买方)[:：]\s*([\u4e00-\u9fa5A-Za-z0-9（）()（）]+)',
    'payee': r'(?:收款人|执收单位|财政)[:：]\s*([\u4e00-\u9fa5A-Za-z0-9（）()]+)',
    'amount': r'(?:金额|缴款金额)[:：]\s*[¥￥]?(\d+\.\d{1,2})元?',
    'amount2': r'[¥￥](\d+\.\d{1,2})元',
    'date': r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)',
    'project': r'(?:项目|款项|收入项目)[:：]\s*([\u4e00-\u9fa5A-Za-z0-9]+)',
    'fiscal_type': r'(?:非税收入|罚没|行政事业性收费|政府性基金|国有资产|票据)',
    'invoice_number': r'\d{8,20}',
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


def extract_fiscal_info(ocr_text: str) -> Dict[str, Any]:
    """从 OCR 文本中提取财政票据信息"""
    info = {
        'invoice_type': 'traditional',
        'receipt_type': 'fiscal_receipt',
        'source_format': 'image',
        'extracted_at': datetime.now().isoformat(),
    }
    
    # 提取缴款人
    payer_match = re.search(FISCAL_PATTERNS['payer'], ocr_text)
    if payer_match:
        info['buyer_name'] = payer_match.group(1).strip()
    
    # 提取执收单位
    payee_match = re.search(FISCAL_PATTERNS['payee'], ocr_text)
    if payee_match:
        info['seller_name'] = payee_match.group(1).strip()
    
    # 提取金额
    amount_match = re.search(FISCAL_PATTERNS['amount'], ocr_text)
    if amount_match:
        info['total'] = float(amount_match.group(1))
    else:
        amounts = re.findall(r'[¥￥](\d+\.\d{1,2})', ocr_text)
        if amounts:
            info['total'] = float(amounts[0])
    
    # 提取日期
    date_matches = re.findall(FISCAL_PATTERNS['date'], ocr_text)
    if date_matches:
        info['billing_date'] = normalize_date(date_matches[0])
    
    # 提取项目类型
    project_match = re.search(FISCAL_PATTERNS['project'], ocr_text)
    if project_match:
        info['fiscal_receipt_type'] = project_match.group(1).strip()
    
    # 财政票据不可抵扣进项税
    info['vat_deduction_rate'] = VAT_DEDUCTION_RATES['fiscal_receipt']
    info['vat_deduction_amount'] = 0.0
    
    # 费用分类（不可抵扣）
    info['expense_category'] = '财政票据'
    
    return info


def parse_fiscal_receipt(ocr_text: str) -> UnifiedInvoice:
    """解析财政票据 OCR 文本，返回统一数据结构"""
    info = extract_fiscal_info(ocr_text)
    invoice = UnifiedInvoice(**info)
    invoice.raw_text = ocr_text
    return invoice


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python fiscal_parser.py <path_to_fiscal_receipt_image>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(file_path)
        ocr_text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        
        invoice = parse_fiscal_receipt(ocr_text)
        print(invoice.to_json())
    except ImportError:
        print("请先安装 pytesseract: pip install pytesseract", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"解析失败: {e}", file=sys.stderr)
        sys.exit(1)
