from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

from .candidate_pipeline import (
    MODES,
    apply_docx_decisions,
    decide_with_ai,
    load_decisions,
    scan_docx_candidates,
    write_decisions_json,
    write_review_docx,
    write_scan_json,
)
from .document_converter import ConversionError, ensure_docx


ENGINES = ["auto", "word", "libreoffice"]


def build_parser() -> argparse.ArgumentParser:
    _load_dotenv()
    parser = argparse.ArgumentParser(
        description="Convert manually typed Word formulas to editable Word OMML equations."
    )
    subparsers = parser.add_subparsers(dest="command")

    convert = subparsers.add_parser("convert", help="Scan and apply formula conversion in one step")
    _add_input_args(convert)
    _add_conversion_args(convert)
    convert.add_argument("-o", "--output", type=Path, help="Output .docx path")
    convert.add_argument("--report", type=Path, help="Write a JSON conversion report")

    scan = subparsers.add_parser("scan", help="Extract candidate formulas without modifying the source")
    _add_input_args(scan)
    _add_conversion_args(scan)
    scan.add_argument("--out", type=Path, default=Path("artifacts/results/candidates.json"))
    scan.add_argument("--review-doc", type=Path, help="Write a Word review table of candidates")
    scan.add_argument("--placeholder-docx", type=Path, help="Write a non-final placeholder DOCX")

    apply = subparsers.add_parser("apply", help="Apply a reviewed decisions JSON to a Word file")
    _add_input_args(apply)
    _add_conversion_args(apply)
    apply.add_argument("--decisions", type=Path, required=True, help="Reviewed candidates JSON")
    apply.add_argument("-o", "--output", type=Path, required=True, help="Output .docx path")
    apply.add_argument("--report", type=Path, help="Write a JSON apply report")

    decide = subparsers.add_parser("decide", help="Create a decisions JSON from scan output")
    decide.add_argument("candidates", type=Path, help="Candidates JSON from scan")
    decide.add_argument("-o", "--output", type=Path, required=True)
    decide.add_argument("--provider", choices=["rule", "ai"], default="rule")
    decide.add_argument("--api-key", default=_env_first("OPENAI_API_KEY", "API_KEY"))
    decide.add_argument("--base-url", default=_env_first("OPENAI_BASE_URL", "BASE_URL", default="https://api.openai.com/v1"))
    decide.add_argument("--model", default=_env_first("OPENAI_MODEL", "MODEL", default="gpt-4.1-mini"))
    decide.add_argument(
        "--ai-timeout",
        type=int,
        default=60,
        help="Per-batch HTTP timeout for --provider ai (seconds).",
    )
    decide.add_argument(
        "--ai-batch-size",
        type=int,
        default=10,
        help="Candidates per AI request when using --provider ai.",
    )
    decide.add_argument(
        "--ai-max-workers",
        type=int,
        default=5,
        help="Max concurrent AI requests (cap for TPM/QPS limits).",
    )
    decide.add_argument(
        "--ai-retries",
        type=int,
        default=1,
        help="Retry count for transient AI HTTP/network errors.",
    )
    decide.add_argument(
        "--ai-failure-fallback",
        choices=["rule", "keep", "review"],
        default="rule",
        help="Decision strategy for an AI batch that still fails after retries.",
    )
    decide.add_argument(
        "--no-ai-progress",
        action="store_true",
        help="Suppress per-candidate progress logs when using --provider ai.",
    )

    return parser


def _add_input_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("input", type=Path, help="Source .doc, .docx, or .wps file")


