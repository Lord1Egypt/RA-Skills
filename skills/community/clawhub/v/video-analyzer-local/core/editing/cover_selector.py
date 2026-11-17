"""封面帧智能选取器 — 对场景切分候选帧评分，输出 Top3 PNG 并附理由"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ..logger import get_logger

logger = get_logger(__name__)


class CoverSelector:
    """
    封面帧智能选取器。

    评分维度：
    1. Laplacian 锐度（清晰度）
    2. 人脸数量与位置（居中优先）
    3. 三分法构图评分
    4. 亮度适中（避免过曝/欠曝）

    输出：Top3 候选帧（PNG）+ 评分理由
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.editing_config = config.get("editing", {})
        self.cover_config = self.editing_config.get("cover", {})

        # 配置参数
        self.ffmpeg_path = self.cover_config.get("ffmpeg_path", "ffmpeg")
        self.ffprobe_path = self.cover_config.get("ffprobe_path", "ffprobe")
        self.output_dir = self.cover_config.get("output_dir", "output/covers")
        self.temp_dir = self.cover_config.get("temp_dir", ".temp/covers")

        # 评分权重
        self.sharpness_weight = self.cover_config.get("sharpness_weight", 0.35)
        self.face_weight = self.cover_config.get("face_weight", 0.30)
        self.composition_weight = self.cover_config.get("composition_weight", 0.20)
        self.brightness_weight = self.cover_config.get("brightness_weight", 0.15)

        # 候选帧提取间隔（秒）
        self.sample_interval = self.cover_config.get("sample_interval", 2.0)

        # 确保目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

    def select(
        self,
        video_path: str,
        scenes: Optional[List[Dict]] = None,
        top_n: int = 3,
    ) -> Dict[str, Any]:
        """
        选取最佳封面帧。

        Args:
            video_path: 视频文件路径
            scenes: 场景边界列表 [{start, end, ...}, ...]
            top_n: 返回前 N 个候选帧

        Returns:
            {
                "candidates": [
                    {
                        "path": "帧路径",
                        "timestamp": 时间戳,
                        "score": 总分,
                        "scores": {"sharpness": ..., "face": ..., "composition": ..., "brightness": ...},
                        "reasons": ["理由1", "理由2"],
                    },
                    ...
                ],
                "total_candidates": 总候选数,
            }
        """
        result = {
            "candidates": [],
            "total_candidates": 0,
        }

        if not video_path or not os.path.exists(video_path):
            logger.error(f"视频文件不存在: {video_path}")
            return result

        # 获取视频时长
        duration = self._get_video_duration(video_path)
        if duration <= 0:
            logger.error("无法获取视频时长")
            return result

        # 提取候选帧
        candidate_frames = self._extract_candidate_frames(video_path, scenes, duration)
        if not candidate_frames:
            logger.warning("未提取到候选帧")
            return result

        result["total_candidates"] = len(candidate_frames)

        # 评分每个候选帧
        scored_frames = []
        for frame_path, timestamp in candidate_frames:
            scores = self._score_frame(frame_path)
            total_score = (
                scores["sharpness"] * self.sharpness_weight
                + scores["face"] * self.face_weight
                + scores["composition"] * self.composition_weight
                + scores["brightness"] * self.brightness_weight
            )
            reasons = self._generate_reasons(scores)
            scored_frames.append({
                "path": frame_path,
                "timestamp": timestamp,
                "score": round(total_score, 4),
                "scores": scores,
                "reasons": reasons,
            })

        # 按总分降序排序
        scored_frames.sort(key=lambda x: x["score"], reverse=True)

        # 取 TopN
        result["candidates"] = scored_frames[:top_n]

        # 复制 TopN 到输出目录
        for i, candidate in enumerate(result["candidates"]):
            src = candidate["path"]
            if src and os.path.exists(src):
                dest_name = f"cover_top{i+1}_{candidate['timestamp']:.1f}s.png"
                dest_path = os.path.join(self.output_dir, dest_name)
                import shutil
                shutil.copy2(src, dest_path)
                candidate["path"] = dest_path

        logger.info(f"封面帧选取完成，从 {len(candidate_frames)} 个候选中选出 Top{top_n}")
        return result

    def _extract_candidate_frames(
        self,
        video_path: str,
        scenes: Optional[List[Dict]],
        duration: float,
    ) -> List[Tuple[str, float]]:
        """从视频中提取候选帧"""
        frames = []

        try:
            # 确定采样时间点
            if scenes:
                # 从每个场景的中间帧采样
                timestamps = []
                for scene in scenes:
                    start = scene.get("start", 0)
                    end = scene.get("end", duration)
                    mid = (start + end) / 2
                    timestamps.append(mid)
                    # 场景开始处也采样
                    timestamps.append(start + 0.5)
            else:
                # 均匀采样
                timestamps = []
                t = 1.0  # 跳过开头 1 秒
                while t < duration - 1.0:
                    timestamps.append(t)
                    t += self.sample_interval

            # 提取帧
            for ts in timestamps:
                if ts >= duration:
                    continue
                frame_path = os.path.join(
                    self.temp_dir,
                    f"frame_{ts:.2f}.png",
                )
                success = self._extract_frame_at(video_path, ts, frame_path)
                if success and os.path.exists(frame_path):
                    frames.append((frame_path, ts))

        except Exception as e:
            logger.error(f"提取候选帧失败: {e}")

        return frames

    def _extract_frame_at(
        self, video_path: str, timestamp: float, output_path: str
    ) -> bool:
        """提取指定时间戳的帧"""
        try:
            import subprocess
            cmd = [
                self.ffmpeg_path, "-y",
                "-ss", str(timestamp),
                "-i", video_path,
                "-vframes", "1",
                "-q:v", "2",
                output_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.returncode == 0 and os.path.exists(output_path)
        except Exception as e:
            logger.debug(f"提取帧失败: {e}")
            return False

    def _score_frame(self, frame_path: str) -> Dict[str, float]:
        """对单帧进行多维度评分"""
        scores = {
            "sharpness": 0.0,
            "face": 0.0,
            "composition": 0.0,
            "brightness": 0.0,
        }

        try:
            import cv2

            img = cv2.imread(frame_path)
            if img is None:
                return scores

            h, w = img.shape[:2]

            # 1. Laplacian 锐度
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            lap = cv2.Laplacian(gray, cv2.CV_64F)
            scores["sharpness"] = min(lap.var() / 500.0, 1.0)

            # 2. 人脸检测
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            if len(faces) > 0:
                # 人脸数量得分
                face_count_score = min(len(faces) * 0.3, 1.0)

                # 人脸居中得分
                center_x, center_y = w / 2, h / 2
                center_scores = []
                for (fx, fy, fw, fh) in faces:
                    face_center_x = fx + fw / 2
                    face_center_y = fy + fh / 2
                    dist = np.sqrt(
                        (face_center_x - center_x) ** 2
                        + (face_center_y - center_y) ** 2
                    )
                    max_dist = np.sqrt(center_x ** 2 + center_y ** 2)
                    center_scores.append(1.0 - dist / max_dist)

                avg_center = sum(center_scores) / len(center_scores)
                scores["face"] = (face_count_score + avg_center) / 2
            else:
                scores["face"] = 0.1  # 无人脸也给少量分

            # 3. 三分法构图
            scores["composition"] = self._score_rule_of_thirds(gray, w, h)

            # 4. 亮度适中
            mean_brightness = np.mean(gray)
            # 理想亮度 100-180
            if 100 <= mean_brightness <= 180:
                scores["brightness"] = 1.0
            elif mean_brightness < 50 or mean_brightness > 220:
                scores["brightness"] = 0.2
            else:
                scores["brightness"] = 0.6

        except Exception as e:
            logger.debug(f"评分帧失败: {e}")

        return scores

    def _score_rule_of_thirds(
        self, gray: np.ndarray, width: int, height: int
    ) -> float:
        """三分法构图评分"""
        try:
            # 三分线位置
            h_lines = [height / 3, 2 * height / 3]
            v_lines = [width / 3, 2 * width / 3]

            # 计算兴趣点（高对比度区域）
            # 使用 Sobel 边缘检测
            import cv2
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            edge_magnitude = np.sqrt(sobelx ** 2 + sobely ** 2)

            # 检查三分线附近的边缘密度
            threshold = np.percentile(edge_magnitude, 75)
            interest_points = edge_magnitude > threshold

            # 计算三分点附近的兴趣点密度
            third_points = [
                (int(height / 3), int(width / 3)),
                (int(height / 3), int(2 * width / 3)),
                (int(2 * height / 3), int(width / 3)),
                (int(2 * height / 3), int(2 * width / 3)),
            ]

            score = 0.0
            region_size = min(width, height) // 6
            for py, px in third_points:
                y_start = max(0, py - region_size)
                y_end = min(height, py + region_size)
                x_start = max(0, px - region_size)
                x_end = min(width, px + region_size)
                region = interest_points[y_start:y_end, x_start:x_end]
                if region.size > 0:
                    score += np.mean(region)

            return min(score / 4.0, 1.0)

        except Exception:
            return 0.5

    def _generate_reasons(self, scores: Dict[str, float]) -> List[str]:
        """根据评分生成推荐理由"""
        reasons = []

        if scores["sharpness"] >= 0.7:
            reasons.append("画面清晰锐利")
        elif scores["sharpness"] >= 0.4:
            reasons.append("清晰度尚可")
        else:
            reasons.append("画面偏糊")

        if scores["face"] >= 0.7:
            reasons.append("主体突出、人物居中")
        elif scores["face"] >= 0.4:
            reasons.append("有人物元素")

        if scores["composition"] >= 0.6:
            reasons.append("三分法构图良好")
        elif scores["composition"] >= 0.3:
            reasons.append("构图尚可")

        if scores["brightness"] >= 0.8:
            reasons.append("亮度适中")
        elif scores["brightness"] <= 0.3:
            reasons.append("亮度异常")

        return reasons

    def _get_video_duration(self, video_path: str) -> float:
        """获取视频时长"""
        try:
            import subprocess
            import json
            cmd = [
                self.ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                video_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return float(data.get("format", {}).get("duration", 0))
        except Exception as e:
            logger.error(f"获取视频时长失败: {e}")
        return 0.0

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "sharpness_weight": 0.35,
            "face_weight": 0.30,
            "composition_weight": 0.20,
            "brightness_weight": 0.15,
            "sample_interval": 2.0,
        }
