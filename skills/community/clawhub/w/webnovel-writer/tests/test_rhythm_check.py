"""rhythm_check.py 的自动化测试"""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import rhythm_check as rc

def make_chapters(chapters_dir, chapters_data):
    """辅助：创建多章，每章 (num, content) 元组"""
    for num, content in chapters_data:
        (chapters_dir / f"第{num:03d}章_测试.md").write_text(content, encoding='utf-8')

class TestDialogueRatio:
    def test_no_dialogue(self):
        assert rc.count_dialogue_ratio("他走在路上") == 0

    def test_half_dialogue(self):
        text = "他说了句话，\u201c你好啊\u201d然后就走了。"
        ratio = rc.count_dialogue_ratio(text)
        assert 0 < ratio < 1

class TestHookDensity:
    def test_no_hooks(self):
        density, types = rc.count_hook_density("今天天气很好，他去散步。")
        assert density == 0

    def test_with_hooks(self):
        density, types = rc.count_hook_density("他愣住了，不可能！这是怎么回事？")
        assert density > 0

class TestEmotionTone:
    def test_tense(self):
        tone, _ = rc.detect_emotion_tone("紧张恐惧，危险逼近，心跳加速")
        assert tone == 'tense'

    def test_neutral(self):
        tone, _ = rc.detect_emotion_tone("他去了公司，开了个会")
        assert tone == 'neutral'

class TestTensionScore:
    def test_range(self):
        score = rc.compute_tension(5, 0.3, 0.2, {'suspense': 1, 'reversal': 0, 'thrill': 0})
        assert 0 <= score <= 100

class TestRhythmIssues:
    def test_consecutive_flat(self, chapters_dir):
        """连续3章太平应报警"""
        flat = "他去了公司，开了个会，然后回家了。" * 50
        make_chapters(chapters_dir, [(1, flat), (2, flat), (3, flat), (4, flat)])
        chs = rc.list_chapters(str(chapters_dir))
        # 手动触发检测逻辑（模拟 run_check 的核心部分）
        chapter_data = []
        for num, path, fname in chs:
            content = rc.normalize_text(rc.read_file(path))
            if not content:
                continue
            density, hook_types = rc.count_hook_density(content)
            dr = rc.count_dialogue_ratio(content)
            sr = rc.count_short_sentence_ratio(content)
            tension = rc.compute_tension(density, dr, sr, hook_types)
            chapter_data.append({'chapter': num, 'tension': tension, 'char_count': 100})

        tensions = [c['tension'] for c in chapter_data]
        avg_t = sum(tensions) / len(tensions)
        low = max(avg_t * 0.5, 20)

        # 4章都太平
        low_count = sum(1 for t in tensions if t <= low)
        assert low_count >= 3  # 至少3章低紧张度

    def test_consecutive_tight(self, chapters_dir):
        """连续3章太紧应报警"""
        tight = "不可能！他愣住了，瞳孔骤然收缩，倒吸一口凉气。追！危险！杀！逃！" * 50
        make_chapters(chapters_dir, [(1, tight), (2, tight), (3, tight), (4, tight)])
        chs = rc.list_chapters(str(chapters_dir))
        chapter_data = []
        for num, path, fname in chs:
            content = rc.normalize_text(rc.read_file(path))
            density, hook_types = rc.count_hook_density(content)
            dr = rc.count_dialogue_ratio(content)
            sr = rc.count_short_sentence_ratio(content)
            tension = rc.compute_tension(density, dr, sr, hook_types)
            chapter_data.append({'chapter': num, 'tension': tension, 'char_count': 100})

        tensions = [c['tension'] for c in chapter_data]
        avg_t = sum(tensions) / len(tensions)
        high = min(avg_t * 1.5, 80)
        high_count = sum(1 for t in tensions if t >= high)
        assert high_count >= 3
