"""伏笔扫描脚本测试"""
import json
import os
import pytest
from pathlib import Path

# 导入被测模块
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from foreshadow_scan import ForeshadowScanner, format_report, list_chapters, __version__


def write_chapter(tmp_path, num, content, title="测试"):
    """辅助：写一个章节文件"""
    d = tmp_path / "chapters"
    d.mkdir(exist_ok=True)
    f = d / f"第{num:03d}章_{title}.md"
    f.write_text(content, encoding='utf-8')
    return str(d)


# ============================================================
# 测试用例
# ============================================================


class TestVersion:
    """版本号测试"""

    def test_version_string(self):
        assert __version__ == "v2.2.0"


class TestPatternMatching:
    """模式匹配测试"""

    def test_ignore_pattern_没在意(self):
        """忽略线索：没在意"""
        scanner = ForeshadowScanner(novel_dir="/tmp/none")
        text = "桌上放着一把钥匙，不过那时候他没在意。\n他继续往前走。"
        findings = scanner.scan_text(text)
        assert any(f["type"] == "忽略线索" for f in findings)

    def test_ignore_pattern_没多想(self):
        """忽略线索：没多想"""
        scanner = ForeshadowScanner(novel_dir="/tmp/none")
        text = "电话那头传来一声叹息，他没多想就挂了。"
        findings = scanner.scan_text(text)
        assert any(f["type"] == "忽略线索" for f in findings)

    def test_hindsight_pattern_后来才知道(self):
        """后知后觉：后来他才知道"""
        scanner = ForeshadowScanner(novel_dir="/tmp/none")
        text = "后来他才知道，那通电话意味着什么。"
        findings = scanner.scan_text(text)
        assert any(f["type"] == "后知后觉" for f in findings)

    def test_hindsight_pattern_多年以后(self):
        """后知后觉：多年以后"""
        scanner = ForeshadowScanner(novel_dir="/tmp/none")
        text = "多年以后他才明白，那天的选择改变了一切。"
        findings = scanner.scan_text(text)
        assert any(f["type"] == "后知后觉" for f in findings)

    def test_unease_pattern_奇怪的是(self):
        """异常感觉：奇怪的是"""
        scanner = ForeshadowScanner(novel_dir="/tmp/none")
        text = "奇怪的是，门锁着，灯却亮着。"
        findings = scanner.scan_text(text)
        assert any(f["type"] == "异常感觉" for f in findings)

    def test_unease_pattern_说不上来哪里不对(self):
        """异常感觉：说不上来哪里不对"""
        scanner = ForeshadowScanner(novel_dir="/tmp/none")
        text = "他看了看四周，说不上来哪里不对，总觉得有点怪。"
        findings = scanner.scan_text(text)
        assert any(f["type"] == "异常感觉" for f in findings)

    def test_no_false_positive(self):
        """正常文本不应误报"""
        scanner = ForeshadowScanner(novel_dir="/tmp/none")
        text = "他走进房间，倒了杯水，坐在沙发上看电视。\n今天天气不错。"
        findings = scanner.scan_text(text)
        assert len(findings) == 0

    def test_detail_description_detection(self):
        """异常细节描写检测"""
        scanner = ForeshadowScanner(novel_dir="/tmp/none", detail_length_threshold=40)
        text = "那个盒子看起来做工极为精细，表面刻着密密麻麻的纹路，散发着淡淡的金属光泽，摸起来冰凉刺骨。"
        findings = scanner.scan_text(text)
        assert any(f["type"] == "异常细节描写" for f in findings)


class TestChapterScanning:
    """章节扫描测试"""

    def test_scan_chapters_finds_foreshadow(self, tmp_path):
        """扫描多章节，能发现伏笔"""
        novel_dir = write_chapter(tmp_path, 1, "不过那时候他没在意那个细节。")
        write_chapter(tmp_path, 2, "后来他才知道，事情没那么简单。")
        write_chapter(tmp_path, 3, "今天天气很好，他出去散步了。")

        scanner = ForeshadowScanner(novel_dir=novel_dir)
        results = scanner.scan_chapters()
        assert 1 in results
        assert 2 in results
        assert 3 not in results  # 第3章没有伏笔

    def test_empty_directory(self, tmp_path):
        """空目录不应报错"""
        empty = tmp_path / "empty"
        empty.mkdir()
        scanner = ForeshadowScanner(novel_dir=str(empty))
        results = scanner.scan_chapters()
        assert results == {}


class TestUnresolvedCheck:
    """未回收伏笔检查测试"""

    def test_unresolved_with_foreshadowing_json(self, tmp_path):
        """有 foreshadowing.json 时检查未回收伏笔"""
        novel_dir = write_chapter(tmp_path, 1, "不过那时候他没在意。")
        write_chapter(tmp_path, 40, "剧情继续发展。")

        foreshadow_file = tmp_path / "foreshadowing.json"
        foreshadow_file.write_text(json.dumps({
            "foreshadowing": [
                {"description": "神秘钥匙", "planted_chapter": 1, "status": "planted"},
                {"description": "已解决的伏笔", "planted_chapter": 2, "status": "resolved"},
            ]
        }, ensure_ascii=False))

        scanner = ForeshadowScanner(
            novel_dir=novel_dir,
            foreshadowing_path=str(foreshadow_file),
            max_unresolved_gap=30,
        )
        results = scanner.scan_chapters()
        unresolved = scanner.check_unresolved(results, 40)
        # 神秘钥匙 跨了39章，超过阈值
        assert len(unresolved) == 1
        assert unresolved[0]["warning"] == "可能遗忘"

    def test_no_foreshadowing_file(self, tmp_path):
        """没有 foreshadowing.json 时返回空列表"""
        novel_dir = write_chapter(tmp_path, 1, "不过那时候他没在意。")
        scanner = ForeshadowScanner(novel_dir=novel_dir)
        results = scanner.scan_chapters()
        unresolved = scanner.check_unresolved(results, 1)
        assert unresolved == []


class TestSuggestions:
    """建议生成测试"""

    def test_suggest_output(self, tmp_path):
        """suggest 模式生成建议"""
        novel_dir = write_chapter(tmp_path, 1, "不过那时候他没在意那个细节。")
        scanner = ForeshadowScanner(novel_dir=novel_dir, suggest=True)
        results = scanner.scan_chapters()
        suggestions = scanner.generate_suggestions(results, [])
        assert len(suggestions) > 0
        assert "忽略线索" in suggestions[1]


class TestReportFormat:
    """报告格式测试"""

    def test_format_report_contains_chapter(self):
        """报告包含章节信息"""
        report = {
            "total_chapters": 2,
            "scan_results": {1: [{"type": "忽略线索", "pattern": "没在意", "line": 3, "context": "不过那时候他没在意"}]},
            "unresolved": [],
            "suggestions": [],
        }
        output = format_report(report)
        assert "第1章" in output
        assert "忽略线索" in output
