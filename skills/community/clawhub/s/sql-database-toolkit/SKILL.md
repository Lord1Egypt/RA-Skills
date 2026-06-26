# SQL Database Toolkit

_全链路 SQL 数据分析工具包：数据连接 → SQL 查询 → 数据可视化 → AI 洞察 → 报告生成_

## 概述

SQL Database Toolkit 是 sql-master、sql-dataviz、sql-report-generator 三大 Skill 的统一整合版本，提供端到端的 SQL 数据分析能力。

**核心能力：**
- **数据连接层**：支持 SQLite/MySQL/PostgreSQL/SQL Server/ClickHouse 等多种数据库，以及 CSV/Excel/JSON/Parquet 等本地文件格式
- **SQL 查询执行**：自然语言转 SQL、SQL 执行与优化、查询结果分析
- **数据可视化**：24+ 种静态图表（PNG base64）+ 12 种交互式图表（HTML），支持 Power BI 风格配色
- **AI 洞察**：基于统计的自动异常检测、趋势分析、相关性分析、TOP N 排名等
- **报告生成**：完整 HTML 报告、KPI 仪表盘、行业模板库（90+ 模板）

## 触发条件

当用户提及以下关键词时触发：
- SQL 查询、执行、优化
- 数据库连接（MySQL/PostgreSQL/SQLite 等）
- 数据可视化、图表生成（折线图/柱状图/饼图/热力图等）
- 报告生成、仪表盘、数据看板
- 数据分析、洞察、异常检测
- 文件数据处理（CSV/Excel 导入导出）

## 安装依赖

```bash
pip install -r requirements.txt
```

**核心依赖：**
- pandas, numpy - 数据处理
- sqlalchemy, pymysql, psycopg2-binary - 数据库连接
- matplotlib, seaborn, plotly - 可视化
- scipy - 统计分析
- jinja2 - 模板引擎

## 快速开始

### 1. 一键端到端分析

```python
from unified_pipeline import analyze_file

# 文件 → SQL → 图表 → 洞察 → 报告
result = analyze_file(
    "sales.csv",
    sql="SELECT region, SUM(sales) as total FROM data GROUP BY region",
    charts=[{"type":"bar","x":"region","y":"total","title":"区域销售"}],
    output="report.html"
)
print(result.log())
```

### 2. 数据库查询

```python
from database_connector import DatabaseConnector

# 连接 MySQL
conn = DatabaseConnector(
    dialect="mysql+pymysql",
    host="localhost", port=3306,
    username="root", password="xxx",
    database="sales_db"
)
result = conn.execute("SELECT * FROM orders WHERE amount > 1000")
print(result.df)
```

### 3. 生成交互式图表

```python
from interactive_charts import InteractiveChartFactory

factory = InteractiveChartFactory(theme="powerbi")
html = factory.create_line({
    "categories": ["1月","2月","3月"],
    "series": [{"name":"销售额","data":[100,120,150]}]
})
factory.save_html(html, "chart.html")
```

### 4. AI 自动洞察

```python
from ai_insights import quick_insights

report = quick_insights(df, date_col="date", value_cols=["sales","profit"])
for insight in report.insights:
    print(f"{insight.title}: {insight.description}")
```

## 模块索引

### 数据连接层

| 模块 | 功能 |
|------|------|
| `database_connector.py` | 数据库连接（支持 6+ 种数据库） |
| `file_connector.py` | 本地文件加载（CSV/Excel/JSON/Parquet 等） |
| `pipeline.py` | SQL Pipeline 编排器 |

### 可视化层

| 模块 | 功能 |
|------|------|
| `charts.py` | 静态图表工厂（24+ 种图表，PNG base64） |
| `interactive_charts.py` | 交互式图表工厂（12 种图表，HTML）+ DashboardBuilder |

### 报告层

