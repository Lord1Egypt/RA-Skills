"""对话标签质量检测 - 测试用例"""
import pytest
from dialogue_tag_check import (
    count_chinese_chars, detect_tags, detect_adverb_tags, detect_full_tags,
    count_dialogue_chars, check_frequency, check_monotony, check_quality,
    check_dialogue_ratio, check_chapter, run, format_text_output,
)


class TestCountChineseChars:
    """中文字符计数"""

    def test_pure_chinese(self):
        assert count_chinese_chars("你好世界") == 4

    def test_mixed(self):
        assert count_chinese_chars("hello你好world世界") == 4


class TestDetectTags:
    """对话标签检测"""

    def test_basic_tag(self):
        tags = detect_tags("他说：")
        assert "他说" in tags

    def test_multiple_tags(self):
        text = "他说要去。她问道。老人笑了。"
        tags = detect_tags(text)
        assert len(tags) >= 2

    def test_no_tags(self):
        tags = detect_tags("今天天气不错，万里无云。")
        assert len(tags) == 0

    def test_complex_tag(self):
        tags = detect_tags("李明笑了笑说")
        assert any("笑" in t and "说" in t for t in tags)


class TestDetectAdverbTags:
    """副词修饰标签检测"""

    def test_adverb_tag(self):
        result = detect_adverb_tags("他愤怒地说了一句话。")
        assert len(result) >= 1

    def test_no_adverb(self):
        result = detect_adverb_tags("他说了一句话。")
        assert len(result) == 0


class TestDetectFullTags:
    """完整标签检测（主语+动词）"""

    def test_basic(self):
        tags = detect_full_tags("他说。她问道。")
        assert len(tags) >= 2

    def test_subject_extraction(self):
        tags = detect_full_tags("李明说了一句话。")
        subjects = [s for s, v in tags]
        assert "李明" in subjects


class TestDialogueRatio:
    """对话占比检测"""

    def test_high_ratio_warning(self):
        # 对话占比 >70% 应警告
        text = "「你说什么」「我说真的」「你确定」「确定」「好吧」他说。"
        result = check_dialogue_ratio(text, count_chinese_chars(text))
        assert any("过高" in w for w in result["warnings"])

    def test_low_ratio_warning(self):
        # 对话占比 <10% 且字数>500 应警告
        dialogue = "「好」"
        narrative = "这是一段很长的叙事。" * 100
        text = narrative + dialogue
        result = check_dialogue_ratio(text, count_chinese_chars(text))
        assert any("过低" in w for w in result["warnings"])

    def test_normal_ratio(self):
        text = "他说「你好」。然后转身离开了。她看着他的背影，心里有些不舍。"
        result = check_dialogue_ratio(text, count_chinese_chars(text))
        assert len(result["warnings"]) == 0


class TestCheckFrequency:
    """标签频率检测"""

    def test_high_frequency_warning(self):
        # 构造高频率文本
        tags = ["他说"] * 20
        result = check_frequency(tags, 1000, 15.0)
        assert any("超过" in w for w in result["warnings"])

    def test_low_frequency_warning(self):
        tags = ["他说"]
        result = check_frequency(tags, 1000, 15.0)
        assert any("过低" in w for w in result["warnings"])

    def test_zero_chars(self):
        result = check_frequency([], 0, 15.0)
        assert result["tags_per_k"] == 0


class TestCheckMonotony:
    """标签单调性检测"""

    def test_consecutive_repeat(self):
        tags = ["他说", "他说", "他说", "她说"]
        result = check_monotony(tags, [("他", "说"), ("他", "说"), ("他", "说"), ("她", "说")])
        assert any("连续" in w for w in result["warnings"])

    def test_few_verb_types(self):
        tags = ["他说", "他说", "她说", "他说", "她道"]
        result = check_monotony(tags, [("他", "说"), ("他", "说"), ("她", "说"), ("他", "说"), ("她", "道")])
        assert any("种类过少" in w for w in result["warnings"])


class TestCheckChapter:
    """整章检测集成"""

    def test_basic_chapter(self):
        text = "张三走进房间。他说「你好」。李四看了他一眼，问道「你来干什么？」"
        result = check_chapter(text, suggest=True)
        assert result["char_count"] > 0
        assert "all_warnings" in result


class TestRun:
    """目录级检测"""

    def test_empty_dir(self, tmp_path):
        result = run(str(tmp_path))
        assert result.get("error") or result["total_chapters"] == 0

    def test_with_chapter(self, tmp_path):
        chapter = tmp_path / "第001章测试.md"
        chapter.write_text("他说「你好」。她笑了笑。", encoding="utf-8")
        result = run(str(tmp_path))
        assert result["total_chapters"] == 1


class TestFormatOutput:
    """输出格式化"""

    def test_text_output(self):
        summary = {
            "total_chapters": 1, "total_warnings": 0,
            "threshold": 15, "version": "v2.2.1",
            "chapters": [{"chapter": 1, "filename": "第001章.md", "char_count": 100,
                          "tag_count": 2, "frequency": {"tags_per_k": 20},
                          "dialogue_ratio": {"ratio": 0.3}, "all_warnings": [],
                          "quality": {"suggestions": []}}]
        }
        output = format_text_output(summary)
        assert "第1章" in output
