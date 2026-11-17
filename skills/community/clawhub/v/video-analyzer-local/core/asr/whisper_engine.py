"""Whisper 引擎封装 — 包装原有音频识别能力"""

import os
from typing import Any, Dict, List

from .base import ASREngine, ASRResult, ASRSegment
from ..logger import get_logger

logger = get_logger(__name__)


class WhisperEngine(ASREngine):
    """
    OpenAI Whisper 引擎封装。
    
    特点：
    - 支持多语言（含中文）
    - 目前默认引擎
    - 模型大小可选：tiny/base/small/medium/large-v3
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.whisper_config = config.get("whisper", {})
        self.model_name = self.whisper_config.get("model_name", "small")
        self.language = self.whisper_config.get("language", "auto")
        self.device = self.whisper_config.get("device", "cpu")
        self.beam_size = self.whisper_config.get("beam_size", 5)
        self.temperature = self.whisper_config.get("temperature", 0.0)
    
    @property
    def name(self) -> str:
        return "whisper"
    
    @property
    def supported_languages(self) -> List[str]:
        return [
            "auto", "zh", "en", "ja", "ko", "fr", "de", "es", "ru",
            "th", "vi", "id", "ms", "tl", "ar", "hi", "it", "pt", "nl",
            "sv", "da", "no", "fi", "pl", "cs", "sk", "hu", "ro", "tr",
            "el", "he", "uk", "bg", "hr", "sr", "sl", "ca", "eu", "gl",
        ]
    
    def load_model(self) -> bool:
        """加载 whisper 模型"""
        try:
            import whisper
            
            logger.info(f"加载 Whisper 模型: {self.model_name} (设备: {self.device})")
            
            self._model = whisper.load_model(self.model_name, device=self.device)
            self._loaded = True
            
            logger.info(f"Whisper 模型加载完成: {self.model_name}")
            return True
            
        except ImportError:
            logger.error("whisper 库未安装。请执行: pip install openai-whisper")
            return False
        except Exception as e:
            logger.error(f"Whisper 模型加载失败: {e}")
            return False
    
    def transcribe(self, audio_path: str, **kwargs) -> ASRResult:
        """
        使用 whisper 执行语音识别。
        
        Args:
            audio_path: WAV 文件路径
            **kwargs: 可选 language, beam_size, temperature 等
            
        Returns:
            ASRResult
        """
        if not os.path.exists(audio_path):
            from .base import ASRResult
            return ASRResult(text="", language="unknown", engine_name=self.name)
        
        self.ensure_loaded()
        
        if not self._loaded:
            return ASRResult(text="", language="unknown", engine_name=self.name)
        
        # 参数覆盖
        language = kwargs.get("language", 
                           None if self.language == "auto" else self.language)
        beam_size = kwargs.get("beam_size", self.beam_size)
        temperature = kwargs.get("temperature", self.temperature)
        
        logger.info(f"Whisper 开始识别: {audio_path} (语言: {language or 'auto'})")
        
        try:
            result = self._model.transcribe(
                audio_path,
                language=language,
                beam_size=beam_size,
                temperature=temperature,
                word_timestamps=True,
                condition_on_previous_text=True,
            )
        except Exception as e:
            logger.error(f"Whisper 识别失败: {e}")
            return ASRResult(text="", language="unknown", engine_name=self.name)
        
        # 转换为统一格式
        return self._parse_result(result)
    
    def _parse_result(self, result: Dict) -> ASRResult:
        """解析 whisper 输出为统一格式"""
        segments = []
        
        for seg in result.get("segments", []):
            words = []
            for word in seg.get("words", []):
                words.append({
                    "word": word.get("word", ""),
                    "start": round(word.get("start", 0), 3),
                    "end": round(word.get("end", 0), 3),
                    "confidence": round(word.get("probability", 0), 4),
                })
            
            segments.append(ASRSegment(
                id=seg.get("id", 0),
                start=round(seg.get("start", 0), 3),
                end=round(seg.get("end", 0), 3),
                text=seg.get("text", "").strip(),
                confidence=round(seg.get("avg_log_prob", 0), 4),
                words=words,
            ))
        
        duration = 0
        if segments:
            duration = max(seg.end for seg in segments)
        
        return ASRResult(
            text=result.get("text", "").strip(),
            language=result.get("language", "unknown"),
            duration=duration,
            segments=segments,
            engine_name=self.name,
        )
