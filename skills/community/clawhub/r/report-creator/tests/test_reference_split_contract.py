from scripts.context_isolation import resolve_required_refs
from tests.reference_loader import (
    RENDERING_REFERENCE_FILES,
    SHELL_REFERENCE_FILES,
    read_reference,
    rendering_reference_text,
    shell_reference_text,
)


def test_split_reference_files_exist_and_entry_files_stay_small():
    for path in SHELL_REFERENCE_FILES + RENDERING_REFERENCE_FILES:
        assert read_reference(path), f"missing or empty reference: {path}"

    assert len(read_reference("references/html-shell-template.md").encode("utf-8")) < 20_000
    assert len(read_reference("references/rendering-rules.md").encode("utf-8")) < 20_000


def test_shell_entry_only_fallback_keeps_historical_red_lines():
    entry = read_reference("references/html-shell-template.md")
    for marker in [
        'id="export-btn"',
        'id="export-menu"',
        'id="export-print"',
        'id="export-png-desktop"',
        'id="export-png-mobile"',
        'id="export-im-share"',
        'id="report-summary"',
        "title-block-header",
        '<p class="date">',
        "duplicate date",
        "version/theme metadata",
        "html-shell/export.md",
    ]:
        assert marker in entry


def test_rendering_entry_only_fallback_keeps_directive_and_selection_red_lines():
    entry = read_reference("references/rendering-rules.md")
    for marker in [
        "Never Let `:::` Leak Into Output",
        "Block Detection Rules",
        "`invalid_syntax`",
        "`invalid_semantics`",
        "`auto_downgrade_target`",
        "references/rendering/kpi.md",
        "references/rendering/chart.md",
        "references/rendering/timeline-diagram.md",
        "narrative reports should not force KPI blocks",
        "charts must never be decorative",
    ]:
        assert marker in entry


def test_aggregated_shell_reference_preserves_complete_export_and_metadata_contracts():
    shell = shell_reference_text()
    for marker in [
        "const printBtn   = document.getElementById('export-print');",
        "const pngDesktop = document.getElementById('export-png-desktop');",
        "const pngMobile  = document.getElementById('export-png-mobile');",
        "const pngIM      = document.getElementById('export-im-share');",
        '<meta name="ir-hash" content="sha256:[ir-hash]">',
        '<div class="report-footer">kai-report-creator v[version] [theme]</div>',
        'data-watermark="kai-report-creator v[version] [theme]"',
    ]:
        assert marker in shell


def test_aggregated_rendering_reference_preserves_component_contracts():
    rendering = rendering_reference_text()
    for marker in [
        "Use **ECharts** for ALL charts",
        "Default mode: do not add `data-accent` to KPI cards.",
        "Whitelist for `Date`",
        "Chart.js is NOT used in the standard template.",
        "Badges are optional visual enhancements, not a first-class IR tag.",
        "`highlight-sentence` is a prose pattern, not an IR tag.",
    ]:
        assert marker in rendering


def test_required_refs_route_to_shell_children_and_component_children():
    refs = resolve_required_refs(
        "corporate-blue",
        {"kpi": 1, "chart": 1, "table": 1, "timeline": 1, "diagram": 1, "callout": 1},
    )

    for path in [
        "references/html-shell-template.md",
        "references/html-shell/export.md",
        "references/html-shell/core-structure.md",
        "references/html-shell/summary-card.md",
        "references/rendering-rules.md",
        "references/rendering/kpi.md",
        "references/rendering/chart.md",
        "references/rendering/table-list.md",
        "references/rendering/timeline-diagram.md",
        "references/rendering/media-code-callout.md",
        "references/diagram-decision-rules.md",
    ]:
        assert path in refs


def test_required_refs_for_narrative_timeline_do_not_load_chart_or_kpi_details():
    refs = resolve_required_refs("minimal", {"timeline": 1, "callout": 1})

    assert "references/rendering/timeline-diagram.md" in refs
    assert "references/rendering/media-code-callout.md" in refs
    assert "references/rendering/chart.md" not in refs
    assert "references/rendering/kpi.md" not in refs
