from pathlib import Path

from evals.contract_checks import (
    extract_block,
    validate_chart,
    validate_diagram,
    validate_kpi,
    validate_timeline,
)


ROOT = Path(__file__).resolve().parent.parent


def test_kpi_canonical_yaml_is_valid():
    body = """
items:
  - label: 总营收
    value: ¥2,450万
    delta: ↑12%
    note: 同比
""".strip()
    assert validate_kpi(body) == {"status": "valid"}


def test_kpi_short_line_is_accepted_for_compatibility():
    body = "- Revenue: $2.45M ↑12%"
    assert validate_kpi(body) == {"status": "valid"}


def test_kpi_sentence_value_is_invalid_semantics():
    body = """
items:
  - label: 能力说明
    value: 支持CSV与Excel等表格文件的统计汇总与趋势分析
""".strip()
    assert validate_kpi(body) == {
        "status": "invalid_semantics",
        "auto_downgrade_target": "callout",
    }


def test_kpi_placeholder_value_is_invalid_for_any_report_class():
    body = """
items:
  - label: Metric A
    value: [INSERT VALUE]
""".strip()
    assert validate_kpi(body, report_class="data") == {
        "status": "invalid_semantics",
        "auto_downgrade_target": "callout",
    }


def test_kpi_value_must_be_quantitative():
    body = """
items:
  - label: Status
    value: 通过
""".strip()
    assert validate_kpi(body, report_class="data") == {
        "status": "invalid_semantics",
        "auto_downgrade_target": "callout",
    }


def test_timeline_requires_whitelisted_dates():
    good = "- 2024-10-15: Launch\n- Q4 2024: Expansion"
    bad = "- 核心原则: 真诚服务\n- 核心能力: 专业高效"
    assert validate_timeline(good) == {"status": "valid"}
    assert validate_timeline(bad) == {
        "status": "invalid_semantics",
        "auto_downgrade_target": "list",
    }


def test_timeline_missing_date_separator_is_invalid_syntax():
    body = "- 2024-10-15 Launch"
    assert validate_timeline(body) == {
        "status": "invalid_syntax",
        "auto_downgrade_target": "list",
    }


def test_chart_requires_schema_for_each_type():
    standard = """
labels: [Jul, Aug, Sep]
datasets:
  - label: Actual
    data: [1, 2, 3]
""".strip()
    sankey = """
nodes: [A, B]
links: [A->B:120]
""".strip()
    broken = "datasets:\n  - label: Actual"

    assert validate_chart("line", standard) == {"status": "valid"}
    assert validate_chart("sankey", sankey) == {"status": "valid"}
    assert validate_chart("line", broken) == {
        "status": "invalid_syntax",
        "auto_downgrade_target": "table",
    }


def test_chart_placeholder_only_block_in_narrative_is_invalid_semantics():
    body = """
labels: [A, B]
datasets:
  - label: Placeholder
    data: [[INSERT VALUE], [INSERT VALUE]]
""".strip()
    assert validate_chart("bar", body, report_class="narrative") == {
        "status": "invalid_semantics",
        "auto_downgrade_target": "table",
    }


def test_diagram_requires_type_specific_schema():
    sequence = """
actors: [用户, Claude]
steps:
  - from: 用户
    to: Claude
    msg: 请求
""".strip()
    flowchart_broken = """
nodes:
  - id: start
    kind: oval
    label: 开始
""".strip()

    assert validate_diagram("sequence", sequence) == {"status": "valid"}
    assert validate_diagram("flowchart", flowchart_broken) == {
        "status": "invalid_syntax",
        "auto_downgrade_target": "callout",
    }


def test_examples_follow_the_documented_contract():
    business = (ROOT / "examples" / "business-report.report.md").read_text(encoding="utf-8")
    tech = (ROOT / "examples" / "tech-doc.report.md").read_text(encoding="utf-8")
    guide = (ROOT / "examples" / "zh" / "kai-report-creator-guide.report.md").read_text(encoding="utf-8")

    _, business_kpi = extract_block(business, "kpi")
    assert validate_kpi(business_kpi) == {"status": "valid"}

    line_header, business_chart = extract_block(business, "chart")
    assert "type=line" in line_header
    assert validate_chart("line", business_chart) == {"status": "valid"}

    _, business_timeline = extract_block(business, "timeline")
    assert validate_timeline(business_timeline) == {"status": "valid"}

    diagram_header, tech_diagram = extract_block(tech, "diagram")
    assert "type=sequence" in diagram_header
    assert validate_diagram("sequence", tech_diagram) == {"status": "valid"}

    guide_kpi_header, guide_kpi = extract_block(guide, "kpi")
    assert guide_kpi_header.startswith(":::kpi")
    assert validate_kpi(guide_kpi) == {"status": "valid"}

    _, guide_timeline = extract_block(guide, "timeline")
    assert validate_timeline(guide_timeline) == {"status": "valid"}
