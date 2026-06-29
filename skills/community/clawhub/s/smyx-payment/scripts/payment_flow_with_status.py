#!/usr/bin/env python3
"""
完整支付流程。

流程：
1. 创建云端订单
2. 生成支付宝支付链接
3. 输出支付二维码 iframe
4. 提示用户完成支付
5. 提示用户如支付成功后，可输入「查询余额」了解账户详情
6. 结束当前支付生成流程，不自动查询订单状态或余额

privateKey 仅保存在当前 Python 进程内存中用于生成支付链接；禁止写入文件、环境变量或命令行参数。
"""

import sys
import os

sys.path.insert(0, ".")

from .platform_detection import get_current_platform, render_qrcode_markdown
from .recharge import create_recharge_order
from .pay_with_cloud_order import (
    create_payment_with_cloud_order,
    query_alipay_trade_status,
    extract_private_key_from_order,
)
from .api_key_config import (
    extract_api_key,
    persist_new_api_key_if_needed,
    print_api_key_stub_notice,
)
from .open_id import require_open_id, get_payment_card_display_account


def get_status_text(trade_status):
    """将支付宝状态码转换为中文描述。"""
    status_map = {
        "WAIT_BUYER_PAY": "⏳ 待支付 - 等待扫码付款",
        "TRADE_SUCCESS": "✅ 支付成功，订单已完成",
        "TRADE_FINISHED": "✅ 已完成 - 交易已完成且不可退款",
        "TRADE_CLOSED": "❌ 已关闭 - 支付超时或已取消",
        "": "🔍 暂未查询到明确支付状态",
        None: "🔍 暂未查询到明确支付状态",
    }
    return status_map.get(trade_status, f"❓ 未知状态 - {trade_status}")


def _print_payment_card(qrcode_content, h5_payment_url, order_no, amount, package_name, uses, account, pay_method="precreate"):
    # 生成二维码图片链接
    qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qrcode_content}"
    
    # 获取当前平台信息
    platform_info = get_current_platform()
    
    print("=" * 80)
    print("# 🦞 小龙虾主厨 · 套餐充值")
    print("=" * 80)
    print()
    print("## 📦 充值信息")
    print()
    print("| 项目 | 内容 |")
    print("|------|------|")
    print(f"| **套餐** | {package_name} |")
    print(f"| **金额** | ¥{amount} 元 |")
    print(f"| **次数** | {uses} 次 |")
    print(f"| **订单号** | {order_no} |")
    print(f"| **账户** | {account} |")
    print(f"| **支付方式** | {'支付宝当面付（直接扫码）' if pay_method == 'precreate' else '支付宝网页支付'} |")
    print(f"| **运行平台** | {platform_info['platform']} (置信度: {platform_info['confidence']:.0%}) |")
    print()
    print("## 📱 支付宝支付信息")
    print()
    print("### 🖼️ 支付二维码")
    print()
    print(render_qrcode_markdown(qr_image_url, "支付宝支付二维码", 300))
    print()
    print("### 🔗 支付方式")
    print()
    if pay_method == "precreate":
        print("💡 支付宝当面付（推荐）：")
        print(f"   使用支付宝 '扫一扫' 功能扫描以下二维码：")
        print(f"   支付链接：{qrcode_content}")
    else:
        print("💡 支付宝网页支付：")
        print(f"   复制以下链接到浏览器打开：")
        print(f"   {qrcode_content}")
    print()
    print("### 📲 备用方式")
    print()
    print("如需使用网页支付方式，请直接扫码支付或联系客服获取帮助。")
    print()
    print("-" * 80)
    print("✅ 支付信息已生成。")
    print("💬 请使用支付宝完成支付。")
    print("🔎 如支付成功后，可输入「查询余额」了解账户详情。")
    print("-" * 80)
    print()


