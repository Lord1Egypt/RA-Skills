"""语音识别模块 — 基于 whisper 本地模型"""

import os
import sys
from typing import Any, Dict, List, Optional

from .logger import get_logger

logger = get_logger(__name__)


class AudioTranscriber:
    """语音识别引擎封装"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.whisper_config = config.get("whisper", {})
        self.model_name = self.whisper_config.get("model_name", "small")
        self.language = self.whisper_config.get("language", "auto")
        self.device = self.whisper_config.get("device", "cpu")
        self.beam_size = self.whisper_config.get("beam_size", 5)
        self.temperature = self.whisper_config.get("temperature", 0.0)
        self._model = None
    
    def _load_model(self):
        """加载 whisper 模型（延迟加载）"""
        if self._model is not None:
            return
        
        logger.info(f"加载 whisper 模型: {self.model_name}")
        
        try:
            import whisper
        except ImportError:
            raise RuntimeError(
                "whisper 库未安装。请执行: pip install openai-whisper"
            )
        
        try:
            self._model = whisper.load_model(
                self.model_name,
                device=self.device
            )
        except Exception as e:
            raise RuntimeError(f"模型加载失败: {e}")
        
        logger.info("模型加载完成")
    
    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """
        执行语音识别。
        
        Args:
            audio_path: WAV 文件路径
            
        Returns:
            识别结果，包含 segments、language、duration 等
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")
        
        self._load_model()
        
        logger.info(f"开始语音识别: {audio_path}")
        
        try:
            import whisper
            
            result = self._model.transcribe(
                audio_path,
                language=None if self.language == "auto" else self.language,
                beam_size=self.beam_size,
                temperature=self.temperature,
                word_timestamps=True,
                condition_on_previous_text=True,
            )
        except Exception as e:
            raise RuntimeError(f"语音识别失败: {e}")
        
        # 标准化输出格式
        transcript = {
            "text": result.get("text", "").strip(),
            "language": result.get("language", "unknown"),
            "duration": None,
            "segments": [],
        }
        
        # 提取 segments
        for seg in result.get("segments", []):
            segment = {
                "id": seg.get("id", 0),
                "start": round(seg.get("start", 0), 3),
                "end": round(seg.get("end", 0), 3),
                "text": seg.get("text", "").strip(),
                "confidence": round(seg.get("avg_log_prob", 0), 4),
                "words": [],
            }
            
            # 词级别时间戳
            for word in seg.get("words", []):
                segment["words"].append({
                    "word": word.get("word", ""),
                    "start": round(word.get("start", 0), 3),
                    "end": round(word.get("end", 0), 3),
                    "confidence": round(word.get("probability", 0), 4),
                })
            
            transcript["segments"].append(segment)
            
            # 更新总时长
            if transcript["duration"] is None or seg.get("end", 0) > transcript["duration"]:
                transcript["duration"] = round(seg.get("end", 0), 3)
        
        logger.info(f"识别完成: {len(transcript['segments'])} 段文字")
        
        return transcript
