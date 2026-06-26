#!/usr/bin/env python3
"""
symx_payment - 支付宝支付集成模块
真正调用 alipay-pay-for-service 技能处理支付
"""

import json
import sys
import os
import urllib.request
import urllib.error

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import recharge


def create_recharge_order(phone: str, amount: float, package_type, detail: str) -> dict:
    return recharge.create_recharge_order(phone, amount, package_type, detail)


def trigger_alipay_payment(cashier_url: str, amount: float, detail: str) -> str:
    """
    触发支付宝支付
    
    在 OpenClaw 环境中，输出包含 cashier*.alipay.com 的链接会自动触发 alipay-pay-for-service 技能
    
    Args:
        cashier_url: 支付宝收银台链接
        amount: 支付金额
        detail: 支付说明
    
    Returns:
        支付引导文本
    """
    output = f"""

{'=' * 60}
📱 支付宝支付请求
{'=' * 60}

订单金额：¥{amount}
支付说明：{detail}

请点击以下链接完成支付：
{cashier_url}

或者在支付宝中扫码支付。

💡 提示：
- 如果是首次使用支付宝支付，系统会引导你开通钱包
- 支付成功后，系统会自动处理回调
- 支付遇到问题，请运行：python3 callback.py <orderId> <paymentProof> <phone>

{'=' * 60}

[ALIPAY_PAYMENT_TRIGGER]
{{
  "type": "alipay_payment_request",
  "cashierUrl": "{cashier_url}",
  "amount": {amount},
  "detail": "{detail}",
  "instruction": "请使用支付宝完成支付"
}}
[/ALIPAY_PAYMENT_TRIGGER]
"""
    return output


def process_payment_result(order_id: str, payment_success: bool, payment_proof: str, phone: str,
                           api_config: dict) -> dict:
    """
    处理支付结果（调用回调接口）
    
    Args:
        order_id: 订单 ID
        payment_success: 是否支付成功
        payment_proof: 支付凭证或失败原因
        phone: 手机号
        api_config: API 配置
    
    Returns:
        回调结果
    """
    # 这里需要导入 callback 模块
    # 由于循环导入问题，我们直接实现回调逻辑

    url_path = api_config['callbackSuccessPath'] if payment_success else api_config['callbackFailPath']
    url = f"{api_config['baseUrl']}{url_path}"

    headers = {
        "Content-Type": "application/json"
    }

    if api_config.get("authType") == "bearer" and api_config.get("token"):
        headers["Authorization"] = f"Bearer {api_config['token']}"

    if payment_success:
        data = {
            "orderId": order_id,
            "paymentProof": payment_proof,
            "phoneNumber": phone,
            "status": "SUCCESS"
        }
    else:
        data = {
            "orderId": order_id,
            "errorReason": payment_proof,
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
                "data": result
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"回调失败：{e}"
        }


if __name__ == "__main__":
    # 测试用法
    print("支付宝支付集成模块 - 测试")

    # 测试生成支付链接
    detail = recharge.generate_recharge_detail("13800138000", 100, "标准套餐", "测试")
    cashier_url = "https://excashier.alipay.com/pc.htm?outTradeNo=2026042813800138000"

    print(trigger_alipay_payment(cashier_url, 100, detail))
