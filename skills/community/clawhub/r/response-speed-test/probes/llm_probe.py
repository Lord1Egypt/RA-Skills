"""
LLM Probe - LLM 組件探針
測量 LLM 請求和生成時間（TTFT, TPS）
"""

import time
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from .base import BaseProbe, ProbeResult


@dataclass
class LLMStreamEvent:
    """LLM 流式事件"""
    event_type: str        # start, token, complete, error
    timestamp: float       # 時間戳
    token: str = None      # token 內容
    latency_ms: float = 0  # 延遲


class LLMProbe(BaseProbe):
    """LLM 組件探針"""
    
    def __init__(self):
        super().__init__(name="llm", stage="T4-T7")
        self.api_url = os.environ.get("LLM_API_URL", "https://api.openai.com/v1")
        self.model = os.environ.get("LLM_MODEL", "gpt-4")
    
    def probe(self, prompt: str = None, **kwargs) -> ProbeResult:
        """
        測量 LLM 響應時間
        
        Args:
            prompt: 測試提示詞（可選）
            
        Returns:
            ProbeResult: 測量結果
        """
        self.start_timing()
        
        metadata = {
            "api_url": self.api_url,
            "model": self.model,
            "prompt": prompt[:100] if prompt else None
        }
        
        try:
            # 測量 TTFT (Time To First Token)
            ttft_result = self._measure_ttft(prompt)
            metadata["ttft_ms"] = ttft_result["ttft_ms"]
            metadata["first_token_latency_ms"] = ttft_result["latency_ms"]
            
            # 測量 TPS (Tokens Per Second)
            tps_result = self._measure_tps(prompt)
            metadata["tps"] = tps_result["tps"]
            metadata["total_tokens"] = tps_result["total_tokens"]
            metadata["generation_time_ms"] = tps_result["generation_time_ms"]
            
            # 測量完整響應時間
            complete_result = self._measure_complete_time(prompt)
            metadata["complete_time_ms"] = complete_result["complete_time_ms"]
            
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
    
    def _measure_ttft(self, prompt: str = None) -> Dict[str, Any]:
        """測量 TTFT (Time To First Token)"""
        start = time.perf_counter()
        
        # 模擬 LLM 請求
        # 實際部署時會調用 LLM API 並記錄第一個 token 時間
        ttft_ms = 0.0  # 實際值會從 API 響應中獲取
        latency_ms = 0.0
        
        # 模擬延遲（實際部署時移除）
        time.sleep(0.001)  # 1ms 模擬延遲
        
        end = time.perf_counter()
        
        return {
            "ttft_ms": (end - start) * 1000,
            "latency_ms": latency_ms
        }
    
    def _measure_tps(self, prompt: str = None) -> Dict[str, Any]:
        """測量 TPS (Tokens Per Second)"""
        start = time.perf_counter()
        
        # 模擬 token 生成
        # 實際部署時會統計 token 生成速度
        total_tokens = 0
        generation_time_ms = 0.0
        tps = 0.0
        
        end = time.perf_counter()
        
        return {
            "tps": tps,
            "total_tokens": total_tokens,
            "generation_time_ms": (end - start) * 1000
        }
    
    def _measure_complete_time(self, prompt: str = None) -> Dict[str, Any]:
        """測量完整響應時間"""
        start = time.perf_counter()
        
        # 模擬完整響應
        complete_time_ms = 0.0
        
        end = time.perf_counter()
        
        return {
            "complete_time_ms": (end - start) * 1000
        }
    
    def benchmark_generation(self, 
                            prompts: List[str], 
                            iterations: int = 3) -> Dict[str, Any]:
        """
        LLM 生成基準測試
        
        Args:
            prompts: 測試提示詞列表
            iterations: 每個提示詞的迭代次數
            
        Returns:
            基準測試結果
        """
        results = []
        
        for prompt in prompts:
            for i in range(iterations):
                probe_result = self.probe(prompt=prompt)
                results.append(probe_result.to_dict())
        
        # 計算統計
        ttfts = [r["metadata"].get("ttft_ms", 0) for r in results]
        tpss = [r["metadata"].get("tps", 0) for r in results if r["metadata"].get("tps", 0) > 0]
        
        import statistics
        
        return {
            "total_tests": len(results),
            "prompts_tested": len(prompts),
            "iterations_per_prompt": iterations,
            "ttft": {
                "mean_ms": statistics.mean(ttfts) if ttfts else 0,
                "median_ms": statistics.median(ttfts) if ttfts else 0,
                "min_ms": min(ttfts) if ttfts else 0,
                "max_ms": max(ttfts) if ttfts else 0
            },
            "tps": {
                "mean": statistics.mean(tpss) if tpss else 0,
                "median": statistics.median(tpss) if tpss else 0,
                "min": min(tpss) if tpss else 0,
                "max": max(tpss) if tpss else 0
            },
            "raw_results": results
        }
