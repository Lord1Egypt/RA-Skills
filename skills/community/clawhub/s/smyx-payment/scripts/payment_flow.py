#!/usr/bin/env python3
"""兼容入口：转到支付流程。"""

try:
    from .payment_flow_with_status import create_order_and_show_payment_with_status
except ImportError:
    from scripts.payment_flow_with_status import create_order_and_show_payment_with_status


def create_order_and_show_payment(*args, **kwargs):
    """兼容旧函数名；实际行为：等待支付确认后查询订单状态。"""
    return create_order_and_show_payment_with_status(*args, **kwargs)


if __name__ == "__main__":
    create_order_and_show_payment()
