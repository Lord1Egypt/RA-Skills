#!/usr/bin/env python3
"""
SkillPay Billing SDK - Python
1 USDT = 1000 tokens | 1 call = 1 token | Min deposit 8 USDT
"""

import os
import requests
import json

BILLING_URL = "https://skillpay.me/api/v1/billing"
API_KEY = "sk_72df482063c0d454184ac7677a9f1094638da3e9f9b51530c9ffab92d0427011"
SKILL_ID = "quant-orchestrator"

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def charge_user(user_id: str) -> dict:
    """Charge user for skill usage"""
    try:
        response = requests.post(
            f"{BILLING_URL}/charge",
            json={
                "user_id": user_id,
                "skill_id": SKILL_ID,
                "amount": 1  # 1 token
            },
            headers=HEADERS,
            timeout=10
        )
        data = response.json()
        
        if data.get("success"):
            return {"ok": True, "balance": data.get("balance")}
        else:
            return {
                "ok": False, 
                "balance": data.get("balance"),
                "payment_url": data.get("payment_url")
            }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def get_balance(user_id: str) -> float:
    """Get user balance"""
    try:
        response = requests.get(
            f"{BILLING_URL}/balance",
            params={"user_id": user_id},
            headers=HEADERS,
            timeout=10
        )
        return response.json().get("balance", 0)
    except:
        return 0

def get_payment_link(user_id: str, amount: float = 10) -> str:
    """Get payment link for user"""
    try:
        response = requests.post(
            f"{BILLING_URL}/payment-link",
            json={
                "user_id": user_id,
                "amount": amount
            },
            headers=HEADERS,
            timeout=10
        )
        return response.json().get("payment_url", "")
    except:
        return ""

def check_and_charge(user_id: str) -> dict:
    """Check balance and charge if sufficient"""
    charge_result = charge_user(user_id)
    
    if charge_result.get("ok"):
        return {
            "success": True,
            "message": "Skill executed successfully",
            "balance": charge_result["balance"]
        }
    else:
        payment_url = charge_result.get("payment_url", get_payment_link(user_id))
        return {
            "success": False,
            "message": "Insufficient balance. Please deposit.",
            "payment_url": payment_url,
            "balance": charge_result.get("balance", 0)
        }

# CLI test
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
    else:
        user_id = "test_user"
    
    print(f"Testing billing for user: {user_id}")
    result = check_and_charge(user_id)
    print(json.dumps(result, indent=2))
