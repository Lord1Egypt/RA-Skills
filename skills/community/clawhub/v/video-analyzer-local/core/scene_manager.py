"""场景管理模块 — 合并场景检测+章节切片为 detect→slice 一条链"""

import os
from typing import Any, Dict, List, Optional

from .logger import get_logger
from .scene_detector import SceneDetector
from .chapter_slicer import ChapterSlicer

logger = get_logger(__name__)


class SceneManager:
    """
    场景管理器 — 统一入口，封装 detect→slice 一条链。
    
    解决 scene_detector 和 chapter_slicer 独立调用但逻辑连续的问题，
    提供 detect() → slice() 的完整工作流。
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._detector = SceneDetector(config)
        self._slicer = ChapterSlicer(config)
        self._last_scenes: Optional[Dict] = None
    
    def detect_and_slice(
        self,
        video_path: str,
        transcript: Dict,
        output_dir: str,
        frames_dir: str = None,
    ) -> Dict[str, Any]:
        """
        场景管理一条龙：检测场景 → 切割章节 → 生成字幕。
        
        Args:
            video_path: 视频文件路径
            transcript: 语音识别结果（含 segments）
            output_dir: 输出目录
            frames_dir: 预提取帧目录（可选）
            
        Returns:
            包含 scenes + chapters 的完整结果
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1: 检测场景边界
        logger.info("🎬 [场景管理] 检测场景边界...")
        scenes = self._detector.detect_scenes(video_path, frames_dir)
        self._last_scenes = scenes
        logger.info(f"   检测到 {scenes.get('total_scenes', 0)} 个场景")
        
        # Step 2: 按场景切割章节
        chapters_dir = os.path.join(output_dir, "chapters")
        logger.info("✂️  [场景管理] 按场景切割章节...")
        chapters_result = self._slicer.slice_chapters(
            video_path, scenes, transcript, chapters_dir
        )
        logger.info(f"   切片完成: {chapters_result.get('total_chapters', 0)} 个章节")
        
        return {
            "scenes": scenes,
            "chapters": chapters_result,
            "total_scenes": scenes.get("total_scenes", 0),
            "total_chapters": chapters_result.get("total_chapters", 0),
            "output_dir": output_dir,
            "chapters_dir": chapters_dir,
        }
    
    def detect_only(
        self,
        video_path: str,
        frames_dir: str = None,
    ) -> Dict[str, Any]:
        """
        仅检测场景边界（不切割）。
        
        Args:
            video_path: 视频文件路径
            frames_dir: 预提取帧目录（可选）
            
        Returns:
            场景检测结果
        """
        logger.info("🎬 [场景管理] 仅检测场景边界...")
        scenes = self._detector.detect_scenes(video_path, frames_dir)
        self._last_scenes = scenes
        logger.info(f"   检测到 {scenes.get('total_scenes', 0)} 个场景")
        return scenes
    
    def slice_with_scenes(
        self,
        video_path: str,
        scenes: Dict,
        transcript: Dict,
        output_dir: str,
    ) -> Dict[str, Any]:
        """
        使用已有的场景结果切割章节。
        
        Args:
            video_path: 视频文件路径
            scenes: 预检测的场景结果
            transcript: 语音识别结果
            output_dir: 输出目录
            
        Returns:
            切片结果
        """
        os.makedirs(output_dir, exist_ok=True)
        self._last_scenes = scenes
        
        chapters_dir = os.path.join(output_dir, "chapters")
        logger.info("✂️  [场景管理] 使用已有场景切割章节...")
        chapters_result = self._slicer.slice_chapters(
            video_path, scenes, transcript, chapters_dir
        )
        logger.info(f"   切片完成: {chapters_result.get('total_chapters', 0)} 个章节")
        
        return {
            "scenes": scenes,
            "chapters": chapters_result,
            "total_chapters": chapters_result.get("total_chapters", 0),
            "output_dir": output_dir,
            "chapters_dir": chapters_dir,
        }
    
    @property
    def last_scenes(self) -> Optional[Dict]:
        """获取最后一次检测的场景结果"""
        return self._last_scenes
