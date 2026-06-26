#!/usr/bin/env python3
"""
WooshPay 创建支付订单脚本 - 交互式版本
"""

import os
import sys
import json
import requests

BASE_URL = "https://api.wooshpay.com/v1/payment_intents"

# 支持的支付方式
PAYMENT_METHODS = {
    "1": ("momo", "越南 MoMo 电子钱包"),
    "2": ("vietcombank", "越南 VCB 银行"),
    "3": ("zalo", "越南 ZaloPay"),
    "4": ("shopeepay", "ShopeePay"),
    "5": ("atome", "Atome 先买后付"),
}

# 支持的货币
CURRENCIES = ["VND", "USD", "CNY", "EUR", "GBP", "THB", "MYR", "SGD"]

def get_api_key():
    """获取 API Key"""
    api_key = os.environ.get("WOOSHPAY_API_KEY")
    if not api_key:
        print("\n❌ 错误: 请先设置 WOOSHPAY_API_KEY 环境变量")
        print("\n请运行以下命令设置 API Key:")
        print("  export WOOSHPAY_API_KEY='你的Base64编码的API Key'")
        print("\n或直接在对话中告诉我你的 API Key，我来帮你设置")
        sys.exit(1)
    return api_key

def input_amount():
    """输入金额"""
    print("\n💰 请输入支付金额（最小货币单位）:")
    print("   例如: 100000 = 1,000,000 VND (如果currency=VND)")
    while True:
        amount = input("金额: ").strip()
        if amount.isdigit() and int(amount) > 0:
            return int(amount)
        print("❌ 请输入有效的正整数")

def input_currency():
    """选择货币"""
    print("\n💱 请选择货币:")
    for curr in CURRENCIES:
        print(f"   {curr}")
    
    while True:
        currency = input("货币 (直接回车默认 VND): ").strip().upper()
        if not currency:
            return "VND"
        if currency in CURRENCIES:
            return currency
        print(f"❌ 不支持的货币，可用: {', '.join(CURRENCIES)}")

def input_payment_method():
    """选择支付方式"""
    print("\n💳 请选择支付方式:")
    for key, (method, desc) in PAYMENT_METHODS.items():
        print(f"   {key}. {desc} ({method})")
    
    while True:
        choice = input("选择 (1-5): ").strip()
        if choice in PAYMENT_METHODS:
            return PAYMENT_METHODS[choice][0]
        print("❌ 请输入 1-5 之间的数字")

def input_buyer_info():
    """输入买家信息"""
    print("\n👤 请输入买家信息（直接回车跳过）:")
    
    name = input("姓名: ").strip() or None
    email = input("邮箱: ").strip() or None
    
    return name, email

def input_return_url():
    """输入回调地址"""
    print("\n🔗 请输入支付完成后跳转的地址:")
    url = input("返回地址: ").strip()
    return url if url else None

def create_payment_interactive():
    """交互式创建支付订单"""
    
    print("\n" + "="*50)
    print("🚀 WooshPay 支付订单创建向导")
    print("="*50)
    
    # 获取 API Key
    api_key = get_api_key()
    
    # 依次输入各项信息
    amount = input_amount()
    currency = input_currency()
    payment_method = input_payment_method()
    buyer_name, buyer_email = input_buyer_info()
    return_url = input_return_url()
    
    # 构建请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {api_key}"
    }
    
    data = {
        "amount": amount,
        "currency": currency,
        "confirm": True,
        "payment_method_data": {
            "type": payment_method
        }
    }
    
    if return_url:
        data["return_url"] = return_url
    
    if buyer_name or buyer_email:
        data["payment_method_data"]["billing_details"] = {}
        if buyer_name:
            data["payment_method_data"]["billing_details"]["name"] = buyer_name
        if buyer_email:
            data["payment_method_data"]["billing_details"]["email"] = buyer_email
    
    # 确认订单
    print("\n" + "-"*50)
    print("📋 订单信息确认:")
    print(f"   金额: {amount} {currency}")
    print(f"   支付方式: {payment_method}")
    if buyer_name:
        print(f"   姓名: {buyer_name}")
    if buyer_email:
        print(f"   邮箱: {buyer_email}")
    if return_url:
        print(f"   返回地址: {return_url}")
    print("-"*50)
    
    confirm = input("\n✅ 确认创建订单? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ 已取消")
        return
    
    print("\n⏳ 正在创建订单...")
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=30)
        result = response.json()
        
        if response.status_code in [200, 201]:
            print("\n" + "="*50)
            print("✅ 订单创建成功!")
            print("="*50)
            print(f"📌 订单ID: {result.get('id')}")
            print(f"📌 状态: {result.get('status')}")
            print(f"📌 金额: {result.get('amount')} {result.get('currency')}")
            print(f"📌 Client Secret: {result.get('client_secret')}")
            
            # 获取支付链接
            payment_url = None
            if result.get('next_action'):
                next_action = result.get('next_action')
                
                # momo_handle_redirect -> bank_transfer_vn_handle_redirect -> url
                if 'bank_transfer_vn_handle_redirect' in next_action:
                    bank_data = next_action.get('bank_transfer_vn_handle_redirect', {})
                    payment_url = bank_data.get('url')
                    qrcode = bank_data.get('qrcode')
                    if qrcode:
                        print(f"\n📱 MoMo 二维码:")
                        print(f"   {qrcode}")
                elif 'url' in next_action:
                    payment_url = next_action.get('url')
            
            if payment_url:
                print(f"\n" + "="*50)
                print("🔗 支付链接 (发给客户):")
                print("="*50)
                print(f"   {payment_url}")
                print("="*50)
            
            if result.get('cancellation_reason'):
                print(f"⚠️ 取消原因: {result.get('cancellation_reason')}")
            
            return result
        else:
            print(f"\n❌ 创建失败: {response.status_code}")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求错误: {e}")
        return None

if __name__ == "__main__":
    create_payment_interactive()
