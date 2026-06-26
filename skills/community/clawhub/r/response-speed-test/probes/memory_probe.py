"""
Memory Probe - Memory 組件探針
測量 Soul Memory 載入和查詢時間
"""

import time
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from .base import BaseProbe, ProbeResult


class MemoryProbe(BaseProbe):
    """Memory 組件探針"""
    
    def __init__(self):
        super().__init__(name="memory", stage="T3")
        self.memory_path = os.environ.get(
            "SOUL_MEMORY_PATH", 
            "/root/.openclaw/workspace/memory"
        )
    
    def probe(self, query: str = None, **kwargs) -> ProbeResult:
        """
        測量 Memory 載入和查詢時間
        
        Args:
            query: 查詢關鍵詞（可選）
            
        Returns:
            ProbeResult: 測量結果
        """
        self.start_timing()
        
        metadata = {
            "memory_path": self.memory_path,
            "query": query
        }
        
        try:
            # 測量 Memory 載入時間
            load_result = self._measure_load_time()
            metadata["load_time_ms"] = load_result["load_time_ms"]
            metadata["segments_loaded"] = load_result["segments"]
            
            # 測量索引載入時間
            index_result = self._measure_index_load()
            metadata["index_load_time_ms"] = index_result["load_time_ms"]
            metadata["index_segments"] = index_result["segments"]
            
            # 如果有查詢，測量查詢時間
            if query:
                search_result = self._measure_search_time(query)
                metadata["search_time_ms"] = search_result["search_time_ms"]
                metadata["results_found"] = search_result["results"]
            
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
    
    def _measure_load_time(self) -> Dict[str, Any]:
        """測量 Memory 載入時間"""
        start = time.perf_counter()
        
        memory_dir = Path(self.memory_path)
        segments = 0
        
        if memory_dir.exists():
            # 統計記憶文件
            memory_files = list(memory_dir.glob("*.md"))
            segments = len(memory_files)
        
        end = time.perf_counter()
        
        return {
            "load_time_ms": (end - start) * 1000,
            "segments": segments
        }
    
    def _measure_index_load(self) -> Dict[str, Any]:
        """測量索引載入時間"""
        start = time.perf_counter()
        
        # 檢查索引文件
        index_file = Path(self.memory_path) / "index.json"
        segments = 0
        
        if index_file.exists():
            import json
            with open(index_file) as f:
                index_data = json.load(f)
                segments = index_data.get("total_segments", 0)
        
        end = time.perf_counter()
        
        return {
            "load_time_ms": (end - start) * 1000,
            "segments": segments
        }
    
    def _measure_search_time(self, query: str) -> Dict[str, Any]:
        """測量查詢時間"""
        start = time.perf_counter()
        
        # 模擬搜索
        # 實際部署時會調用 Soul Memory API
        results = 0
        
        end = time.perf_counter()
        
        return {
            "search_time_ms": (end - start) * 1000,
            "results": results
        }
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """獲取 Memory 統計信息"""
        memory_dir = Path(self.memory_path)
        
        stats = {
            "memory_path": str(memory_dir),
            "exists": memory_dir.exists(),
            "total_files": 0,
            "total_size_kb": 0,
            "segments": 0
        }
        
        if memory_dir.exists():
            memory_files = list(memory_dir.glob("*.md"))
            stats["total_files"] = len(memory_files)
            stats["total_size_kb"] = sum(f.stat().st_size for f in memory_files) / 1024
            stats["segments"] = len(memory_files)
        
        return stats
