"""媒体处理模块 — 封装 ffmpeg/ffprobe"""

import json
import os
import subprocess
from typing import Any, Dict, List

from .logger import get_logger

logger = get_logger(__name__)


class MediaProcessor:
    """基于 ffmpeg 和 ffprobe 的视频媒体处理"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cache_dir = config.get("processing", {}).get("cache_dir", ".cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 验证 ffmpeg/ffprobe 可用性
        self._verify_ffmpeg()
    
    def _verify_ffmpeg(self):
        """验证 ffmpeg 是否可用"""
        for tool in ("ffmpeg", "ffprobe"):
            try:
                result = subprocess.run(
                    [tool, "-version"],
                    capture_output=True,
                    timeout=10
                )
                if result.returncode != 0:
                    raise RuntimeError(f"{tool} 不可用")
            except FileNotFoundError:
                raise RuntimeError(
                    f"❌ {tool} 未安装。请先安装 ffmpeg:\n"
                    f"  Windows: scoop install ffmpeg  أو  choco install ffmpeg\n"
                    f"  macOS: brew install ffmpeg\n"
                    f"  Ubuntu/Debian: sudo apt install ffmpeg\n"
                    f"  下载地址: https://ffmpeg.org/download.html"
                )
    
    def get_media_info(self, video_path: str) -> Dict[str, Any]:
        """
        获取视频元数据信息。
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            媒体信息字典
        """
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            error_msg = result.stderr or "未知错误"
            # 检查是否是文件损坏
            if "Invalid data" in error_msg or "error reading" in error_msg.lower():
                raise ValueError(
                    f"文件可能损坏或不是有效的视频文件。\n"
                    f"路径: {video_path}\n"
                    f"ffprobe 错误: {error_msg}"
                )
            raise RuntimeError(f"ffprobe 失败: {error_msg}")
        
        probe_data = json.loads(result.stdout)
        
        # 提取视频流信息
        video_stream = None
        audio_stream = None
        for stream in probe_data.get("streams", []):
            if stream["codec_type"] == "video" and not video_stream:
                video_stream = stream
            elif stream["codec_type"] == "audio" and not audio_stream:
                audio_stream = stream
        
        if not video_stream:
            raise ValueError(
                f"文件不包含视频流，请确认输入的是视频文件而非纯音频文件。\n"
                f"路径: {video_path}"
            )
        
        # 解析帧率
        fps = self._parse_fps(video_stream.get("r_frame_rate", "30/1"))
        
        # 获取时长和码率
        format_info = probe_data.get("format", {})
        duration = float(format_info.get("duration", 0))
        
        info = {
            "width": int(video_stream.get("width", 0)),
            "height": int(video_stream.get("height", 0)),
            "duration": duration,
            "fps": fps,
            "total_frames": int(video_stream.get("nb_frames", 0)),
            "video_codec": video_stream.get("codec_name", "unknown"),
            "pixel_format": video_stream.get("pix_fmt", "unknown"),
            "bitrate": int(format_info.get("bit_rate", 0)),
            "format_name": format_info.get("format_name", "unknown"),
            "has_audio": audio_stream is not None,
        }
        
        if audio_stream:
            info.update({
                "audio_codec": audio_stream.get("codec_name", "unknown"),
                "sample_rate": int(audio_stream.get("sample_rate", 0)),
                "channels": int(audio_stream.get("channels", 0)),
            })
        
        return info
    
    def extract_audio(self, video_path: str) -> str:
        """
        从视频中提取音频为 16kHz 单声道 WAV 格式。
        适合 whisper 识别的最佳输入格式。
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            WAV 文件路径
        """
        cache_key = f"audio_{self._hash_path(video_path)}.wav"
        output_path = os.path.join(self.cache_dir, cache_key)
        
        if os.path.exists(output_path):
            logger.info(f"音频缓存命中: {output_path}")
            return output_path
        
        cmd = [
            "ffmpeg",
            "-y",  # 覆盖
            "-i", video_path,
            "-vn",  # 不处理视频
            "-acodec", "pcm_s16le",  # 16-bit PCM
            "-ar", "16000",  # 16kHz
            "-ac", "1",  # 单声道
            "-loglevel", "error",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            error_msg = result.stderr.decode() if result.stderr else "未知错误"
            if "Invalid data" in error_msg:
                raise RuntimeError(
                    f"音频提取失败：视频文件可能损坏。\n"
                    f"建议尝试用 ffmpeg 手动修复：\n"
                    f"  ffmpeg -i input.mp4 -c copy output.mp4"
                )
            raise RuntimeError(f"音频提取失败: {error_msg}")
        
        logger.info(f"音频已提取: {output_path}")
        return output_path
    
    def extract_frames(self, video_path: str, fps: int = 1) -> str:
        """
        按指定帧率提取帧序列。
        
        Args:
            video_path: 视频文件路径
            fps: 每秒提取帧数，默认 1
            
        Returns:
            帧序列目录路径
        """
        dir_name = f"frames_{self._hash_path(video_path)}_{fps}fps"
        frames_dir = os.path.join(self.cache_dir, dir_name)
        os.makedirs(frames_dir, exist_ok=True)
        
        output_pattern = os.path.join(frames_dir, "frame_%05d.jpg")
        
        cmd = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vf", f"fps={fps}",
            "-q:v", "2",  # JPEG 质量
            "-loglevel", "error",
            output_pattern
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            error_msg = result.stderr.decode() if result.stderr else "未知错误"
            raise RuntimeError(f"帧提取失败: {error_msg}")
        
        frame_count = len([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])
        logger.info(f"提取 {frame_count} 帧到: {frames_dir}")
        return frames_dir
    
    def extract_keyframes(self, video_path: str, timestamps: List[float]) -> str:
        """
        提取指定时间点的关键帧。
        
        Args:
            video_path: 视频文件路径
            timestamps: 时间戳列表（秒）
            
        Returns:
            关键帧目录路径
        """
        dir_name = f"keyframes_{self._hash_path(video_path)}"
        frames_dir = os.path.join(self.cache_dir, dir_name)
        os.makedirs(frames_dir, exist_ok=True)
        
        for i, ts in enumerate(timestamps):
            output_path = os.path.join(frames_dir, f"keyframe_{i:04d}.jpg")
            if os.path.exists(output_path):
                continue
            
            cmd = [
                "ffmpeg",
                "-y",
                "-ss", str(ts),
                "-i", video_path,
                "-vframes", "1",
                "-q:v", "2",
                "-loglevel", "error",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode != 0:
                logger.warning(f"关键帧提取失败 (t={ts}s): {result.stderr.decode()}")
        
        return frames_dir
    
    @staticmethod
    def _parse_fps(fps_str: str) -> float:
        """解析帧率字符串，如 '30/1' -> 30.0"""
        try:
            if "/" in fps_str:
                num, den = fps_str.split("/")
                return float(num) / float(den)
            return float(fps_str)
        except (ValueError, ZeroDivisionError):
            return 30.0
    
    def _hash_path(self, path: str) -> str:
        """生成路径的短哈希"""
        import hashlib
        return hashlib.md5(path.encode()).hexdigest()[:12]
