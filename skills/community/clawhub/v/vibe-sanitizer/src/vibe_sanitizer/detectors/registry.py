from __future__ import annotations

from .base import DetectorContext, RegexDetector
from .builtins import build_builtin_detectors


def build_detector_registry(context: DetectorContext) -> list[RegexDetector]:
    return build_builtin_detectors(context)
