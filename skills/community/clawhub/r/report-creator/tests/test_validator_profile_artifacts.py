from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_requirements_lock_exists_for_python_scripts():
    src = read("scripts/requirements.lock")
    assert "pytest==" in src
    assert "playwright==" in src
    assert "pytest-playwright==" in src
    package_lines = [line for line in src.splitlines() if "==" in line]
    assert package_lines
    assert all("--hash=sha256:" in line or line.endswith("\\") for line in package_lines)


def test_golden_cases_manifest_has_ten_real_cases():
    src = read("evals/golden_cases.yaml")
    assert "signoff:" in src
    assert "oa_ticket:" in src
    case_count = sum(1 for line in src.splitlines() if line.startswith("  - id: "))
    assert case_count >= 10
    for marker in [
        "zh-ai-collaboration",
        "en-ops-weekly",
        "zh-quarterly-growth",
        "guard-broken-chart-schema",
        "guard-narrative-placeholder-kpi",
        "duplicate-date-guard",
        "export-shell-complete",
        "skill-routing-budget",
    ]:
        assert marker in src


def test_references_index_routes_core_reference_files():
    src = read("references/INDEX.md")
    for marker in [
        "html-shell-template.md",
        "html-shell/export.md",
        "html-shell/summary-card.md",
        "theme-css.md",
        "rendering-rules.md",
        "rendering/chart.md",
        "rendering/kpi.md",
        "anti-patterns.md",
        "diagram-decision-rules.md",
        "regular-report-content-rules.md",
        "review-checklist.md",
        "spec-loading-matrix.md",
    ]:
        assert marker in src


def test_usage_boundary_examples_exist():
    when_to_use = read("examples/when-to-use.md")
    do_not_use = read("examples/do-not-use.md")
    assert "/report --plan" in when_to_use
    assert "/report --generate" in when_to_use
    assert "/report --review" in when_to_use
    assert "PPTX" in do_not_use
    assert "kai-html-export" in do_not_use
    assert "kai-slide-creator" in do_not_use


def test_verify_release_includes_generated_file_cleanup():
    src = read("scripts/verify-release.py")
    assert "clean-generated" in src
    assert "cleanup-generated" in src
