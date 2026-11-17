"""场景检测模块 — 基于直方图差分 + 自适应阈值"""

import math
import os
from typing import Any, Dict, List, Tuple

import cv2
import numpy as np

from .logger import get_logger

logger = get_logger(__name__)


class SceneDetector:
    """视频场景边界检测器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.scene_config = config.get("scene_detection", {})
        self.threshold = self.scene_config.get("threshold", 0.5)
        self.min_scene_duration = self.scene_config.get("min_scene_duration", 2.0)
        self.hist_bins = self.scene_config.get("hist_bins", 50)
        self.color_space = self.scene_config.get("color_space", "hsv")
    
    def detect_scenes(self, video_path: str, frames_dir: str = None) -> Dict[str, Any]:
        """
        检测视频场景边界。
        
        Args:
            video_path: 视频文件路径
            frames_dir: 预提取帧目录（可选，不提供则直接从视频读取）
            
        Returns:
            场景检测结果
        """
        logger.info("开始场景检测...")
        
        # 获取帧列表
        if frames_dir and os.path.exists(frames_dir):
            frames = self._load_frames_from_dir(frames_dir)
        else:
            frames = self._extract_frames_from_video(video_path)
        
        if len(frames) < 2:
            logger.warning("帧数不足，无法检测场景")
            return {
                "scenes": [{"start": 0, "end": 0, "duration": 0, "keyframe_index": 0}],
                "total_scenes": 1,
                "avg_scene_duration": 0,
                "method": "histogram_diff",
            }
        
        # 计算帧间差异
        diffs = self._compute_frame_differences(frames)
        
        # 自适应阈值检测
        boundaries = self._detect_boundaries(diffs)
        
        # 合并短场景
        boundaries = self._merge_short_scenes(boundaries, len(frames))
        
        # 构建场景列表
        scenes = self._build_scenes(boundaries, len(frames))
        
        result = {
            "scenes": scenes,
            "total_scenes": len(scenes),
            "avg_scene_duration": sum(s["duration"] for s in scenes) / len(scenes) if scenes else 0,
            "frame_count": len(frames),
            "method": "histogram_diff",
            "config": {
                "threshold": self.threshold,
                "min_scene_duration": self.min_scene_duration,
                "color_space": self.color_space,
            },
        }
        
        logger.info(f"场景检测完成: {len(scenes)} 个场景")
        return result
    
    def _load_frames_from_dir(self, frames_dir: str) -> List[np.ndarray]:
        """从目录加载帧图像"""
        frames = []
        for fname in sorted(os.listdir(frames_dir)):
            if fname.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                path = os.path.join(frames_dir, fname)
                frame = cv2.imread(path)
                if frame is not None:
                    frames.append(frame)
        return frames
    
    def _extract_frames_from_video(self, video_path: str) -> List[np.ndarray]:
        """直接从视频文件提取帧"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"无法打开视频: {video_path}")
        
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        
        cap.release()
        return frames
    
    def _compute_frame_differences(self, frames: List[np.ndarray]) -> List[float]:
        """
        计算相邻帧之间的差异。
        使用 HSV 颜色直方图的巴卡系数（Bhattacharyya distance）。
        """
        diffs = []
        prev_hist = None
        
        for frame in frames:
            # 颜色空间转换
            if self.color_space == "hsv":
                converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                h_bins = self.hist_bins
                s_bins = self.hist_bins // 2
                hist = cv2.calcHist(
                    [converted], [0, 1], None,
                    [h_bins, s_bins],
                    [0, 180, 0, 256]
                )
            elif self.color_space == "rgb":
                converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                hist = cv2.calcHist(
                    [converted], [0, 1, 2], None,
                    [self.hist_bins // 2] * 3,
                    [0, 256, 0, 256, 0, 256]
                )
            else:  # lab
                converted = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
                hist = cv2.calcHist(
                    [converted], [0, 1], None,
                    [self.hist_bins, self.hist_bins // 2],
                    [0, 256, 0, 256]
                )
            
            # 归一化
            cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
            
            if prev_hist is not None:
                # 巴卡系数: 0=完全相同, 1=完全不同
                correlation = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA)
                diffs.append(correlation)
            
            prev_hist = hist
        
        return diffs
    
    def _detect_boundaries(self, diffs: List[float]) -> List[int]:
        """
        检测场景边界帧索引。
        使用自适应阈值（基于均值+标准差）。
        """
        if not diffs:
            return []
        
        # 计算统计量
        mean_diff = np.mean(diffs)
        std_diff = np.std(diffs)
        
        # 自适应阈值 = 均值 + k * 标准差
        adaptive_threshold = mean_diff + self.threshold * std_diff
        
        boundaries = []
        for i, diff in enumerate(diffs):
            if diff > adaptive_threshold:
                boundaries.append(i + 1)  # +1 表示差异在第 i 和 i+1 帧之间
        
        return boundaries
    
    def _merge_short_scenes(self, boundaries: List[int], total_frames: int) -> List[int]:
        """
        合并过短场景。
        场景时长低于 min_scene_duration 秒则合并到前一个场景。
        """
        if not boundaries:
            return []
        
        # 计算帧间隔（假设 1fps 采样）
        fps = 1  # 每秒 1 帧
        min_frames = int(self.min_scene_duration * fps)
        
        # 构建完整边界列表
        all_boundaries = [0] + sorted(boundaries) + [total_frames]
        
        merged = []
        last_kept = 0
        
        for i in range(1, len(all_boundaries)):
            scene_length = all_boundaries[i] - last_kept
            
            if scene_length >= min_frames:
                merged.append(all_boundaries[i])
                last_kept = all_boundaries[i]
            else:
                # 场景太短，跳过（合并到前一个）
                pass
        
        return merged
    
    def _build_scenes(self, boundaries: List[int], total_frames: int) -> List[Dict]:
        """
        构建场景信息列表。
        """
        all_boundaries = [0] + sorted(boundaries) + [total_frames]
        scenes = []
        
        for i in range(len(all_boundaries) - 1):
            start_frame = all_boundaries[i]
            end_frame = all_boundaries[i + 1]
            
            scenes.append({
                "index": i + 1,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "start_time": float(start_frame),  # 假设 1fps
                "end_time": float(end_frame),
                "duration": float(end_frame - start_frame),
                "keyframe_index": start_frame,  # 使用场景首帧作为关键帧
            })
        
        return scenes
