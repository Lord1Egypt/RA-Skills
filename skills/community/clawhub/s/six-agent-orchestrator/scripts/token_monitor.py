#!/usr/bin/env python3
"""
Token配额监控工具
实时监控各Tier的Token消耗，超限预警
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict


class TokenMonitor:
    """Token配额监控器"""
    
    def __init__(self, quota_file: str = "token-quota.json"):
        self.quota_file = Path(quota_file)
        self.quota = self._load_quota()
    
    def _load_quota(self) -> Dict:
        """加载配额配置"""
        if self.quota_file.exists():
            return json.loads(self.quota_file.read_text())
        
        return {
            "tier_0": {"name": "GLM-4.7-Flash", "total": 10000, "used": 0, "limit": 0.45},
            "tier_1": {"name": "DeepSeek系列", "total": 10000, "used": 0, "limit": 0.40},
            "tier_2": {"name": "千问qwen-plus", "total": 10000, "used": 0, "limit": 0.15},
            "tier_3": {"name": "豆包2.0", "total": 10000, "used": 0, "limit": 0.001}
        }
    
    def update_usage(self, tier: int, tokens: int):
        """更新使用量"""
        tier_key = f"tier_{tier}"
        self.quota[tier_key]["used"] += tokens
        self._save_quota()
    
    def check_status(self) -> Dict:
        """检查配额状态"""
        status = {}
        
        for tier_key, info in self.quota.items():
            used = info["used"]
            limit = info["total"] * info["limit"]
            percent = used / limit * 100
            
            # 预警级别
            if percent > 90:
                level = "critical"
            elif percent > 80:
                level = "warning"
            else:
                level = "ok"
            
            status[tier_key] = {
                "name": info["name"],
                "used": used,
                "limit": limit,
                "percent": percent,
                "level": level,
                "remaining": limit - used
            }
        
        return status
    
    def display_status(self):
        """展示配额状态"""
        status = self.check_status()
        
        print(f"\n{'='*50}")
        print(f"Token配额监控")
        print(f"{'='*50}")
        
        for tier_key, info in status.items():
            # 进度条
            bar_length = 20
            filled = int(bar_length * info["percent"] / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            # 预警图标
            icon = "✅" if info["level"] == "ok" else "🟡" if info["level"] == "warning" else "🔴"
            
            print(f"\n{icon} {info['name']}")
            print(f"  [{bar}] {info['percent']:.1f}%")
            print(f"  已用: {info['used']} / 上限: {info['limit']}")
            print(f"  剩余: {info['remaining']}")
        
        # 总计
        total_used = sum(s["used"] for s in status.values())
        total_limit = sum(s["limit"] for s in status.values())
        total_percent = total_used / total_limit * 100
        
        print(f"\n{'='*50}")
        print(f"总消耗: {total_used} / {total_limit} ({total_percent:.1f}%)")
        print(f"{'='*50}")
    
    def _save_quota(self):
        """保存配额"""
        with open(self.quota_file, 'w', encoding='utf-8') as f:
            json.dump(self.quota, f, ensure_ascii=False, indent=2)
    
    def reset(self):
        """重置配额"""
        for tier_key in self.quota:
            self.quota[tier_key]["used"] = 0
        self._save_quota()
        print("配额已重置")


if __name__ == '__main__':
    monitor = TokenMonitor()
    monitor.display_status()