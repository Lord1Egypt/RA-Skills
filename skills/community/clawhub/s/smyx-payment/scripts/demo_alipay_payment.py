#!/usr/bin/env python3
"""
symx_payment - 支付宝支付流程演示（真正输出支付宝链接）
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import recharge

# 模拟账户数据
MOCK_ACCOUNT = {
    "phoneNumber": "13800138000",
    "totalRecharged": 500.00,
    "balance": 20.00,
    "remainingUses": 5,
    "usedCount": 45,
    "isInsufficient": True
}

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def main():
    print("\n\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "symx_payment 支付宝支付流程演示" + " " * 20 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # 步骤 1: 查询账户
    print_section("步骤 1: 查询账户信息")
    print(f"查询手机号：{MOCK_ACCOUNT['phoneNumber']}")
    print(f"✅ 查询成功（模拟数据）")
    print(f"   已充值金额：¥{MOCK_ACCOUNT['totalRecharged']:.2f}")
    print(f"   账户余额：¥{MOCK_ACCOUNT['balance']:.2f}")
    print(f"   剩余次数：{MOCK_ACCOUNT['remainingUses']}")
    print(f"   已用次数：{MOCK_ACCOUNT['usedCount']}")
    print(f"   余额不足：{'是 ⚠️' if MOCK_ACCOUNT['isInsufficient'] else '否 ✅'}")
    
    # 步骤 2: 检查余额
    print_section("步骤 2: 余额检查")
    if MOCK_ACCOUNT['isInsufficient']:
        print(f"⚠️  余额不足！当前余额：¥{MOCK_ACCOUNT['balance']:.2f}")
        print(f"💡 建议：立即充值")
    else:
        print(f"✅ 余额充足，无需充值")
        return
    
    # 步骤 3: 选择充值金额
    print_section("步骤 3: 选择充值金额")
    recharge_amounts = [10, 50, 100, 500]
    print("可选充值档位：")
    for i, amount in enumerate(recharge_amounts, 1):
        print(f"  {i}. ¥{amount}")
    
    # 默认选择 100 元
    selected_amount = 100
    print(f"\n✅ 已选择：¥{selected_amount}")
    
    # 步骤 4: 生成充值明细
    print_section("步骤 4: 生成充值明细")
    detail = recharge.generate_recharge_detail(
        phone=MOCK_ACCOUNT['phoneNumber'],
        amount=selected_amount,
        package_type="标准套餐",
        remark="演示充值"
    )
    print(f"充值明细：{detail}")
    
    # 步骤 5: 创建订单
    print_section("步骤 5: 创建充值订单")
    order_id = f"ORD{os.popen('date +%Y%m%d%H%M%S').read().strip()}"
    print(f"✅ 订单创建成功")
    print(f"   订单 ID: {order_id}")
    print(f"   订单金额：¥{selected_amount}")
    
    # 生成支付宝收银台链接
    cashier_url = f"https://excashier.alipay.com/pc.htm?outTradeNo=20260428{MOCK_ACCOUNT['phoneNumber']}&amount={selected_amount}"
    print(f"   收银台链接：{cashier_url}")
    
    # 步骤 6: 调起支付宝支付 ⭐ 关键步骤
    print_section("步骤 6: 🔴 调起支付宝支付")
    
    print(f"""
┌─────────────────────────────────────────────────────────────────────┐
│  📱 支付宝支付请求                                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  订单 ID:    {order_id}
│  支付金额：  ¥{selected_amount}
│  支付说明：  {detail}
│                                                                     │
│  请点击以下链接完成支付：
│  {cashier_url}
│                                                                     │
│  💡 提示：
│  • 如果是首次使用，系统会引导开通支付宝钱包
│  • 支付成功后自动回调云端接口
│  • 支付遇到问题请联系客服
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴

[ALIPAY_PAYMENT_REQUEST]
{json.dumps({
    "type": "alipay_payment",
    "orderId": order_id,
    "amount": selected_amount,
    "cashierUrl": cashier_url,
    "detail": detail,
    "phoneNumber": MOCK_ACCOUNT['phoneNumber'],
    "instruction": "请使用支付宝完成支付"
}, ensure_ascii=False, indent=2)}
[/ALIPAY_PAYMENT_REQUEST]

🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴

💡 在 OpenClaw 环境中：
   • 检测到 excashier.alipay.com 链接会自动触发 alipay-pay-for-service 技能
   • 支付宝支付技能会引导用户完成支付
   • 支付成功后自动调用回调接口

✅ 支付宝支付流程已调起！
""")
    
    # 步骤 7: 支付回调（演示）
    print_section("步骤 7: 支付回调（演示）")
    print(f"📞 调用支付成功回调：/api/payment/success")
    print(f"   订单 ID: {order_id}")
    print(f"   支付凭证：ALIPAY_PROOF_20260428123456")
    print(f"   充值金额：¥{selected_amount}")
    print(f"\n✅ 回调成功！账户数据已更新")
    print(f"   新增充值：¥{selected_amount}")
    print(f"   新增次数：1")
    print(f"   新余额：¥{MOCK_ACCOUNT['balance'] + selected_amount:.2f}")
    
    # 完成
    print_section("✅ 流程完成")
    print("""
流程总结:
  1. ✅ 账户查询
  2. ✅ 余额检查（余额不足）
  3. ✅ 选择充值金额（¥100）
  4. ✅ 生成充值明细
  5. ✅ 创建订单
  6. ✅ 调起支付宝支付 ⭐ 真正输出支付宝链接
  7. ✅ 支付回调（演示）

📁 相关文档:
  • references/alipay-integration-guide.md - 支付宝集成指南
  • scripts/index.py - 主入口脚本
  • scripts/alipay_integration.py - 支付宝集成模块
""")

if __name__ == "__main__":
    main()
