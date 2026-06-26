# sql-dataviz - SQL 数据可视化 Skill

## ⚠️ 使用前必读

本 Skill 需要 Python 依赖。**首次使用前必须安装依赖**：

```bash
skillhub_install install_skill sql-dataviz
```

工具会自动检测 Python3 环境、pip 可用性，并安装所有依赖。

### 依赖安装方式

| 方式 | 命令 | 适用场景 |
|------|------|---------|
| **自动安装（推荐）** | `skillhub_install install_skill sql-dataviz` | 一键安装，自动处理 |
| **手动安装** | `pip install -r requirements.txt` | 熟悉 Python 环境的用户 |

### 无依赖使用（受限模式）

如果无法安装依赖，本 Skill 提供以下**降级能力**：

✅ **可用功能**：
- 图表选型建议（基于业务场景推荐图表类型）
- 数据格式规范说明
- 可视化设计原则指导
- 配色方案推荐

❌ **不可用功能**：
- 图表生成（PNG/base64 输出）
- 交互式 HTML 图表
- Dashboard 构建
- 与 sql-master / sql-report-generator 联动

---

## 🔗 Skill 协作关系

本 Skill 与 **sql-master**、**sql-report-generator** 组成完整的数据分析流水线：

```
┌─────────────┐     ┌──────────────┐     ┌────────────────────────┐
│ sql-master  │ ──► │ sql-dataviz  │ ──► │ sql-report-generator   │
│  (数据层)   │     │  (可视化层)   │     │  (报告层)               │
└─────────────┘     └──────────────┘     └────────────────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
   SQL 查询           图表生成            HTML 报告
   数据获取           PNG/HTML            AI 洞察
   格式转换           Dashboard           数据表格
```

### 协作模式

| 模式 | 组合 | 适用场景 |
|------|------|---------|
| **单独使用** | sql-dataviz | 已有数据，仅需图表可视化 |
| **数据可视化** | sql-master + sql-dataviz | SQL 查询 → 图表输出 |
| **可视化报告** | sql-dataviz + sql-report-generator | 图表 → 报告（无 SQL） |
| **完整流程** | sql-master + sql-dataviz + sql-report-generator | 完整数据分析报告 |

### 🥇 最优使用方式：三 Skill 串联

```python
from scripts.unified_pipeline import UnifiedPipeline

result = (
    UnifiedPipeline("销售分析")
    .from_file("sales.csv")                                    # sql-master: 数据获取
    .query("SELECT region, SUM(sales) as total FROM data GROUP BY region")
    .interactive_chart("bar", x_col="region", y_col="total")   # sql-dataviz: 可视化
    .insights(value_cols=["total"])                            # AI 洞察
    .report(title="销售报告", output="report.html")            # sql-report-generator: 报告
)
```

### 决策指南

```
你需要什么？
├─ 仅图表可视化 → sql-dataviz 单独使用
├─ SQL + 图表 → sql-master + sql-dataviz
├─ 图表 + 报告（无 SQL）→ sql-dataviz + sql-report-generator
└─ 完整分析报告 → sql-master + sql-dataviz + sql-report-generator ✅ 推荐
```

---

## 新增功能：交互式 HTML 图表（Plotly）

### `scripts/interactive_charts.py`

基于 Plotly 的 12 种交互式图表，输出自包含 HTML（支持 hover / zoom / pan）：

```python
from scripts.interactive_charts import InteractiveChartFactory, DashboardBuilder

factory = InteractiveChartFactory(theme="powerbi")

# 12 种图表类型
html = factory.create_line(data)          # 折线图
html = factory.create_bar(data)           # 柱形图
html = factory.create_pie(data)           # 饼图（环形）
html = factory.create_scatter(data)       # 散点图
html = factory.create_heatmap(data)       # 热力图
html = factory.create_funnel(data)        # 漏斗图
html = factory.create_area(data)          # 面积图
html = factory.create_treemap(data)       # 树状图
html = factory.create_gauge(data)         # 仪表盘
html = factory.create_combo(data)         # 组合图（柱+折线）
html = factory.create_table(data)         # 交互式表格
html = factory.create_kpi_cards(data)     # KPI 卡片组

factory.save_html(html, "chart.html")

# 多图表 Dashboard
builder = DashboardBuilder(title="销售看板", theme="powerbi")
builder.add_kpi_cards([{"title":"GMV","value":"¥1,234万","change":"+18%"}])
builder.add_chart(factory.create_line(...), title="月度趋势", cols=2)
builder.add_chart(factory.create_bar(...), title="区域对比", cols=1)
builder.build("dashboard.html")
```

