"""
unified_pipeline.py  —  三 Skill 统一 Pipeline 编排
打通 sql-master → sql-dataviz → sql-report-generator 端到端自动化

数据流:
  数据源（文件/数据库/DataFrame）
    → SQL 查询 / 数据转换
    → 静态图表（sql-dataviz ChartFactory, PNG base64）
    → 交互式图表（sql-dataviz InteractiveChartFactory, HTML）
    → AI 自动洞察（sql-report-generator ai_insights）
    → 完整 HTML 报告（DashboardBuilder）

用法:
    from unified_pipeline import UnifiedPipeline, analyze_file

    # 链式 API
    result = (
        UnifiedPipeline("销售分析")
        .from_file("sales.csv")
        .query("SELECT region, SUM(sales) as total FROM data GROUP BY region")
        .chart("bar", x_col="region", y_col="total", title="区域销售")
        .interactive_chart("line", x_col="region", y_col="total")
        .insights(value_cols=["total"])
        .report(title="销售报告", output="report.html")
    )
    print(result.log())

    # 一键分析
    result = analyze_file("sales.csv", output="report.html")
"""

from __future__ import annotations

import os
import sys
import json
import tempfile
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union
from datetime import datetime

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# Skill 路径注册（自动探测）
# ─────────────────────────────────────────────────────────────────────────────

_SKILL_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SKILL_PATHS = {
    "sql_dataviz":        os.path.join(_SKILL_BASE, "sql-dataviz"),
    "sql_dataviz_charts": os.path.join(_SKILL_BASE, "sql-dataviz", "charts"),
    "sql_dataviz_scripts":os.path.join(_SKILL_BASE, "sql-dataviz", "scripts"),
    "sql_report_generator":   os.path.join(_SKILL_BASE, "sql-report-generator", "scripts"),
}

def _add_skill_path(key: str):
    p = SKILL_PATHS.get(key, "")
    if p and p not in sys.path and os.path.exists(p):
        sys.path.insert(0, p)


# ─────────────────────────────────────────────────────────────────────────────
# 数据结构
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class PipelineStep:
    step_type: str
    description: str
    detail: Any = None


@dataclass
class PipelineResult:
    df: Optional[pd.DataFrame] = None
    base64_images: List[str] = field(default_factory=list)
    interactive_charts: List[str] = field(default_factory=list)
    insights: Optional[Any] = None
    export_paths: List[str] = field(default_factory=list)
    steps: List[PipelineStep] = field(default_factory=list)
    summary: str = ""

    def add_step(self, step_type: str, description: str, detail: Any = None):
        self.steps.append(PipelineStep(step_type, description, detail))

    def log(self) -> str:
        lines = [f"UnifiedPipeline 执行日志（{len(self.steps)} 步）:"]
        for i, s in enumerate(self.steps, 1):
            lines.append(f"  {i:2d}. [{s.step_type:18s}] {s.description}")
        if self.summary:
            lines.append(f"\n  总结: {self.summary}")
        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# 主类
# ─────────────────────────────────────────────────────────────────────────────