def _query_status_and_balance(order_no, private_key_string, open_id):
    print("🔎 正在根据您的确认查询支付宝订单状态...")
    status_result = query_alipay_trade_status(order_no, private_key_string=private_key_string)
    trade_status = status_result.get("trade_status", "")
    status_text = get_status_text(trade_status)

    print()
    print("| 项目 | 内容 |")
    print("|------|------|")
    print(f"| **订单号** | {order_no} |")
    print(f"| **订单状态** | {status_text} |")
    if status_result.get("total_amount"):
        print(f"| **支付金额** | ¥{status_result.get('total_amount')} |")
    if status_result.get("send_pay_date"):
        print(f"| **支付时间** | {status_result.get('send_pay_date')} |")
    if status_result.get("trade_no"):
        print(f"| **支付宝交易号** | {status_result.get('trade_no')} |")
    print()

    if trade_status not in {"TRADE_SUCCESS", "TRADE_FINISHED"}:
        print("⚠️ 当前未验证到支付成功，暂不查询余额，也不会提示充值成功。")
        print("💡 如果您刚刚支付，可能存在支付宝同步延迟；如支付成功后，可输入「查询余额」了解账户详情。")
        return {
            "order_no": order_no,
            "status": "not_success",
            "trade_status": trade_status,
            "status_result": status_result,
        }

    print("🎉🎉🎉")
    print("✅ 支付成功！")
    print("🎉🎉🎉")
    print()
    print("📊 正在查询账户余额...")

    from .query import query_account

    balance_result = query_account(open_id)

    print()
    print("=" * 60)
    print("🦞 支付状态已验证成功，充值已入账！")
    print("=" * 60)
    print()
    print("| 项目 | 内容 |")
    print("|------|------|")
    print(f"| **账户** | {balance_result.get('phoneNumber', '')} |")
    print(f"| **总可用次数** | {balance_result.get('totalRecharged', 0)} 次 |")
    print(f"| **已使用次数** | {balance_result.get('usedCount', 0)} 次 |")
    print(f"| **剩余次数** | ✅ {balance_result.get('remainingUses', 0)} 次 |")
    print(f"| **余额不足** | {'是' if balance_result.get('isInsufficient', False) else '否'} |")
    print()
    print("=" * 60)
    print(f"✅ 当前剩余 {balance_result.get('remainingUses', 0)} 次，可以继续使用技能！")
    print("=" * 60)
    print()
    print("🦞 虾主厨祝您使用愉快！有任何问题随时找我～")

    return {
        "order_no": order_no,
        "status": "success",
        "trade_status": trade_status,
        "status_result": status_result,
        "balance": balance_result,
    }


def create_order_and_show_payment_with_status(
    amount: float = 0.01,
    package_name: str = "测试套餐",
    uses: int = 10,
    subject: str = "小龙虾主厨 - 测试套餐充值",
    phone: str = None,
    timeout_seconds: int = 0,
    poll_interval: int = 0,
):
    """
    生成支付信息并提示用户支付成功后可手动输入「查询余额」。
    """
    print()
    print("📦" * 15)
    print("📦 正在创建云端订单...")
    print("📦" * 15)

    result = create_recharge_order(
        phone=phone,
        amount=amount,
        package_type=package_name,
        detail=f"增值账户续费 - {package_name}",
    )
    if not isinstance(result, dict):
        raise RuntimeError(f"创建订单失败：{result}")

    order_no = result.get("orderNo")
    if not order_no:
        raise RuntimeError("创建订单失败：云端未返回 orderNo，已终止。")

    private_key_string = extract_private_key_from_order(result)
    api_key_info = persist_new_api_key_if_needed(extract_api_key(result))

    print("✅ 订单创建成功！")
    print(f"🔢 订单号: {order_no}")
    print(f"💰 金额: ¥{amount}")
    print(f"📦 套餐: {package_name}")
    print(f"🎯 次数: {uses} 次")
    print_api_key_stub_notice(api_key_info)
    print()

    print("🔗" * 15)
    print("🔗 正在生成支付宝支付链接...")
    print("🔗" * 15)

    open_id = require_open_id(phone)
    display_account = get_payment_card_display_account()
    pay_result = create_payment_with_cloud_order(
        cloud_order_no=order_no,
        phone=open_id,
        amount=amount,
        subject=subject,
        package_name=package_name,
        uses=uses,
        private_key_string=private_key_string,
    )
    payment_url = pay_result.get("pay_url")
    print("✅ 支付链接已生成！")
    print()

    pay_method = pay_result.get("method", "page_pay")
    
    # 二维码始终使用原生支付码（当面付成功时用 qr.alipay.com，降级时先生成H5链接作为二维码内容）
    qrcode_content = pay_result.get("qr_code", payment_url)
    # 备用方式始终使用 H5 网页支付链接（openapi.alipay.com 格式）
    h5_payment_url = payment_url
    
    _print_payment_card(qrcode_content, h5_payment_url, order_no, amount, package_name, uses, account=display_account, pay_method=pay_method)
    return {
        "order_no": order_no,
        "account": display_account,
        "qrcode_content": qrcode_content,
        "h5_payment_url": h5_payment_url,
        "method": pay_method,
        "status": "payment_page_created",
        "next_action": "支付成功后，可输入「查询余额」了解账户详情。",
    }


if __name__ == "__main__":
    amount = 0.01
    package_name = "测试套餐"
    uses = 10
    phone = None

    if len(sys.argv) >= 2:
        amount = float(sys.argv[1])
    if len(sys.argv) >= 3:
        package_name = sys.argv[2]
    if len(sys.argv) >= 4:
        uses = int(sys.argv[3])
    if len(sys.argv) >= 5:
        phone = sys.argv[4]

    create_order_and_show_payment_with_status(
        amount=amount,
        package_name=package_name,
        uses=uses,
        phone=phone,
    )
