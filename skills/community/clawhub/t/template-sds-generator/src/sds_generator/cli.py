from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import ValidationError

from sds_generator.exceptions import InvalidInputBundleError
from sds_generator.models import GenerationMode, RunInputBundle
from sds_generator.pipeline import generate_sds_package


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a reconciled SDS package.")
    parser.add_argument(
        "--template-docx",
        type=Path,
        help="Client layout template (.docx). Required for the primary role-aware input path.",
    )
    parser.add_argument(
        "--prompt-file",
        type=Path,
        help="Prompt/rule file (.txt or .md). Required for the primary role-aware input path.",
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        type=Path,
        help="1-3 source SDS/MSDS evidence files (.pdf, .docx, .txt).",
    )
    parser.add_argument(
        "--inputs",
        nargs="+",
        type=Path,
        help="Legacy compatibility path for source SDS/MSDS files only.",
    )
    parser.add_argument("--outdir", type=Path, required=False, help="Output directory.")
    parser.add_argument("--mode", choices=["draft", "release"], default="draft")
    parser.add_argument(
        "--enable-ocr",
        action="store_true",
        help="Attempt OCR for scanned PDFs. Disabled by default; fails clearly if no OCR backend is configured.",
    )
    parser.add_argument("--allow-estimated-physchem", action="store_true")
    parser.add_argument("--product-name")
    parser.add_argument("--cas")
    parser.add_argument("--issue-date", help="Override Section 16 issue date (YYYY-MM-DD or client-approved display text).")
    parser.add_argument("--revision-date", help="Override Section 16 revision date (YYYY-MM-DD or client-approved display text).")
    parser.add_argument("--version", help="Override Section 16 version number.")
    return parser


def _format_validation_error(exc: ValidationError) -> str:
    messages = []
    for error in exc.errors():
        location = ".".join(str(item) for item in error.get("loc", ()) if item != "__root__")
        prefix = f"{location}: " if location else ""
        messages.append(f"{prefix}{error.get('msg', 'Invalid input')}")
    return "; ".join(messages) or str(exc)


def _resolve_cli_inputs(args: argparse.Namespace, parser: argparse.ArgumentParser) -> tuple[list[Path] | None, RunInputBundle | None]:
    role_mode_requested = any(value is not None for value in (args.template_docx, args.prompt_file, args.sources))
    legacy_mode_requested = bool(args.inputs)

    if role_mode_requested and legacy_mode_requested:
        parser.error("Use either legacy --inputs or the role-aware --template-docx/--prompt-file/--sources path, not both.")

    if role_mode_requested:
        try:
            input_bundle = RunInputBundle(
                template_docx=args.template_docx,
                prompt_file=args.prompt_file,
                source_sds=args.sources or [],
            )
        except InvalidInputBundleError as exc:
            parser.error(str(exc))
        except ValidationError as exc:
            parser.error(_format_validation_error(exc))
        return None, input_bundle

    if legacy_mode_requested:
        return list(args.inputs), None

    parser.error("Provide either legacy --inputs or the role-aware --template-docx, --prompt-file, and --sources arguments.")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    inputs, input_bundle = _resolve_cli_inputs(args, parser)
    _final_document, artifacts = generate_sds_package(
        inputs,
        input_bundle=input_bundle,
        outdir=args.outdir,
        mode=GenerationMode(args.mode),
        enable_ocr=args.enable_ocr,
        allow_estimated_physchem=args.allow_estimated_physchem,
        product_name=args.product_name,
        cas=args.cas,
        issue_date=args.issue_date,
        revision_date=args.revision_date,
        version=args.version,
    )
    print(artifacts.docx_path)
    if artifacts.pdf_path is not None:
        print(artifacts.pdf_path)
    print(artifacts.structured_json_path)
    print(artifacts.field_source_map_csv_path)
    print(artifacts.review_checklist_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
