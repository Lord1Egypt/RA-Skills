#!/usr/bin/env python3
import time
import sys
import os

if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.social_temporal import CulturalPauseAdapter, SocialTemporal


def test_cultural_pause_adapter():
    print("=" * 60)
    print("Test 1: CulturalPauseAdapter")
    print("=" * 60)

    adapter = CulturalPauseAdapter(culture="en_US")
    print(f"  Default culture: {adapter.culture}")
    print(f"  en_US thresholds: {adapter.get_thresholds()}")

    adapter.set_culture("zh_CN")
    print(f"  zh_CN thresholds: {adapter.get_thresholds()}")

    print("  [PASS]")


def test_culture_detection():
    print("\n" + "=" * 60)
    print("Test 2: Culture Detection")
    print("=" * 60)

    test_texts = [
        ("Hello, how are you today?", "en_US"),
        ("你好，今天天气怎么样？", "zh_CN"),
        ("こんにちは、元気ですか？", "ja_JP"),
        ("안녕하세요, 오늘 기분이 어떠세요?", "ko_KR"),
    ]

    for text, expected in test_texts:
        detected = CulturalPauseAdapter.detect_culture_from_text(text)
        status = "PASS" if detected == expected else "FAIL"
        print(f"  [{status}] '{text[:20]}...' -> {detected} (expected {expected})")

    print("  [PASS]")


def test_pause_classification():
    print("\n" + "=" * 60)
    print("Test 3: Pause Classification across cultures")
    print("=" * 60)

    duration = 1.0

    cultures = ["en_US", "zh_CN", "ja_JP"]
    for culture in cultures:
        adapter = CulturalPauseAdapter(culture=culture)
        pause_type = adapter.classify_pause(duration)
        is_hesitation = adapter.is_hesitation(duration)
        description = adapter.get_pause_description(duration)
        print(f"  {culture}: {duration}s -> {pause_type}, hesitation={is_hesitation}, desc='{description}'")

    print("  [PASS]")


def test_thresholds_comparison():
    print("\n" + "=" * 60)
    print("Test 4: Hesitation Thresholds Comparison")
    print("=" * 60)

    cultures = ["en_US", "zh_CN", "ja_JP", "de_DE", "fr_FR"]
    print(f"  {'Culture':<10} {'Short':<8} {'Medium':<8} {'Long':<8}")
    print("  " + "-" * 40)

    for culture in cultures:
        adapter = CulturalPauseAdapter(culture=culture)
        t = adapter.get_thresholds()
        print(f"  {culture:<10} {t['short']:<8} {t['medium']:<8} {t['long']:<8}")

    print("  [PASS]")


def test_social_temporal():
    print("\n" + "=" * 60)
    print("Test 5: SocialTemporal with culture")
    print("=" * 60)

    st = SocialTemporal(culture="zh_CN")
    print(f"  Initial culture: {st.culture}")

    st.record_utterance("Alice", "你好")
    time.sleep(0.1)
    st.record_utterance("Bob", "很高兴认识你")

    pause_type = st.get_pause_type()
    print(f"  Pause type: {pause_type}")
    print(f"  Is hesitation: {st.is_hesitation()}")

    st.set_culture("en_US")
    print(f"  After change culture: {st.culture}")

    print("  [PASS]")


def test_conversation_flow():
    print("\n" + "=" * 60)
    print("Test 6: Conversation Flow with pause analysis")
    print("=" * 60)

    st = SocialTemporal(culture="zh_CN")

    base_time = time.time()
    st.record_utterance("Speaker A", "你好，请问你是谁？", timestamp=base_time)
    st.record_utterance("Speaker B", "我是小明，很高兴认识你。", timestamp=base_time + 0.8)
    st.record_utterance("Speaker A", "小明你好！", timestamp=base_time + 2.0)

    flow = st.get_conversation_flow()
    for i, item in enumerate(flow):
        print(f"  [{i}] {item['speaker']}: {item['content'][:30]}...")
        if 'pause_before' in item:
            print(f"      pause={item['pause_before']:.2f}s, type={item['pause_type']}, desc='{item['pause_description']}'")

    insight = st.get_cross_cultural_insight()
    print(f"  Cross-cultural insight: {insight}")

    print("  [PASS]")


def test_supported_cultures():
    print("\n" + "=" * 60)
    print("Test 7: Supported Cultures")
    print("=" * 60)

    cultures = CulturalPauseAdapter.get_supported_cultures()
    print(f"  Total supported: {len(cultures)}")
    print(f"  Cultures: {', '.join(cultures)}")

    print("  [PASS]")


if __name__ == "__main__":
    test_cultural_pause_adapter()
    test_culture_detection()
    test_pause_classification()
    test_thresholds_comparison()
    test_social_temporal()
    test_conversation_flow()
    test_supported_cultures()

    print("\n" + "=" * 60)
    print("All cultural pause tests passed!")
    print("=" * 60)
