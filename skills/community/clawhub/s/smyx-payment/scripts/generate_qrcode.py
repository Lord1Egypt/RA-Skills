#!/usr/bin/env python3
"""
symx_payment - 生成支付宝收款二维码
"""

import json
import os
import qrcode
from alipay_pay import create_order, ALIPAY_CONFIG

def generate_qr_code(pay_url, output_path="./qrcode.png"):
    """
    生成二维码图片
    
    Args:
        pay_url: 支付链接
        output_path: 输出路径
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(pay_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    
    return output_path

def main():
    print("\n\n")
    print("╔" + "═" * 70 + "╗")
    print("║" + " " * 22 + "🔴 支付宝收款码 - 1 分钱测试 🔴" + " " * 22 + "║")
    print("╚" + "═" * 70 + "╝")
    
    # 创建订单
    print("\n正在创建支付订单...")
    result = create_order(
        phone="13800138000",
        amount=0.01,
        detail="增值账户续费 - 扫码支付测试"
    )
    
    if not result.get("success"):
        print(f"❌ 订单创建失败：{result.get('error')}")
        return
    
    pay_url = result["pay_url"]
    order_id = result["order_id"]
    amount = result["amount"]
    
    print(f"✅ 订单创建成功")
    print(f"   订单 ID: {order_id}")
    print(f"   支付金额：¥{amount}")
    
    # 生成二维码
    print("\n正在生成收款二维码...")
    qr_path = generate_qr_code(pay_url, "./payment_qrcode.png")
    print(f"✅ 二维码已生成：{qr_path}")
    
    # 打印支付信息
    print(f"""
┌──────────────────────────────────────────────────────────────────────┐
│  📱 扫码支付                                                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  订单 ID:    {order_id}
│  支付金额：  ¥{amount}
│  二维码：    {qr_path}
│                                                                      │
│  💡 支付方式：                                                       │
│  1. 打开支付宝 APP                                                   │
│  2. 点击"扫一扫"                                                     │
│  3. 扫描上方二维码                                                   │
│  4. 确认支付 ¥{amount}                                                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════

📋 后续操作：

# 查看二维码图片
eog {qr_path}  # Linux
open {qr_path}  # Mac
start {qr_path}  # Windows

# 查询订单状态
python3 alipay_real_payment.py query {order_id}

═══════════════════════════════════════════════════════════════════════

✅ 收款二维码已生成，请扫码支付！
""")
    
    # 返回二维码路径
    return {
        "order_id": order_id,
        "amount": amount,
        "qr_path": qr_path,
        "pay_url": pay_url
    }

if __name__ == "__main__":
    result = main()
    print("\n订单数据（JSON 格式）：")
    print(json.dumps(result, ensure_ascii=False, indent=2))
