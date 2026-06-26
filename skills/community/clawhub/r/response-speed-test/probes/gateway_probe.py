"""
Gateway Probe - Gateway 組件探針
測量 Gateway 消息接收和處理時間
"""

import time
import os
import json
from typing import Dict, Any, Optional
from .base import BaseProbe, ProbeResult


class GatewayProbe(BaseProbe):
    """Gateway 組件探針"""
    
    def __init__(self):
        super().__init__(name="gateway", stage="T1")
        self.gateway_url = os.environ.get("OPENCLAW_GATEWAY_URL", "http://localhost:3000")
    
    def probe(self, message_id: str = None, **kwargs) -> ProbeResult:
        """
        測量 Gateway 響應時間
        
        Args:
            message_id: 消息 ID（可選）
            
        Returns:
            ProbeResult: 測量結果
        """
        self.start_timing()
        
        metadata = {
            "gateway_url": self.gateway_url,
            "message_id": message_id
        }
        
        try:
            # 模擬 Gateway 處理測量
            # 實際部署時會調用 Gateway API
            start = time.perf_counter()
            
            # 檢查 Gateway 狀態
            gateway_status = self._check_gateway_status()
            metadata["gateway_status"] = gateway_status
            
            # 測量消息處理延遲
            processing_delay = self._measure_processing_delay()
            metadata["processing_delay_ms"] = processing_delay
            
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
    
    def _check_gateway_status(self) -> str:
        """檢查 Gateway 狀態"""
        # 實際部署時會調用 Gateway 健康檢查 API
        # 這裡模擬返回
        return "healthy"
    
    def _measure_processing_delay(self) -> float:
        """測量處理延遲"""
        # 模擬處理延遲測量
        # 實際部署時會測量消息從接收到分發的時間
        return 0.0  # ms
    
    def measure_throughput(self, duration_seconds: int = 10) -> Dict[str, Any]:
        """
        測量 Gateway 吞吐量
        
        Args:
            duration_seconds: 測量時長（秒）
            
        Returns:
            吞吐量統計
        """
        # 實際部署時會統計一段時間內處理的消息數
        return {
            "duration_seconds": duration_seconds,
            "messages_processed": 0,
            "messages_per_second": 0.0,
            "avg_latency_ms": 0.0
        }
