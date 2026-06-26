"""
JSON Reporter - JSON 格式報告
導出測量結果為 JSON 格式
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from ..core import ResponseSpeedMeter, ResponseSpeedBenchmark


class JSONReporter:
    """JSON 報告器"""
    
    def __init__(self, 
                 output_dir: str = None,
                 pretty_print: bool = True):
        """
        初始化 JSON 報告器
        
        Args:
            output_dir: 輸出目錄
            pretty_print: 是否美化輸出
        """
        self.output_dir = Path(output_dir) if output_dir else None
        self.pretty_print = pretty_print
    
    def export_meter(self, meter: ResponseSpeedMeter) -> str:
        """導出單次測量結果"""
        summary = meter.get_summary()
        if not summary:
            return json.dumps({"error": "無測量數據"}, ensure_ascii=False)
        
        report = self._create_report(summary)
        
        if self.pretty_print:
            return json.dumps(report, indent=2, ensure_ascii=False)
        return json.dumps(report, ensure_ascii=False)
    
    def export_benchmark(self, benchmark: ResponseSpeedBenchmark) -> str:
        """導出基準測試結果"""
        stats = benchmark.get_statistics()
        if not stats:
            return json.dumps({"error": "無測試數據"}, ensure_ascii=False)
        
        report = {
            "report_type": "benchmark",
            "generated_at": datetime.now().isoformat(),
            "statistics": stats,
            "raw_results": benchmark.results
        }
        
        if self.pretty_print:
            return json.dumps(report, indent=2, ensure_ascii=False)
        return json.dumps(report, ensure_ascii=False)
    
    def _create_report(self, summary: Dict[str, Any]) -> Dict[str, Any]:
        """創建報告結構"""
        return {
            "report_type": "single_test",
            "generated_at": datetime.now().isoformat(),
            "test_info": {
                "test_id": summary.get("test_id"),
                "total_time_ms": summary.get("total_time_ms"),
                "total_time_s": summary.get("total_time_s"),
                "ttft_ms": summary.get("ttft_ms")
            },
            "stage_analysis": summary.get("stage_times", {}),
            "timing_points": summary.get("timing_points", [])
        }
    
    def save_meter(self, 
                   meter: ResponseSpeedMeter, 
                   filename: str = None) -> Path:
        """保存測量結果到文件"""
        if not self.output_dir:
            raise ValueError("未設置輸出目錄")
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = filename or f"response_test_{meter.test_id}.json"
        filepath = self.output_dir / filename
        
        content = self.export_meter(meter)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def save_benchmark(self,
                       benchmark: ResponseSpeedBenchmark,
                       filename: str = None) -> Path:
        """保存基準測試結果到文件"""
        if not self.output_dir:
            raise ValueError("未設置輸出目錄")
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filename or f"benchmark_{timestamp}.json"
        filepath = self.output_dir / filename
        
        content = self.export_benchmark(benchmark)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def export_comparison(self, 
                          results: List[Dict[str, Any]]) -> str:
        """導出比較報告"""
        report = {
            "report_type": "comparison",
            "generated_at": datetime.now().isoformat(),
            "total_tests": len(results),
            "tests": results
        }
        
        if self.pretty_print:
            return json.dumps(report, indent=2, ensure_ascii=False)
        return json.dumps(report, ensure_ascii=False)
