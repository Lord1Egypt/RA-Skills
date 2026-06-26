"""
Session Probe - Session 組件探針
測量 Session 分發和處理時間
"""

import time
import os
from typing import Dict, Any, Optional
from .base import BaseProbe, ProbeResult


class SessionProbe(BaseProbe):
    """Session 組件探針"""
    
    def __init__(self):
        super().__init__(name="session", stage="T2")
        self.state_dir = os.environ.get("OPENCLAW_STATE_DIR", "/root/.openclaw/state")
    
    def probe(self, session_key: str = None, **kwargs) -> ProbeResult:
        """
        測量 Session 響應時間
        
        Args:
            session_key: Session 鍵（可選）
            
        Returns:
            ProbeResult: 測量結果
        """
        self.start_timing()
        
        metadata = {
            "session_key": session_key,
            "state_dir": self.state_dir
        }
        
        try:
            # 測量 Session 分發時間
            dispatch_time = self._measure_dispatch_time(session_key)
            metadata["dispatch_time_ms"] = dispatch_time
            
            # 獲取 Session 信息
            session_info = self._get_session_info(session_key)
            metadata["session_info"] = session_info
            
            self.end_timing()
            
            metadata["total_probe_time_ms"] = round(self.duration_ms, 3)
            
            return self._create_result(
                success=True,
                metadata=metadata
            )
            
        except Exception as e:
            self.end_timing()
            return self._create_result(
                success=False,
                metadata=metadata,
                error=str(e)
            )
    
    def _measure_dispatch_time(self, session_key: str = None) -> float:
        """測量分發時間"""
        start = time.perf_counter()
        # 模擬 Session 分發
        # 實際部署時會測量消息從 Gateway 到 Session 的時間
        end = time.perf_counter()
        return (end - start) * 1000
    
    def _get_session_info(self, session_key: str = None) -> Dict[str, Any]:
        """獲取 Session 信息"""
        info = {
            "active": True,
            "created_at": None,
            "last_activity": None
        }
        
        # 實際部署時會讀取 Session 狀態文件
        # 這裡返回基本信息
        
        return info
    
    def list_active_sessions(self) -> Dict[str, Any]:
        """列出所有活躍 Session"""
        # 實際部署時會掃描 state 目錄
        return {
            "total_sessions": 0,
            "active_sessions": [],
            "state_dir": self.state_dir
        }
