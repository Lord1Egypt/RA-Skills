#!/usr/bin/env python3
"""冲突检测与解决机制
参考 xiaoyi-claw-omega-final 的冲突处理体系
"""
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from pathlib import Path

class ConflictDetector:
    """冲突检测器"""
    
    # 冲突类型
    TYPE_USER_PROFILE = "user_profile"      # 用户画像冲突
    TYPE_FACT = "fact"                     # 事实性冲突
    TYPE_PREFERENCE = "preference"         # 偏好冲突
    TYPE_DECISION = "decision"             # 决策冲突
    TYPE_SYSTEM = "system"                  # 系统配置冲突
    
    # 冲突级别
    LEVEL_HIGH = "high"      # 必须确认
    LEVEL_MEDIUM = "medium"  # 建议确认
    LEVEL_LOW = "low"        # 自动处理
    
    def __init__(self, memory_index: List[Dict]):
        self.memory_index = memory_index
        self.conflicts = []
    
    def check_conflict(self, new_item: Dict) -> List[Dict]:
        """检测新记忆是否与现有记忆冲突
        
        Args:
            new_item: 新记忆 {"title": ..., "content": ..., "type": ..., "importance": ...}
            
        Returns:
            冲突列表 []
        """
        conflicts = []
        new_title = new_item.get("title", "").lower()
        new_content = new_item.get("content", "").lower()
        new_type = new_item.get("type", "info")
        
        for existing in self.memory_index:
            existing_title = existing.get("title", "").lower()
            existing_type = existing.get("type", "info")
            
            # 1. 用户画像冲突检测
            if new_type == "preference" and existing_type == "preference":
                if self._similar_text(new_title, existing_title):
                    conflicts.append({
                        "type": self.TYPE_PREFERENCE,
                        "level": self.LEVEL_MEDIUM,
                        "existing": existing,
                        "new": new_item,
                        "reason": "偏好信息重复或冲突"
                    })
            
            # 2. 决策冲突检测
            if new_type == "decision" and existing_type == "decision":
                if self._similar_text(new_title, existing_title):
                    conflicts.append({
                        "type": self.TYPE_DECISION,
                        "level": self.LEVEL_HIGH,
                        "existing": existing,
                        "new": new_item,
                        "reason": "决策信息可能重复"
                    })
            
            # 3. 事实性冲突检测（时间敏感）
            if self._has_time_conflict(new_content, existing.get("content", "")):
                conflicts.append({
                    "type": self.TYPE_FACT,
                    "level": self.LEVEL_HIGH,
                    "existing": existing,
                    "new": new_item,
                    "reason": "时间或事实信息冲突"
                })
            
            # 4. 系统配置冲突
            if new_type == "system" and existing_type == "system":
                if new_title == existing_title:
                    conflicts.append({
                        "type": self.TYPE_SYSTEM,
                        "level": self.LEVEL_HIGH,
                        "existing": existing,
                        "new": new_item,
                        "reason": "系统配置冲突"
                    })
        
        return conflicts
    
    def _similar_text(self, text1: str, text2: str, threshold: float = 0.7) -> bool:
        """检查两个文本是否相似（简单版）"""
        # 去除标点符号
        text1_clean = re.sub(r'[^\w\s]', '', text1)
        text2_clean = re.sub(r'[^\w\s]', '', text2)
        
        # 词集合
        words1 = set(text1_clean.split())
        words2 = set(text2_clean.split())
        
        if not words1 or not words2:
            return False
        
        # Jaccard 相似度
        intersection = words1 & words2
        union = words1 | words2
        jaccard = len(intersection) / len(union) if union else 0
        
        return jaccard >= threshold
    
    def _has_time_conflict(self, text1: str, text2: str) -> bool:
        """检查两个文本是否有时间冲突"""
        # 提取时间表达式
        time_pattern = r'\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}'
        
        times1 = set(re.findall(time_pattern, text1))
        times2 = set(re.findall(time_pattern, text2))
        
        # 如果有相同时间但内容不同，标记为冲突
        if times1 & times2:
            # 进一步检查关键信息是否矛盾
            conflict_indicators = ["不是", "不等于", "错误", "假的", "wrong", "incorrect", "no", "not"]
            for indicator in conflict_indicators:
                if indicator in text1 and any(word in text2 for word in times1):
                    return True
        
        return False
    
    def resolve_conflict(self, conflict: Dict, resolution: str) -> Dict:
        """解决冲突
        
        Args:
            conflict: 冲突信息
            resolution: 解决方案 ("keep_existing", "keep_new", "merge", "manual")
            
        Returns:
            处理结果
        """
        existing = conflict["existing"]
        new = conflict["new"]
        
        if resolution == "keep_existing":
            return {
                "action": "kept_existing",
                "item": existing
            }
        elif resolution == "keep_new":
            return {
                "action": "replaced_existing",
                "item": new
            }
        elif resolution == "merge":
            # 合并内容
            merged = {
                **existing,
                "content": existing.get("content", "") + "\n" + new.get("content", ""),
                "last_modified": datetime.now().isoformat()
            }
            return {
                "action": "merged",
                "item": merged
            }
        else:
            return {
                "action": "manual_review_required",
                "existing": existing,
                "new": new
            }
    
    def auto_resolve(self, conflict: Dict) -> str:
        """自动决定解决方案
        
        Args:
            conflict: 冲突信息
            
        Returns:
            推荐解决方案
        """
        level = conflict.get("level")
        
        # 高优先级必须手动确认
        if level == self.LEVEL_HIGH:
            return "manual"
        
        # 低优先级自动处理
        if level == self.LEVEL_LOW:
            return "merge"
        
        # 中优先级按类型处理
        conflict_type = conflict.get("type")
        if conflict_type == self.TYPE_PREFERENCE:
            return "merge"  # 偏好可以合并
        elif conflict_type == self.TYPE_DECISION:
            return "keep_new"  # 决策保留新的
        elif conflict_type == self.TYPE_FACT:
            return "manual"  # 事实必须确认
        else:
            return "keep_new"  # 默认保留新的
    
    def get_conflict_summary(self) -> str:
        """生成冲突摘要"""
        if not self.conflicts:
            return "✅ 未检测到冲突"
        
        high = [c for c in self.conflicts if c["level"] == self.LEVEL_HIGH]
        medium = [c for c in self.conflicts if c["level"] == self.LEVEL_MEDIUM]
        low = [c for c in self.conflicts if c["level"] == self.LEVEL_LOW]
        
        summary = f"⚠️ 检测到 {len(self.conflicts)} 个冲突：\n"
        if high:
            summary += f"  🔴 高优先级: {len(high)} 个（需手动确认）\n"
        if medium:
            summary += f"  🟡 中优先级: {len(medium)} 个\n"
        if low:
            summary += f"  🟢 低优先级: {len(low)} 个\n"
        
        return summary