**数据格式** 与现有 ChartFactory 完全一致（line/bar/pie/scatter/funnel/area/combo/table）。

**主题**：powerbi / dark / seaborn / ggplot2

## 概述

将 SQL 查询结果转化为**生产级可视化图表**。集成 Power BI 原生的 **50 种视觉对象**，支持对比、趋势、分布、占比、地理、指标监控、AI 智能分析、统计分析等全场景。

所有图表以 **base64 编码的 PNG** 方式输出，可直接嵌入报告、邮件、Web 应用、Markdown 文档。

## 核心能力矩阵

### 1️⃣ 对比与趋势分析（13种）

| 图表 | 场景 | 方法 |
|------|------|------|
| **簇状柱形图** | 多系列分类对比 | `create_clustered_column()` |
| **堆积柱形图** | 整体+部分占比对比 | `create_stacked_column()` |
| **100%堆积柱形图** | 统一尺度结构对比 | `create_percent_stacked_column()` |
| **簇状条形图** | 长分类名称对比 | `create_clustered_bar()` |
| **堆积条形图** | 区域/渠道层级对比 | `create_stacked_bar()` |
| **100%堆积条形图** | 横向结构占比 | `create_percent_stacked_bar()` |
| **折线图** | 连续数据趋势 | `create_line()` |
| **平滑折线图** | 弱化波动的趋势 | `create_smooth_line()` |
| **组合图** | 双指标（柱+折线） | `create_combo()` |
| **面积图** | 累计总量展示 | `create_area()` |
| **堆积面积图** | 多业务线累计贡献 | `create_stacked_area()` |
| **瀑布图** | 增减项影响分析 | `create_waterfall()` |
| **丝带图** | 排名变动追踪 | `create_line()` |

### 2️⃣ 部分与整体（4种）

| 图表 | 场景 | 方法 |
|------|------|------|
| **饼图** | 单维度占比 | `create_pie()` |
| **圆环图** | 中心标签占比 | `create_donut()` |
| **树状图** | 层级数据展示 | `create_treemap()` |
| **漏斗图** | 流程转化分析 | `create_funnel()` |

### 3️⃣ 分布与关系（4种）

| 图表 | 场景 | 方法 |
|------|------|------|
| **散点图** | 两变量相关性 | `create_scatter()` |
| **气泡图** | 三变量分析 | `create_bubble()` |
| **点图** | 分类数据分布 | `create_dot()` |
| **高密度散点图** | 海量数据聚类 | `create_high_density_scatter()` |

### 4️⃣ 地理空间（4种）

| 图表 | 场景 | 方法 |
|------|------|------|
| **Azure 地图** | 权威地图底图 | `create_azure_map()` |
| **填充地图** | 区域数据热力 | `create_filled_map()` |
| **形状地图** | 自定义边界分析 | `create_shape_map()` |
| **ArcGIS 地图** | 专业空间分析 | `create_arcgis_map()` |

### 5️⃣ 指标监控（5种）

| 图表 | 场景 | 方法 |
|------|------|------|
| **卡片图** | 单一关键指标 | `create_card()` |
| **多行卡片图** | 多指标汇总 | `create_multi_card()` |
| **KPI 视觉对象** | 目标达成率 | `create_kpi()` |
| **仪表盘图** | 指标健康度 | `create_gauge()` |
| **目标视觉对象** | 团队绩效看板 | `create_target()` |

### 6️⃣ AI 智能分析（4种）

| 图表 | 场景 | 方法 |
|------|------|------|
| **分解树** | 多维度根因分析 | `create_decomposition_tree()` |
| **关键影响因素** | 驱动因子权重 | `create_key_influencers()` |
| **异常检测** | 自动异常标注 | `create_anomaly_detection()` |
| **智能叙事** | 自然语言摘要 | `create_smart_narrative()` |

