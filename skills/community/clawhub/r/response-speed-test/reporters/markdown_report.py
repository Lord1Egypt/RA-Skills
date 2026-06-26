"""
Markdown Reporter - Markdown 格式報告
生成適合文檔的 Markdown 報告
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from ..core import ResponseSpeedMeter, ResponseSpeedBenchmark


class MarkdownReporter:
    """Markdown 報告器"""
    
    def __init__(self, output_dir: str = None):
        """
        初始化 Markdown 報告器
        
        Args:
            output_dir: 輸出目錄
        """
        self.output_dir = Path(output_dir) if output_dir else None
    
    def export_meter(self, meter: ResponseSpeedMeter) -> str:
        """導出單次測量結果為 Markdown"""
        return meter.generate_markdown_report()
    
    def export_benchmark(self, benchmark: ResponseSpeedBenchmark) -> str:
        """導出基準測試結果為 Markdown"""
        return benchmark.generate_comparison_report()
    
    def export_detailed_report(self, meter: ResponseSpeedMeter) -> str:
        """導出詳細報告"""
        summary = meter.get_summary()
        if not summary:
            return "# 無測量數據"
        
        lines = [
            f"# ⏱️ 響應速度測試報告",
            f"",
            f"> 生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            f"## 📊 測試概覽",
            f"",
            f"| 指標 | 數值 |",
            f"|------|------|",
            f"| 測試 ID | `{summary['test_id']}` |",
            f"| 總時間 | **{summary['total_time_s']} 秒** ({summary['total_time_ms']:.3f} ms) |",
            f"| TTFT | {summary['ttft_ms']:.3f} ms |",
            f"",
            f"## 📈 階段時間分析",
            f"",
            f"| 階段 | 名稱 | 耗時 (ms) | 佔比 |",
            f"|------|------|----------:|-----:|"
        ]
        
        for stage, data in summary['stage_times'].items():
            lines.append(
                f"| {stage} | {data['name']} | {data['delta_ms']:.3f} | {data['percentage']}% |"
            )
        
        # 添加時間線
        lines.extend([
            f"",
            f"## 🕐 時間線詳細",
            f"",
            f"```",
            f"階段   名稱                       累計           增量"
        ])
        
        for point in meter.timing_points:
            lines.append(
                f"{point.stage:<6} {point.stage_name:<25} "
                f"{point.cumulative_ms:>10.3f}ms  {point.delta_ms:>10.3f}ms"
            )
        
        lines.append(f"```")
        
        # 添加圖表（使用 Mermaid 語法）
        lines.extend(self._create_mermaid_chart(meter))
        
        return "\n".join(lines)
    
    def _create_mermaid_chart(self, meter: ResponseSpeedMeter) -> List[str]:
        """創建 Mermaid 時序圖"""
        lines = [
            f"",
            f"## 📊 時序圖",
            f"",
            f"```mermaid",
            f"sequenceDiagram",
            f"    participant User",
            f"    participant Gateway",
            f"    participant Session",
            f"    participant Memory",
            f"    participant LLM",
            f"    "
        ]
        
        # 根據 timing points 生成時序
        for point in meter.timing_points:
            stage = point.stage
            if stage == "T0":
                lines.append(f"    User->>Gateway: 發送消息")
            elif stage == "T1":
                lines.append(f"    Gateway->>Session: 分發消息")
            elif stage == "T3":
                lines.append(f"    Session->>Memory: 載入記憶")
            elif stage == "T4":
                lines.append(f"    Session->>LLM: 發送請求")
            elif stage == "T5":
                lines.append(f"    LLM-->>Session: 第一個 Token")
            elif stage == "T7":
                lines.append(f"    Session-->>User: 返回響應")
        
        lines.append(f"```")
        
        return lines
    
    def save_meter(self, 
                   meter: ResponseSpeedMeter, 
                   filename: str = None) -> Path:
        """保存測量結果到文件"""
        if not self.output_dir:
            raise ValueError("未設置輸出目錄")
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = filename or f"response_test_{meter.test_id}.md"
        filepath = self.output_dir / filename
        
        content = self.export_detailed_report(meter)
        
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
        filename = filename or f"benchmark_{timestamp}.md"
        filepath = self.output_dir / filename
        
        content = self.export_benchmark(benchmark)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def export_comparison_table(self, 
                                meters: List[ResponseSpeedMeter]) -> str:
        """導出比較表格"""
        lines = [
            "# 📊 響應速度比較報告",
            "",
            f"> 測試數量：{len(meters)}",
            "",
            "| 測試 ID | 總時間 (ms) | TTFT (ms) |",
            "|---------|------------:|----------:|"
        ]
        
        for meter in meters:
            summary = meter.get_summary()
            if summary:
                lines.append(
                    f"| {summary['test_id']} | {summary['total_time_ms']:.3f} | {summary['ttft_ms']:.3f} |"
                )
        
        return "\n".join(lines)
