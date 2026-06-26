#!/usr/bin/env python3
"""
WooshPay 创建支付收银台脚本 - 交互式版本
"""

import os
import sys
import json
import requests

BASE_URL = "https://api.wooshpay.com/v1/checkout/sessions"

# 支持的货币
CURRENCIES = ["MYR", "VND", "USD", "CNY", "EUR", "GBP", "THB", "SGD", "IDR"]

# 支持的支付方式
PAYMENT_METHODS = {
    "1": ("touchngo", "Touch 'n Go (马来西亚)"),
    "2": ("momo", "MoMo (越南)"),
    "3": ("vietcombank", "VCB (越南)"),
    "4": ("zalo", "ZaloPay (越南)"),
    "5": ("shopeepay", "ShopeePay (越南)"),
    "6": ("atome", "Atome (东南亚)"),
    "7": ("gopay", "GoPay (印尼)"),
    "8": ("ovo", "OVO (印尼)"),
}

def get_api_key():
    """获取 API Key"""
    api_key = os.environ.get("WOOSHPAY_API_KEY")
    if not api_key:
        print("\n❌ 错误: 请先设置 WOOSHPAY_API_KEY 环境变量")
        print("\n请运行:")
        print("  export WOOSHPAY_API_KEY='你的Base64编码的API Key'")
        sys.exit(1)
    return api_key

def input_product_info():
    """输入商品信息"""
    print("\n📦 请输入商品信息:")
    
    name = input("商品名称: ").strip()
    if not name:
        print("❌ 商品名称不能为空")
        sys.exit(1)
    
    description = input("商品描述 (可选): ").strip() or "商品购买"
    
    return name, description

def input_price():
    """输入价格"""
    print("\n💰 请输入价格:")
    print("   注意：金额为最小货币单位")
    print("   例如: 100 = 1.00 MYR")
    
    while True:
        price = input("金额: ").strip()
        if price.isdigit() and int(price) > 0:
            return int(price)
        print("❌ 请输入有效的正整数")

def input_currency():
    """选择货币"""
    print("\n💱 请选择货币:")
    for curr in CURRENCIES:
        print(f"   {curr}")
    
    while True:
        currency = input("货币 (直接回车默认 MYR): ").strip().upper()
        if not currency:
            return "MYR"
        if currency in CURRENCIES:
            return currency
        print(f"❌ 不支持的货币，可用: {', '.join(CURRENCIES)}")

def input_quantity():
    """输入数量"""
    while True:
        qty = input("数量 (直接回车默认 1): ").strip()
        if not qty:
            return 1
        if qty.isdigit() and int(qty) > 0:
            return int(qty)
        print("❌ 请输入有效的正整数")

def input_payment_methods():
    """选择支付方式（可多选）"""
    print("\n💳 请选择支付方式（可多选，用逗号分隔，如: 1,2,3）:")
    for key, (method, desc) in PAYMENT_METHODS.items():
        print(f"   {key}. {desc} ({method})")
    print("   直接回车选择全部")
    
    choice = input("选择: ").strip()
    
    if not choice:
        return [m for m, _ in PAYMENT_METHODS.values()]
    
    methods = []
    for c in choice.split(","):
        c = c.strip()
        if c in PAYMENT_METHODS:
            methods.append(PAYMENT_METHODS[c][0])
    
    if not methods:
        print("❌ 未选择有效支付方式，使用全部")
        return [m for m, _ in PAYMENT_METHODS.values()]
    
    return methods

def input_urls():
    """输入成功/取消返回地址"""
    print("\n🔗 请输入返回地址:")
    
    success_url = input("支付成功返回地址: ").strip()
    if not success_url:
        print("❌ 成功返回地址不能为空")
        sys.exit(1)
    
    cancel_url = input("取消支付返回地址 (可选): ").strip() or "https://example.com/cancel"
    
    return success_url, cancel_url

def create_checkout_interactive():
    """交互式创建收银台"""
    
    print("\n" + "="*50)
    print("🚀 WooshPay 支付收银台创建向导")
    print("="*50)
    
    api_key = get_api_key()
    
    # 输入商品信息
    product_name, product_desc = input_product_info()
    price = input_price()
    currency = input_currency()
    quantity = input_quantity()
    payment_methods = input_payment_methods()
    success_url, cancel_url = input_urls()
    
    # 构建请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {api_key}"
    }
    
    data = {
        "mode": "payment",
        "success_url": success_url,
        "cancel_url": cancel_url,
        "line_items": [
            {
                "price_data": {
                    "currency": currency,
                    "unit_amount": price,
                    "product_data": {
                        "name": product_name,
                        "description": product_desc
                    }
                },
                "quantity": quantity
            }
        ]
    }
    
    # 确认订单
    total = price * quantity
    print("\n" + "-"*50)
    print("📋 收银台信息确认:")
    print(f"   商品: {product_name}")
    print(f"   描述: {product_desc}")
    print(f"   单价: {price} {currency}")
    print(f"   数量: {quantity}")
    print(f"   总计: {total} {currency}")
    print(f"   支付方式: {', '.join(payment_methods)}")
    print(f"   成功返回: {success_url}")
    print(f"   取消返回: {cancel_url}")
    print("-"*50)
    
    confirm = input("\n✅ 确认创建收银台? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ 已取消")
        return
    
    print("\n⏳ 正在创建收银台...")
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=30)
        result = response.json()
        
        if response.status_code in [200, 201]:
            print("\n" + "="*50)
            print("✅ 收银台创建成功!")
            print("="*50)
            
            print(f"📌 Session ID: {result.get('id')}")
            print(f"📌 状态: {result.get('status')}")
            print(f"📌 金额: {result.get('amount_total')} {result.get('currency')}")
            print(f"📌 过期时间: {result.get('expires_at')}")
            
            # 获取支付链接
            checkout_url = result.get('url')
            if checkout_url:
                print(f"\n" + "="*50)
                print("🔗 支付链接 (发给客户):")
                print("="*50)
                print(f"   {checkout_url}")
                print("="*50)
            
            client_secret = result.get('client_secret')
            if client_secret:
                print(f"\n📌 Client Secret: {client_secret}")
            
            return result
        else:
            print(f"\n❌ 创建失败: {response.status_code}")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求错误: {e}")
        return None

if __name__ == "__main__":
    create_checkout_interactive()
