#!/usr/bin/env python3
"""
直接调用 recharge.py 创建云端订单
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recharge import create_recharge_order

if __name__ == "__main__":
    # 测试参数
    phone = "13829295590"
    amount = 10
    package_name = "体验套餐"
    detail = f"增值账户续费 - {package_name}"
    package = {"amount": 10, "uses": 100, "name": "体验套餐"}
    
    print("=" * 80)
    print("🚀 直接调用 recharge.py 创建云端订单")
    print("=" * 80)
    print()
    
    # 调用 recharge.py 的 create_recharge_order 函数
    result = create_recharge_order(
        phone=phone,
        amount=amount,
        package_type=package_name,
        detail=detail,
        package=package
    )
    
    print()
    print("=" * 80)
    print("📋 执行结果")
    print("=" * 80)
    
    if result.get("success"):
        print("✅ 云端订单创建成功！")
        print()
        print(f"   云端订单 ID: {result['orderId']}")
        print(f"   云端订单号 (orderNo): {result['orderNo']}")
        print(f"   充值金额：¥{result['amount']}")
        print(f"   充值套餐：{result['package_name']}")
        print(f"   充值账号：{result['phone']}")
        print()
        print("=" * 80)
        print("✅ 可以继续使用 orderNo 生成支付宝支付链接")
        print("=" * 80)
    else:
        print("❌ 云端订单创建失败！")
        print()
        print(f"   错误信息：{result.get('error', '未知错误')}")
        print()
        print("=" * 80)
        print("🔴 流程已终止，无法继续")
        print("=" * 80)
