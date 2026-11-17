"""Paraformer 引擎封装 — 阿里达摩院中文语音识别 SOTA"""

import os
from typing import Any, Dict, List, Optional

from .base import ASREngine, ASRResult, ASRSegment
from ..logger import get_logger

logger = get_logger(__name__)


class ParaformerEngine(ASREngine):
    """
    阿里达摩院 Paraformer 引擎封装。
    
    特点：
    - 中文识别 SOTA（优于 Whisper 中文场景）
    - 支持标点符号自动插入
    - 支持热词增强（用户可设置人名、专业术语）
    - 完全离线
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model_name = config.get("asr", {}).get(
            "paraformer_model", "paraformer-zh"
        )
        self.device = config.get("asr", {}).get("paraformer_device", "cpu")
        self.hotwords = config.get("asr", {}).get("hotwords", [])
        self._model = None
    
    @property
    def name(self) -> str:
        return "paraformer"
    
    @property
    def supported_languages(self) -> List[str]:
        return ["zh", "en", "auto"]
    
    def load_model(self) -> bool:
        """
        加载 Paraformer 模型。
        
        需要 funasr 库：pip install funasr modelscope torch torchaudio
        """
        try:
            logger.info(f"加载 Paraformer 模型: {self.model_name}")
            
            # 尝试通过 ModelScope 加载（阿里官方）
            try:
                from modelscope.pipelines import pipeline
                from modelscope.utils.constant import Tasks
                
                self._model = pipeline(
                    Tasks.auto_speech_recognition,
                    model=f"damio/{self.model_name}",
                    device=self.device,
                )
                
                self._loaded = True
                logger.info("Paraformer 模型加载完成")
                return True
                
            except ImportError:
                logger.debug("ModelScope 不可用，尝试直接 funasr 加载...")
            
            # 备选：通过 funasr 直接加载
            try:
                from funasr import AutoModel
                
                self._model = AutoModel(
                    model=f"paraformer-zh",
                    device=self.device,
                )
                
                self._loaded = True
                logger.info("Paraformer 模型加载完成 (via funasr)")
                return True
                
            except ImportError:
                logger.error(
                    "Paraformer 需要安装 funasr 或 modelscope。\n"
                    "  安装命令: pip install funasr modelscope torch torchaudio"
                )
                return False
                
        except Exception as e:
            logger.error(f"Paraformer 模型加载失败: {e}")
            return False
    
    def transcribe(self, audio_path: str, **kwargs) -> ASRResult:
        """
        使用 Paraformer 执行语音识别。
        
        Args:
            audio_path: WAV 文件路径
            **kwargs: 可选 hotwords 等参数
            
        Returns:
            ASRResult
        """
        if not os.path.exists(audio_path):
            return ASRResult(text="", language="unknown", engine_name=self.name)
        
        self.ensure_loaded()
        
        if not self._loaded:
            return ASRResult(text="", language="unknown", engine_name=self.name)
        
        # 热词增强
        hotwords = kwargs.get("hotwords", self.hotwords)
        
        logger.info(f"Paraformer 开始识别: {audio_path}")
        
        try:
            # ModelScope pipeline 调用方式
            gen_kwargs = {}
            if hotwords:
                gen_kwargs["hotwords"] = " ".join(hotwords)
            
            result = self._model(audio_path, **gen_kwargs)
            
            # 处理返回值格式
            if isinstance(result, list):
                result = result[0]
            
            text = result.get("text", "")
            
            # 获取时间戳（如果有）
            timestamps = result.get("timestamp", [])
            
            return self._parse_result(text, timestamps, audio_path)
            
        except AttributeError:
            # funasr AutoModel 调用方式
            try:
                result = self._model.generate(input=audio_path)
                text = result[0].get("text", "") if result else ""
                return ASRResult(
                    text=text,
                    language="zh",
                    engine_name=self.name,
                )
            except Exception as e2:
                logger.error(f"Paraformer funasr 调用也失败: {e2}")
                return ASRResult(text="", language="unknown", engine_name=self.name)
                
        except Exception as e:
            logger.error(f"Paraformer 识别失败: {e}")
            return ASRResult(text="", language="unknown", engine_name=self.name)
    
    def _parse_result(
        self, text: str, timestamps: List, audio_path: str
    ) -> ASRResult:
        """解析 Paraformer 输出"""
        segments = []
        
        if timestamps:
            # 有时间戳，按时间戳分段
            for i, (start, end) in enumerate(timestamps):
                start_s = self._timestamp_to_seconds(start)
                end_s = self._timestamp_to_seconds(end)
                
                # 提取对应文本段
                seg_text = self._extract_text_between(text, i, len(timestamps))
                
                segments.append(ASRSegment(
                    id=i,
                    start=start_s,
                    end=end_s,
                    text=seg_text,
                    confidence=0.9,  # Paraformer 不输出置信度
                ))
        else:
            # 无时间戳，整段文本作为一个段
            segments.append(ASRSegment(
                id=0,
                start=0,
                end=0,  # 后续填充
                text=text,
                confidence=0.9,
            ))
        
        # 获取音频时长
        duration = 0
        if segments and segments[-1].end > 0:
            duration = segments[-1].end
        else:
            duration = self._get_audio_duration(audio_path)
            if segments:
                segments[-1].end = duration
        
        return ASRResult(
            text=text,
            language="zh",
            duration=duration,
            segments=segments,
            engine_name=self.name,
        )
    
    @staticmethod
    def _timestamp_to_seconds(ts) -> float:
        """将时间戳（毫秒或[ms,ms]）转为秒"""
        if isinstance(ts, (list, tuple)):
            return ts[0] / 1000.0
        elif isinstance(ts, (int, float)):
            return ts / 1000.0
        return 0.0
    
    @staticmethod
    def _extract_text_between(text: str, idx: int, total: int) -> str:
        """按索引提取文本段（Paraformer 不返回段级文本时的启发式分法）"""
        if total <= 1:
            return text
        # 简单均匀分割
        chunk_size = max(len(text) // total, 1)
        start = idx * chunk_size
        end = start + chunk_size if idx < total - 1 else len(text)
        return text[start:end].strip()
    
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
