"""章节开头吸引力评分测试 v2.2.1"""

import os
import sys
import json
import tempfile
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opening_score import (
    VERSION, get_opening_text, detect_opening_type, check_short_first_sentence,
    check_no_specific_info, check_heavy_background, calculate_score,
    detect_hooks, generate_suggestions, analyze_chapter, run_score,
    list_chapter_files,
)


# ============================================================
# 辅助
# ============================================================

def make_chapter(tmpdir: str, fname: str, content: str) -> str:
    path = os.path.join(tmpdir, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


# ============================================================
# 测试用例
# ============================================================

class TestGetOpeningText:
    """开头文本提取"""

    def test_skip_title(self):
        text = "# 第一章 标题\n正文从这里开始" + "，继续" * 100
        result = get_opening_text(text, 50)
        assert "标题" not in result
        assert "正文" in result

    def test_char_limit(self):
        text = "a" * 500
        assert len(get_opening_text(text, 300)) == 300

    def test_empty(self):
        assert get_opening_text("") == ""


class TestDetectOpeningType:
    """开头类型识别"""

    def test_dialogue_type(self):
        text = '"你到底在搞什么？"李明怒吼道。'
        t, s = detect_opening_type(text)
        assert t == "对话"
        assert s == 80

    def test_suspense_type(self):
        text = "怎么可能？他明明已经死了。"
        t, s = detect_opening_type(text)
        assert t == "悬念"
        assert s == 85

    def test_action_type(self):
        text = "他猛地推开大门，冲了进去。"
        t, s = detect_opening_type(text)
        assert t == "动作"
        assert s == 75

    def test_environment_type(self):
        text = "窗外下着大雨，雷声轰隆作响。"
        t, s = detect_opening_type(text)
        assert t == "环境"
        assert s == 60

    def test_narration_default(self):
        text = "这件事要从三年前说起。"
        t, s = detect_opening_type(text)
        assert t == "叙述"
        assert s == 55


class TestCalculateScore:
    """评分测试"""

    def test_high_score_suspense_with_conflict(self):
        text = "不可能！他明明已经死了三天！张伟瞪大了眼睛看着眼前的男人。"
        score, otype, bonuses, penalties = calculate_score(text)
        assert score >= 80
        assert any("冲突" in b for b in bonuses)

    def test_low_score_plain_narration(self):
        text = "这是一个关于成长的故事。从前有一个小村庄，村子里住着很多人。大家都过着平静的生活。总而言之这里什么也没发生过。"
        score, otype, bonuses, penalties = calculate_score(text)
        assert score <= 60

    def test_score_clamp_100(self):
        """分数不超过100"""
        text = "不可能！李明大喊。2026年4月10日，他亲眼看到那具尸体。突然，门开了。"
        score, _, _, _ = calculate_score(text)
        assert score <= 100

    def test_score_clamp_0(self):
        """分数不低于0"""
        text = "从古至今。一直以来。据说。众所周知。事实上。实际上。总而言之。"
        score, _, _, _ = calculate_score(text)
        assert score >= 0


class TestDetectHooks:
    """钩子检测"""

    def test_crisis_hook(self):
        hooks = detect_hooks("突然，危险降临了，他感到一阵剧痛。")
        assert "危机" in hooks

    def test_reversal_hook(self):
        hooks = detect_hooks("没想到，他居然还活着。")
        assert "意外反转" in hooks

    def test_no_hooks(self):
        hooks = detect_hooks("今天天气不错，阳光明媚。")
        assert hooks == []


class TestCheckFunctions:
    """辅助检查函数"""

    def test_short_first_sentence_true(self):
        assert check_short_first_sentence("他死了。就这么简单。")

    def test_short_first_sentence_false(self):
        assert not check_short_first_sentence("这是一个关于一个年轻人从农村来到大城市闯荡最终功成名就的故事。")

    def test_no_specific_info_true(self):
        assert not check_no_specific_info("一切都是那么的平静，没有任何波澜起伏。")

    def test_no_specific_info_false(self):
        assert not check_no_specific_info("李明站在上海外滩，看着2026年的夜景。")

    def test_heavy_background_true(self):
        text = "据说这个村子有很长的历史。众所周知这里曾经发生过大事。实际上情况远比想象的复杂。总而言之这就是背景。"
        assert check_heavy_background(text)

    def test_heavy_background_false(self):
        assert not check_heavy_background("他跑进房间，看到了那封信。")


class TestSuggestions:
    """建议生成"""

    def test_low_score_suggests_rewrite(self):
        suggestions = generate_suggestions(40, "叙述", [], ["无具体信息 -10"], [])
        assert any("重写" in s for s in suggestions)

    def test_high_score_positive(self):
        suggestions = generate_suggestions(85, "悬念", ["含冲突 +10"], [], ["意外反转"])
        assert any("不错" in s for s in suggestions)


class TestRunScore:
    """完整流程测试"""

    def test_json_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            make_chapter(tmpdir, "第001章_测试.md",
                         "# 第001章 测试\n" + '"你来了。"他说。\n' + "不可能。" * 50)
            result = json.loads(run_score(tmpdir, fmt="json"))
            assert "results" in result
            assert result["version"] == VERSION

    def test_top_n(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            make_chapter(tmpdir, "第001章_差.md", "# 第1章\n" + "从前有座山。" * 50)
            make_chapter(tmpdir, "第002章_好.md", "# 第2章\n" + '"快跑！"他喊道。\n' + "不可能！" * 50)
            text = run_score(tmpdir, top_n=1, fmt="text")
            assert "第2章" in text

    def test_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            text = run_score(tmpdir, fmt="text")
            assert "未找到" in text


class TestVersion:
    def test_version(self):
        assert VERSION == "v2.2.1"
