#!/usr/bin/env python3
"""Skill Vetter Plus v2.0 — Security scanner for AI agent skills.

Loads detection signatures from signatures.json and performs fast
line-by-line text matching. No regex compilation. No dynamic code.
"""

import argparse
import json
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Finding:
    severity: str
    rule_id: str
    file: str
    line: int
    message: str
    matched: str

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "rule_id": self.rule_id,
            "file": self.file,
            "line": self.line,
            "message": self.message,
            "matched_fragment": self.matched,
        }


@dataclass
class Report:
    findings: List[Finding] = field(default_factory=list)
    scanned_files: int = 0
    duration_ms: float = 0.0

    def to_dict(self) -> dict:
        return {
            "summary": {
                "scanned_files": self.scanned_files,
                "duration_ms": round(self.duration_ms, 2),
                "total_findings": len(self.findings),
            },
            "findings": [f.to_dict() for f in self.findings],
        }


def load_signatures(path: Path) -> List[Dict]:
    data = json.load(open(path))
    return data["signatures"]


def scan_file(path: Path, signatures: List[Dict]) -> List[Finding]:
    findings: List[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = text.splitlines()
    for lineno, line in enumerate(lines, start=1):
        line_lower = line.lower()
        for sig in signatures:
            for frag in sig["fragments"]:
                frag_lower = frag.lower()
                if frag in line or frag_lower in line_lower:
                    findings.append(
                        Finding(
                            severity=sig["severity"],
                            rule_id=sig["id"],
                            file=str(path),
                            line=lineno,
                            message=f"{sig['message']}",
                            matched=frag,
                        )
                    )
                    break  # One finding per signature per line
    return findings


def scan_skill(skill_dir: Path, signatures: List[Dict]) -> Report:
    start = time.monotonic()
    report = Report()

    for root, _, files in os.walk(skill_dir):
        for fname in files:
            path = Path(root) / fname
            report.scanned_files += 1
            findings = scan_file(path, signatures)
            report.findings.extend(findings)

    report.duration_ms = (time.monotonic() - start) * 1000
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Skill Vetter Plus — Security scanner for AI agent skills")
    parser.add_argument("path", type=Path, help="Skill directory to scan")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    parser.add_argument("--signatures", type=Path, default=None, help="Custom signatures.json path")
    args = parser.parse_args()

    sig_path = args.signatures or Path(__file__).parent.parent / "signatures.json"
    signatures = load_signatures(sig_path)

    report = scan_skill(args.path, signatures)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(f"Scanned {report.scanned_files} files in {report.duration_ms:.0f}ms")
        if report.findings:
            print(f"Found {len(report.findings)} issue(s):")
            for f in report.findings:
                print(f"  [{f.severity.upper()}] {f.rule_id} at {f.file}:{f.line}")
                print(f"    → {f.message} (matched: '{f.matched}')")
        else:
            print("No issues found.")
    return 0 if len(report.findings) == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
