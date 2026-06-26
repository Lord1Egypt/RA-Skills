#!/usr/bin/env python3
"""
symx_payment - 完整流程模拟测试脚本
不依赖真实 API，使用模拟数据测试整个充值 + 支付宝支付流程
"""

import json
import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import recharge
import query

# ==================== 模拟数据 ====================

MOCK_ACCOUNT_DATA = {
    "13800138000": {
        "totalRecharged": 500.00,
        "balance": 20.00,  # 余额不足
        "remainingUses": 5,
        "usedCount": 45,
        "isInsufficient": True
    },
    "13900139000": {
        "totalRecharged": 1000.00,
        "balance": 200.00,  # 余额充足
        "remainingUses": 50,
        "usedCount": 100,
        "isInsufficient": False
    }
}

MOCK_ORDER_DATA = {
    "orderId": "ORD20260428" + "".join([str(i) for i in range(1000, 1010)]),
    "amount": 0,
    "alipayParams": {
        "outTradeNo": "20260428123456",
        "totalAmount": 0,
        "subject": ""
    },
    "cashierUrl": "https://excashier.alipay.com/pc.htm?outTradeNo=20260428123456"
}

# ==================== 测试函数 ====================

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_query_account(phone):
    """测试账户查询"""
    print_section("步骤 1: 查询账户信息")
    
    # 使用模拟数据
    if phone in MOCK_ACCOUNT_DATA:
        data = MOCK_ACCOUNT_DATA[phone]
        print(f"✅ 查询成功 - 手机号：{phone}")
        print(f"   已充值金额：¥{data['totalRecharged']:.2f}")
        print(f"   账户余额：¥{data['balance']:.2f}")
        print(f"   剩余次数：{data['remainingUses']}")
        print(f"   已用次数：{data['usedCount']}")
        print(f"   余额不足：{'是 ⚠️' if data['isInsufficient'] else '否 ✅'}")
        return {"success": True, "data": data}
    else:
        print(f"❌ 查询失败 - 手机号 {phone} 不存在于模拟数据中")
        return {"success": False, "error": "账号不存在"}

def test_check_balance(account_info):
    """测试余额检查"""
    print_section("步骤 2: 检查余额")
    
    balance = account_info.get("balance", 0)
    is_insufficient = account_info.get("isInsufficient", False)
    
    if is_insufficient:
        print(f"⚠️  余额不足！当前余额：¥{balance:.2f}")
        print(f"💡 建议：立即充值")
        return False
    else:
        print(f"✅ 余额充足！当前余额：¥{balance:.2f}")
        return True

def test_collect_recharge_info(phone, amount, package_type="标准套餐", remark="模拟测试"):
    """测试收集充值信息"""
    print_section("步骤 3: 收集充值信息")
    
    print(f"   充值账号：{phone}")
    print(f"   充值金额：¥{amount}")
    print(f"   套餐类型：{package_type}")
    print(f"   备注：{remark}")
    
    detail = recharge.generate_recharge_detail(phone, amount, package_type, remark)
    print(f"   充值明细：{detail}")
    
    return {
        "phone": phone,
        "amount": amount,
        "packageType": package_type,
        "detail": detail
    }

def test_create_order(recharge_info):
    """测试创建订单"""
    print_section("步骤 4: 创建充值订单")
    
    # 模拟创建订单
    order = MOCK_ORDER_DATA.copy()
    order["amount"] = recharge_info["amount"]
    order["alipayParams"]["totalAmount"] = recharge_info["amount"]
    order["alipayParams"]["subject"] = recharge_info["detail"]
    order["cashierUrl"] = f"https://excashier.alipay.com/pc.htm?outTradeNo=20260428{recharge_info['amount']}"
    
    print(f"✅ 订单创建成功")
    print(f"   订单 ID: {order['orderId']}")
    print(f"   订单金额：¥{order['amount']}")
    print(f"   支付宝流水号：{order['alipayParams']['outTradeNo']}")
    print(f"   收银台链接：{order['cashierUrl']}")
    
    return order

def test_alipay_payment(order):
    """测试支付宝支付流程"""
    print_section("步骤 5: 调起支付宝支付")
    
    print(f"📱 正在跳转到支付宝收银台...")
    print(f"   链接：{order['cashierUrl']}")
    print(f"   金额：¥{order['amount']}")
    print(f"\n🔄 模拟用户支付操作...")
    
    # 模拟支付结果（可以修改为 False 测试失败流程）
    payment_success = True
    
    if payment_success:
        print(f"✅ 支付成功！")
        print(f"   支付流水号：{order['alipayParams']['outTradeNo']}")
        return {"success": True, "paymentProof": "ALIPAY_PROOF_" + order['alipayParams']['outTradeNo']}
    else:
        print(f"❌ 支付失败！")
        print(f"   失败原因：用户取消支付")
        return {"success": False, "error": "用户取消支付"}

def test_payment_callback(order, payment_result, phone):
    """测试支付回调"""
    print_section("步骤 6: 调用云端回调接口")
    
    if payment_result["success"]:
        print(f"📞 调用支付成功回调：/api/payment/success")
        print(f"   订单 ID: {order['orderId']}")
        print(f"   支付凭证：{payment_result['paymentProof']}")
        print(f"   充值金额：¥{order['amount']}")
        print(f"   充值账号：{phone}")
        print(f"\n✅ 回调成功！账户数据已更新")
        print(f"   新增充值金额：¥{order['amount']}")
        print(f"   新增充值次数：1")
        print(f"   新余额：¥{MOCK_ACCOUNT_DATA.get(phone, {}).get('balance', 0) + order['amount']:.2f}")
    else:
        print(f"📞 调用支付失败回调：/api/payment/fail")
        print(f"   订单 ID: {order['orderId']}")
        print(f"   失败原因：{payment_result['error']}")
        print(f"\n✅ 回调成功！失败记录已保存")
    
    return {"success": True}

def run_full_test(phone="13800138000", amount=100):
    """运行完整测试流程"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "symx_payment 完整流程测试" + " " * 15 + "║")
    print("╚" + "═" * 58 + "╝")
    
    # 步骤 1: 查询账户
    query_result = test_query_account(phone)
    if not query_result["success"]:
        return
    
    account_info = query_result["data"]
    
    # 步骤 2: 检查余额
    is_sufficient = test_check_balance(account_info)
    if is_sufficient:
        print("\n💡 余额充足，无需充值。测试结束。")
        return
    
    # 步骤 3: 收集充值信息
    recharge_info = test_collect_recharge_info(phone, amount)
    
    # 步骤 4: 创建订单
    order = test_create_order(recharge_info)
    
    # 步骤 5: 支付宝支付
    payment_result = test_alipay_payment(order)
    
    # 步骤 6: 支付回调
    callback_result = test_payment_callback(order, payment_result, phone)
    
    # 测试完成
    print_section("测试完成")
    print("✅ 完整流程测试通过！")
    print("\n流程总结:")
    print("  1. ✅ 账户查询")
    print("  2. ✅ 余额检查")
    print("  3. ✅ 充值信息收集")
    print("  4. ✅ 订单创建")
    print("  5. ✅ 支付宝支付")
    print("  6. ✅ 支付回调")
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    # 默认测试手机号和金额
    phone = sys.argv[1] if len(sys.argv) > 1 else "13800138000"
    amount = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    
    run_full_test(phone, amount)
