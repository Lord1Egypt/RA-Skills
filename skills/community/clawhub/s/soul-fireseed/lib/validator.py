#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
lib/validator.py
火种·灵魂 v2.0 - 置信度校验器

基于贝叶斯更新机制校准化石置信度，检测矛盾化石。
"""

import json
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
from pathlib import Path

try:
    from .extractor import Fossil
except ImportError:
    from extractor import Fossil


class ConfidenceValidator:
    """
    置信度校验器
    
    功能:
    - 校准提取器的置信度评分
    - 检测化石间的一致性
    - 标记矛盾或低质量化石
    - 维护历史准确率记录
    
    使用示例:
        >>> validator = ConfidenceValidator()
        >>> result = validator.validate(fossil, context_fossils)
        >>> print(result['calibrated_confidence'])
    """
    
    def __init__(self, history_db: Optional[str] = None,
                historical_window: int = 100):
        """
        初始化校验器
        
        参数:
            history_db: 历史数据库路径（可选）
            historical_window: 历史准确率窗口大小
        """
        self.historical_window = historical_window
        self.history_db = Path(history_db) if history_db else None
        
        # 历史准确率追踪 {dimension: [accuracies]}
        self.accuracy_history: Dict[int, List[float]] = defaultdict(list)
        
        # 加载历史数据
        if self.history_db and self.history_db.exists():
            self._load_history()
    
    def validate(self, fossil: Fossil, context: List[Fossil] = None) -> Dict:
        """
        验证化石的可信度
        
        参数:
            fossil: 待验证的化石
            context: 相关历史化石列表
            
        返回:
            验证结果字典，包含:
            - calibrated_confidence: 校准后的置信度
            - consistency_score: 一致性评分
            - has_contradiction: 是否存在矛盾
            - recommendations: 建议列表
        """
        result = {
            "original_confidence": fossil.confidence,
            "calibrated_confidence": fossil.confidence,
            "consistency_score": 1.0,
            "has_contradiction": False,
            "recommendations": []
        }
        
        # 1. 基于历史准确率校准
        historical_accuracy = self._get_historical_accuracy(fossil.dimension)
        calibrated_conf = fossil.confidence * historical_accuracy
        result["calibrated_confidence"] = min(1.0, calibrated_conf)
        
        # 2. 一致性检查
        if context:
            consistency = self._check_consistency(fossil, context)
            result["consistency_score"] = consistency
            
            # 调整置信度
            if consistency < 0.5:
                result["calibrated_confidence"] *= 0.8
                result["recommendations"].append("与历史化石一致性较低，建议人工审核")
        
        # 3. 矛盾检测
        contradictions = self._detect_contradictions(fossil, context or [])
        if contradictions:
            result["has_contradiction"] = True
            result["calibrated_confidence"] *= 0.6
            result["recommendations"].append(f"检测到{len(contradictions)}个矛盾化石")
            
            for contra_fossil in contradictions:
                result["recommendations"].append(
                    f"与化石 {contra_fossil.id} 存在矛盾"
                )
        
        # 4. 更新历史记录
        self._update_history(fossil.dimension, result["calibrated_confidence"])
        
        return result
    
    def detect_contradiction(self, fossil1: Fossil, fossil2: Fossil) -> bool:
        """
        检测两个化石是否矛盾
        
        参数:
            fossil1: 化石1
            fossil2: 化石2
            
        返回:
            是否矛盾
        """
        # 同一维度但内容相反
        if fossil1.dimension != fossil2.dimension:
            return False
        
        # 简单的关键词矛盾检测
        contradiction_pairs = [
            ("喜欢", "讨厌"),
            ("高", "低"),
            ("积极", "消极"),
            ("开放", "保守"),
            ("冒险", "谨慎"),
        ]
        
        content1 = fossil1.content.lower()
        content2 = fossil2.content.lower()
        
        for word1, word2 in contradiction_pairs:
            if word1 in content1 and word2 in content2:
                return True
            if word2 in content1 and word1 in content2:
                return True
        
        return False
    
    def adjust_confidence(self, original_confidence: float, 
                         historical_accuracy: float,
                         consistency: float = 1.0) -> float:
        """
        根据历史准确率和一致性调整置信度
        
        参数:
            original_confidence: 原始置信度
            historical_accuracy: 历史准确率
            consistency: 一致性系数
            
        返回:
            调整后的置信度
        """
        adjusted = original_confidence * historical_accuracy * consistency
        return min(1.0, max(0.0, adjusted))
    
    def get_accuracy_history(self, dimension: int) -> List[float]:
        """获取指定维度的准确率历史"""
        return self.accuracy_history.get(dimension, [])
    
    def _get_historical_accuracy(self, dimension: int) -> float:
        """获取维度的平均历史准确率"""
        accuracies = self.accuracy_history.get(dimension, [])
        if not accuracies:
            return 1.0  # 无历史数据时返回默认值
        
        # 取最近 N 次的平均
        recent = accuracies[-self.historical_window:]
        return sum(recent) / len(recent)
    
    def _check_consistency(self, fossil: Fossil, context: List[Fossil]) -> float:
        """
        检查化石与上下文的一致性
        
        返回:
            一致性评分 (0.0 - 1.0)
        """
        same_dim_fossils = [f for f in context if f.dimension == fossil.dimension]
        
        if not same_dim_fossils:
            return 1.0  # 无上下文，默认一致
        
        # 计算相似度（简化版：基于标签重叠）
        similarities = []
        for other in same_dim_fossils:
            # Jaccard 相似度
            tags1 = set(fossil.tags)
            tags2 = set(other.tags)
            
            if not tags1 or not tags2:
                similarities.append(0.5)
                continue
            
            intersection = len(tags1 & tags2)
            union = len(tags1 | tags2)
            jaccard = intersection / union if union > 0 else 0
            
            similarities.append(jaccard)
        
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0.5
        return avg_similarity
    
    def _detect_contradictions(self, fossil: Fossil, 
                              context: List[Fossil]) -> List[Fossil]:
        """检测与给定化石矛盾的历史化石"""
        same_dim_fossils = [f for f in context if f.dimension == fossil.dimension]
        contradictions = []
        
        for other in same_dim_fossils:
            if self.detect_contradiction(fossil, other):
                contradictions.append(other)
        
        return contradictions
    
    def _update_history(self, dimension: int, confidence: float):
        """更新历史准确率记录"""
        self.accuracy_history[dimension].append(confidence)
        
        # 保持窗口大小
        if len(self.accuracy_history[dimension]) > self.historical_window * 2:
            self.accuracy_history[dimension] = \
                self.accuracy_history[dimension][-self.historical_window:]
        
        # 定期保存
        if self.history_db and len(self.accuracy_history[dimension]) % 10 == 0:
            self._save_history()
    
    def _load_history(self):
        """从磁盘加载历史数据"""
        try:
            with open(self.history_db, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for dim_str, accuracies in data.items():
                    self.accuracy_history[int(dim_str)] = accuracies
        except Exception as e:
            print(f"加载历史数据失败: {e}")
    
    def _save_history(self):
        """保存历史数据到磁盘"""
        try:
            self.history_db.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_db, 'w', encoding='utf-8') as f:
                json.dump(dict(self.accuracy_history), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史数据失败: {e}")
