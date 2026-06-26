#!/usr/bin/env python3
"""
WooshPay 查询支付订单脚本 - 交互式版本
"""

import os
import sys
import json
import requests

BASE_URL = "https://api.wooshpay.com/v1/payment_intents"

# 订单状态映射
STATUS_MAP = {
    "requires_payment_method": "等待支付",
    "requires_confirmation": "待确认",
    "requires_action": "需要操作",
    "processing": "处理中",
    "succeeded": "支付成功",
    "canceled": "已取消",
    "failed": "支付失败"
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

def input_order_id():
    """输入订单ID"""
    print("\n🔍 请输入要查询的订单ID:")
    print("   格式: pi_xxxxxxxxxxxxxxxxxx")
    order_id = input("订单ID: ").strip()
    
    if not order_id:
        print("❌ 订单ID不能为空")
        sys.exit(1)
    
    # 补全完整URL
    if not order_id.startswith("http"):
        if not order_id.startswith("pi_"):
            print("❌ 订单ID格式错误，应以 pi_ 开头")
            sys.exit(1)
    
    return order_id

def get_payment_interactive():
    """交互式查询支付订单"""
    
    print("\n" + "="*50)
    print("🔍 WooshPay 订单查询")
    print("="*50)
    
    api_key = get_api_key()
    order_id = input_order_id()
    
    headers = {
        "Authorization": f"Basic {api_key}"
    }
    
    # 构建URL
    if order_id.startswith("http"):
        url = order_id
    else:
        url = f"{BASE_URL}/{order_id}"
    
    print(f"\n⏳ 正在查询订单 {order_id}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("\n" + "="*50)
            print("📋 订单详情")
            print("="*50)
            
            status = result.get('status', 'unknown')
            status_cn = STATUS_MAP.get(status, status)
            
            print(f"📌 订单ID: {result.get('id')}")
            print(f"📌 状态: {status} ({status_cn})")
            print(f"📌 金额: {result.get('amount')} {result.get('currency')}")
            print(f"📌 创建时间: {result.get('created')}")
            print(f"📌 支付方式: {', '.join(result.get('payment_method_types', []))}")
            
            if result.get('client_secret'):
                print(f"📌 Client Secret: {result.get('client_secret')}")
            
            if result.get('payment_method'):
                print(f"📌 Payment Method ID: {result.get('payment_method')}")
            
            if result.get('return_url'):
                print(f"📌 返回地址: {result.get('return_url')}")
            
            if result.get('next_action'):
                print(f"\n📌 Next Action: {result.get('next_action')}")
            
            # 成功提示
            if status == "succeeded":
                print("\n✅ 订单已支付成功!")
            elif status == "failed":
                print("\n❌ 订单支付失败")
            elif status == "canceled":
                print("\n⚠️ 订单已取消")
            elif status == "requires_action":
                print("\n⏳ 订单待支付，请提醒客户完成支付")
            
            return result
        else:
            print(f"\n❌ 查询失败: {response.status_code}")
            try:
                error = response.json()
                print(json.dumps(error, indent=2, ensure_ascii=False))
            except:
                print(response.text)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求错误: {e}")
        return None

if __name__ == "__main__":
    get_payment_interactive()
