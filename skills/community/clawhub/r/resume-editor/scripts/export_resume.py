#!/usr/bin/env python3
"""
Unified export entrypoint for resume HTML and PDF outputs.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from resume_utils import DEFAULT_THEME, SUPPORTED_LANGUAGES, list_available_themes, resolve_theme_assets


def resolve_output_paths(output_path, output_format):
    """Return the HTML intermediary path and final output path."""
    output = Path(output_path)

    if output_format == "html":
        html_output = output if output.suffix.lower() == ".html" else output.with_suffix(".html")
        return html_output, html_output

    if output.suffix.lower() == ".pdf":
        pdf_output = output
        html_output = output.with_suffix(".html")
    elif output.suffix.lower() == ".html":
        html_output = output
        pdf_output = output.with_suffix(".pdf")
    else:
        pdf_output = output.with_suffix(".pdf")
        html_output = output.with_suffix(".html")

    return html_output, pdf_output


def main():
    parser = argparse.ArgumentParser(description="Export a resume JSON file to HTML or PDF")
    parser.add_argument("resume_json", help="Path to resume JSON file")
    parser.add_argument("output", help="Path to final output file")
    parser.add_argument("--format", default="html", choices=["html", "pdf"], help="Output format")
    parser.add_argument(
        "--theme",
        default=DEFAULT_THEME,
        help="Built-in theme name, a user-themes/<name> custom theme, or a path to a custom theme directory",
    )
    parser.add_argument("--lang", default="en", choices=SUPPORTED_LANGUAGES, help="Output language")
    parser.add_argument(
        "--editable",
        action="store_true",
        help="Generate editable HTML. Ignored for PDF exports, which always use a clean final HTML.",
    )

    args = parser.parse_args()

    if args.editable and args.format == "pdf":
        print(
            "Warning: --editable is ignored for PDF export (PDF always renders a clean, "
            "non-editable HTML intermediary). Drop --editable, or export HTML with "
            "--editable first, then convert the reviewed JSON to PDF.",
            file=sys.stderr,
        )

    script_dir = Path(__file__).resolve().parent
    try:
        resolve_theme_assets(args.theme, script_dir.parent)
    except ValueError as exc:
        print(f"Error: {exc}")
        print(f"Available themes: {', '.join(list_available_themes(script_dir.parent))}")
        sys.exit(1)

    html_output, final_output = resolve_output_paths(args.output, args.format)

    generate_html_cmd = [
        sys.executable,
        str(script_dir / "generate_html.py"),
        "--theme",
        args.theme,
        "--lang",
        args.lang,
    ]
    if args.editable and args.format == "html":
        generate_html_cmd.append("--editable")
    generate_html_cmd.extend([args.resume_json, str(html_output)])

    print(f"Generating HTML resume with theme '{args.theme}' in {args.lang}...")
    subprocess.run(generate_html_cmd, check=True)

    if args.format == "pdf":
        print(f"Converting HTML to PDF: {final_output}")
        subprocess.run(
            [
                sys.executable,
                str(script_dir / "generate_pdf.py"),
                str(html_output),
                str(final_output),
            ],
            check=True,
        )

    print(f"Final output: {final_output}")
    if args.format == "html":
        print(f"Open in browser to view: file://{html_output.resolve()}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
