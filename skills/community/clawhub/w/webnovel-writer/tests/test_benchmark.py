"""测试 benchmark.py"""
import tempfile
from pathlib import Path


def test_benchmark_script():
    from scripts import benchmark as bm
    result = bm.benchmark_script("nonexistent_script", [])
    assert result is None


def test_list_chapters(tmp_path):
    from scripts import benchmark as bm

    d = tmp_path / "chapters"
    d.mkdir()
    (d / "第001章_开始.md").write_text("内容" * 100)
    (d / "第002章_发展.md").write_text("内容" * 200)
    (d / "not_a_chapter.md").write_text("无关")

    chapters = bm.list_chapters(str(d))
    # list_chapters 返回所有 .md，不过滤
    assert len(chapters) == 3
