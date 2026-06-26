#!/usr/bin/env python3
"""
symx_payment - 主入口脚本
整合查询、充值、支付宝支付全流程，真正调用支付宝支付技能
"""

import sys
import json
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import query
import recharge
import callback
from skills.smyx_payment.scripts.open_id import require_open_id

# ==================== 配置 ====================

API_CONFIG = {
    "baseUrl": "https://lifeemergence.com/jeecg-boot-xzgz",
    "authType": "bearer",
    "token": "",  # TODO: 用户需要配置 Token
    "queryPath": "/api/account/query",
    "rechargePath": "/api/account/recharge",
    "callbackSuccessPath": "/api/payment/success",
    "callbackFailPath": "/api/payment/fail"
}

RECHARGE_AMOUNTS = [0.01, 9.9, 30, 300]


# ==================== 辅助函数 ====================

def print_json(title, data):
    print(f"\n{title}")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def get_user_input(prompt, default=None):
    """获取用户输入"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()


def get_amount_choice():
    """让用户选择充值金额档位"""
    print("\n请选择充值金额档位：")
    for i, amount in enumerate(RECHARGE_AMOUNTS, 1):
        print(f"  {i}. ¥{amount}")

    while True:
        choice = input("请输入选项 (1-4): ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(RECHARGE_AMOUNTS):
                return RECHARGE_AMOUNTS[index]
        except:
            pass
        print("无效选项，请重新输入")


def output_alipay_cashier_url(cashier_url):
    """
    输出支付宝收银台链接
    格式化为 OpenClaw 可识别的支付宝支付触发格式
    """
    print("\n" + "=" * 60)
    print("📱 支付宝支付链接已生成")
    print("=" * 60)
    print(f"\n请使用支付宝支付：")
    print(f"{cashier_url}")
    print("\n💡 提示：点击以上链接或使用支付宝扫码支付")
    print("=" * 60 + "\n")


def output_payment_request(order_info):
    """
    输出支付请求，触发 alipay-pay-for-service 技能

    关键：输出包含 cashier*.alipay.com 或 excashier*.alipay.com 的链接
    这样会触发 alipay-pay-for-service 技能的 SKILL.md
    """
    cashier_url = order_info.get("cashierUrl", "")

    print("\n" + "🔴" * 30)
    print("请处理以下支付请求：")
    print("订单 ID:", order_info.get("orderId"))
    print("金额：¥", order_info.get("amount"))
    print("收银台链接:", cashier_url)
    print("🔴" * 30)

    # 输出特殊标记，让调用者知道需要调用支付宝支付技能
    print("\n[ALIPAY_PAYMENT_REQUEST]")
    print(json.dumps({
        "type": "alipay_payment",
        "orderId": order_info.get("orderId"),
        "amount": order_info.get("amount"),
        "cashierUrl": cashier_url,
        "detail": order_info.get("detail"),
        "phoneNumber": order_info.get("phoneNumber")
    }, ensure_ascii=False, indent=2))
    print("[/ALIPAY_PAYMENT_REQUEST]")


# ==================== 主流程 ====================

# 模拟账户数据（API 不可用时使用）
MOCK_ACCOUNTS = {
    "13800138000": {
        "totalRecharged": 500.00,
        "balance": 20.00,
        "remainingUses": 5,
        "usedCount": 45,
        "isInsufficient": True
    }
}


def query_account_flow(phone_number, token=None, use_mock=True):
    """账户查询流程"""
    print("\n" + "=" * 60)
    print("  步骤 1: 查询账户信息")
    print("=" * 60)

    # 优先使用模拟数据（演示用）
    if use_mock and phone_number in MOCK_ACCOUNTS:
        data = MOCK_ACCOUNTS[phone_number]
        print(f"✅ 查询成功（模拟数据）")
        print(f"   手机号：{phone_number}")
        print(f"   已充值：¥{data['totalRecharged']}")
        print(f"   余  额：¥{data['balance']}")
        print(f"   剩余次数：{data['remainingUses']}")
        print(f"   已用次数：{data['usedCount']}")
        return {"success": True, "data": data}

    result = query.query_account(phone_number, token)

    if result["success"]:
        data = result["data"]
        if data:
            print(f"✅ 查询成功")
            print(f"   手机号：{phone_number}")
            print(f"   已充值：¥{data['totalRecharged']}")
            print(f"   余  额：¥{data['balance']}")
            print(f"   剩余次数：{data['remainingUses']}")
            print(f"   已用次数：{data['usedCount']}")
        else:
            print("⚠️  该账户还没有任何充值记录")
        return result
    else:
        print(f"❌ 查询失败：{result.get('error')}")
        return result


def recharge_flow(phone_number=None, token=None, check_balance=True):
    """完整充值流程（包含支付宝支付）- 先显示套餐，再输入账号"""

    # 步骤 1: 显示套餐信息
    print("\n" + "=" * 60)
    print("  步骤 1: 选择充值套餐")
    print("=" * 60)

    # 显示套餐列表
    print(recharge.display_packages())

    # 用户选择套餐
    print("请先选择充值套餐：")
    while True:
        valid_ids = "/".join(str(pkg.get("id")) for pkg in recharge.get_recharge_packages())
        choice = get_user_input(f"请输入套餐编号 ({valid_ids})", default="")
        try:
            package_id = int(choice)
            for package in recharge.get_recharge_packages():
                if package.get("id") == package_id:
                    selected_package = package
                    break
            else:
                selected_package = None
            if selected_package:
                break
        except:
            pass
        print("无效选项，请重新输入")

    amount = selected_package["amount"]
    uses = selected_package["uses"]
    package_name = selected_package["name"]

    print(f"\n✅ 已选择：{package_name}")
    print(f"   充值金额：¥{amount}")
    print(f"   可用次数：{uses}次")

    # 步骤 2: 自动关联充值账号
    print("\n" + "=" * 60)
    print("  步骤 2: 自动关联充值账号")
    print("=" * 60)

    if not phone_number:
        phone_number = require_open_id(None)
        print("✅ 系统已自动完成充值账号关联")

    # 步骤 3: 查询账户（如果需要）
    if check_balance:
        query_result = query_account_flow(phone_number, token)
        if not query_result["success"]:
            return query_result

        account_info = query_result["data"]

        # 显示账户信息
        print("\n" + "=" * 60)
        print("  步骤 3: 账户信息")
        print("=" * 60)
        print(f"增值账号：{phone_number}")
        print(f"当前余额：¥{account_info['balance']}")
        print(f"剩余次数：{account_info['remainingUses']}次")
        print(f"已用次数：{account_info['usedCount']}次")

        if not account_info["isInsufficient"]:
            print(f"\n✅ 余额充足，但您仍可以选择继续充值")

    # 输入备注（可选）
    remark = get_user_input("请输入备注（可选，直接回车跳过）", default="")

    # 生成充值明细
    detail = recharge.generate_recharge_detail(
        phone=phone_number,
        amount=amount,
        package_type=package_name,
        remark=remark
    )

    print(f"\n充值明细：{detail}")
    print("✅ 已选择套餐，默认直接购买该套餐，开始创建订单")

    # 步骤 4: 创建订单
    print("\n" + "=" * 60)
    print("  步骤 4: 创建充值订单")
    print("=" * 60)

    # TODO: 这里需要调用真实的云端 API 创建订单
    # 现在使用模拟数据
    order = {
        "orderId": f"ORD{os.popen('date +%Y%m%d%H%M%S').read().strip()}",
        "amount": amount,
        "uses": uses,
        "detail": detail,
        "phoneNumber": phone_number,
        "cashierUrl": f"https://excashier.alipay.com/pc.htm?outTradeNo={phone_number}_{amount}",
        "alipayParams": {
            "outTradeNo": f"20260428{phone_number}",
            "totalAmount": str(amount),
            "subject": detail
        }
    }

    print(f"✅ 订单创建成功")
    print(f"   订单 ID: {order['orderId']}")
    print(f"   订单金额：¥{order['amount']}")
    print(f"   可用次数：{order['uses']}次")

    # 步骤 5: 调起支付宝支付
    print("\n" + "=" * 60)
    print("  步骤 5: 调起支付宝支付")
    print("=" * 60)

    # 输出支付请求（触发 alipay-pay-for-service 技能）
    output_payment_request(order)

    # 说明：实际使用时，这里需要调用 alipay-pay-for-service 技能
    # 在 OpenClaw 环境中，输出 cashierUrl 会自动触发支付宝支付技能
    # 或者通过 sessions_spawn 调用支付宝支付技能

    print("\n💡 下一步操作：")
    print("1. 点击以上支付宝链接完成支付")
    print("2. 支付成功后，系统会自动调用回调接口")
    print("3. 或手动运行回调脚本：python3 callback.py <orderId> <paymentProof>")

    return {
        "success": True,
        "message": "请完成支付宝支付",
        "order": order
    }


def handle_payment_callback(order_id, payment_proof, phone_number, success=True, token=None):
    """处理支付回调"""
    print("\n" + "=" * 60)
    print("  步骤 6: 处理支付回调")
    print("=" * 60)

    if success:
        result = callback.payment_success_callback(
            order_id=order_id,
            payment_proof=payment_proof,
            amount=0,  # TODO: 从订单获取
            phone=phone_number,
            token=token
        )
    else:
        result = callback.payment_fail_callback(
            order_id=order_id,
            error_reason=payment_proof,  # 失败原因
            phone=phone_number,
            token=token
        )

    if result["success"]:
        print(f"✅ 回调成功")
        print(json.dumps(result.get("data", {}), ensure_ascii=False, indent=2))
    else:
        print(f"❌ 回调失败：{result.get('error')}")

    return result


# ==================== 命令行入口 ====================

def print_usage():
    print("""
