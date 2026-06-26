"""Project-wide HTML report renderer.

Skills produce a Markdown research note and an optional JSON evidence pack,
then call ``HtmlReportBuilder`` to wrap them in a self-contained HTML page
with a chosen style theme. Domain charts (valuation bands, K-lines, …) are
contributed by each skill as ``ChartHook`` payloads + JS bodies.
"""

from .builder import HtmlReportBuilder, list_themes
from .chart_hook import ChartHook
from .markdown_engine import render_markdown
from .text_validator import validate_text_preserved

__all__ = [
    "HtmlReportBuilder",
    "ChartHook",
    "list_themes",
    "render_markdown",
    "validate_text_preserved",
]
