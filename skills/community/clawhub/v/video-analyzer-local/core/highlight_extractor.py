"""精华提取模块 — 高光检测 + 节奏分析 + 摘要生成"""

import math
from typing import Any, Dict, List

from .logger import get_logger

logger = get_logger(__name__)


class HighlightExtractor:
    """视频精华提取器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.highlight_config = config.get("highlight", {})
        self.sensitivity = self.highlight_config.get("sensitivity", 0.6)
        self.top_n = self.highlight_config.get("top_n", 10)
        self.min_duration = self.highlight_config.get("min_highlight_duration", 5)
        self.audio_weight = self.highlight_config.get("audio_weight", 0.5)
        self.visual_weight = self.highlight_config.get("visual_weight", 0.5)
    
    def extract(self, fused_data: Dict) -> List[Dict]:
        """
        从融合数据中提取精华片段。
        
        Args:
            fused_data: 融合后的多模态数据
            
        Returns:
            精华片段列表
        """
        logger.info("提取精华片段...")
        
        scenes = fused_data.get("scenes", [])
        metrics = fused_data.get("metrics", {})
        
        if not scenes:
            return []
        
        # 计算每个场景的精华分数
        scored_scenes = self._score_scenes(scenes)
        
        # 提取高光时刻
        highlights = self._extract_highlights(scored_scenes)
        
        # 分析节奏
        rhythm = self._analyze_rhythm(scenes)
        
        # 构建结果
        result = {
            "highlights": highlights,
            "rhythm_analysis": rhythm,
            "total_highlights": len(highlights),
            "total_highlight_duration": sum(h["duration"] for h in highlights),
        }
        
        logger.info(f"精华提取完成: {len(highlights)} 个片段")
        
        return result
    
    def _score_scenes(self, scenes: List[Dict]) -> List[Dict]:
        """
        为每个场景计算精华分数。
        
        考虑：
        - 对话密度（高密度 = 高信息量）
        - 视觉复杂度（物体数量、OCR 文字）
        - 情感强度（基于语速和音量变化）
        - 场景切换频率（切换多 = 节奏快）
        """
        scored = []
        
        for scene in scenes:
            score = 0.0
            content = scene.get("content", {})
            scene_metrics = scene.get("metrics", {})
            
            # 1. 对话密度分数 (0-40)
            dialog_coverage = scene_metrics.get("dialog_coverage", 0)
            score += dialog_coverage * 40
            
            # 2. 视觉复杂度分数 (0-30)
            object_count = scene_metrics.get("object_count", 0)
            visual_score = min(object_count * 5, 20)
            if content.get("ocr_text"):
                visual_score += 10
            score += visual_score
            
            # 3. 识别置信度分数 (0-15)
            confidence = scene_metrics.get("avg_confidence", 0)
            score += confidence * 15
            
            # 4. 场景类型加分 (0-15)
            scene_types = content.get("scene_types", [])
            if "outdoor" in scene_types or "nature" in scene_types:
                score += 10
            if "urban" in scene_types or "street" in scene_types:
                score += 8
            
            scored.append({
                **scene,
                "highlight_score": round(min(score, 100), 2),
            })
        
        return scored
    
    def _extract_highlights(self, scored_scenes: List[Dict]) -> List[Dict]:
        """
        从评分场景中提取 Top-N 精华片段。
        """
        # 按分数排序
        sorted_scenes = sorted(scored_scenes, key=lambda x: x.get("highlight_score", 0), reverse=True)
        
        # 取 Top-N
        top_scenes = sorted_scenes[:self.top_n]
        
        # 按时间排序
        top_scenes.sort(key=lambda x: x.get("time_range", {}).get("start", 0))
        
        highlights = []
        for scene in top_scenes:
            time_range = scene.get("time_range", {})
            duration = time_range.get("duration", 0)
            
            # 过滤太短的片段
            if duration < self.min_duration:
                continue
            
            highlights.append({
                "scene_index": scene.get("index"),
                "start_time": time_range.get("start"),
                "end_time": time_range.get("end"),
                "duration": round(duration, 2),
                "score": scene.get("highlight_score"),
                "text_preview": scene.get("content", {}).get("dialog", "")[:100],
                "tags": scene.get("semantic_tags", []),
                "objects": scene.get("content", {}).get("objects", []),
            })
        
        return highlights
    
    def _analyze_rhythm(self, scenes: List[Dict]) -> Dict:
        """
        分析视频节奏。
        
        基于：
        - 场景切换频率
        - 对话密度变化
        - 视觉复杂度变化
        """
        if not scenes:
            return {}
        
        # 计算场景时长分布
        durations = [s.get("time_range", {}).get("duration", 0) for s in scenes]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # 计算对话密度变化
        densities = [s.get("metrics", {}).get("dialog_coverage", 0) for s in scenes]
        avg_density = sum(densities) / len(densities) if densities else 0
        
        # 计算视觉复杂度变化
        complexities = [s.get("metrics", {}).get("object_count", 0) for s in scenes]
        avg_complexity = sum(complexities) / len(complexities) if complexities else 0
        
        # 节奏分类
        rhythm_type = self._classify_rhythm(avg_duration, avg_density, avg_complexity)
        
        return {
            "avg_scene_duration": round(avg_duration, 2),
            "avg_dialog_density": round(avg_density, 4),
            "avg_visual_complexity": round(avg_complexity, 2),
            "rhythm_type": rhythm_type,
            "scene_durations": durations,
            "dialog_densities": densities,
        }
    
    def _classify_rhythm(self, avg_duration: float, avg_density: float, avg_complexity: float) -> str:
        """分类视频节奏类型"""
        if avg_duration < 5:
            if avg_density > 0.7:
                return "快节奏-对话密集"
            else:
                return "快节奏-视觉驱动"
        elif avg_duration < 15:
            if avg_density > 0.7:
                return "中等节奏-对话为主"
            else:
                return "中等节奏-平衡"
        else:
            if avg_density > 0.7:
                return "慢节奏-深度对话"
            else:
                return "慢节奏-画面为主"
