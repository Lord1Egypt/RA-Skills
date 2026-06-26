"""段落长度检测脚本测试"""
import json
import os
import sys
import pytest

# 将脚本目录加入路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from paragraph_check import (
    count_chinese_chars,
    split_paragraphs,
    has_dialogue,
    has_action,
    check_paragraph_lengths,
    check_consecutive_long_paragraphs,
    check_visual_rhythm,
    check_wall_text,
    generate_suggestions,
    compute_statistics,
    check_single_chapter,
    run_check,
)


# ============================================================
# 辅助函数
# ============================================================

def make_chapter(dir_path, num, content, title="测试"):
    """创建一个测试章节文件"""
    fname = f"第{num:03d}章_{title}.md"
    fpath = os.path.join(dir_path, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    return fpath


# ============================================================
# 基础函数测试
# ============================================================

class TestCountChineseChars:
    """测试中文字符统计"""

    def test_pure_chinese(self):
        assert count_chinese_chars("你好世界") == 4

    def test_mixed(self):
        assert count_chinese_chars("你好hello世界") == 4

    def test_empty(self):
        assert count_chinese_chars("") == 0

    def test_punctuation_only(self):
        assert count_chinese_chars("。，！？") == 0


class TestSplitParagraphs:
    """测试段落拆分"""

    def test_basic_split(self):
        content = "第一段内容。\n\n第二段内容。\n\n第三段内容。"
        paras = split_paragraphs(content)
        assert len(paras) == 3

    def test_skip_title(self):
        content = "# 第一章 标题\n\n第一段。\n\n第二段。"
        paras = split_paragraphs(content)
        assert len(paras) == 2

    def test_merge_inner_newlines(self):
        content = "这是一段\n有内部换行\n的内容。"
        paras = split_paragraphs(content)
        assert len(paras) == 1
        assert '\n' not in paras[0]

    def test_empty_content(self):
        paras = split_paragraphs("")
        assert len(paras) == 0


class TestHasDialogue:
    """测试对话检测"""

    def test_has_chinese_quotes(self):
        assert has_dialogue("\u201c你好\u201d") is True

    def test_has_ascii_quotes(self):
        assert has_dialogue('"你好"') is True

    def test_no_dialogue(self):
        assert has_dialogue("他走出了房间。") is False


class TestHasAction:
    """测试动作检测"""

    def test_has_action(self):
        assert has_action("他走到窗前。") is True

    def test_no_action(self):
        assert has_action("天空是蓝色的。") is False


# ============================================================
# 检查函数测试
# ============================================================

class TestCheckParagraphLengths:
    """测试过长段落检测"""

    def test_long_paragraph_detected(self):
        # 生成一个超长段落
        long_text = "他" * 200 + "。"
        issues = check_paragraph_lengths([long_text])
        assert len(issues) == 1
        assert issues[0]['type'] == '过长段落'

    def test_normal_paragraph_no_issue(self):
        normal = "这是一段正常长度的段落，大概五十个字左右，不应该被标记为过长段落。"
        issues = check_paragraph_lengths([normal])
        assert len(issues) == 0

    def test_custom_threshold(self):
        long_text = "他" * 80 + "。"
        # 默认150不触发
        assert len(check_paragraph_lengths([long_text])) == 0
        # 自定义阈值50触发
        assert len(check_paragraph_lengths([long_text], max_paragraph=50)) == 1


class TestCheckConsecutiveLongParagraphs:
    """测试连续长段落检测"""

    def test_consecutive_long_detected(self):
        long_paras = ["他" * 120 + "。" for _ in range(4)]
        issues = check_consecutive_long_paragraphs(long_paras)
        assert len(issues) == 1
        assert issues[0]['type'] == '节奏过重'

    def test_short_sequence_no_issue(self):
        long_paras = ["他" * 120 + "。" for _ in range(2)]
        issues = check_consecutive_long_paragraphs(long_paras)
        assert len(issues) == 0

    def test_interrupted_sequence(self):
        # 2长1短2长，不触发
        paras = ["他" * 120 + "。"] * 2 + ["短段。"] + ["他" * 120 + "。"] * 2
        issues = check_consecutive_long_paragraphs(paras)
        assert len(issues) == 0


class TestCheckVisualRhythm:
    """测试视觉节奏检测"""

    def test_too_few_paragraphs(self):
        # 少量长段
        paras = ["他" * 200 + "。" for _ in range(5)]
        issues = check_visual_rhythm(paras)
        types = [i['type'] for i in issues]
        assert any('段落数量偏少' in t for t in types) or any('平均段落过长' in t for t in types)

    def test_balanced_paragraphs(self):
        # 理想段落分布
        paras = [
            "这是一段合适长度的段落，字数在三十到八十之间，节奏合适。",
            "短句。",
            "\u201c你好。\u201d他笑了笑。",
            "她点了点头，转身离开了房间。",
            "又是一段正常长度的文字描写，描述场景和氛围。",
        ]
        issues = check_visual_rhythm(paras)
        # 不应有严重问题
        assert all(i['severity'] == 'low' for i in issues)


class TestCheckWallText:
    """测试墙文字检测"""

    def test_no_dialogue_streak(self):
        # 连续5段纯描写无对话无动作
        pure_desc = ["天空中飘着白云，阳光洒在大地上，一切看起来很平静。" for _ in range(6)]
        issues = check_wall_text(pure_desc)
        assert any(i['type'] == '墙文字·缺少互动' for i in issues)

    def test_consecutive_very_long(self):
        # 连续3段超长
        very_long = ["这是一段非常非常长的段落，" + "文字" * 200 + "，描写了很多内容。"]
        very_long = very_long * 4
        issues = check_wall_text(very_long)
        assert any(i['type'] == '墙文字·超长段堆砌' for i in issues)

    def test_mixed_content_no_issue(self):
        paras = [
            "\u201c你好啊。\u201d",
            "他笑了笑，走过去。",
            "风景不错。",
            "\u201c嗯。\u201d她点了点头。",
        ]
        issues = check_wall_text(paras)
        assert len(issues) == 0


class TestComputeStatistics:
    """测试统计数据"""

    def test_basic_stats(self):
        paras = [
            "这是一段合适长度的段落。",
            "\u201c短。\u201d",
            "他" * 200 + "。",
        ]
        stats = compute_statistics(paras)
        assert stats['paragraph_count'] == 3
        assert stats['dialogue_count'] == 1
        assert stats['long_count'] == 1

    def test_empty_stats(self):
        stats = compute_statistics([])
        assert stats['paragraph_count'] == 0
        assert stats['avg_length'] == 0


class TestGenerateSuggestions:
    """测试建议生成"""

    def test_split_suggestion(self):
        long_text = "第一句内容。" + "第二句内容。" * 80 + "最后一句。"
        suggestions = generate_suggestions(
            [long_text],
            [{'type': '过长段落', 'paragraph_index': 0}],
        )
        assert any(s['type'] == '拆分建议' for s in suggestions)


class TestRunCheck:
    """测试完整检测流程"""

    def test_run_check_with_real_files(self, tmp_path):
        # 创建临时章节
        ch_dir = tmp_path / "chapters"
        ch_dir.mkdir()

        content = "# 第1章 测试\n\n"
        # 加入一些正常段落和一段超长段落
        for i in range(10):
            content += f"这是第{i+1}段正常长度的段落内容，描述一些场景。\n\n"
        # 超长段落
        content += "这是一段非常非常长的段落，" + "文字不断地持续着" * 30 + "。\n\n"
        # 加入对话
        content += "\u201c你好。\u201d他说道。\n\n"

        make_chapter(str(ch_dir), 1, content)

        result = run_check(str(ch_dir), output_format='text')
        assert 'chapters' in result
        assert len(result['chapters']) == 1
        assert result['chapters'][0]['chapter'] == 1

    def test_run_check_json_output(self, tmp_path, capsys):
        ch_dir = tmp_path / "chapters"
        ch_dir.mkdir()
        make_chapter(str(ch_dir), 1, "正常段落内容。\n\n\u201c对话。\u201d\n\n")

        result = run_check(str(ch_dir), output_format='json')
        assert 'version' in result
        # JSON输出到stdout
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed['version'] == 'v2.2.1'

    def test_empty_directory(self, tmp_path, capsys):
        ch_dir = tmp_path / "empty"
        ch_dir.mkdir()
        result = run_check(str(ch_dir))
        assert 'error' in result

    def test_suggest_flag(self, tmp_path):
        ch_dir = tmp_path / "chapters"
        ch_dir.mkdir()
        # 创建一个有问题的章节
        long_para = "很长的段落，" + "内容" * 200 + "。"
        content = f"# 第1章\n\n{long_para}\n\n"
        for i in range(6):
            content += f"纯描写段落{i+1}，天空很蓝，阳光很好，一切都很安静和平静。\n\n"

        make_chapter(str(ch_dir), 1, content)
        result = run_check(str(ch_dir), suggest=True)
        ch_data = result['chapters'][0]
        # 有问题时应生成建议
        if ch_data['issues']:
            assert 'suggestions' in ch_data
