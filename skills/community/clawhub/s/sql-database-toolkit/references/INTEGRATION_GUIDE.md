# 三 Skill 协作完整指南

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    数据分析完整流程                          │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  sql-master  │  →   │ sql-dataviz  │  →   │report-gen    │
│              │      │              │      │              │
│ SQL 查询     │      │ 可视化图表   │      │ 报告生成     │
│ 数据获取     │      │ 24 种图表    │      │ 交互组件     │
│ 数据清洗     │      │ Base64 PNG   │      │ HTML/PDF     │
└──────────────┘      └──────────────┘      └──────────────┘
     ↓                      ↓                      ↓
  SQL 结果              图表 Base64            完整报告
  DataFrame             JSON 元数据            HTML 文件
```

## 三个 Skill 的职责

### 1. sql-master（数据层）

**职责：**
- 执行 SQL 查询
- 数据清洗与转换
- 数据聚合与分组
- 性能优化

**输出：**
- DataFrame / 列表
- JSON 格式数据

**示例：**
```python
from sql_master import SQLMaster

sql = SQLMaster()
result = sql.execute_query("""
    SELECT 
        DATE_TRUNC(order_date, MONTH) as month,
        region,
        SUM(sales) as total_sales,
        COUNT(*) as order_count
    FROM orders
    WHERE order_date >= '2026-01-01'
    GROUP BY month, region
    ORDER BY month, region
""")
```

### 2. sql-dataviz（可视化层）

**职责：**
- 将数据转换为图表格式
- 生成 24 种 Power BI 风格图表
- 输出 Base64 PNG
- 支持多种主题

**输入：**
- DataFrame / 列表 / 字典

**输出：**
- Base64 PNG 字符串
- 可直接嵌入 HTML/Markdown

**示例：**
```python
from sql_dataviz.charts import ChartFactory

factory = ChartFactory()
factory.set_theme('powerbi')

# 转换数据格式
data = {
    'categories': [row['month'] for row in result],
    'series': [
        {'name': '北京', 'data': [...]},
        {'name': '上海', 'data': [...]}
    ]
}

# 生成图表
chart_b64 = factory.create_clustered_column(data)
```

### 3. sql-report-generator（报告层）

**职责：**
- 组织图表与内容
- 生成表格、矩阵、切片器
- 导出 HTML/PDF/JSON
- 提供交互功能

**输入：**
- Base64 图表
- 表格数据
- 文本内容

**输出：**
- HTML 报告
- PDF 文件
- JSON 数据

**示例：**
```python
from sql_report_generator.scripts.interactive_components import ReportBuilder

report = ReportBuilder()
report.set_metadata(title='月度销售报告')
report.add_title('销售分析', level=1)
report.add_chart('销售趋势', chart_b64)
report.export_html('report.html')
```

## 完整工作流示例

### 场景：生成月度销售报告

#### 步骤 1：sql-master 查询数据

```python
from sql_master import SQLMaster
import pandas as pd

sql = SQLMaster()

# 查询 1：月度销售总额
monthly_sales = sql.execute_query("""
    SELECT 
        DATE_TRUNC(order_date, MONTH) as month,
        SUM(sales) as total
    FROM orders
    WHERE order_date >= '2026-01-01'
    GROUP BY month
    ORDER BY month
""")

# 查询 2：地区销售对比
regional_sales = sql.execute_query("""
    SELECT 
        region,
        SUM(sales) as total
    FROM orders
    WHERE order_date >= '2026-01-01'
    GROUP BY region
    ORDER BY total DESC
""")

# 查询 3：订单明细
orders = sql.execute_query("""
    SELECT 
        order_id, customer_name, region, sales, order_date
    FROM orders
    WHERE order_date >= '2026-01-01'
    ORDER BY order_date DESC
    LIMIT 100
""")
```

#### 步骤 2：sql-dataviz 生成图表

```python
from sql_dataviz.charts import ChartFactory
import pandas as pd

factory = ChartFactory()
factory.set_theme('powerbi')

