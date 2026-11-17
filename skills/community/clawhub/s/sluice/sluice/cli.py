"""Command-line interface.

    sluice scan  [files...]        # report findings to stderr; exit non-zero if any breach
    sluice redact [files...]       # write cleaned text to stdout

With no files, reads stdin. Designed to sit in a pipe or a pre-send hook:

    draft.md | sluice scan && send-it      # only sends if clean
    sluice redact draft.md > safe.md
"""
from __future__ import annotations

import argparse
import json
import sys

from .core import scan, redact, worst_severity, _SEVERITY_RANK


def _read_inputs(paths: list[str]) -> str:
    if not paths:
        return sys.stdin.read()
    chunks = []
    for p in paths:
        with open(p, "r", encoding="utf-8", errors="replace") as fh:
            chunks.append(fh.read())
    return "\n".join(chunks)


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sluice", description="Outbound egress guard.")
    p.add_argument("mode", choices=["scan", "redact"], help="scan or redact")
    p.add_argument("files", nargs="*", help="files to read (default: stdin)")
    p.add_argument("--json", action="store_true", help="machine-readable findings")
    p.add_argument(
        "--allow", action="append", default=[], metavar="REGEX",
        help="suppress findings whose secret matches REGEX (repeatable)",
    )
    p.add_argument(
        "--min-severity", choices=["low", "medium", "high"], default="low",
        help="ignore findings below this severity",
    )
    p.add_argument(
        "--fail-on", choices=["low", "medium", "high", "never"], default="high",
        help="exit non-zero when a finding at/above this severity is seen (scan mode)",
    )
    p.add_argument(
        "--template", default="[redacted:{label}]",
        help="redaction placeholder; use {label} for the detector label",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    text = _read_inputs(args.files)

    if args.mode == "redact":
        sys.stdout.write(
            redact(
                text, allow=args.allow,
                min_severity=args.min_severity, template=args.template,
            )
        )
        return 0

    findings = scan(text, allow=args.allow, min_severity=args.min_severity)

    if args.json:
        sys.stderr.write(
            json.dumps(
                [
                    {
                        "detector": f.detector, "severity": f.severity,
                        "line": f.line, "preview": f.preview, "label": f.label,
                    }
                    for f in findings
                ],
                indent=2,
            ) + "\n"
        )
    else:
        if not findings:
            sys.stderr.write("sluice: clean — no secrets detected\n")
        else:
            sys.stderr.write(f"sluice: {len(findings)} finding(s)\n")
            for f in findings:
                sys.stderr.write(
                    f"  [{f.severity:>6}] line {f.line}: "
                    f"{f.detector} → {f.preview}\n"
                )

    if args.fail_on == "never":
        return 0
    worst = worst_severity(findings)
    if worst is not None and _SEVERITY_RANK[worst] >= _SEVERITY_RANK[args.fail_on]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