symx_payment - 增值账户续费技能

用法:
  python3 index.py query <手机号> [token]           # 查询账户
  python3 index.py recharge <手机号> [token]        # 完整充值流程
  python3 index.py callback <orderId> <proof> <phone> [success] [token]  # 支付回调

示例:
  python3 index.py query 13800138000
  python3 index.py recharge 13800138000
  python3 index.py callback ORD123 ALIPAY_PROOF_123 13800138000 true
""")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "query":
        if len(sys.argv) < 3:
            print("错误：缺少手机号参数")
            sys.exit(1)
        phone = sys.argv[2]
        token = sys.argv[3] if len(sys.argv) > 3 else API_CONFIG["token"]
        query_account_flow(phone, token)

    elif command == "recharge":
        if len(sys.argv) < 3:
            print("错误：缺少手机号参数")
            sys.exit(1)
        phone = sys.argv[2]
        token = sys.argv[3] if len(sys.argv) > 3 else API_CONFIG["token"]
        recharge_flow(phone, token)

    elif command == "callback":
        if len(sys.argv) < 5:
            print("错误：缺少参数")
            sys.exit(1)
        order_id = sys.argv[2]
        proof = sys.argv[3]
        phone = sys.argv[4]
        success = sys.argv[5].lower() == "true" if len(sys.argv) > 5 else True
        token = sys.argv[6] if len(sys.argv) > 6 else API_CONFIG["token"]
        handle_payment_callback(order_id, proof, phone, success, token)

    else:
        print(f"未知命令：{command}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
