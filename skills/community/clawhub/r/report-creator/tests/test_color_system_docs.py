from pathlib import Path

from tests.reference_loader import rendering_reference_text, shell_reference_text


REPO_ROOT = Path(__file__).parent.parent
DEMO_PAGES = sorted((REPO_ROOT / "templates").glob("*/**/*.html"))


def read(rel_path: str) -> str:
    return (REPO_ROOT / rel_path).read_text(encoding="utf-8")


def test_corporate_blue_theme_uses_warm_business_tokens():
    src = read("templates/themes/corporate-blue.css")
    assert "--bg: #F8F5EF;" in src
    assert "--surface: #FFFDF9;" in src
    assert "--text: #2B2623;" in src
    assert "--primary: #1F6F50;" in src
    assert "--accent: #C79A2B;" in src
    assert "--border: #E7DDD2;" in src


def test_design_quality_business_hint_matches_new_default_direction():
    src = read("references/design-quality.md")
    assert "| **Business / Data** | 销售、营收、KPI、增长、季报、业绩 / sales, revenue, KPI, growth, quarterly | `#1F6F50` (pine green) | Restrained, commercial, premium |" in src


def test_rendering_rules_remove_rainbow_kpi_cycle_and_define_comparison_mode():
    src = rendering_reference_text()
    assert "assign `data-accent` cycling `blue → green → purple → orange`" not in src
    assert "Default mode: do not add `data-accent` to KPI cards." in src
    assert 'Set `data-report-mode="comparison"` on the comparison wrapper only when the report is explicitly comparing named entities.' in src
    assert ".badge--entity-a" in src


def test_html_shell_template_uses_neutral_badges_and_report_mode_attribute():
    src = shell_reference_text()
    assert 'data-report-mode="[default|comparison]"' in src
    assert ".badge--blue   { background: var(--report-chip-bg" in src
    assert ".badge--entity-a" in src
    assert '.kpi-card[data-accent="blue"]' not in src


def test_skill_guidance_keeps_corporate_blue_id_but_teaches_comparison_mode():
    src = read("SKILL.md")
    assert "theme: corporate-blue                  # Optional. Default: corporate-blue" in src
    assert 'When the report is explicitly comparing named vendors, models, or tools, set `data-report-mode=\"comparison\"` on the outer report container and use `.badge--entity-a/.badge--entity-b/.badge--entity-c` only for entity identity.' in src


def test_demo_pages_replace_rainbow_shared_css_with_neutral_chip_system():
    assert DEMO_PAGES
    for page in DEMO_PAGES:
        src = page.read_text(encoding="utf-8")
        assert '.kpi-card[data-accent="blue"]' not in src, page
        assert ".badge--blue { background: #DBEAFE; color: #1E40AF; }" not in src, page
        assert "data-report-mode=\"default\"" in src, page
        assert ".badge--blue { background: var(--report-chip-bg" in src, page


def test_readmes_describe_corporate_blue_as_warm_premium_default():
    readme_en = read("README.md")
    readme_zh = read("README.zh-CN.md")
    assert "<sub>Warm Premium · Business</sub>" in readme_en
    assert "<sub>暖感商务 · 高级汇报</sub>" in readme_zh
