"""Write report files in multiple formats."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .junit import render_junit
from .model import Report
from .render_html import render_html
from .render_json import render_json
from .render_md import render_markdown


def write_reports(
    report: Report, out_dir: Path, formats: Iterable[str] | None = None
) -> dict[str, Path]:
    selected = {item.strip().lower() for item in (formats or ["json", "md", "html", "junit"])}
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    if "json" in selected:
        paths["json"] = render_json(report, out_dir / "report.json")
    if "md" in selected or "markdown" in selected:
        paths["md"] = render_markdown(report, out_dir / "report.md")
    if "html" in selected:
        paths["html"] = render_html(report, out_dir / "report.html")
    if "junit" in selected or "xml" in selected:
        paths["junit"] = render_junit(report, out_dir / "junit.xml")
    return paths
