"""
Console Reporter - 控制台輸出報告
實時顯示測量結果到終端
"""

import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..core import ResponseSpeedMeter, ResponseSpeedBenchmark


class ConsoleReporter:
    """控制台報告器"""
    
    # ANSI 顏色代碼
    COLORS = {
        "reset": "\033[0m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "bold": "\033[1m",
        "dim": "\033[2m"
    }
    
    def __init__(self, 
                 use_colors: bool = True,
                 verbose: bool = False):
        """
        初始化控制台報告器
        
        Args:
            use_colors: 是否使用顏色
            verbose: 是否顯示詳細信息
        """
        self.use_colors = use_colors
        self.verbose = verbose
    
    def _color(self, text: str, color: str) -> str:
        """添加顏色"""
        if not self.use_colors:
            return text
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"
    
    def report_meter(self, meter: ResponseSpeedMeter) -> None:
        """報告單次測量結果"""
        summary = meter.get_summary()
        if not summary:
            print(self._color("無測量數據", "yellow"))
            return
        
        # 標題
        print()
        print(self._color("⏱️  響應速度測試報告", "bold"))
        print(self._color("=" * 50, "dim"))
        
        # 基本信息
        print(f"\n{self._color('測試 ID:', 'cyan')} {summary['test_id']}")
        print(f"{self._color('總時間:', 'cyan')} {self._color(f'{summary[\"total_time_s\"]} 秒', 'green')} ({summary['total_time_ms']:.3f} ms)")
        print(f"{self._color('TTFT:', 'cyan')} {self._color(f'{summary[\"ttft_ms\"]:.3f} ms', 'yellow')}")
        
        # 階段時間
        print(f"\n{self._color('📊 各階段時間分析', 'bold')}")
        print(self._color("-" * 50, "dim"))
        
        for stage, data in summary['stage_times'].items():
            name = data['name']
            delta = data['delta_ms']
            percentage = data['percentage']
            
            # 根據時間長度選擇顏色
            if delta < 100:
                color = "green"
            elif delta < 500:
                color = "yellow"
            else:
                color = "red"
            
            bar = self._create_bar(percentage)
            print(f"  {stage} {name:<25} {self._color(f'{delta:>8.3f} ms', color)} {bar}")
        
        print()
    
    def report_benchmark(self, benchmark: ResponseSpeedBenchmark) -> None:
        """報告基準測試結果"""
        stats = benchmark.get_statistics()
        if not stats:
            print(self._color("無測試數據", "yellow"))
            return
        
        # 標題
        print()
        print(self._color("📊 基準測試報告", "bold"))
        print(self._color("=" * 50, "dim"))
        
        print(f"\n{self._color('測試次數:', 'cyan')} {stats['iterations']}")
        
        # 總響應時間統計
        print(f"\n{self._color('📈 總響應時間統計', 'bold')}")
        print(self._color("-" * 30, "dim"))
        
        for key, value in stats['total_time'].items():
            print(f"  {key:<15} {self._color(f'{value:.3f} ms', 'green')}")
        
        # TTFT 統計
        print(f"\n{self._color('⚡ TTFT 統計', 'bold')}")
        print(self._color("-" * 30, "dim"))
        
        for key, value in stats['ttft'].items():
            print(f"  {key:<15} {self._color(f'{value:.3f} ms', 'yellow')}")
        
        print()
    
    def _create_bar(self, percentage: float, width: int = 20) -> str:
        """創建進度條"""
        filled = int(percentage / 100 * width)
        empty = width - filled
        return self._color("█" * filled + "░" * empty, "dim")
    
    def report_live(self, meter: ResponseSpeedMeter) -> None:
        """實時報告（用於流式輸出）"""
        # 簡化版本，實際可以支持動態更新
        pass
    
    def print_separator(self, char: str = "-", length: int = 50) -> None:
        """打印分隔線"""
        print(self._color(char * length, "dim"))
    
    def print_header(self, text: str) -> None:
        """打印標題"""
        print(f"\n{self._color(text, 'bold')}")
        self.print_separator()
