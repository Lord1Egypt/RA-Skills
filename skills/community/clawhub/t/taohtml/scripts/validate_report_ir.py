#!/usr/bin/env python3
"""Validate and normalize a TaoHtml Report IR v1 project source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from report_ir_core import load_json, validate_ir, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_ir", type=Path)
    parser.add_argument(
        "--artifact-root",
        type=Path,
        help="Optional project root for checking project-relative source and asset hashes.",
    )
    parser.add_argument("--output", type=Path, help="Write the machine-readable validation report.")
    parser.add_argument(
        "--normalized-output",
        type=Path,
        help="Write normalized Report IR only when every validation layer passes.",
    )
    args = parser.parse_args()

    try:
        raw = load_json(args.report_ir)
        result = validate_ir(raw, args.artifact_root)
        if args.output is not None:
            public_result = {key: value for key, value in result.items() if key != "normalized_ir"}
            write_json(args.output, public_result)
        if args.normalized_output is not None and result["compiler_ready"]:
            write_json(args.normalized_output, result["normalized_ir"])
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"REPORT_IR_INVALID {exc}")
        return 1

    print(
        "REPORT_IR_VALIDATION "
        f"schema_valid={str(result['schema_valid']).lower()} "
        f"references_valid={str(result['references_valid']).lower()} "
        f"semantics_valid={str(result['semantics_valid']).lower()} "
        f"compiler_ready={str(result['compiler_ready']).lower()}"
    )
    for layer, issues in result["issues"].items():
        for issue in issues:
            print(f"ISSUE {layer}: {issue}")
    return 0 if result["compiler_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
