"""章节切片模块 — 按场景切割短视频片段 + 生成SRT字幕"""

import os
import subprocess
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .logger import get_logger

logger = get_logger(__name__)


class ChapterSlicer:
    """视频章节切片器 — 按场景边界切割短视频并生成字幕"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cache_dir = config.get("processing", {}).get("cache_dir", ".cache")
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def slice_chapters(
        self,
        video_path: str,
        scenes: Dict,
        transcript: Dict,
        output_dir: str,
    ) -> Dict[str, Any]:
        """
        按场景章节切割视频，每段配独立SRT字幕。
        
        Args:
            video_path: 视频文件路径
            scenes: 场景检测结果
            transcript: 语音识别结果
            output_dir: 输出目录
            
        Returns:
            切片结果，包含章节列表和路径
        """
        os.makedirs(output_dir, exist_ok=True)
        
        scene_list = scenes.get("scenes", [])
        segments = transcript.get("segments", [])
        
        if not scene_list:
            logger.warning("无场景数据，跳过章节切片")
            return {"chapters": [], "output_dir": output_dir}
        
        logger.info(f"开始章节切片: {len(scene_list)} 个场景")
        
        chapters = []
        for scene in scene_list:
            chapter = self._cut_single_chapter(video_path, scene, segments, output_dir)
            if chapter:
                chapters.append(chapter)
        
        # 生成章节索引文件
        index_path = self._generate_chapters_index(chapters, output_dir)
        
        result = {
            "chapters": chapters,
            "total_chapters": len(chapters),
            "output_dir": output_dir,
            "index_path": index_path,
        }
        
        logger.info(f"章节切片完成: {len(chapters)} 个章节")
        return result
    
    def _cut_single_chapter(
        self,
        video_path: str,
        scene: Dict,
        segments: List[Dict],
        output_dir: str,
    ) -> Optional[Dict]:
        """切割单个场景章节"""
        idx = scene.get("index", 0)
        start_time = scene.get("start_time", 0)
        end_time = scene.get("end_time", 0)
        duration = end_time - start_time
        
        if duration <= 0:
            return None
        
        # 输出文件路径
        chapter_video = os.path.join(output_dir, f"chapter_{idx:03d}.mp4")
        chapter_srt = os.path.join(output_dir, f"chapter_{idx:03d}.srt")
        chapter_vtt = os.path.join(output_dir, f"chapter_{idx:03d}.vtt")
        
        # 提取视频片段
        success = self._extract_video_clip(video_path, start_time, duration, chapter_video)
        if not success:
            logger.warning(f"场景 {idx} 视频切割失败")
            return None
        
        # 提取该场景的字幕段
        scene_segments = self._filter_segments_for_scene(segments, start_time, end_time)
        
        # 生成SRT字幕
        srt_content = self._generate_srt(scene_segments, start_time)
        with open(chapter_srt, "w", encoding="utf-8") as f:
            f.write(srt_content)
        
        # 生成WebVTT字幕（供HTML5播放器使用）
        vtt_content = self._generate_vtt(scene_segments, start_time)
        with open(chapter_vtt, "w", encoding="utf-8") as f:
            f.write(vtt_content)
        
        return {
            "index": idx,
            "start_time": start_time,
            "end_time": end_time,
            "duration": round(duration, 2),
            "video_path": chapter_video,
            "srt_path": chapter_srt,
            "vtt_path": chapter_vtt,
            "subtitle_count": len(scene_segments),
        }
    
    def _extract_video_clip(
        self,
        video_path: str,
        start: float,
        duration: float,
        output_path: str,
    ) -> bool:
        """使用ffmpeg切割视频片段（快速复制流）"""
        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start),
            "-i", video_path,
            "-t", str(duration),
            "-c", "copy",  # 直接复制流，不重新编码（极速）
            "-avoid_negative_ts", "make_zero",
            "-loglevel", "error",
            output_path,
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=120)
            if result.returncode != 0:
                # 如果复制流失败（可能是关键帧问题），回退到重新编码
                return self._extract_video_clip_reencode(video_path, start, duration, output_path)
            return os.path.exists(output_path) and os.path.getsize(output_path) > 0
        except subprocess.TimeoutExpired:
            logger.warning("视频切割超时，尝试重新编码方式")
            return self._extract_video_clip_reencode(video_path, start, duration, output_path)
        except Exception as e:
            logger.debug(f"视频切割失败: {e}")
            return False
    
    def _extract_video_clip_reencode(
        self,
        video_path: str,
        start: float,
        duration: float,
        output_path: str,
    ) -> bool:
        """使用ffmpeg重新编码方式切割（兼容性更好但较慢）"""
        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start),
            "-i", video_path,
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-loglevel", "error",
            output_path,
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=300)
            return result.returncode == 0 and os.path.exists(output_path)
        except Exception as e:
            logger.debug(f"重新编码切割失败: {e}")
            return False
    
    def _filter_segments_for_scene(
        self,
        segments: List[Dict],
        scene_start: float,
        scene_end: float,
    ) -> List[Dict]:
        """筛选出属于该场景的语音段"""
        result = []
        for seg in segments:
            seg_start = seg.get("start", 0)
            seg_end = seg.get("end", 0)
            
            # 计算与场景的重叠
            overlap_start = max(seg_start, scene_start)
            overlap_end = min(seg_end, scene_end)
            
            if overlap_start < overlap_end:
                result.append(seg)
        
        return result
    
    def _generate_srt(self, segments: List[Dict], scene_offset: float) -> str:
        """生成SRT字幕内容"""
        parts = []
        for i, seg in enumerate(segments):
            # 时间戳需要相对场景起点
            start = seg.get("start", 0) - scene_offset
            end = seg.get("end", 0) - scene_offset
            
            # 确保不小于0
            start = max(0, start)
            end = max(start + 0.5, end)
            
            start_ts = self._format_srt_time(start)
            end_ts = self._format_srt_time(end)
            text = seg.get("text", "").strip()
            
            if text:
                parts.append(f"{i+1}\n{start_ts} --> {end_ts}\n{text}\n")
        
        return "\n".join(parts)
    
    def _generate_vtt(self, segments: List[Dict], scene_offset: float) -> str:
        """生成WebVTT字幕内容（HTML5播放器兼容）"""
        parts = ["WEBVTT\n\n"]
        
        for seg in segments:
            start = max(0, seg.get("start", 0) - scene_offset)
            end = max(start + 0.5, seg.get("end", 0) - scene_offset)
            
            start_ts = self._format_vtt_time(start)
            end_ts = self._format_vtt_time(end)
            text = seg.get("text", "").strip()
            
            if text:
                parts.append(f"{start_ts} --> {end_ts}\n{text}\n\n")
        
        return "".join(parts)
    
    def _generate_chapters_index(self, chapters: List[Dict], output_dir: str) -> str:
        """生成章节索引JSON文件"""
        index = {
            "total_chapters": len(chapters),
            "chapters": [
                {
                    "index": ch.get("index"),
                    "start_time": ch.get("start_time"),
                    "end_time": ch.get("end_time"),
                    "duration": ch.get("duration"),
                    "video_file": os.path.basename(ch.get("video_path", "")),
                    "srt_file": os.path.basename(ch.get("srt_path", "")),
                    "vtt_file": os.path.basename(ch.get("vtt_path", "")),
                }
                for ch in chapters
            ]
        }
        
        # JSON索引
        json_path = os.path.join(output_dir, "chapters_index.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        
        # 同时生成纯文本章节文件（兼容播放器）
        txt_path = os.path.join(output_dir, "chapters.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            for ch in chapters:
                ts = self._format_srt_time(ch.get("start_time", 0))
                f.write(f"CHAPTER{ch['index']:03d}={ts}\n")
                f.write(f"CHAPTER{ch['index']:03d}NAME=章节 {ch['index']}\n")
        
        return json_path
    
    @staticmethod
    def _format_srt_time(seconds: float) -> str:
        """格式化为 SRT 时间格式: HH:MM:SS,mmm"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    
    @staticmethod
    def _format_vtt_time(seconds: float) -> str:
        """格式化为 VTT 时间格式: HH:MM:SS.mmm"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
