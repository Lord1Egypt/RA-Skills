"""OCR 引擎抽象基类 — 所有 OCR 引擎的统一接口"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OCRResult:
    """OCR 识别结果"""
    bbox: List[List[int]] = field(default_factory=list)  # [x1,y1,x2,y2]
    text: str = ""
    confidence: float = 0.0
    lang: str = "auto"


@dataclass
class OCRFrameResult:
    """单帧 OCR 结果"""
    texts: List[OCRResult] = field(default_factory=list)
    full_text: str = ""
    lang: str = "auto"


class OCREngine(ABC):
    """
    OCR 引擎抽象基类。
    
    所有 OCR 引擎必须实现此接口，保证可插拔替换。
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._engine = None
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
        加载 OCR 模型到内存。
        
        Returns:
            是否加载成功
        """
        pass
    
    @abstractmethod
    def recognize(self, image_path: str, **kwargs) -> OCRFrameResult:
        """
        对图像执行 OCR 识别。
        
        Args:
            image_path: 图像文件路径
            **kwargs: 额外参数
            
        Returns:
            OCRFrameResult 识别结果
        """
        pass
    
    def unload(self):
        """卸载模型释放内存"""
        self._engine = None
        self._loaded = False
    
    def ensure_loaded(self):
        """确保模型已加载"""
        if not self._loaded:
            self.load_model()
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(loaded={self._loaded})>"
