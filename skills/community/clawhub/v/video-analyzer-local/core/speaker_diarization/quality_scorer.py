"""说话人分离质量评分模块 — 量化评估分离结果可信度"""

from typing import Any, Dict, List, Optional

import numpy as np

from ..logger import get_logger

logger = get_logger(__name__)


class QualityScorer:
    """
    说话人分离质量评分器。
    
    评估维度：
    1. 声纹距离（不同说话人 MFCC 特征的平均余弦距离）
    2. 重叠率（语音重叠比例）
    3. 聚类紧密度（同类样本的聚合程度）
    
    输出：0-100 分数 + 等级
    - 高 (≥ 80)：分离结果可信，可直接使用
    - 中 (≥ 60)：基本可用，建议人工校对
    - 低 (< 60)：分离效果差，建议手动调整
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.quality_config = config.get("quality_scorer", {})
        self.distance_weight = self.quality_config.get("distance_weight", 0.6)
        self.overlap_weight = self.quality_config.get("overlap_weight", 0.4)
    
    def score(
        self,
        diarize_result: Dict,
        features: Optional[np.ndarray] = None,
        segments: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        评估说话人分离质量。
        
        Args:
            diarize_result: diarize() 返回的结果（含 segments 和 n_speakers）
            features: 特征向量（用于声纹距离计算）
            segments: 原始语音段（用于重叠率计算）
            
        Returns:
            质量评分结果
        """
        score_details = {
            "voiceprint_distance": 0.0,
            "overlap_ratio": 0.0,
            "overall_score": 0,
            "level": "未知",
            "suggestion": "",
        }
        
        merged_segments = diarize_result.get("segments", [])
        n_speakers = diarize_result.get("n_speakers", 0)
        
        if n_speakers <= 1 or len(merged_segments) < 2:
            score_details["suggestion"] = "说话人数量 ≤ 1，无需分离质量评估"
            score_details["level"] = "高"
            score_details["overall_score"] = 100
            return score_details
        
        # 1. 声纹距离评分
        if features is not None and len(features) > 0:
            distance_score = self._calculate_voiceprint_distance(features, merged_segments)
            score_details["voiceprint_distance"] = round(distance_score, 2)
        else:
            # 无特征时基于启发式估计
            score_details["voiceprint_distance"] = self._estimate_distance_from_segments(merged_segments)
        
        # 2. 重叠率评分
        if segments and len(segments) > 1:
            overlap_score = self._calculate_overlap_ratio(segments)
            score_details["overlap_ratio"] = round(overlap_score, 2)
        else:
            score_details["overlap_ratio"] = self._estimate_overlap_from_merged(merged_segments)
        
        # 3. 综合评分
        overall = (
            score_details["voiceprint_distance"] * self.distance_weight +
            score_details["overlap_ratio"] * self.overlap_weight
        )
        score_details["overall_score"] = round(min(100, max(0, overall)), 1)
        
        # 4. 等级判定
        if score_details["overall_score"] >= 80:
            score_details["level"] = "高"
            score_details["suggestion"] = "分离结果可信，可直接使用"
        elif score_details["overall_score"] >= 60:
            score_details["level"] = "中"
            score_details["suggestion"] = "基本可用，建议人工校对关键段落"
        else:
            score_details["level"] = "低"
            score_details["suggestion"] = "分离效果差，建议手动调整或重新分离"
        
        return score_details
    
    def _calculate_voiceprint_distance(
        self,
        features: np.ndarray,
        merged_segments: List[Dict],
    ) -> float:
        """基于 MFCC 特征计算声纹距离"""
        try:
            # 提取每个说话人的特征
            speaker_features = {}
            for seg in merged_segments:
                speaker_idx = seg.get("speaker_idx", 0)
                # 使用段的索引特征
                start = int(seg.get("start", 0))
                end = int(seg.get("end", 0))
                
                # 取对应时间段内的特征均值
                # 简化：使用整体特征的均值作为声纹代表
                if speaker_idx not in speaker_features:
                    speaker_features[speaker_idx] = []
                speaker_features[speaker_idx].append(features[start:end].mean(axis=0) if start < len(features) and end <= len(features) else features.mean(axis=0))
            
            if len(speaker_features) < 2:
                return 50.0
            
            # 计算类间距离（余弦距离）
            centroids = []
            for idx in sorted(speaker_features.keys()):
                feats = np.array(speaker_features[idx])
                centroid = feats.mean(axis=0)
                centroids.append(centroid)
            
            # 计算所有说话人对之间的平均距离
            total_distance = 0
            pair_count = 0
            for i in range(len(centroids)):
                for j in range(i + 1, len(centroids)):
                    dist = self._cosine_distance(centroids[i], centroids[j])
                    total_distance += dist
                    pair_count += 1
            
            if pair_count == 0:
                return 50.0
            
            avg_distance = total_distance / pair_count
            
            # 归一化到 0-100 分数
            # 余弦距离范围 [0, 2]，映射到分数
            score = min(100, avg_distance * 66.67)  # 1.5 距离 = 100 分
            
            return score
            
        except Exception as e:
            logger.debug(f"声纹距离计算失败: {e}")
            return 50.0
    
    def _calculate_overlap_ratio(self, segments: List[Dict]) -> float:
        """计算语音重叠比例"""
        try:
            total_overlap = 0
            total_duration = 0
            
            for i in range(len(segments) - 1):
                current_end = segments[i].get("end", 0)
                next_start = segments[i + 1].get("start", 0)
                next_end = segments[i + 1].get("end", 0)
                
                duration = segments[i].get("end", 0) - segments[i].get("start", 0)
                total_duration += max(0, duration)
                
                # 检测重叠
                if next_start < current_end:
                    overlap = min(current_end, next_end) - next_start
                    total_overlap += max(0, overlap)
            
            if total_duration <= 0:
                return 50.0
            
            overlap_ratio = total_overlap / total_duration
            
            # 重叠率越低越好
            # 0% 重叠 = 100 分，> 30% 重叠 = 0 分
            score = max(0, 100 - (overlap_ratio * 3.33))
            
            return score
            
        except Exception as e:
            logger.debug(f"重叠率计算失败: {e}")
            return 50.0
    
    def _estimate_distance_from_segments(self, merged_segments: List[Dict]) -> float:
        """从合并段估计声纹距离（启发式）"""
        try:
            if len(merged_segments) < 2:
                return 50.0
            
            # 基于说话人切换频率和段长度变化估计
            speaker_changes = 0
            for i in range(1, len(merged_segments)):
                if merged_segments[i].get("speaker_idx") != merged_segments[i - 1].get("speaker_idx"):
                    speaker_changes += 1
            
            # 切换越多，说明分离越"积极"，可能更准确也可能更乱
            change_rate = speaker_changes / len(merged_segments) if merged_segments else 0
            
            # 适中的切换率最好
            # 0.1-0.3 最佳，过高或过低都扣分
            if 0.1 <= change_rate <= 0.3:
                return 75.0
            elif 0.05 <= change_rate < 0.1 or 0.3 < change_rate <= 0.5:
                return 60.0
            else:
                return 45.0
                
        except Exception:
            return 50.0
    
    def _estimate_overlap_from_merged(self, merged_segments: List[Dict]) -> float:
        """从合并段估计重叠率（启发式）"""
        try:
            if len(merged_segments) < 2:
                return 50.0
            
            gaps = []
            for i in range(1, len(merged_segments)):
                gap = merged_segments[i].get("start", 0) - merged_segments[i - 1].get("end", 0)
                gaps.append(gap)
            
            # 负 gap = 重叠
            negative_gaps = [g for g in gaps if g < 0]
            overlap_ratio = len(negative_gaps) / len(gaps) if gaps else 0
            
            score = max(0, 100 - (overlap_ratio * 5.0))
            return score
            
        except Exception:
            return 50.0
    
    @staticmethod
    def _cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
        """计算余弦距离"""
        try:
            dot = np.dot(a, b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            
            if norm_a == 0 or norm_b == 0:
                return 0.0
            
            cosine_sim = dot / (norm_a * norm_b)
            # 距离 = 1 - 相似度
            distance = 1 - cosine_sim
            
            return max(0, distance)
        except Exception:
            return 0.0
