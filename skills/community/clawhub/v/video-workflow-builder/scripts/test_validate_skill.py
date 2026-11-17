import os
import validate_skill as v

_REQUIRED = ["content_db.py", "archive_content.py", "query_db.py",
             "update_metrics.py", "generate_cover.py", "fetch_hotlist.py",
             "web_search.py"]


def _make_skill(tmp_path, with_scripts):
    (tmp_path / "SKILL.md").write_text(
        "---\nname: x-workflow\ndescription: d\n---\n# x\n", encoding="utf-8")
    if with_scripts:
        sd = tmp_path / "scripts"
        sd.mkdir()
        for name in _REQUIRED:
            (sd / name).write_text("# stub\n", encoding="utf-8")


def test_missing_scripts_reported(tmp_path):
    _make_skill(tmp_path, with_scripts=False)
    problems = v.validate_skill_dir(str(tmp_path))
    assert any("archive_content.py" in p for p in problems)
    assert any("query_db.py" in p for p in problems)


def test_all_scripts_present_ok(tmp_path):
    _make_skill(tmp_path, with_scripts=True)
    problems = v.validate_skill_dir(str(tmp_path))
    assert problems == []
