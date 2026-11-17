"""ASR 引擎抽象基类 — 所有语音识别引擎的统一接口"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ASRSegment:
    """语音识别段"""
    id: int = 0
    start: float = 0.0
    end: float = 0.0
    text: str = ""
    confidence: float = 0.0
    words: List[Dict] = field(default_factory=list)
    speaker: Optional[str] = None
    emotion: Optional[str] = None  # SenseVoice 支持


@dataclass
class ASRResult:
    """语音识别结果"""
    text: str = ""
    language: str = "unknown"
    duration: float = 0.0
    segments: List[ASRSegment] = field(default_factory=list)
    engine_name: str = ""
    is_final: bool = True


class ASREngine(ABC):
    """
    ASR 引擎抽象基类。
    
    所有语音识别引擎必须实现此接口，保证可插拔替换。
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._model = None
        self._loaded = False
    
    @property
    @abstractmethod
    def name(self) -> str:
        """引擎名称标识"""
        pass
    
    @property
    @abstractmethod
    def supported_languages(self) -> List[str]:
        """支持的语言列表"""
        pass
    
    @property
    def is_loaded(self) -> bool:
        return self._loaded
    
    @abstractmethod
    def load_model(self) -> bool:
        """
        加载模型到内存。
        
        Returns:
            是否加载成功
        """
        pass
    
    @abstractmethod
    def transcribe(self, audio_path: str, **kwargs) -> ASRResult:
        """
        执行语音识别。
        
        Args:
            audio_path: WAV 音频文件路径
            **kwargs: 额外参数（language, beam_size 等）
            
        Returns:
            ASRResult 识别结果
        """
        pass
    
    def unload(self):
        """卸载模型释放内存"""
        self._model = None
        self._loaded = False
    
    def ensure_loaded(self):
        """确保模型已加载（延迟加载）"""
        if not self._loaded:
            self.load_model()
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(loaded={self._loaded})>"
