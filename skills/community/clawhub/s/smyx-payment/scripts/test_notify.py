#!/usr/bin/env python3
"""
直接调用 recharge.py 创建云端订单
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .recharge import notify_recharge_order

if __name__ == "__main__":
    # 测试参数
    phone = "13829295590"
    amount = 0.01
    trade_no = "HY26043015320751568234"
    # package_name = "体验套餐"
    detail = f"增值账户续费"
    # package = {"amount": 10, "uses": 100, "name": "体验套餐"}
    #
    # print("=" * 80)
    # print("🚀 直接调用 recharge.py 创建云端订单")
    # print("=" * 80)
    # print()

    # 调用 recharge.py 的 create_recharge_order 函数
    result = notify_recharge_order(
        phone=phone,
        amount=amount,
        trade_no=trade_no,
        # package_type=package_name,
        detail=detail
        # package=package
    )

    print()
    print("=" * 80)
    print("📋 执行结果", result)
    print("=" * 80)
