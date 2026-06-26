#!/usr/bin/env python3
import sys
import json
import re
from pathlib import Path

def extract_receipt_fields(ocr_text):
    data = {}
    # Amount
    amount_match = re.search(r'TOTAL[:\s]*[\$]?([0-9,]+\.?[0-9]*)', ocr_text, re.IGNORECASE)
    data['total'] = amount_match.group(1).replace(',', '') if amount_match else None
    # Date
    date_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', ocr_text)
    if date_match:
        data['date'] = '0/1/2'.format(date_match.group(1), date_match.group(2), date_match.group(3))
    # Vendor
    lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
    data['vendor'] = lines[0] if lines else None
    # receipt specific
    if 'receipt' in ['mileage', 'log']:
        mileage_match = re.search(r'(\d{1,3}(?:,\d{3})*)', ocr_text)
        data['mileage'] = mileage_match.group(1).replace(',', '') if mileage_match else None
    data['category'] = 'receipt'
    return data

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ocr_text = Path(sys.argv[1]).read_text(encoding='utf-8')
    else:
        ocr_text = sys.stdin.read()
    result = extract_receipt_fields(ocr_text)
    print(json.dumps(result, indent=2))
