"""ASR 路由器 — 语言检测 + 引擎选择 + 降级策略"""

from typing import Any, Dict, List, Optional

from .base import ASREngine, ASRResult
from .whisper_engine import WhisperEngine
from ..logger import get_logger

logger = get_logger(__name__)


class ASRRouter:
    """
    ASR 引擎路由器。
    
    功能：
    1. 自动检测音频语言
    2. 根据语言选择最优引擎
    3. 引擎不可用时自动降级
    4. 统一管理多个引擎的生命周期
    """
    
    # 引擎优先级（按语言）
    ENGINE_PRIORITY = {
        "zh": ["paraformer", "sensevoice", "whisper"],
        "en": ["whisper", "sensevoice"],
        "ja": ["sensevoice", "whisper"],
        "ko": ["sensevoice", "whisper"],
        "auto": ["whisper", "paraformer", "sensevoice"],
    }
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._engines: Dict[str, ASREngine] = {}
        self._active_engine: Optional[str] = None
        self._fallback_chain: List[str] = []
    
    @property
    def active_engine(self) -> Optional[ASREngine]:
        """获取当前激活的引擎"""
        if self._active_engine and self._active_engine in self._engines:
            return self._engines[self._active_engine]
        return None
    
    def get_engine(self, engine_name: str) -> Optional[ASREngine]:
        """获取指定名称的引擎"""
        return self._engines.get(engine_name)
    
    def list_engines(self) -> List[str]:
        """列出所有可用引擎"""
        available = []
        for name in self._engines:
            if self._engines[name].is_loaded:
                available.append(name)
        return available
    
    def select_engine(
        self,
        audio_path: str,
        preferred_engine: Optional[str] = None,
        language: str = "auto",
    ) -> ASREngine:
        """
        智能选择最优引擎。
        
        策略：
        1. 用户指定引擎 > 自动选择
        2. 中文优先 Paraformer
        3. 英文/多语言用 Whisper
        4. 需要情感识别用 SenseVoice
        5. 引擎加载失败自动降级
        
        Args:
            audio_path: 音频文件路径
            preferred_engine: 用户偏好的引擎名
            language: 语言偏好
            
        Returns:
            选中的引擎实例
        """
        # 1. 用户使用偏好
        if preferred_engine:
            engine = self._load_engine(preferred_engine)
            if engine:
                self._active_engine = preferred_engine
                logger.info(f"用户选择引擎: {preferred_engine}")
                return engine
            logger.warning(f"用户指定的引擎 {preferred_engine} 不可用，自动选择")
        
        # 2. 确定语言
        if language == "auto":
            language = self._detect_language(audio_path)
            logger.info(f"自动检测语言: {language}")
        
        # 3. 按优先级选择引擎
        priority = self.ENGINE_PRIORITY.get(language, self.ENGINE_PRIORITY["auto"])
        
        for engine_name in priority:
            engine = self._load_engine(engine_name)
            if engine:
                self._active_engine = engine_name
                logger.info(f"自动选择引擎: {engine_name} (语言: {language})")
                return engine
        
        # 4. 所有引擎都失败，使用 Whisper（默认）
        logger.warning("所有高级引擎不可用，回退到 Whisper")
        whisper = WhisperEngine(self.config)
        whisper.ensure_loaded()
        self._engines["whisper"] = whisper
        self._active_engine = "whisper"
        return whisper
    
    def transcribe(
        self,
        audio_path: str,
        preferred_engine: Optional[str] = None,
        language: str = "auto",
        **kwargs,
    ) -> ASRResult:
        """
        统一识别接口。
        
        Args:
            audio_path: 音频路径
            preferred_engine: 偏好引擎
            language: 语言偏好
            **kwargs: 传递给引擎的额外参数
            
        Returns:
            ASRResult
        """
        engine = self.select_engine(audio_path, preferred_engine, language)
        
        try:
            return engine.transcribe(audio_path, **kwargs)
        except Exception as e:
            logger.error(f"引擎 {engine.name} 识别失败: {e}")
            
            # 尝试降级
            for fallback_name in self.ENGINE_PRIORITY.get("auto", []):
                if fallback_name != engine.name:
                    fallback = self._load_engine(fallback_name)
                    if fallback:
                        logger.info(f"降级到引擎: {fallback_name}")
                        return fallback.transcribe(audio_path, **kwargs)
            
            # 全部失败，返回空结果
            return ASRResult(text="", language="unknown", engine_name="none")
    
    def _load_engine(self, engine_name: str) -> Optional[ASREngine]:
        """加载指定引擎（如果尚未加载）"""
        if engine_name in self._engines:
            return self._engines[engine_name]
        
        engine: Optional[ASREngine] = None
        
        if engine_name == "whisper":
            engine = WhisperEngine(self.config)
        elif engine_name == "paraformer":
            try:
                from .paraformer_engine import ParaformerEngine
                engine = ParaformerEngine(self.config)
            except ImportError:
                logger.debug("Paraformer 模块导入失败")
                return None
        elif engine_name == "sensevoice":
            try:
                from .sensevoice_engine import SenseVoiceEngine
                engine = SenseVoiceEngine(self.config)
            except ImportError:
                logger.debug("SenseVoice 模块导入失败")
                return None
        
        if engine is None:
            return None
        
        # 尝试加载模型
        if engine.load_model():
            self._engines[engine_name] = engine
            return engine
        
        return None
    
    def _detect_language(self, audio_path: str) -> str:
        """
        简单语言检测（基于 whisper 的 decode 前几秒）。
        
        策略：用 whisper tiny 模型的前 30 秒做语言检测（快速）
        """
        try:
            import whisper
            
            # 只取前30秒检测语言
            device = self.config.get("whisper", {}).get("device", "cpu") if self.config else "cpu"
            model = whisper.load_model("tiny", device=device)
            
            # 加载音频
            try:
                import soundfile as sf
                import numpy as np
                
                audio, sr = sf.read(audio_path)
                if sr != 16000:
                    import librosa
                    audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
                    sr = 16000
            except ImportError:
                # 无 soundfile/librosa 时，用 whisper 内置加载
                audio = whisper.load_audio(audio_path)
                sr = 16000
            
            # 取前30秒
            audio_30s = audio[:30 * sr]
            
            # pad or trim
            audio = whisper.pad_or_trim(audio_30s)
            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            
            # 检测语言
            _, probs = model.detect_language(mel)
            language = max(probs, key=probs.get)
            
            logger.info(f"检测到语言: {language} (置信度: {probs[language]:.2f})")
            return language
            
        except Exception as e:
            logger.debug(f"语言检测失败: {e}，默认 zh")
            return "zh"
    
    def cleanup(self):
        """清理所有引擎"""
        for engine in self._engines.values():
            engine.unload()
        self._engines.clear()
        self._active_engine = None
