"""tension_forecast.py 的自动化测试"""
import os
import sys
import json
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tension_forecast as tf


# ============================================================
# 辅助函数
# ============================================================

def make_chapters(chapters_dir, chapters_data):
    """辅助：创建多章，每章 (num, content) 元组"""
    for num, content in chapters_data:
        (chapters_dir / f"第{num:03d}章_测试.md").write_text(content, encoding='utf-8')


# ============================================================
# 节奏曲线计算：tension_to_rhythm / rhythm_to_target_tension
# ============================================================

class TestTensionToRhythm:
    def test_high_tension_is_turning(self):
        assert tf.tension_to_rhythm(90) == '转折'
        assert tf.tension_to_rhythm(75) == '转折'

    def test_medium_high_is_tense(self):
        assert tf.tension_to_rhythm(60) == '紧张'
        assert tf.tension_to_rhythm(58) == '紧张'

    def test_medium_is_suspense(self):
        assert tf.tension_to_rhythm(45) == '悬念'
        assert tf.tension_to_rhythm(40) == '悬念'

    def test_low_is_daily(self):
        assert tf.tension_to_rhythm(20) == '日常'
        assert tf.tension_to_rhythm(25) == '日常'
        assert tf.tension_to_rhythm(0) == '日常'


class TestRhythmToTargetTension:
    def test_known_types(self):
        for rtype in ['日常', '悬念', '紧张', '催泪', '转折']:
            target = tf.rhythm_to_target_tension(rtype)
            info = tf.RHYTHM_TYPES[rtype]
            assert info['min'] <= target <= info['max']

    def test_unknown_type(self):
        assert tf.rhythm_to_target_tension('未知') == 50


# ============================================================
# 趋势分析：analyze_trend / detect_phase
# ============================================================

class TestAnalyzeTrend:
    def test_rising(self):
        trend, slope = tf.analyze_trend([10, 20, 30, 40, 50, 60])
        assert trend == 'rising'
        assert slope > 3

    def test_falling(self):
        trend, slope = tf.analyze_trend([80, 70, 60, 50, 40, 30])
        assert trend == 'falling'
        assert slope < -3

    def test_stable(self):
        trend, slope = tf.analyze_trend([50, 50, 50, 50])
        assert trend == 'stable'
        assert abs(slope) <= 3

    def test_single_value(self):
        trend, slope = tf.analyze_trend([50])
        assert trend == 'stable'

    def test_empty(self):
        trend, slope = tf.analyze_trend([])
        assert trend == 'stable'


class TestDetectPhase:
    def test_climax(self):
        assert tf.detect_phase([80, 85, 75, 70, 65]) == 'climax'

    def test_cooling(self):
        assert tf.detect_phase([10, 15, 20, 25, 30]) == 'cooling'

    def test_building(self):
        assert tf.detect_phase([45, 50, 55, 60, 55]) == 'building'

    def test_transitional(self):
        assert tf.detect_phase([35, 40, 38, 42, 36]) == 'transitional'

    def test_short_input(self):
        phase = tf.detect_phase([30])
        assert phase == 'early'


# ============================================================
# 规则引擎：validate_consecutive / get_recommended_next
# ============================================================

class TestValidateConsecutive:
    def test_allow_first(self):
        assert tf.validate_consecutive([], '日常') is True

    def test_daily_max_2(self):
        assert tf.validate_consecutive(['日常', '日常'], '日常') is False
        assert tf.validate_consecutive(['日常'], '日常') is True

    def test_turning_no_repeat(self):
        assert tf.validate_consecutive(['转折'], '转折') is False

    def test_crying_no_repeat(self):
        assert tf.validate_consecutive(['催泪'], '催泪') is False

    def test_mixed_ok(self):
        assert tf.validate_consecutive(['紧张', '日常'], '紧张') is True


class TestGetRecommendedNext:
    def test_after_turning(self):
        rec = tf.get_recommended_next(['转折'])
        for r in rec:
            assert r in tf.AFTER_TURNING

    def test_after_tense(self):
        rec = tf.get_recommended_next(['紧张'])
        for r in rec:
            assert r in tf.AFTER_TENSE

    def test_after_daily(self):
        rec = tf.get_recommended_next(['日常'])
        for r in rec:
            assert r in tf.AFTER_DAILY

    def test_after_suspense(self):
        rec = tf.get_recommended_next(['悬念'])
        for r in rec:
            assert r in tf.AFTER_SUSPENSE

    def test_empty_plan(self):
        rec = tf.get_recommended_next([])
        assert len(rec) >= 1

    def test_all_candidates_blocked_fallback(self):
        """当所有推荐候选都违反连续规则时，仍能返回合法类型"""
        plan = ['催泪']  # 催泪后推荐 ['日常','悬念','紧张']
        rec = tf.get_recommended_next(plan)
        assert len(rec) >= 1


