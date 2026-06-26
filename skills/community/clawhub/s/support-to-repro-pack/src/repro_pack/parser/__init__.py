"""Parser module — log, stack trace, and ticket parsing."""

from .formats import detect_file_format, detect_format
from .log_parser import parse_log
from .stack_trace import extract_stack_traces
from .ticket_parser import parse_ticket

__all__ = [
    "detect_file_format",
    "detect_format",
    "parse_log",
    "extract_stack_traces",
    "parse_ticket",
]
