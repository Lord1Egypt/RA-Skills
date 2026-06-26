"""Unified production CLI for psd-batch-export v4.4."""

from __future__ import annotations

import argparse
import contextlib
import json
import sys
from typing import Callable

from console_utils import configure_stdio

configure_stdio()

from psd_core import (  # noqa: E402
    EXIT_DEPENDENCY_ERROR,
    EXIT_INPUT_ERROR,
    EXIT_SUCCESS,
    EXIT_UNEXPECTED_ERROR,
    EXIT_VERIFY_ERROR,
    PsdBatchError,
    analyze,
    diagnose,
    export_batch,
    preview,
    templates_payload,
    verify_output,
    write_json,
)


def parse_color(values: list[int] | None) -> tuple[int, int, int] | None:
    if not values:
        return None
    return tuple(values)  # type: ignore[return-value]


def emit(payload: dict, *, json_stdout: bool = False, json_out: str | None = None) -> None:
    write_json(json_out, payload)
    if json_stdout:
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    else:
        print(f"status: {payload.get('status')}")
        if payload.get("warnings"):
            print("warnings:")
            for warning in payload["warnings"]:
                print(f"  - {warning}")
        if payload.get("errors"):
            print("errors:")
            for error in payload["errors"]:
                print(f"  - {error}")
        outputs = payload.get("outputs") or {}
        if outputs:
            print("outputs:")
            for key, value in outputs.items():
                print(f"  {key}: {value}")


def exit_code_for(payload: dict) -> int:
    if payload.get("status") == "ok":
        return EXIT_SUCCESS
    if payload.get("verify"):
        return EXIT_VERIFY_ERROR
    if payload.get("dependencies", {}).get("required"):
        missing = [k for k, ok in payload["dependencies"]["required"].items() if not ok]
        if missing:
            return EXIT_DEPENDENCY_ERROR
    return EXIT_INPUT_ERROR


def run_action(args: argparse.Namespace, action: Callable[[], dict]) -> int:
    try:
        if getattr(args, "json", False):
            with contextlib.redirect_stdout(sys.stderr):
                payload = action()
        else:
            payload = action()
        emit(payload, json_stdout=getattr(args, "json", False), json_out=getattr(args, "json_out", None))
        return exit_code_for(payload)
    except PsdBatchError as exc:
        payload = {
            "status": "error",
            "inputs": {},
            "layers": [],
            "mapping": [],
            "capacity_risks": [],
            "fonts": {},
            "outputs": {},
            "warnings": [],
            "errors": exc.errors,
            "runtime_sec": 0.0,
        }
        emit(payload, json_stdout=getattr(args, "json", False), json_out=getattr(args, "json_out", None))
        return exc.exit_code
    except KeyboardInterrupt:
        return EXIT_UNEXPECTED_ERROR
    except Exception as exc:
        payload = {
            "status": "error",
            "inputs": {},
            "layers": [],
            "mapping": [],
            "capacity_risks": [],
            "fonts": {},
            "outputs": {},
            "warnings": [],
            "errors": [f"{type(exc).__name__}: {exc}"],
            "runtime_sec": 0.0,
        }
        emit(payload, json_stdout=getattr(args, "json", False), json_out=getattr(args, "json_out", None))
        return EXIT_UNEXPECTED_ERROR