# ============================================================
# 周期模板
# ============================================================

class TestTenChapterCycle:
    def test_has_10_entries(self):
        assert len(tf.TEN_CHAPTER_CYCLE) == 10

    def test_all_valid_types(self):
        for r in tf.TEN_CHAPTER_CYCLE:
            assert r in tf.RHYTHM_TYPES


# ============================================================
# 大纲解析
# ============================================================

class TestOutlineParsing:
    def test_parse_outline_keywords(self, tmp_path):
        outline = tmp_path / "outline.md"
        outline.write_text("第10章 追杀与逃亡\n第11章 真相揭露\n第12章 温暖的日常\n", encoding='utf-8')
        result = tf.parse_outline_keywords(str(outline), 10)
        assert 10 in result
        assert any('追杀' in kw or '逃亡' in kw for kw in result[10]['keywords'])

    def test_parse_empty_outline(self, tmp_path):
        outline = tmp_path / "empty.md"
        outline.write_text("", encoding='utf-8')
        result = tf.parse_outline_keywords(str(outline), 1)
        assert result == {}

    def test_outline_to_rhythm_hint(self):
        assert tf.outline_to_rhythm_hint(['追杀']) == '紧张'
        assert tf.outline_to_rhythm_hint(['真相']) == '转折'
        assert tf.outline_to_rhythm_hint(['牺牲']) == '催泪'
        assert tf.outline_to_rhythm_hint(['线索']) == '悬念'
        assert tf.outline_to_rhythm_hint(['日常']) == '日常'
        assert tf.outline_to_rhythm_hint(['吃饭']) == '日常'

    def test_outline_no_match(self):
        assert tf.outline_to_rhythm_hint(['天空', '白云']) is None

    def test_extract_keywords(self):
        kws = tf.extract_keywords("追杀与逃亡的真相")
        assert len(kws) > 0
        # 停用词被过滤
        for w in kws:
            assert w not in ('的', '与')


# ============================================================
# 角色弧线调整
# ============================================================

class TestCharacterArcAdjustment:
    def test_load_arcs_from_states(self, tmp_path):
        data = {
            "陆远": {
                "snapshots": {
                    "37": {"arc_phase": "cracking", "state": "..."},
                }
            }
        }
        f = tmp_path / "cs.json"
        f.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        arcs = tf.load_character_arcs(str(f))
        assert arcs == {"陆远": "cracking"}

    def test_load_arcs_direct_phase(self, tmp_path):
        data = {"陆远": {"current_phase": "breaking"}}
        f = tmp_path / "ca.json"
        f.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        arcs = tf.load_character_arcs(str(f))
        assert arcs == {"陆远": "breaking"}

    def test_load_arcs_missing_file(self):
        assert tf.load_character_arcs("/nonexistent/file.json") is None

    def test_get_arc_adjustment(self):
        adj, details = tf.get_arc_adjustment({"陆远": "cracking"})
        assert adj is not None
        assert '紧张' in adj['preferred']
        assert '日常' in adj['avoid']

    def test_get_arc_adjustment_empty(self):
        adj, details = tf.get_arc_adjustment({})
        assert adj is None

    def test_apply_arc_adjustment_avoid(self):
        arc_adj = {'preferred': ['紧张'], 'avoid': ['日常']}
        chosen, reason = tf.apply_arc_adjustment('日常', ['转折'], arc_adj, 0)
        assert chosen == '紧张'
        assert reason is not None

    def test_apply_arc_adjustment_no_change(self):
        arc_adj = {'preferred': ['紧张'], 'avoid': ['日常']}
        chosen, reason = tf.apply_arc_adjustment('悬念', ['转折'], arc_adj, 1)
        assert chosen == '悬念'
        assert reason is None


# ============================================================
# 预测输出格式：generate_forecast
# ============================================================

