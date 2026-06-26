#!/usr/bin/env python3
"""
更新交易标的清单
用法: python3 update_stock_list.py <uuid> [--dry-run]
"""
import json
import sys
from datetime import datetime
from pathlib import Path

def ocr_stocks(uuid: str) -> list:
    """用RapidOCR识别图片中的股票"""
    try:
        from rapidocr_onnxruntime import RapidOCR
        import cv2
        
        img_path = f"/Users/wy/.openclaw/media/inbound/{uuid}.jpg"
        img = cv2.imread(img_path)
        if img is None:
            print(f"❌ 图片不存在: {img_path}")
            return []
        
        ocr = RapidOCR()
        result, _ = ocr(img)
        
        if not result:
            print("⚠️ 未识别到文字")
            return []
        
        stocks = []
        for line in result:
            bbox, text, confidence = line
            if confidence < 0.9:
                continue
            # 6位数字股票代码
            if len(text) == 6 and text.isdigit():
                stocks.append({"code": text, "name": "", "add_time": datetime.now().strftime("%Y-%m-%d %H:%M")})
            # 排除无关文字
            skip = ['万热度', '天板', '热股', '板块', 'ETF', '热门', '可转债', '新股', '技术交易', 
                    '大家都在看', '快速飙升中', '同花顺', '分钟前', '公告', '公司']
            if any(s in text for s in skip):
                continue
            # 清理后的中文名称
            if len(text) >= 2 and len(text) <= 8 and not any(c in text for c in '+-%>0123456789'):
                # 可能的名字，暂存
                pass
        
        return stocks
    except Exception as e:
        print(f"❌ OCR失败: {e}")
        return []

def load_current_list() -> dict:
    """加载当前清单"""
    path = Path("/Users/wy/.openclaw/workspace-changniu/stone_quant/manual_stock_list.json")
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"stocks": [], "update_date": "", "note": ""}

def save_list(data: dict):
    """保存清单"""
    data['update_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    path = Path("/Users/wy/.openclaw/workspace-changniu/stone_quant/manual_stock_list.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存到 {path}")

def fifo_limit(stocks: list, limit: int = 30) -> list:
    """FIFO: 超过30只时保留最新的"""
    if len(stocks) > limit:
        print(f"⚠️ 超过30只，执行FIFO，保留前{limit}只")
        return stocks[:limit]
    return stocks

def main():
    if len(sys.argv) < 2:
        print("用法: python3 update_stock_list.py <uuid>")
        sys.exit(1)
    
    uuid = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    
    print(f"📷 开始识别图片: {uuid}")
    new_stocks = ocr_stocks(uuid)
    
    if not new_stocks:
        print("❌ 未识别到股票")
        sys.exit(1)
    
    print(f"✅ 识别到 {len(new_stocks)} 只股票")
    
    data = load_current_list()
    existing_codes = {s['code'] for s in data['stocks']}
    
    # 追加新股票（去重）
    added = 0
    for stock in new_stocks:
        if stock['code'] not in existing_codes:
            data['stocks'].append(stock)
            existing_codes.add(stock['code'])
            added += 1
    
    print(f"➕ 新增 {added} 只股票")
    
    # FIFO限制
    data['stocks'] = fifo_limit(data['stocks'])
    
    print(f"📋 当前共 {len(data['stocks'])} 只股票")
    
    if not dry_run:
        save_list(data)
    
    # 打印清单
    print("\n📋 交易标的清单:")
    for i, s in enumerate(data['stocks'], 1):
        name = s.get('name', '-') or '-'
        add_time = s.get('add_time', '-')
        print(f"  {i}. {s['code']} {name} ({add_time})")

if __name__ == "__main__":
    main()