class EvidenceTracker:
    """证据链追溯"""
    
    def __init__(self):
        self.evidence_chain = []
    
    def add_evidence(self, claim: str, source: str, confidence: float = 1.0):
        """添加证据
        
        Args:
            claim: 主张/结论
            source: 来源（对话/文档/用户）
            confidence: 置信度 0-1
        """
        self.evidence_chain.append({
            "claim": claim,
            "source": source,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_evidence(self, claim: str) -> List[Dict]:
        """获取主张的证据"""
        return [e for e in self.evidence_chain if e["claim"] == claim]
    
    def format_evidence_report(self, claim: str) -> str:
        """格式化证据报告"""
        evidence = self.get_evidence(claim)
        if not evidence:
            return f"❓ 未找到 '{claim}' 的相关证据"
        
        report = f"📋 证据报告: {claim}\n"
        report += "=" * 40 + "\n\n"
        
        for i, e in enumerate(evidence, 1):
            conf = "⭐" * int(e["confidence"] * 5)
            report += f"{i}. {conf} ({e['confidence']:.0%})\n"
            report += f"   来源: {e['source']}\n"
            report += f"   时间: {e['timestamp']}\n\n"
        
        return report


if __name__ == "__main__":
    # 测试
    print("=== 冲突检测测试 ===")
    
    # 模拟记忆索引
    index = [
        {"title": "用户喜欢中文", "type": "preference", "content": "用户偏好使用中文"},
        {"title": "系统配置", "type": "system", "content": "配置项A=true"},
    ]
    
    detector = ConflictDetector(index)
    
    # 测试新记忆
    new_item = {"title": "用户喜欢中文交流", "type": "preference", "content": "用户偏好中文交流"}
    conflicts = detector.check_conflict(new_item)
    
    print(f"检测到 {len(conflicts)} 个冲突")
    for c in conflicts:
        print(f"  - {c['type']}: {c['reason']}")
    
    # 测试证据链
    print("\n=== 证据链测试 ===")
    tracker = EvidenceTracker()
    tracker.add_evidence("用户使用飞书", "对话记录2026-04-07", 0.95)
    tracker.add_evidence("用户使用微信", "对话记录2026-04-06", 0.8)
    
    print(tracker.format_evidence_report("用户使用飞书"))
