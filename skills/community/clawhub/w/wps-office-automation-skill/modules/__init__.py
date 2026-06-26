"""WPS Office处理模块"""

from .document import DocumentProcessor
from .spreadsheet import SpreadsheetProcessor
from .presentation import PresentationProcessor
from .pdf import PDFProcessor

__all__ = [
    "DocumentProcessor",
    "SpreadsheetProcessor",
    "PresentationProcessor",
    "PDFProcessor",
]