| 模块 | 功能 |
|------|------|
| `ai_insights.py` | AI 自动洞察生成器 |
| `dashboard_templates.py` | 行业看板模板库（90+ 模板） |
| `report_generator.py` | 报告生成器（表格/矩阵/切片器） |

### 统一入口

| 模块 | 功能 |
|------|------|
| `unified_pipeline.py` | 端到端统一 Pipeline（推荐） |
| `__init__.py` | 统一导出所有核心类 |

## 使用示例

### 示例 1：完整分析流程

```python
from unified_pipeline import UnifiedPipeline

# 创建 Pipeline
p = UnifiedPipeline("销售分析").set_theme("powerbi")

# 加载数据
p.from_file("sales.csv")

# SQL 查询
p.query("SELECT region, SUM(amount) as total FROM data GROUP BY region")

# 生成交互式图表
p.interactive_chart("bar", x_col="region", y_col="total", title="区域销售")
p.interactive_chart("pie", x_col="region", y_col="total", title="区域占比")

# AI 洞察
p.insights(value_cols=["total"])

# 生成完整报告
p.report(title="销售分析报告", output="report.html")

# 打印日志
print(p.log())
```

### 示例 2：数据库 → 可视化

```python
from database_connector import DatabaseConnector
from interactive_charts import InteractiveChartFactory

# 查询数据
conn = DatabaseConnector(dialect="sqlite", database="sales.db")
df = conn.execute("SELECT month, sales FROM monthly_sales").df

# 生成图表
factory = InteractiveChartFactory()
html = factory.create_line({
    "categories": df["month"].tolist(),
    "series": [{"name": "销售额", "data": df["sales"].tolist()}]
}, title="月度销售趋势")
factory.save_html(html, "trend.html")
```

### 示例 3：构建 Dashboard

```python
from interactive_charts import DashboardBuilder, InteractiveChartFactory

builder = DashboardBuilder(title="销售看板", theme="powerbi")

# KPI 卡片
builder.add_kpi_cards([
    {"title": "GMV", "value": "¥1,234万", "change": "+18%"},
    {"title": "订单量", "value": "45,678", "change": "+12%"},
])

# 添加图表
factory = InteractiveChartFactory()
line_html = factory.create_line({...})
builder.add_chart(line_html, title="趋势", cols=2)

# 生成
builder.build("dashboard.html")
```

### 示例 4：使用行业模板

```python
from dashboard_templates import get_template

# 获取电商概览模板
template = get_template("ecommerce_overview")

# 根据模板配置生成图表
# template.charts 包含所有图表规格
```

## 配置与主题

### 配色主题

```python
from charts import Theme

# 支持的主题：POWERBI, ALIBABA, TENCENT, BYTEDANCE, NEUTRAL
factory = ChartFactory()
factory.set_theme("powerbi")
```

### 图表类型

**静态图表（charts.py）：**
- 对比分析：clustered_column, stacked_column, bar, line, area, waterfall
- 占比分析：pie, donut, treemap, funnel
- 分布分析：scatter, bubble, box_plot, histogram
- 指标监控：card, kpi, gauge, target
- 高级图表：heatmap, gantt, candlestick, sankey, word_cloud

**交互式图表（interactive_charts.py）：**
- line, bar, pie, scatter, heatmap, funnel, area, treemap, gauge, combo, table, kpi_cards

## 配置文件

- `requirements.txt` - Python 依赖
- `references/` - 参考文档（SQL 优化、图表选择、模板使用等）
- `templates/` - 行业报告模板（90+ 个）

## 注意事项

1. **中文字体**：Windows 环境自动使用 Microsoft YaHei，其他系统需确保已安装中文字体
2. **数据库驱动**：首次使用 MySQL/PostgreSQL 等需要安装对应驱动（pymysql/psycopg2）
3. **Plotly CDN**：交互式图表默认使用 CDN，如需离线使用可替换为本地路径

## 版本

v2.0.0 - 合并版（基于 sql-master + sql-dataviz + sql-report-generator）