# 图表 1：月度趋势
trend_data = {
    'categories': [row['month'].strftime('%Y-%m') for row in monthly_sales],
    'series': [{'name': '销售额', 'data': [row['total'] for row in monthly_sales]}]
}
trend_chart = factory.create_line(trend_data)

# 图表 2：地区对比
region_data = {
    'categories': [row['region'] for row in regional_sales],
    'series': [{'name': '销售额', 'data': [row['total'] for row in regional_sales]}]
}
region_chart = factory.create_clustered_column(region_data)

# 图表 3：地区占比
region_pie_data = {
    'labels': [row['region'] for row in regional_sales],
    'values': [row['total'] for row in regional_sales]
}
region_pie_chart = factory.create_pie(region_pie_data)

# 图表 4：KPI 卡片
kpi_data = {
    'title': '本月销售额',
    'value': f"¥{sum(row['total'] for row in monthly_sales):,.0f}",
    'change': '+15.2%'
}
kpi_chart = factory.create_card(kpi_data)
```

#### 步骤 3：sql-report-generator 生成报告

```python
from sql_report_generator.scripts.interactive_components import (
    ReportBuilder, TableChart, MatrixChart, SlicerComponent
)

# 创建表格
table = TableChart()
table_b64 = table.create({
    'columns': ['订单ID', '客户', '地区', '金额', '日期'],
    'rows': [[row['order_id'], row['customer_name'], row['region'], 
              f"¥{row['sales']}", row['order_date']] for row in orders],
    'title': '订单明细'
})

# 创建切片器
slicer = SlicerComponent()
slicer_b64 = slicer.create({
    'title': '地区筛选',
    'options': ['全部', '北京', '上海', '广州', '深圳'],
    'selected': '全部'
})

# 生成报告
report = ReportBuilder()
report.set_metadata(
    title='月度销售报告',
    author='销售部',
    date='2026-03-26'
)

# 添加内容
report.add_title('月度销售报告', level=1)
report.add_text('本报告汇总了本月的销售业绩和地区分析。')

# 关键指标
report.add_title('关键指标', level=2)
report.add_chart('本月销售额', kpi_chart)

# 趋势分析
report.add_title('趋势分析', level=2)
report.add_chart('月度销售趋势', trend_chart, '销售额呈上升趋势')

# 地区分析
report.add_title('地区分析', level=2)
report.add_chart('地区销售对比', region_chart)
report.add_chart('地区占比', region_pie_chart)

# 明细数据
report.add_title('订单明细', level=2)
report.add_slicer(slicer_b64)
report.add_table('订单列表', table_b64)

# 导出
report.export_html('monthly_sales_report.html')
report.export_json('monthly_sales_report.json')

print("✓ 报告已生成: monthly_sales_report.html")
```

## 数据格式规范

### sql-master 输出格式

```python
# 格式 1：列表字典
[
    {'month': '2026-01', 'total': 100000},
    {'month': '2026-02', 'total': 120000},
    {'month': '2026-03', 'total': 150000}
]

# 格式 2：DataFrame
import pandas as pd
df = pd.DataFrame({
    'month': ['2026-01', '2026-02', '2026-03'],
    'total': [100000, 120000, 150000]
})

# 格式 3：JSON
{
    "data": [
        {"month": "2026-01", "total": 100000},
        {"month": "2026-02", "total": 120000}
    ]
}
```

### sql-dataviz 输入格式

```python
# 对比类图表
{
    'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
    'series': [
        {'name': '销售额', 'data': [100, 150, 120, 200]},
        {'name': '成本', 'data': [60, 80, 70, 100]}
    ]
}

# 占比类图表
{
    'labels': ['北京', '上海', '广州'],
    'values': [35, 30, 35]
}

# 分布类图表
{
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 5, 4, 6],
    'labels': ['A', 'B', 'C', 'D', 'E']
}
```

### sql-dataviz 输出格式

```python
# Base64 PNG 字符串
"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

# 可直接嵌入 HTML
f'<img src="data:image/png;base64,{chart_b64}" />'

# 可直接嵌入 Markdown
f'![chart](data:image/png;base64,{chart_b64})'
```

### sql-report-generator 输入格式

```python
# 图表
chart_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

