# sql-dataviz - SQL 数据可视化 Skill

## 概述

将 SQL 查询结果转化为**生产级可视化图表**。集成 Power BI 原生的 24+ 种视觉对象，支持对比、趋势、分布、占比、地理、指标监控、AI 智能分析等全场景。

所有图表以 **base64 编码的 PNG/SVG** 方式输出，可直接嵌入报告、邮件、Web 应用。

## 核心能力

### 1. 对比与趋势分析（8种）
- **簇状柱形图** - 多系列分类对比
- **堆积柱形图** - 整体+部分占比对比
- **100%堆积柱形图** - 统一尺度结构对比
- **簇状条形图** - 长分类名称对比
- **堆积条形图** - 区域/渠道层级对比
- **100%堆积条形图** - 横向结构占比
- **折线图** - 连续数据趋势
- **平滑折线图** - 弱化波动的趋势

### 2. 高级趋势（5种）
- **组合图** - 双指标（柱+折线）
- **面积图** - 累计总量展示
- **堆积面积图** - 多系列累计贡献
- **瀑布图** - 增减项影响分析
- **丝带图** - 排名变动追踪

### 3. 部分与整体（4种）
- **饼图** - 单维度占比
- **圆环图** - 中心标签占比
- **树状图** - 层级数据展示
- **漏斗图** - 流程转化分析

### 4. 分布与关系（4种）
- **散点图** - 两变量相关性
- **气泡图** - 三变量分析
- **点图** - 分类数据分布
- **高密度散点图** - 海量数据聚类

### 5. 地理空间（3种）
- **填充地图** - 区域数据热力
- **形状地图** - 自定义边界分析
- **ArcGIS 地图** - 专业空间分析

### 6. 指标监控（3种）
- **卡片图** - 单一关键指标
- **KPI 视觉对象** - 目标达成率
- **仪表盘图** - 指标健康度

### 7. AI 智能分析（4种）
- **分解树** - 多维度根因分析
- **关键影响因素** - 驱动因子权重
- **异常检测** - 自动异常标注
- **智能叙事** - 自然语言摘要

## 使用方式

### 基础用法

```python
from sql_dataviz import ChartFactory

# 创建图表工厂
factory = ChartFactory()

# 从 SQL 结果生成图表
data = {
    'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
    'series': [
        {'name': '销售额', 'data': [100, 150, 120, 200]},
        {'name': '成本', 'data': [60, 80, 70, 100]}
    ]
}

# 生成簇状柱形图（base64）
chart_b64 = factory.create_clustered_column(data)

# 输出为 HTML 可嵌入
html = f'<img src="data:image/png;base64,{chart_b64}" />'
```

### 高级用法 - 组合分析

```python
# 多图表联动
dashboard = factory.create_dashboard({
    'title': '季度业绩分析',
    'charts': [
        {'type': 'clustered_column', 'data': sales_data, 'position': (0, 0)},
        {'type': 'pie', 'data': channel_data, 'position': (1, 0)},
        {'type': 'line', 'data': trend_data, 'position': (0, 1)},
        {'type': 'heatmap', 'data': region_data, 'position': (1, 1)}
    ]
})
```

## 依赖安装

### 自动安装（推荐）

```bash
# 使用 SkillHub 一键安装
skillhub_install install_skill sql-dataviz
```

### 手动安装

```bash
# 1. 安装 Python 依赖
pip install matplotlib seaborn plotly pandas numpy

# 2. 安装可选的地理数据库
pip install geopandas shapely

# 3. 验证安装
python -c "import matplotlib; print(matplotlib.__version__)"
```

## 文件结构

```
sql-dataviz/
├── SKILL.md                          # 本文件
├── charts/
│   ├── __init__.py
│   ├── comparison.py                 # 对比类图表
│   ├── trend.py                      # 趋势类图表
│   ├── composition.py                # 占比类图表
│   ├── distribution.py               # 分布类图表
│   ├── geographic.py                 # 地理类图表
│   ├── kpi.py                        # 指标监控
│   ├── ai_analysis.py                # AI 智能分析
│   └── base.py                       # 基类与工具函数
├── scripts/
│   ├── install_deps.sh               # 依赖安装脚本
│   └── demo.py                       # 演示脚本
└── references/
    ├── POWERBI_CHARTS.md             # Power BI 图表参考
    └── COLOR_SCHEMES.md              # 大厂配色方案
```

## 配置选项

### 主题与样式

```python
# 内置主题
factory.set_theme('powerbi')      # Power BI 官方配色
factory.set_theme('alibaba')      # 阿里巴巴配色
factory.set_theme('tencent')      # 腾讯配色
factory.set_theme('bytedance')    # 字节跳动配色
```

### 导出格式

```python
# 支持多种输出格式
chart_b64 = factory.export_base64()    # Base64 PNG
chart_svg = factory.export_svg()       # SVG 矢量
chart_html = factory.export_html()     # 交互式 HTML
```

## 与其他 Skill 的协作

### 与 sql-master 协作

```python
# sql-master 提供 SQL 查询结果
query_result = sql_master.execute_query(
    "SELECT region, SUM(sales) as total FROM orders GROUP BY region"
)

# sql-dataviz 进行可视化
chart = dataviz.create_pie(query_result)
```

### 与 sql-report-generator 协作

```python
# sql-dataviz 生成图表
charts = dataviz.create_dashboard(data)

# sql-report-generator 组织成报告
report = sql_report_generator.create_report({
    'title': '月度业绩报告',
    'charts': charts,
    'tables': tables
})
```

## 性能优化

- **大数据集**：自动采样 + 聚合，保留关键信息
- **缓存机制**：相同查询结果缓存 1 小时
- **异步渲染**：支持后台生成，前台异步加载
- **流式输出**：支持分页报表流式生成

## 常见问题

**Q: 如何处理超大数据集（>100万行）？**
A: 使用高密度散点图或自动聚合功能，系统会智能采样保留关键分布特征。

**Q: 支持实时数据更新吗？**
A: 支持。通过 WebSocket 连接 SQL 数据源，图表自动刷新。

**Q: 能否自定义图表样式？**
A: 完全支持。提供 CSS/JSON 配置接口，可自定义颜色、字体、动画等。

## 许可证

MIT License - 生产级可商用

## 更新日志

- **v1.0.0** (2026-03-26) - 初始版本，支持 24+ 种图表
