"""Smart Report - 智能报告（内嵌 smart-charts 图表引擎）"""

# 图表引擎版本号：smart-report 的图表核心组件即 smart-charts，此处与其保持同步。
# 本值标识「内嵌图表引擎」的版本（与 smart-charts v8.2.0 对齐），
# 并非 smart-report 自身的版本号（后者见 SKILL.md frontmatter 的 version 字段）。
__version__ = '8.2.1'

from .chart_generator import ChartGenerator, ChartType
from .data_parser import DataParser
from .data_transformer import DataTransformer, CodeValidationError
from .exceptions import (
    SmartChartsError,
    FileError,
    DataError,
    ChartError,
    TransformError,
    ErrorCode,
)

__all__ = [
    'ChartGenerator',
    'ChartType',
    'DataParser',
    'DataTransformer',
    'CodeValidationError',
    'SmartChartsError',
    'FileError',
    'DataError',
    'ChartError',
    'TransformError',
    'ErrorCode',
]
