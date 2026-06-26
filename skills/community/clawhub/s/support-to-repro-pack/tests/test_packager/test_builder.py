"""Tests for pack builder."""

import json
import os
import tempfile

from repro_pack.models import EnvironmentFacts, RedactionReport, TimelineEvent
from repro_pack.packager.builder import PackBuilder


class TestPackBuilder:
    def test_creates_output_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            outdir = os.path.join(tmpdir, "output")
            builder = PackBuilder(outdir)
            assert os.path.isdir(outdir)

    def test_writes_all_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = PackBuilder(tmpdir)
            builder.write_sanitized_ticket("# Test ticket")
            builder.write_sanitized_logs("test log line")
            builder.write_facts(EnvironmentFacts(app_version="1.0"))
            builder.write_timeline([TimelineEvent(timestamp="2024-01-01", event="test")])
            builder.write_engineering_issue("## Issue")
            builder.write_internal_escalation("## Escalation")
            builder.write_customer_reply("Dear customer")
            builder.write_redaction_report(RedactionReport(total_found=0))

            result = builder.finalize()
            assert len(result.files_created) == 9  # 8 + validation_report
            assert all(v for v in result.validation.values())
            assert result.warnings == []

    def test_validation_detects_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = PackBuilder(tmpdir)
            builder.write_sanitized_ticket("test")
            # Don't write other files

            result = builder.finalize()
            missing = [k for k, v in result.validation.items() if not v]
            assert len(missing) > 0
            assert len(result.warnings) > 0

    def test_facts_json_valid(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = PackBuilder(tmpdir)
            facts = EnvironmentFacts(
                app_version="2.0",
                environment="staging",
                region="us-east-1",
            )
            builder.write_facts(facts)

            with open(os.path.join(tmpdir, "3_facts.json")) as f:
                data = json.load(f)
            assert data["app_version"] == "2.0"
            assert data["environment"] == "staging"

    def test_validation_report_is_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = PackBuilder(tmpdir)
            builder.write_sanitized_ticket("test")
            builder.finalize()

            with open(os.path.join(tmpdir, "validation_report.json")) as f:
                data = json.load(f)
            assert "files_created" in data
            assert "validation" in data
