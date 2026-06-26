#!/usr/bin/env python3
"""
smyx_payment - 充值流程演示（模拟用户交互）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recharge import get_recharge_packages, generate_recharge_detail
from alipay_pay import create_order
import qrcode
from datetime import datetime
from skills.smyx_payment.scripts.open_id import require_open_id

def demo_recharge_flow():
    """演示完整充值流程"""
    
    print("\n\n")
    print("╔" + "═" * 80 + "╗")
    print("║" + " " * 24 + "smyx_payment 充值流程演示" + " " * 24 + "║")
    print("╚" + "═" * 80 + "╝")
    
    # ========== 步骤 1: 显示套餐信息 ==========
    print("\n" + "=" * 80)
    print("【步骤 1】显示所有充值套餐信息")
    print("=" * 80)
    print("\n📋 系统提示：请先查看所有充值套餐")
    print()
    
    packages = get_recharge_packages()
    print("请选择充值套餐：\n")
    for i, pkg in enumerate(packages, 1):
        print(f"  {i}. {pkg['name']}")
        print(f"     💰 充值金额：¥{pkg['amount']}元")
        print(f"     📊 可用次数：{pkg['uses']}次")
        if i == 1:
            unit_price = pkg['amount'] / pkg['uses'] * 10000
            print(f"     💡 性价比：{unit_price:.2f}元/万次")
        else:
            prev_pkg = packages[0]
            savings = (pkg['uses'] / pkg['amount'] - prev_pkg['uses'] / prev_pkg['amount']) / (prev_pkg['uses'] / prev_pkg['amount']) * 100
            print(f"     💡 性价比：节省{savings:.0f}%")
        print()
    
    # ========== 步骤 2: 用户选择套餐 ==========
    print("=" * 80)
    print("【步骤 2】用户选择充值套餐")
    print("=" * 80)
    print("\n👤 用户输入：3")
    print("\n✅ 已选择套餐：专业套餐")
    print("   充值金额：¥200 元")
    print("   可用次数：30000 次")
    selected_package = packages[2]
    
    # ========== 步骤 3: 自动关联充值账号 ==========
    print("\n" + "=" * 80)
    print("【步骤 3】自动关联充值账号")
    print("=" * 80)
    phone = require_open_id(None)
    print("✅ 系统已自动完成充值账号关联，无需用户输入账号信息")
    
    # ========== 步骤 5: 生成订单 ==========
    print("\n" + "=" * 80)
    print("【步骤 5】生成充值订单")
    print("=" * 80)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    cloud_order_id = f"CLOUD_{phone}_{timestamp}"
    detail = generate_recharge_detail(phone, selected_package['amount'], selected_package['name'], "流程演示")
    
    result = create_order(phone, selected_package['amount'], detail, selected_package, cloud_order_id)
    
    if result['success']:
        print("\n✅ 订单生成成功！")
        print(f"   业务订单 ID: {cloud_order_id}")
        print(f"   支付宝订单号：{result['out_trade_no']}")
        print(f"   充值套餐：{selected_package['name']}")
        print(f"   充值金额：¥{selected_package['amount']}元")
        print(f"   可用次数：{selected_package['uses']}次")
        print(f"   充值账号：{phone}")
        
        # ========== 步骤 6: 生成支付二维码 ==========
        print("\n" + "=" * 80)
        print("【步骤 6】生成支付二维码")
        print("=" * 80)
        
        # 生成二维码
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(result['pay_url'])
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        qr_path = 'demo_payment_qr.png'
        img.save(qr_path)
        
        print(f"\n✅ 支付二维码已生成：{qr_path}")
        print(f"   支付链接：{result['pay_url'][:80]}...")
        
        # ========== 流程总结 ==========
        print("\n" + "=" * 80)
        print("【流程总结】")
        print("=" * 80)
        print("\n✅ 完整充值流程演示完成！")
        print("\n流程步骤：")
        print("  1. ✅ 显示所有充值套餐信息")
        print("  2. ✅ 用户选择充值套餐")
        print("  3. ✅ 用户自动关联充值账号（含格式验证）")
        print("  4. ✅ 用户选择套餐后默认直接购买，无需二次确认")
        print("  5. ✅ 生成充值订单")
        print("  6. ✅ 生成支付二维码")
        
        print("\n📊 订单信息：")
        print("┌─────────────────────────────────────────────────┐")
        print(f"│  业务订单 ID:    {cloud_order_id}")
        print(f"│  支付宝订单号：  {result['out_trade_no']}")
        print(f"│  充值套餐：      {selected_package['name']}")
        print(f"│  充值金额：      ¥{selected_package['amount']}元")
        print(f"│  可用次数：      {selected_package['uses']}次")
        print(f"│  充值账号：      {phone}")
        print(f"│  订单状态：      ⏳ 待支付")
        print("└─────────────────────────────────────────────────┘")
        
        print("\n💡 下一步：")
        print("  • 扫描二维码完成支付")
        print("  • 支付成功后自动更新账户")
        
        return True
    else:
        print(f"\n❌ 订单生成失败：{result.get('error')}")
        return False

if __name__ == "__main__":
    success = demo_recharge_flow()
    if success:
        print("\n✅ 演示完成！")
        print("\n📁 生成的文件：")
        print("  • demo_payment_qr.png - 支付二维码")
    else:
        print("\n❌ 演示失败！")
