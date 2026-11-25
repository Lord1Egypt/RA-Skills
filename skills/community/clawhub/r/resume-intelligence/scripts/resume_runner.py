#!/usr/bin/env python3
"""Create a Resume Intelligence run folder from bundled templates."""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import date as date_type
from pathlib import Path


DEFAULT_TEMPLATES = [
    "source-inventory.md",
    "tool-usage-log.md",
    "evidence.md",
    "run-summary.md",
    "safe-local-mode-checklist.md",
    "disclosure-approval-queue.md",
    "final-redaction-review.md",
    "draft-resume.md",
    "detailed-resume.md",
    "career-master-run.md",
    "missing-information-loop.md",
    "career-positioning-coach.md",
    "resume-scorecard.md",
    "professional-resume.md",
    "visual-template-selector.md",
    "job-match-report.md",
    "project-interview-briefs.md",
    "technical-stack-interview-guide.md",
    "interview-readiness-scorecard.md",
    "interview-prep-pack.md",
    "linkedin-recommendations.md",
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "resume-run"


def default_templates_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "assets" / "templates"


def create_run_folder(
    *,
    output_root: Path,
    templates_dir: Path,
    slug: str,
    template_names: list[str],
    date: str | None = None,
) -> Path:
    run_date = date or date_type.today().isoformat()
    run_dir = output_root / f"{run_date}-{slugify(slug)}"
    run_dir.mkdir(parents=True, exist_ok=False)

    copied: list[str] = []
    missing: list[str] = []
    for template_name in template_names:
        source = templates_dir / template_name
        if source.exists():
            shutil.copyfile(source, run_dir / template_name)
            copied.append(template_name)
        else:
            missing.append(template_name)

    readme_lines = [
        "# Resume Intelligence Run",
        "",
        f"- Run folder: `{run_dir.name}`",
        f"- Template source: `{templates_dir}`",
        f"- Templates copied: {', '.join(copied) if copied else 'none'}",
        f"- Templates missing: {', '.join(missing) if missing else 'none'}",
        "",
        "Start with `source-inventory.md` and `tool-usage-log.md`, then build evidence-backed outputs.",
    ]
    (run_dir / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")
    return run_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="Descriptive run name, such as target role or company.")
    parser.add_argument(
        "--output-root",
        default="resume-runs",
        help="Directory where run folders are created.",
    )
    parser.add_argument(
        "--templates-dir",
        default=str(default_templates_dir()),
        help="Template directory to copy from.",
    )
    parser.add_argument(
        "--template",
        action="append",
        dest="templates",
        help="Template filename to copy. Repeat to select multiple templates.",
    )
    parser.add_argument("--date", help="Run date in YYYY-MM-DD format. Defaults to today.")
    args = parser.parse_args()

    run_dir = create_run_folder(
        output_root=Path(args.output_root),
        templates_dir=Path(args.templates_dir),
        slug=args.slug,
        template_names=args.templates or DEFAULT_TEMPLATES,
        date=args.date,
    )
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
