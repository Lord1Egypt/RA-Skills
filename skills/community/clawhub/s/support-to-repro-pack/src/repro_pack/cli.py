"""CLI entry point for repro-pack."""

from __future__ import annotations

import json
import sys

import click


@click.group()
@click.version_option(package_name="repro-pack")
def main() -> None:
    """repro-pack: Convert support tickets into sanitized, reproducible issue packs."""


@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--audit", is_flag=True, help="Detect-only mode: report PII without replacing.")
@click.option("--format", "fmt", type=click.Choice(["text", "json"]), default="text")
def redact(file: str, audit: bool, fmt: str) -> None:
    """Redact PII from a file."""
    from .redactor import RedactionEngine, report_to_json, report_to_text
    from .redactor.detector import detect_pii

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    if audit:
        matches = detect_pii(content)
        if fmt == "json":
            data = [
                {
                    "type": m.pii_type.value,
                    "line": m.line_number,
                    "snippet": m.original_snippet,
                    "placeholder": m.placeholder,
                }
                for m in matches
            ]
            click.echo(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            click.echo(f"Found {len(matches)} PII instances:")
            for m in matches:
                click.echo(f"  Line {m.line_number}: [{m.pii_type.value}] {m.original_snippet}")
    else:
        engine = RedactionEngine()
        sanitized = engine.redact(content)
        click.echo(sanitized, nl=False)

        report = engine.get_report()
        if fmt == "json":
            click.echo(report_to_json(report), err=True)
        else:
            click.echo(report_to_text(report), err=True)


@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--format", "fmt", type=click.Choice(["json", "text"]), default="json")
def parse(file: str, fmt: str) -> None:
    """Parse a log file into structured entries."""
    from .parser import parse_log

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    entries = parse_log(content)

    if fmt == "json":
        data = [
            {
                "line": e.line_number,
                "timestamp": e.timestamp,
                "level": e.level,
                "message": e.message,
                "source": e.source,
            }
            for e in entries
        ]
        click.echo(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        for e in entries:
            ts = e.timestamp or "---"
            level = e.level or "---"
            click.echo(f"[{ts}] [{level}] {e.message}")


@main.command()
@click.argument("file", type=click.Path(exists=True))
def extract(file: str) -> None:
    """Extract structured environment facts from a file."""
    from .extractor import extract_env_facts

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    facts = extract_env_facts(content)
    click.echo(json.dumps(facts.to_dict(), indent=2, ensure_ascii=False))


@main.command()
@click.argument("files", type=click.Path(exists=True), nargs=-1, required=True)
@click.option("--format", "fmt", type=click.Choice(["json", "markdown"]), default="json")
def timeline(files: tuple[str, ...], fmt: str) -> None:
    """Build event timeline from log files."""
    from .extractor import build_timeline, timeline_to_markdown
    from .parser import parse_log

    all_entries = []
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            all_entries.extend(parse_log(f.read()))

    events = build_timeline(all_entries)

    if fmt == "json":
        click.echo(json.dumps([e.to_dict() for e in events], indent=2, ensure_ascii=False))
    else:
        click.echo(timeline_to_markdown(events))


@main.command()
@click.option("--ticket", type=click.Path(exists=True), help="Path to support ticket file.")
@click.option("--logs", type=click.Path(exists=True), multiple=True, help="Path(s) to log files.")
@click.option("--outdir", type=click.Path(), default="repro_output", help="Output directory.")
@click.option("--zip", "do_zip", is_flag=True, help="Also create a zip archive.")
def run(ticket: str | None, logs: tuple[str, ...], outdir: str, do_zip: bool) -> None:
    """Run the full pipeline: parse, redact, extract, and package."""
    from .packager import create_archive
    from .pipeline import run_pipeline

    result = run_pipeline(
        ticket_path=ticket,
        log_paths=list(logs),
        output_dir=outdir,
    )

    click.echo(f"Repro pack created at: {result.output_dir}")
    click.echo(f"Files created: {len(result.files_created)}")
    for f in result.files_created:
        click.echo(f"  ✓ {f}")

    if result.warnings:
        click.echo("\nWarnings:")
        for w in result.warnings:
            click.echo(f"  ! {w}")

    validation = result.validation
    passed = sum(1 for v in validation.values() if v)
    click.echo(f"\nValidation: {passed}/{len(validation)} files present")

    if do_zip:
        zip_path = create_archive(outdir, f"{outdir}.zip")
        click.echo(f"Archive: {zip_path}")


@main.command()
@click.argument("file", type=click.Path(exists=True))
def traces(file: str) -> None:
    """Extract stack traces from a file."""
    from .parser import extract_stack_traces

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    results = extract_stack_traces(content)
    data = []
    for t in results:
        data.append({
            "language": t.language,
            "exception_type": t.exception_type,
            "exception_message": t.exception_message,
            "frames": [
                {"file": f.file_path, "line": f.line_number, "function": f.function_name}
                for f in t.frames
            ],
        })
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))
