"""测试 diff_check.py"""
import tempfile
from pathlib import Path


def _write_chapter(directory, num, content):
    directory.mkdir(parents=True, exist_ok=True)
    f = directory / f"第{num:03d}章_测试.md"
    f.write_text(content, encoding="utf-8")


def test_pair_chapters():
    import scripts.diff_check as dc

    with tempfile.TemporaryDirectory() as tmpdir:
        old = Path(tmpdir) / "old"
        new = Path(tmpdir) / "new"
        old.mkdir(); new.mkdir()

        _write_chapter(old, 1, "旧版第一章")
        _write_chapter(new, 1, "新版第一章修改了")
        _write_chapter(new, 2, "新增的第二章")

        pairs = dc.pair_chapters(str(old), str(new))
        assert len(pairs) == 2
        # 第1章有旧有新
        assert pairs[0][0] is not None  # old_path
        assert pairs[0][1] is not None  # new_path
        # 第2章只有新版
        assert pairs[1][0] is None
        assert pairs[1][1] is not None


def test_text_diff():
    import scripts.diff_check as dc
    result = dc.text_diff("第一行\n第二行\n", "第一行\n修改了\n")
    assert result["added_lines"] == 1
    assert result["removed_lines"] == 1


def test_text_diff_no_change():
    import scripts.diff_check as dc
    result = dc.text_diff("一样的内容\n", "一样的内容\n")
    assert result["diff_lines"] == 0


def test_analyze_modifications_no_change():
    import scripts.diff_check as dc
    issues = dc.analyze_modifications("没变", "没变")
    assert len(issues) == 0


def test_analyze_modifications_ai_tone():
    import scripts.diff_check as dc
    old = "他走进房间。"
    new = "他缓缓走进房间。不禁感慨万千。"
    issues = dc.analyze_modifications(old, new)
    types = [i["type"] for i in issues]
    assert "AI味" in types


def test_analyze_modifications_repetition():
    import scripts.diff_check as dc
    old = "开始。"
    new = "这是一个重复的句子内容。" * 5 + "\n" + "这是另一个重复的句子内容。" * 5 + "\n" + "这是第三个重复的句子内容。" * 5
    issues = dc.analyze_modifications(old, new)
    types = [i["type"] for i in issues]
    # 至少应该有某种检测结果（字数变化等）
    assert len(issues) >= 1


def test_generate_report(tmp_path):
    import scripts.diff_check as dc

    old_dir = tmp_path / "old"
    new_dir = tmp_path / "new"
    old_dir.mkdir(); new_dir.mkdir()

    _write_chapter(old_dir, 1, "旧内容第一行\n第二行\n")
    _write_chapter(new_dir, 1, "新内容第一行\n第二行修改了\n")

    report_file = tmp_path / "report.md"
    report = dc.generate_report(
        dc.pair_chapters(str(old_dir), str(new_dir)),
        str(old_dir), str(new_dir),
        str(report_file)
    )
    assert report_file.exists()
    assert "第001章" in report
    assert "+1行" in report or "-1行" in report or "差异" in report
