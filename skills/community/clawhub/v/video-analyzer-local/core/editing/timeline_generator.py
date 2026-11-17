"""剪辑时间线生成器"""

from typing import Any, Dict, List, Optional

from ..logger import get_logger

logger = get_logger(__name__)


class TimelineGenerator:
    """
    基于高光检测和冗余检测结果，生成优化剪辑时间线。
    
    功能：
    1. 自动排列高光片段
    2. 跳过冗余片段
    3. 生成剪辑顺序
    4. 计算总时长
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.editing_config = config.get("editing", {})
        self.timeline_config = self.editing_config.get("timeline", {})
        
        self.max_output_duration = self.timeline_config.get("max_output_duration", 120)
        self.min_clip_duration = self.timeline_config.get("min_clip_duration", 1.0)
        self.transition_duration = self.timeline_config.get("transition_duration", 0.5)
    
    def generate(
        self,
        highlights: List[Dict],
        redundancies: List[Dict],
        original_duration: float,
    ) -> Dict:
        """
        生成剪辑时间线。
        
        Args:
            highlights: 高光片段列表
            redundancies: 冗余片段列表
            original_duration: 原始视频时长
            
        Returns:
            剪辑时间线字典
        """
        if not highlights:
            return {
                "clips": [],
                "total_duration": 0,
                "original_duration": original_duration,
                "compression_ratio": 0,
                "transition_count": 0,
            }
        
        # 1. 过滤掉冗余片段中的高光
        filtered_highlights = self._filter_redundant_highlights(
            highlights, redundancies
        )
        
        # 2. 按原始顺序排列
        sorted_clips = sorted(filtered_highlights, key=lambda x: x["start"])
        
        # 3. 应用时长限制
        final_clips = self._apply_duration_limit(sorted_clips)
        
        # 4. 生成时间线
        timeline = self._build_timeline(final_clips, original_duration)
        
        logger.info(
            f"生成时间线: {len(timeline['clips'])} 个片段, "
            f"总时长 {timeline['total_duration']:.1f}s"
        )
        
        return timeline
    
    def _filter_redundant_highlights(
        self, highlights: List[Dict], redundancies: List[Dict]
    ) -> List[Dict]:
        """过滤掉与冗余片段重叠的高光"""
        if not redundancies:
            return highlights
        
        filtered = []
        
        for hl in highlights:
            hl_start = hl["start"]
            hl_end = hl["end"]
            
            # 检查是否与冗余片段重叠
            is_redundant = False
            for red in redundancies:
                # 计算重叠
                overlap_start = max(hl_start, red["start"])
                overlap_end = min(hl_end, red["end"])
                
                if overlap_start < overlap_end:
                    overlap_duration = overlap_end - overlap_start
                    hl_duration = hl_end - hl_start
                    
                    # 如果重叠超过 50%，认为是冗余
                    if overlap_duration > hl_duration * 0.5:
                        is_redundant = True
                        break
            
            if not is_redundant:
                filtered.append(hl)
        
        return filtered
    
    def _apply_duration_limit(self, clips: List[Dict]) -> List[Dict]:
        """应用时长限制"""
        if not clips:
            return []
        
        # 按分数降序，取满足时长限制的片段
        sorted_by_score = sorted(clips, key=lambda x: x["score"], reverse=True)
        
        selected = []
        total_duration = 0
        
        for clip in sorted_by_score:
            clip_duration = clip["end"] - clip["start"]
            
            if total_duration + clip_duration <= self.max_output_duration:
                selected.append(clip)
                total_duration += clip_duration
        
        # 按原始顺序排列
        selected.sort(key=lambda x: x["start"])
        
        return selected
    
    def _build_timeline(
        self, clips: List[Dict], original_duration: float
    ) -> Dict:
        """构建时间线"""
        if not clips:
            return {
                "clips": [],
                "total_duration": 0,
                "original_duration": original_duration,
                "compression_ratio": 0,
                "transition_count": 0,
            }
        
        timeline_clips = []
        total_duration = 0
        
        for i, clip in enumerate(clips):
            duration = clip["end"] - clip["start"]
            
            timeline_clip = {
                "index": i + 1,
                "source_start": clip["start"],
                "source_end": clip["end"],
                "output_start": round(total_duration, 2),
                "output_end": round(total_duration + duration, 2),
                "duration": round(duration, 2),
                "score": clip.get("score", 0),
                "type": clip.get("type", "highlight"),
            }
            
            timeline_clips.append(timeline_clip)
            total_duration += duration
            
            # 添加转场
            if i < len(clips) - 1:
                total_duration += self.transition_duration
        
        compression_ratio = total_duration / original_duration if original_duration > 0 else 0
        
        return {
            "clips": timeline_clips,
            "total_duration": round(total_duration, 2),
            "original_duration": round(original_duration, 2),
            "compression_ratio": round(compression_ratio, 2),
            "transition_count": len(clips) - 1,
        }
    
    def suggest_output_duration(self, original_duration: float, platform: str = "douyin") -> float:
        """
        建议输出时长。
        
        Args:
            original_duration: 原始时长
            platform: 目标平台
            
        Returns:
            建议输出时长（秒）
        """
        platform_limits = {
            "douyin": 60,
            "kuaishou": 60,
            "bilibili": 180,
            "wechat_video": 60,
        }
        
        max_duration = platform_limits.get(platform, 60)
        
        if original_duration <= max_duration:
            return original_duration
        
        # 建议压缩到平台限制
        return max_duration
