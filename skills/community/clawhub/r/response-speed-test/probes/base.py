"""
Base Probe - 探針基礎類
所有探針模組的父類，定義統一接口
"""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class ProbeResult:
    """探針測量結果"""
    probe_name: str                    # 探針名稱
    stage: str                         # 測量階段 (T0-T8)
    success: bool                      # 是否成功
    duration_ms: float                 # 耗時（毫秒）
    timestamp: float                   # Unix 時間戳
    metadata: Dict[str, Any] = field(default_factory=dict)  # 附加信息
    error: Optional[str] = None        # 錯誤信息
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return {
            "probe_name": self.probe_name,
            "stage": self.stage,
            "success": self.success,
            "duration_ms": round(self.duration_ms, 3),
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "error": self.error
        }


class BaseProbe(ABC):
    """探針基礎類"""
    
    def __init__(self, name: str, stage: str):
        """
        初始化探針
        
        Args:
            name: 探針名稱
            stage: 測量階段 (T0-T8)
        """
        self.name = name
        self.stage = stage
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None
    
    def start_timing(self) -> float:
        """開始計時"""
        self._start_time = time.perf_counter()
        return self._start_time
    
    def end_timing(self) -> float:
        """結束計時"""
        self._end_time = time.perf_counter()
        return self._end_time
    
    @property
    def duration_ms(self) -> float:
        """獲取耗時（毫秒）"""
        if self._start_time is None or self._end_time is None:
            return 0
        return (self._end_time - self._start_time) * 1000
    
    @abstractmethod
    def probe(self, **kwargs) -> ProbeResult:
        """
        執行探測（子類實現）
        
        Returns:
            ProbeResult: 測量結果
        """
        pass
    
    def _create_result(self, 
                       success: bool, 
                       metadata: Dict[str, Any] = None,
                       error: str = None) -> ProbeResult:
        """創建測量結果"""
        return ProbeResult(
            probe_name=self.name,
            stage=self.stage,
            success=success,
            duration_ms=self.duration_ms,
            timestamp=time.time(),
            metadata=metadata or {},
            error=error
        )
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} stage={self.stage}>"
