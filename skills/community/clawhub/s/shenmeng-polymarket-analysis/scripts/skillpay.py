#!/usr/bin/env python3
"""
SkillPay Billing Integration for Polymarket Analysis Skill
官网: https://skillpay.me

使用方法:
    python3 scripts/skillpay.py <user_id> [amount]

参数:
    user_id   - 用户的 SkillPay ID（首次运行可填 anonymous_user）
    amount    - 扣费金额（默认 0.001 USDT）
"""

import sys
import requests
import json
import os

# ─────────────────────────────────────────
#  ⚙️  配置区
# ─────────────────────────────────────────
BILLING_API_URL = "https://skillpay.me"
# API Key（已配置）
BILLING_API_KEY = "sk_f03aa8f8bbcf79f7aa11c112d904780f22e62add1464e3c41a79600a451eb1d2"
# SKILL_ID（已配置）
SKILL_ID = "dc2ff7e7-172c-4e78-a450-0522abb0cf31"
# ─────────────────────────────────────────

HEADERS = {
    "X-API-Key": BILLING_API_KEY,
    "Content-Type": "application/json",
}


def check_balance(user_id: str) -> dict:
    """检查用户余额"""
    try:
        r = requests.get(
            f"{BILLING_API_URL}/api/balance",
            headers=HEADERS,
            params={"user_id": user_id},
            timeout=10,
        )
        return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}


def charge_user(user_id: str, amount: float = 0.001) -> dict:
    """
    向用户扣费。
    成功返回 {"ok": true, "balance": ...}
    余额不足返回 {"ok": false, "payment_url": "https://skillpay.me/pay/..."}
    """
    try:
        payload = {
            "skill_id": SKILL_ID,
            "user_id": user_id,
            "amount": str(amount),
        }
        r = requests.post(
            f"{BILLING_API_URL}/api/charge",
            headers=HEADERS,
            json=payload,
            timeout=10,
        )
        return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_payment_link(user_id: str) -> str:
    """获取充值链接"""
    try:
        r = requests.get(
            f"{BILLING_API_URL}/api/pay",
            headers=HEADERS,
            params={"user_id": user_id, "skill_id": SKILL_ID},
            timeout=10,
        )
        data = r.json()
        return data.get("payment_url", f"{BILLING_API_URL}/pay?user_id={user_id}")
    except Exception:
        return f"{BILLING_API_URL}/pay?user_id={user_id}"


def billing_check(user_id: str, amount: float = 0.001) -> bool:
    """
    完整扣费流程：检查余额 → 扣费 → 处理结果
    返回 True 表示扣费成功，可以继续执行主逻辑
    返回 False 表示扣费失败（余额不足/网络错误）
    """
    if BILLING_API_KEY == "sk_your_api_key_here":
        print("[SkillPay] ⚠️  未配置 BILLING_API_KEY，跳过扣费（演示模式）")
        return True

    print(f"[SkillPay] 🔍 检查用户 {user_id} 余额...")
    balance_info = check_balance(user_id)
    if not balance_info.get("ok"):
        print(f"[SkillPay] ❌ 余额查询失败: {balance_info.get('error', 'unknown')}")
        # 网络等临时错误不阻挡执行
        return True

    print(f"[SkillPay] 💰 当前余额: {balance_info.get('balance', 'N/A')} USDT")

    print(f"[SkillPay] 💸 扣费 {amount} USDT...")
    result = charge_user(user_id, amount)

    if result.get("ok"):
        print(f"[SkillPay] ✅ 扣费成功，剩余余额: {result.get('balance', 'N/A')} USDT")
        return True
    else:
        payment_url = result.get("payment_url", get_payment_link(user_id))
        print(f"[SkillPay] ❌ 余额不足，请充值: {payment_url}")
        return False


if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else "anonymous_user"
    amount = float(sys.argv[2]) if len(sys.argv) > 2 else 0.001

    success = billing_check(user_id, amount)
    if success:
        print("[SkillPay] 可以继续执行主逻辑")
    else:
        print("[SkillPay] 扣费失败，退出")
        sys.exit(1)