def add_common_json_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="Write structured JSON to stdout")
    parser.add_argument("--json-out", help="Write structured JSON report to this path")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PSD Batch Export v4.4 unified CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    diagnose_p = sub.add_parser("diagnose", help="Check dependencies, fonts, templates, and optional features")
    add_common_json_flags(diagnose_p)
    diagnose_p.set_defaults(func=lambda a: run_action(a, diagnose))

    analyze_p = sub.add_parser("analyze", help="Analyze PSD layers and optional data mapping")
    analyze_p.add_argument("psd", help="PSD path or built-in template id")
    analyze_p.add_argument("--data", help="Excel/CSV/TSV data source")
    analyze_p.add_argument("--sheet", default=0, help="Excel sheet name or index")
    analyze_p.add_argument("--font", help="Manual font path for matching")
    add_common_json_flags(analyze_p)
    analyze_p.set_defaults(func=lambda a: run_action(a, lambda: analyze(a.psd, a.data, sheet=a.sheet, font=a.font)))

    preview_p = sub.add_parser("preview", help="Render preview PNG files without exporting the full batch")
    preview_p.add_argument("psd", help="PSD path or built-in template id")
    preview_p.add_argument("--data", required=True, help="Excel/CSV/TSV data source")
    preview_p.add_argument("--out", required=True, help="Output directory")
    preview_p.add_argument("--rows", type=int, default=3, help="Number of preview rows")
    preview_p.add_argument("--sheet", default=0, help="Excel sheet name or index")
    preview_p.add_argument("--font", help="Manual font path")
    preview_p.add_argument("--color", nargs=3, type=int, metavar=("R", "G", "B"), help="Text color RGB override (default: keep PSD layer colors)")
    preview_p.add_argument("--size", type=int, help="Font size override")
    preview_p.add_argument("--align", choices=["left", "center", "right"], default="center")
    preview_p.add_argument("--dpi", type=int, default=300)
    preview_p.add_argument("--strict", action="store_true", help="Fail on low-confidence mapping, capacity, or font risks")
    add_common_json_flags(preview_p)
    preview_p.set_defaults(
        func=lambda a: run_action(
            a,
            lambda: preview(
                a.psd,
                a.data,
                a.out,
                rows=a.rows,
                sheet=a.sheet,
                font=a.font,
                color=parse_color(a.color),
                font_size=a.size,
                align=a.align,
                dpi=a.dpi,
                strict=a.strict,
            ),
        )
    )

    export_p = sub.add_parser("export", help="Export batch PSD and PNG files")
    export_p.add_argument("psd", help="PSD path or built-in template id")
    export_p.add_argument("--data", required=True, help="Excel/CSV/TSV data source")
    export_p.add_argument("--out", required=True, help="Output directory")
    export_p.add_argument("--sheet", default=0, help="Excel sheet name or index")
    export_p.add_argument("--font", help="Manual font path")
    export_p.add_argument("--color", nargs=3, type=int, metavar=("R", "G", "B"), help="Text color RGB override (default: keep PSD layer colors)")
    export_p.add_argument("--size", type=int, help="Font size override")
    export_p.add_argument("--align", choices=["left", "center", "right"], default="center")
    export_p.add_argument("--dpi", type=int, default=300)
    export_p.add_argument("--cols", help="Manual comma-separated column mapping")
    export_p.add_argument("--verify-samples", type=int, default=3)
    export_p.add_argument("--ocr", action="store_true")
    export_p.add_argument("--ocr-lang")
    export_p.add_argument("--tesseract-cmd")
    export_p.add_argument("--tessdata-dir")
    export_p.add_argument("--strict", action="store_true", help="Fail before export on mapping, capacity, or font risks")
    add_common_json_flags(export_p)
    export_p.set_defaults(
        func=lambda a: run_action(
            a,
            lambda: export_batch(
                a.psd,
                a.data,
                a.out,
                sheet=a.sheet,
                font=a.font,
                color=parse_color(a.color),
                font_size=a.size,
                align=a.align,
                dpi=a.dpi,
                cols=a.cols,
                verify_samples=a.verify_samples,
                ocr=a.ocr,
                ocr_lang=a.ocr_lang,
                tesseract_cmd=a.tesseract_cmd,
                tessdata_dir=a.tessdata_dir,
                strict=a.strict,
            ),
        )
    )

    verify_p = sub.add_parser("verify", help="Verify an existing batch output directory")
    verify_p.add_argument("out", help="Output directory containing psd/ and png/")
    verify_p.add_argument("--samples", type=int, default=3)
    verify_p.add_argument("--dpi", type=int, default=300)
    verify_p.add_argument("--color", nargs=3, type=int, metavar=("R", "G", "B"), help="Text color RGB override used for re-render comparison (default: keep PSD layer colors)")
    verify_p.add_argument("--ocr", action="store_true")
    verify_p.add_argument("--ocr-lang")
    verify_p.add_argument("--tesseract-cmd")
    verify_p.add_argument("--tessdata-dir")
    add_common_json_flags(verify_p)
    verify_p.set_defaults(
        func=lambda a: run_action(
            a,
            lambda: verify_output(
                a.out,
                samples=a.samples,
                dpi=a.dpi,
                color=parse_color(a.color),
                ocr=a.ocr,
                ocr_lang=a.ocr_lang,
                tesseract_cmd=a.tesseract_cmd,
                tessdata_dir=a.tessdata_dir,
            ),
        )
    )

    templates_p = sub.add_parser("templates", help="List or inspect built-in templates")
    templates_sub = templates_p.add_subparsers(dest="templates_command", required=True)
    templates_list = templates_sub.add_parser("list", help="List templates")
    add_common_json_flags(templates_list)
    templates_list.set_defaults(func=lambda a: run_action(a, lambda: templates_payload()))
    templates_info = templates_sub.add_parser("info", help="Inspect one template")
    templates_info.add_argument("slug")
    add_common_json_flags(templates_info)
    templates_info.set_defaults(func=lambda a: run_action(a, lambda: templates_payload(a.slug)))

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
