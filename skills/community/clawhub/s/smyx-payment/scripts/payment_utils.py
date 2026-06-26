#!/usr/bin/env python3
"""
支付工具库。

支付页生成后，只提示用户支付成功后可输入「查询余额」查看账户详情。

保留 create_order/show_payment_info 作为展示工具。
"""
import sys
import os
import json
import time
import subprocess
from pathlib import Path

PAYMENT_RESULT_FILE = "/tmp/payment_success.json"


def create_order(
        amount: float = 0.01,
        package_name: str = "测试套餐",
        uses: int = 10,
        subject: str = "小龙虾主厨 - 测试套餐充值",
        phone: str = "13822542262"
):
    """
    创建订单
    """
    sys.path.insert(0, '.')
    from scripts.recharge import create_recharge_order
    from scripts.pay_with_cloud_order import create_payment_with_cloud_order, extract_private_key_from_order

    # 1. 创建云端订单
    result = create_recharge_order(
        phone=None,
        amount=amount,
        package_type=package_name,
        detail=f"增值账户续费 - {package_name}"
    )
    order_no = result.get('orderNo')
    private_key_string = extract_private_key_from_order(result)

    # 2. 生成支付链接
    pay_result = create_payment_with_cloud_order(
        cloud_order_no=order_no,
        phone=phone,
        amount=amount,
        subject=subject,
        package_name=package_name,
        uses=uses,
        private_key_string=private_key_string
    )
    payment_url = pay_result.get('pay_url')

    return {
        "order_no": order_no,
        "payment_url": payment_url,
        "amount": amount,
        "package_name": package_name,
        "uses": uses,
        # 仅供当前 Python 对象内存传递；调用 show_payment_info / 用户输出前必须避免打印该字段。
        "_runtime_private_key": private_key_string,
        "open_id": phone,
    }


def start_background_detection(
        order_no: str,
        timeout_seconds: int = 60,
        interval_seconds: int = 3,
        private_key_string: str | None = None,
        result_file: str = PAYMENT_RESULT_FILE,
        open_id: str | None = None,
):
    """该入口不用于当前支付流程。"""
    raise RuntimeError("当前支付流程不自动查单或查余额；如支付成功后，可输入『查询余额』了解账户详情。")


def check_payment_result(show_result: bool = True):
    """
    检查支付结果（主会话调用）
    如果有支付成功结果，显示完整信息
    返回 True=有结果，False=无结果
    """
    if not os.path.exists(PAYMENT_RESULT_FILE):
        return False

    try:
        with open(PAYMENT_RESULT_FILE, 'r') as f:
            result = json.load(f)

        # 清理文件
        os.remove(PAYMENT_RESULT_FILE)

        if show_result:
            print('🎉' * 10)
            print(f"✅ 检测到支付成功！")
            print(f"✅ 订单号：{result.get('order_no', '')}")
            print(f"✅ 支付金额：{result.get('total_amount', '0.00')} 元")
            print(f"✅ 支付时间：{result.get('send_pay_date', '未知')}")
            print('🎉' * 10)
            print()

            # 查询余额
            print("📊 正在查询账户余额...")
            balance_str = subprocess.getoutput(
                'cd /root/.openclaw/workspace/skills/smyx_payment && python3 -m scripts.query'
            )
            import ast
            balance = ast.literal_eval(balance_str)
            print()
            print('=' * 60)
            print('🦞 支付状态已验证成功，充值已入账！')
            print('=' * 60)
            print()
            print('| 项目 | 内容 |')
            print('|---|---:|')
            print(f'| **账户** | {balance.get("phoneNumber", "")} |')
            print(f'| **总可用次数** | {balance.get("totalRecharged", 0)} 次 |')
            print(f'| **已使用次数** | {balance.get("usedCount", 0)} 次 |')
            print(f'| **剩余次数/余额** | ✅ {balance.get("remainingUses", 0)} 次 |')
            print(f'| **是否余额不足** | {"是" if balance.get("isInsufficient", False) else "否"} |')
            print()
            print('=' * 60)

        return True

    except Exception as e:
        print(f"⚠️  读取支付结果失败: {e}")
        return False


def show_payment_info(order_info: dict, timeout_seconds: int = 60):
    """
    显示支付信息（Markdown格式）
    """
    # 绝不打印 order_info 中的 _runtime_private_key。
    print('# 🦞 小龙虾主厨 · 套餐充值')
    print()
    print('---')
    print()
    print('## 📦 充值信息')
    print()
    print('| 项目 | 内容 |')
    print('|------|------|')
    print(f'| **套餐** | {order_info["package_name"]} |')
    print(f'| **金额** | ¥{order_info["amount"]} 元 |')
    print(f'| **次数** | {order_info["uses"]} 次 |')
    print(f'| **订单号** | {order_info["order_no"]} |')
    print()
    print('## 📱 支付宝扫码支付')
    print()
    print('<iframe ')
    print(f'  src=\"{order_info["payment_url"]}\" ')
    print('  width=\"300\" ')
    print('  height=\"300\" ')
    print('  frameborder=\"0\"')
    print('  scrolling=\"no\"')
    print(
        '  style=\"border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); overflow: hidden; display: block; margin: 0 auto;\"')
    print('>')
    print('</iframe>')
    print()
    print('💡 备用方式：如 iframe 显示不完整，点击下面链接直接打开支付页面')
    print(f'[👉 点击打开支付宝付款页面]({order_info["payment_url"]})')
    print()
    print('---')
    print()
    print('💬 请完成扫码支付；如支付成功后，可输入「查询余额」了解账户详情。')
    print()


if __name__ == "__main__":
    # 快速测试
    info = create_order()
    show_payment_info(info, 10)
    print("✅ 支付页已生成；如支付成功后，可输入『查询余额』了解账户详情。")
