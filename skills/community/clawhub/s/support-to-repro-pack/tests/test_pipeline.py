"""Integration test for the full pipeline."""

import json
import os
import tempfile

from repro_pack.pipeline import run_pipeline


class TestPipeline:
    def _get_example_path(self, case: str, filename: str) -> str:
        return os.path.join(
            os.path.dirname(__file__), "..", "examples", case, filename
        )

    def test_easy_case(self):
        ticket = self._get_example_path("case_easy", "input_ticket.md")
        logs = self._get_example_path("case_easy", "input_logs.txt")

        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_pipeline(
                ticket_path=ticket,
                log_paths=[logs],
                output_dir=tmpdir,
            )

            # All expected files should be created
            assert len(result.files_created) >= 9

            # Sanitized ticket should not contain raw PII
            with open(os.path.join(tmpdir, "1_sanitized_ticket.md")) as f:
                content = f.read()
            assert "zhang.wei@acmecorp.com" not in content
            assert "13812345678" not in content
            assert "david.chen@example.com" not in content
            assert "+1-415-555-0198" not in content

            # Facts should have key info
            with open(os.path.join(tmpdir, "3_facts.json")) as f:
                facts = json.load(f)
            assert facts.get("app_version") == "2.4.1"
            assert facts.get("browser") == "Chrome"

            # Redaction report should show findings
            with open(os.path.join(tmpdir, "8_redaction_report.json")) as f:
                report = json.load(f)
            assert report["total_pii_found"] > 0

    def test_medium_case(self):
        ticket = self._get_example_path("case_medium", "input_ticket.md")
        logs = self._get_example_path("case_medium", "input_logs.txt")

        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_pipeline(
                ticket_path=ticket,
                log_paths=[logs],
                output_dir=tmpdir,
            )

            # Sanitized ticket should redact Chinese PII
            with open(os.path.join(tmpdir, "1_sanitized_ticket.md")) as f:
                content = f.read()
            assert "13900139000" not in content
            assert "xiaoming.wang@bjtech.cn" not in content
            assert "110105199003071234" not in content
            assert "Admin@2024!" not in content

    def test_hard_case(self):
        ticket = self._get_example_path("case_hard", "input_ticket.md")
        logs = self._get_example_path("case_hard", "input_logs.txt")

        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_pipeline(
                ticket_path=ticket,
                log_paths=[logs],
                output_dir=tmpdir,
            )

            # Check PII redaction
            with open(os.path.join(tmpdir, "1_sanitized_ticket.md")) as f:
                content = f.read()
            assert "sarah@globalfinance.co.uk" not in content
            assert "sk_live_TESTKEY000000000demo" not in content
            assert "james.wilson@globalfinance.co.uk" not in content

            # Check facts extraction
            with open(os.path.join(tmpdir, "3_facts.json")) as f:
                facts = json.load(f)
            assert facts.get("region") == "eu-west-1"

    def test_no_inputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_pipeline(output_dir=tmpdir)
            assert len(result.files_created) > 0

    def test_nonexistent_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_pipeline(
                ticket_path="/nonexistent/ticket.md",
                log_paths=["/nonexistent/log.txt"],
                output_dir=tmpdir,
            )
            # Should not crash
            assert len(result.files_created) > 0
