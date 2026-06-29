#!/usr/bin/env python3
"""
使用云端订单号创建支付宝 H5/网页支付链接。

安全规则：
- 禁止在本地硬编码支付宝 privateKey。
- 禁止把 privateKey 写入任何本地文件、配置、日志或用户可见输出。
- privateKey 必须来自 create_order 云端创单接口返回字段，并仅以内存参数传入本模块。
"""

import base64
import json
from datetime import datetime
from urllib import parse

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

ALIPAY_CONFIG = {
    "app_id": "2021006150611467",
    "gateway_url": "https://openapi.alipay.com/gateway.do",
    "notify_url": "https://lifeemergence.com/jeecg-boot-xzgz/health/order/alipay/on-notify",
    "return_url": "https://lifeemergence.com/payment-success.html",
    "sign_type": "RSA2",
    "charset": "utf-8",
}


def _require_runtime_private_key(private_key_string: str | None):
    """Load runtime-only Alipay private key; never persist or print it."""
    if not private_key_string or not str(private_key_string).strip():
        raise ValueError("缺少支付宝 privateKey：必须使用 create_order 接口返回字段，且禁止本地硬编码/落盘。")
    return RSA.import_key(str(private_key_string).strip())


def sign_data(data: str, private_key) -> str:
    """RSA2 签名。"""
    h = SHA256.new(data.encode("utf-8"))
    signer = PKCS1_v1_5.new(private_key)
    signature = signer.sign(h)
    return base64.b64encode(signature).decode("utf-8")


def _alipay_urlencode(params: dict) -> str:
    """支付宝参数编码：逐项 quote，确保空格为 %20，避免 urlencode 的 + 空格问题。"""
    return "&".join(f"{k}={parse.quote(str(v), safe='')}" for k, v in sorted(params.items()))


def extract_private_key_from_order(order_result: dict | None) -> str:
    """从 create_order 返回对象中提取 privateKey；不打印、不保存。"""
    if not isinstance(order_result, dict):
        raise ValueError("创单结果格式异常，无法读取 privateKey。")
    for key in ("privateKey", "private_key", "alipayPrivateKey", "alipay_private_key"):
        value = order_result.get(key)
        if value:
            return str(value)
    data = order_result.get("data")
    if isinstance(data, dict):
        for key in ("privateKey", "private_key", "alipayPrivateKey", "alipay_private_key"):
            value = data.get(key)
            if value:
                return str(value)
    raise ValueError("云端创单结果未返回 privateKey，无法生成支付宝 H5 支付链接。")


def sanitize_order_result(order_result):
    """返回脱敏副本，避免日志/用户输出泄露 privateKey。"""
    if isinstance(order_result, dict):
        cleaned = {}
        for k, v in order_result.items():
            if str(k).lower() in {"privatekey", "private_key", "alipayprivatekey", "alipay_private_key"}:
                cleaned[k] = "[REDACTED_RUNTIME_ONLY]"
            elif isinstance(v, dict):
                cleaned[k] = sanitize_order_result(v)
            else:
                cleaned[k] = v
        return cleaned
    return order_result


def create_payment_with_cloud_order(
    cloud_order_no: str,
    phone: str,
    amount: float,
    subject: str,
    package_name: str,
    uses: int,
    private_key_string: str | None = None,
):
    """
    创建支付宝「当面付」二维码（无需跳转H5，直接扫码支付）。

    使用 alipay.trade.precreate 接口，直接返回二维码链接 qr_code（格式：https://qr.alipay.com/xxx），
    用户扫码即可完成支付，无需跳转H5页面。

    Args:
        cloud_order_no: 云端订单号，必须来自 create_order/orderNo。
        phone: 用户账号或系统自动解析的内部身份值。
        amount: 支付金额。
        subject: 订单标题。
        package_name: 套餐名称。
        uses: 可用次数。
        private_key_string: create_order 返回的 privateKey，仅内存传递，禁止保存。
    """
    import requests

    private_key = _require_runtime_private_key(private_key_string)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out_trade_no = cloud_order_no

    # 使用当面付接口 alipay.trade.precreate
    # 注意：biz_content 不需要 nonce_str，这是支付宝官方要求
    biz_content = json.dumps(
        {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": str(amount),
        },
        separators=(",", ":"),
        ensure_ascii=False,
    )

    params = {
        "app_id": ALIPAY_CONFIG["app_id"],
        "method": "alipay.trade.precreate",
        "charset": ALIPAY_CONFIG["charset"],
        "sign_type": ALIPAY_CONFIG["sign_type"],
        "timestamp": timestamp,
        "version": "1.0",
        "biz_content": biz_content,
        "notify_url": ALIPAY_CONFIG["notify_url"],
    }

    # 支付宝签名规则：参数按ASCII排序后，用 key=value& 拼接，最后签名
    sorted_params = sorted(params.items())
    sign_string = "&".join([f"{k}={v}" for k, v in sorted_params])
    params["sign"] = sign_data(sign_string, private_key)

    # 调用支付宝当面付接口获取二维码链接
    try:
        # 注意：POST 请求时 charset 必须放在 query string 中，不能只在 body 里
        # 这是支付宝的特殊要求！
        url_with_charset = f"{ALIPAY_CONFIG['gateway_url']}?charset={ALIPAY_CONFIG['charset']}"
        response = requests.post(url_with_charset, data=params, timeout=10)
        result = response.json()
        response_key = "alipay_trade_precreate_response"
        
        if response_key in result and result[response_key].get("code") == "10000":
            qr_code = result[response_key].get("qr_code")
            print(f"✅ 支付宝当面付成功！原生支付码：{qr_code}")
            # 当面付成功时：同时生成 H5 链接作为备用方式
            h5_result = _create_h5_payment(
                cloud_order_no, phone, amount, subject, package_name, uses, private_key_string
            )
            return {
                "success": True,
                "qr_code": qr_code,          # 原生支付码：用于二维码
                "pay_url": h5_result["pay_url"],  # H5链接：用于备用方式
                "out_trade_no": out_trade_no,
                "amount": amount,
                "subject": subject,
                "phone": phone,
                "package_name": package_name,
                "uses": uses,
                "timestamp": timestamp,
                "method": "precreate",  # 标记为当面付模式
            }
        else:
            # 当面付失败时，降级回 H5 模式
            print(f"⚠️ 当面付接口调用失败，降级为 H5 模式：{result}")
            return _create_h5_payment(
                cloud_order_no, phone, amount, subject, package_name, uses, private_key_string
            )
    except Exception as e:
        # 异常时降级回 H5 模式
        print(f"⚠️ 当面付调用异常，降级为 H5 模式：{str(e)}")
        import traceback
        traceback.print_exc()
        return _create_h5_payment(
            cloud_order_no, phone, amount, subject, package_name, uses, private_key_string
        )


