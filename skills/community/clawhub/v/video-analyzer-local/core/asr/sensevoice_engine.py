"""SenseVoice 引擎封装 — 阿里达摩院多语言+情感识别"""

import os
import re
from typing import Any, Dict, List, Optional

from .base import ASREngine, ASRResult, ASRSegment
from ..logger import get_logger

logger = get_logger(__name__)


class SenseVoiceEngine(ASREngine):
    """
    阿里达摩院 SenseVoice 引擎封装。
    
    特点：
    - 多语言识别（中/英/日/韩等）
    - 情感识别（开心/悲伤/愤怒/中性）
    - 音频事件检测（笑声/掌声等）
    - 低延迟
    """
    
    # 情感标签映射
    EMOTION_LABELS = {
        "<|NEUTRAL|>": "中性",
        "<|HAPPY|>": "开心",
        "<|SAD|>": "悲伤",
        "<|ANGRY|>": "愤怒",
        "<|FEAR|>": "恐惧",
        "<|SURPRISE|>": "惊讶",
        "<|DISGUST|>": "厌恶",
        "<|EMOTIONLESS|>": "无明显情感",
    }
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model_name = config.get("asr", {}).get(
            "sensevoice_model", "SenseVoiceSmall"
        )
        self.device = config.get("asr", {}).get("sensevoice_device", "cpu")
        self.use_itn = config.get("asr", {}).get("sensevoice_use_itn", True)  # 逆文本归一化
        self._model = None
    
    @property
    def name(self) -> str:
        return "sensevoice"
    
    @property
    def supported_languages(self) -> List[str]:
        return ["auto", "zh", "en", "ja", "ko"]
    
    def load_model(self) -> bool:
        """
        加载 SenseVoice 模型。
        
        需要 funasr 库：pip install funasr modelscope torch torchaudio
        """
        try:
            logger.info(f"加载 SenseVoice 模型: {self.model_name}")
            
            try:
                from funasr import AutoModel
                
                self._model = AutoModel(
                    model="iic/SenseVoiceSmall",
                    device=self.device,
                )
                
                self._loaded = True
                logger.info("SenseVoice 模型加载完成")
                return True
                
            except ImportError:
                try:
                    from modelscope.pipelines import pipeline
                    from modelscope.utils.constant import Tasks
                    
                    self._model = pipeline(
                        Tasks.auto_speech_recognition,
                        model="iic/SenseVoiceSmall",
                        device=self.device,
                    )
                    self._loaded = True
                    logger.info("SenseVoice 模型加载完成 (via modelscope)")
                    return True
                except ImportError:
                    logger.error(
                        "SenseVoice 需要安装 funasr 或 modelscope。\n"
                        "  安装命令: pip install funasr modelscope torch torchaudio"
                    )
                    return False
        
        except Exception as e:
            logger.error(f"SenseVoice 模型加载失败: {e}")
            return False
    
    def transcribe(self, audio_path: str, **kwargs) -> ASRResult:
        """
        使用 SenseVoice 执行语音识别。
        
        Args:
            audio_path: WAV 文件路径
            **kwargs: 可选参数
            
        Returns:
            ASRResult（含情感标签）
        """
        if not os.path.exists(audio_path):
            return ASRResult(text="", language="unknown", engine_name=self.name)
        
        self.ensure_loaded()
        
        if not self._loaded:
            return ASRResult(text="", language="unknown", engine_name=self.name)
        
        logger.info(f"SenseVoice 开始识别: {audio_path}")
        
        try:
            try:
                result = self._model.generate(
                    input=audio_path,
                    use_itn=self.use_itn,
                    **kwargs,
                )
            except TypeError:
                result = self._model.generate(input=audio_path)
            
            if isinstance(result, list) and result:
                result = result[0]
            
            raw_text = result.get("text", "")
            
            # 解析情感标签
            text, emotion = self._parse_emotion(raw_text)
            
            # 提取时间戳
            timestamps = result.get("timestamp", [])
            
            return self._parse_result(text, emotion, timestamps, audio_path)
            
        except Exception as e:
            logger.error(f"SenseVoice 识别失败: {e}")
            return ASRResult(text="", language="unknown", engine_name=self.name)
    
    def _parse_emotion(self, raw_text: str) -> tuple:
        """
        从 SenseVoice 输出中解析情感标签。
        
        Returns:
            (清洗后的文本, 情感标签)
        """
        emotion = "中性"
        
        # 查找情感标签
        for label, label_zh in self.EMOTION_LABELS.items():
            if label in raw_text:
                emotion = label_zh
                break
        
        # 移除所有标签，只保留文本
        text = raw_text
        for label in self.EMOTION_LABELS:
            text = text.replace(label, "")
        text = re.sub(r"<\|[^|]*\|>", "", text).strip()
        
        return text, emotion
    
    def _parse_result(
        self, text: str, emotion: str, timestamps: List, audio_path: str
    ) -> ASRResult:
        """解析 SenseVoice 输出"""
        segments = []
        
        if timestamps:
            for i, ts in enumerate(timestamps):
                start = self._timestamp_to_seconds(ts[0]) if len(ts) >= 2 else 0
                end = self._timestamp_to_seconds(ts[1]) if len(ts) >= 2 else 0
                
                segments.append(ASRSegment(
                    id=i,
                    start=start,
                    end=end,
                    text=self._extract_text_at_timestamp(text, i),
                    confidence=0.9,
                    emotion=emotion,
                ))
        else:
            segments.append(ASRSegment(
                id=0,
                start=0,
                end=self._get_audio_duration(audio_path),
                text=text,
                confidence=0.9,
                emotion=emotion,
            ))
        
        # 检测语言
        language = self._detect_language(text)
        
        duration = 0
        if segments and segments[-1].end > 0:
            duration = segments[-1].end
        
        return ASRResult(
            text=text,
            language=language,
            duration=duration,
            segments=segments,
            engine_name=self.name,
        )
    
    @staticmethod
    def _timestamp_to_seconds(ts) -> float:
        """时间戳转秒"""
        if isinstance(ts, (list, tuple)):
            return ts[0] / 1000.0
        elif isinstance(ts, (int, float)):
            return ts / 1000.0
        return 0.0
    
    @staticmethod
    def _extract_text_at_timestamp(text: str, idx: int) -> str:
        """提取时间戳对应的文本段"""
        return text  # SenseVoice 整段返回，暂不拆分
    
    @staticmethod
    def _detect_language(text: str) -> str:
        """简单语言检测"""
        if not text:
            return "unknown"
        # 检测中文字符比例
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        if chinese_chars > len(text) * 0.3:
            return "zh"
        # 检测日文假名
        if re.search(r'[\u3040-\u309f\u30a0-\u30ff]', text):
            return "ja"
        # 检测韩文
        if re.search(r'[\uac00-\ud7af]', text):
            return "ko"
        return "en"
    
    @staticmethod
    def _get_audio_duration(audio_path: str) -> float:
        """获取音频时长"""
        try:
            import wave
            with wave.open(audio_path, "r") as w:
                frames = w.getnframes()
                rate = w.getframerate()
                return frames / float(rate)
        except Exception:
            return 0