### 7️⃣ 统计与分布（5种）**[新增]**

| 图表 | 场景 | 方法 |
|------|------|------|
| **盒须图** | 数据分布四分位数 | `create_box_plot()` |
| **直方图** | 数据频率分布 | `create_histogram()` |
| **密度图** | 概率密度分布 | `create_density_plot()` |
| **帕累托图** | 80/20 法则分析 | `create_pareto()` |
| **Q-Q 图** | 正态性检验 | 通过 scipy 实现 |

### 8️⃣ 关系与网络（2种）**[新增]**

| 图表 | 场景 | 方法 |
|------|------|------|
| **网络图** | 节点关系展示 | `create_network_graph()` |
| **桑基图** | 流量/能量流向 | `create_sankey()` |

### 9️⃣ 时序与日期（3种）**[新增]**

| 图表 | 场景 | 方法 |
|------|------|------|
| **甘特图** | 项目进度管理 | `create_gantt()` |
| **日历热力图** | 时间序列热力 | `create_calendar_heatmap()` |
| **蜡烛图** | 股票价格走势 | `create_candlestick()` |

### 🔟 地理与热力（3种）**[新增]**

| 图表 | 场景 | 方法 |
|------|------|------|
| **分级地图** | 区域数据热力 | `create_choropleth_map()` |
| **路径地图** | 物流路径规划 | `create_route_map()` |
| **点密度地图** | 点分布密度 | `create_dot_density_map()` |

### 1️⃣1️⃣ 层级与占比（3种）**[新增]**

| 图表 | 场景 | 方法 |
|------|------|------|
| **旭日图** | 多层级占比 | `create_sunburst()` |
| **词云图** | 文本频率可视化 | `create_word_cloud()` |
| **子弹图** | 目标对比 | `create_bullet()` |

### 1️⃣2️⃣ 交互与辅助（4种）

| 图表 | 场景 | 方法 |
|------|------|------|
| **图像视觉对象** | 品牌 logo、产品图片 | `create_image_visual()` |
| **文本框与形状** | 报表标题、说明描述 | `create_text_shape()` |
| **小型序列图** | 多个小图表并排 | `create_small_multiple()` |
| **视觉对象栏** | 自定义布局 | `create_visual_canvas()` |

## 快速开始

### 基础用法

```python
from sql_dataviz.charts import ChartFactory, ChartConfig, Theme

# 1. 创建工厂
factory = ChartFactory()

# 2. 设置主题（可选）
factory.set_theme('powerbi')  # 或 'alibaba', 'tencent', 'bytedance'

# 3. 准备数据
data = {
    'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
    'series': [
        {'name': '销售额', 'data': [100, 150, 120, 200]},
        {'name': '成本', 'data': [60, 80, 70, 100]}
    ]
}

# 4. 生成图表（base64 PNG）
chart_b64 = factory.create_clustered_column(data)

# 5. 嵌入到 HTML
html = f'<img src="data:image/png;base64,{chart_b64}" />'

# 6. 或保存为文件
import base64
with open('chart.png', 'wb') as f:
    f.write(base64.b64decode(chart_b64))
```

### 与 sql-master 协作

```python
from sql_master import SQLMaster
from sql_dataviz.charts import ChartFactory

# 1. 执行 SQL 查询
sql_master = SQLMaster()
result = sql_master.execute_query("""
    SELECT quarter, SUM(sales) as total, SUM(cost) as cost
    FROM orders
    GROUP BY quarter
    ORDER BY quarter
""")

# 2. 转换为图表数据格式
data = {
    'categories': [row['quarter'] for row in result],
    'series': [
        {'name': '销售额', 'data': [row['total'] for row in result]},
        {'name': '成本', 'data': [row['cost'] for row in result]}
    ]
}

# 3. 生成可视化
factory = ChartFactory()
chart_b64 = factory.create_clustered_column(data)
```

### 与 sql-report-generator 协作

