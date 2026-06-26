#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片使用计数器
跟踪每个图片服务的使用量，支持免费额度管理
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class UsageCounter:
    """图片服务使用计数器"""
    
    def __init__(self, counter_file: str = ".usage_counter.json"):
        """
        初始化计数器
        
        Args:
            counter_file: 计数器文件路径
        """
        self.counter_file = Path(counter_file)
        self.data = self._load_counter()
    
    def _load_counter(self) -> Dict:
        """加载计数器数据"""
        if self.counter_file.exists():
            try:
                with open(self.counter_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 检查是否需要重置（每月重置）
                self._check_monthly_reset(data)
                return data
            except Exception as e:
                logger.warning(f"加载计数器失败：{e}")
        
        # 默认数据（限额由配置决定，这里使用默认值）
        return {
            "last_reset": datetime.now().strftime("%Y-%m-%d"),
            "providers": {
                "tongyi-wanxiang": {"count": 0, "limit": 100},  # 通义万相
                "bailian": {"count": 0, "limit": 100},          # 阿里百炼
                "volcengine": {"count": 0, "limit": 100},       # 火山方舟
                "baidu-yige": {"count": 0, "limit": 100},       # 文心一格
                "dall-e-3": {"count": 0, "limit": None},        # DALL-E 3（付费）
                "unsplash": {"count": 0, "limit": None},        # Unsplash（免费）
                "placeholder": {"count": 0, "limit": None}      # 占位图
            },
            "total_images": 0
        }
    
    def _check_monthly_reset(self, data: Dict):
        """检查是否需要月度重置"""
        last_reset = data.get("last_reset", "")
        if not last_reset:
            return
        
        try:
            last_reset_date = datetime.strptime(last_reset, "%Y-%m-%d")
            now = datetime.now()
            
            # 如果已经是下个月，重置计数器
            if now.month > last_reset_date.month or now.year > last_reset_date.year:
                logger.info("检测到新月份，重置免费额度计数器")
                self._reset_monthly(data)
        except Exception as e:
            logger.warning(f"检查月度重置失败：{e}")
    
    def _reset_monthly(self, data: Dict):
        """重置月度计数器"""
        data["last_reset"] = datetime.now().strftime("%Y-%m-%d")
        
        # 重置所有有限额的服务
        for provider, info in data["providers"].items():
            if info.get("limit") is not None:
                info["count"] = 0
                logger.info(f"重置 {provider} 计数器为 0")
    
    def increment(self, provider: str, count: int = 1):
        """
        增加使用计数
        
        Args:
            provider: 服务提供商
            count: 增加数量
        """
        if provider not in self.data["providers"]:
            self.data["providers"][provider] = {"count": 0, "limit": None}
        
        self.data["providers"][provider]["count"] += count
        self.data["total_images"] += count
        self._save_counter()
        
        logger.info(f"{provider} 使用计数 +{count}，当前：{self.data['providers'][provider]['count']}")
    
    def get_usage(self, provider: str) -> Dict:
        """
        获取服务提供商的使用情况
        
        Args:
            provider: 服务提供商
            
        Returns:
            使用情况字典 {count, limit, remaining, percentage}
        """
        if provider not in self.data["providers"]:
            return {"count": 0, "limit": None, "remaining": None, "percentage": 0}
        
        info = self.data["providers"][provider]
        count = info.get("count", 0)
        limit = info.get("limit")
        
        if limit is None:
            # 无限制服务
            return {
                "count": count,
                "limit": None,
                "remaining": None,
                "percentage": 0,
                "unlimited": True
            }
        
        remaining = max(0, limit - count)
        percentage = (count / limit * 100) if limit > 0 else 0
        
        return {
            "count": count,
            "limit": limit,
            "remaining": remaining,
            "percentage": percentage,
            "unlimited": False
        }
    
    def is_quota_exceeded(self, provider: str, threshold: float = 90.0) -> bool:
        """
        检查是否超出额度（或接近额度）
        
        Args:
            provider: 服务提供商
            threshold: 阈值（默认 90%，百分比格式）
            
        Returns:
            True 如果超出或接近额度
        """
        usage = self.get_usage(provider)
        
        # 无限制服务或剩余 None
        if usage.get("unlimited", False) or usage.get("remaining") is None:
            return False
        
        # 剩余额度不足或已达到阈值
        return usage["remaining"] <= 0 or usage["percentage"] >= threshold
    
    def should_use_provider(self, provider: str) -> bool:
        """
        判断是否应该使用某个服务提供商
        
        Args:
            provider: 服务提供商
            
        Returns:
            True 如果可以使用
        """
        # 检查是否超出额度
        if self.is_quota_exceeded(provider):
            logger.warning(f"{provider} 免费额度已用尽或接近用尽，建议切换")
            return False
        
        return True
    
    def _save_counter(self):
        """保存计数器数据"""
        try:
            with open(self.counter_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存计数器失败：{e}")
    
    def get_summary(self) -> str:
        """获取使用摘要"""
        lines = ["📊 图片服务使用统计"]
        lines.append("=" * 40)
        
        for provider, info in self.data["providers"].items():
            count = info.get("count", 0)
            limit = info.get("limit")
            
            if limit is None:
                lines.append(f"{provider}: {count} 张（无限制）")
            else:
                remaining = max(0, limit - count)
                percentage = (count / limit * 100) if limit > 0 else 0
                status = "⚠️ 接近限额" if percentage >= 90 else "✅"
                lines.append(f"{provider}: {count}/{limit} 张 ({percentage:.1f}%) - 剩余 {remaining} 张 {status}")
        
        lines.append("=" * 40)
        lines.append(f"总计：{self.data['total_images']} 张图片")
        lines.append(f"最后重置：{self.data.get('last_reset', '未知')}")
        
        return "\n".join(lines)
    
    def reset(self, provider: Optional[str] = None):
        """
        重置计数器
        
        Args:
            provider: 指定服务提供商（None 则重置所有）
        """
        if provider:
            if provider in self.data["providers"]:
                self.data["providers"][provider]["count"] = 0
                logger.info(f"已重置 {provider} 计数器")
        else:
            self._reset_monthly(self.data)
            logger.info("已重置所有计数器")
        
        self._save_counter()


# 全局计数器实例
_global_counter: Optional[UsageCounter] = None


def get_counter() -> UsageCounter:
    """获取全局计数器实例"""
    global _global_counter
    if _global_counter is None:
        _global_counter = UsageCounter()
    return _global_counter


def test_counter():
    """测试计数器功能"""
    counter = UsageCounter()
    
    print("初始状态:")
    print(counter.get_summary())
    print()
    
    # 模拟使用
    counter.increment("tongyi-wanxiang", 5)
    counter.increment("baidu-yige", 3)
    counter.increment("unsplash", 10)
    
    print("使用后:")
    print(counter.get_summary())
    print()
    
    # 检查额度
    print("额度检查:")
    print(f"通义万相是否可用：{counter.should_use_provider('tongyi-wanxiang')}")
    print(f"通义万相使用情况：{counter.get_usage('tongyi-wanxiang')}")


if __name__ == "__main__":
    test_counter()
