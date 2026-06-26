#!/usr/bin/env python3
"""
symx_payment - 完整支付流程测试（1 分钱测试）
创建虚拟订单 → 调起支付宝支付
"""

import json
import os
from datetime import datetime

def create_test_order(amount=0.01):
    """创建测试订单"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    order = {
        "orderId": f"TEST_{timestamp}",
        "outTradeNo": f"TRADE_{timestamp}",
        "subject": "增值账户续费 - 1 分钱测试",
        "totalAmount": amount,
        "body": "支付宝支付流程测试 - 1 分钱",
        "timeout": "30m",
        "phoneNumber": "13800138000",
        "detail": f"增值账户续费 - 标准套餐 - 账号：13800138000 - 金额：{amount}元 - 备注：1 分钱支付测试"
    }
    
    return order

def generate_alipay_url(order):
    """生成支付宝收银台链接"""
    base_url = "https://excashier.alipay.com/pc.htm"
    params = {
        "outTradeNo": order["outTradeNo"],
        "totalAmount": str(order["totalAmount"]),
        "subject": order["subject"],
        "body": order.get("body", ""),
        "timeout": order.get("timeout", "30m")
    }
    param_str = "&".join([f"{k}={v}" for k, v in params.items() if v])
    return f"{base_url}?{param_str}"

def main():
    # 创建订单
    order = create_test_order(0.01)
    cashier_url = generate_alipay_url(order)
    
    print("\n\n")
    print("╔" + "═" * 70 + "╗")
    print("║" + " " * 22 + "🔴 支付宝支付流程测试 - 1 分钱 🔴" + " " * 22 + "║")
    print("╚" + "═" * 70 + "╝")
    
    print(f"""
┌──────────────────────────────────────────────────────────────────────┐
│  📦 测试订单信息                                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  订单 ID:      {order["orderId"]}
│  交易号：      {order["outTradeNo"]}
│  订单主题：    {order["subject"]}
│  订单描述：    {order["body"]}
│  支付金额：    ¥{order["totalAmount"]} (1 分钱测试)
│  超时时间：    {order["timeout"]}
│  增值账号：    {order["phoneNumber"]}
│  充值明细：    {order["detail"]}
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  📱 支付宝收银台链接                                                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  {cashier_url}
│                                                                      │
│  💡 支付方式：                                                       │
│  • 电脑端：复制链接到浏览器打开，扫码支付                           │
│  • 手机端：点击链接唤起支付宝 APP 完成支付                            │
│  • 测试金额：¥{order["totalAmount"]}，不会实际扣款（沙箱环境）                 │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  🔴 调起支付宝支付技能                                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  检测到 excashier.alipay.com 链接，自动触发 alipay-pay-for-service 技能   │
│                                                                      │
│  [ALIPAY_PAYMENT_REQUEST]                                            │
│  {json.dumps({
    "action": "alipay_payment",
    "orderId": order["orderId"],
    "outTradeNo": order["outTradeNo"],
    "cashierUrl": cashier_url,
    "amount": order["totalAmount"],
    "subject": order["subject"],
    "instruction": "请调起支付宝支付技能完成 1 分钱测试支付"
}, ensure_ascii=False, indent=4)}
│  [/ALIPAY_PAYMENT_REQUEST]                                           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════

📋 支付流程：

1. ✅ 创建虚拟订单（1 分钱）
2. ✅ 生成支付宝收银台链接
3. 🔴 调起支付宝支付技能
4. ⏳ 等待用户完成支付
5. ⏳ 支付成功后回调

═══════════════════════════════════════════════════════════════════════

✅ 测试订单已创建，支付宝支付链接已生成！
""")
    
    return {
        "order": order,
        "cashierUrl": cashier_url
    }

if __name__ == "__main__":
    result = main()