def _add_conversion_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--engine",
        choices=ENGINES,
        default="auto",
        help="Conversion engine for .doc/.wps inputs. auto tries Word, then LibreOffice.",
    )
    parser.add_argument(
        "--mode",
        choices=sorted(MODES),
        default="balanced",
        help="Formula decision strictness.",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=Path("artifacts/work"),
        help="Directory for intermediate converted files.",
    )
    parser.add_argument(
        "--no-skip-bibliography",
        action="store_true",
        help="Also consider formula-like text in bibliography/reference sections.",
    )
    parser.add_argument(
        "--keep-intermediate",
        action="store_true",
        help="Keep intermediate DOCX files in --work-dir.",
    )


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] not in {"convert", "scan", "apply", "decide", "-h", "--help"}:
        argv.insert(0, "convert")
    args = build_parser().parse_args(argv)
    command = args.command
    if command is None:
        build_parser().print_help()
        return 2
    if command == "decide":
        return _cmd_decide(args)
    input_path = args.input.resolve()
    if not input_path.exists():
        print(f"Input file does not exist: {input_path}", file=sys.stderr)
        return 2
    if command == "scan":
        return _cmd_scan(args, input_path)
    if command == "apply":
        return _cmd_apply(args, input_path)
    return _cmd_convert(args, input_path)


def _prepare_docx(args: argparse.Namespace, input_path: Path) -> tuple[Path, str, Path]:
    work_dir = args.work_dir.resolve()
    scratch = work_dir if args.keep_intermediate else Path(tempfile.mkdtemp(prefix="latex-convert-"))
    docx_path, engine_used = ensure_docx(input_path, scratch, args.engine)
    return docx_path, engine_used, scratch


def _cmd_scan(args: argparse.Namespace, input_path: Path) -> int:
    scratch: Path | None = None
    try:
        docx_path, engine_used, scratch = _prepare_docx(args, input_path)
        scan = scan_docx_candidates(
            docx_path,
            input_path=input_path,
            engine=engine_used,
            mode=args.mode,
            skip_bibliography=not args.no_skip_bibliography,
        )
        write_scan_json(scan, args.out.resolve())
        if args.review_doc:
            write_review_docx(scan, args.review_doc.resolve())
        if args.placeholder_docx:
            decisions = {candidate.id: "placeholder" for candidate in scan.candidates}
            apply_docx_decisions(
                docx_path,
                args.placeholder_docx.resolve(),
                decisions,
                mode=args.mode,
                skip_bibliography=not args.no_skip_bibliography,
                placeholder=True,
            )
    except (ConversionError, RuntimeError, ValueError) as exc:
        print(f"Scan failed: {exc}", file=sys.stderr)
        return 1
    finally:
        _cleanup(args, scratch)
    print(json.dumps(scan.to_dict(), ensure_ascii=False, indent=2))
    return 0