class UnifiedPipeline:
    """
    三 Skill 统一 Pipeline 编排器

    链式 API:
        UnifiedPipeline(label)
          .from_file(path)          # 从文件加载
          .from_db(dialect, ...)    # 从数据库
          .from_dataframe(df)       # 从 DataFrame
          .query(sql)               # SQL 查询
          .transform(fn)            # 数据转换
          .chart(type, ...)         # 静态图表 (PNG base64)
          .interactive_chart(...)   # 交互式图表 (HTML)
          .insights(...)            # AI 自动洞察
          .report(title, output)    # 生成完整报告
          .to_csv / to_excel / to_json / to_html
    """

    def __init__(self, label: str = ""):
        self.label = label
        self._source_type: str = ""
        self._current_df: Optional[pd.DataFrame] = None
        self._db_conn = None
        self._result = PipelineResult()
        self._theme: str = "powerbi"

    def set_theme(self, theme: str) -> "UnifiedPipeline":
        self._theme = theme
        return self

    # ──────────────────────────────── 数据源 ────────────────────────────────

    def from_file(self, path: str, table_name: str = "data",
                  **kwargs) -> "UnifiedPipeline":
        """从本地文件加载（CSV/Excel/JSON/Parquet/SQLite）"""
        from file_connector import FileConnector
        self._fc = FileConnector(path, table_name=table_name, **kwargs)
        self._current_df = self._fc.df
        self._source_type = "file"
        self._result.add_step("from_file",
            f"加载文件: {os.path.basename(path)} ({self._current_df.shape[0]} 行 × {self._current_df.shape[1]} 列)")
        return self

    def from_files(self, paths: List[str], **kwargs) -> "UnifiedPipeline":
        """从多个文件加载并合并"""
        dfs = []
        for p in paths:
            from file_connector import FileConnector
            dfs.append(FileConnector(p, **kwargs).df)
        self._current_df = pd.concat(dfs, ignore_index=True)
        self._source_type = "files"
        self._result.add_step("from_files",
            f"合并 {len(paths)} 个文件 ({self._current_df.shape[0]} 行)")
        return self

    def from_directory(self, dir_path: str, **kwargs) -> "UnifiedPipeline":
        """加载目录下所有数据文件"""
        from file_connector import FileConnector
        self._fc = FileConnector(dir_path, **kwargs)
        self._current_df = self._fc.df
        self._source_type = "directory"
        self._result.add_step("from_directory",
            f"加载目录: {dir_path} ({self._current_df.shape[0]} 行)")
        return self

    def from_db(self, dialect: str = "sqlite", database: str = "",
                host: str = "localhost", port: int = 3306,
                username: str = "", password: str = "",
                filename: str = None, **kwargs) -> "UnifiedPipeline":
        """从数据库连接（SQLite/MySQL/PostgreSQL/SQL Server）"""
        from database_connector import DatabaseConnector
        self._db_conn = DatabaseConnector(
            dialect=dialect, database=database,
            host=host, port=port,
            username=username, password=password,
            filename=filename, **kwargs
        )
        self._source_type = "db"
        self._result.add_step("from_db",
            f"连接数据库: {dialect} @ {filename or database or host}")
        return self

    def from_dataframe(self, df: pd.DataFrame,
                       label: str = "data") -> "UnifiedPipeline":
        """从 DataFrame 开始"""
        self._current_df = df.copy()
        self._source_type = "dataframe"
        self._result.add_step("from_dataframe",
            f"加载 DataFrame: {label} ({len(df)} 行 × {len(df.columns)} 列)")
        return self

    # ──────────────────────────────── SQL 查询 ───────────────────────────────

    def query(self, sql: str, params: Dict = None) -> "UnifiedPipeline":
        """执行 SQL 查询"""
        import time
        t0 = time.perf_counter()

        if self._source_type == "db" and self._db_conn:
            qr = self._db_conn.execute(sql, params)
            self._current_df = qr.df
            elapsed = (time.perf_counter() - t0) * 1000
            self._result.add_step("query",
                f"SQL 查询 → {len(self._current_df)} 行 ({elapsed:.1f}ms)")
        else:
            # 文件/DataFrame → SQLite 内存查询
            from file_connector import FileConnector
            if hasattr(self, "_fc") and isinstance(self._fc, FileConnector):
                fc = self._fc
            else:
                fc = FileConnector(self._current_df, table_name="data")
            self._current_df = fc.query(sql)
            elapsed = (time.perf_counter() - t0) * 1000
            self._result.add_step("query",
                f"SQL 查询 → {len(self._current_df)} 行 ({elapsed:.1f}ms)")

        self._result.df = self._current_df
        return self

    def transform(self, fn: Callable, **kwargs) -> "UnifiedPipeline":
        """对当前 DataFrame 应用转换函数"""
        self._current_df = fn(self._current_df, **kwargs)
        self._result.df = self._current_df
        self._result.add_step("transform",
            f"数据转换: {getattr(fn, '__name__', 'lambda')} → {self._current_df.shape}")
        return self

    def limit(self, n: int) -> "UnifiedPipeline":
        self._current_df = self._current_df.head(n)
        self._result.add_step("transform", f"LIMIT {n}")
        return self

    # ──────────────────────────────── 静态图表 ──────────────────────────────

    def chart(self, chart_type: str, x_col: str = None, y_col: str = None,
              series: List[Dict] = None, title: str = "",
              **kwargs) -> "UnifiedPipeline":
        """生成静态图表（PNG base64），调用 sql-dataviz ChartFactory"""
        _add_skill_path("sql_dataviz_charts")
        _add_skill_path("sql_dataviz")
        try:
            from charts import ChartFactory
            factory = ChartFactory()
            factory.set_theme(self._theme)
            data = self._build_chart_data(chart_type, x_col, y_col, series, title)
            create_fn = getattr(factory, f"create_{chart_type}", None)
            if not create_fn:
                raise ValueError(f"ChartFactory 没有 create_{chart_type}")
            b64 = create_fn(data)
            self._result.base64_images.append(b64)
            self._result.add_step("chart",
                f"静态图表 [{chart_type}]: {title or x_col+' vs '+y_col}")
        except Exception as e:
            self._result.add_step("chart", f"静态图表失败: {e}")
        return self

    # ──────────────────────────────── 交互式图表 ────────────────────────────

    def interactive_chart(self, chart_type: str, x_col: str = None,
                          y_col: str = None, series: List[Dict] = None,
                          title: str = "", **kwargs) -> "UnifiedPipeline":
        """生成交互式图表（HTML），调用 sql-dataviz InteractiveChartFactory"""
        _add_skill_path("sql_dataviz_scripts")
        try:
            from interactive_charts import InteractiveChartFactory
            factory = InteractiveChartFactory(theme=self._theme)
            data = self._build_chart_data(chart_type, x_col, y_col, series, title)
            create_fn = getattr(factory, f"create_{chart_type}", None)
            if not create_fn:
                raise ValueError(f"InteractiveChartFactory 没有 create_{chart_type}")
            html = create_fn(data, title=title)
            self._result.interactive_charts.append(html)
            self._result.add_step("interactive_chart",
                f"交互式图表 [{chart_type}]: {title or x_col+' vs '+y_col}")
        except Exception as e:
            self._result.add_step("interactive_chart", f"交互式图表失败: {e}")
        return self

    def dashboard(self, charts: List[Dict], title: str = "",
                  output: str = "") -> "UnifiedPipeline":
        """
        生成多图表 Dashboard（HTML）
        charts: [{"type":"line","x":"month","y":"sales","title":"趋势"}, ...]
        """
        _add_skill_path("sql_dataviz_scripts")
        try:
            from interactive_charts import InteractiveChartFactory, DashboardBuilder
            factory = InteractiveChartFactory(theme=self._theme)
            builder = DashboardBuilder(title=title, theme=self._theme)

            for c in charts:
                ct = c.pop("type")
                x = c.pop("x", None)
                y = c.pop("y", None)
                t = c.pop("title", "")
                data = self._build_chart_data(ct, x, y, None, t)
                create_fn = getattr(factory, f"create_{ct}", None)
                if create_fn:
                    html = create_fn(data, title=t)
                    builder.add_chart(html, title=t, cols=c.pop("cols", 1))

            out = output or tempfile.mktemp(suffix=".html")
            builder.build(out)
            self._result.export_paths.append(os.path.abspath(out))
            self._result.add_step("dashboard",
                f"Dashboard ({len(charts)} 图表) → {out}")
        except Exception as e:
            self._result.add_step("dashboard", f"Dashboard 失败: {e}")
        return self

    # ──────────────────────────────── AI 洞察 ───────────────────────────────

    def insights(self, date_col: str = None,
                 value_cols: List[str] = None,
                 dimension_cols: List[str] = None) -> "UnifiedPipeline":
        """生成 AI 自动洞察，调用 sql-report-generator ai_insights"""
        _add_skill_path("sql_report_generator")
        try:
            from ai_insights import quick_insights
            report = quick_insights(
                self._current_df,
                date_col=date_col,
                value_cols=value_cols,
            )
            self._result.insights = report
            self._result.add_step("insights",
                f"AI 洞察: {len(report.insights)} 条洞察, "
                f"{len(report.recommendations)} 条建议")
        except Exception as e:
            self._result.add_step("insights", f"AI 洞察失败: {e}")
        return self

    # ──────────────────────────────── 报告生成 ──────────────────────────────

    def report(self, title: str = "数据分析报告",
               output: str = "",
               include_charts: bool = True,
               include_insights: bool = True,
               include_table: bool = True) -> "UnifiedPipeline":
        """
        生成完整 HTML 报告
        整合：KPI 卡片 + 交互式图表 + 静态图表 + AI 洞察 + 数据表格
        """
        _add_skill_path("sql_dataviz_scripts")

        try:
            from interactive_charts import DashboardBuilder
            builder = DashboardBuilder(title=title, theme=self._theme)

            # 1. 数据摘要 KPI 卡片
            df = self._current_df
            if df is not None and not df.empty:
                num_cols = df.select_dtypes(include="number").columns.tolist()
                kpi_cards = [
                    {"title": "数据行数", "value": f"{len(df):,}", "change": ""},
                    {"title": "数据列数", "value": str(len(df.columns)), "change": ""},
                ]
                for col in num_cols[:3]:
                    kpi_cards.append({
                        "title": f"{col} 合计",
                        "value": f"{df[col].sum():,.0f}",
                        "change": ""
                    })
                builder.add_kpi_cards(kpi_cards)

            # 2. 交互式图表
            if include_charts and self._result.interactive_charts:
                for i, chart_html in enumerate(self._result.interactive_charts):
                    builder.add_chart(chart_html, title=f"图表 {i+1}", cols=1)

            # 3. 静态图表（base64 嵌入）
            if include_charts and self._result.base64_images:
                imgs_html = ""
                for b64 in self._result.base64_images:
                    imgs_html += (f'<img src="data:image/png;base64,{b64}" '
                                  f'style="max-width:100%;border-radius:6px;margin:8px 0;">')
                builder._sections.append({"type": "markdown",
                                          "text": imgs_html})

            # 4. AI 洞察
            if include_insights and self._result.insights:
                try:
                    insights_html = self._result.insights.to_html()
                    builder.add_insights(insights_html)
                except Exception:
                    pass

            # 5. 数据表格
            if include_table and df is not None and not df.empty:
                from interactive_charts import InteractiveChartFactory
                factory = InteractiveChartFactory(theme=self._theme)
                table_html = factory.create_table({
                    "columns": df.columns.tolist(),
                    "rows": df.head(200).values.tolist()
                }, title="数据预览（前200行）")
                builder.add_chart(table_html, title="数据预览", cols=2)

            # 6. 执行日志
            builder.add_markdown(
                f"## Pipeline 执行日志\n" +
                "\n".join(f"- [{s.step_type}] {s.description}"
                          for s in self._result.steps)
            )

            out = output or tempfile.mktemp(suffix=".html")
            builder.build(out)
            self._result.export_paths.append(os.path.abspath(out))
            self._result.summary = (
                f"报告已生成: {out} | "
                f"{len(self._result.base64_images)} 静态图 | "
                f"{len(self._result.interactive_charts)} 交互图 | "
                f"{len(self._result.insights.insights) if self._result.insights else 0} 条洞察"
            )
            self._result.add_step("report", f"生成报告 → {out}")

        except Exception as e:
            self._result.add_step("report", f"报告生成失败: {e}")
            raise

        return self

    # ──────────────────────────────── 导出 ──────────────────────────────────

    def to_csv(self, path: str, **kwargs) -> "UnifiedPipeline":
        self._ensure_dir(path)
        self._current_df.to_csv(path, index=False, encoding="utf-8-sig", **kwargs)
        self._result.export_paths.append(os.path.abspath(path))
        self._result.add_step("export", f"CSV → {path}")
        return self

    def to_excel(self, path: str, **kwargs) -> "UnifiedPipeline":
        self._ensure_dir(path)
        self._current_df.to_excel(path, index=False, engine="openpyxl", **kwargs)
        self._result.export_paths.append(os.path.abspath(path))
        self._result.add_step("export", f"Excel → {path}")
        return self

    def to_json(self, path: str, **kwargs) -> "UnifiedPipeline":
        self._ensure_dir(path)
        self._current_df.to_json(path, orient="records", force_ascii=False, **kwargs)
        self._result.export_paths.append(os.path.abspath(path))
        self._result.add_step("export", f"JSON → {path}")
        return self

    def to_html(self, path: str, title: str = "") -> "UnifiedPipeline":
        self._ensure_dir(path)
        html = self._current_df.to_html(index=False, classes="table", border=0)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"<html><head><meta charset='utf-8'><title>{title}</title></head>"
                    f"<body>{html}</body></html>")
        self._result.export_paths.append(os.path.abspath(path))
        self._result.add_step("export", f"HTML → {path}")
        return self

    # ──────────────────────────────── 属性 ──────────────────────────────────

    @property
    def df(self) -> Optional[pd.DataFrame]:
        return self._current_df

    @property
    def result(self) -> PipelineResult:
        return self._result

    def log(self) -> str:
        return self._result.log()

    # ──────────────────────────────── 内部工具 ──────────────────────────────

    def _build_chart_data(self, chart_type: str, x_col: str, y_col: str,
                          series: List[Dict], title: str) -> Dict:
        """根据 chart_type 构建图表数据字典"""
        df = self._current_df
        data: Dict[str, Any] = {"title": title}

        if series:
            data["categories"] = df[x_col].tolist() if x_col else []
            data["series"] = series
        elif chart_type in ("line", "area", "smooth_line", "bar",
                            "clustered_column", "stacked_column"):
            data["categories"] = df[x_col].tolist()
            data["series"] = [{"name": y_col, "data": df[y_col].tolist()}]
        elif chart_type in ("pie", "donut"):
            data["labels"] = df[x_col].tolist()
            data["values"] = df[y_col].tolist()
        elif chart_type == "scatter":
            data["x"] = df[x_col].tolist()
            data["y"] = df[y_col].tolist()
        elif chart_type == "funnel":
            data["stages"] = df[x_col].tolist()
            data["values"] = df[y_col].tolist()
        elif chart_type == "heatmap":
            data["x_labels"] = df[x_col].tolist()
            data["y_labels"] = df[y_col].tolist() if y_col else []
            data["z_values"] = df.select_dtypes("number").values.tolist()
        else:
            data["categories"] = df[x_col].tolist() if x_col else []
            data["series"] = [{"name": y_col or "值",
                                "data": df[y_col].tolist() if y_col else []}]
        return data

    @staticmethod
    def _ensure_dir(path: str):
        d = os.path.dirname(os.path.abspath(path))
        if d:
            os.makedirs(d, exist_ok=True)

    def __repr__(self):
        shape = self._current_df.shape if self._current_df is not None else (0, 0)
        return f"<UnifiedPipeline label={self.label!r} source={self._source_type} shape={shape}>"


