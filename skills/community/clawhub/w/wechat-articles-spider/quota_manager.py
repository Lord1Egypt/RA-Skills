#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User Quota Manager
用户额度管理系统 - 管理免费额度、包月订阅、使用记录
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

from config import FREE_TIER, PRICING


DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "users")
os.makedirs(DATA_DIR, exist_ok=True)


@dataclass
class FreeQuota:
    """免费额度"""
    total: int = 10
    used: int = 0
    
    @property
    def remaining(self) -> int:
        return max(0, self.total - self.used)


@dataclass
class Subscription:
    """包月订阅"""
    active: bool = False
    started_at: Optional[str] = None
    expires_at: Optional[str] = None
    tx_hash: Optional[str] = None
    
    def is_valid(self) -> bool:
        if not self.active:
            return False
        if not self.expires_at:
            return False
        expires = datetime.fromisoformat(self.expires_at)
        return datetime.now() < expires


@dataclass
class UsageRecord:
    """使用记录"""
    time: str
    action: str
    resource: str
    count: int
    cost: float
    paid_by: str  # 'free' | 'subscription' | 'x402'
    tx_hash: Optional[str] = None


class UserQuotaManager:
    """用户额度管理器"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id.lower()
        self.user_file = os.path.join(DATA_DIR, f"{self.user_id}.json")
        self.data = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """加载用户数据"""
        if os.path.exists(self.user_file):
            with open(self.user_file, 'r') as f:
                return json.load(f)
        
        # 新用户初始化
        return {
            "user_id": self.user_id,
            "created_at": datetime.now().isoformat(),
            "free_quota": asdict(FreeQuota()),
            "subscription": asdict(Subscription()),
            "usage_history": [],
        }
    
    def _save(self) -> None:
        """保存用户数据"""
        with open(self.user_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
    
    # ============ 免费额度 ============
    
    def get_free_quota(self) -> FreeQuota:
        """获取免费额度"""
        return FreeQuota(**self.data.get("free_quota", {}))
    
    def use_free_quota(self, count: int) -> bool:
        """
        使用免费额度
        返回: 是否成功
        """
        quota = self.get_free_quota()
        
        if quota.remaining < count:
            return False
        
        self.data["free_quota"]["used"] += count
        self._save()
        return True
    
    # ============ 包月订阅 ============
    
    def get_subscription(self) -> Subscription:
        """获取订阅状态"""
        return Subscription(**self.data.get("subscription", {}))
    
    def subscribe(self, tx_hash: str) -> bool:
        """
        开通包月
        返回: 是否成功
        """
        now = datetime.now()
        expires = now + timedelta(days=30)
        
        self.data["subscription"] = {
            "active": True,
            "started_at": now.isoformat(),
            "expires_at": expires.isoformat(),
            "tx_hash": tx_hash,
        }
        self._save()
        return True
    
    def check_subscription(self) -> bool:
        """检查订阅是否有效"""
        sub = self.get_subscription()
        
        if not sub.is_valid():
            # 过期自动关闭
            if sub.active:
                self.data["subscription"]["active"] = False
                self._save()
            return False
        
        return True
    
    # ============ 使用记录 ============
    
    def add_usage(
        self,
        action: str,
        resource: str,
        count: int,
        cost: float,
        paid_by: str,
        tx_hash: Optional[str] = None
    ) -> None:
        """添加使用记录"""
        record = {
            "time": datetime.now().isoformat(),
            "action": action,
            "resource": resource,
            "count": count,
            "cost": cost,
            "paid_by": paid_by,
            "tx_hash": tx_hash,
        }
        
        self.data.setdefault("usage_history", []).append(record)
        self._save()
    
    def get_usage_history(self, limit: int = 10) -> List[Dict]:
        """获取使用历史"""
        history = self.data.get("usage_history", [])
        return history[-limit:][::-1]  # 最近 limit 条，倒序
    
    # ============ 状态查询 ============
    
    def get_status(self) -> Dict[str, Any]:
        """获取用户完整状态"""
        quota = self.get_free_quota()
        sub = self.get_subscription()
        
        return {
            "user_id": self.user_id,
            "free": {
                "total": quota.total,
                "used": quota.used,
                "remaining": quota.remaining,
            },
            "subscription": {
                "active": sub.active and sub.is_valid(),
                "expires_at": sub.expires_at,
            },
            "total_usage": len(self.data.get("usage_history", [])),
        }
    
    # ============ 计费决策 ============
    
    def can_execute(
        self, 
        mode: str, 
        count: int = 1
    ) -> tuple[bool, float, str]:
        """
        检查是否可以执行，返回 (能否执行, 费用, 支付方式)
        
        优先级:
        1. 免费额度
        2. 包月订阅
        3. x402 支付
        """
        # 计算费用
        if mode == "per_article":
            cost = PRICING["per_article"] * count
        elif mode == "per_account":
            cost = PRICING["per_account"]
        elif mode == "monthly":
            cost = PRICING["monthly"]
        else:
            return False, 0, "unknown"
        
        # 1. 检查免费额度
        quota = self.get_free_quota()
        if quota.remaining >= count:
            return True, 0, "free"
        
        # 2. 检查包月订阅
        if self.check_subscription():
            return True, 0, "subscription"
        
        # 3. 需要 x402 支付
        return True, cost, "x402"


if __name__ == "__main__":
    # 测试
    manager = UserQuotaManager("0xTestUser123")
    
    print("=== 初始状态 ===")
    print(json.dumps(manager.get_status(), indent=2))
    
    print("\n=== 检查能否爬5篇文章 ===")
    can_exec, cost, method = manager.can_execute("per_article", 5)
    print(f"能否执行: {can_exec}, 费用: ${cost}, 方式: {method}")
    
    if can_exec and method == "free":
        manager.use_free_quota(5)
        manager.add_usage("crawl", "articles", 5, 0, "free")
        print("已使用免费额度5篇")
    
    print("\n=== 更新后状态 ===")
    print(json.dumps(manager.get_status(), indent=2))
