import os
import tempfile
import textwrap

from scripts.validate_skill import validate_skill_dir


def _write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def test_missing_skill_md_is_reported():
    with tempfile.TemporaryDirectory() as d:
        problems = validate_skill_dir(d)
        assert any("SKILL.md" in p for p in problems)


def test_missing_frontmatter_fields_reported():
    with tempfile.TemporaryDirectory() as d:
        _write(os.path.join(d, "SKILL.md"), "# no frontmatter here\n")
        problems = validate_skill_dir(d)
        assert any("name" in p for p in problems)
        assert any("description" in p for p in problems)


def test_broken_reference_link_reported():
    with tempfile.TemporaryDirectory() as d:
        _write(
            os.path.join(d, "SKILL.md"),
            textwrap.dedent(
                """\
                ---
                name: sample
                description: sample skill
                ---
                See [topic](references/topic-selection.md).
                """
            ),
        )
        problems = validate_skill_dir(d)
        assert any("references/topic-selection.md" in p for p in problems)


_REQUIRED_SCRIPTS = [
    "content_db.py", "archive_content.py", "query_db.py",
    "update_metrics.py", "generate_cover.py", "fetch_hotlist.py",
    "web_search.py",
]


def test_valid_skill_returns_no_problems():
    with tempfile.TemporaryDirectory() as d:
        _write(
            os.path.join(d, "SKILL.md"),
            textwrap.dedent(
                """\
                ---
                name: sample
                description: sample skill
                ---
                See [topic](references/topic-selection.md).
                """
            ),
        )
        _write(os.path.join(d, "references", "topic-selection.md"), "# topic\n")
        # 校验器现在还要求产物自带一组必需脚本，合法样本得把它们补齐
        for name in _REQUIRED_SCRIPTS:
            _write(os.path.join(d, "scripts", name), "# stub\n")
        problems = validate_skill_dir(d)
        assert problems == []
