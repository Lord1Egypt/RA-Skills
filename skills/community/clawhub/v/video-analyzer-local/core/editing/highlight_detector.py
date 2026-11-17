"""高光片段自动检测器"""

import os
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ..logger import get_logger

logger = get_logger(__name__)


class HighlightDetector:
    """
    自动检测视频中的高光片段。
    
    检测维度：
    1. 视觉活跃度（帧间差异）
    2. 音频能量（音量变化）
    3. 语音情感（激动/兴奋检测）
    4. 画面内容（人脸/动作检测）
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.editing_config = config.get("editing", {})
        self.highlight_config = self.editing_config.get("highlight", {})
        
        # 配置参数
        self.min_duration = self.highlight_config.get("min_duration", 2.0)
        self.max_duration = self.highlight_config.get("max_duration", 30.0)
        self.visual_weight = self.highlight_config.get("visual_weight", 0.3)
        self.audio_weight = self.highlight_config.get("audio_weight", 0.3)
        self.emotion_weight = self.highlight_config.get("emotion_weight", 0.2)
        self.content_weight = self.highlight_config.get("content_weight", 0.2)
        self.threshold = self.highlight_config.get("threshold", 0.6)
    
    def detect(
        self,
        video_path: str,
        transcript: Dict = None,
        scenes: Dict = None,
    ) -> List[Dict]:
        """
        检测视频中的高光片段。
        
        Args:
            video_path: 本地视频路径
            transcript: 语音识别结果（含情感标签）
            scenes: 场景检测结果
            
        Returns:
            高光片段列表，每个元素包含 start, end, score, type
        """
        if not video_path or not os.path.exists(video_path):
            return []
        
        highlights = []
        
        try:
            # 1. 视觉活跃度分析
            visual_scores = self._analyze_visual_activity(video_path)
            
            # 2. 音频能量分析
            audio_scores = self._analyze_audio_energy(video_path)
            
            # 3. 情感分析（从 transcript）
            emotion_scores = self._analyze_emotion(transcript)
            
            # 4. 内容分析（从 scenes）
            content_scores = self._analyze_content(scenes)
            
            # 5. 综合评分
            combined_scores = self._combine_scores(
                visual_scores, audio_scores, emotion_scores, content_scores
            )
            
            # 6. 提取高光片段
            highlights = self._extract_highlights(combined_scores, video_path)
            
            logger.info(f"检测到 {len(highlights)} 个高光片段")
            
        except Exception as e:
            logger.error(f"高光检测失败: {e}")
        
        return highlights
    
    def _analyze_visual_activity(self, video_path: str) -> List[Tuple[float, float]]:
        """
        分析视觉活跃度。
        
        Returns:
            [(timestamp, score), ...] 列表
        """
        scores = []
        
        try:
            import cv2
            
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return scores
            
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            frame_interval = int(fps * 0.5)  # 每0.5秒采样一次
            
            prev_frame = None
            frame_idx = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_idx % frame_interval == 0:
                    timestamp = frame_idx / fps
                    
                    if prev_frame is not None:
                        # 计算帧间差异
                        diff = cv2.absdiff(prev_frame, frame)
                        mean_diff = np.mean(diff)
                        # 归一化到 0-1
                        score = min(mean_diff / 50.0, 1.0)
                        scores.append((timestamp, score))
                    
                    prev_frame = frame
                
                frame_idx += 1
            
            cap.release()
            
        except Exception as e:
            logger.debug(f"视觉活跃度分析失败: {e}")
        
        return scores
    
    def _analyze_audio_energy(self, video_path: str) -> List[Tuple[float, float]]:
        """
        分析音频能量。
        
        Returns:
            [(timestamp, score), ...] 列表
        """
        scores = []
        
        try:
            import subprocess
            import json
            
            # 使用 ffmpeg 提取音频能量
            cmd = [
                "ffmpeg", "-i", video_path,
                "-af", "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level",
                "-f", "null", "-"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            # 解析输出（简化处理）
            lines = result.stderr.split("\n")
            timestamp = 0.0
            for line in lines:
                if "RMS_level" in line:
                    try:
                        value = float(line.split("=")[-1].strip())
                        # 归一化（假设范围 -60 到 0 dB）
                        score = max(0, min(1, (value + 60) / 60))
                        scores.append((timestamp, score))
                        timestamp += 0.5
                    except (ValueError, IndexError):
                        pass
            
        except Exception as e:
            logger.debug(f"音频能量分析失败: {e}")
        
        return scores
    
    def _analyze_emotion(self, transcript: Dict = None) -> List[Tuple[float, float]]:
        """
        分析语音情感（激动程度）。
        
        Returns:
            [(timestamp, score), ...] 列表
        """
        scores = []
        
        if not transcript:
            return scores
        
        try:
            for seg in transcript.get("segments", []):
                start = seg.get("start", 0)
                text = seg.get("text", "")
                
                # 激动关键词
                excited_keywords = [
                    "哇", "太棒了", "厉害", "牛", "绝了", "不可思议",
                    "震惊", "惊人", "太强了", "无敌", "完美", "精彩",
                ]
                
                # 计算激动程度
                excited_count = sum(1 for kw in excited_keywords if kw in text)
                score = min(excited_count * 0.3, 1.0)
                
                if score > 0:
                    scores.append((start, score))
                
        except Exception as e:
            logger.debug(f"情感分析失败: {e}")
        
        return scores
    
    def _analyze_content(self, scenes: Dict = None) -> List[Tuple[float, float]]:
        """
        分析画面内容（人脸/动作）。
        
        Returns:
            [(timestamp, score), ...] 列表
        """
        scores = []
        
        if not scenes:
            return scores
        
        try:
            for scene in scenes.get("scenes", []):
                start = scene.get("start", 0)
                objects = scene.get("objects", [])
                
                # 人脸检测得分
                face_count = sum(1 for obj in objects if obj.get("name") == "person")
                score = min(face_count * 0.2, 1.0)
                
                if score > 0:
                    scores.append((start, score))
                
        except Exception as e:
            logger.debug(f"内容分析失败: {e}")
        
        return scores
    
    def _combine_scores(
        self,
        visual: List[Tuple[float, float]],
        audio: List[Tuple[float, float]],
        emotion: List[Tuple[float, float]],
        content: List[Tuple[float, float]],
    ) -> List[Tuple[float, float]]:
        """
        综合各维度评分。
        
        Returns:
            [(timestamp, combined_score), ...] 列表
        """
        # 按时间戳合并所有分数
        all_timestamps = set()
        for scores in [visual, audio, emotion, content]:
            for ts, _ in scores:
                all_timestamps.add(ts)
        
        combined = []
        for ts in sorted(all_timestamps):
            v_score = self._get_score_at_timestamp(visual, ts)
            a_score = self._get_score_at_timestamp(audio, ts)
            e_score = self._get_score_at_timestamp(emotion, ts)
            c_score = self._get_score_at_timestamp(content, ts)
            
            total = (
                v_score * self.visual_weight +
                a_score * self.audio_weight +
                e_score * self.emotion_weight +
                c_score * self.content_weight
            )
            
            combined.append((ts, round(total, 3)))
        
        return combined
    
    def _get_score_at_timestamp(
        self, scores: List[Tuple[float, float]], timestamp: float, tolerance: float = 0.5
    ) -> float:
        """获取指定时间戳的分数"""
        for ts, score in scores:
            if abs(ts - timestamp) <= tolerance:
                return score
        return 0.0
    
    def _extract_highlights(
        self, combined_scores: List[Tuple[float, float]], video_path: str
    ) -> List[Dict]:
        """从综合评分中提取高光片段"""
        if not combined_scores:
            return []
        
        highlights = []
        current_start = None
        current_scores = []
        
        for ts, score in combined_scores:
            if score >= self.threshold:
                if current_start is None:
                    current_start = ts
                current_scores.append(score)
            else:
                if current_start is not None:
                    end = ts
                    duration = end - current_start
                    
                    if self.min_duration <= duration <= self.max_duration:
                        avg_score = sum(current_scores) / len(current_scores)
                        highlights.append({
                            "start": round(current_start, 2),
                            "end": round(end, 2),
                            "duration": round(duration, 2),
                            "score": round(avg_score, 3),
                            "type": self._classify_highlight(avg_score),
                        })
                    
                    current_start = None
                    current_scores = []
        
        # 处理最后一个片段
        if current_start is not None and current_scores:
            end = combined_scores[-1][0] if combined_scores else current_start + 5
            duration = end - current_start
            
            if self.min_duration <= duration <= self.max_duration:
                avg_score = sum(current_scores) / len(current_scores)
                highlights.append({
                    "start": round(current_start, 2),
                    "end": round(end, 2),
                    "duration": round(duration, 2),
                    "score": round(avg_score, 3),
                    "type": self._classify_highlight(avg_score),
                })
        
        # 按分数降序排序
        highlights.sort(key=lambda x: x["score"], reverse=True)
        
        return highlights
    
    def _classify_highlight(self, score: float) -> str:
        """分类高光类型"""
        if score >= 0.85:
            return "极强高光"
        elif score >= 0.7:
            return "强高光"
        elif score >= 0.6:
            return "中等高光"
        else:
            return "弱高光"
