#!/usr/bin/env python3
"""
Sih.Ai 配额管理
验证用户余额、生成充值链接、扣除积分（MVP本地版本）
"""

import os
import json
import time
import uuid
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime


class QuotaChecker:
    """用户配额验证和管理（本地文件版本 - MVP）"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化配额检查器

        Args:
            api_key: Sih.Ai API Key（用于内部调用，可选）
        """
        self.api_key = api_key

        # 本地配额文件
        self.quota_dir = Path.home() / ".sih_ai"
        self.quota_dir.mkdir(parents=True, exist_ok=True)
        self.user_file = self.quota_dir / "current_user.json"
        self.history_file = self.quota_dir / "usage_history.jsonl"

        # 获取或创建用户
        self.user_id = self._get_or_create_user_id()

    def _get_or_create_user_id(self) -> str:
        """获取或创建用户唯一ID"""
        if self.user_file.exists():
            data = json.loads(self.user_file.read_text())
            return data["user_id"]
        else:
            # 生成新用户ID
            user_id = f"claw_{int(time.time())}_{uuid.uuid4().hex[:8]}"

            # 新用户赠送5次免费体验
            initial_data = {
                "user_id": user_id,
                "credits": 5,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_topup": 0,
                "total_used": 0
            }

            self.user_file.write_text(json.dumps(initial_data, indent=2))

            print(f"\n{'='*60}")
            print(f"🎉 欢迎使用 Sih.Ai!")
            print(f"📱 您的用户ID: {user_id}")
            print(f"🎁 新用户福利: 已赠送 {initial_data['credits']} 次免费体验")
            print(f"{'='*60}\n")

            return user_id

    def check_balance(self) -> Dict:
        """
        检查用户余额

        Returns:
            {
                "user_id": "xxx",
                "credits": 100,
                "created_at": "2026-03-13T...",
                "total_topup": 0,
                "total_used": 0
            }
        """
        if not self.user_file.exists():
            return self._get_or_create_user_id()

        data = json.loads(self.user_file.read_text())
        return {
            "user_id": data["user_id"],
            "credits": data["credits"],
            "created_at": data.get("created_at"),
            "total_topup": data.get("total_topup", 0),
            "total_used": data.get("total_used", 0)
        }

    def has_balance(self, required: int = 1) -> bool:
        """
        检查余额是否足够

        Args:
            required: 需要的积分数

        Returns:
            True if 余额足够
        """
        balance_info = self.check_balance()
        return balance_info.get("credits", 0) >= required

    def deduct(self, credits: int, operation: str = "image_edit", prompt: str = "") -> Dict:
        """
        扣除用户积分

        Args:
            credits: 扣除的积分数
            operation: 操作类型（image_edit, batch_edit, style_transfer等）
            prompt: 用户的prompt描述

        Returns:
            {
                "success": true,
                "user_id": "xxx",
                "credits_deducted": 10,
                "remaining": 90,
                "operation": "image_edit"
            }
        """
        data = json.loads(self.user_file.read_text())

        if data["credits"] < credits:
            return {
                "success": False,
                "error": "insufficient_credits",
                "message": f"余额不足，需要 {credits} 积分，当前余额 {data['credits']}"
            }

        # 扣除积分
        data["credits"] -= credits
        data["total_used"] = data.get("total_used", 0) + credits
        data["last_updated"] = datetime.now().isoformat()

        # 保存更新
        self.user_file.write_text(json.dumps(data, indent=2))

        # 记录使用历史
        self._log_usage(credits, operation, prompt)

        return {
            "success": True,
            "user_id": data["user_id"],
            "credits_deducted": credits,
            "remaining": data["credits"],
            "operation": operation
        }

    def add_credits(self, credits: int, source: str = "topup") -> Dict:
        """
        添加积分（充值后调用）

        Args:
            credits: 添加的积分数
            source: 来源（topup, free, bonus等）

        Returns:
            操作结果
        """
        data = json.loads(self.user_file.read_text())
        data["credits"] += credits
        data["total_topup"] = data.get("total_topup", 0) + credits
        data["last_updated"] = datetime.now().isoformat()

        self.user_file.write_text(json.dumps(data, indent=2))

        print(f"\n{'='*60}")
        print(f"✅ 充值成功！")
        print(f"💰 添加积分: +{credits}")
        print(f"📊 当前余额: {data['credits']} 积分")
        print(f"{'='*60}\n")

        return {
            "success": True,
            "user_id": data["user_id"],
            "credits_added": credits,
            "remaining": data["credits"]
        }

    def show_topup_url(self, package: Optional[str] = None) -> str:
        """
        生成充值链接

        Args:
            package: 推荐的套餐（basic/pro/enterprise）

        Returns:
            充值页面URL
        """
        base_topup_url = "https://sih.ai/topup"
        params = {"user": self.user_id, "source": "claw"}

        if package:
            params["package"] = package

        # 构建URL
        from urllib.parse import urlencode
        url = f"{base_topup_url}?{urlencode(params)}"

        # 显示充值引导
        balance = self.check_balance()
        print(f"\n{'='*60}")
        print(f"⚠️  余额不足")
        print(f"📊 当前余额: {balance['credits']} 积分")
        print(f"💡 请访问以下地址充值:")
        print(f"\n   {url}")
        print(f"\n充值后，返回这里发送 '已充值' 即可继续使用")
        print(f"{'='*60}\n")

        return url

    def _log_usage(self, credits: int, operation: str, prompt: str):
        """记录使用历史"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "credits": credits,
            "prompt": prompt[:100] if prompt else "",  # 只保存前100字符
            "user_id": self.user_id
        }

        with open(self.history_file, "a") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def get_usage_history(self, limit: int = 10) -> list:
        """获取最近的使用历史"""
        if not self.history_file.exists():
            return []

        history = []
        with open(self.history_file, "r") as f:
            for line in f:
                try:
                    history.append(json.loads(line.strip()))
                except:
                    continue

        return history[-limit:]

    def get_pricing(self) -> Dict:
        """
        获取操作定价

        Returns:
            定价表
        """
        return {
            "change_clothes": 10,      # 换装
            "change_background": 5,    # 换背景
            "swap_face": 15,           # 换脸
            "style_transfer": 8,       # 风格转换
            "beautify": 5,             # 美颜
            "remove_background": 3,    # 去背景
            "anime_style": 10,         # 动漫化
            "batch_discount": 0.8      # 批量处理折扣
        }

    def estimate_cost(self, prompt: str) -> int:
        """
        根据prompt估算所需积分

        Args:
            prompt: 用户输入的编辑指令

        Returns:
            预估积分数
        """
        pricing = self.get_pricing()
        prompt_lower = prompt.lower()

        # 简单的关键词匹配
        if "换脸" in prompt_lower or "swap" in prompt_lower or "脸换成" in prompt_lower:
            return pricing["swap_face"]
        elif "换衣服" in prompt_lower or "换装" in prompt_lower or "服装" in prompt_lower or "衣服换成" in prompt_lower:
            return pricing["change_clothes"]
        elif "背景" in prompt_lower:
            return pricing["change_background"]
        elif "动漫" in prompt_lower or "anime" in prompt_lower or "风格" in prompt_lower or "转换成" in prompt_lower:
            return pricing["style_transfer"]
        elif "美颜" in prompt_lower or "美化" in prompt_lower or "磨皮" in prompt_lower:
            return pricing["beautify"]
        else:
            return 5  # 默认价格

    def show_user_info(self):
        """显示用户信息"""
        balance = self.check_balance()
        history = self.get_usage_history(5)

        print(f"\n{'='*60}")
        print(f"👤 Sih.Ai 用户信息")
        print(f"{'='*60}")
        print(f"📱 用户ID: {balance['user_id']}")
        print(f"💰 当前余额: {balance['credits']} 积分")
        print(f"📅 注册时间: {balance.get('created_at', 'N/A')}")
        print(f"📊 累计充值: {balance.get('total_topup', 0)} 积分")
        print(f"📈 累计使用: {balance.get('total_used', 0)} 积分")

        if history:
            print(f"\n📝 最近使用:")
            for i, entry in enumerate(reversed(history[-5:]), 1):
                prompt_preview = entry.get('prompt', '')[:30]
                print(f"   {i}. {entry['operation']} ({entry['credits']}积分) - {prompt_preview}...")

        print(f"{'='*60}\n")


# 便捷函数
def get_quota_checker() -> QuotaChecker:
    """获取配额检查器实例（单例模式）"""
    return QuotaChecker()


# 命令行工具
if __name__ == "__main__":
    import sys

    quota = QuotaChecker()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "info":
            quota.show_user_info()

        elif command == "topup":
            quota.show_topup_url()

        elif command == "add":
            # 模拟充值（测试用）
            if len(sys.argv) > 2:
                credits = int(sys.argv[2])
                quota.add_credits(credits, source="test")

        elif command == "history":
            history = quota.get_usage_history(20)
            print(f"\n📝 最近 {len(history)} 次使用记录:\n")
            for entry in reversed(history):
                print(f"  • {entry['timestamp']}")
                print(f"    操作: {entry['operation']} ({entry['credits']}积分)")
                print(f"    Prompt: {entry.get('prompt', 'N/A')}")
                print()

        else:
            print(f"未知命令: {command}")
            print("可用命令: info, topup, add <credits>, history")
    else:
        quota.show_user_info()