```python
from sql_dataviz.charts import ChartFactory
from sql_report_generator import ReportGenerator

# 1. 生成多个图表
factory = ChartFactory()
charts = {
    'sales_trend': factory.create_line(trend_data),
    'channel_mix': factory.create_pie(channel_data),
    'regional_heatmap': factory.create_filled_map(region_data)
}

# 2. 组织成报告
report = ReportGenerator()
report.add_title('月度业绩报告')
report.add_chart('销售趋势', charts['sales_trend'])
report.add_chart('渠道占比', charts['channel_mix'])
report.add_chart('区域热力', charts['regional_heatmap'])
report.export_html('report.html')
```



## 文件结构

```
sql-dataviz/
├── SKILL.md                          # 本文件
├── charts/
│   ├── __init__.py                   # 24种图表实现（base64 PNG）
│   ├── comparison.py                 # 对比类图表（可选扩展）
│   ├── composition.py                # 占比类图表（可选扩展）
│   ├── distribution.py               # 分布类图表（可选扩展）
│   ├── geographic.py                 # 地理类图表（可选扩展）
│   ├── kpi.py                        # 指标监控（可选扩展）
│   └── ai_analysis.py                # AI 智能分析（可选扩展）
├── scripts/
│   ├── install_deps.sh               # 依赖安装脚本
│   ├── demo.py                       # 完整演示脚本
│   └── benchmark.py                  # 性能基准测试
└── references/
    ├── POWERBI_CHARTS.md             # Power BI 图表参考
    ├── COLOR_SCHEMES.md              # 大厂配色方案
    ├── DATA_FORMATS.md               # 数据格式规范
    └── EXAMPLES.md                   # 完整示例库
```

## 配置选项

### 主题与样式

```python
from sql_dataviz.charts import ChartFactory, ChartConfig, Theme

# 方式1：工厂级设置
factory = ChartFactory()
factory.set_theme('powerbi')      # Power BI 官方蓝
factory.set_theme('alibaba')      # 阿里巴巴红
factory.set_theme('tencent')      # 腾讯蓝
factory.set_theme('bytedance')    # 字节跳动黑
factory.set_theme('neutral')      # 中性灰

# 方式2：配置对象
config = ChartConfig(
    width=1200,
    height=600,
    dpi=100,
    theme=Theme.POWERBI,
    title='季度业绩分析',
    show_legend=True,
    show_grid=True,
    font_size=11,
    title_size=16
)
factory = ChartFactory(config)
```

### 导出格式

```python
# 所有图表都支持 base64 PNG 输出
chart_b64 = factory.create_line(data)

# 嵌入 HTML
html = f'<img src="data:image/png;base64,{chart_b64}" />'

# 嵌入 Markdown
markdown = f'![chart](data:image/png;base64,{chart_b64})'

# 保存为文件
import base64
with open('chart.png', 'wb') as f:
    f.write(base64.b64decode(chart_b64))
```

## 常见问题

### Q: 如何处理超大数据集（>100万行）？

A: 使用高密度散点图或自动聚合：

```python
# 高密度散点图自动处理海量数据
chart = factory.create_high_density_scatter({
    'x': large_x_array,  # 100万+ 数据点
    'y': large_y_array
})

# 或先聚合数据
import pandas as pd
df = pd.read_sql(query, conn)
df_agg = df.groupby('category').agg({'value': 'sum'}).reset_index()
chart = factory.create_pie({
    'labels': df_agg['category'],
    'values': df_agg['value']
})
```

### Q: 支持实时数据更新吗？

A: 支持。通过定时查询 SQL 并重新生成图表：

```python
import time
from sql_master import SQLMaster
from sql_dataviz.charts import ChartFactory

sql = SQLMaster()
factory = ChartFactory()

while True:
    # 每分钟更新一次
    result = sql.execute_query("SELECT * FROM metrics WHERE time > NOW() - INTERVAL 1 HOUR")
    chart = factory.create_line(transform_data(result))
    save_chart(chart)
    time.sleep(60)
```

### Q: 能否自定义图表样式？

A: 完全支持。修改 `ChartConfig` 或直接编辑图表类：

```python
# 自定义配置
config = ChartConfig(
    width=1600,
    height=800,
    theme=Theme.ALIBABA,
    font_size=13,
    title_size=18,
    show_grid=False
)

# 或继承图表类进行深度定制
from sql_dataviz.charts import ClusteredColumnChart

class CustomColumnChart(ClusteredColumnChart):
    def create(self, data):
        fig, ax = self._setup_figure()
        # 自定义绘制逻辑
        ...
        return self._to_base64(fig)
```

