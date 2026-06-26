"""
SkillPay 支付集成模块
Agent Harness Skill - 付费验证
"""

import os
import sys
import json
import requests

# SkillPay API 配置
SKILLPAY_API_KEY = "sk_f03aa8f8bbcf79f7aa11c112d904780f22e62add1464e3c41a79600a451eb1d2"
SKILLPAY_BASE_URL = "https://api.skillpay.io/v1"
SKILL_SLUG = "shenmeng-agent-harness"
PRICE_PER_CALL = 0.01  # USDT


def require_payment():
    """
    验证支付状态
    
    在使用本 Skill 的功能前调用此函数验证用户已支付
    """
    try:
        headers = {
            "Authorization": f"Bearer {SKILLPAY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "skill_slug": SKILL_SLUG,
            "price": PRICE_PER_CALL
        }
        
        response = requests.post(
            f"{SKILLPAY_BASE_URL}/verify",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("verified"):
                return True
            else:
                balance = result.get("balance", 0)
                required = result.get("required", PRICE_PER_CALL)
                print(f"⚠️  余额不足: 当前 {balance} USDT, 需要 {required} USDT")
                print(f"💳 充值链接: {result.get('payment_url', '请访问 SkillPay 官网充值')}")
                return False
        else:
            print(f"⚠️  支付验证失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️  支付验证出错: {e}")
        # 错误时不阻止使用，记录日志即可
        return True


def get_balance():
    """获取当前账户余额"""
    try:
        headers = {
            "Authorization": f"Bearer {SKILLPAY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{SKILLPAY_BASE_URL}/balance",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("balance", 0)
        return 0
    except:
        return 0


if __name__ == "__main__":
    # 测试支付验证
    print(f"Skill: {SKILL_SLUG}")
    print(f"Price: {PRICE_PER_CALL} USDT per call")
    print(f"Balance: {get_balance()} USDT")
    print(f"Verified: {require_payment()}")
