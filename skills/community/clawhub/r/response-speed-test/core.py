"""
Response Speed Test - Core Measurement Engine
精確測量 OpenClaw 系統響應速度的核心引擎

Author: kingofqin2026
Version: 1.0.0
"""

import time
import json
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, List
import statistics


@dataclass
class TimingPoint:
    """時間測量點"""
    stage: str              # 階段名稱 (T0, T1, ...)
    stage_name: str         # 階段描述
    timestamp: float        # Unix 時間戳（秒，含毫秒）
    delta_ms: float         # 與上一階段的時間差（毫秒）
    cumulative_ms: float    # 累計時間（毫秒）
    metadata: Dict = field(default_factory=dict)  # 附加信息


class ResponseSpeedMeter:
    """響應速度測量器"""
    
    STAGE_NAMES = {
        "T0": "MESSAGE_SENT",
        "T1": "GATEWAY_RECEIVE",
        "T2": "SESSION_DISPATCH",
        "T3": "MEMORY_LOAD_COMPLETE",
        "T4": "LLM_REQUEST_START",
        "T5": "LLM_FIRST_TOKEN",
        "T6": "LLM_RESPONSE_COMPLETE",
        "T7": "MESSAGE_DELIVERED",
        "T8": "COMPLETE"
    }
    
    def __init__(self, test_id: str = None):
        self.test_id = test_id or datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        self.timing_points: List[TimingPoint] = []
        self._start_time: Optional[float] = None
        self._last_time: Optional[float] = None
    
    def start(self, metadata: Dict = None) -> 'ResponseSpeedMeter':
        """開始測量 - 記錄 T0"""
        self._start_time = time.perf_counter()
        self._last_time = self._start_time
        self._record_point("T0", metadata or {})
        return self
    
    def checkpoint(self, stage: str, metadata: Dict = None) -> 'ResponseSpeedMeter':
        """記錄檢查點"""
        if stage not in self.STAGE_NAMES:
            raise ValueError(f"Unknown stage: {stage}")
        self._record_point(stage, metadata or {})
        return self
    
    def end(self, metadata: Dict = None) -> 'ResponseSpeedMeter':
        """結束測量 - 記錄 T8"""
        self._record_point("T8", metadata or {})
        return self
    
    def _record_point(self, stage: str, metadata: Dict):
        """記錄時間點"""
        current = time.perf_counter()
        delta_ms = (current - self._last_time) * 1000 if self._last_time else 0
        cumulative_ms = (current - self._start_time) * 1000 if self._start_time else 0
        
        point = TimingPoint(
            stage=stage,
            stage_name=self.STAGE_NAMES.get(stage, "UNKNOWN"),
            timestamp=current,
            delta_ms=round(delta_ms, 3),
            cumulative_ms=round(cumulative_ms, 3),
            metadata=metadata
        )
        self.timing_points.append(point)
        self._last_time = current
    
    @property
    def ttft(self) -> float:
        """Time To First Token (T5 - T4)"""
        t4 = next((p for p in self.timing_points if p.stage == "T4"), None)
        t5 = next((p for p in self.timing_points if p.stage == "T5"), None)
        if t4 and t5:
            return round(t5.cumulative_ms - t4.cumulative_ms, 3)
        return 0
    
    @property
    def total_time_ms(self) -> float:
        """總響應時間"""
        if len(self.timing_points) < 2:
            return 0
        return self.timing_points[-1].cumulative_ms
    
    @property
    def total_time_s(self) -> float:
        """總響應時間（秒）"""
        return round(self.total_time_ms / 1000, 3)
    
    def get_summary(self) -> Dict:
        """獲取測量摘要"""
        if len(self.timing_points) < 2:
            return {}
        
        total_time = self.total_time_ms
        
        # 計算各階段時間
        stage_times = {}
        for point in self.timing_points[1:]:
            stage_times[point.stage] = {
                "name": point.stage_name,
                "delta_ms": point.delta_ms,
                "percentage": round(point.delta_ms / total_time * 100, 2) if total_time > 0 else 0
            }
        
        return {
            "test_id": self.test_id,
            "total_time_ms": round(total_time, 3),
            "total_time_s": self.total_time_s,
            "ttft_ms": self.ttft,
            "stage_times": stage_times,
            "timing_points": [asdict(p) for p in self.timing_points]
        }
    
    def generate_markdown_report(self) -> str:
        """生成 Markdown 報告"""
        summary = self.get_summary()
        if not summary:
            return "無測量數據"
        
        lines = [
            f"# ⏱️ 響應速度測試報告",
            f"",
            f"**測試 ID**: `{self.test_id}`",
            f"**總時間**: {summary['total_time_s']} 秒 ({summary['total_time_ms']:.3f} ms)",
            f"**TTFT**: {summary['ttft_ms']:.3f} ms",
            f"",
            f"## 📊 各階段時間分析",
            f"",
            f"| 階段 | 名稱 | 耗時 | 佔比 |",
            f"|------|------|-------------|------|"
        ]
        
        for stage, data in summary['stage_times'].items():
            lines.append(
                f"| {stage} | {data['name']} | **{data['delta_ms']:.3f}** | {data['percentage']}% |"
            )
        
        lines.extend([
            f"",
            f"## 📈 時間線詳細",
            f"",
            f"```",
            f"{'階段':<6} {'名稱':<25} {'累計':<15} {'增量':<15}",
            f"{'-'*65}"
        ])
        
        for point in self.timing_points:
            lines.append(
                f"{point.stage:<6} {point.stage_name:<25} "
                f"{point.cumulative_ms:>10.3f}ms {point.delta_ms:>10.3f}ms"
            )
        
        lines.append(f"```")
        return "\n".join(lines)
    
    def to_json(self) -> str:
        """導出為 JSON"""
        return json.dumps(self.get_summary(), indent=2, ensure_ascii=False)


