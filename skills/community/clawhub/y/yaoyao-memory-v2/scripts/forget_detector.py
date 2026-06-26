#!/usr/bin/env python3
"""
遗忘检测模块 - v2.0.0
借鉴kektordb的记忆衰减机制

增强：
1. 多维度衰减计算
2. 遗忘风险分级
3. 自动强化建议
4. 矛盾检测
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import Counter


MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


class DecayCalculator:
    """衰减计算器 - 借鉴kektordb"""
    
    # 衰减参数
    BASE_DECAY_RATE = 0.05  # 基础衰减率（每天）
    ACCESS_BOOST = 0.3      # 访问时增强
    IMPORTANCE_MULTIPLIER = {
        "Critical": 0.2,     # 低衰减，高权重
        "High": 0.4,
        "Normal": 0.6,
        "Low": 0.8           # 高衰减，低权重
    }
    
    @classmethod
    def calculate_decay_score(
        cls,
        days_since_access: int,
        importance: str = "Normal",
        access_count: int = 1,
        topic_stability: float = 1.0
    ) -> float:
        """
        计算衰减分数 (0-100, 越高越需要强化)
        
        因素:
        - 时间衰减
        - 重要性
        - 访问频率
        - 话题稳定性
        """
        # 基础衰减（指数衰减）
        base_decay = 100 * (1 - (1 - cls.BASE_DECAY_RATE) ** days_since_access)
        
        # 重要性调整
        importance_factor = cls.IMPORTANCE_MULTIPLIER.get(importance, 0.6)
        adjusted_decay = base_decay * importance_factor
        
        # 访问频率调整（多次访问降低衰减）
        frequency_factor = 1.0 / (1 + 0.1 * (access_count - 1))
        adjusted_decay *= frequency_factor
        
        # 话题稳定性（稳定话题衰减更慢）
        adjusted_decay *= (2.0 - topic_stability)
        
        return min(100, max(0, adjusted_decay))
    
    @classmethod
    def suggest_action(cls, decay_score: float) -> str:
        """根据衰减分数建议行动"""
        if decay_score >= 80:
            return "🔥 紧急强化"
        elif decay_score >= 60:
            return "⚠️ 需要强化"
        elif decay_score >= 40:
            return "📝 可选强化"
        else:
            return "✅ 状态良好"


class ForgetDetector:
    """增强版遗忘检测器"""
    
    def __init__(self):
        self.memory_dir = MEMORY_DIR
        self.decay = DecayCalculator()
        self._load_access_history()
    
    def _load_access_history(self):
        """加载访问历史"""
        history_file = self.memory_dir / ".access_history.json"
        if history_file.exists():
            try:
                self.access_history = json.loads(history_file.read_text())
            except:
                self.access_history = {}
        else:
            self.access_history = {}
    
    def _save_access_history(self):
        """保存访问历史"""
        history_file = self.memory_dir / ".access_history.json"
        try:
            history_file.write_text(json.dumps(self.access_history, ensure_ascii=False))
        except:
            pass
    
    def _record_access(self, memory_id: str):
        """记录访问"""
        if memory_id not in self.access_history:
            self.access_history[memory_id] = {
                "count": 0,
                "last_access": None,
                "access_times": []
            }
        
        self.access_history[memory_id]["count"] += 1
        self.access_history[memory_id]["last_access"] = datetime.now().isoformat()
        self.access_history[memory_id]["access_times"].append(datetime.now().isoformat())
        
        # 只保留最近100次访问
        if len(self.access_history[memory_id]["access_times"]) > 100:
            self.access_history[memory_id]["access_times"] = \
                self.access_history[memory_id]["access_times"][-100:]
        
        self._save_access_history()
    
    def analyze_memory(self, memory: Dict) -> Dict:
        """分析单条记忆的遗忘风险"""
        memory_id = memory.get("id", "unknown")
        content = memory.get("content", "")
        importance = memory.get("importance", "Normal")
        memory_type = memory.get("type", "info")
        
        # 访问历史
        history = self.access_history.get(memory_id, {"count": 0, "last_access": None})
        access_count = history["count"]
        last_access = history["last_access"]
        
        # 计算时间
        if last_access:
            last_access_dt = datetime.fromisoformat(last_access)
            days_since = (datetime.now() - last_access_dt).days
        else:
            days_since = 999  # 从未访问
        
        # 话题稳定性（基于内容hash变化频率）
        topic_stability = self._calculate_topic_stability(memory_id, content)
        
        # 计算衰减分数
        decay_score = self.decay.calculate_decay_score(
            days_since_access=days_since,
            importance=importance,
            access_count=access_count,
            topic_stability=topic_stability
        )
        
        return {
            "id": memory_id,
            "type": memory_type,
            "importance": importance,
            "decay_score": decay_score,
            "days_since_access": days_since,
            "access_count": access_count,
            "topic_stability": topic_stability,
            "action": self.decay.suggest_action(decay_score),
            "preview": content[:100] if content else ""
        }
    
    def _calculate_topic_stability(self, memory_id: str, content: str) -> float:
        """计算话题稳定性（0-1，越高越稳定）"""
        # 基于内容hash计算
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # 存储历史hash
        hash_file = self.memory_dir / ".content_hashes.json"
        if hash_file.exists():
            try:
                hashes = json.loads(hash_file.read_text())
            except:
                hashes = {}
        else:
            hashes = {}
        
        # 记录当前hash
        if memory_id not in hashes:
            hashes[memory_id] = []
        
        if memory_id in hashes and hashes[memory_id]:
            if hashes[memory_id][-1] != content_hash:
                # 内容变化了
                hashes[memory_id].append(content_hash)
                if len(hashes[memory_id]) > 10:
                    hashes[memory_id] = hashes[memory_id][-10:]
        else:
            hashes[memory_id] = [content_hash]
        
        try:
            hash_file.write_text(json.dumps(hashes, ensure_ascii=False))
        except:
            pass
        
        # 变化次数越多，稳定性越低
        changes = len(hashes.get(memory_id, [content_hash])) - 1
        return max(0.1, 1.0 - (changes * 0.15))
    
    def detect_contradictions(self, memories: List[Dict]) -> List[Dict]:
        """
        矛盾检测 - 借鉴kektordb
        找出内容冲突的记忆对
        """
        contradictions = []
        
        # 关键词冲突映射
        conflict_keywords = {
            ("喜欢", "讨厌"): 0.8,
            ("是", "不是"): 0.7,
            ("要", "不要"): 0.8,
            ("做", "不做"): 0.7,
            ("对", "错"): 0.6,
            ("真", "假"): 0.7,
            ("有", "没有"): 0.6,
        }
        
        # 简化版：按类型分组检测
        by_type = {}
        for mem in memories:
            mem_type = mem.get("type", "info")
            if mem_type not in by_type:
                by_type[mem_type] = []
            by_type[mem_type].append(mem)
        
        # 检测同一类型的矛盾
        for mem_type, mems in by_type.items():
            if len(mems) < 2:
                continue
            
            for i, mem1 in enumerate(mems):
                for mem2 in mems[i+1:]:
                    content1 = mem1.get("content", "")[:200].lower()
                    content2 = mem2.get("content", "")[:200].lower()
                    
                    # 检测关键词冲突
                    for (pos_kw, neg_kw), score in conflict_keywords.items():
                        if pos_kw in content1 and neg_kw in content2:
                            contradictions.append({
                                "memory1": mem1.get("id"),
                                "memory2": mem2.get("id"),
                                "type": "keyword_conflict",
                                "keywords": (pos_kw, neg_kw),
                                "severity": score,
                                "preview1": mem1.get("content", "")[:50],
                                "preview2": mem2.get("content", "")[:50]
                            })
                        elif neg_kw in content1 and pos_kw in content2:
                            contradictions.append({
                                "memory1": mem1.get("id"),
                                "memory2": mem2.get("id"),
                                "type": "keyword_conflict",
                                "keywords": (neg_kw, pos_kw),
                                "severity": score,
                                "preview1": mem1.get("content", "")[:50],
                                "preview2": mem2.get("content", "")[:50]
                            })
        
        return contradictions
    
    def analyze(self, memories: List[Dict] = None) -> Dict:
        """分析所有记忆的遗忘风险"""
        # 如果没有传入记忆列表，从.meta.json加载
        if memories is None:
            meta_file = self.memory_dir / ".meta.json"
            if meta_file.exists():
                try:
                    meta = json.loads(meta_file.read_text())
                    memories = meta.get("index", [])
                except:
                    memories = []
        
        # 分析每条记忆
        analyses = []
        for mem in memories:
            analysis = self.analyze_memory(mem)
            analyses.append(analysis)
        
        # 按衰减分数排序
        analyses.sort(key=lambda x: x["decay_score"], reverse=True)
        
        # 统计
        urgent = sum(1 for a in analyses if a["decay_score"] >= 80)
        warning = sum(1 for a in analyses if 60 <= a["decay_score"] < 80)
        optional = sum(1 for a in analyses if 40 <= a["decay_score"] < 60)
        good = sum(1 for a in analyses if a["decay_score"] < 40)
        
        # 矛盾检测
        contradictions = self.detect_contradictions(memories)
        
        return {
            "total": len(analyses),
            "urgent": urgent,
            "warning": warning,
            "optional": optional,
            "good": good,
            "contradictions": contradictions,
            "needs_attention": urgent + warning,
            "analyses": analyses[:50],  # 只返回前50个
            "summary": self._generate_summary(urgent, warning, optional, good, len(contradictions))
        }
    
    def _generate_summary(self, urgent, warning, optional, good, contradiction_count) -> str:
        """生成总结"""
        parts = []
        if urgent > 0:
            parts.append(f"🔥 {urgent}条需要紧急强化")
        if warning > 0:
            parts.append(f"⚠️ {warning}条需要强化")
        if contradiction_count > 0:
            parts.append(f"⚡ {contradiction_count}对矛盾")
        if not parts:
            parts.append("✅ 记忆状态良好")
        
        return " | ".join(parts)
    
    def suggest_reinforcement(self, memory_id: str) -> Dict:
        """建议如何强化记忆"""
        history = self.access_history.get(memory_id, {"count": 0})
        analysis = None
        
        # 找到对应的分析
        meta_file = self.memory_dir / ".meta.json"
        if meta_file.exists():
            try:
                meta = json.loads(meta_file.read_text())
                for mem in meta.get("index", []):
                    if mem.get("id") == memory_id:
                        analysis = self.analyze_memory(mem)
                        break
            except:
                pass
        
        if not analysis:
            return {"error": "Memory not found"}
        
        suggestions = []
        
        if analysis["decay_score"] >= 80:
            suggestions.append("🔴 立即强化：今天内复习这条记忆")
            suggestions.append("🔴 操作：找到这条记忆，重新阅读并确认")
        
        if analysis["access_count"] < 3:
            suggestions.append("📝 增加访问：未来几天多提及/查询相关内容")
        
        if analysis["days_since_access"] > 30:
            suggestions.append("📅 时间衰减：记忆已超过30天未访问")
            suggestions.append("💡 建议：将相关决策重新记录到MEMORY.md")
        
        return {
            "memory_id": memory_id,
            "analysis": analysis,
            "suggestions": suggestions
        }


def main():
    print("🧠 遗忘检测分析 v2.0.0")
    print("=" * 50)
    
    detector = ForgetDetector()
    result = detector.analyze()
    
    print(f"\n📊 分析结果:")
    print(f"   总记忆: {result['total']}")
    print(f"   🔥 紧急: {result['urgent']}")
    print(f"   ⚠️ 警告: {result['warning']}")
    print(f"   📝 可选: {result['optional']}")
    print(f"   ✅ 良好: {result['good']}")
    print(f"   ⚡ 矛盾: {len(result['contradictions'])}")
    
    print(f"\n📋 总结: {result['summary']}")
    
    # 显示需要关注的记忆
    if result['needs_attention'] > 0:
        print(f"\n🔍 需要关注的记忆 (Top 10):")
        for a in result["analyses"][:10]:
            if a["decay_score"] >= 40:
                print(f"\n   [{a['action']}] {a['id']}")
                print(f"   衰减: {a['decay_score']:.1f}% | 距上次访问: {a['days_since_access']}天 | 访问次数: {a['access_count']}")
                print(f"   预览: {a['preview'][:60]}...")
    
    # 显示矛盾
    if result["contradictions"]:
        print(f"\n⚡ 检测到的矛盾:")
        for c in result["contradictions"][:5]:
            print(f"   {c['memory1']} <-> {c['memory2']}")
            print(f"   关键词: {c['keywords']} | 严重度: {c['severity']}")
            print(f"   A: {c['preview1']}...")
            print(f"   B: {c['preview2']}...")


if __name__ == "__main__":
    main()