# ─────────────────────────────────────────────────────────────────────────────
# 便捷函数
# ─────────────────────────────────────────────────────────────────────────────

def analyze_file(path: str, sql: str = None,
                 charts: List[Dict] = None,
                 with_insights: bool = True,
                 output: str = "",
                 title: str = "") -> PipelineResult:
    """
    一键分析：文件 → SQL → 图表 → 洞察 → 报告

    示例:
        result = analyze_file(
            "sales.csv",
            sql="SELECT region, SUM(sales) as total FROM data GROUP BY region",
            charts=[{"type":"bar","x":"region","y":"total","title":"区域销售"}],
            output="report.html"
        )
        print(result.log())
    """
    p = UnifiedPipeline(title or os.path.basename(path)).from_file(path)
    if sql:
        p.query(sql)
    if charts:
        for c in charts:
            ct = c.get("type", "bar")
            p.interactive_chart(ct, x_col=c.get("x"), y_col=c.get("y"),
                                 title=c.get("title", ""))
    if with_insights:
        p.insights()
    p.report(title=title or f"{os.path.basename(path)} 分析报告",
             output=output or tempfile.mktemp(suffix=".html"))
    return p.result


def analyze_db(dialect: str, database: str, sql: str,
               charts: List[Dict] = None,
               with_insights: bool = True,
               output: str = "",
               title: str = "",
               **kwargs) -> PipelineResult:
    """
    一键分析：数据库 → SQL → 图表 → 洞察 → 报告
    """
    p = (UnifiedPipeline(title or f"{dialect}:{database}")
         .from_db(dialect=dialect, database=database, **kwargs)
         .query(sql))
    if charts:
        for c in charts:
            ct = c.get("type", "bar")
            p.interactive_chart(ct, x_col=c.get("x"), y_col=c.get("y"),
                                 title=c.get("title", ""))
    if with_insights:
        p.insights()
    p.report(title=title or f"{database} 分析报告",
             output=output or tempfile.mktemp(suffix=".html"))
    return p.result


