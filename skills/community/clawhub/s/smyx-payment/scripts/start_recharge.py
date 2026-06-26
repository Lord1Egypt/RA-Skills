#!/usr/bin/env python3
"""
🚀 一键启动充值流程

使用方法：
    python3 -m skills.smyx_payment.scripts.start_recharge <套餐编号>

套餐编号：
    0 = 测试套餐 (¥0.01, 10次)
    1 = 体验套餐 (¥9.9, 500次)
    2 = 标准套餐 (¥30, 1200次)
    3 = 专业套餐 (¥300, 15000次)

功能特点：
    ✅ 创建云端订单
    ✅ 生成支付宝支付二维码 iframe
    ✅ 提示用户支付成功后可输入「查询余额」查看账户详情
    ✅ 支付页生成后结束，不自动查询订单状态或余额
"""

import sys
import os

# 添加工作区路径
current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, workspace_dir)

from .package_config import get_selectable_packages
from .payment_flow_with_status import create_order_and_show_payment_with_status


def get_package_by_id(package_id):
    """根据套餐ID获取套餐信息"""
    packages = get_selectable_packages()
    for pkg in packages:
        if pkg.get("id") == package_id:
            return pkg
    return None


def main():
    if len(sys.argv) < 2:
        print("=" * 80)
        print("🚀 smyx_payment 一键充值")
        print("=" * 80)
        print()
        print("使用方法：")
        print(f"    python {sys.argv[0]} <套餐编号>")
        print()
        print("可选套餐：")
        packages = get_selectable_packages()
        for pkg in packages:
            print(f"    {pkg['id']} = {pkg['name']} (¥{pkg['amount']}, {pkg['uses']}次)")
        print()
        print("示例：")
        print(f"    python {sys.argv[0]} 0  # 选择测试套餐")
        print(f"    python {sys.argv[0]} 1  # 选择体验套餐")
        print()
        print("=" * 80)
        return 1

    try:
        package_id = int(sys.argv[1])
    except ValueError:
        print(f"❌ 无效的套餐编号：{sys.argv[1]}")
        return 1

    package = get_package_by_id(package_id)
    if not package:
        print(f"❌ 未找到编号为 {package_id} 的套餐")
        return 1

    print()
    print("🦞" * 20)
    print("🦞 小龙虾主厨 · 欢迎使用充值流程！")
    print("🦞" * 20)
    print()
    print(f"✅ 已选择套餐: {package['name']}")
    print(f"✅ 充值金额: ¥{package['amount']}")
    print(f"✅ 可用次数: {package['uses']} 次")
    print()
    print("📋 支付流程：")
    print("   1. 生成支付宝支付页面")
    print("   2. 您完成扫码支付")
    print("   3. 如支付成功后，可输入「查询余额」了解账户详情")
    print("   4. 当前流程只生成支付页面，不自动查询订单状态或余额")
    print()

    create_order_and_show_payment_with_status(
        amount=package["amount"],
        package_name=package["name"],
        uses=package["uses"],
        phone=None,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
