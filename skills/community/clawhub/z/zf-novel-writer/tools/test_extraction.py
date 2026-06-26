#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for comprehensive_check.py extraction functions
"""
import json
import sys
import io
from pathlib import Path

# Set UTF-8 output for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from comprehensive_check import extract_emotional_changes, extract_character_interactions


def test_extract_emotional_changes_basic():
    """Test basic emotional change extraction for Chen An"""
    text = """
    陈安感到心中一阵紧张，手心微微出汗。面对眼前的情况，他深吸一口气，
    重新找回了自信。看到对方的表情，他内心涌起一股愤怒，但很快冷静下来。
    他眼神中透露出坚定的决心。
    """

    result = extract_emotional_changes(text, chapter_num=10)

    # Should return list of emotional changes
    assert isinstance(result, list), "Should return a list"

    # Should find Chen An's emotions
    chen_an_emotions = [e for e in result if e.get('character') == '陈安']
    assert len(chen_an_emotions) > 0, "Should find Chen An's emotions"

    # Check structure
    for emotion in chen_an_emotions:
        assert 'character' in emotion, "Should have character field"
        assert 'emotion' in emotion, "Should have emotion field"
        assert 'trigger' in emotion, "Should have trigger field"
        assert 'intensity' in emotion, "Should have intensity field"
        assert isinstance(emotion['intensity'], int), "Intensity should be integer"
        assert 1 <= emotion['intensity'] <= 10, "Intensity should be 1-10"

    print("[PASS] test_extract_emotional_changes_basic")


def test_extract_emotional_changes_with_female_characters():
    """Test emotional extraction for female characters"""
    text = """
    林晚晴看着陈安，心中充满好奇。她对陈安的信任逐渐增加，
    脸上露出了喜欢的神情。但随即又有些怀疑，眼神中闪过一丝不安。
    """

    result = extract_emotional_changes(text, chapter_num=15)

    # Should find female character emotions
    female_emotions = [e for e in result if e.get('character') in ['林晚晴', '苏清歌', '叶唯']]
    assert len(female_emotions) > 0, "Should find female character emotions"

    print("[PASS] test_extract_emotional_changes_with_female_characters")


def test_extract_emotional_changes_empty_text():
    """Test with empty text"""
    result = extract_emotional_changes("", chapter_num=1)
    assert isinstance(result, list), "Should return empty list for empty text"
    assert len(result) == 0, "Should return empty list for empty text"

    print("[PASS] test_extract_emotional_changes_empty_text")


def test_extract_character_interactions_basic():
    """Test basic character interaction extraction"""
    text = """
    陈安走进教室，第一次见到了林晚晴。两人相视一笑，开始交谈。
    "你好，我叫陈安。"他主动打招呼。
    """

    result = extract_character_interactions(text, chapter_num=5)

    # Should return list of interactions
    assert isinstance(result, list), "Should return a list"

    # Should find interaction
    assert len(result) > 0, "Should find at least one interaction"

    # Check structure
    for interaction in result:
        assert 'from' in interaction, "Should have 'from' field"
        assert 'to' in interaction, "Should have 'to' field"
        assert 'event' in interaction, "Should have 'event' field"
        assert 'type' in interaction, "Should have 'type' field"

    print("[PASS] test_extract_character_interactions_basic")


def test_extract_character_interactions_dialogue():
    """Test interaction detection through dialogue"""
    text = """苏清歌询问陈安是否确定。陈安回答必须这么做。两人在房间里进行了深入的对话。"""

    result = extract_character_interactions(text, chapter_num=20)

    # Should find interaction between characters
    assert len(result) > 0, f"Should detect interactions, got {len(result)}: {result}"

    print("[PASS] test_extract_character_interactions_dialogue")


def test_extract_character_interactions_empty_text():
    """Test with empty text"""
    result = extract_character_interactions("", chapter_num=1)
    assert isinstance(result, list), "Should return empty list for empty text"
    assert len(result) == 0, "Should return empty list for empty text"

    print("[PASS] test_extract_character_interactions_empty_text")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running extraction function tests...")
    print("=" * 60)

    try:
        test_extract_emotional_changes_basic()
        test_extract_emotional_changes_with_female_characters()
        test_extract_emotional_changes_empty_text()
        test_extract_character_interactions_basic()
        test_extract_character_interactions_dialogue()
        test_extract_character_interactions_empty_text()

        print("\n" + "=" * 60)
        print("[SUCCESS] ALL TESTS PASSED")
        print("=" * 60)
        return True

    except AssertionError as e:
        print("\n" + "=" * 60)
        print(f"[FAIL] TEST FAILED: {e}")
        print("=" * 60)
        return False
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"[ERROR] {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
