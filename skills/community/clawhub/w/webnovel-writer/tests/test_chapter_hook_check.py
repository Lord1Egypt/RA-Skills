from pathlib import Path
"""章末钩子检测脚本测试"""
import json
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chapter_hook_check import (
    extract_ending,
    detect_hook_type,
    check_single_chapter,
    check_consecutive_weak,
    generate_hook_suggestion,
    run_check,
    list_chapters,
)


# ============================================================
# 辅助函数
# ============================================================

def make_chapter(dir_path, num, content, title="测试"):
    fname = f"第{num:03d}章_{title}.md"
    fpath = os.path.join(dir_path, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    return fpath


# ============================================================
# 1. extract_ending 测试
# ============================================================

class TestExtractEnding:
    def test_short_content(self):
        """短文本直接返回全部"""
        text = "短内容"
        result = extract_ending(text, 200)
        assert result == "短内容"

    def test_long_content(self):
        """长文本截取最后200字"""
        text = "头" * 300 + "尾"
        result = extract_ending(text, 200)
        assert result.endswith("尾")
        assert len(result) <= 201

    def test_skip_title(self):
        """跳过标题行"""
        text = "# 第一章 标题\n正文内容"
        result = extract_ending(text, 200)
        assert "# " not in result
        assert "正文内容" in result


# ============================================================
# 2. detect_hook_type 测试
# ============================================================

class TestDetectHookType:
    def test_suspense_hook(self):
        """悬念钩子：问句结尾"""
        text = "他走到门口，突然停下了脚步。这里面到底有什么？"
        hook_type, score, _ = detect_hook_type(text)
        assert hook_type == "悬念钩子"
        assert score >= 5

    def test_emotion_hook(self):
        """情感钩子：泪水和沉默"""
        text = "她看着那张照片，泪水止不住地流。沉默良久，她把照片放下。"
        hook_type, score, _ = detect_hook_type(text)
        assert hook_type == "情感钩子"
        assert score >= 5

    def test_twist_hook(self):
        """反转钩子：出乎意料"""
        text = "一切看起来都很正常。但是，竟然是他自己安排的这一切。"
        hook_type, score, _ = detect_hook_type(text)
        assert hook_type == "反转钩子"
        assert score >= 6

    def test_crisis_hook(self):
        """危机钩子：危险逼近"""
        text = "倒计时还剩三分钟，而他还不知道炸弹在哪里。完了。"
        hook_type, score, _ = detect_hook_type(text)
        assert hook_type == "危机钩子"
        assert score >= 6

    def test_secret_hook(self):
        """秘密钩子：隐藏信息"""
        text = "文件最后一页被人撕掉了。这背后一定有不为人知的秘密。"
        hook_type, score, _ = detect_hook_type(text)
        assert hook_type == "秘密钩子"
        assert score >= 5

    def test_decision_hook(self):
        """决定钩子：做出选择"""
        text = "他站在路口。要么回去假装什么都没发生，要么走进去面对真相。他下定决心。"
        hook_type, score, _ = detect_hook_type(text)
        assert hook_type == "决定钩子"
        assert score >= 5

    def test_no_hook(self):
        """无钩子：平淡结尾"""
        text = "吃完饭，他们各自回房间休息了。窗外月光很好。"
        hook_type, score, _ = detect_hook_type(text)
        assert hook_type == "无钩子"
        assert score < 5

    def test_empty_text(self):
        """空文本"""
        hook_type, score, _ = detect_hook_type("")
        assert hook_type == "无钩子"
        assert score < 2

    def test_score_capped_at_10(self):
        """评分上限为10"""
        text = "危险逼近！死！杀！炸弹！塌了！到底是谁？竟然不可能！必须下定决心！秘密真相！"
        _, score, _ = detect_hook_type(text)
        assert score <= 10.0


# ============================================================
# 3. check_single_chapter 测试
# ============================================================

class TestCheckSingleChapter:
    def test_returns_required_fields(self):
        """返回结果包含必要字段"""
        result = check_single_chapter(1, "他看向窗外。到底发生了什么？")
        assert "chapter" in result
        assert "hook_type" in result
        assert "score" in result
        assert "severity" in result
        assert "ending_preview" in result
        assert "matched_keywords" in result

    def test_chapter_number_preserved(self):
        """章节号正确传递"""
        result = check_single_chapter(42, "平淡的一天过去了。")
        assert result["chapter"] == 42

    def test_severity_mapping(self):
        """严重程度映射正确"""
        weak = check_single_chapter(1, "平淡结尾。")
        assert weak["severity"] == "high"
        strong = check_single_chapter(2, "突然，门被踹开了！危险逼近！")
        assert strong["severity"] == "low"


# ============================================================
# 4. check_consecutive_weak 测试
# ============================================================

class TestCheckConsecutiveWeak:
    def test_no_weak_streak(self):
        """无连续弱结尾时不报警"""
        results = [
            {"chapter": i, "score": 6.0, "hook_type": "悬念钩子"}
            for i in range(1, 11)
        ]
        warnings = check_consecutive_weak(results, 4.0)
        assert len(warnings) == 0

    def test_three_weak_streak(self):
        """连续3章弱结尾触发警告"""
        results = [
            {"chapter": 1, "score": 6.0, "hook_type": "悬念钩子"},
            {"chapter": 2, "score": 2.0, "hook_type": "无钩子"},
            {"chapter": 3, "score": 3.0, "hook_type": "无钩子"},
            {"chapter": 4, "score": 2.5, "hook_type": "无钩子"},
            {"chapter": 5, "score": 7.0, "hook_type": "反转钩子"},
        ]
        warnings = check_consecutive_weak(results, 4.0)
        assert len(warnings) == 1
        assert "第2-4章" in warnings[0]["detail"]
        assert warnings[0]["severity"] == "medium"

    def test_five_weak_streak_high_severity(self):
        """连续5章以上弱结尾为高严重度"""
        results = [
            {"chapter": i, "score": 2.0, "hook_type": "无钩子"}
            for i in range(1, 6)
        ]
        warnings = check_consecutive_weak(results, 4.0)
        assert len(warnings) == 1
        assert warnings[0]["severity"] == "high"

    def test_two_weak_no_warning(self):
        """仅2章弱结尾不触发警告"""
        results = [
            {"chapter": 1, "score": 7.0, "hook_type": "悬念钩子"},
            {"chapter": 2, "score": 3.0, "hook_type": "无钩子"},
            {"chapter": 3, "score": 2.0, "hook_type": "无钩子"},
            {"chapter": 4, "score": 8.0, "hook_type": "危机钩子"},
        ]
        warnings = check_consecutive_weak(results, 4.0)
        assert len(warnings) == 0


# ============================================================
# 5. generate_hook_suggestion 测试
# ============================================================

class TestGenerateHookSuggestion:
    def test_strong_score_no_suggestion(self):
        """强钩子不生成建议"""
        result = generate_hook_suggestion("ending", "悬念钩子", 8.0)
        assert result is None

    def test_no_hook_suggestion(self):
        """无钩子生成建议"""
        result = generate_hook_suggestion("平淡结尾", "无钩子", 2.0)
        assert result is not None
        assert len(result) > 10

    def test_each_type_has_suggestion(self):
        """每种类型弱分数都有建议"""
        for hook_type in ["悬念钩子", "情感钩子", "反转钩子", "危机钩子", "秘密钩子", "决定钩子"]:
            result = generate_hook_suggestion("ending", hook_type, 3.0)
            assert result is not None, f"{hook_type} 应该有建议"


# ============================================================
# 6. run_check 集成测试
# ============================================================

class TestRunCheck:
    def test_empty_dir(self, tmp_path):
        """空目录返回错误"""
        d = tmp_path / "empty"
        d.mkdir()
        result = run_check(str(d))
        assert "error" in result

    def test_with_chapters(self, tmp_path):
        """有章节时正常返回结果"""
        d = tmp_path / "novel"
        d.mkdir()
        # 写3章
        make_chapter(str(d), 1, "他看向远方。到底发生了什么？")
        make_chapter(str(d), 2, "日子一天天过去了。窗外阳光明媚。")
        make_chapter(str(d), 3, "突然门被踹开——危险逼近！完了！")
        
        result = run_check(str(d))
        assert "chapters" in result
        assert len(result["chapters"]) == 3
        assert "average_score" in result
        assert result["total_chapters"] == 3

    def test_json_output(self, tmp_path, capsys):
        """JSON格式输出"""
        d = tmp_path / "novel"
        d.mkdir()
        make_chapter(str(d), 1, "悬念结尾。到底是谁？")
        
        import subprocess
        script = str(Path(__file__).resolve().parent.parent / "scripts" /
                              "chapter_hook_check.py")
        r = subprocess.run(
            [sys.executable, script, "--novel-dir", str(d), "--format", "json"],
            capture_output=True, text=True, timeout=30,
        )
        assert r.returncode == 0
        output = r.stdout
        # 找到最后一个完整的顶层JSON对象（以 {\n  "version" 开头）
        json_start = output.rfind('{\n  "version"')
        if json_start < 0:
            json_start = output.rfind('{')
        if json_start >= 0:
            data = json.loads(output[json_start:])
            assert "chapters" in data
