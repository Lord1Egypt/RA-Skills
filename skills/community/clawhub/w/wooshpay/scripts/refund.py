#!/usr/bin/env python3
"""
WooshPay 退款脚本 - 交互式版本
"""

import os
import sys
import json
import requests

BASE_URL = "https://api.wooshpay.com/v1/refunds"

# 退款原因
REFUND_REASONS = {
    "1": ("requested_by_customer", "客户请求退款"),
    "2": ("duplicate", "重复扣款"),
    "3": ("fraudulent", "欺诈交易"),
    "4": ("requested_by_merchant", "商户请求退款"),
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

def input_payment_intent():
    """输入支付订单ID"""
    print("\n🔍 请输入要退款的支付订单ID:")
    print("   格式: pi_xxxxxxxxxxxxxxxxxx")
    print("   ⚠️ 注意：并非所有支付都支持退款，请先咨询 WooshPay 客服")
    
    intent_id = input("订单ID: ").strip()
    
    if not intent_id:
        print("❌ 订单ID不能为空")
        sys.exit(1)
    
    if not intent_id.startswith("pi_"):
        print("❌ 订单ID格式错误，应以 pi_ 开头")
        sys.exit(1)
    
    return intent_id

def input_refund_reason():
    """选择退款原因"""
    print("\n📝 请选择退款原因:")
    for key, (reason, desc) in REFUND_REASONS.items():
        print(f"   {key}. {desc} ({reason})")
    print("   直接回车使用默认: 客户请求退款")
    
    choice = input("选择: ").strip()
    
    if not choice:
        return "requested_by_customer"
    
    if choice in REFUND_REASONS:
        return REFUND_REASONS[choice][0]
    
    print("❌ 无效选择，使用默认")
    return "requested_by_customer"

def input_amount():
    """输入退款金额（可选）"""
    print("\n💰 请输入退款金额（可选）:")
    print("   直接回车表示全额退款")
    print("   输入具体金额表示部分退款")
    
    amount = input("金额: ").strip()
    
    if not amount:
        return None
    
    if amount.isdigit() and int(amount) > 0:
        return int(amount)
    
    print("❌ 无效金额，将全额退款")
    return None

def refund_interactive():
    """交互式退款"""
    
    print("\n" + "="*50)
    print("💸 WooshPay 退款向导")
    print("="*50)
    print("⚠️  注意：并非所有支付都支持退款")
    print("   请先咨询 WooshPay 客服确认")
    print("="*50)
    
    api_key = get_api_key()
    
    # 输入订单ID
    payment_intent = input_payment_intent()
    
    # 确认风险
    print("\n⚠️ 重要提示:")
    print(f"   订单ID: {payment_intent}")
    print("   请确保该订单支持退款后再继续!")
    
    confirm_check = input("\n确认该订单支持退款? (y/n): ").strip().lower()
    if confirm_check != 'y':
        print("❌ 已取消退款")
        return
    
    # 输入退款原因
    reason = input_refund_reason()
    
    # 输入金额
    amount = input_amount()
    
    # 构建请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {api_key}"
    }
    
    data = {
        "payment_intent": payment_intent,
        "reason": reason
    }
    
    if amount:
        data["amount"] = amount
    
    # 确认
    print("\n" + "-"*50)
    print("📋 退款信息确认:")
    print(f"   订单ID: {payment_intent}")
    print(f"   退款原因: {reason}")
    if amount:
        print(f"   退款金额: {amount}")
    else:
        print(f"   退款金额: 全额退款")
    print("-"*50)
    
    confirm = input("\n✅ 确认发起退款? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ 已取消")
        return
    
    print("\n⏳ 正在发起退款...")
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=30)
        result = response.json()
        
        if response.status_code in [200, 201]:
            print("\n" + "="*50)
            print("✅ 退款成功!")
            print("="*50)
            
            print(f"📌 退款ID: {result.get('id')}")
            print(f"📌 状态: {result.get('status')}")
            print(f"📌 金额: {result.get('amount')}")
            print(f"📌 货币: {result.get('currency')}")
            print(f"📌 原因: {result.get('reason')}")
            
            if result.get('payment_intent'):
                print(f"📌 原始订单: {result.get('payment_intent')}")
            
            if result.get('balance_transaction'):
                print(f"📌 交易流水: {result.get('balance_transaction')}")
            
            return result
        else:
            print(f"\n❌ 退款失败: {response.status_code}")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求错误: {e}")
        return None

if __name__ == "__main__":
    refund_interactive()
