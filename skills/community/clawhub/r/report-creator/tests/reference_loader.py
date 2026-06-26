from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


SHELL_REFERENCE_FILES = [
    "references/html-shell-template.md",
    "references/html-shell/core-structure.md",
    "references/html-shell/shared-component-css.md",
    "references/html-shell/toc-edit-summary.md",
    "references/html-shell/summary-card.md",
    "references/html-shell/export.md",
    "references/html-shell/print-responsive.md",
]

RENDERING_REFERENCE_FILES = [
    "references/rendering-rules.md",
    "references/rendering/plain-markdown.md",
    "references/rendering/kpi.md",
    "references/rendering/chart.md",
    "references/rendering/table-list.md",
    "references/rendering/timeline-diagram.md",
    "references/rendering/media-code-callout.md",
]


def read_reference(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def aggregate_reference(paths: list[str]) -> str:
    return "\n\n".join(read_reference(path) for path in paths)


def shell_reference_text() -> str:
    return aggregate_reference(SHELL_REFERENCE_FILES)


def rendering_reference_text() -> str:
    return aggregate_reference(RENDERING_REFERENCE_FILES)