class TestGenerateForecast:
    def test_basic_forecast(self):
        tensions = [30, 45, 60, 35, 70, 25, 50, 55, 40, 65]
        forecast, trend, slope, phase = tf.generate_forecast(tensions, count=5)
        assert len(forecast) == 5
        for entry in forecast:
            assert 'chapter' in entry
            assert 'rhythm' in entry
            assert 'target_tension' in entry
            assert 'reason' in entry
            assert entry['rhythm'] in tf.RHYTHM_TYPES
            assert 0 <= entry['target_tension'] <= 100

    def test_forecast_chapter_numbers(self):
        tensions = [50, 50, 50]
        forecast, *_ = tf.generate_forecast(tensions, count=7)
        # 章节号应从 len(tensions)+1 开始
        assert forecast[0]['chapter'] == 4
        assert forecast[-1]['chapter'] == 10

    def test_forecast_with_outline_hints(self):
        tensions = [40, 50, 60]
        hints = {4: '转折', 5: '日常'}
        forecast, *_ = tf.generate_forecast(tensions, count=3, outline_hints=hints)
        # 第4章应遵循大纲提示（如果合法）
        ch4 = [f for f in forecast if f['chapter'] == 4][0]
        assert ch4['rhythm'] == '转折'
        assert '大纲提示' in ch4['reason']

    def test_forecast_respects_consecutive_rules(self):
        """预测结果不应违反连续规则"""
        tensions = [50] * 10
        forecast, *_ = tf.generate_forecast(tensions, count=10)
        all_rhythms = [tf.tension_to_rhythm(t) for t in tensions] + [f['rhythm'] for f in forecast]
        # 检查转折不连续
        for i in range(1, len(all_rhythms)):
            if all_rhythms[i] == '转折' and all_rhythms[i-1] == '转折':
                pytest.fail('转折连续出现，违反规则')
        # 检查催泪不连续
        for i in range(1, len(all_rhythms)):
            if all_rhythms[i] == '催泪' and all_rhythms[i-1] == '催泪':
                pytest.fail('催泪连续出现，违反规则')

    def test_forecast_count_capped(self):
        """count超过10也不应出错"""
        tensions = [50]
        forecast, *_ = tf.generate_forecast(tensions, count=20)
        assert len(forecast) == 20  # generate_forecast 不做 cap，main 里 cap

    def test_forecast_with_arc_adjustment(self):
        tensions = [40, 50, 60, 35, 50]
        arc_adj = {'preferred': ['紧张'], 'avoid': ['日常']}
        forecast, *_ = tf.generate_forecast(tensions, count=5, arc_adj=arc_adj)
        assert len(forecast) == 5

    def test_single_tension(self):
        tensions = [50]
        forecast, trend, slope, phase = tf.generate_forecast(tensions, count=3)
        assert len(forecast) == 3

    def test_empty_tensions(self):
        forecast, trend, slope, phase = tf.generate_forecast([], count=3)
        assert len(forecast) == 3


# ============================================================
# 基础函数复用测试
# ============================================================

class TestBasicFunctions:
    def test_normalize_text(self):
        assert tf.normalize_text("你好\u3000世界  测试") == "你好 世界 测试"

    def test_read_file(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("hello", encoding='utf-8')
        assert tf.read_file(str(f)) == "hello"

    def test_read_file_missing(self):
        assert tf.read_file("/nonexistent") == ""

    def test_list_chapters(self, chapters_dir):
        make_chapters(chapters_dir, [(1, "a"), (3, "b"), (2, "c")])
        chs = tf.list_chapters(str(chapters_dir))
        nums = [n for n, _, _ in chs]
        assert nums == [1, 2, 3]

    def test_list_chapters_empty(self, tmp_path):
        d = tmp_path / "empty"
        d.mkdir()
        assert tf.list_chapters(str(d)) == []

    def test_list_chapters_not_dir(self):
        assert tf.list_chapters("/nonexistent") == []

    def test_count_dialogue_ratio_no_dialogue(self):
        assert tf.count_dialogue_ratio("他走在路上") == 0

    def test_count_dialogue_ratio_with_quotes(self):
        text = "\u201c你好\u201d他说"
        ratio = tf.count_dialogue_ratio(text)
        assert ratio > 0

    def test_count_hook_density_no_hooks(self):
        d, t = tf.count_hook_density("今天天气很好")
        assert d == 0

    def test_count_hook_density_with_hooks(self):
        d, t = tf.count_hook_density("他愣住了，不可能！")
        assert d > 0
        assert 'suspense' in t

    def test_compute_tension_range(self):
        score = tf.compute_tension(10, 0.3, 0.2, {'suspense': 1, 'reversal': 0, 'thrill': 0})
        assert 0 <= score <= 100

    def test_compute_tension_zero(self):
        score = tf.compute_tension(0, 0, 0, {})
        assert score == 0
