#!/usr/bin/env python3
"""
从OCR识别结果自动加入股票池
使用方法: python add_stocks.py [img_path]
"""

import json
import sys
from datetime import datetime
from rapidocr_onnxruntime import RapidOCR
import cv2

STOCK_LIST_PATH = "/Users/wy/.openclaw/workspace-changniu/stone_quant/manual_stock_list.json"
MAX_STOCKS = 30

def ocr_stocks(img_path):
    """从图片识别股票"""
    ocr = RapidOCR()
    img = cv2.imread(img_path)
    result, _ = ocr(img)
    
    if not result:
        return []
    
    # 解析股票列表
    stocks = []
    for i, (bbox, text, conf) in enumerate(result):
        if text.isdigit() and len(text) == 6:
            code = text
            # 尝试获取名称（下一条）
            name = ""
            if i + 1 < len(result):
                next_text = result[i + 1][1]
                # 名称不应该是纯数字
                if not next_text.isdigit():
                    name = next_text
            stocks.append({"code": code, "name": name})
    
    return stocks

def load_stock_list():
    """加载现有股票列表"""
    try:
        with open(STOCK_LIST_PATH, 'r') as f:
            return json.load(f)
    except:
        return {"stocks": []}

def save_stock_list(data):
    """保存股票列表"""
    with open(STOCK_LIST_PATH, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_stocks(new_stocks, source="图片识别"):
    """添加股票到列表，FIFO去重"""
    data = load_stock_list()
    existing_codes = {s['code'] for s in data['stocks']}
    add_time = datetime.now().strftime("%H:%M")
    
    added = []
    skipped = []
    
    for stock in new_stocks:
        code = stock['code']
        name = stock.get('name', '')
        
        if code not in existing_codes:
            data['stocks'].append({
                "code": code,
                "name": name,
                "add_time": add_time,
                "source": source
            })
            added.append((code, name))
        else:
            skipped.append((code, name))
    
    # FIFO: 超过30只移除最旧的
    removed = []
    if len(data['stocks']) > MAX_STOCKS:
        data['stocks'].sort(key=lambda x: (x.get('add_time', ''), x['code']))
        removed = data['stocks'][:-MAX_STOCKS]
        data['stocks'] = data['stocks'][-MAX_STOCKS:]
    
    save_stock_list(data)
    
    return {
        "added": added,
        "skipped": skipped,
        "removed": removed,
        "total": len(data['stocks'])
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python add_stocks.py <图片路径>")
        sys.exit(1)
    
    img_path = sys.argv[1]
    
    # 识别股票
    stocks = ocr_stocks(img_path)
    if not stocks:
        print("未识别到股票")
        sys.exit(1)
    
    print(f"识别到 {len(stocks)} 只股票")
    
    # 加入列表
    result = add_stocks(stocks)
    
    print(f"\n新增: {len(result['added'])} 只")
    for code, name in result['added']:
        print(f"  ✅ {code} {name}")
    
    print(f"\n已存在: {len(result['skipped'])} 只")
    for code, name in result['skipped']:
        print(f"  ⏭️  {code} {name}")
    
    if result['removed']:
        print(f"\nFIFO移除: {len(result['removed'])} 只")
        for s in result['removed']:
            print(f"  ❌ {s['code']} {s['name']}")
    
    print(f"\n当前股票池: {result['total']} 只")

if __name__ == "__main__":
    main()
