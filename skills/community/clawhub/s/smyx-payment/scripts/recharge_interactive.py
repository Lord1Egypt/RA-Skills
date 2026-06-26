#!/usr/bin/env python3
"""
smyx_payment - 交互式充值流程（正式版本）
"""

import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recharge import get_recharge_packages, generate_recharge_detail
from alipay_pay import create_order
from datetime import datetime
from skills.smyx_payment.scripts.open_id import require_open_id

def get_user_input(prompt, default=""):
    """获取用户输入"""
    try:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            return user_input if user_input else default
        else:
            return input(f"{prompt}: ").strip()
    except EOFError:
        return default

def main():
    print("\n\n")
    print("╔" + "═" * 80 + "╗")
    print("║" + " " * 26 + "🔴 增值账户续费 - 充值套餐 🔴" + " " * 26 + "║")
    print("╚" + "═" * 80 + "╝")
    
    # ========== 步骤 1: 显示套餐信息 ==========
    print("\n" + "=" * 80)
    print("【步骤 1】请选择充值套餐")
    print("=" * 80)
    print("\n📋 系统提示：请先查看所有充值套餐")
    print()
    
    packages = get_recharge_packages()
    print("请选择充值套餐：\n")
    for pkg in packages:
        print(f"  {pkg.get('id')}. {pkg['name']}")
        print(f"     💰 充值金额：¥{pkg['amount']}元")
        print(f"     📊 可用次数：{pkg['uses']}次")
        if pkg.get('remark'):
            print(f"     💡 备注：{pkg['remark']}")
        print()
    
    # ========== 步骤 2: 用户选择套餐 ==========
    print("=" * 80)
    print("【步骤 2】用户选择充值套餐")
    print("=" * 80)
    print("\n⚠️  提示：必须先选择套餐，才能自动关联充值账号")
    
    while True:
        choice = get_user_input("\n请输入套餐编号 (0-3)")
        try:
            package_id = int(choice)
            selected_package = next((pkg for pkg in packages if pkg.get("id") == package_id), None)
            if selected_package:
                break
            print("❌ 无效选项，请输入 0-3")
        except ValueError:
            print("❌ 请输入数字 0-3")
    
    print(f"\n✅ 已选择套餐：{selected_package['name']}")
    print(f"   充值金额：¥{selected_package['amount']}元")
    print(f"   可用次数：{selected_package['uses']}次")
    
    # ========== 步骤 3: 自动关联充值账号 ==========
    print("\n" + "=" * 80)
    print("【步骤 3】自动关联充值账号")
    print("=" * 80)
    phone = require_open_id(None)
    print("✅ 系统已自动完成充值账号关联")
    print("✅ 已选择套餐，默认直接购买该套餐，开始创建订单")
    
    # ========== 步骤 4: 生成订单 ==========
    print("\n" + "=" * 80)
    print("【步骤 4】生成充值订单")
    print("=" * 80)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    cloud_order_id = f"CLOUD_{phone}_{timestamp}"
    detail = generate_recharge_detail(
        phone=phone,
        amount=selected_package['amount'],
        package_type=selected_package['name'],
        remark="正式测试"
    )
    
    print(f"\n正在创建订单...")
    result = create_order(phone, selected_package['amount'], detail, selected_package, cloud_order_id)
    
    if result['success']:
        print("\n✅ 订单生成成功！")
        print(f"   业务订单 ID: {cloud_order_id}")
        print(f"   支付宝订单号：{result['out_trade_no']}")
        print(f"   充值套餐：{selected_package['name']}")
        print(f"   充值金额：¥{selected_package['amount']}元")
        print(f"   可用次数：{selected_package['uses']}次")
        print(f"   充值账号：{phone}")
        
        # ========== 步骤 5: 生成支付二维码 ==========
        print("\n" + "=" * 80)
        print("【步骤 5】生成支付二维码")
        print("=" * 80)
        
        try:
            import qrcode
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(result['pay_url'])
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')
            qr_path = 'payment_qrcode_final.png'
            img.save(qr_path)
            
            print(f"\n✅ 支付二维码已生成：{qr_path}")
            print(f"   支付链接：{result['pay_url'][:80]}...")
        except Exception as e:
            print(f"\n⚠️  二维码生成失败：{e}")
            print(f"   支付链接：{result['pay_url']}")
        
        # ========== 流程总结 ==========
        print("\n" + "=" * 80)
        print("【流程总结】")
        print("=" * 80)
        print("\n✅ 完整充值流程完成！")
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
    success = main()
    if success:
        print("\n✅ 测试完成！")
    else:
        print("\n❌ 测试失败！")
