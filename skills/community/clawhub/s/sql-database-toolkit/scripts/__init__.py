# -*- coding: utf-8 -*-
"""
SQL Database Toolkit - 全链路 SQL 数据分析工具包
合并 sql-master + sql-dataviz + sql-report-generator 三大 Skill
"""

# ── 数据连接层（原 sql-master）───────────────────────────────────────
from .database_connector import (
    DatabaseConnector,
    QueryResult,
    connect_sqlite,
    connect_mysql,
    connect_postgresql,
)
from .file_connector import (
    FileConnector,
    load_file,
    load_directory,
    load_glob,
    load_dataframe,
)

# ── Pipeline 编排（原 sql-master）───────────────────────────────────
from .pipeline import SQLPipeline
from .unified_pipeline import UnifiedPipeline, analyze_file, analyze_db

# ── 静态图表工厂（原 sql-dataviz）────────────────────────────────────
from .charts import ChartFactory, ChartConfig, Theme

# ── 交互式图表工厂（原 sql-dataviz）─────────────────────────────────
from .interactive_charts import (
    InteractiveChartFactory,
    DashboardBuilder,
    add_annotations,
)

# ── 报告生成组件（原 sql-report-generator）──────────────────────────
from .report_generator import (
    ReportBuilder,
    TableChart,
    MatrixChart,
    SlicerComponent,
    ButtonNavigator,
)

# ── AI 自动洞察（原 sql-report-generator）───────────────────────────
from .ai_insights import InsightGenerator, quick_insights, InsightReport

__all__ = [
    # 数据连接
    "DatabaseConnector", "QueryResult",
    "connect_sqlite", "connect_mysql", "connect_postgresql",
    "FileConnector", "load_file", "load_directory", "load_glob", "load_dataframe",
    # Pipeline
    "SQLPipeline", "UnifiedPipeline", "analyze_file", "analyze_db",
    # 静态图表
    "ChartFactory", "ChartConfig", "Theme",
    # 交互式图表
    "InteractiveChartFactory", "DashboardBuilder", "add_annotations",
    # 报告生成
    "ReportBuilder", "TableChart", "MatrixChart", "SlicerComponent", "ButtonNavigator",
    # AI 洞察
    "InsightGenerator", "quick_insights", "InsightReport",
]
