import sys
import json
import base64
import os
import random
from datetime import datetime
from file_utils import save_order, load_config, get_db_connection, compute_indicator
from sm4_utils import sm4_encrypt, is_valid_key

SLUG = "塔罗牌占卜"

def create_order(question: str, style: str = "default") -> tuple:
    config = load_config()
    sm4_key_b64 = config.get("crypto", {}).get("sm4_key")
    if not sm4_key_b64 or sm4_key_b64 == "YOUR_SM4_KEY_BASE64":
        raise RuntimeError("请先配置 crypto.sm4_key")
    sm4_key = base64.b64decode(sm4_key_b64)
    if not is_valid_key(sm4_key):
        raise RuntimeError("SM4 密钥必须为 16 字节")
    pay_to = config.get("payment", {}).get("pay_to")
    if not pay_to or pay_to == "YOUR_PAY_TO_VALUE":
        raise RuntimeError("请先配置 payment.pay_to")
    amount = config.get("service", {}).get("amount", 1)
    order_no = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(100000, 999999))
    plain_dict = {"orderNo": order_no, "amount": amount, "payTo": pay_to}
    plain_text = json.dumps(plain_dict, ensure_ascii=False)
    encrypted_data = sm4_encrypt(plain_text, sm4_key)
    conn = get_db_connection()
    now = datetime.now().isoformat()
    conn.execute("INSERT INTO orders (order_no, question, style, amount, pay_to, order_status, fulfill_status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, 'INIT', 'UNFULFILLED', ?, ?)", (order_no, question, style, amount, pay_to, now, now))
    conn.commit()
    conn.close()
    return order_no, amount, encrypted_data, pay_to

def save_order_info(order_no, amount, question, encrypted_data, pay_to, indicator, style):
    order_data = {"skill-id": "si-塔罗牌占卜", "order_no": order_no, "amount": amount, "question": question, "style": style, "encrypted_data": encrypted_data, "pay_to": pay_to, "description": "塔罗牌占卜，回复风格：每日一张牌解读运势", "slug": SLUG, "resource_url": "local"}
    return save_order(indicator, order_no, order_data)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?", default="塔罗牌占卜，回复风格：每日一张牌解读运势")
    parser.add_argument("style", nargs="?", default="default")
    args = parser.parse_args()
    indicator = compute_indicator(SLUG)
    order_no, amount, encrypted_data, pay_to = create_order(args.question, args.style)
    save_order_info(order_no, amount, args.question, encrypted_data, pay_to, indicator, args.style)
    print("ORDER_NO=" + order_no)
    print("AMOUNT=" + str(amount))
    print("QUESTION=" + args.question)
    print("INDICATOR=" + indicator)
