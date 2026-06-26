"""
Sum2Slides v1.0.1 - 将文本摘要自动转换为结构化的幻灯片演示文稿
"""

__version__ = "1.0.1"
__author__ = "技能研发中心"
__email__ = "skill-dev@openclaw.dev"

from .core.parser import TextParser
from .core.analyzer import ContentAnalyzer
from .core.generator import SlideGenerator
from .exporters.pptx import PowerPointExporter
from .models.document import Document, Slide, Presentation
from .api import Sum2Slides

__all__ = [
    "TextParser",
    "ContentAnalyzer", 
    "SlideGenerator",
    "PowerPointExporter",
    "Document",
    "Slide",
    "Presentation",
    "Sum2Slides",
]