"""Shared CLI for ``render_report_html.py`` entrypoints.

Every skill renderer did the same dance: parse ``--input/--output/--title/
--theme/--no-validate``, read the Markdown, build an ``HtmlReportBuilder``,
render with a "warn-don't-fail" validation policy, write the file, print a
JSON summary. That orchestration lives here once. A skill supplies only the
variable part — a ``build_job(args) -> RenderJob`` that loads its evidence,
extracts chart payloads and configures the builder — plus any extra CLI args.

Usage in a skill::

    from html_report import render_report, RenderJob

    def add_arguments(parser):
        parser.add_argument("--evidence", default=None)

    def build_job(args):
        ...
        return RenderJob(markdown_text=md, builder=builder,
                         output_path=out, summary={...})

    if __name__ == "__main__":
        raise SystemExit(render_report(
            description="Render ... to static HTML.",
            build_job=build_job, add_arguments=add_arguments))
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Sequence

from .builder import HtmlReportBuilder, list_themes


@dataclass
class RenderJob:
    """What a skill's ``build_job`` hands back to the shared runner."""

    markdown_text: str
    builder: HtmlReportBuilder
    output_path: Path
    summary: Dict[str, Any] = field(default_factory=dict)


def render_report(
    *,
    description: str,
    build_job: Callable[[argparse.Namespace], RenderJob],
    add_arguments: Optional[Callable[[argparse.ArgumentParser], None]] = None,
    argv: Optional[Sequence[str]] = None,
) -> int:
    """Parse args, run ``build_job``, render with warn-not-fail validation,
    write the HTML and print a JSON summary. Returns a process exit code.

    Any error (including a ``--strict`` preservation failure) is printed as
    ``error: <msg>`` and turned into exit code 1, matching the per-skill
    wrappers this replaces. ``argv`` defaults to ``sys.argv[1:]``.
    """
    try:
        return _run(description, build_job, add_arguments, argv)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 — CLI boundary: report cleanly, exit 1
        print(f"error: {exc}", file=sys.stderr)
        return 1


def _run(
    description: str,
    build_job: Callable[[argparse.Namespace], RenderJob],
    add_arguments: Optional[Callable[[argparse.ArgumentParser], None]],
    argv: Optional[Sequence[str]],
) -> int:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--input", "-i", required=True, help="Markdown report path.")
    parser.add_argument("--output", "-o", default=None, help="HTML output path. Defaults to input with .html suffix.")
    parser.add_argument("--title", default=None, help="HTML document title. Defaults to the input stem.")
    parser.add_argument("--theme", default="default", choices=list_themes(),
                        help="Style theme. default = AlphaVault (Google Material); claude = Claude.ai (warm); "
                             "print = monochrome serif, A4-friendly.")
    parser.add_argument("--no-validate", action="store_true", help="Skip Markdown text-preservation validation.")
    parser.add_argument("--strict", action="store_true",
                        help="Abort on text-preservation mismatch instead of warning. Off by default so content "
                             "changes never block HTML generation.")
    if add_arguments is not None:
        add_arguments(parser)

    args = parser.parse_args(argv)
    job = build_job(args)

    validation_warning: Optional[str] = None
    try:
        html_text = job.builder.render(job.markdown_text, validate=not args.no_validate)
    except RuntimeError as exc:
        if args.strict or args.no_validate:
            raise
        # Content and format are decoupled: a preservation mismatch is a warning,
        # never a hard stop (run with --strict to fail instead).
        validation_warning = str(exc)
        print(f"warning: {exc}", file=sys.stderr)
        html_text = job.builder.render(job.markdown_text, validate=False)

    job.output_path.parent.mkdir(parents=True, exist_ok=True)
    job.output_path.write_text(html_text, encoding="utf-8")

    summary = {
        "input": str(args.input),
        "output": str(job.output_path),
        "theme": args.theme,
        "validation_warning": validation_warning,
    }
    summary.update(job.summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0
