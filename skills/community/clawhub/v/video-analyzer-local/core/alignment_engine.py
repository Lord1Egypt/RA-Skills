"""时空对齐模块 — 音频↔场景↔时间戳的精准关联引擎"""

from typing import Any, Dict, List, Optional, Tuple

from .logger import get_logger

logger = get_logger(__name__)


class AlignmentEngine:
    """时空对齐引擎 - 统一不同模态数据到同一时间轴"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def align(
        self,
        transcript: Dict,
        scenes: Dict,
        visual_data: Dict,
        media_info: Dict,
    ) -> Dict:
        """
        将各模块数据按时间戳对齐，生成时空关联数据。
        
        Args:
            transcript: 语音识别结果
            scenes: 场景检测结果
            visual_data: 视觉分析结果
            media_info: 媒体元数据
            
        Returns:
            对齐后的多模态数据
        """
        logger.info("执行时空对齐...")
        
        # 对齐音频段落
        audio_alignments = self._align_transcript_to_scenes(
            transcript.get("segments", []),
            scenes.get("scenes", []),
        )
        
        # 对齐视觉数据
        visual_alignments = self._align_visual_to_scenes(
            visual_data.get("scenes", []),
            scenes.get("scenes", []),
        )
        
        # 构建统一时间轴
        timeline = self._build_timeline(
            transcript.get("segments", []),
            scenes.get("scenes", []),
            visual_alignments,
        )
        
        # 关联场景与对话
        scene_dialog_mapping = self._map_dialog_to_scenes(
            transcript.get("segments", []),
            scenes.get("scenes", []),
        )
        
        result = {
            "media_info": media_info,
            "audio_alignments": audio_alignments,
            "visual_alignments": visual_alignments,
            "timeline": timeline,
            "scene_dialog_mapping": scene_dialog_mapping,
        }
        
        logger.info(f"对齐完成: {len(timeline)} 个时间事件")
        return result
    
    def _align_transcript_to_scenes(
        self,
        segments: List[Dict],
        scene_list: List[Dict],
    ) -> List[List[Dict]]:
        """
        将语音段映射到所属场景。
        
        Args:
            segments: 语音段列表
            scene_list: 场景列表
            
        Returns:
            每个场景对应的语音段列表
        """
        # 初始化映射
        alignments = [[] for _ in range(len(scene_list))]
        
        for seg in segments:
            seg_start = seg.get("start", 0)
            seg_end = seg.get("end", 0)
            
            # 找到覆盖此语音段的主要场景
            best_scene_idx = self._find_best_scene(seg_start, seg_end, scene_list)
            
            if best_scene_idx is not None:
                alignments[best_scene_idx].append({
                    **seg,
                    "scene_index": scene_list[best_scene_idx].get("index", best_scene_idx + 1),
                })
            else:
                # 未找到匹配场景，放入最近的一个
                nearest = self._find_nearest_scene(seg_start, scene_list)
                if nearest is not None:
                    alignments[nearest].append({
                        **seg,
                        "scene_index": scene_list[nearest].get("index", nearest + 1),
                    })
        
        # 统计
        for i, segs in enumerate(alignments):
            if segs:
                logger.debug(f"场景 {i+1}: {len(segs)} 个语音段")
        
        return alignments
    
    def _align_visual_to_scenes(
        self,
        visual_scenes: List[Dict],
        scene_list: List[Dict],
    ) -> List[Dict]:
        """
        将视觉分析结果映射到场景列表。
        
        视觉分析结果按 scene_index 直接映射。
        """
        # 构建 scene_index 到视觉数据的快速索引
        visual_index = {}
        for vs in visual_scenes:
            idx = vs.get("scene_index", 0)
            visual_index[idx] = vs
        
        # 为每个场景查找对应的视觉数据
        alignments = []
        for scene in scene_list:
            idx = scene.get("index")
            visual = visual_index.get(idx, {})
            alignments.append({
                "scene_index": idx,
                "start_time": scene.get("start_time"),
                "end_time": scene.get("end_time"),
                "scene_types": visual.get("scene_types", []),
                "objects": visual.get("objects", []),
                "ocr_text": visual.get("ocr_text", ""),
            })
        
        return alignments
    
    def _build_timeline(
        self,
        segments: List[Dict],
        scene_list: List[Dict],
        visual_alignments: List[Dict],
    ) -> List[Dict]:
        """
        构建统一时间轴。
        
        将所有事件（场景开始、对话开始、视觉变化）按时间排序。
        """
        events = []
        
        # 添加场景事件
        for scene in scene_list:
            events.append({
                "time": scene.get("start_time", 0),
                "type": "scene_start",
                "scene_index": scene.get("index"),
                "duration": scene.get("duration"),
                "label": f"场景 {scene.get('index', '?')}",
            })
        
        # 添加语音事件
        for seg in segments:
            text = seg.get("text", "")
            events.append({
                "time": seg.get("start", 0),
                "type": "speech_start",
                "text_preview": text[:50] + "..." if len(text) > 50 else text,
                "segment_id": seg.get("id"),
                "label": "语音",
            })
            
            # 添加语音结束事件（用于计算静默期）
            events.append({
                "time": seg.get("end", 0),
                "type": "speech_end",
                "segment_id": seg.get("id"),
                "label": "语音结束",
            })
        
        # 按时间排序
        events.sort(key=lambda x: x["time"])
        
        # 添加序号
        for i, event in enumerate(events):
            event["sequence"] = i
        
        return events
    
    def _map_dialog_to_scenes(
        self,
        segments: List[Dict],
        scene_list: List[Dict],
    ) -> List[Dict]:
        """
        建立场景-对话映射关系。
        
        为每个场景生成：
        - 该场景内的完整对话文本
        - 对话时长占比
        - 平均置信度
        """
        mapping = []
        
        for scene in scene_list:
            scene_start = scene.get("start_time", 0)
            scene_end = scene.get("end_time", 0)
            
            # 找出所有落入该场景的对话
            scene_dialogs = []
            total_dialog_duration = 0
            total_confidence = 0
            count = 0
            
            for seg in segments:
                seg_start = seg.get("start", 0)
                seg_end = seg.get("end", 0)
                
                # 判断与场景的重叠
                overlap_start = max(seg_start, scene_start)
                overlap_end = min(seg_end, scene_end)
                
                if overlap_start < overlap_end:
                    # 有重叠
                    overlap_duration = overlap_end - overlap_start
                    scene_dialogs.append({
                        "text": seg.get("text", ""),
                        "start": seg_start,
                        "end": seg_end,
                        "overlap": overlap_duration,
                    })
                    total_dialog_duration += overlap_duration
                    total_confidence += seg.get("confidence", 0)
                    count += 1
            
            scene_duration = scene_end - scene_start
            
            mapping.append({
                "scene_index": scene.get("index"),
                "start_time": scene_start,
                "end_time": scene_end,
                "dialogs": scene_dialogs,
                "dialog_text": " ".join(d["text"] for d in scene_dialogs),
                "dialog_duration": total_dialog_duration,
                "dialog_coverage": (
                    total_dialog_duration / scene_duration
                    if scene_duration > 0 else 0
                ),
                "avg_confidence": (
                    total_confidence / count if count > 0 else 0
                ),
                "is_silent": len(scene_dialogs) == 0,
            })
        
        return mapping
    
    def _find_best_scene(
        self,
        seg_start: float,
        seg_end: float,
        scene_list: List[Dict],
    ) -> Optional[int]:
        """
        找到覆盖对话段的最佳场景。
        
        策略：计算对话与每个场景的时间重叠，选重叠最大的场景。
        """
        best_idx = None
        best_overlap = 0
        
        for i, scene in enumerate(scene_list):
            scene_start = scene.get("start_time", 0)
            scene_end = scene.get("end_time", 0)
            
            # 计算重叠
            overlap_start = max(seg_start, scene_start)
            overlap_end = min(seg_end, scene_end)
            overlap = overlap_end - overlap_start
            
            if overlap > best_overlap:
                best_overlap = overlap
                best_idx = i
        
        return best_idx
    
    def _find_nearest_scene(
        self,
        timestamp: float,
        scene_list: List[Dict],
    ) -> Optional[int]:
        """找到离给定时间戳最近的场景"""
        best_idx = None
        best_dist = float("inf")
        
        for i, scene in enumerate(scene_list):
            center = (scene.get("start_time", 0) + scene.get("end_time", 0)) / 2
            dist = abs(timestamp - center)
            if dist < best_dist:
                best_dist = dist
                best_idx = i
        
        return best_idx
