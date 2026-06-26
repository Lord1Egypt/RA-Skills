"""
Stock Realtime Brief — A 股实时分析与操作建议生成器

主要 API:
    analyze_single(code) -> AnalysisResult
    analyze_multi(codes) -> AnalysisResult
    analyze_portfolio(path=None) -> AnalysisResult
"""
from .analyzers import analyze_single, analyze_multi, analyze_portfolio, AnalysisResult

__version__ = "2.2.0"
__all__ = [
    "analyze_single",
    "analyze_multi",
    "analyze_portfolio",
    "AnalysisResult",
    "__version__",
]
