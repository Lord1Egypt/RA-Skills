"""
pipeline.py
SQL 数据分析 Pipeline - 连接数据获取 → SQL 查询 → 格式转换 → 可视化 → 报告生成

三大用途:
  1. SQL 查询（对数据库或本地文件执行 SQL）
  2. 格式转换（CSV ⇄ Excel ⇄ JSON ⇄ Parquet ⇄ SQLite）
  3. 传给 sql-dataviz / sql-report-generator（输出 HTML/PDF/PNG 看板）

用法:
    from pipeline import SQLPipeline

    # 方式一：从文件开始
    p = SQLPipeline().from_file("data/sales.csv").query("SELECT * FROM data LIMIT 5")

    # 方式二：从数据库开始
    p = SQLPipeline().from_db(dialect="sqlite", database="data.db").query("SELECT * FROM sales")

    # 方式三：从 DataFrame 开始
    p = SQLPipeline().from_dataframe(df)

    # 管道操作
    p.query("SELECT region, SUM(amount) GROUP BY region") \\
     .to_csv("output/result.csv") \\
     .to_dataviz("line", x="month", y="sales") \\
     .to_report(title="销售分析报告", output="html")
"""

from __future__ import annotations

import os
import json
from typing import Optional, Dict, Any, List, Union, Tuple
from pathlib import Path
from dataclasses import dataclass, field

import pandas as pd

from .database_connector import DatabaseConnector, QueryResult
from .file_connector import FileConnector


# ─────────────────────────────────────────────────────────────────────────────
# Pipeline 数据结构
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class PipelineStep:
    """流水线步骤记录"""
    step_type: str        # file_load | db_connect | sql_query | transform | export | viz | report
    description: str
    detail: Any = None


@dataclass
class PipelineResult:
    """流水线执行结果"""
    df: Optional[pd.DataFrame]
    query_result: Optional[QueryResult]
    base64_images: List[str]         # 图表 base64 列表
    export_paths: List[str]           # 导出文件路径列表
    steps: List[PipelineStep]         # 执行步骤记录
    summary: str = ""

    def add_step(self, step_type: str, description: str, detail: Any = None):
        self.steps.append(PipelineStep(step_type, description, detail))

    def log(self) -> str:
        lines = [f"Pipeline 执行日志（共 {len(self.steps)} 步）:"]
        for i, s in enumerate(self.steps, 1):
            lines.append(f"  {i}. [{s.step_type}] {s.description}")
        if self.summary:
            lines.append(f"\n总结: {self.summary}")
        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Pipeline 主类
# ─────────────────────────────────────────────────────────────────────────────