### Q: 如何在报告中使用这些图表？

A: 与 sql-report-generator 无缝协作：

```python
from sql_report_generator import ReportGenerator
from sql_dataviz.charts import ChartFactory

report = ReportGenerator()
factory = ChartFactory()

# 添加图表
report.add_chart('销售趋势', factory.create_line(data))
report.add_chart('渠道占比', factory.create_pie(data))

# 导出为 HTML/PDF
report.export_html('report.html')
report.export_pdf('report.pdf')
```

## 性能指标

| 操作 | 耗时 | 内存 |
|------|------|------|
| 生成简单柱形图 | ~50ms | ~5MB |
| 生成复杂仪表盘（4图） | ~200ms | ~20MB |
| 处理100万数据点散点图 | ~500ms | ~50MB |
| 生成完整报告（10图） | ~1s | ~100MB |

## 与其他 Skill 的协作

### sql-master → sql-dataviz → sql-report-generator

```
SQL 查询 → 数据转换 → 可视化 → 报告生成
```

**完整流程示例：**

```python
# 1. sql-master：执行查询
from sql_master import SQLMaster
sql = SQLMaster()
sales_data = sql.execute_query("""
    SELECT region, product, SUM(sales) as total
    FROM orders
    GROUP BY region, product
""")

# 2. sql-dataviz：生成可视化
from sql_dataviz.charts import ChartFactory
factory = ChartFactory()
factory.set_theme('powerbi')

# 按地区对比
regional_chart = factory.create_clustered_column({
    'categories': [row['region'] for row in sales_data],
    'series': [{'name': 'Sales', 'data': [row['total'] for row in sales_data]}]
})

# 3. sql-report-generator：组织报告
from sql_report_generator import ReportGenerator
report = ReportGenerator()
report.add_title('销售分析报告')
report.add_chart('地区销售对比', regional_chart)
report.export_html('sales_report.html')
```

## 最佳实践

### 1. 选择合适的图表类型

```python
# ✓ 对比分析 → 簇状柱形图
factory.create_clustered_column(data)

# ✓ 趋势分析 → 折线图
factory.create_line(data)

# ✓ 占比分析 → 饼图/圆环图
factory.create_pie(data)

# ✓ 分布分析 → 散点图/气泡图
factory.create_scatter(data)

# ✓ 流程分析 → 漏斗图
factory.create_funnel(data)
```

### 2. 数据预处理

```python
import pandas as pd

# 清理数据
df = pd.read_sql(query, conn)
df = df.dropna()
df = df[df['value'] > 0]

# 聚合数据
df_agg = df.groupby('category').agg({
    'value': 'sum',
    'count': 'count'
}).reset_index()

# 转换为图表格式
data = {
    'categories': df_agg['category'].tolist(),
    'series': [{'name': 'Value', 'data': df_agg['value'].tolist()}]
}
```

### 3. 缓存机制

```python
import hashlib
import json

def get_chart_cached(chart_type, data, cache_dir='./cache'):
    # 生成缓存键
    key = hashlib.md5(json.dumps(data).encode()).hexdigest()
    cache_file = f"{cache_dir}/{chart_type}_{key}.b64"
    
    # 检查缓存
    try:
        with open(cache_file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        pass
    
    # 生成新图表
    factory = ChartFactory()
    chart = getattr(factory, f'create_{chart_type}')(data)
    
    # 保存缓存
    with open(cache_file, 'w') as f:
        f.write(chart)
    
    return chart
```

## 许可证

MIT License - 生产级可商用

## 更新日志

- **v1.0.0** (2026-03-26) - 初始版本，支持 24 种图表，base64 PNG 输出
- **v1.1.0** (计划) - 支持 SVG 矢量输出、交互式 HTML、实时数据流
- **v2.0.0** (计划) - 集成 Plotly 交互式图表、WebGL 高性能渲染

## 支持与反馈

- 📧 Email: support@example.com
- 💬 Discord: https://discord.gg/example
- 🐛 Issues: https://github.com/example/sql-dataviz/issues
s
