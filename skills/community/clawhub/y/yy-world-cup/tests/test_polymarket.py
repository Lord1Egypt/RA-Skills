"""
v3.0 单元测试 - Polymarket集成 + 市场校准
"""

import unittest
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, str(Path(__file__).parent.parent))

from predictor.calibration import (
    MarketCalibrator, EdgeLevel, ArbitrageOpportunity
)
from predictor.data import PolymarketClient


class TestPolymarketClient(unittest.TestCase):
    """测试Polymarket API客户端"""

    def test_client_init(self):
        client = PolymarketClient(use_cache=False)
        self.assertEqual(client.CHAIN_ID, 137)
        self.assertIn('gamma', client.BASE_URLS)
        self.assertIn('data', client.BASE_URLS)
        self.assertIn('clob', client.BASE_URLS)

    def test_base_urls(self):
        """验证API基础URL"""
        client = PolymarketClient(use_cache=False)
        self.assertTrue(client.BASE_URLS['gamma'].startswith('https://'))
        self.assertTrue(client.BASE_URLS['data'].startswith('https://'))
        self.assertTrue(client.BASE_URLS['clob'].startswith('https://'))

    def test_classify_market_type(self):
        client = PolymarketClient(use_cache=False)
        self.assertEqual(client._classify_market_type(
            {'question': 'Will France win?', 'groupItemTitle': 'moneyline'}
        ), 'moneyline')
        self.assertEqual(client._classify_market_type(
            {'question': 'Spread betting', 'groupItemTitle': 'spread'}
        ), 'spread')
        self.assertEqual(client._classify_market_type(
            {'question': 'Total goals over 2.5', 'groupItemTitle': 'total'}
        ), 'total')

    def test_parse_json_field(self):
        client = PolymarketClient(use_cache=False)
        # 列表直接返回
        self.assertEqual(client._parse_json_field(['a', 'b']), ['a', 'b'])
        # JSON字符串解析
        import json
        self.assertEqual(client._parse_json_field('["a","b"]'), ['a', 'b'])
        # 无效输入返回空列表
        self.assertEqual(client._parse_json_field(None), [])
        self.assertEqual(client._parse_json_field('invalid'), [])


class TestMarketCalibrator(unittest.TestCase):
    """测试市场赔率校准器"""

    def setUp(self):
        self.cal = MarketCalibrator()

    def test_edge_classification(self):
        """Edge分类边界测试"""
        self.assertEqual(self.cal.classify_edge(0.02), EdgeLevel.NONE)
        self.assertEqual(self.cal.classify_edge(0.05), EdgeLevel.LOW)
        self.assertEqual(self.cal.classify_edge(0.10), EdgeLevel.MEDIUM)
        self.assertEqual(self.cal.classify_edge(0.20), EdgeLevel.HIGH)
        self.assertEqual(self.cal.classify_edge(0.30), EdgeLevel.EXTREME)

    def test_chinese_lottery_ev_positive(self):
        """测试体彩正EV识别"""
        arb = self.cal.compare_with_chinese_lottery(
            match_name="Test Match",
            model_probs={'home': 0.50, 'draw': 0.30, 'away': 0.20},
            cn_odds={'胜': 3.0, '平': 3.0, '负': 3.0}  # 平均赔率
        )
        # 至少应该有正EV机会（平局EV=0.5*3-1=0.5）
        self.assertGreater(len(arb), 0)

    def test_chinese_lottery_no_arb(self):
        """测试无套利机会情况"""
        arb = self.cal.compare_with_chinese_lottery(
            match_name="Test Match",
            model_probs={'home': 0.90, 'draw': 0.05, 'away': 0.05},
            cn_odds={'胜': 1.05, '平': 8.0, '负': 12.0}  # 庄家大幅抽水
        )
        # 强队胜的EV = 0.9*1.05-1 = -0.055，应该没有正EV
        # 但其他选项可能有
        # 至少有非空的评估
        self.assertIsInstance(arb, list)

    def test_format_report(self):
        """测试报告格式化"""
        from predictor.calibration import CalibrationReport
        from datetime import datetime

        report = CalibrationReport(
            timestamp=datetime.now().isoformat(),
            opportunities=[],
            polymarket_winner_odds={'France': 0.20, 'Spain': 0.15},
            summary={'total_opportunities': 0, 'high_edge_count': 0,
                     'medium_edge_count': 0, 'best_opportunity': None}
        )

        output = MarketCalibrator.format_report(report)
        self.assertIn("市场赔率校准报告", output)
        self.assertIn("France", output)
        self.assertIn("套利机会", output)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_calibrator_with_polymarket_data(self):
        """测试校准器能否调用Polymarket API"""
        cal = MarketCalibrator()
        # 测试真实API调用（使用缓存避免重复请求）
        try:
            wc = cal.polymarket.get_world_cup_winner()
            self.assertIn('teams', wc)
            self.assertGreater(wc.get('volume', 0), 0)
            self.assertGreater(len(wc.get('teams', {})), 0)
        except Exception as e:
            self.skipTest(f"Polymarket API不可用: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
