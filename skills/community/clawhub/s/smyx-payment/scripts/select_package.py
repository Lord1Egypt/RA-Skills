#!/usr/bin/env python3
"""
smyx_payment - 充值套餐选择
显示可选套餐，用户选择后生成支付订单
"""

import sys
import os
import json
from datetime import datetime
from skills.smyx_payment.scripts.open_id import require_open_id

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, workspace_dir)

try:
    # 优先使用相对导入（包模块方式）
    from .recharge import generate_recharge_detail
    from .package_config import get_display_packages, get_selectable_packages
except ImportError:
    # 兼容直接脚本执行
    from skills.smyx_payment.scripts.recharge import generate_recharge_detail
    from skills.smyx_payment.scripts.package_config import get_display_packages, get_selectable_packages

def display_packages():
    """显示充值套餐列表"""
    print("\n")
    print("╔" + "═" * 60 + "╗")
    print("║" + " " * 22 + "充值套餐选择" + " " * 22 + "║")
    print("╚" + "═" * 60 + "╝")
    print("\n请选择充值套餐：\n")
    
    for pkg in get_display_packages():
        print(f"  {pkg['id']}. {pkg['name']}")
        if pkg.get("contact_only"):
            print(f"     💰 充值金额：{pkg['amount']}")
            print(f"     📊 可用次数：{pkg['uses']}")
            print(f"     📩 说明：{pkg['remark']}")
            print("     ⚠️ 该套餐不支持直接下单，请邮件联系获取专属报价与额度方案")
        else:
            print(f"     💰 充值金额：¥{pkg['amount']}元")
            print(f"     📊 可用次数：{pkg['uses']}次")
            if pkg.get('remark'):
                print(f"     💡 备注：{pkg['remark']}")
        print()

def select_package():
    """用户选择套餐"""
    while True:
        packages = get_selectable_packages()
        valid_ids = "/".join(str(pkg.get('id')) for pkg in packages)
        choice = input(f"请输入套餐编号 ({valid_ids}): ").strip()
        try:
            package_id = int(choice)
            for package in packages:
                if package.get('id') == package_id:
                    return package
        except Exception:
            pass
        print("无效选项，请重新输入")

def create_order(phone, package, remark="", cloud_order_id=None):
    """创建充值订单（包含套餐信息和云端订单 ID）"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    out_trade_no = f"ORDER_{phone}_{timestamp}"
    
    detail = generate_recharge_detail(
        phone=phone,
        amount=package["amount"],
        package_type=package["name"],
        remark=remark
    )
    
    order = {
        "orderId": out_trade_no,  # 商户订单号
        "out_trade_no": out_trade_no,  # 支付宝商户订单号
        "amount": package["amount"],
        "uses": package["uses"],
        "package_name": package["name"],
        "phone": phone,
        "detail": detail,
        "package": {  # 套餐详细信息（传递给云端接口）
            "amount": package["amount"],
            "uses": package["uses"],
            "name": package["name"]
        },
        "cloud_order_id": cloud_order_id  # 云端订单 ID（用于绑定）
    }
    
    return order

def main():
    print("\n\n")
    print("╔" + "═" * 80 + "╗")
    print("║" + " " * 26 + "🔴 增值账户续费 - 充值套餐 🔴" + " " * 26 + "║")
    print("╚" + "═" * 80 + "╝")
    
    # 步骤 1: 显示套餐信息
    print("\n【步骤 1】请选择充值套餐")
    print("=" * 80)
    display_packages()
    
    # 选择套餐
    print("\n请先选择充值套餐，然后自动关联充值账号")
    package = select_package()
    
    print(f"\n✅ 已选择套餐：{package['name']}")
    print(f"   充值金额：¥{package['amount']}元")
    print(f"   可用次数：{package['uses']}次")
    
    # 步骤 2: 自动关联充值账号
    print("\n【步骤 2】自动关联充值账号")
    print("=" * 80)
    phone = require_open_id(None)
    print("✅ 系统已自动完成充值账号关联")
    print("✅ 已选择套餐，默认直接购买该套餐，开始创建订单")
    
    # 创建订单
    order = create_order(phone, package)
    
    print("\n" + "=" * 70)
    print("  订单信息")
    print("=" * 70)
    print(f"  订单 ID:    {order['orderId']}")
    print(f"  充值金额：  ¥{order['amount']}元")
    print(f"  可用次数：  {order['uses']}次")
    print(f"  充值明细：  {order['detail']}")
    print("=" * 70)
    
    print("\n✅ 订单创建成功！")
    print("\n下一步：调用支付宝支付接口...")
    
    # 返回订单信息
    return order

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        # 仅显示套餐列表
        display_packages()
    else:
        # 完整流程
        main()
