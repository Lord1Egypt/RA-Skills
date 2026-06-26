#!/usr/bin/env python3
"""
订单状态检查器 - 封装 check_order_status 方法

功能说明：
    check_order_status(order_no, wait_seconds=15) - 阻塞等待指定秒数后，查询订单状态
    默认为15秒，可以通过参数自定义等待时间
"""

import sys
import time
from datetime import datetime

sys.path.insert(0, '.')

from .pay_with_cloud_order import query_alipay_trade_status
from .query import query_account


def check_order_status(order_no, wait_seconds=15, print_progress=True, auto_query_balance=False, open_id=None, private_key_string=None):
    """
    ✅ 阻塞等待指定秒数后，查询订单状态
    
    参数说明：
        order_no (str): 订单号，必填
        wait_seconds (int): 阻塞等待的秒数，默认15秒
        print_progress (bool): 是否打印进度提示，默认True
        auto_query_balance (bool): 是否查询余额，默认False；当前主流程不自动查询余额
        open_id (str): 内部身份值，用于查询余额，默认None
    
    返回值：
        dict: 包含订单状态和相关信息
        {
            'order_no': 订单号,
            'wait_seconds': 实际等待秒数,
            'start_time': 开始等待时间,
            'end_time': 结束等待时间,
            'trade_status': 支付宝交易状态,
            'status_text': 中文状态描述,
            'alipay_code': 支付宝返回码,
            'total_amount': 支付金额,
            'send_pay_date': 支付时间,
            'trade_no': 支付宝交易号,
            'balance_result': 账户余额信息（仅显式启用查询余额时）,
            'success': 是否支付成功
        }
    
    使用示例：
        # 默认等待15秒
        result = check_order_status('HY26061720240829425738')
        
        # 自定义等待30秒
        result = check_order_status('HY26061720240829425738', wait_seconds=30)
        
        # 不打印进度
        result = check_order_status('HY26061720240829425738', print_progress=False)
    """
    start_time = datetime.now()

    if print_progress:
        print("=" * 60)
        print(f"🔍 订单状态检查器 - 开始时间: {start_time.strftime('%H:%M:%S')}")
        print(f"⏳ 将阻塞等待 {wait_seconds} 秒后查询订单状态...")
        print("=" * 60)
        print()

    # 🔴 阻塞等待指定秒数
    time.sleep(wait_seconds)

    end_time = datetime.now()
    actual_wait = (end_time - start_time).total_seconds()

    if print_progress:
        print(f"✅ 等待完成！实际等待时间: {actual_wait:.1f} 秒")
        print(f"🕐 当前时间: {end_time.strftime('%H:%M:%S')}")
        print()
        print(f"📋 正在查询订单 {order_no} 的状态...")
        print()

    # 查询支付宝订单状态
    result = query_alipay_trade_status(order_no, private_key_string=private_key_string)
    trade_status = result.get('trade_status', '')
    alipay_code = result.get('code', '')

    # 状态映射
    status_map = {
        'WAIT_BUYER_PAY': '⏳ 待支付 - 等待用户扫码付款',
        'TRADE_SUCCESS': '✅ 已支付 - 支付成功，订单已完成',
        'TRADE_FINISHED': '✅ 已完成 - 交易已完成且不可退款',
        'TRADE_CLOSED': '❌ 已关闭 - 支付超时或已取消',
        '': '🔍 查询中 - 订单尚未创建或暂未查询到状态',
        None: '🔍 查询中 - 订单尚未创建或暂未查询到状态'
    }
    status_text = status_map.get(trade_status, f'❓ 未知状态 - {trade_status}')

    # 判断是否支付成功
    is_success = trade_status in ['TRADE_SUCCESS', 'TRADE_FINISHED']

    # 构建返回结果
    return_data = {
        'order_no': order_no,
        'wait_seconds': wait_seconds,
        'actual_wait_seconds': round(actual_wait, 1),
        'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'trade_status': trade_status,
        'status_text': status_text,
        'alipay_code': alipay_code,
        'total_amount': result.get('total_amount', ''),
        'send_pay_date': result.get('send_pay_date', ''),
        'trade_no': result.get('trade_no', ''),
        'success': is_success,
        'balance_result': None
    }

    if print_progress:
        # 检测到支付成功，先显示提示
        if is_success:
            print("🎉" * 10)
            print("✅ 检测到支付成功！")
            print("🎉" * 10)
            print()
            print("📢 支付成功。如需了解账户详情，可输入「查询余额」。")
            print()

        # 打印查询结果
        print("=" * 60)
        print("📋 订单状态查询结果")
        print("=" * 60)
        print(f"订单号: {order_no}")
        print(f"当前状态: {status_text}")
        print(f"支付宝状态码: {trade_status or '暂无'}")
        print(f"支付宝返回码: {alipay_code or '暂无'}")

        if result.get('total_amount'):
            print(f"支付金额: ¥{result.get('total_amount')} 元")
        if result.get('send_pay_date'):
            print(f"支付时间: {result.get('send_pay_date')}")
        if result.get('trade_no'):
            print(f"支付宝交易号: {result.get('trade_no')}")

        print("=" * 60)
        print()

        # 仅显式启用时查询余额；主支付流程不自动查询。
        if is_success and auto_query_balance and open_id:
            print("💰 正在查询账户余额...")
            print()

            balance_result = query_account(open_id)
            return_data['balance_result'] = balance_result

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
        elif is_success:
            print("✅ 支付成功！如需了解账户详情，可输入「查询余额」。")
        else:
            print(f"ℹ️  当前状态: {status_text}")
            print()
            print("📢 订单状态查询已结束")
            print("📢 如支付成功后，可输入「查询余额」了解账户详情。")
        print()

    return return_data


def check_order_status_simple(order_no, wait_seconds=15, private_key_string=None):
    """
    简化版：只返回状态文本，不打印任何信息
    """
    time.sleep(wait_seconds)
    result = query_alipay_trade_status(order_no, private_key_string=private_key_string)
    trade_status = result.get('trade_status', '')

    status_map = {
        'WAIT_BUYER_PAY': '待支付',
        'TRADE_SUCCESS': '已支付',
        'TRADE_FINISHED': '已完成',
        'TRADE_CLOSED': '已关闭'
    }

    return status_map.get(trade_status, '未知状态')


if __name__ == "__main__":
    """
    命令行使用示例：
    
    # 使用默认15秒等待
    python3 skills/smyx_payment/scripts/order_status_checker.py HY26061720240829425738
    
    # 自定义等待30秒
    python3 skills/smyx_payment/scripts/order_status_checker.py HY26061720240829425738 30
    
    # 如需账户详情，请在支付成功后手动查询余额
    python3 skills/smyx_payment/scripts/order_status_checker.py HY26061720240829425738 15
    """
    if len(sys.argv) < 2:
        print("使用方法:")
        print(f"  python3 {sys.argv[0]} <订单号> [等待秒数]")
        print()
        print("示例:")
        print(f"  python3 {sys.argv[0]} HY26061720240829425738")
        print(f"  python3 {sys.argv[0]} HY26061720240829425738 30")
        print(f"  python3 {sys.argv[0]} HY26061720240829425738 15")
        sys.exit(1)

    order_no = sys.argv[1]
    wait_seconds = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    open_id = sys.argv[3] if len(sys.argv) > 3 else None

    # 调用检查方法
    result = check_order_status(
        order_no=order_no,
        wait_seconds=wait_seconds,
        print_progress=True,
        auto_query_balance=True,
        open_id=open_id
    )

    # 打印返回的完整数据（用于调试）
    # print("完整返回数据:", result)
