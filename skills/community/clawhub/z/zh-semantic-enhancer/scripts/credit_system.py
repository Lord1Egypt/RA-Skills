#!/usr/bin/env python3
"""
API积分系统 / API Credit System
"""

import json
import os
from datetime import datetime
from pathlib import Path

class CreditSystem:
    """积分管理系统"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.credit_file = Path(f"~/.openclaw/zh_semantic_credits/{user_id}.json").expanduser()
        self.credit_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()
    
    def _load(self) -> dict:
        if self.credit_file.exists():
            with open(self.credit_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "credits": 100,  # 默认100积分
            "used": 0,
            "purchases": [],
            "created_at": datetime.now().isoformat()
        }
    
    def _save(self):
        with open(self.credit_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_balance(self) -> int:
        return self.data["credits"] - self.data["used"]
    
    def use_credit(self, amount: int = 1) -> bool:
        if self.get_balance() >= amount:
            self.data["used"] += amount
            self._save()
            return True
        return False
    
    def add_credits(self, amount: int, payment_method: str = ""):
        self.data["credits"] += amount
        self.data["purchases"].append({
            "amount": amount,
            "date": datetime.now().isoformat(),
            "method": payment_method
        })
        self._save()
    
    def get_usage_stats(self) -> dict:
        return {
            "total_credits": self.data["credits"],
            "used_credits": self.data["used"],
            "remaining": self.get_balance(),
            "purchase_count": len(self.data["purchases"])
        }

# 积分定价
CREDIT_PACKAGES = {
    "starter": {"credits": 500, "price": 0.5, "bonus": 0},
    "popular": {"credits": 2000, "price": 1.5, "bonus": 200},
    "pro": {"credits": 10000, "price": 5.0, "bonus": 1500},
    "enterprise": {"credits": 50000, "price": 20.0, "bonus": 10000}
}