def _create_h5_payment(
    cloud_order_no: str,
    phone: str,
    amount: float,
    subject: str,
    package_name: str,
    uses: int,
    private_key_string: str | None = None,
):
    """
    创建支付宝 H5/网页支付链接（降级方案）。
    """
    import random
    import string

    private_key = _require_runtime_private_key(private_key_string)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out_trade_no = cloud_order_no
    nonce_str = "".join(random.choices(string.ascii_letters + string.digits, k=16))

    biz_content = json.dumps(
        {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": str(amount),
            "product_code": "FAST_INSTANT_TRADE_PAY",
            "qr_pay_mode": 4,
            "nonce_str": nonce_str,
        },
        separators=(",", ":"),
        ensure_ascii=False,
    )

    params = {
        "app_id": ALIPAY_CONFIG["app_id"],
        "method": "alipay.trade.page.pay",
        "charset": ALIPAY_CONFIG["charset"],
        "sign_type": ALIPAY_CONFIG["sign_type"],
        "timestamp": timestamp,
        "version": "1.0",
        "biz_content": biz_content,
        "notify_url": ALIPAY_CONFIG["notify_url"],
        "return_url": ALIPAY_CONFIG["return_url"],
    }

    sign_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    params["sign"] = sign_data(sign_string, private_key)
    pay_url = f"{ALIPAY_CONFIG['gateway_url']}?{_alipay_urlencode(params)}"

    return {
        "success": True,
        "pay_url": pay_url,
        "out_trade_no": out_trade_no,
        "amount": amount,
        "subject": subject,
        "phone": phone,
        "package_name": package_name,
        "uses": uses,
        "timestamp": timestamp,
        "method": "page_pay",  # 标记为 H5 模式
    }


def query_alipay_trade_status(out_trade_no: str, private_key_string: str | None = None):
    """查询支付宝订单状态；签名私钥必须由调用方以内存参数传入。"""
    private_key = _require_runtime_private_key(private_key_string)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    biz_content = json.dumps({"out_trade_no": out_trade_no}, separators=(",", ":"), ensure_ascii=False)
    params = {
        "app_id": ALIPAY_CONFIG["app_id"],
        "method": "alipay.trade.query",
        "charset": ALIPAY_CONFIG["charset"],
        "sign_type": ALIPAY_CONFIG["sign_type"],
        "timestamp": timestamp,
        "version": "1.0",
        "biz_content": biz_content,
    }

    sign_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    params["sign"] = sign_data(sign_string, private_key)

    import requests

    try:
        response = requests.get(ALIPAY_CONFIG["gateway_url"], params=params, timeout=10)
        result = response.json()
        response_key = "alipay_trade_query_response"
        if response_key in result:
            trade_data = result[response_key]
            return {
                "code": trade_data.get("code"),
                "msg": trade_data.get("msg"),
                "trade_status": trade_data.get("trade_status", ""),
                "total_amount": trade_data.get("total_amount", ""),
                "send_pay_date": trade_data.get("send_pay_date", ""),
                "trade_no": trade_data.get("trade_no", ""),
            }
        return {"code": "-1", "msg": "查询失败", "trade_status": ""}
    except Exception as e:
        return {"code": "-1", "msg": str(e), "trade_status": ""}


if __name__ == "__main__":
    raise SystemExit("禁止从命令行测试/传入/打印支付宝 privateKey；请通过 create_order 结果在内存中调用。")
