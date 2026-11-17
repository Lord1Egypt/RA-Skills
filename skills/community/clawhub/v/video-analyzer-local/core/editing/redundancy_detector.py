"""冗余/废话片段检测器"""

import os
from typing import Any, Dict, List, Optional, Tuple

from ..logger import get_logger

logger = get_logger(__name__)


class RedundancyDetector:
    """
    检测视频中的冗余/废话片段。
    
    检测维度：
    1. 静音片段（长时间无语音）
    2. 重复内容（相似语音/画面）
    3. 语速异常（过慢/卡顿）
    4. 填充词（嗯、啊、那个、这个）
    5. 画面静止（长时间无变化）
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.editing_config = config.get("editing", {})
        self.redundancy_config = self.editing_config.get("redundancy", {})
        
        # 配置参数
        self.silence_threshold = self.redundancy_config.get("silence_threshold", 2.0)
        self.filler_threshold = self.redundancy_config.get("filler_threshold", 3)
        self.slow_speed_threshold = self.redundancy_config.get("slow_speed_threshold", 3.0)
        self.static_threshold = self.redundancy_config.get("static_threshold", 5.0)
    
    def detect(
        self,
        video_path: str,
        transcript: Dict = None,
        scenes: Dict = None,
    ) -> List[Dict]:
        """
        检测冗余片段。
        
        Args:
            video_path: 本地视频路径
            transcript: 语音识别结果
            scenes: 场景检测结果
            
        Returns:
            冗余片段列表
        """
        if not video_path or not os.path.exists(video_path):
            return []
        
        redundancies = []
        
        # 1. 静音片段检测
        silence_segments = self._detect_silence(transcript)
        redundancies.extend(silence_segments)
        
        # 2. 填充词检测
        filler_segments = self._detect_fillers(transcript)
        redundancies.extend(filler_segments)
        
        # 3. 语速异常检测
        speed_segments = self._detect_speed_anomaly(transcript)
        redundancies.extend(speed_segments)
        
        # 4. 画面静止检测
        static_segments = self._detect_static_frames(video_path)
        redundancies.extend(static_segments)
        
        # 5. 重复内容检测
        repeat_segments = self._detect_repetition(transcript)
        redundancies.extend(repeat_segments)
        
        # 合并重叠片段
        redundancies = self._merge_overlapping(redundancies)
        
        logger.info(f"检测到 {len(redundancies)} 个冗余片段")
        
        return redundancies
    
    def _detect_silence(self, transcript: Dict = None) -> List[Dict]:
        """检测静音片段"""
        segments = []
        
        if not transcript:
            return segments
        
        try:
            segs = transcript.get("segments", [])
            for i in range(len(segs) - 1):
                current_end = segs[i].get("end", 0)
                next_start = segs[i + 1].get("start", 0)
                gap = next_start - current_end
                
                if gap >= self.silence_threshold:
                    segments.append({
                        "start": round(current_end, 2),
                        "end": round(next_start, 2),
                        "duration": round(gap, 2),
                        "type": "静音片段",
                        "reason": f"静音 {gap:.1f} 秒",
                        "suggestion": "建议剪掉或加速",
                    })
            
            # 开头静音
            if segs and segs[0].get("start", 0) >= self.silence_threshold:
                segments.append({
                    "start": 0,
                    "end": round(segs[0].get("start", 0), 2),
                    "duration": round(segs[0].get("start", 0), 2),
                    "type": "开头静音",
                    "reason": f"开头静音 {segs[0].get('start', 0):.1f} 秒",
                    "suggestion": "建议剪掉",
                })
            
        except Exception as e:
            logger.debug(f"静音检测失败: {e}")
        
        return segments
    
    def _detect_fillers(self, transcript: Dict = None) -> List[Dict]:
        """检测填充词"""
        segments = []
        
        if not transcript:
            return segments
        
        try:
            # 中文填充词
            filler_words = [
                "嗯", "啊", "呃", "那个", "这个", "就是", "然后",
                "对吧", "是吧", "就是说", "那个那个", "啊啊",
            ]
            
            for seg in transcript.get("segments", []):
                text = seg.get("text", "")
                filler_count = sum(text.count(fw) for fw in filler_words)
                
                if filler_count >= self.filler_threshold:
                    segments.append({
                        "start": round(seg.get("start", 0), 2),
                        "end": round(seg.get("end", 0), 2),
                        "duration": round(seg.get("end", 0) - seg.get("start", 0), 2),
                        "type": "填充词过多",
                        "reason": f"检测到 {filler_count} 个填充词",
                        "suggestion": "建议剪掉或精简",
                    })
            
        except Exception as e:
            logger.debug(f"填充词检测失败: {e}")
        
        return segments
    
    def _detect_speed_anomaly(self, transcript: Dict = None) -> List[Dict]:
        """检测语速异常"""
        segments = []
        
        if not transcript:
            return segments
        
        try:
            for seg in transcript.get("segments", []):
                start = seg.get("start", 0)
                end = seg.get("end", 0)
                text = seg.get("text", "")
                
                duration = end - start
                if duration <= 0:
                    continue
                
                # 计算语速（字/秒）
                char_count = len(text.replace(" ", ""))
                speed = char_count / duration
                
                # 正常语速 4-8 字/秒
                if speed < self.slow_speed_threshold:
                    segments.append({
                        "start": round(start, 2),
                        "end": round(end, 2),
                        "duration": round(duration, 2),
                        "type": "语速过慢",
                        "reason": f"语速 {speed:.1f} 字/秒（正常 4-8）",
                        "suggestion": "建议加速或剪掉",
                    })
            
        except Exception as e:
            logger.debug(f"语速检测失败: {e}")
        
        return segments
    
    def _detect_static_frames(self, video_path: str) -> List[Dict]:
        """检测画面静止片段"""
        segments = []
        
        try:
            import cv2
            import numpy as np
            
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return segments
            
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            frame_interval = int(fps * 1)  # 每秒采样一次
            
            prev_frame = None
            frame_idx = 0
            static_start = None
            static_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_idx % frame_interval == 0:
                    timestamp = frame_idx / fps
                    
                    if prev_frame is not None:
                        diff = cv2.absdiff(prev_frame, frame)
                        mean_diff = np.mean(diff)
                        
                        if mean_diff < 5:  # 几乎无变化
                            if static_start is None:
                                static_start = timestamp
                            static_count += 1
                        else:
                            if static_start is not None and static_count >= self.static_threshold:
                                segments.append({
                                    "start": round(static_start, 2),
                                    "end": round(timestamp, 2),
                                    "duration": round(timestamp - static_start, 2),
                                    "type": "画面静止",
                                    "reason": f"画面静止 {static_count} 秒",
                                    "suggestion": "建议剪掉或加速",
                                })
                            static_start = None
                            static_count = 0
                    
                    prev_frame = frame
                
                frame_idx += 1
            
            cap.release()
            
            # 处理最后一段
            if static_start is not None and static_count >= self.static_threshold:
                segments.append({
                    "start": round(static_start, 2),
                    "end": round(frame_idx / fps, 2),
                    "duration": round(frame_idx / fps - static_start, 2),
                    "type": "画面静止",
                    "reason": f"画面静止 {static_count} 秒",
                    "suggestion": "建议剪掉或加速",
                })
            
        except Exception as e:
            logger.debug(f"画面静止检测失败: {e}")
        
        return segments
    
    def _detect_repetition(self, transcript: Dict = None) -> List[Dict]:
        """检测重复内容"""
        segments = []
        
        if not transcript:
            return segments
        
        try:
            segs = transcript.get("segments", [])
            
            for i in range(len(segs) - 1):
                text = segs[i].get("text", "").strip()
                next_text = segs[i + 1].get("text", "").strip()
                
                # 简单重复检测
                if text and text == next_text:
                    segments.append({
                        "start": round(segs[i].get("start", 0), 2),
                        "end": round(segs[i + 1].get("end", 0), 2),
                        "duration": round(segs[i + 1].get("end", 0) - segs[i].get("start", 0), 2),
                        "type": "重复内容",
                        "reason": f"重复: {text[:20]}...",
                        "suggestion": "建议删除重复部分",
                    })
            
        except Exception as e:
            logger.debug(f"重复检测失败: {e}")
        
        return segments
    
    def _merge_overlapping(self, segments: List[Dict]) -> List[Dict]:
        """合并重叠的冗余片段"""
        if not segments:
            return []
        
        # 按开始时间排序
        segments.sort(key=lambda x: x["start"])
        
        merged = [segments[0]]
        
        for seg in segments[1:]:
            last = merged[-1]
            
            if seg["start"] <= last["end"]:
                # 合并
                last["end"] = max(last["end"], seg["end"])
                last["duration"] = round(last["end"] - last["start"], 2)
                last["reason"] += f"; {seg['reason']}"
                last["type"] = "复合冗余"
            else:
                merged.append(seg)
        
        return merged
