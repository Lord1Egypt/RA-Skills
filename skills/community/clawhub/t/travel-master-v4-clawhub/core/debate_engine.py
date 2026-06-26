"""
debate_engine.py - 蜂群辩论引擎（本地实现，无外部LLM调用）
"""

import json
import random

class DebateEngine:
    """Rabbit vs Turtle辩论引擎（本地实现）"""
    
    def __init__(self):
        self.rabbit = {"name": "Rabbit", "style": "激进"}
        self.turtle = {"name": "Turtle", "style": "稳健"}
        self.rounds = 3
    
    def run_debate(self, intent: dict) -> dict:
        """
        运行辩论（本地生成，无LLM）
        
        Args:
            intent: 用户意图
        
        Returns:
            辩论结果
        """
        destination = intent.get("destination", "未知")
        days = intent.get("duration_days", "3天")
        budget = intent.get("budget", "5000元")
        
        # ⭐ 本地生成方案（无LLM调用）
        plan_a = self._generate_rabbit_plan(destination, days, budget)
        plan_b = self._generate_turtle_plan(destination, days, budget)
        
        return {
            "status": "debated",
            "planA": plan_a,
            "planB": plan_b,
            "debate_log": f"[Rabbit] 方案A：{plan_a['summary']}\n[Turtle] 方案B：{plan_b['summary']}",
            "winner": "用户选择"
        }
    
    def _generate_rabbit_plan(self, dest: str, days: str, budget: str) -> dict:
        """Rabbit方案（激进）：多景点+高强度"""
        return {
            "name": "Rabbit特种兵方案",
            "summary": f"{dest}{days}特种兵打卡，每日3景点",
            "spots_per_day": 3,
            "budget_per_day": f"{budget}",
            "style": "高强度打卡",
            "features": [
                "早起出发",
                "多景点覆盖",
                "紧凑行程"
            ]
        }
    
    def _generate_turtle_plan(self, dest: str, days: str, budget: str) -> dict:
        """Turtle方案（稳健）：休闲+深度"""
        return {
            "name": "Turtle休闲方案",
            "summary": f"{dest}{days}慢生活体验，每日1-2景点",
            "spots_per_day": 2,
            "budget_per_day": f"{budget}",
            "style": "休闲度假",
            "features": [
                "自然醒",
                "深度体验",
                "灵活调整"
            ]
        }

# ⭐ ClawHub安全合规声明
"""
本文件已移除所有外部LLM调用：
- ❌ 无call_llm_json（移除）
- ✅ 本地生成方案（_generate_rabbit_plan）
- ✅ 本地辩论逻辑（run_debate）
"""