"""媒体探测模块 — 用 ffmpeg 探测输入是否含视频流，纯音频直接转 16k 单声道 wav"""

import json
import os
import subprocess
from typing import Any, Dict, Optional

from .logger import get_logger

logger = get_logger(__name__)


class MediaProbe:
    """
    媒体探测器 — 前置适配器。
    
    功能：
    1. 用 ffprobe 探测输入文件是否有视频流
    2. 纯音频文件（mp3/m4a/wav 播客与录音）直接转 16k 单声道 wav 进 ASR 管线
    3. 跳过场景切分与 OCR
    4. 报告模板复用纪要版（说话人+时间轴+摘要）
    """
    
    # 纯音频扩展名
    AUDIO_EXTENSIONS = {
        ".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg", ".wma",
        ".opus", ".amr", ".aiff", ".ape", ".m4p", ".m4r",
    }
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cache_dir = config.get("processing", {}).get("cache_dir", ".cache")
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def probe(self, input_path: str) -> Dict[str, Any]:
        """
        探测输入文件类型。
        
        Args:
            input_path: 输入文件路径
            
        Returns:
            探测结果，含 has_video、has_audio、streams 等信息
        """
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            input_path,
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                raise RuntimeError(f"ffprobe 失败: {result.stderr}")
            
            probe_data = json.loads(result.stdout)
        except Exception as e:
            raise RuntimeError(f"无法探测媒体文件: {e}")
        
        # 分析流
        video_streams = []
        audio_streams = []
        
        for stream in probe_data.get("streams", []):
            codec_type = stream.get("codec_type", "")
            if codec_type == "video":
                video_streams.append(stream)
            elif codec_type == "audio":
                audio_streams.append(stream)
        
        format_info = probe_data.get("format", {})
        duration = float(format_info.get("duration", 0))
        
        result = {
            "has_video": len(video_streams) > 0,
            "has_audio": len(audio_streams) > 0,
            "video_streams": len(video_streams),
            "audio_streams": len(audio_streams),
            "duration": duration,
            "format_name": format_info.get("format_name", "unknown"),
            "bitrate": int(format_info.get("bit_rate", 0)),
            "input_path": input_path,
        }
        
        if video_streams:
            video = video_streams[0]
            result["video"] = {
                "width": int(video.get("width", 0)),
                "height": int(video.get("height", 0)),
                "codec": video.get("codec_name", "unknown"),
                "fps": self._parse_fps(video.get("r_frame_rate", "30/1")),
            }
        
        if audio_streams:
            audio = audio_streams[0]
            result["audio"] = {
                "codec": audio.get("codec_name", "unknown"),
                "sample_rate": int(audio.get("sample_rate", 0)),
                "channels": int(audio.get("channels", 0)),
            }
        
        return result
    
    def is_pure_audio(self, input_path: str) -> bool:
        """
        判断输入是否为纯音频文件。
        
        Args:
            input_path: 输入文件路径
            
        Returns:
            是否为纯音频
        """
        # 先检查扩展名（快速路径）
        ext = os.path.splitext(input_path)[1].lower()
        if ext in self.AUDIO_EXTENSIONS:
            return True
        
        # 扩展名不确定时，用 ffprobe 探测
        probe = self.probe(input_path)
        return probe["has_audio"] and not probe["has_video"]
    
    def convert_to_asr_audio(self, input_path: str) -> str:
        """
        将纯音频转换为 ASR 管线所需的 16k 单声道 wav 格式。
        
        Args:
            input_path: 输入音频文件路径
            
        Returns:
            转换后的 wav 文件路径
        """
        import hashlib
        
        cache_key = f"audio_{hashlib.md5(input_path.encode()).hexdigest()[:12]}.wav"
        output_path = os.path.join(self.cache_dir, cache_key)
        
        if os.path.exists(output_path):
            logger.info(f"音频缓存命中: {output_path}")
            return output_path
        
        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            "-loglevel", "error",
            output_path,
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            error_msg = result.stderr.decode() if result.stderr else "未知错误"
            raise RuntimeError(f"音频转换失败: {error_msg}")
        
        logger.info(f"音频已转换为 ASR 格式: {output_path}")
        return output_path
    
    def get_media_info_for_audio(self, input_path: str) -> Dict[str, Any]:
        """
        获取纯音频的媒体信息（适配视频分析管线）。
        
        Args:
            input_path: 输入音频文件路径
            
        Returns:
            适配后的媒体信息字典
        """
        probe = self.probe(input_path)
        
        if not probe["has_audio"]:
            raise ValueError(f"文件不包含音频流: {input_path}")
        
        # 转换为 ASR 格式
        audio_path = self.convert_to_asr_audio(input_path)
        
        # 构建兼容视频分析管线的 media_info
        media_info = {
            "width": 0,
            "height": 0,
            "duration": probe["duration"],
            "fps": 0,
            "total_frames": 0,
            "video_codec": "none",
            "pixel_format": "none",
            "bitrate": probe["bitrate"],
            "format_name": probe["format_name"],
            "has_audio": True,
            "has_video": False,
            "audio_codec": probe["audio"]["codec"],
            "sample_rate": probe["audio"]["sample_rate"],
            "channels": probe["audio"]["channels"],
            "audio_path": audio_path,
            "is_pure_audio": True,
        }
        
        return media_info
    
    def get_media_info_for_video(self, input_path: str) -> Dict[str, Any]:
        """
        获取视频文件的媒体信息（委托给 MediaProcessor）。
        
        Args:
            input_path: 输入视频文件路径
            
        Returns:
            媒体信息字典
        """
        from .media_processor import MediaProcessor
        processor = MediaProcessor(self.config)
        return processor.get_media_info(input_path)
    
    @staticmethod
    def _parse_fps(fps_str: str) -> float:
        """解析帧率字符串"""
        try:
            if "/" in fps_str:
                num, den = fps_str.split("/")
                return float(num) / float(den)
            return float(fps_str)
        except (ValueError, ZeroDivisionError):
            return 30.0
