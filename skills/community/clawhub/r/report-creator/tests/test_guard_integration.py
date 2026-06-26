"""
Guard Integration Contract Tests — v4 guardrails regression suite.

Root cause (v3 findings):
  Guard introduced new report_class default (drift from contract_checks.py)
  Guard assumed file-backed IR (broke context-backed path)
  Guard cloned validator logic (drift risk)

These tests verify:
  - Guard resolves report_class using existing --generate path (no new default)
  - Guard accepts ir_text: str (not file path)
  - Guard calls contract_checks validators (no cloning)
  - KPI placeholder policy stays centralized in contract_checks
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = ROOT / "scripts"
FIXTURES_DIR = Path(__file__).parent / "fixtures"

# Import guard function directly for testing
sys.path.insert(0, str(ROOT))
from scripts.guard_validate import validate_ir_text, resolve_report_class


# ── Test Fixtures ───────────────────────────────────────────────────────────────

PLACEHOLDER_KPI_IR = """---
title: Test Report
report_class: narrative
---

## Test Section

:::kpi
items:
  - label: Metric A
    value: [INSERT VALUE]
  - label: Metric B
    value: [数据待填写]
:::
"""

PLACEHOLDER_KPI_IR_DATA = """---
title: Test Report
report_class: data
---

## Test Section

:::kpi
items:
  - label: Metric A
    value: [INSERT VALUE]
  - label: Metric B
    value: [数据待填写]
:::
"""

EXPLICIT_DATA_IR = """---
title: Test Report
report_class: data
---

## Test Section

:::kpi
items:
  - label: Revenue
    value: ¥2,450万
    delta: ↑12%
:::
"""

NO_TITLE_IR = """---
report_class: mixed
---

## Test Section

Some content without title.
"""


# ── Acceptance Tests ───────────────────────────────────────────────────────────

class TestReportClassResolution:
    """Guard must resolve report_class using existing path (验收清单 #3, #4)."""

    def test_mixed_vs_data_classification(self):
        """placeholder-only KPI must fail for every report_class (验收清单 #7)."""
        # Narrative + placeholder KPI → invalid_semantics (should downgrade)
        report_narrative = validate_ir_text(PLACEHOLDER_KPI_IR)
        assert report_narrative["status"] == "invalid_blocks", (
            "placeholder-only KPI in narrative should be invalid"
        )
        assert report_narrative["resolved_report_class"] == "narrative"

        # Data + placeholder KPI → invalid_semantics (KPI cards require real metrics)
        report_data = validate_ir_text(PLACEHOLDER_KPI_IR_DATA)
        assert report_data["status"] == "invalid_blocks", (
            "placeholder-only KPI in data should be invalid"
        )
        assert report_data["resolved_report_class"] == "data"

    def test_explicit_report_class_data(self):
        """explicit report_class: data must NOT be remapped to mixed (验收清单 #8)."""
        report = validate_ir_text(EXPLICIT_DATA_IR)
        assert report["resolved_report_class"] == "data", (
            "explicit report_class: data must stay data, not remap to mixed"
        )
        assert report["status"] == "valid"


class TestIRFromContextVsFile:
    """Guard must accept ir_text from both file and context (验收清单 #5, #6, #9)."""

    def test_ir_from_context(self):
        """Context-backed IR must be validated via ir_text (验收清单 #9)."""
        # Pass ir_text directly (no file read)
        report = validate_ir_text(EXPLICIT_DATA_IR)
        assert report["status"] == "valid"
        assert report["resolved_report_class"] == "data"

    def test_ir_from_file_adapter(self):
        """File-backed IR must be read by adapter, not by guard (验收清单 #9)."""
        # Create temp IR file
        temp_ir = FIXTURES_DIR / "temp_test.report.md"
        temp_ir.write_text(EXPLICIT_DATA_IR, encoding="utf-8")

        # Call guard CLI (adapter reads file, passes ir_text to guard)
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "guard_validate.py"), str(temp_ir)],
            capture_output=True,
            text=True
        )

        # Parse JSON output
        report = json.loads(result.stdout)
        assert report["status"] == "valid"
        assert report["resolved_report_class"] == "data"

        # Clean up
        temp_ir.unlink()


class TestValidatorReuse:
    """Guard must call contract_checks validators, not clone logic (验收清单 #10)."""

    def test_guard_calls_validate_block(self):
        """Guard must import and call validate_block from contract_checks."""
        # This test verifies the guard script imports validate_block
        guard_script = SCRIPTS_DIR / "guard_validate.py"
        guard_source = guard_script.read_text(encoding="utf-8")

        # Check import
        assert "from evals.contract_checks import" in guard_source, (
            "Guard must import from contract_checks, not reimplement validators"
        )
        assert "validate_block" in guard_source, (
            "Guard must import validate_block function"
        )

        # Check usage (explicit pass report_class=resolved_class)
        assert "validate_block(block, report_class=resolved_class)" in guard_source, (
            "Guard must call validate_block with explicit report_class (no drift)"
        )

    def test_guard_no_placeholder_detection_clone(self):
        """Guard must NOT clone PLACEHOLDER_RE detection logic."""
        guard_script = SCRIPTS_DIR / "guard_validate.py"
        guard_source = guard_script.read_text(encoding="utf-8")

        # Guard can import PLACEHOLDER_RE for density detection, but must not reimplement
        # The key is: placeholder detection in validate_block (contract_checks), not in guard
        assert "PLACEHOLDER_RE" not in guard_source or "import PLACEHOLDER_RE" in guard_source, (
            "Guard must not clone PLACEHOLDER_RE detection — rely on validate_block"
        )


class TestFatalContract:
    """Guard must enforce fatal contracts (验收清单 #14)."""

    def test_missing_title_fatal(self):
        """Missing title must be fatal (exit code 2)."""
        report = validate_ir_text(NO_TITLE_IR)
        assert report["status"] == "fatal"
        assert report["exit_code"] == 2
        assert "title is required" in report["error"]
