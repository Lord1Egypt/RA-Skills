#!/usr/bin/env python3
"""
symx_payment - 真实支付宝支付流程演示
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alipay_real_payment import create_order, ALIPAY_CONFIG

def print_payment_page(order_result):
    """打印支付页面"""
    if not order_result.get("success"):
        print(f"❌ 订单创建失败：{order_result.get('error')}")
        return
    
    pay_url = order_result["pay_url"]
    order_id = order_result["order_id"]
    amount = order_result["amount"]
    subject = order_result["subject"]
    
    print("\n\n")
    print("╔" + "═" * 70 + "╗")
    print("║" + " " * 20 + "🔴 支付宝真实支付 - 订单已创建 🔴" + " " * 20 + "║")
    print("╚" + "═" * 70 + "╝")
    
    print(f"""
┌──────────────────────────────────────────────────────────────────────┐
│  📦 订单信息                                                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  订单 ID:      {order_id}
│  支付金额：    ¥{amount}
│  订单主题：    {subject}
│  支付网关：    支付宝官方网关
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  💳 支付方式                                                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  方式 1：点击链接支付                                                │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ 👉 https://openapi.alipay.com/gateway.do?...                   │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  方式 2：扫码支付（复制链接到浏览器打开后扫码）                      │
│                                                                      │
│  💡 提示：                                                           │
│  • 这是真实支付宝支付，会产生实际扣款                               │
│  • 支付金额为 ¥{amount}（测试金额）                                    │
│  • 支持支付宝余额、余额宝、银行卡等多种支付方式                     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  📋 支付流程                                                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. 点击以上支付链接                                                 │
│  2. 跳转到支付宝收银台页面                                          │
│  3. 扫码或登录支付宝完成支付                                        │
│  4. 支付成功后自动回调                                              │
│  5. 查询订单状态确认支付结果                                        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════

📋 后续操作命令：

# 查询订单状态
python3 alipay_real_payment.py query {order_id}

# 验证支付回调
python3 -c "from alipay_real_payment import verify_notify; print(verify_notify({...}))"

═══════════════════════════════════════════════════════════════════════

✅ 真实支付宝支付订单已创建！
""")

def main():
    print("\n🔐 支付宝商户配置信息：")
    print("=" * 50)
    print(f"  APP_ID: {ALIPAY_CONFIG['app_id']}")
    print(f"  网关地址：{ALIPAY_CONFIG['gateway_url']}")
    print(f"  回调地址：{ALIPAY_CONFIG['notify_url']}")
    print("=" * 50)
    
    # 创建订单
    print("\n正在创建支付订单...")
    result = create_order(
        phone="13800138000",
        amount=0.01,
        detail="增值账户续费 - 真实支付测试"
    )
    
    # 打印支付页面
    print_payment_page(result)
    
    return result

if __name__ == "__main__":
    result = main()
    print("\n订单数据（JSON 格式）：")
    print(json.dumps(result, ensure_ascii=False, indent=2))
