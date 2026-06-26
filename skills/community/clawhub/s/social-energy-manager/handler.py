"""Social Energy Manager - 社交电量管理器"""
import json
import re
from datetime import datetime

def parse_social_text(text: str) -> dict:
    result = {"current_level": None, "situation": None}
    if any(k in text for k in ["很累", "精疲力竭", "耗尽", "充电"]): result["current_level"] = "低"
    elif any(k in text for k in ["还行", "正常", "平衡"]): result["current_level"] = "中"
    elif any(k in text for k in ["兴奋", "满格", "能量足"]): result["current_level"] = "高"
    result["situation"] = text[:80]
    return result

def assess_energy_level(level: str) -> dict:
    levels = {
        "低": {"score": 25, "color": "红色", "status": "需要立即充电", "action": "减少社交，增加独处和恢复性活动"},
        "中": {"score": 55, "color": "黄色", "status": "基本平衡，可以维持", "action": "选择性社交，优先高质量独处"},
        "高": {"score": 85, "color": "绿色", "status": "社交电量充沛", "action": "适合深度社交和建立连接"}
    }
    return levels.get(level, levels["中"])

def energy_recovery_plan(level: str) -> dict:
    plans = {
        "低": {
            "immediate": ["拒绝非必要社交", "至少2小时独处", "做一件让自己开心的小事"],
            "daily": ["设定每日社交上限（如不超过2次）", "社交后安排恢复时间", "优先一对一小聚而非大群体"],
            "weekly": ["安排1次'社交戒毒日'（完全独处）", "进行恢复性活动：散步、阅读、冥想"]
        },
        "中": {
            "immediate": ["保持现有节奏", "有意识地选择高质量社交"],
            "daily": ["社交前后做5分钟自我检测", "避免'为社交而社交'"],
            "weekly": ["复盘本周社交：哪些充电？哪些耗电？"]
        },
        "高": {
            "immediate": ["保持开放心态", "主动发起高质量深度交流"],
            "daily": ["把握能量高峰期建立新的连接"],
            "weekly": ["设置社交上限，防止过度社交"]
        }
    }
    return plans.get(level, plans["中"])

def handle(text: str) -> dict:
    parsed = parse_social_text(text)
    assessment = assess_energy_level(parsed["current_level"] or "中")
    recovery = energy_recovery_plan(parsed["current_level"] or "中")
    return {
        "currentEnergyLevel": parsed["current_level"] or "中",
        "energyAssessment": assessment,
        "recoveryPlan": recovery,
        "socialEnergyLog": {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "logged": True
        },
        "tips": [
            "社交能量是真实存在的资源，不是性格缺陷",
            "高质量社交（少数深度连接）> 低质量社交（多数泛泛之交）",
            "学会说'不'，是对自己社交电量的保护"
        ]
    }

if __name__ == "__main__":
    for tc in ["今天social了一下午，感觉被耗尽了", "周末精力充沛想约朋友出来玩"]:
        r = handle(tc)
        print(f"Input: {tc}\n  -> 电量: {r['currentEnergyLevel']} ({r['energyAssessment']['color']}区 | {r['energyAssessment']['status']})\n  -> 立即行动: {r['recoveryPlan']['immediate'][0]}\n")
