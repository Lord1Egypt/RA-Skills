from pathlib import Path

from tests.reference_loader import rendering_reference_text, shell_reference_text


ROOT = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_skill_declares_ir_validity_taxonomy():
    src = read("SKILL.md")
    for marker in [
        "`invalid_syntax`",
        "`invalid_semantics`",
        "`contract_conflict`",
        "`auto_downgrade_target`",
    ]:
        assert marker in src, f"SKILL.md missing IR taxonomy marker: {marker}"


def test_chart_contract_is_echarts_only_everywhere():
    skill = read("SKILL.md")
    rules = rendering_reference_text()
    shell = shell_reference_text()

    assert "Use **ECharts** for ALL charts" in skill
    assert "Use **ECharts** for ALL charts" in rules
    assert "Chart.js is NOT used in the standard template." in rules
    assert "Default to Chart.js" not in skill
    assert "Default to Chart.js" not in rules
    assert "using Chart.js" not in shell


def test_docs_mark_badges_as_optional_and_highlight_sentence_as_prose():
    skill = read("SKILL.md")
    rules = rendering_reference_text()
    readme_en = read("README.md")
    readme_zh = read("README.zh-CN.md")

    assert "Badges are optional visual enhancements, not a first-class IR tag." in skill
    assert "Badges are optional visual enhancements, not a first-class IR tag." in rules
    assert "`highlight-sentence` is a prose pattern, not an IR tag." in rules
    assert "Badges remain optional HTML chips" in readme_en
    assert "`badge` 仍然只是可选的 HTML 扫读增强" in readme_zh


def test_docs_publish_canonical_kpi_form_and_timeline_whitelist():
    skill = read("SKILL.md")
    rules = rendering_reference_text()
    readme_en = read("README.md")
    readme_zh = read("README.zh-CN.md")

    assert "items:" in skill
    assert "items:" in rules
    assert "items:" in readme_en
    assert "items:" in readme_zh
    assert "Allowed `Date` tokens" in skill
    assert "Whitelist for `Date`" in rules
