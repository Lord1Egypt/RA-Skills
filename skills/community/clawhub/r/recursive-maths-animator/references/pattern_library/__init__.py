"""
Animation Pattern Library
AutoAgent-trained patterns for Manim animations.

This library contains working animation patterns for:
- Table to graph transformations
- Statistical visualizations  
- Pie chart animations

All patterns are VoiceoverScene subclasses with configurable parameters.

Usage:
    from references.pattern_library import TableToBarChartPattern
    
    scene = TableToBarChartPattern()
    scene.data = [("Q1", 1000), ("Q2", 1500)]
    scene.construct()
    
Or run directly:
    python -m references.pattern_library.table_transforms
"""

from .table_transforms import (
    TableToBarChartPattern,
    TableToLineGraphPattern,
    TableToScatterPlotPattern,
)

from .statistical_viz import (
    DistributionAnimation,
    FormulaDerivation,
    SamplingVisualization,
)

from .pie_chart_animations import (
    BasicPieChart,
    StaggeredPieChart,
    PieToBarTransition,
)

__version__ = "1.0.0"
__author__ = "AutoAgent Training System"

__all__ = [
    # Table transforms
    "TableToBarChartPattern",
    "TableToLineGraphPattern",
    "TableToScatterPlotPattern",
    # Statistical viz
    "DistributionAnimation",
    "FormulaDerivation",
    "SamplingVisualization",
    # Pie charts
    "BasicPieChart",
    "StaggeredPieChart",
    "PieToBarTransition",
]
