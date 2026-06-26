import sys
import json
import base64
import os
import random
from datetime import datetime

from file_utils import save_order, load_config, compute_indicator
from sm4_utils import sm4_encrypt, is_valid_key

# 硬编码的 slug，用于计算 indicator
SLUG = "ai-chunlian"


def create_order(question: str) -> tuple:
    """创建订单，返回 (order_no, amount, encrypted_data, pay_to)"""
    config = load_config()
    
    # 从配置获取
    sm4_key_b64 = config.get("crypto", {}).get("sm4_key")
    if not sm4_key_b64:
        raise RuntimeError("配置文件缺少 crypto.sm4_key")
    
    try:
        sm4_key = base64.b64decode(sm4_key_b64)
    except Exception:
        raise RuntimeError("crypto.sm4_key 必须是有效的 Base64 编码")
    
    if not is_valid_key(sm4_key):
        raise RuntimeError("SM4 密钥必须为 16 字节")
    
    pay_to = config.get("payment", {}).get("pay_to")
    if not pay_to:
        raise RuntimeError("配置文件缺少 payment.pay_to")
    
    amount = config.get("service", {}).get("amount", 1)
    
    # 生成订单号
    order_no = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(100000, 999999))
    
    # 构建明文数据
    plain_dict = {
        "orderNo": order_no,
        "amount": amount,
        "payTo": pay_to
    }
    plain_text = json.dumps(plain_dict, ensure_ascii=False)
    
    # SM4 加密（ECB 模式）
    encrypted_data = sm4_encrypt(plain_text, sm4_key)
    
    return order_no, amount, encrypted_data, pay_to


def save_order_info(order_no: str, amount: str, question: str,
                    encrypted_data: str, pay_to: str, indicator: str) -> str:
    """保存订单信息"""
    order_data = {
        "skill-id": f"si-{SLUG}",
        "order_no": order_no,
        "amount": amount,
        "question": question,
        "encrypted_data": encrypted_data,
        "pay_to": pay_to,
        "description": "春联生成服务费用",
        "slug": SLUG,
        "resource_url": "local",
    }
    return save_order(indicator, order_no, order_data)


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create order")
    parser.add_argument("question", help="Service description")
    args = parser.parse_args()

    indicator = compute_indicator(SLUG)

    try:
        order_no, amount, encrypted_data, pay_to = create_order(args.question)
    except RuntimeError as e:
        print(f"订单创建失败: {e}")
        sys.exit(1)

    save_order_info(order_no, amount, args.question,
                    encrypted_data, pay_to, indicator)

    print(f"ORDER_NO={order_no}")
    print(f"AMOUNT={amount}")
    print(f"QUESTION={args.question}")
    print(f"INDICATOR={indicator}")
