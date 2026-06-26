"""
习惯分析器测试
"""
import pytest
from datetime import datetime
from src.services.habit_analyzer import HabitAnalyzer


@pytest.fixture
def analyzer():
    return HabitAnalyzer()


def test_analyze_empty_history(analyzer):
    """测试空历史"""
    result = analyzer.analyze("light.test", [])
    assert result.entity_id == "light.test"
    assert result.confidence == 0.0
    assert result.sample_count == 0


def test_analyze_single_sample(analyzer):
    """测试单样本"""
    history = [
        {"last_changed": "2026-03-17T20:00:00+00:00", "state": "on"},
    ]
    result = analyzer.analyze("light.test", history)
    assert result.sample_count == 1


def test_analyze_multiple_samples(analyzer):
    """测试多样本"""
    history = [
        {"last_changed": f"2026-03-17T20:00:00+00:00", "state": "on"}
        for _ in range(10)
    ]
    result = analyzer.analyze("light.test", history)
    assert result.sample_count == 10


def test_confidence_calculation_low(analyzer):
    """测试低置信度"""
    # 少于5个样本
    history = [
        {"last_changed": f"2026-03-17T20:00:00+00:00", "state": "on"}
        for _ in range(3)
    ]
    result = analyzer.analyze("light.test", history)
    assert result.confidence == 0.0


def test_confidence_calculation_medium(analyzer):
    """测试中等置信度"""
    # 10个样本
    history = [
        {"last_changed": f"2026-03-17T20:00:00+00:00", "state": "on"}
        for _ in range(10)
    ]
    result = analyzer.analyze("light.test", history)
    assert result.confidence >= 0.5


def test_typical_time_calculation(analyzer):
    """测试典型时间计算"""
    # 多个相同时间
    history = [
        {"last_changed": f"2026-03-17T20:00:00+00:00", "state": "on"},
        {"last_changed": f"2026-03-16T20:00:00+00:00", "state": "on"},
        {"last_changed": f"2026-03-15T20:00:00+00:00", "state": "on"},
    ]
    result = analyzer.analyze("light.test", history)
    assert result.typical_on_time == "20:00"


def test_should_suggest(analyzer):
    """测试是否应该生成建议"""
    # 高置信度
    history = [
        {"last_changed": f"2026-03-17T20:00:00+00:00", "state": "on"}
        for _ in range(20)
    ]
    result = analyzer.analyze("light.test", history)
    assert analyzer.should_suggest(result) == True


def test_should_not_suggest(analyzer):
    """测试不应该生成建议"""
    # 低置信度
    history = [
        {"last_changed": f"2026-03-17T20:00:00+00:00", "state": "on"}
        for _ in range(3)
    ]
    result = analyzer.analyze("light.test", history)
    assert analyzer.should_suggest(result) == False
