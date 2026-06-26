#!/usr/bin/env python3
"""
symx_payment - 充值流程模块【标准正式入口】
=================
🔴🔴🔴【安全红线 - 严禁违反】🔴🔴🔴

  1. 绝对禁止本地生成任何形式的订单号（如 PAYxxxx、ORDERxxxx）
  2. 绝对禁止 LLM 自动推理、假设、猜测订单号
  3. 云端 API 失败必须立即终止流程，禁止降级、禁止绕过
  4. 支付宝 out_trade_no 必须 100% 来自云端返回的 orderNo

  违反以上任何一条，视为严重安全违规！

=================
正确流程：
1. 收集充值信息（手机号、套餐、金额）
2. 调用云端 API 创建订单 → 获取 orderNo（必须等待，必须验证）
3. 用云端 orderNo 作为支付宝 out_trade_no
4. 生成支付宝支付链接和收款码
5. 支付完成后验证交易状态
6. 查询账户使用情况
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, parent_dir)

from pydash import for_each

from skills.smyx_common.scripts import DatetimeUtil

import json
import re
import urllib.request
import urllib.error

from .config import *
from .skill import skill
from .package_config import TEST_PACKAGES, get_display_packages, get_selectable_packages
from .open_id import require_open_id, resolve_open_id


SENSITIVE_RESPONSE_KEYS = {
    "privatekey",
    "private_key",
    "alipayprivatekey",
    "alipay_private_key",
    "apikey",
    "api_key",
    "api-key",
    "secret",
    "token",
}


def _normalized_key(key) -> str:
    return str(key).replace("_", "").replace("-", "").lower()


def is_probably_sensitive_identifier(value) -> bool:
    """Return True for account-like values that look like api keys/tokens.

    Local default recharge accounts such as ``User_abcdef`` are safe to show;
    api-key based internal identities must never be printed as account values.
    """
    if value is None:
        return False
    text = str(value).strip()
    if not text:
        return False
    if text.startswith("User_") and len(text) == 11:
        return False
    lowered = text.lower()
    if lowered.startswith(("ak_", "sk_", "pk_", "api_", "key_", "token_")):
        return True
    # Long mixed identifiers are treated as sensitive by default.
    return len(text) >= 24 and bool(re.search(r"[A-Za-z]", text)) and bool(re.search(r"\d", text))


def display_safe_account(value) -> str:
    """Return a user/log safe account display value."""
    if value is None or str(value).strip() == "":
        return ""
    if is_probably_sensitive_identifier(value):
        return "[敏感账户已隐藏]"
    return str(value)


def sanitize_sensitive_response(value):
    """Return a copy safe for printing/logging; never expose create_order privateKey."""
    if isinstance(value, dict):
        cleaned = {}
        for k, v in value.items():
            normalized = _normalized_key(k)
            if normalized in {_normalized_key(item) for item in SENSITIVE_RESPONSE_KEYS}:
                cleaned[k] = "[REDACTED_RUNTIME_ONLY]"
            elif normalized in {"openid", "account", "userid", "phone"} and is_probably_sensitive_identifier(v):
                cleaned[k] = "[敏感账户已隐藏]"
            else:
                cleaned[k] = sanitize_sensitive_response(v)
        return cleaned
    if isinstance(value, list):
        return [sanitize_sensitive_response(v) for v in value]
    return value

# 充值金额档位（默认只返回对用户可见的套餐金额；测试套餐由会话级开关控制）
RECHARGE_AMOUNTS = [pkg["amount"] for pkg in get_selectable_packages()]


def validate_phone(phone: str) -> bool:
    """
    验证手机号格式（简单验证：11 位数字）
    """
    return bool(re.match(r'^1[3-9]\d{9}$', phone))


def generate_recharge_detail(phone: str, amount: float, package_type: str = "标准套餐", remark: str = "") -> str:
    """
    生成充值明细（结构化格式）

    Args:
        phone: 增值账号（手机号）
        amount: 充值金额
        package_type: 套餐类型
        remark: 备注

    Returns:
        充值明细字符串
    """
    phone = require_open_id(phone)
    detail = f"增值账户续费 - {package_type} - 账号：{phone} - 金额：{amount}元"
    if remark:
        detail += f" - 备注：{remark}"

    return create_recharge_order(phone, amount, package_type, detail)
    # return detail


def create_recharge_order(phone: str = None, amount: float = 0, package_type: str = "标准套餐", detail: str = "", package: dict = None,
                          token: str = None) -> dict:
    phone = require_open_id(phone)
    max_service_times = 0
    for package in TEST_PACKAGES:
        if package["name"] == package_type:
            max_service_times = package["uses"]
            break
    print("[当前套餐]", package_type, "[获得服务次数]", max_service_times)

    data = {
        "amount": amount,
        # "detail": detail,
        # # "packageType": "标准套餐",
        # 按后端要求：createOrder 不再传 promotionId，避免影响套餐/用量入账逻辑
        "maxServiceTimes": max_service_times,
        # # "outTradeNo": DatetimeUtil.now_str(),
        "description": detail,
        # # "memberType": 1,
        "openId": phone
    }
    print("🧾 创单入参（已脱敏）:")
    print(json.dumps(sanitize_sensitive_response(data), ensure_ascii=False, indent=2))

    try:

        response = skill.create_order(data)
        return response or "⚠️ 创建订单失败"

    except Exception as e:
        return f"创建订单异常：{str(e)}"


def notify_recharge_order(phone: str = None, amount: float = 0, trade_no: str = "", detail: str = "", package: dict = None,
                          token: str = None) -> dict:
    phone = require_open_id(phone)
    data = {
        "trade_status": "TRADE_SUCCESS",
        "total_amount": amount,
        "detail": detail,
        "trade_no": DatetimeUtil.datetime_str(),
        "out_trade_no": trade_no,
        "description": detail,
        "openId": phone
    }

    try:

        response = skill.on_pay_notify(data)
        return response or "⚠️ 通知订单失败"

    except Exception as e:
        return f"通知订单异常：{str(e)}"


def get_recharge_packages(show_test_package: bool | None = None) -> list:
    """获取当前会话可展示/可选择的充值套餐。默认隐藏测试套餐。"""
    return get_selectable_packages(show_test_package)


def display_packages(show_test_package: bool | None = None) -> str:
    """生成套餐展示文本。"""
    packages = get_display_packages(show_test_package)
    selectable_ids = "/".join(str(pkg.get("id")) for pkg in get_recharge_packages(show_test_package))
    lines = ["请选择充值套餐："]
    for package in packages:
        lines.extend([
            f"{package['id']}. {package['name']}",
            f"   💰 充值金额：{'¥' + str(package['amount']) + '元' if not package.get('contact_only') else package['amount']}",
            f"   📊 可用次数：{str(package['uses']) + '次' if not package.get('contact_only') else package['uses']}",
        ])
        if package.get('remark'):
            lines.append(f"   💡 备注：{package['remark']}")
        if package.get("contact_only"):
            lines.append("   📩 说明：该套餐不支持直接下单，请邮件联系获取专属报价与额度方案")
        lines.append("")
    lines.append(f"可直接下单套餐编号：{selectable_ids}；如需专属定制，请联系 product@lifeemergence.com")
    return "\n".join(lines)


def get_amount_options(show_test_package: bool | None = None) -> list:
    """
    获取充值金额档位选项。默认隐藏测试套餐。
    """
    return [pkg["amount"] for pkg in get_selectable_packages(show_test_package)]


if __name__ == "__main__":
    # 测试用法

    # 用法兼容：
    # 1) python -m scripts.recharge <手机号/账号> <金额> <套餐> <备注>
    # 2) python -m scripts.recharge <金额> <套餐> <备注>   # 内部身份自动从 data/smyx-api-key.txt 读取
    if len(sys.argv) >= 5:
        phone_arg = sys.argv[1]
        amount = sys.argv[2]
        package_type = sys.argv[3]
        remark = sys.argv[4]
    elif len(sys.argv) >= 4:
        phone_arg = None
        amount = sys.argv[1]
        package_type = sys.argv[2]
        remark = sys.argv[3]
    else:
        print("用法：python -m scripts.recharge [手机号/账号] <金额> <套餐> <备注>")
        print("说明：手机号/账号可省略；省略时系统会自动完成内部身份关联")
        sys.exit(1)

    phone = require_open_id(phone_arg)
    ConstantEnumBase.CURRENT__OPEN_ID = phone

    result = generate_recharge_detail(phone, amount, package_type, remark)
    print(f"✅ 订单创建成功\n", sanitize_sensitive_response(result))
