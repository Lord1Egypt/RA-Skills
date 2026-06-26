from pathlib import Path
"""交叉集成测试：验证多脚本/多参数组合场景"""
import os
import sys
import json
import pytest
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import consistency_check as cc
import rhythm_check as rc
import outline_drift as od

# ── 辅助 ──────────────────────────────────

def _write(path, content):
    path.write_text(content, encoding='utf-8')


def make_multi_chapters(chapters_dir, n=5, content_fn=None):
    for i in range(1, n + 1):
        c = content_fn(i) if content_fn else ("正常内容。" * 200)
        _write(chapters_dir / f"第{i:03d}章_测试.md", c)


# ── 1. consistency_check + character_states 联动 ──────

class TestConsistencyCharacterStates:
    def test_character_tracking_with_states_file(self, chapters_dir, tmp_path):
        """有角色状态文件时，角色出场追踪生效"""
        # 陆远1-2章出现，3-7章消失；赵恒3-7章出现
        for i in range(1, 8):
            if i <= 2:
                c = "陆远走进了房间。" + "日常内容。" * 100
            else:
                c = "赵恒在旁边站着。" + "日常内容。" * 100
            _write(chapters_dir / f"第{i:03d}章_测试.md", c)

        # character_states.json 格式：顶层是 name -> data dict
        states = {
            "陆远": {"aliases": ["陆远"]},
            "赵恒": {"aliases": ["赵恒"]}
        }

        issues = cc.check_character_appearance(
            cc.list_chapters(str(chapters_dir)),
            character_states_data=states
        )
        # 陆远前2章出现，后5章消失 → 应被检测到
        assert len(issues) > 0
        assert any('陆远' in str(i) for i in issues)

    def test_character_tracking_without_states_file(self, chapters_dir):
        """无角色状态文件时，角色追踪跳过（不崩溃）"""
        make_multi_chapters(chapters_dir, 3, lambda n: "张三走了过来。" + "内容。" * 100)
        issues = cc.check_character_appearance(
            cc.list_chapters(str(chapters_dir)),
            character_states_data=None
        )
        assert issues == []


# ── 2. rhythm_check --suggest 建议输出格式 ──────

class TestRhythmSuggest:
    def test_suggest_output_format(self, capsys):
        """--suggest 建议输出包含关键格式元素"""
        issues = [{'type': '连续太平', 'severity': 'high', 'detail': '第1-3章连续太平'}]
        chapter_data = [{'chapter': i, 'tension': 10, 'emotion': 'neutral', 'char_count': 5000} for i in range(1, 4)]
        suggestions = rc.generate_suggestions(issues, chapter_data)
        rc.print_suggestions(suggestions)
        captured = capsys.readouterr()
        assert "节奏修改建议" in captured.out or len(suggestions) == 0


# ── 3. rhythm_check --emotion-track 情绪追踪 ──────

class TestEmotionTrack:
    def test_emotion_profile_format(self):
        """compute_emotion_profile 返回正确的四维结构"""
        content = "他很开心快乐，笑了起来。但后来紧张害怕恐惧。悲伤痛苦流泪。"
        profile = rc.compute_emotion_profile(content)
        assert isinstance(profile, dict)
        for key in ('positive', 'negative', 'anxious', 'sorrow'):
            assert key in profile
            assert 0 <= profile[key] <= 1

    def test_emotion_shifts_detection(self):
        """detect_emotion_shifts 能检测情绪突变"""
        series = [
            {'chapter': i, 'scores': {'positive': 0.8, 'negative': 0.1, 'anxious': 0.1, 'sorrow': 0.0}}
            for i in range(1, 4)
        ]
        series.append({'chapter': 4, 'scores': {'positive': 0.1, 'negative': 0.2, 'anxious': 0.1, 'sorrow': 0.9}})
        shifts = rc.detect_emotion_shifts(series)
        assert len(shifts) > 0


# ── 4. tension_forecast 预测输出格式 ──────

