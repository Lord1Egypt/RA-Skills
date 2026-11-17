"""OCR 引擎路由层 — PaddleOCR + EasyOCR 备选"""

from .base import OCREngine, OCRResult
from .paddleocr_engine import PaddleOCREngine

__all__ = [
    "OCREngine",
    "OCRResult",
    "PaddleOCREngine",
]
