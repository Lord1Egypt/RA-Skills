"""
trends/formatters/__init__.py - Formatter exports
"""

from trends.formatters.base import BaseFormatter
from trends.formatters.text import TextFormatter
from trends.formatters.json import JsonFormatter
from trends.formatters.html import HtmlFormatter


def get_formatter(result, format_type: str, max_items: int = 10) -> BaseFormatter:
    """
    Get formatter instance by format type.

    Args:
        result: TrendingResult to format
        format_type: One of 'text', 'json', 'html'
        max_items: Maximum items to include

    Returns:
        Formatter instance
    """
    formatters = {
        'text': TextFormatter,
        'json': JsonFormatter,
        'html': HtmlFormatter,
    }
    formatter_class = formatters.get(format_type, TextFormatter)
    return formatter_class(result, max_items)


__all__ = [
    'BaseFormatter',
    'TextFormatter',
    'JsonFormatter',
    'HtmlFormatter',
    'get_formatter',
]