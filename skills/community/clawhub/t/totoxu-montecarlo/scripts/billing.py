#!/usr/bin/env python3
"""
SkillPay Billing Module (Official SDK)
1 USDT = 1000 tokens | 1 call = 1 token | Min 8 USDT

SECURITY MANIFEST:
- Only communicates with https://skillpay.me/api/v1/billing
- API key is a publisher-side charge-only key (cannot withdraw funds)
"""

import os
import sys
import json
import requests

BILLING_URL = "https://skillpay.me/api/v1/billing"
API_KEY = os.environ.get("SKILL_BILLING_API_KEY", "sk_91dc212149c7ee3184de119159a89a3a432455bfbfb1d87cf3f3db4b8764ab0c")
SKILL_ID = os.environ.get("SKILL_ID", "paythefly")
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}


def charge_user(user_id: str) -> dict:
    """Charge 1 token (= 0.001 USDT) per call."""
    try:
        resp = requests.post(f"{BILLING_URL}/charge", headers=HEADERS, json={
            "user_id": user_id, "skill_id": SKILL_ID, "amount": 0,
        }, timeout=10)
        data = resp.json()
        if data["success"]:
            return {"ok": True, "balance": data["balance"]}
        return {"ok": False, "balance": data["balance"], "payment_url": data.get("payment_url")}
    except Exception as e:
        return {"ok": False, "message": f"Billing error: {str(e)}"}


def get_balance(user_id: str) -> float:
    resp = requests.get(f"{BILLING_URL}/balance", params={"user_id": user_id}, headers=HEADERS, timeout=10)
    return resp.json()["balance"]


def get_payment_link(user_id: str, amount: float = 8) -> str:
    resp = requests.post(f"{BILLING_URL}/payment-link", headers=HEADERS, json={
        "user_id": user_id, "amount": amount,
    }, timeout=10)
    return resp.json()["payment_url"]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(charge_user(sys.argv[1]), indent=2))
    else:
        print("Usage: python billing.py <user_id>")
