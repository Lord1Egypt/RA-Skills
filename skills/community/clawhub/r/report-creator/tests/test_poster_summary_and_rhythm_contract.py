from pathlib import Path

from tests.reference_loader import shell_reference_text


ROOT = Path(__file__).resolve().parent.parent


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def test_html_shell_template_uses_poster_summary_title_hierarchy():
    src = shell_reference_text()

    required_markers = [
        '"poster_title"',
        '"poster_subtitle"',
        ".sc-title-main",
        ".sc-title-sub",
        "font-size: clamp(3.45rem, 6.9vw, 5.25rem);",
        "max-width: 82%;",
        "poster title should dominate the card",
    ]

    for marker in required_markers:
        assert marker in src, f"html-shell-template.md missing poster summary marker: {marker}"

    assert ".sc-byline" not in src, "summary card should not duplicate byline/meta copy"
    assert "metaParts.length" not in src, "summary card should not inject author/date filler text"


def test_minimal_fixture_reflects_poster_summary_contract():
    html = read("tests/fixtures/minimal_report.html")

    for marker in [
        '"poster_title"',
        '"poster_subtitle"',
        ".sc-title-main",
        ".sc-title-sub",
    ]:
        assert marker in html, f"minimal_report.html missing poster summary marker: {marker}"


def test_docs_require_narrative_rhythm_blocks_not_just_shorter_paragraphs():
    skill = read("SKILL.md")
    checklist = read("references/review-checklist.md")
    shell = shell_reference_text()
    design = read("references/design-quality.md")

    for marker in [
        "lead-block",
        "section-quote",
        "action-grid",
    ]:
        assert marker in skill, f"SKILL.md missing narrative rhythm marker: {marker}"
        assert marker in checklist, f"review-checklist.md missing narrative rhythm marker: {marker}"
        assert marker in shell, f"html-shell-template.md missing narrative rhythm CSS marker: {marker}"
        assert marker in design, f"design-quality.md missing narrative rhythm guidance marker: {marker}"

    assert "claim -> explanation -> scan anchor" in skill
    assert "promote a decisive opening sentence into a lead block" in checklist
