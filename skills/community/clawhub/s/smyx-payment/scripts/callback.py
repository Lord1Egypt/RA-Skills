#!/usr/bin/env python3
"""
symx_payment - 支付回调模块
处理支付成功/失败回调，回写云端接口
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, parent_dir)

import json
import urllib.request
import urllib.error

from skills.smyx_common.scripts import DatetimeUtil
from .config import ApiEnum, ConstantEnum
from .config import *
from .skill import skill

# API 配置
API_CONFIG = {
    "baseUrl": "https://lifeemergence.com/jeecg-boot-xzgz",
    "callbackSuccessPath": "/health/order/alipay/on-notify",
    "callbackFailPath": "/health/order/alipay/on-notify",
    "authType": "bearer",
    "token": ""
}


def payment_success_callback(order_id: str, amount: float, token: str = None) -> dict:
    """
    支付成功回调
    
    Args:
        order_id: 订单 ID
        payment_proof: 支付凭证（支付宝返回）
        amount: 充值金额
        phone: 增值账号
        token: Bearer Token
    
    Returns:
        回调结果
    """
    token = token or API_CONFIG.get("token", "")

    url = f"{API_CONFIG['baseUrl']}{API_CONFIG['callbackSuccessPath']}"

    headers = {
        "Content-Type": "application/json"
    }

    if API_CONFIG["authType"] == "bearer" and token:
        headers["Authorization"] = f"Bearer {token}"

    trade_no = DatetimeUtil.format_timestamp()
    # out_trade_no = "11111"
    data = {
        # "orderId": order_id,
        "out_trade_no": order_id,
        "trade_no": trade_no,
        "subject": "支付宝支付回调成功:" + order_id,
        "total_amount": amount,
        "trade_status": "TRADE_SUCCESS"
    }

    try:

        response = skill.on_pay_notify(data)

        # return response
        return response or f"支付成功回调失败"

        # req = urllib.request.Request(
        #     url,
        #     data=json.dumps(data).encode('utf-8'),
        #     headers=headers,
        #     method='POST'
        # )
        #
        # with urllib.request.urlopen(req, timeout=30) as response:
        #     result = json.loads(response.read().decode('utf-8'))
        #
        #     return {
        #         "success": True,
        #         "data": {
        #             "message": "支付成功回调完成",
        #             "rechargedAmount": result.get("rechargedAmount", amount),
        #             "rechargedCount": result.get("rechargedCount", 1),
        #             "newBalance": result.get("newBalance", 0)
        #         }
        #     }

    except Exception as e:
        return f"支付成功回调异常：{str(e)}"
        # return {
        #     "success": False,
        #     "error": f"支付成功回调失败：{str(e)}"
        # }


def payment_fail_callback(order_id: str, error_reason: str, phone: str, token: str = None) -> dict:
    """
    支付失败回调
    
    Args:
        order_id: 订单 ID
        error_reason: 失败原因
        phone: 增值账号
        token: Bearer Token
    
    Returns:
        回调结果
    """
    token = token or API_CONFIG.get("token", "")

    url = f"{API_CONFIG['baseUrl']}{API_CONFIG['callbackFailPath']}"

    headers = {
        "Content-Type": "application/json"
    }

    if API_CONFIG["authType"] == "bearer" and token:
        headers["Authorization"] = f"Bearer {token}"

    data = {
        "orderId": order_id,
        "errorReason": error_reason,
        "phoneNumber": phone,
        "status": "FAILED"
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))

            return {
                "success": True,
                "data": {
                    "message": "支付失败回调完成",
                    "orderId": order_id
                }
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"支付失败回调失败：{str(e)}"
        }


if __name__ == "__main__":
    # 测试用法
    # print("支付回调模块 - 测试")
    if len(sys.argv) < 4:
        print("用法：python callback.py <手机号> <订单号> <金额>")
        sys.exit(1)

    phone = sys.argv[1]
    order_id = sys.argv[2]
    amount = sys.argv[3]

    ConstantEnumBase.CURRENT__OPEN_ID = phone

    result = payment_success_callback(order_id, amount)
    print(result)
    # 实际使用时需要传入真实参数