def _cmd_apply(args: argparse.Namespace, input_path: Path) -> int:
    scratch: Path | None = None
    try:
        docx_path, engine_used, scratch = _prepare_docx(args, input_path)
        decisions = load_decisions(args.decisions.resolve())
        stats = apply_docx_decisions(
            docx_path,
            args.output.resolve(),
            decisions,
            mode=args.mode,
            skip_bibliography=not args.no_skip_bibliography,
        )
    except (ConversionError, ValueError) as exc:
        print(f"Apply failed: {exc}", file=sys.stderr)
        return 1
    finally:
        _cleanup(args, scratch)
    report = _apply_report(input_path, args.output.resolve(), engine_used, stats)
    if args.report:
        _write_json(args.report.resolve(), report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def _cmd_convert(args: argparse.Namespace, input_path: Path) -> int:
    scratch: Path | None = None
    output_path = (args.output or input_path.with_name(f"{input_path.stem}_converted.docx")).resolve()
    try:
        docx_path, engine_used, scratch = _prepare_docx(args, input_path)
        scan = scan_docx_candidates(
            docx_path,
            input_path=input_path,
            engine=engine_used,
            mode=args.mode,
            skip_bibliography=not args.no_skip_bibliography,
        )
        decisions = {candidate.id: candidate.default_action for candidate in scan.candidates}
        stats = apply_docx_decisions(
            docx_path,
            output_path,
            decisions,
            mode=args.mode,
            skip_bibliography=not args.no_skip_bibliography,
        )
    except (ConversionError, ValueError) as exc:
        print(f"Conversion failed: {exc}", file=sys.stderr)
        return 1
    finally:
        _cleanup(args, scratch)
    report = _apply_report(input_path, output_path, engine_used, stats)
    report["scan_summary"] = scan.to_dict()["summary"]
    if args.report:
        _write_json(args.report.resolve(), report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def _cmd_decide(args: argparse.Namespace) -> int:
    try:
        payload = json.loads(args.candidates.resolve().read_text(encoding="utf-8"))
        scan = _scan_from_payload(payload)
        if args.provider == "ai":
            if not args.api_key:
                print("AI provider requires --api-key or OPENAI_API_KEY", file=sys.stderr)
                return 2
            decisions = decide_with_ai(
                scan,
                api_key=args.api_key,
                base_url=args.base_url,
                model=args.model,
                timeout_seconds=args.ai_timeout,
                batch_size=args.ai_batch_size,
                max_workers=args.ai_max_workers,
                retries=args.ai_retries,
                failure_fallback=args.ai_failure_fallback,
                progress_callback=None if args.no_ai_progress else _print_ai_progress,
                failure_callback=None if args.no_ai_progress else _print_ai_failure,
            )
        else:
            decisions = {candidate.id: candidate.default_action for candidate in scan.candidates}
        write_decisions_json(scan, decisions, args.output.resolve())
    except Exception as exc:
        print(f"Decide failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"output": str(args.output.resolve()), "decisions": len(decisions)}, ensure_ascii=False, indent=2))
    return 0


def _print_ai_progress(index: int, total: int, candidate: object, action: str) -> None:
    candidate_id = getattr(candidate, "id", "")
    text = getattr(candidate, "text", "")
    print(
        f"正在用 AI 分析第 {index} / {total} 个公式候选：\n"
        f"候选ID：{candidate_id}\n"
        f"原文：{_short_log_text(str(text))}\n"
        f"AI输出：{action}\n",
        flush=True,
    )


def _print_ai_failure(batch_index: int, candidates: list[object], exc: Exception, fallback: str) -> None:
    ids = ", ".join(str(getattr(candidate, "id", "")) for candidate in candidates[:6])
    if len(candidates) > 6:
        ids += ", ..."
    print(
        f"AI请求第 {batch_index} 批失败，已使用 fallback-{fallback} 继续处理。"
        f"候选：{ids}。错误：{exc}",
        file=sys.stderr,
        flush=True,
    )


def _short_log_text(text: str, limit: int = 220) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def _load_dotenv(path: Path | None = None) -> None:
    candidates = []
    if path is not None:
        candidates.append(path)
    candidates.extend(
        [
            Path.cwd() / ".env",
            Path(__file__).resolve().parents[1] / ".env",
        ]
    )
    for env_path in candidates:
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def _env_first(*names: str, default: str | None = None) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


def _scan_from_payload(payload: dict) -> Any:
    from .candidate_pipeline import Candidate, ScanResult

    scan = ScanResult(
        input=payload.get("input", ""),
        prepared_docx=payload.get("prepared_docx", ""),
        engine=payload.get("engine", ""),
        mode=payload.get("mode", "balanced"),
        source_sha256=payload.get("source_sha256", ""),
    )
    scan.paragraphs_skipped = payload.get("summary", {}).get("paragraphs_skipped", 0)
    scan.runs_merged = payload.get("summary", {}).get("runs_merged", 0)
    scan.candidates = [Candidate(**{k: v for k, v in item.items() if k in Candidate.__dataclass_fields__}) for item in payload.get("candidates", [])]
    return scan


def _apply_report(input_path: Path, output_path: Path, engine_used: str, stats: Any) -> dict:
    return {
        "input": str(input_path),
        "output": str(output_path),
        "engine": engine_used,
        "formulas_converted": stats.formulas_converted,
        "formulas_kept": stats.formulas_kept,
        "candidates_seen": stats.candidates_seen,
        "paragraphs_skipped": stats.paragraphs_skipped,
        "runs_merged": stats.runs_merged,
        "parts_changed": stats.parts_changed,
        "failed": stats.failed,
        "samples": stats.samples,
    }


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _cleanup(args: argparse.Namespace, scratch: Path | None) -> None:
    if scratch is not None and not args.keep_intermediate and scratch.exists():
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