# 表格
{
    'columns': ['订单ID', '客户', '金额'],
    'rows': [
        ['ORD001', '张三', '¥1,000'],
        ['ORD002', '李四', '¥2,500']
    ],
    'title': '订单列表'
}

# 矩阵
{
    'rows': ['北京', '上海', '广州'],
    'columns': ['Q1', 'Q2', 'Q3', 'Q4'],
    'values': [
        [100, 150, 120, 200],
        [80, 120, 100, 180],
        [60, 90, 80, 140]
    ]
}
```

## 性能优化建议

### 1. 数据聚合（sql-master）

```python
# ✓ 好：在 SQL 中聚合
SELECT DATE_TRUNC(date, MONTH) as month, SUM(sales) as total
FROM orders
GROUP BY month

# ✗ 差：在 Python 中聚合
df = pd.read_sql("SELECT * FROM orders", conn)
df.groupby(pd.Grouper(key='date', freq='M')).sum()
```

### 2. 数据采样（sql-dataviz）

```python
# 处理大数据集时采样
import pandas as pd

df = pd.read_sql(query, conn)
if len(df) > 100000:
    df = df.sample(n=10000)  # 采样 10000 行

chart = factory.create_scatter({
    'x': df['x'].tolist(),
    'y': df['y'].tolist()
})
```

### 3. 缓存机制（sql-report-generator）

```python
import hashlib
import json

def get_report_cached(config, cache_dir='./cache'):
    key = hashlib.md5(json.dumps(config).encode()).hexdigest()
    cache_file = f"{cache_dir}/report_{key}.html"
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return f.read()
    
    # 生成新报告...
    report = ReportBuilder()
    # ...
    html = report._generate_html()
    
    # 保存缓存
    with open(cache_file, 'w') as f:
        f.write(html)
    
    return html
```

## 错误处理

```python
from sql_master import SQLMaster
from sql_dataviz.charts import ChartFactory
from sql_report_generator.scripts.interactive_components import ReportBuilder

try:
    # 1. 查询数据
    sql = SQLMaster()
    result = sql.execute_query(query)
    
    if not result:
        raise ValueError("查询结果为空")
    
    # 2. 生成图表
    factory = ChartFactory()
    chart = factory.create_line(data)
    
    if not chart:
        raise ValueError("图表生成失败")
    
    # 3. 生成报告
    report = ReportBuilder()
    report.add_chart('标题', chart)
    report.export_html('report.html')
    
except ValueError as e:
    print(f"数据错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
    import traceback
    traceback.print_exc()
```

## 常见问题

### Q: 如何处理大数据集？

A: 使用聚合和采样：

```python
# 在 SQL 中聚合
result = sql.execute_query("""
    SELECT DATE_TRUNC(date, DAY) as day, SUM(sales) as total
    FROM orders
    GROUP BY day
""")

# 或在 Python 中采样
import pandas as pd
df = pd.read_sql(query, conn)
df_sample = df.sample(n=min(10000, len(df)))
```

### Q: 如何自定义图表样式？

A: 使用 ChartConfig：

```python
from sql_dataviz.charts import ChartFactory, ChartConfig, Theme

config = ChartConfig(
    width=1600,
    height=800,
    theme=Theme.ALIBABA,
    font_size=13,
    title_size=18
)

factory = ChartFactory(config)
chart = factory.create_line(data)
```

### Q: 如何导出为 PDF？

A: 使用 sql-report-generator：

```python
report = ReportBuilder()
# ... 添加内容 ...
report.export_pdf('report.pdf')  # 需要安装 reportlab
```

## 总结

| 阶段 | Skill | 输入 | 输出 | 示例 |
|------|-------|------|------|------|
| 数据 | sql-master | SQL 查询 | DataFrame/列表 | `execute_query()` |
| 可视化 | sql-dataviz | DataFrame/字典 | Base64 PNG | `create_line()` |
| 报告 | sql-report-generator | Base64 图表 | HTML/PDF | `export_html()` |

通过三个 Skill 的协作，可以快速构建完整的数据分析流程，从 SQL 查询到最终报告生成。
