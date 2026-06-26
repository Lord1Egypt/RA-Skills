"""Pack builder — assemble the final repro pack output."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

from ..models import EnvironmentFacts, RedactionReport, TimelineEvent
from ..parser.stack_trace import StackTrace


@dataclass
class PackResult:
    """Result of the pack building process."""
    output_dir: str
    files_created: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    validation: dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "output_dir": self.output_dir,
            "files_created": self.files_created,
            "warnings": self.warnings,
            "validation": self.validation,
        }


class PackBuilder:
    """Assembles all outputs into a structured repro pack directory."""

    def __init__(self, output_dir: str) -> None:
        self.output_dir = os.path.abspath(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        self._result = PackResult(output_dir=self.output_dir)

    def write_sanitized_ticket(self, content: str) -> None:
        self._write("1_sanitized_ticket.md", content)

    def write_sanitized_logs(self, content: str) -> None:
        self._write("2_sanitized_logs.txt", content)

    def write_facts(self, facts: EnvironmentFacts) -> None:
        self._write("3_facts.json", json.dumps(facts.to_dict(), indent=2, ensure_ascii=False))

    def write_timeline(self, events: list[TimelineEvent]) -> None:
        data = [e.to_dict() for e in events]
        self._write("4_timeline.json", json.dumps(data, indent=2, ensure_ascii=False))

    def write_engineering_issue(self, content: str) -> None:
        self._write("5_engineering_issue.md", content)

    def write_internal_escalation(self, content: str) -> None:
        self._write("6_internal_escalation.md", content)

    def write_customer_reply(self, content: str) -> None:
        self._write("7_customer_reply.md", content)

    def write_redaction_report(self, report: RedactionReport) -> None:
        self._write(
            "8_redaction_report.json",
            json.dumps(report.to_dict(), indent=2, ensure_ascii=False),
        )

    def write_stack_traces(self, traces: list[StackTrace]) -> None:
        if not traces:
            return
        data = []
        for t in traces:
            data.append({
                "language": t.language,
                "exception_type": t.exception_type,
                "exception_message": t.exception_message,
                "frames": [
                    {
                        "file": f.file_path,
                        "line": f.line_number,
                        "function": f.function_name,
                    }
                    for f in t.frames
                ],
            })
        self._write("9_stack_traces.json", json.dumps(data, indent=2, ensure_ascii=False))

    def validate(self) -> dict[str, bool]:
        """Check which expected output files were created."""
        expected = [
            "1_sanitized_ticket.md",
            "2_sanitized_logs.txt",
            "3_facts.json",
            "4_timeline.json",
            "5_engineering_issue.md",
            "6_internal_escalation.md",
            "7_customer_reply.md",
            "8_redaction_report.json",
        ]
        self._result.validation = {
            f: os.path.exists(os.path.join(self.output_dir, f))
            for f in expected
        }
        return self._result.validation

    def finalize(self) -> PackResult:
        """Validate and return the build result."""
        self.validate()

        missing = [k for k, v in self._result.validation.items() if not v]
        if missing:
            self._result.warnings.append(f"Missing files: {', '.join(missing)}")

        # Write validation report
        self._write(
            "validation_report.json",
            json.dumps(self._result.to_dict(), indent=2, ensure_ascii=False),
        )
        return self._result

    def _write(self, filename: str, content: str) -> None:
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        self._result.files_created.append(filename)