class ResponseSpeedBenchmark:
    """響應速度基準測試"""
    
    def __init__(self):
        self.results: List[Dict] = []
    
    def add_result(self, meter: ResponseSpeedMeter):
        """添加測試結果"""
        self.results.append(meter.get_summary())
    
    def get_statistics(self) -> Dict:
        """獲取統計數據"""
        if not self.results:
            return {}
        
        times = [r['total_time_ms'] for r in self.results]
        ttfts = [r['ttft_ms'] for r in self.results]
        
        def percentile(data: List[float], p: float) -> float:
            sorted_data = sorted(data)
            k = (len(sorted_data) - 1) * p / 100
            f = int(k)
            c = f + 1 if f + 1 < len(sorted_data) else f
            return sorted_data[f] + (k - f) * (sorted_data[c] - sorted_data[f])
        
        return {
            "iterations": len(self.results),
            "total_time": {
                "mean_ms": round(statistics.mean(times), 3),
                "median_ms": round(statistics.median(times), 3),
                "std_dev_ms": round(statistics.stdev(times), 3) if len(times) > 1 else 0,
                "min_ms": round(min(times), 3),
                "max_ms": round(max(times), 3),
                "p95_ms": round(percentile(times, 95), 3),
                "p99_ms": round(percentile(times, 99), 3)
            },
            "ttft": {
                "mean_ms": round(statistics.mean(ttfts), 3),
                "median_ms": round(statistics.median(ttfts), 3),
                "min_ms": round(min(ttfts), 3),
                "max_ms": round(max(ttfts), 3)
            }
        }
    
    def generate_comparison_report(self) -> str:
        """生成比較報告"""
        stats = self.get_statistics()
        if not stats:
            return "無測試數據"
        
        lines = [
            "# 📊 基準測試報告",
            "",
            f"**測試次數**: {stats['iterations']}",
            "",
            "## 總響應時間統計",
            "",
            "| 指標 | 數值 |",
            "|------|------|"
        ]
        
        for key, value in stats['total_time'].items():
            lines.append(f"| {key} | {value:.3f} ms |")
        
        lines.extend([
            "",
            "## TTFT 統計",
            "",
            "| 指標 | 數值 |",
            "|------|------|"
        ])
        
        for key, value in stats['ttft'].items():
            lines.append(f"| {key} | {value:.3f} ms |")
        
        return "\n".join(lines)


# 使用範例
if __name__ == "__main__":
    # 創建測量器
    meter = ResponseSpeedMeter("test_001")
    
    # 模擬測量過程
    meter.start({"message": "測試消息"})
    
    time.sleep(0.05)  # 模擬 Gateway 處理
    meter.checkpoint("T1", {"gateway": "openclaw-gateway"})
    
    time.sleep(0.01)  # 模擬 Session 分發
    meter.checkpoint("T2", {"session": "main"})
    
    time.sleep(0.15)  # 模擬 Memory 載入
    meter.checkpoint("T3", {"segments": 89})
    
    time.sleep(0.01)  # 模擬 LLM 請求開始
    meter.checkpoint("T4", {"model": "glm5"})
    
    time.sleep(1.2)  # 模擬 TTFT
    meter.checkpoint("T5", {"first_token": True})
    
    time.sleep(0.8)  # 模擬生成完成
    meter.checkpoint("T6", {"completion_tokens": 100})
    
    time.sleep(0.03)  # 模擬消息發送
    meter.checkpoint("T7", {"delivered": True})
    
    meter.end()
    
    # 輸出報告
    print(meter.generate_markdown_report())
