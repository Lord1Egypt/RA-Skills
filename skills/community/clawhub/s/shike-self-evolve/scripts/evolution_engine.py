#!/usr/bin/env python3
"""
self-evolve.skill 进化引擎 v2.0
配合SKILL.md使用，提供辅助功能
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# ============================================================
# 关键词检测器
# ============================================================

EVOLUTION_KEYWORDS = {
    "urgent": ["以后", "永远", "每次", "必须", "一定", "禁止"],
    "standard": ["记住", "下次", "别再", "不要再", "记得"],
    "mild": ["倾向", "偏好", "喜欢", "习惯"],
}

NOISE_PATTERNS = [
    "今天好累", "现在很忙", "今天心情",
    "开心", "生气", "天气不错", "想吃", "喜欢吃的",
]

def detect_keyword_level(text: str) -> Optional[str]:
    """检测关键词级别：urgent/standard/mild/None"""
    for level in ["urgent", "standard", "mild"]:
        for kw in EVOLUTION_KEYWORDS[level]:
            if kw in text:
                return level
    return None

def is_noise(text: str) -> bool:
    """判断是否为噪音内容"""
    for pattern in NOISE_PATTERNS:
        if pattern in text:
            return True
    return False

def is_negation(text: str, keyword: str) -> bool:
    """检查关键词是否在否定句中"""
    idx = text.find(keyword)
    if idx <= 0:
        return False
    prefix = text[:idx]
    negation_words = ["不要", "不用", "别", "无需"]
    return any(nw in prefix for nw in negation_words)

def is_question(text: str) -> bool:
    """检查是否为疑问句"""
    return text.rstrip().endswith("？") or text.rstrip().endswith("?")


# ============================================================
# 踩坑检测器
# ============================================================

FAILURE_THRESHOLDS = {
    "tool_calls_exceeded": 5,
    "multiple_retries": 3,
    "user_corrections": 2,
    "git_rollback": 1,
    "timeout_failure": 1,
}

def detect_failures(stats: Dict[str, int]) -> List[Dict]:
    """检测踩坑情况，返回超过阈值的指标列表"""
    failures = []
    for indicator, threshold in FAILURE_THRESHOLDS.items():
        actual = stats.get(indicator, 0)
        if actual >= threshold:
            failures.append({
                "indicator": indicator,
                "actual": actual,
                "threshold": threshold,
            })
    return failures


# ============================================================
# 进化频率控制器
# ============================================================

class RateController:
    """进化频率控制"""
    
    def __init__(self, max_daily: int = 5, max_weekly: int = 15):
        self.max_daily = max_daily
        self.max_weekly = max_weekly
        self.daily_count = 0
        self.weekly_count = 0
    
    def should_evolve(self, importance: str) -> Tuple[bool, str]:
        """判断是否允许进化"""
        if importance == "high":
            return True, "重要内容不受限制"
        if self.daily_count >= self.max_daily:
            return False, f"今日已达上限({self.max_daily}次)"
        if self.weekly_count >= self.max_weekly:
            return False, f"本周已达上限({self.max_weekly}次)"
        return True, "频率正常"
    
    def record(self):
        """记录一次进化"""
        self.daily_count += 1
        self.weekly_count += 1


# ============================================================
# 进化请求生成器
# ============================================================

def generate_evolution_card(
    request_id: int,
    trigger: str,
    level: str,
    content: str,
    target_layer: str,
    target_path: str,
    importance: str,
    reusability: str,
    risk: str,
) -> str:
    """生成进化请求卡片"""
    return f"""🧬 进化请求 #{request_id}

触发：{trigger} | 级别：{level}
建议记忆：> {content}
目标：{target_layer} → {target_path}
评估：重要性{importance} 复用性{reusability} 风险{risk}
→ 「进化」确认 | 「进化 L2」变更层级 | 「忽略」跳过 | 「修改」调整"""


def determine_layer(text: str, trigger: str) -> Tuple[str, str]:
    """判断目标层级和路径"""
    if any(kw in text for kw in ["技能", "skill"]):
        return "L2", "SKILL.md（需指定具体skill）"
    if any(kw in text for kw in ["所有", "全局", "规范", "CLAUDE"]):
        return "L3", "/root/.openclaw/workspace/CLAUDE.md"
    if trigger == "failure":
        return "L2", "SKILL.md（需指定具体skill）"
    return "L1", "/root/.openclaw/workspace/MEMORY.md"


def extract_core_intent(text: str, keyword: str) -> str:
    """提取核心意图（去除触发词）"""
    result = text
    for level_keywords in EVOLUTION_KEYWORDS.values():
        for kw in level_keywords:
            result = result.replace(kw, "")
    return result.strip()


# ============================================================
# 主流程
# ============================================================

def process_user_message(text: str, stats: Optional[Dict] = None) -> Optional[str]:
    """处理用户消息，检测进化机会"""
    
    # 1. 关键词检测
    level = detect_keyword_level(text)
    if level:
        # 误触发保护
        if is_negation(text, "记住"):
            return None
        if is_question(text):
            level = "mild"  # 疑问句降级
        
        # 噪音过滤
        if is_noise(text):
            return None
        
        # 提取意图
        content = extract_core_intent(text, "")
        if not content:
            return None
        
        # 判断层级
        layer, path = determine_layer(text, "keyword")
        
        # 生成卡片
        return generate_evolution_card(
            request_id=1,
            trigger=f"关键词",
            level=level,
            content=content,
            target_layer=layer,
            target_path=path,
            importance="H" if level == "urgent" else "M",
            reusability="H" if layer == "L1" else "M",
            risk="无" if layer == "L1" else "低",
        )
    
    # 2. 踩坑检测
    if stats:
        failures = detect_failures(stats)
        if failures:
            failure_desc = "、".join(f"{f['indicator']}({f['actual']}次)" for f in failures)
            return generate_evolution_card(
                request_id=1,
                trigger=f"踩坑-{failure_desc}",
                level="standard",
                content="[需Agent分析根因后填入]",
                target_layer="L2",
                target_path="SKILL.md（需指定具体skill）",
                importance="H",
                reusability="M",
                risk="低",
            )
    
    return None


# ============================================================
# 命令行测试
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("self-evolve.skill v2.0 进化引擎测试")
    print("=" * 60)
    
    # 测试1：关键词触发
    print("\n--- 测试1：关键词触发 ---")
    result = process_user_message("以后回复简洁一点，不要长篇大论")
    print(result or "未触发进化")
    
    # 测试2：踩坑检测
    print("\n--- 测试2：踩坑检测 ---")
    result = process_user_message("", {"tool_calls_exceeded": 6, "multiple_retries": 4})
    print(result or "未触发进化")
    
    # 测试3：噪音过滤
    print("\n--- 测试3：噪音过滤 ---")
    result = process_user_message("今天心情不太好，以后少说点开心的")
    print(result or "未触发进化（噪音过滤）")
    
    # 测试4：否定句不触发
    print("\n--- 测试4：否定句不触发 ---")
    result = process_user_message("不要记住这个")
    print(result or "未触发进化")
    
    # 测试5：频率控制
    print("\n--- 测试5：频率控制 ---")
    controller = RateController()
    for i in range(6):
        allowed, reason = controller.should_evolve("medium")
        if allowed:
            controller.record()
            print(f"  第{i+1}次：✅ 允许 - {reason}")
        else:
            print(f"  第{i+1}次：❌ 拒绝 - {reason}")