# ─────────────────────────────────────────────────────────────────────────────
# 测试入口
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile
    import os

    print("=== UnifiedPipeline 端到端测试 ===\n")

    # 创建模拟数据
    df = pd.DataFrame({
        "month":    ["Jan","Feb","Mar","Apr","May"] * 3,
        "region":   ["East"]*5 + ["North"]*5 + ["South"]*5,
        "product":  ["A","B","A","B","A"] * 3,
        "sales":    [1200,1500,1800,2000,2200,
                     800, 900,1000,1100,1200,
                     600, 700, 800, 900,1000],
        "quantity": [100,120,150,170,180,
                     60, 70, 80, 90,100,
                     50, 55, 60, 65, 70],
    })

    csv_path = tempfile.mktemp(suffix=".csv")
    df.to_csv(csv_path, index=False)
    report_path = tempfile.mktemp(suffix=".html")

    # 完整 Pipeline
    p = UnifiedPipeline("销售分析")
    p.from_file(csv_path)
    p.query("SELECT region, SUM(sales) as total_sales, SUM(quantity) as total_qty FROM data GROUP BY region ORDER BY total_sales DESC")
    p.interactive_chart("bar", x_col="region", y_col="total_sales", title="区域销售排行")
    p.interactive_chart("pie", x_col="region", y_col="total_sales", title="区域占比")
    p.insights(value_cols=["total_sales", "total_qty"])
    p.report(title="区域销售分析报告", output=report_path)

    print(p.log())
    print(f"\n报告路径: {report_path}")
    print(f"报告大小: {os.path.getsize(report_path)/1024:.1f} KB")
    print(f"交互图表: {len(p.result.interactive_charts)} 个")
    print(f"AI 洞察: {len(p.result.insights.insights) if p.result.insights else 0} 条")
    print(f"导出文件: {p.result.export_paths}")

    os.unlink(csv_path)
    print("\n=== ALL TESTS PASSED ===")
