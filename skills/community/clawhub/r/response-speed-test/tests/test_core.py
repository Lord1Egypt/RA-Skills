"""
Test Core - 核心模組測試
"""

import unittest
import time
from ..core import ResponseSpeedMeter, TimingPoint, ResponseSpeedBenchmark


class TestResponseSpeedMeter(unittest.TestCase):
    """ResponseSpeedMeter 測試"""
    
    def setUp(self):
        """測試前置"""
        self.meter = ResponseSpeedMeter("test_001")
    
    def test_initialization(self):
        """測試初始化"""
        self.assertEqual(self.meter.test_id, "test_001")
        self.assertEqual(len(self.meter.timing_points), 0)
    
    def test_start(self):
        """測試開始"""
        self.meter.start({"message": "test"})
        self.assertEqual(len(self.meter.timing_points), 1)
        self.assertEqual(self.meter.timing_points[0].stage, "T0")
    
    def test_checkpoint(self):
        """測試檢查點"""
        self.meter.start()
        self.meter.checkpoint("T1", {"gateway": "test"})
        
        self.assertEqual(len(self.meter.timing_points), 2)
        self.assertEqual(self.meter.timing_points[1].stage, "T1")
    
    def test_end(self):
        """測試結束"""
        self.meter.start()
        self.meter.end()
        
        self.assertEqual(len(self.meter.timing_points), 2)
        self.assertEqual(self.meter.timing_points[-1].stage, "T8")
    
    def test_full_measurement(self):
        """測試完整測量"""
        self.meter.start({"message": "test"})
        time.sleep(0.01)
        self.meter.checkpoint("T1")
        time.sleep(0.01)
        self.meter.checkpoint("T2")
        self.meter.end()
        
        self.assertTrue(self.meter.total_time_ms > 0)
        self.assertTrue(self.meter.total_time_s > 0)
    
    def test_ttft(self):
        """測試 TTFT 計算"""
        self.meter.start()
        self.meter.checkpoint("T4")
        time.sleep(0.01)
        self.meter.checkpoint("T5")
        self.meter.end()
        
        self.assertTrue(self.meter.ttft > 0)
    
    def test_get_summary(self):
        """測試獲取摘要"""
        self.meter.start()
        self.meter.checkpoint("T1")
        self.meter.end()
        
        summary = self.meter.get_summary()
        
        self.assertIn("test_id", summary)
        self.assertIn("total_time_ms", summary)
        self.assertIn("stage_times", summary)
    
    def test_generate_markdown_report(self):
        """測試生成 Markdown 報告"""
        self.meter.start()
        self.meter.checkpoint("T1")
        self.meter.end()
        
        report = self.meter.generate_markdown_report()
        
        self.assertIn("#", report)
        self.assertIn("test_001", report)
    
    def test_to_json(self):
        """測試 JSON 導出"""
        self.meter.start()
        self.meter.end()
        
        json_str = self.meter.to_json()
        
        self.assertIn("test_id", json_str)
        self.assertIn("total_time_ms", json_str)


class TestResponseSpeedBenchmark(unittest.TestCase):
    """ResponseSpeedBenchmark 測試"""
    
    def setUp(self):
        """測試前置"""
        self.benchmark = ResponseSpeedBenchmark()
    
    def test_add_result(self):
        """測試添加結果"""
        meter = ResponseSpeedMeter()
        meter.start()
        meter.end()
        
        self.benchmark.add_result(meter)
        
        self.assertEqual(len(self.benchmark.results), 1)
    
    def test_get_statistics(self):
        """測試獲取統計"""
        for i in range(5):
            meter = ResponseSpeedMeter(f"test_{i}")
            meter.start()
            time.sleep(0.01 * (i + 1))
            meter.end()
            self.benchmark.add_result(meter)
        
        stats = self.benchmark.get_statistics()
        
        self.assertEqual(stats['iterations'], 5)
        self.assertIn('total_time', stats)
        self.assertIn('ttft', stats)
    
    def test_generate_comparison_report(self):
        """測試生成比較報告"""
        for i in range(3):
            meter = ResponseSpeedMeter(f"test_{i}")
            meter.start()
            meter.end()
            self.benchmark.add_result(meter)
        
        report = self.benchmark.generate_comparison_report()
        
        self.assertIn("#", report)
        self.assertIn("測試次數", report)


class TestTimingPoint(unittest.TestCase):
    """TimingPoint 測試"""
    
    def test_timing_point_creation(self):
        """測試時間點創建"""
        point = TimingPoint(
            stage="T0",
            stage_name="MESSAGE_SENT",
            timestamp=time.time(),
            delta_ms=0.0,
            cumulative_ms=0.0
        )
        
        self.assertEqual(point.stage, "T0")
        self.assertEqual(point.stage_name, "MESSAGE_SENT")


if __name__ == '__main__':
    unittest.main()
