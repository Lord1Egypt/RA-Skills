"""
ValU AI 智能估值分析器 - 核心模块
用户配额管理与计费系统
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path

# ====================== 定价配置 ======================
PRICING = {
    "free": {
        "name": "免费版",
        "quota_per_week": 2,
        "batch_size": 0,  # 免费版不支持批量
        "price": 0
    },
    "pay_per_use": {
        "name": "专业版（按次）",
        "price_per_time": 9.9,
        "batch_size": 1
    },
    "packages": {
        "starter": {
            "name": "尝鲜包",
            "times": 10,
            "original_price": 99,
            "discount_price": 79,
            "unit_price": 7.9
        },
        "pro": {
            "name": "进阶包",
            "times": 30,
            "original_price": 297,
            "discount_price": 199,
            "unit_price": 6.6
        },
        "enterprise": {
            "name": "专业包",
            "times": 50,
            "original_price": 495,
            "discount_price": 299,
            "unit_price": 5.98
        }
    },
    "batch_analysis": {
        "name": "批量分析",
        "price": 29.9,
        "max_stocks": 5,
        "description": "最多5只股票横向对比分析"
    }
}

# 用户数据存储路径
USER_DATA_DIR = Path(__file__).parent.parent / "user_data"
USER_DB_PATH = USER_DATA_DIR / "users.json"

# ====================== 用户配额管理类 ======================
class UserQuotaManager:
    """用户配额管理器"""

    def __init__(self):
        self.user_db = self._load_user_db()

    def _load_user_db(self) -> Dict[str, Any]:
        """加载用户数据库"""
        USER_DATA_DIR.mkdir(exist_ok=True)
        if USER_DB_PATH.exists():
            with open(USER_DB_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_user_db(self):
        """保存用户数据库"""
        with open(USER_DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.user_db, f, ensure_ascii=False, indent=2)

    def _get_week_key(self) -> str:
        """获取当前周的唯一标识"""
        today = datetime.now()
        # ISO周码
        week_num = today.isocalendar()[1]
        return f"{today.year}-W{week_num:02d}"

    def _init_user(self, user_id: str) -> Dict[str, Any]:
        """初始化新用户"""
        if user_id not in self.user_db:
            self.user_db[user_id] = {
                "created_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat(),
                "free_quota": {
                    "used_this_week": 0,
                    "week_key": self._get_week_key()
                },
                "credits": 0,  # 剩余次数
                "packages": {},  # 已购套餐
                "usage_history": []
            }
        return self.user_db[user_id]

    def _reset_weekly_quota_if_needed(self, user: Dict[str, Any]):
        """检查并重置周配额"""
        current_week = self._get_week_key()
        if user["free_quota"]["week_key"] != current_week:
            user["free_quota"]["used_this_week"] = 0
            user["free_quota"]["week_key"] = current_week

    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """获取用户信息"""
        user = self._init_user(user_id)
        self._reset_weekly_quota_if_needed(user)

        return {
            "user_id": user_id,
            "free_quota_remaining": PRICING["free"]["quota_per_week"] - user["free_quota"]["used_this_week"],
            "free_quota_total": PRICING["free"]["quota_per_week"],
            "credits": user["credits"],
            "packages": user["packages"],
            "created_at": user["created_at"]
        }

    def check_can_analyze(self, user_id: str) -> tuple[bool, str]:
        """
        检查用户是否可以进行分析
        返回: (can_analyze, reason)
        """
        user = self._init_user(user_id)
        self._reset_weekly_quota_if_needed(user)

        # 1. 检查免费额度
        if user["free_quota"]["used_this_week"] < PRICING["free"]["quota_per_week"]:
            return True, "free_quota"

        # 2. 检查积分
        if user["credits"] > 0:
            return True, "credits"

        # 3. 检查套餐
        for pkg_id, pkg_info in user["packages"].items():
            if pkg_info["remaining"] > 0:
                return True, f"package_{pkg_id}"

        return False, "no_quota"

    def use_quota(self, user_id: str, count: int = 1) -> bool:
        """
        使用配额
        返回: 是否成功
        """
        user = self._init_user(user_id)
        self._reset_weekly_quota_if_needed(user)

        can_use, source = self.check_can_analyze(user_id)

        if not can_use:
            return False

        # 记录使用
        usage = {
            "time": datetime.now().isoformat(),
            "count": count,
            "source": source
        }
        user["usage_history"].append(usage)
        user["last_active"] = datetime.now().isoformat()

        # 扣减配额
        if source == "free_quota":
            user["free_quota"]["used_this_week"] += count
        elif source == "credits":
            user["credits"] -= count
        elif source.startswith("package_"):
            pkg_id = source.replace("package_", "")
            if pkg_id in user["packages"]:
                user["packages"][pkg_id]["remaining"] -= count

        self._save_user_db()
        return True

    def add_credits(self, user_id: str, credits: int, source: str = "manual"):
        """添加积分"""
        user = self._init_user(user_id)
        user["credits"] += credits
        user["last_active"] = datetime.now().isoformat()

        # 记录购买
        if source != "manual":
            usage = {
                "time": datetime.now().isoformat(),
                "type": "purchase",
                "credits_added": credits,
                "source": source
            }
            user["usage_history"].append(usage)

        self._save_user_db()
        return True

    def purchase_package(self, user_id: str, package_id: str) -> bool:
        """购买套餐"""
        if package_id not in PRICING["packages"]:
            return False

        pkg = PRICING["packages"][package_id]

        if user_id not in self.user_db:
            self._init_user(user_id)

        user = self.user_db[user_id]

        # 添加套餐
        if package_id not in user["packages"]:
            user["packages"][package_id] = {
                "name": pkg["name"],
                "total": pkg["times"],
                "remaining": pkg["times"],
                "purchased_at": datetime.now().isoformat()
            }
        else:
            # 累加套餐次数
            user["packages"][package_id]["total"] += pkg["times"]
            user["packages"][package_id]["remaining"] += pkg["times"]

        user["last_active"] = datetime.now().isoformat()
        self._save_user_db()
        return True

    def get_pricing_info(self) -> Dict[str, Any]:
        """获取定价信息"""
        return PRICING


# ====================== 批量分析管理类 ======================
class BatchAnalyzer:
    """批量分析管理器"""

    def __init__(self, quota_manager: UserQuotaManager):
        self.quota_manager = quota_manager
        self.max_stocks_per_batch = PRICING["batch_analysis"]["max_stocks"]

    def validate_batch(self, stock_list: list) -> tuple[bool, str]:
        """验证批量分析请求"""
        if len(stock_list) == 0:
            return False, "股票列表为空"

        if len(stock_list) > self.max_stocks_per_batch:
            return False, f"批量分析最多支持{self.max_stocks_per_batch}只股票"

        if len(stock_list) == 1:
            return False, "单只股票请使用普通分析功能"

        return True, "valid"

    def can_use_batch(self, user_id: str) -> bool:
        """检查用户是否可以使用批量分析"""
        # 批量分析优先使用积分，积分不足时检查套餐
        user = self.quota_manager._init_user(user_id)
        if user.get("credits", 0) >= PRICING["batch_analysis"]["price"]:
            return True
        # 检查套餐剩余次数
        for pkg_id, pkg_info in user.get("packages", {}).items():
            if pkg_info.get("remaining", 0) >= 1:
                return True
        # 批量分析不消耗免费配额
        return False

    def use_batch_quota(self, user_id: str, stock_count: int) -> bool:
        """批量分析扣费：按批次收费（无论几只股票，统一收费）"""
        user = self.quota_manager._init_user(user_id)
        batch_price = PRICING["batch_analysis"]["price"]
        # 优先扣积分
        if user.get("credits", 0) >= batch_price:
            user["credits"] -= batch_price
            user["usage_history"].append({
                "time": datetime.now().isoformat(),
                "type": "batch_analysis",
                "count": stock_count,
                "cost": batch_price
            })
            self.quota_manager._save_user_db()
            return True
        # 扣套餐次数（1次）
        for pkg_id, pkg_info in user.get("packages", {}).items():
            if pkg_info.get("remaining", 0) >= 1:
                pkg_info["remaining"] -= 1
                user["usage_history"].append({
                    "time": datetime.now().isoformat(),
                    "type": "batch_analysis",
                    "count": stock_count,
                    "cost": 0
                })
                self.quota_manager._save_user_db()
                return True
        return False

    def get_comparison_metrics(self, results: list) -> Dict[str, Any]:
        """
        生成对比分析指标
        来自各个股票的分析结果
        """
        comparison = {
            "summary": {},
            "rankings": {},
            "highlights": []
        }

        # 提取共同指标进行对比
        for result in results:
            # 这里需要根据实际分析结果调整
            pass

        return comparison


# ====================== 便捷函数 ======================
_quota_manager = None

def get_quota_manager() -> UserQuotaManager:
    """获取配额管理器单例"""
    global _quota_manager
    if _quota_manager is None:
        _quota_manager = UserQuotaManager()
    return _quota_manager


def check_user_quota(user_id: str) -> Dict[str, Any]:
    """快捷函数：检查用户配额"""
    manager = get_quota_manager()
    return manager.get_user_info(user_id)


def use_analysis_quota(user_id: str) -> tuple[bool, str]:
    """快捷函数：使用分析配额"""
    manager = get_quota_manager()
    can_analyze, reason = manager.check_can_analyze(user_id)
    if can_analyze:
        manager.use_quota(user_id, 1)
    return can_analyze, reason


if __name__ == "__main__":
    # 测试代码
    manager = UserQuotaManager()

    print("=" * 50)
    print("ValU AI 定价与配额系统测试")
    print("=" * 50)

    # 测试用户
    test_user = "test_user_001"

    # 查看定价
    print("\n[Pricing]")
    pricing = manager.get_pricing_info()
    print(f"  Free: {pricing['free']['quota_per_week']} times/week")
    print(f"  Per use: {pricing['pay_per_use']['price_per_time']} CNY")
    print(f"  Batch: {pricing['batch_analysis']['price']} CNY (max {pricing['batch_analysis']['max_stocks']} stocks)")
    print("\n  Packages:")
    for pkg_id, pkg in pricing['packages'].items():
        print(f"    {pkg['name']}: {pkg['times']} times original {pkg['original_price']} CNY -> {pkg['discount_price']} CNY")

    # Test quota check
    print(f"\n[User] {test_user} quota:")
    info = manager.get_user_info(test_user)
    print(f"  Free remaining: {info['free_quota_remaining']}/{info['free_quota_total']}/week")
    print(f"  Credits: {info['credits']}")
    print(f"  Packages: {info['packages']}")

    # Test quota usage
    print(f"\n[Check]")
    can, reason = manager.check_can_analyze(test_user)
    print(f"  Can analyze: {can}, source: {reason}")

    # Use quota
    if can:
        manager.use_quota(test_user, 1)
        print(f"  [OK] Quota used")

        # Check again
        can, reason = manager.check_can_analyze(test_user)
        print(f"  Re-check: can={can}, source={reason}")
