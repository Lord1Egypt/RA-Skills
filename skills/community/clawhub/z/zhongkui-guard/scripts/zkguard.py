#!/usr/bin/env python3
"""Local-first command line entrypoint for Zhongkui Guard."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from zhongkui.audit import audit
from zhongkui.doctor import doctor
from zhongkui.redact import redact
from zhongkui.report import write_report
from zhongkui.scan import scan


def emit(value: dict, fmt: str) -> None:
    if fmt == "json":
        print(json.dumps(value, ensure_ascii=False, sort_keys=True))
    else:
        print(value.get("summary", value.get("status", "completed")))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="zkguard", description="Zhongkui Guard local security checks")
    sub = p.add_subparsers(dest="operation", required=True)
    d = sub.add_parser("doctor")
    d.add_argument("--format", choices=("json", "text"), default="text")
    s = sub.add_parser("scan")
    s.add_argument("--path", required=True)
    s.add_argument("--kind", choices=("skill", "response", "tool-log"), required=True)
    s.add_argument("--fail-on", choices=("low", "medium", "high"))
    s.add_argument("--format", choices=("json", "text"), default="text")
    r = sub.add_parser("redact")
    r.add_argument("--input", required=True)
    r.add_argument("--output", required=True)
    r.add_argument("--sensitive-word", action="append", default=[])
    r.add_argument("--format", choices=("json", "text"), default="text")
    a = sub.add_parser("audit")
    a.add_argument("--target", required=True)
    a.add_argument("--reference")
    a.add_argument("--profile", choices=("quick",), default="quick")
    a.add_argument("--config", required=True)
    a.add_argument("--plan", action="store_true")
    a.add_argument("--max-requests", type=int)
    a.add_argument("--max-output-tokens", type=int)
    a.add_argument("--format", choices=("json", "text"), default="text")
    rep = sub.add_parser("report")
    rep.add_argument("--input", required=True)
    rep.add_argument("--output", required=True)
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        if args.operation == "doctor": result = doctor(ROOT)
        elif args.operation == "scan": result = scan(Path(args.path), args.kind)
        elif args.operation == "redact": result = redact(Path(args.input), Path(args.output), args.sensitive_word)
        elif args.operation == "audit": result = audit(args)
        else:
            source = json.loads(Path(args.input).read_text(encoding="utf-8"))
            write_report(source, Path(args.output)); result = {"schema_version":"1.0", "operation":"report", "status":"completed", "output":str(Path(args.output).resolve()), "summary":"报告已生成"}
        emit(result, getattr(args, "format", "json"))
        if args.operation == "scan" and args.fail_on:
            order = {"low": 1, "medium": 2, "high": 3}
            if any(order[f["severity"]] >= order[args.fail_on] for f in result["findings"]): return 4
        return 0
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"zkguard: {str(exc)[:300]}", file=sys.stderr); return 2
    except OSError as exc:
        print(f"zkguard: operation incomplete: {str(exc)[:300]}", file=sys.stderr); return 3


if __name__ == "__main__":
    raise SystemExit(main())

