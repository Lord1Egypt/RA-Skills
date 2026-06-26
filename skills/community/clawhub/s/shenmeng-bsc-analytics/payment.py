#!/usr/bin/env python3
"""
SkillPay 支付验证模块
BSC Analytics Skill - 付费验证
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

# SkillPay API 配置
SKILLPAY_API_URL = "https://api.skillpay.io/v1"
SKILLPAY_API_KEY = "sk_f03aa8f8bbcf79f7aa11c112d904780f22e62add1464e3c41a79600a451eb1d2"
SKILL_SLUG = "shenmeng-bsc-analytics"
PRICE = "0.01"  # USDT

def verify_payment(user_address: str = None) -> dict:
    """
    验证用户支付状态
    
    Args:
        user_address: 用户钱包地址 (可选)
        
    Returns:
        dict: 验证结果
    """
    try:
        headers = {
            "Authorization": f"Bearer {SKILLPAY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = json.dumps({
            "skill_slug": SKILL_SLUG,
            "user_address": user_address,
            "timestamp": datetime.utcnow().isoformat()
        }).encode('utf-8')
        
        req = urllib.request.Request(
            f"{SKILLPAY_API_URL}/verify",
            data=data,
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
            
    except urllib.error.HTTPError as e:
        return {
            "success": False,
            "error": f"API Error: {e.code}",
            "message": e.read().decode('utf-8')
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Payment verification failed"
        }

def require_payment(user_address: str = None):
    """
    要求支付 - 在 Skill 入口调用
    
    Args:
        user_address: 用户钱包地址
        
    Returns:
        bool: 是否已支付
    """
    # 检查环境变量是否跳过验证 (测试模式)
    if os.environ.get('SKILLPAY_SKIP_VERIFICATION') == 'true':
        print("⚠️  [DEV MODE] Payment verification skipped")
        return True
    
    result = verify_payment(user_address)
    
    if result.get('success') and result.get('verified'):
        print(f"✅ Payment verified for {SKILL_SLUG}")
        return True
    else:
        # 输出支付指引
        payment_url = f"https://pay.skillpay.io/{SKILL_SLUG}"
        print(f"""
💳  BSC Analytics 付费使用

价格: {PRICE} USDT / 次调用
链: BNB Chain

请完成支付后重试:
{payment_url}

或联系管理员获取访问权限。
        """)
        return False

def get_payment_info() -> dict:
    """获取支付信息"""
    return {
        "skill_name": "BSC Analytics",
        "slug": SKILL_SLUG,
        "price": f"{PRICE} USDT",
        "chain": "BNB Chain",
        "payment_url": f"https://pay.skillpay.io/{SKILL_SLUG}"
    }

# 如果直接运行此脚本，显示支付信息
if __name__ == '__main__':
    info = get_payment_info()
    print(json.dumps(info, indent=2, ensure_ascii=False))
