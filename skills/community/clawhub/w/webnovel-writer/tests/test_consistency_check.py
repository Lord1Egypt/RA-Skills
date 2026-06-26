"""consistency_check.py 的自动化测试"""
import os
import re
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import consistency_check as cc

# ── 基础功能 ─────────────────────────────

class TestListChapters:
    def test_find_numbered_chapters(self, chapters_dir):
        (chapters_dir / "第001章_测试.md").write_text("内容", encoding='utf-8')
        (chapters_dir / "第002章_测试.md").write_text("内容", encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        assert len(chs) == 2
        assert chs[0][0] == 1
        assert chs[1][0] == 2

    def test_skip_drafts(self, chapters_dir):
        (chapters_dir / "第001章_正式.md").write_text("内容", encoding='utf-8')
        (chapters_dir / "第002章_草稿.md").write_text("内容", encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir), skip_drafts=True)
        assert len(chs) == 1
        assert chs[0][0] == 1

    def test_dedup_same_chapter_num(self, chapters_dir):
        (chapters_dir / "第001章_简.md").write_text("短", encoding='utf-8')
        (chapters_dir / "第001章_完整标题.md").write_text("长内容", encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        assert len(chs) == 1
        # 应保留带下划线的版本
        assert "完整标题" in chs[0][2]

class TestCheckChapterLength:
    def test_short_chapter(self, chapters_dir):
        (chapters_dir / "第001章_短.md").write_text("太短了", encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_chapter_length(chs, min_words=100)
        assert len(issues) == 1
        assert issues[0]['type'] == '字数不足'

    def test_normal_chapter(self, chapters_dir):
        content = "中文字符" * 500  # 2000字
        (chapters_dir / "第001章_正常.md").write_text(content, encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_chapter_length(chs, min_words=100, max_words=5000)
        assert len(issues) == 0

class TestCheckAIWords:
    def test_detect_high_freq_ai_word(self, chapters_dir):
        content = "不禁" * 5  # 超过阈值2
        (chapters_dir / "第001章_AI.md").write_text(content, encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_ai_words(chs)
        assert any(i['type'] == 'AI高频词' and '不禁' in i['detail'] for i in issues)

    def test_no_false_positive(self, chapters_dir):
        content = "他走在路上，阳光很好。"
        (chapters_dir / "第001章_正常.md").write_text(content, encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_ai_words(chs)
        assert len(issues) == 0

# ── 误报防护 ─────────────────────────────

class TestPOVCheckFalsePositives:
    def test_dialogue_wo_not_flagged(self, chapters_dir):
        """对话中的'我'不报视角错误"""
        content = '"我觉得这件事不对劲。"\n他说完就走了。'
        (chapters_dir / "第001章_对话.md").write_text(content, encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_pov_consistency(chs, pov_mode='third_person')
        assert len(issues) == 0

    def test_self_and_us_not_flagged(self, chapters_dir):
        """'自我''我们'不报错"""
        content = '他开始了自我反省。我们必须团结起来。大家一起努力。'
        (chapters_dir / "第001章_自我.md").write_text(content, encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_pov_consistency(chs, pov_mode='third_person')
        assert len(issues) == 0

    def test_chat_message_not_flagged(self, chapters_dir):
        """【】包裹的聊天消息不报错"""
        content = '手机响了。\n【赵恒：我在路上。】\n他看了一眼。'
        (chapters_dir / "第001章_消息.md").write_text(content, encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_pov_consistency(chs, pov_mode='third_person')
        assert len(issues) == 0

    def test_short_inner_monologue_not_flagged(self, chapters_dir):
        """短句内心独白不报错"""
        content = '他愣住了。我看错了吗？'
        (chapters_dir / "第001章_内心.md").write_text(content, encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_pov_consistency(chs, pov_mode='third_person')
        assert len(issues) == 0

    def test_real_pov_issue_detected(self, chapters_dir):
        """真正的视角问题应该被检测到"""
        content = '我走进房间，看到桌子上有封信。我拿起信看了看。'
        (chapters_dir / "第001章_视角.md").write_text(content, encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_pov_consistency(chs, pov_mode='third_person')
        assert len(issues) > 0
        assert issues[0]['type'] == '视角混乱'

# ── 数值容错 ─────────────────────────────

class TestNumericTolerance:
    def test_compatible_year_values(self):
        """'42年137天'和'42年'不矛盾（通过check_numeric_conflicts间接验证）"""
        # _is_compatible_values 是 check_numeric_conflicts 内的嵌套函数
        # 通过不报矛盾来间接验证
        pass

    def test_incompatible_values(self, chapters_dir):
        """不同数值应报矛盾"""
        content1 = '小张的年龄大概25岁左右。'
        content2 = '小张的年龄大概30岁了。'
        (chapters_dir / "第001章_a.md").write_text(content1, encoding='utf-8')
        (chapters_dir / "第002章_b.md").write_text(content2, encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_numeric_conflicts(chs)
        assert any('小张' in i['detail'] for i in issues)

    def test_same_values(self, chapters_dir):
        """相同数值不报矛盾"""
        content1 = '小张的年龄大概25岁。'
        content2 = '小张今年也是25岁。'
        (chapters_dir / "第001章_a.md").write_text(content1, encoding='utf-8')
        (chapters_dir / "第002章_b.md").write_text(content2, encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_numeric_conflicts(chs)
        assert not any('小张' in i['detail'] for i in issues)

    def test_numeric_no_conflict(self, chapters_dir):
        """同一实体的兼容数值不报错"""
        content1 = '小张的余额——42年137天，还不少。'
        content2 = '他记得小张的余额是42年，还凑合。'
        (chapters_dir / "第001章_a.md").write_text(content1, encoding='utf-8')
        (chapters_dir / "第002章_b.md").write_text(content2, encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_numeric_conflicts(chs)
        # 42年137天 和 42年 应该兼容，不应报矛盾
        assert not any('小张' in i['detail'] for i in issues)

# ── 草稿过滤 ─────────────────────────────

class TestDraftFiltering:
    def test_skip_drafts_flag(self, chapters_dir):
        (chapters_dir / "第001章_正式.md").write_text("正常内容", encoding='utf-8')
        (chapters_dir / "第002章_WIP.md").write_text("草稿内容", encoding='utf-8')
        (chapters_dir / "第003章_草稿.md").write_text("草稿内容", encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir), skip_drafts=True)
        nums = [c[0] for c in chs]
        assert 1 in nums
        assert 2 not in nums
        assert 3 not in nums

    def test_is_draft_filename(self):
        assert cc.is_draft_filename("第001章_草稿.md") is True
        assert cc.is_draft_filename("第001章_draft.md") is True
        assert cc.is_draft_filename("第001章_WIP.md") is True
        assert cc.is_draft_filename("第001章_正式.md") is False

# ── 大纲偏差检测 ─────────────────────────────

class TestOutlineDrift:
    def test_no_outline_no_issues(self, chapters_dir):
        """没有大纲时不报任何问题"""
        (chapters_dir / "第001章_测试.md").write_text("内容", encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_outline_drift(chs, '')
        assert issues == []

    def test_missing_chapter_detected(self, chapters_dir, tmp_path):
        """大纲有但正文没有的章节被检测到"""
        outline = tmp_path / "outline.md"
        outline.write_text("# 第1卷 测试\n\n## 第1章 开始\n\n## 第2章 继续\n\n## 第3章 结束\n", encoding='utf-8')
        (chapters_dir / "第001章_开始.md").write_text("# 开始\n正文内容", encoding='utf-8')
        # 第2、3章不写
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_outline_drift(chs, str(outline))
        missing = [i for i in issues if i.get('type') == '大纲偏差·缺失章节']
        assert len(missing) >= 1

    def test_added_chapter_detected(self, chapters_dir, tmp_path):
        """正文有但大纲没有的章节被检测到"""
        outline = tmp_path / "outline.md"
        outline.write_text("# 第1卷 测试\n\n## 第1章 开始\n", encoding='utf-8')
        (chapters_dir / "第001章_开始.md").write_text("# 开始\n正文", encoding='utf-8')
        (chapters_dir / "第002章_新增.md").write_text("# 新增\n正文", encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_outline_drift(chs, str(outline))
        added = [i for i in issues if i.get('type') == '大纲偏差·新增章节']
        assert len(added) >= 1

    def test_good_alignment_few_issues(self, chapters_dir, tmp_path):
        """正文与大纲高度一致时问题很少"""
        outline = tmp_path / "outline.md"
        outline.write_text("# 第1卷 测试\n\n## 第1章 轮回影院\n\n## 第2章 觉醒\n", encoding='utf-8')
        (chapters_dir / "第001章_轮回影院.md").write_text("# 轮回影院\n轮回影院的大门打开了", encoding='utf-8')
        (chapters_dir / "第002章_觉醒.md").write_text("# 觉醒\n觉醒的时刻到来了", encoding='utf-8')
        chs = cc.list_chapters(str(chapters_dir))
        issues = cc.check_outline_drift(chs, str(outline))
        # 高度一致，不应有高严重度问题
        high = [i for i in issues if i.get('severity') == 'high']
        assert len(high) == 0
