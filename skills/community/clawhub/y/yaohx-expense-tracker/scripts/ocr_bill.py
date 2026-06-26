#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
支付截图 OCR 识别脚本
支持微信支付和支付宝截图的账单信息提取

用法:
    python3 ocr_bill.py <图片路径>

依赖 (按优先级):
    1. easyocr (推荐，中文识别效果好，pip install easyocr)
    2. pytesseract + Tesseract OCR (需要安装 Tesseract: https://github.com/tesseract-ocr/tesseract)
    3. 无需依赖的纯文本输出 (兜底方案，提示用户手动输入)
"""

import json
import os
import re
import sys
from datetime import datetime


def try_easyocr(image_path):
    """使用 easyocr 进行中文 OCR 识别"""
    try:
        import easyocr
        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        results = reader.readtext(image_path)
        texts = [item[1] for item in results]
        return "\n".join(texts)
    except ImportError:
        return None
    except Exception as e:
        print(f"[easyocr 错误] {e}", file=sys.stderr)
        return None


def try_pytesseract(image_path):
    """使用 pytesseract 进行 OCR 识别"""
    try:
        from PIL import Image
        import pytesseract
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        return text
    except ImportError:
        return None
    except Exception as e:
        print(f"[pytesseract 错误] {e}", file=sys.stderr)
        return None


def parse_wechat_payment(text):
    """
    解析微信支付账单信息
    常见格式:
        微信支付
        收款方: XXX
        金额: ¥XX.XX
        支付方式: XXX
        交易时间: XXXX-XX-XX XX:XX:XX
    """
    records = []

    # 尝试匹配微信支付格式
    # 金额匹配
    amount_patterns = [
        r'[¥￥]\s*(\d+\.?\d{0,2})',
        r'金额[：:]\s*(\d+\.?\d{0,2})',
        r'付款金额[：:]\s*[¥￥]?\s*(\d+\.?\d{0,2})',
        r'消费[：:]\s*[¥￥]?\s*(\d+\.?\d{0,2})',
        r'实付[：:]\s*[¥￥]?\s*(\d+\.?\d{0,2})',
    ]

    # 商家匹配
    merchant_patterns = [
        r'收款方[：:]\s*(.+?)(?:\n|$)',
        r'商户[：:]\s*(.+?)(?:\n|$)',
        r'商家[：:]\s*(.+?)(?:\n|$)',
        r'对方[：:]\s*(.+?)(?:\n|$)',
    ]

    # 时间匹配
    time_patterns = [
        r'(\d{4}[-/]\d{2}[-/]\d{2})\s+(\d{2}:\d{2}:\d{2})',
        r'交易时间[：:]\s*(\d{4}[-/]\d{2}[-/]\d{2})\s*(\d{2}:\d{2}:\d{2})?',
        r'支付时间[：:]\s*(\d{4}[-/]\d{2}[-/]\d{2})\s*(\d{2}:\d{2}:\d{2})?',
    ]

    # 支付方式匹配
    payment_patterns = [
        r'支付方式[：:]\s*(.+?)(?:\n|$)',
        r'付款方式[：:]\s*(.+?)(?:\n|$)',
    ]

    # 提取金额
    amount = None
    for pattern in amount_patterns:
        match = re.search(pattern, text)
        if match:
            amount = float(match.group(1))
            break

    # 提取商家
    merchant = ""
    for pattern in merchant_patterns:
        match = re.search(pattern, text)
        if match:
            merchant = match.group(1).strip()
            break

    # 提取时间
    date_str = ""
    time_str = ""
    for pattern in time_patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(1).replace("/", "-")
            if match.lastindex and match.lastindex >= 2 and match.group(2):
                time_str = match.group(2)
            break

    # 提取支付方式
    payment_method = ""
    for pattern in payment_patterns:
        match = re.search(pattern, text)
        if match:
            payment_method = match.group(1).strip()
            break

    # 判断来源
    if "支付宝" in text or "alipay" in text.lower():
        source = "支付宝截图"
        if not payment_method:
            payment_method = "支付宝"
    elif "微信" in text or "wechat" in text.lower():
        source = "微信支付截图"
        if not payment_method:
            payment_method = "微信支付"
    else:
        source = "截图识别"

    if amount is not None:
        records.append({
            "date": date_str or datetime.now().strftime("%Y-%m-%d"),
            "time": time_str or datetime.now().strftime("%H:%M:%S"),
            "amount": amount,
            "currency": "CNY",
            "merchant": merchant or "未知商家",
            "payment_method": payment_method,
            "notes": "",
            "source": source
        })

    return records


def parse_alipay_payment(text):
    """
    解析支付宝账单信息
    常见格式:
        支付宝
        对方账户: XXX
        付款金额: ¥XX.XX
        商品说明: XXX
        创建时间: XXXX-XX-XX XX:XX
    """
    records = parse_wechat_payment(text)  # 复用通用解析逻辑

    # 支付宝特有的额外字段
    product_match = re.search(r'商品说明[：:]\s*(.+?)(?:\n|$)', text)
    if product_match and records:
        records[0]["notes"] = product_match.group(1).strip()

    # 调整 source
    for record in records:
        if "支付宝" in text or "alipay" in text.lower():
            record["source"] = "支付宝截图"

    return records


def ocr_bill(image_path):
    """主 OCR 识别流程"""
    if not os.path.exists(image_path):
        return {"status": "error", "message": f"图片文件不存在: {image_path}"}

    # 尝试 OCR 引擎
    raw_text = None
    engine = None

    # 优先 easyocr
    raw_text = try_easyocr(image_path)
    if raw_text:
        engine = "easyocr"
    else:
        # 回退到 pytesseract
        raw_text = try_pytesseract(image_path)
        if raw_text:
            engine = "pytesseract"

    if not raw_text:
        return {
            "status": "error",
            "message": "OCR 识别失败。请确保已安装 easyocr (pip install easyocr) 或 Tesseract OCR。\n"
                       "您也可以手动输入账单信息。",
            "engine": None,
            "raw_text": None,
            "records": []
        }

    print(f"[OCR 引擎] {engine}", file=sys.stderr)
    print(f"[原始文本]\n{raw_text}", file=sys.stderr)

    # 解析账单
    records = parse_wechat_payment(raw_text)
    if not records:
        records = parse_alipay_payment(raw_text)

    # 如果没有识别到消费记录，返回原始文本让用户手动处理
    if not records:
        return {
            "status": "partial",
            "message": "未能识别到有效的账单信息，以下是 OCR 原始文本，请手动输入。",
            "engine": engine,
            "raw_text": raw_text,
            "records": []
        }

    return {
        "status": "success",
        "message": f"成功识别 {len(records)} 条消费记录",
        "engine": engine,
        "raw_text": raw_text,
        "records": records
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python3 ocr_bill.py <图片路径>", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]
    result = ocr_bill(image_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
