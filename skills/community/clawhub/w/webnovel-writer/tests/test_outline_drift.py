"""outline_drift.py 的自动化测试"""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import outline_drift as od

class TestCharSimilarity:
    def test_identical(self):
        assert od.char_similarity("轮回影院", "轮回影院") == 1.0

    def test_similar(self):
        s = od.char_similarity("轮回影院的密室", "轮回影院")
        assert s > 0.3

    def test_different(self):
        s = od.char_similarity("完全不同", "毫不相干")
        assert s < 0.3

class TestNormalizeTitle:
    def test_strip_chapter_prefix(self):
        assert "第1章" not in od.normalize_title("第1章 轮回影院")
        assert "轮回" in od.normalize_title("第1章 轮回影院") or od.normalize_title("第1章 轮回影院").strip() != ""

class TestCnNumToInt:
    def test_basic(self):
        assert od.cn_num_to_int("一") == 1
        assert od.cn_num_to_int("十") == 10
        assert od.cn_num_to_int("二十一") == 21
        assert od.cn_num_to_int("三") == 3

class TestTitleMatch:
    def test_matching_titles(self):
        outline = [{"num": 1, "title": "轮回影院"}]
        actual = [{"num": 1, "title": "轮回影院的密室", "content": "内容", "filename": "第001章.md", "char_count": 100}]
        results = od.check_title_match(outline, actual)
        assert len(results) == 1
        assert results[0]["similarity"] > 0.3

    def test_missing_chapter(self):
        outline = [{"num": 1, "title": "开始"}, {"num": 2, "title": "继续"}]
        actual = [{"num": 1, "title": "开始了", "content": "c", "filename": "f", "char_count": 100}]
        results = od.check_title_match(outline, actual)
        statuses = [r["status"] for r in results]
        assert "缺失" in statuses

class TestDriftTrend:
    def test_stable_trend(self):
        results = [{"num": i, "similarity": 0.8, "status": "匹配"} for i in range(1, 11)]
        trend, points = od.calculate_drift_trend(results)
        assert "稳定" in trend

    def test_diverging_trend(self):
        results = [{"num": i, "similarity": 0.9 - i * 0.08, "status": "偏差" if i > 5 else "匹配"} for i in range(1, 11)]
        trend, points = od.calculate_drift_trend(results)
        assert "偏离" in trend

class TestComputeDriftScore:
    def test_perfect_match(self):
        title_r = [{"num": 1, "similarity": 1.0}]
        kw_r = [{"num": 1, "coverage": 1.0}]
        char_r = [{"num": 1, "expected": ["张三"], "present": ["张三"]}]
        score = od.compute_drift_score(1, title_r, kw_r, char_r)
        assert score == 0.0

    def test_total_drift(self):
        title_r = [{"num": 1, "similarity": 0.0}]
        kw_r = [{"num": 1, "coverage": 0.0}]
        char_r = [{"num": 1, "expected": ["张三"], "present": []}]
        score = od.compute_drift_score(1, title_r, kw_r, char_r)
        assert score == 100.0

class TestParseOutline:
    def test_parse_chapter_list(self, tmp_path):
        outline_content = """# 第1卷 觉醒（第1-10章）
1. 初始之日
2. 命运邂逅
3. 暗流涌动

# 第2卷 挣扎（第11-20章）
11. 新的开始
"""
        f = tmp_path / "outline.md"
        f.write_text(outline_content, encoding='utf-8')
        vols = od.parse_chapter_list(str(f))
        assert len(vols) == 2
        assert vols[0]["vol"] == 1
        assert len(vols[0]["chapters"]) == 3
        assert vols[1]["chapters"][0]["num"] == 11

    def test_parse_chapters_dir(self, tmp_path):
        d = tmp_path / "chapters"
        d.mkdir()
        (d / "第001章_测试章节.md").write_text("# 测试章节\n正文内容", encoding='utf-8')
        (d / "第002章_另一个.md").write_text("# 另一个\n更多内容", encoding='utf-8')
        chs = od.parse_chapters_dir(str(d))
        assert len(chs) == 2
        assert chs[0]["num"] == 1

class TestKeywordCoverage:
    def test_full_coverage(self):
        outline = [{"num": 1, "keywords": ["轮回", "影院"]}]
        actual = [{"num": 1, "title": "t", "content": "轮回影院的大门", "filename": "f", "char_count": 100}]
        results = od.check_keyword_coverage(outline, actual)
        assert results[0]["coverage"] == 1.0

    def test_no_coverage(self):
        outline = [{"num": 1, "keywords": ["量子", "纠缠"]}]
        actual = [{"num": 1, "title": "t", "content": "完全无关的内容", "filename": "f", "char_count": 100}]
        results = od.check_keyword_coverage(outline, actual)
        assert results[0]["coverage"] == 0.0