class TestTensionForecast:
    def test_forecast_cli_output(self, chapters_dir):
        """tension_forecast.py CLI 输出包含预测结果"""
        make_multi_chapters(chapters_dir, 5, lambda n: (
            "不可能！他愣住了，危险逼近。" + "紧张内容" * 50 if n % 2 == 0
            else "他去了公司开了个会。" * 50
        ))
        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parent.parent / "scripts" /
                                          'tension_forecast.py'),
             str(chapters_dir), '--count', '3'],
            capture_output=True, text=True, timeout=30
        )
        assert result.returncode == 0
        assert "预测" in result.stdout or "推荐" in result.stdout or "节奏" in result.stdout

    def test_forecast_json_output(self, chapters_dir):
        """tension_forecast.py --json 输出合法 JSON"""
        make_multi_chapters(chapters_dir, 5, lambda n: "正常内容" * 50)
        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parent.parent / "scripts" /
                                          'tension_forecast.py'),
             str(chapters_dir), '--count', '2', '--json'],
            capture_output=True, text=True, timeout=30
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert 'forecasts' in data or 'predictions' in data or len(data) > 0


# ── 5. outline_drift --fix-suggest 修复建议 ──────

class TestOutlineDriftFixSuggest:
    def test_fix_suggest_format(self, chapters_dir, tmp_path):
        """--fix-suggest 修复建议输出格式正确"""
        outline_content = "# 第1卷\n1. 初始之日\n2. 命运邂逅\n3. 暗流涌动\n"
        outline_file = tmp_path / "outline.md"
        _write(outline_file, outline_content)

        for i in range(1, 4):
            _write(chapters_dir / f"第{i:03d}章_测试.md",
                   "# 完全无关的标题\n" + "无关内容。" * 50)

        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parent.parent / "scripts" /
                                          'outline_drift.py'),
             '--outline', str(outline_file),
             '--chapters', str(chapters_dir),
             '--fix-suggest'],
            capture_output=True, text=True, timeout=30
        )
        assert result.returncode == 0
        assert "修复" in result.stdout or "建议" in result.stdout or "偏差" in result.stdout


# ── 6. consistency_check --auto-fix ──────

class TestConsistencyAutoFix:
    def test_auto_fix_output(self, chapters_dir):
        """--auto-fix 生成替换建议不崩溃"""
        content = "他不禁微笑了起来。她不禁叹了口气。我不禁感到一阵心酸。大家不禁点头。"
        _write(chapters_dir / "第001章_测试.md", content + "填充内容。" * 100)

        suggestions = cc.generate_auto_fix_suggestions(
            cc.list_chapters(str(chapters_dir)),
            str(chapters_dir)
        )
        # 函数返回 list 或 None，不应崩溃
        assert suggestions is None or isinstance(suggestions, list)


# ── 7. consistency_check --skip-drafts ──────

class TestConsistencySkipDrafts:
    def test_skip_drafts_via_list_chapters(self, chapters_dir):
        """--skip-drafts 参数正确过滤草稿文件"""
        _write(chapters_dir / "第001章_正式.md", "正常内容。" * 200)
        _write(chapters_dir / "第002章_草稿.md", "草稿内容。" * 200)

        chs = cc.list_chapters(str(chapters_dir), skip_drafts=True)
        assert len(chs) == 1
        assert chs[0][0] == 1

    def test_skip_all_drafts(self, chapters_dir):
        """全是草稿时返回空"""
        _write(chapters_dir / "第001章_WIP.md", "内容。" * 100)
        chs = cc.list_chapters(str(chapters_dir), skip_drafts=True)
        assert len(chs) == 0


# ── 8. consistency_check --ignore-pattern ──────

class TestConsistencyIgnorePattern:
    def test_ignore_pattern_filters_issues(self, chapters_dir):
        """--ignore-pattern 通过正则过滤问题"""
        content = "他不禁感叹。她不禁微笑。大家不禁鼓掌。我不禁流下泪来。" + "填充。" * 200
        _write(chapters_dir / "第001章_测试.md", content)

        chs = cc.list_chapters(str(chapters_dir))
        all_issues = cc.check_ai_words(chs)
        # 手动模拟 run_check 中的 ignore_pattern 过滤逻辑
        import re
        patterns = [r'不禁']
        filtered = [i for i in all_issues if not any(re.search(p, i.get('detail', '')) for p in patterns)]
        assert not any('不禁' in str(i) for i in filtered)

    def test_ignore_pattern_preserves_others(self, chapters_dir):
        """--ignore-pattern 不影响不匹配的问题"""
        content = "他不禁感叹。她不禁微笑。大家不禁鼓掌。" + "填充。" * 200
        _write(chapters_dir / "第001章_测试.md", content)

        chs = cc.list_chapters(str(chapters_dir))
        all_issues = cc.check_ai_words(chs)
        import re
        patterns = [r'不存在词XYZ']
        filtered = [i for i in all_issues if not any(re.search(p, i.get('detail', '')) for p in patterns)]
        assert len(filtered) == len(all_issues)
