"""
意图解析器测试
"""
import pytest
from src.services.intent_parser import IntentParser
from src.models.intent import IntentRequest


@pytest.fixture
def parser():
    return IntentParser()


def test_match_movie(parser):
    """测试观影场景识别"""
    result = parser.parse(IntentRequest(utterance="看电影"))
    assert result.intent_type == "scene"
    assert result.scene_id == "movie"
    assert result.confidence > 0


def test_match_bath(parser):
    """测试洗澡场景识别"""
    result = parser.parse(IntentRequest(utterance="我要洗澡"))
    assert result.intent_type == "scene"
    assert result.scene_id == "bath_prep"


def test_match_cyberpunk(parser):
    """测试赛博朋克场景识别"""
    result = parser.parse(IntentRequest(utterance="赛博朋克"))
    assert result.intent_type == "scene"
    assert result.scene_id == "cyberpunk"


def test_match_home(parser):
    """测试回家场景识别"""
    result = parser.parse(IntentRequest(utterance="我回来了"))
    assert result.intent_type == "scene"
    assert result.scene_id == "home"


def test_match_away(parser):
    """测试离家场景识别"""
    result = parser.parse(IntentRequest(utterance="我出门了"))
    assert result.intent_type == "scene"
    assert result.scene_id == "away"


def test_unknown_intent(parser):
    """测试未知意图"""
    result = parser.parse(IntentRequest(utterance="abcdefg"))
    assert result.intent_type == "unknown"


def test_turn_on_action(parser):
    """测试开灯动作"""
    result = parser.parse(IntentRequest(utterance="开灯"))
    assert result.intent_type == "action"


def test_turn_off_action(parser):
    """测试关灯动作"""
    result = parser.parse(IntentRequest(utterance="关灯"))
    assert result.intent_type == "action"


def test_confidence_calculation(parser):
    """测试置信度计算"""
    result = parser.parse(IntentRequest(utterance="看电影"))
    assert result.confidence > 0
    assert result.confidence <= 1.0
