#!/usr/bin/env python3
"""
compute_gaps.py 單元測試

運行：
    pytest tests/test_compute_gaps.py -v
"""

import sys
import os
import math
import json
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from compute_gaps import (
    compute_gaps,
    _compute_days_remaining,
    _compute_urgency_tag,
    _compute_ease_tag,
    _sort_gaps,
    _compute_avg_premium_per_case,
    _compute_avg_daily_capacity,
)


class TestUrgencyTag:
    """測試緊急度標籤計算"""

    def test_urgency_critical(self):
        assert _compute_urgency_tag(7) == "緊急"
        assert _compute_urgency_tag(0) == "緊急"
        assert _compute_urgency_tag(-1) == "緊急"

    def test_urgency_important(self):
        assert _compute_urgency_tag(8) == "重要"
        assert _compute_urgency_tag(30) == "重要"

    def test_urgency_normal(self):
        assert _compute_urgency_tag(31) == "常規"
        assert _compute_urgency_tag(100) == "常規"

    def test_urgency_none(self):
        assert _compute_urgency_tag(None) == "常規"


class TestEaseTag:
    """測試容易度標籤計算"""

    def test_ease_easy(self):
        assert _compute_ease_tag(5000, 1000, 10) == "容易"
        assert _compute_ease_tag(5000, 1000, 100) == "容易"

    def test_ease_not_easy(self):
        assert _compute_ease_tag(50000, 100, 10) is None
        assert _compute_ease_tag(50000, 1000, 1) is None

    def test_ease_no_days(self):
        assert _compute_ease_tag(5000, 1000, None) is None

    def test_ease_zero_capacity(self):
        assert _compute_ease_tag(5000, 0, 10) is None


class TestAvgPremiumPerCase:
    """測試件均保費計算"""

    def test_normal(self):
        data = {"personalPremium": 250000, "personalPolicyNum": 10}
        assert _compute_avg_premium_per_case(data) == 25000.0

    def test_half_policy(self):
        data = {"personalPremium": 12500, "personalPolicyNum": 0.5}
        assert _compute_avg_premium_per_case(data) == 25000.0

    def test_missing_data(self):
        assert _compute_avg_premium_per_case({}) is None
        assert _compute_avg_premium_per_case(None) is None

    def test_zero_policy(self):
        data = {"personalPremium": 100000, "personalPolicyNum": 0}
        assert _compute_avg_premium_per_case(data) is None


class TestAvgDailyCapacity:
    """測試日均產能計算"""

    def test_personal_capacity(self):
        data = {"personalPremium": 180000}
        assert _compute_avg_daily_capacity(data) == 1000.0

    def test_company_fallback(self):
        data = {"companyYtdPremium": 36000000, "activeAgentCount": 100}
        result = _compute_avg_daily_capacity(data)
        expected = 36000000 / 100 / 180
        assert abs(result - expected) < 0.01

    def test_no_data(self):
        assert _compute_avg_daily_capacity({}) == 0.0
        assert _compute_avg_daily_capacity(None) == 0.0


class TestSortGaps:
    """測試缺口排序"""

    def test_sort_by_urgency(self):
        gaps = [
            {"gapName": "A", "urgencyTag": "常規", "gapAmount": 100000},
            {"gapName": "B", "urgencyTag": "緊急", "gapAmount": 10000},
            {"gapName": "C", "urgencyTag": "重要", "gapAmount": 50000},
        ]
        sorted_gaps = _sort_gaps(gaps)
        assert sorted_gaps[0]["gapName"] == "B"
        assert sorted_gaps[1]["gapName"] == "C"
        assert sorted_gaps[2]["gapName"] == "A"

    def test_sort_by_amount_within_same_urgency(self):
        gaps = [
            {"gapName": "A", "urgencyTag": "緊急", "gapAmount": 10000},
            {"gapName": "B", "urgencyTag": "緊急", "gapAmount": 50000},
        ]
        sorted_gaps = _sort_gaps(gaps)
        assert sorted_gaps[0]["gapName"] == "B"
        assert sorted_gaps[1]["gapName"] == "A"


class TestComputeGapsIntegration:
    """集成測試"""

    def test_no_data(self):
        result = compute_gaps()
        assert result["gapIndicators"] == []
        assert result["diagnosis"]["skillGap"] == []
        assert "dataAsOfDate" in result

    def test_campaign_gaps(self):
        campaign_data = {
            "competitionList": [
                {
                    "competitionName": "2026 Q2 業績衝刺",
                    "gapIndicators": [
                        {
                            "blockName": "Q2 保障保費里程碑",
                            "indicatorName": "保障保費",
                            "targetVal": 500000,
                            "actualVal": 350000,
                            "gapVal": 150000,
                            "unit": "AMOUNT",
                            "deadline": "2026-06-30"
                        }
                    ],
                    "knowledgeQueryHint": "2026 Q2 業績衝刺攻略"
                }
            ]
        }
        perf_data = {"personalPremium": 350000, "personalPolicyNum": 14}
        result = compute_gaps(performance_data=perf_data, campaign_data=campaign_data)

        assert len(result["gapIndicators"]) == 1
        gap = result["gapIndicators"][0]
        assert gap["gapName"] == "2026 Q2 業績衝刺保障保費"
        assert gap["gapAmount"] == 150000
        assert gap["urgencyTag"] in ["緊急", "重要", "常規"]
        assert "knowledgeRetrievalHints" in result
        assert "2026 Q2 業績衝刺攻略" in result["knowledgeRetrievalHints"]

    def test_honor_qualified_skipped(self):
        honor_data = {
            "honorList": [
                {
                    "honorName": "百萬圓桌",
                    "isQualified": True,
                    "gapAmt": 0,
                    "items": []
                }
            ]
        }
        result = compute_gaps(honor_data=honor_data)
        assert len(result["gapIndicators"]) == 0

    def test_honor_not_qualified(self):
        honor_data = {
            "honorList": [
                {
                    "honorName": "百萬圓桌",
                    "isQualified": False,
                    "gapAmt": 437947,
                    "deadlineDate": "2026-12-31",
                    "items": [
                        {"itemRole": "TARGET_FYC", "itemValue": 512800},
                        {"itemRole": "ACTUAL_FYC", "itemValue": 74853}
                    ]
                }
            ]
        }
        result = compute_gaps(honor_data=honor_data)
        assert len(result["gapIndicators"]) == 1
        assert result["gapIndicators"][0]["gapAmount"] == 437947

    def test_skill_gap_detection(self):
        skill_data = {
            "aiDrill": {"completionRate": 30, "usageNum": 0},
            "university": {
                "mandatoryCompleted": 2,
                "mandatoryTotal": 5
            }
        }
        result = compute_gaps(skill_data=skill_data)
        skill_gaps = result["diagnosis"]["skillGap"]
        assert "AI陪練未使用" in skill_gaps
        assert "AI陪練完成率低" in skill_gaps
        assert "必修課未完成" in skill_gaps

    def test_empty_gaps_congratulations(self):
        perf_data = {"personalPremium": 500000, "personalPolicyNum": 20}
        result = compute_gaps(performance_data=perf_data)
        assert result["gapIndicators"] == []


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