class SQLPipeline:
    """
    SQL 数据分析流水线

    链式 API:
        SQLPipeline()
          .from_file(...)    # 从文件加载数据
          .from_db(...)      # 从数据库连接
          .from_dataframe(...)  # 从 DataFrame
          .query(sql)        # 执行 SQL 查询
          .transform(fn)      # 数据转换
          .to_csv(path)       # 导出 CSV
          .to_excel(path)     # 导出 Excel
          .to_json(path)      # 导出 JSON
          .to_parquet(path)   # 导出 Parquet
          .to_sqlite(path)    # 导出 SQLite
          .to_dataviz(...)    # 生成图表
          .to_report(...)     # 生成 HTML/PDF 报告
          .run()              # 执行
    """

    def __init__(self, label: str = ""):
        self.label = label
        self._source: Optional[Union[FileConnector, DatabaseConnector, pd.DataFrame]] = None
        self._source_type: str = ""   # file | db | dataframe
        self._current_df: Optional[pd.DataFrame] = None
        self._result = PipelineResult(
            df=None,
            query_result=None,
            base64_images=[],
            export_paths=[],
            steps=[],
        )

    # ──────────────────────────────── 数据源 ────────────────────────────────

    def from_file(
        self,
        path: str,
        table_name: Optional[str] = None,
        **kwargs
    ) -> "SQLPipeline":
        """
        从本地文件加载数据

        支持: CSV, Excel, JSON, Parquet, Feather, SQLite, Stata, SAS 等
        """
        fc = FileConnector(path, table_name=table_name, **kwargs)
        self._source = fc
        self._source_type = "file"
        self._current_df = fc.df
        self._result.add_step("file_load", f"加载文件: {path} ({fc.shape[0]} 行)")
        return self

    def from_files(self, paths: List[str], **kwargs) -> "SQLPipeline":
        """从多个文件加载（自动合并）"""
        import glob
        all_dfs = []
        for p in paths:
            fc = FileConnector(p, **kwargs)
            all_dfs.append(fc.df)
        self._current_df = pd.concat(all_dfs, ignore_index=True)
        self._source_type = "files"
        self._source = self._current_df
        self._result.add_step("file_load", f"加载 {len(paths)} 个文件")
        return self

    def from_directory(self, dir_path: str, **kwargs) -> "SQLPipeline":
        """加载目录下所有数据文件"""
        fc = FileConnector(dir_path, **kwargs)
        self._source = fc
        self._source_type = "directory"
        self._current_df = fc.df
        self._result.add_step("file_load", f"加载目录: {dir_path} ({fc.shape[0]} 行)")
        return self

    def from_db(
        self,
        dialect: str = "sqlite",
        database: str = "",
        host: str = "localhost",
        port: int = 3306,
        username: str = "",
        password: str = "",
        filename: Optional[str] = None,
        **kwargs
    ) -> "SQLPipeline":
        """
        从数据库连接加载

        支持: SQLite, MySQL, PostgreSQL, SQL Server 等
        """
        conn = DatabaseConnector(
            dialect=dialect, database=database,
            host=port, username=username, password=password,
            filename=filename, **kwargs
        )
        self._source = conn
        self._source_type = "db"
        self._result.add_step("db_connect", f"连接数据库: {dialect} @ {host or database}")
        return self

    def from_dataframe(self, df: pd.DataFrame, label: str = "data") -> "SQLPipeline":
        """从 DataFrame 开始"""
        self._source = df
        self._source_type = "dataframe"
        self._current_df = df.copy()
        self._result.add_step("df_load", f"加载 DataFrame: {label} ({len(df)} 行)")
        return self

    # ──────────────────────────────── SQL 查询 ───────────────────────────────

    def query(self, sql: str, params: Optional[Dict] = None) -> "SQLPipeline":
        """
        执行 SQL 查询

        - 如果数据源是 FileConnector → 使用 SQLite 内存查询
        - 如果数据源是 DatabaseConnector → 直接执行 SQL
        - 如果数据源是 DataFrame → 先转 SQLite 再查
        """
        if self._source_type == "db":
            qres = self._source.execute(sql, params)
            self._current_df = qres.df
            self._result.query_result = qres
            self._result.df = qres.df
            self._result.add_step(
                "sql_query",
                f"执行 SQL → {qres.rowcount} 行 ({qres.execution_time_ms:.1f}ms)",
                {"sql": sql[:100], "rowcount": qres.rowcount}
            )
        elif self._source_type in ("file", "directory", "files", "dataframe"):
            if isinstance(self._source, FileConnector):
                fc = self._source
            else:
                fc = FileConnector(self._current_df if isinstance(self._source, pd.DataFrame) else None,
                                   table_name=self.label or "data")
            qres = fc.sql_result(sql, params)
            self._current_df = qres.df
            self._result.query_result = qres
            self._result.df = qres.df
            self._result.add_step(
                "sql_query",
                f"SQL 查询 → {qres.rowcount} 行 ({qres.execution_time_ms:.1f}ms)",
                {"sql": sql[:100], "rowcount": qres.rowcount}
            )
        else:
            raise RuntimeError("请先设置数据源（from_file / from_db / from_dataframe）")

        return self

    def transform(self, fn: callable, **kwargs) -> "SQLPipeline":
        """
        对当前数据应用转换函数

        示例:
            p.transform(lambda df: df[df["amount"] > 1000])
            p.transform(lambda df: df.groupby("region").sum().reset_index())
            p.transform(lambda df: df.assign(year=df["date"].dt.year))
        """
        df = fn(self._current_df, **kwargs)
        self._current_df = df
        self._result.df = df
        self._result.add_step("transform", f"数据转换: {fn.__name__ or 'anonymous'}")
        return self

    def limit(self, n: int) -> "SQLPipeline":
        """限制行数"""
        self._current_df = self._current_df.head(n)
        self._result.df = self._current_df
        self._result.add_step("transform", f"LIMIT {n}")
        return self

    def columns(self, cols: List[str]) -> "SQLPipeline":
        """选择列"""
        self._current_df = self._current_df[cols]
        self._result.df = self._current_df
        self._result.add_step("transform", f"SELECT {cols}")
        return self

    # ──────────────────────────────── 导出格式 ───────────────────────────────

    def to_csv(self, path: str, **kwargs) -> "SQLPipeline":
        """导出为 CSV"""
        self._ensure_output_dir(path)
        self._current_df.to_csv(path, index=False, encoding="utf-8-sig", **kwargs)
        self._result.export_paths.append(os.path.abspath(path))
        self._result.add_step("export", f"导出 CSV → {path}")
        return self

    def to_excel(self, path: str, sheet_name: str = "Sheet1", **kwargs) -> "SQLPipeline":
        """导出为 Excel"""
        self._ensure_output_dir(path)
        self._current_df.to_excel(path, index=False, sheet_name=sheet_name, engine="openpyxl", **kwargs)
        self._result.export_paths.append(os.path.abspath(path))
        self._result.add_step("export", f"导出 Excel → {path}")
        return self

    def to_json(self, path: str, **kwargs) -> "SQLPipeline":
        """导出为 JSON"""
        self._ensure_output_dir(path)
        self._current_df.to_json(path, orient="records", force_ascii=False, **kwargs)
        self._result.export_paths.append(os.path.abspath(path))
        self._result.add_step("export", f"导出 JSON → {path}")
        return self

    def to_parquet(self, path: str, **kwargs) -> "SQLPipeline":
        """导出为 Parquet"""
        self._ensure_output_dir(path)
        self._current_df.to_parquet(path, index=False, **kwargs)
        self._result.export_paths.append(os.path.abspath(path))
        self._result.add_step("export", f"导出 Parquet → {path}")
        return self

    def to_sqlite(self, db_path: str, table_name: str = "data", **kwargs) -> "SQLPipeline":
        """导出为 SQLite 数据库"""
        self._ensure_output_dir(db_path)
        import sqlite3
        conn = sqlite3.connect(db_path)
        self._current_df.to_sql(table_name, conn, index=False, **kwargs)
        conn.close()
        self._result.export_paths.append(os.path.abspath(db_path))
        self._result.add_step("export", f"导出 SQLite → {db_path}")
        return self

    def to_html(self, path: str, title: str = "数据表格", **kwargs) -> "SQLPipeline":
        """导出为 HTML 表格"""
        self._ensure_output_dir(path)
        html = self._current_df.to_html(index=False, classes="table table-striped", border=0)
        full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
  body {{ font-family: 'Microsoft YaHei', sans-serif; padding: 20px; }}
  .table {{ border-collapse: collapse; width: 100%; }}
  .table th {{ background: #0078D4; color: white; padding: 8px; }}
  .table td {{ padding: 8px; border: 1px solid #ddd; }}
  .table tr:nth-child(even) {{ background: #f5f5f5; }}
</style></head><body>
<h2>{title}</h2>{html}
</body></html>"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(full_html)
        self._result.export_paths.append(os.path.abspath(path))
        self._result.add_step("export", f"导出 HTML → {path}")
        return self

    # ──────────────────────────────── 可视化 ───────────────────────────────

    def to_dataviz(
        self,
        chart_type: str,
        x_col: Optional[str] = None,
        y_col: Optional[str] = None,
        series: Optional[List[Dict]] = None,
        title: str = "",
        width: int = 800,
        height: int = 500,
        **kwargs
    ) -> "SQLPipeline":
        """
        生成图表（base64 PNG）

        chart_type: line | bar | clustered_column | pie | donut | scatter | funnel |
                    area | stacked_column | heatmap | treemap 等
        """
        try:
            from charts import ChartFactory
        except ImportError:
            import sys
            skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.insert(0, skill_dir)
            # 尝试从 dataviz skill 加载
            import os as _os
            dataviz_path = os.path.join(os.path.dirname(skill_dir), "sql-dataviz", "charts")
            if _os.path.exists(dataviz_path):
                sys.path.insert(0, dataviz_path)
            from charts import ChartFactory

        factory = ChartFactory()

        # 构建图表数据
        if series:
            data = kwargs.pop("data", None) or {
                "categories": self._current_df[x_col].tolist() if x_col else None,
                "series": series
            }
        elif chart_type in ("line", "area", "smooth_line"):
            data = {
                "categories": self._current_df[x_col].tolist(),
                "series": [{"name": y_col, "data": self._current_df[y_col].tolist()}]
            }
        elif chart_type in ("bar", "clustered_column"):
            data = {
                "categories": self._current_df[x_col].tolist(),
                "series": [{"name": y_col, "data": self._current_df[y_col].tolist()}]
            }
        elif chart_type in ("pie", "donut"):
            data = {
                "labels": self._current_df[x_col].tolist(),
                "values": self._current_df[y_col].tolist()
            }
        elif chart_type == "scatter":
            data = {
                "x": self._current_df[x_col].tolist(),
                "y": self._current_df[y_col].tolist()
            }
        elif chart_type == "funnel":
            data = {
                "stages": self._current_df[x_col].tolist(),
                "values": self._current_df[y_col].tolist()
            }
        else:
            raise ValueError(f"不支持的图表类型: {chart_type}")

        data["title"] = title

        create_fn = getattr(factory, f"create_{chart_type}", None)
        if not create_fn:
            raise ValueError(f"图表工厂没有 create_{chart_type} 方法")

        b64 = create_fn(data)
        self._result.base64_images.append(b64)
        self._result.add_step("viz", f"生成图表 [{chart_type}]: {title}")
        return self

    def to_multi_chart(
        self,
        charts: List[Dict],
        layout: str = "grid",
        cols: int = 2,
        title: str = "看板"
    ) -> "SQLPipeline":
        """
        生成多图表看板（拼接为一张 PNG）

        charts: [
            {"type": "line", "x": "month", "y": "sales", "title": "月度趋势"},
            {"type": "bar", "x": "region", "y": "amount", "title": "区域销售"},
            ...
        ]
        """
        try:
            from charts import ChartFactory
        except ImportError:
            import sys
            skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.insert(0, skill_dir)
            import os as _os
            dataviz_path = os.path.join(os.path.dirname(skill_dir), "sql-dataviz", "charts")
            if _os.path.exists(dataviz_path):
                sys.path.insert(0, dataviz_path)
            from charts import ChartFactory

        factory = ChartFactory()
        rows = (len(charts) + cols - 1) // cols

        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(rows, cols, figsize=(cols * 8, rows * 5))
        axes = axes.flatten() if rows > 1 else [axes]

        for ax, chart in zip(axes, charts):
            chart_type = chart.pop("type")
            x_col = chart.pop("x", None)
            y_col = chart.pop("y", None)
            series = chart.pop("series", None)
            chart_title = chart.pop("title", "")

            if series:
                data = {"categories": self._current_df[x_col].tolist(), "series": series}
            elif chart_type in ("line", "bar"):
                data = {"categories": self._current_df[x_col].tolist(),
                        "series": [{"name": y_col, "data": self._current_df[y_col].tolist()}]}
            elif chart_type in ("pie", "donut"):
                data = {"labels": self._current_df[x_col].tolist(),
                        "values": self._current_df[y_col].tolist()}
            else:
                continue

            data["title"] = chart_title
            create_fn = getattr(factory, f"create_{chart_type}", None)
            if create_fn:
                b64 = create_fn(data)
                import base64, io
                img_data = base64.b64decode(b64)
                from PIL import Image
                img = Image.open(io.BytesIO(img_data))
                ax.imshow(img)
                ax.axis("off")
                ax.set_title(chart_title, fontsize=12, pad=10)

        # 隐藏多余的子图
        for ax in axes[len(charts):]:
            ax.axis("off")

        plt.suptitle(title, fontsize=16, fontweight="bold")
        plt.tight_layout()

        import base64, io
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", dpi=120)
        plt.close()
        b64 = base64.b64encode(buf.getvalue()).decode()
        self._result.base64_images.append(b64)
        self._result.add_step("viz", f"生成多图表看板 [{layout}]: {title}")
        return self

    # ──────────────────────────────── 报告生成 ─────────────────────────────

    def to_report(
        self,
        title: str = "数据分析报告",
        output: str = "html",
        output_path: str = "",
        include_charts: bool = True,
        **kwargs
    ) -> "SQLPipeline":
        """
        生成 HTML/PDF 报告

        整合: 数据表格 + base64 图表 + 统计摘要
        """
        import base64, io
        from datetime import datetime

        # 将 base64 图片转为 data URI
        chart_imgs = ""
        if include_charts and self._result.base64_images:
            for b64 in self._result.base64_images:
                chart_imgs += f'<img src="data:image/png;base64,{b64}" style="max-width:100%;margin:10px 0;">'

        # 数据预览
        df_html = self._current_df.head(100).to_html(
            index=False, classes="data-table", border=0
        )

        # 统计摘要
        stats = self._current_df.describe().to_html(
            classes="stats-table", border=0
        ) if not self._current_df.empty else "<p>无数据</p>"

        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
  .container {{ max-width: 1200px; margin: 0 auto; }}
  h1 {{ color: #0078D4; border-bottom: 3px solid #0078D4; padding-bottom: 10px; }}
  h2 {{ color: #333; margin-top: 30px; }}
  .meta {{ color: #666; font-size: 14px; margin-bottom: 20px; }}
  .section {{ background: white; border-radius: 8px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
  .data-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  .data-table th {{ background: #0078D4; color: white; padding: 10px; text-align: left; }}
  .data-table td {{ padding: 8px 10px; border-bottom: 1px solid #eee; }}
  .data-table tr:nth-child(even) {{ background: #f5f9fc; }}
  .stats-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  .stats-table th {{ background: #50E6FF; padding: 8px; text-align: left; }}
  .stats-table td {{ padding: 6px 8px; border: 1px solid #ddd; }}
  img {{ border-radius: 8px; }}
  .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 40px; }}
</style>
</head>
<body>
<div class="container">
  <h1>{title}</h1>
  <div class="meta">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 数据行数: {len(self._current_df):,} | 列数: {len(self._current_df.columns)}</div>

  <div class="section">
    <h2>📊 数据图表</h2>
    {chart_imgs if chart_imgs else '<p>无图表</p>'}
  </div>

  <div class="section">
    <h2>📋 数据预览（前 100 行）</h2>
    {df_html}
  </div>

  <div class="section">
    <h2>📈 统计摘要</h2>
    {stats}
  </div>

  <div class="footer">
    由 SQL Pipeline 生成 | sql-master skill
  </div>
</div>
</body>
</html>"""

        if output_path:
            self._ensure_output_dir(output_path)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            self._result.export_paths.append(os.path.abspath(output_path))
            self._result.add_step("report", f"生成报告 → {output_path}")
        else:
            # 返回 HTML 字符串
            self._result.add_step("report", "生成报告（内存）")

        self._result.summary = f"Pipeline 完成: {len(self._current_df)} 行, {len(self._result.base64_images)} 张图"
        return self

    # ──────────────────────────────── 工具方法 ─────────────────────────────

    @staticmethod
    def _ensure_output_dir(path: str):
        dir_path = os.path.dirname(path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    @property
    def df(self) -> pd.DataFrame:
        """当前 DataFrame"""
        return self._current_df

    @property
    def result(self) -> PipelineResult:
        """Pipeline 执行结果"""
        return self._result

    def log(self) -> str:
        """打印执行日志"""
        return self._result.log()

    def __repr__(self):
        shape = self._current_df.shape if self._current_df is not None else (0, 0)
        return f"<SQLPipeline source={self._source_type} shape={shape}>"


# ─────────────────────────────────────────────────────────────────────────────
# 便捷入口
# ─────────────────────────────────────────────────────────────────────────────

def from_file(path: str, **kwargs) -> SQLPipeline:
    """从文件创建 Pipeline"""
    return SQLPipeline().from_file(path, **kwargs)


def from_db(dialect: str = "sqlite", database: str = "", **kwargs) -> SQLPipeline:
    """从数据库创建 Pipeline"""
    return SQLPipeline().from_db(dialect=dialect, database=database, **kwargs)


def from_dataframe(df: pd.DataFrame, **kwargs) -> SQLPipeline:
    """从 DataFrame 创建 Pipeline"""
    return SQLPipeline().from_dataframe(df, **kwargs)


if __name__ == "__main__":
    import tempfile

    # 测试完整 Pipeline
    csv_path = tempfile.mktemp(suffix=".csv")
    df = pd.DataFrame({
        "month": ["1月", "2月", "3月", "4月", "5月"],
        "华东": [1200, 1400, 1600, 1800, 2000],
        "华北": [800, 900, 1000, 1100, 1200],
        "华南": [600, 700, 800, 900, 1000],
    })
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    # 测试: 加载 → SQL查询 → 导出多格式 → 生成图表
    p = SQLPipeline()
    p = SQLPipeline()
    p.from_file(csv_path)
    p.query("SELECT * FROM data WHERE month != '1月'")
    p.to_csv(tempfile.mktemp(suffix=".csv"))
    p.to_json(tempfile.mktemp(suffix=".json"))
    p.to_excel(tempfile.mktemp(suffix=".xlsx"))

    print(p.log())

    os.unlink(csv_path)
    print("SQLPipeline test passed")

