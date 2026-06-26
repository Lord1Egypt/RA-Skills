# Visualization Patterns Reference

> 本文件覆盖 `viz_engine.py` 中所有图表类型的选型指南、参数说明和样式规范。
> **快速定位：** 先看「图表选型矩阵」确定图表类型，再看对应章节的代码。

---

## 图表选型矩阵

| 数据特征 | 首选图表 | 备选 | `viz_engine.py` 函数 | Plotly 底层 |
|---|---|---|---|---|
| 时间序列趋势 | 折线图 | 面积图 | `create_dashboard()` | `px.line` / `px.area` |
| 类别对比 | 柱状图 | 条形图 | `create_dashboard()` | `px.bar` |
| 多维度对比 | 雷达图 | 平行坐标 | `create_radar()` | `go.Scatterpolar` |
| 层级占比 | 树状图 | 旭日图 | `create_treemap()` | `px.treemap` / `px.sunburst` |
| 流量 / 转化路径 | 桑基图 | 漏斗图 | `create_sankey()` / `create_funnel()` | `go.Sankey` / `px.funnel` |
| 两变量相关 | 散点图 | 气泡图 | `create_dashboard()` | `px.scatter` |
| 多变量相关 | 热力图 | 平行坐标 | `create_dashboard()` | `px.imshow` |
| 数值分布 | 箱线图 | 直方图 | `create_dashboard()` | `px.box` / `px.histogram` |
| 节点关系网络 | 网络图 | 弦图 | `create_network_graph()` | `go.Scatter` (networkx 布局) |
| 地理散点 | 气泡地图 | 散点地图 | `create_geo_map()` | `px.scatter_mapbox` |
| 地理区域填色 | Choropleth | 等值线图 | `create_choropleth()` | `px.choropleth` |
| 综合分析报告 | 多面板仪表盘 | — | `create_dashboard()` | `make_subplots` |

---

## 全局样式配置

所有图表统一使用以下配置，通过 `_apply_style(fig)` 自动应用：

```python
STYLE = {
    'font':       'Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif',
    'bg':         '#FAFAFA',
    'grid':       '#E8E8E8',
    'colors':     ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B4A6B',
                   '#6BAB5E', '#E8854A', '#5B8C5A', '#8E5572', '#4A90D9'],
    'title_size': 18,
    'axis_size':  12,
}

def _apply_style(fig):
    fig.update_layout(
        font=dict(family=STYLE['font'], size=STYLE['axis_size']),
        paper_bgcolor=STYLE['bg'],
        plot_bgcolor=STYLE['bg'],
        colorway=STYLE['colors'],
    )
    fig.update_xaxes(gridcolor=STYLE['grid'])
    fig.update_yaxes(gridcolor=STYLE['grid'])
    return fig
```

---

## 综合仪表盘

```python
from scripts.viz_engine import create_dashboard, export_viz

# 接受 DeepAnalyzer.run_full_analysis() 的返回值
fig = create_dashboard(report, title="销售数据智能仪表盘")
export_viz(fig, "outputs/report", formats=["html", "png"])
```

**仪表盘面板布局（2×2）：**

| 位置 | 有时间序列时 | 无时间序列时 |
|---|---|---|
| 左上 | 7日趋势折线图 | 首个数值列分布柱图 |
| 右上 | 缺失率条形图 | 缺失率条形图 |
| 左下 | 异常值数量柱图 | 异常值数量柱图 |
| 右下 | 相关性热力图 | 相关性热力图 |

### KPI 指标卡（嵌入仪表盘）

```python
import plotly.graph_objects as go

def add_kpi_row(fig, metrics: list[dict], row=1):
    """
    metrics: [{"value": 1234, "title": "总收入", "delta": 1000}, ...]
    """
    specs = [[{"type": "indicator"}] * len(metrics)]
    for col, m in enumerate(metrics, 1):
        fig.add_trace(
            go.Indicator(
                mode="number+delta" if m.get("delta") else "number",
                value=m["value"],
                delta={"reference": m["delta"], "relative": True} if m.get("delta") else None,
                title={"text": m["title"], "font": {"size": 14}},
                number={"font": {"size": 32}},
            ),
            row=row, col=col
        )
```

---

## 网络关系图

```python
from scripts.viz_engine import create_network_graph, export_viz

# 边列表：(源节点, 目标节点) 或 (源, 目标, 权重)
edges = [
    ("总部", "上海", 10),
    ("总部", "北京", 8),
    ("上海", "客户A", 5),
    ("北京", "客户B", 3),
]

# 自定义节点标签
labels = {"总部": "总部(HQ)", "客户A": "大客户A"}

fig = create_network_graph(edges, node_labels=labels, title="业务关系网络")
export_viz(fig, "outputs/network")
```

**节点大小**根据度（连接数）自动调整，颜色深浅表示度值高低。

---

## 地理散点图

```python
from scripts.viz_engine import create_geo_map, export_viz
import pandas as pd

df = pd.DataFrame({
    'city':  ['北京', '上海', '广州', '深圳'],
    'lat':   [39.90, 31.23, 23.13, 22.54],
    'lon':   [116.41, 121.47, 113.26, 114.06],
    'sales': [1200, 980, 760, 850],
})

fig = create_geo_map(
    df,
    lat_col='lat', lon_col='lon',
    value_col='sales',    # 气泡大小 + 颜色
    label_col='city',     # 悬停标签
    title='各城市销售分布',
    map_style='open-street-map',   # 免费底图，无需 Token
)
export_viz(fig, "outputs/geo_map")
```

---

## Choropleth 区域填色地图

```python
from scripts.viz_engine import create_choropleth, export_viz
import pandas as pd

# 国家级别
df = pd.DataFrame({
    'country': ['China', 'United States', 'Germany', 'Japan'],
    'value':   [100, 85, 60, 72],
})
fig = create_choropleth(df, location_col='country', value_col='value',
                        location_mode='country names', title='各国销售指数')

# 中国省级别（需要 ISO 3166-2 代码）
df_cn = pd.DataFrame({'province': ['CN-BJ', 'CN-SH', 'CN-GD'], 'value': [90, 85, 75]})
fig = create_choropleth(df_cn, location_col='province', value_col='value',
                        location_mode='ISO-3', title='省级销售分布')
export_viz(fig, "outputs/choropleth")
```

---

## 桑基图（流量 / 转化）

```python
from scripts.viz_engine import create_sankey, export_viz

# 节点列表
labels = ['官网', '搜索引擎', '社交媒体', '注册', '付费', '流失']

# 边：source/target 为 labels 中的索引
fig = create_sankey(
    source=[0, 1, 2, 3, 3],
    target=[3, 3, 3, 4, 5],
    value= [500, 300, 200, 400, 600],
    labels=labels,
    title='用户转化漏斗流向',
)
export_viz(fig, "outputs/sankey")
```

---

## 雷达图（多维对比）

```python
from scripts.viz_engine import create_radar, export_viz

categories = ['速度', '质量', '成本', '交付', '创新']
values = {
    '产品A': [80, 90, 70, 85, 60],
    '产品B': [70, 75, 85, 80, 90],
}

fig = create_radar(categories, values, title='产品维度对比')
export_viz(fig, "outputs/radar")
```

---

## 树状图（层级占比）

```python
from scripts.viz_engine import create_treemap, export_viz
import pandas as pd

df = pd.DataFrame({
    'region':  ['华东', '华东', '华南', '华南', '华北'],
    'product': ['A', 'B', 'A', 'C', 'B'],
    'revenue': [300, 200, 180, 150, 250],
})

fig = create_treemap(
    df,
    path_cols=['region', 'product'],   # 层级路径
    value_col='revenue',
    title='区域产品销售树状图',
)
export_viz(fig, "outputs/treemap")
```

---

## 漏斗图（转化率）

```python
from scripts.viz_engine import create_funnel, export_viz

stages = ['访问', '注册', '激活', '付费', '复购']
values = [10000, 3500, 2100, 800, 350]

fig = create_funnel(stages, values, title='用户转化漏斗')
export_viz(fig, "outputs/funnel")
```

---

## Matplotlib 报告级配置

适用于导出高清静态图（论文 / PPT / 印刷）：

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')   # 服务器/Docker 无头环境必须设置

CJK_FONTS = ['Microsoft YaHei', 'SimHei', 'PingFang SC', 'Noto Sans CJK SC']
plt.rcParams.update({
    'font.sans-serif':    CJK_FONTS,
    'axes.unicode_minus': False,
    'figure.dpi':         150,
    'savefig.dpi':        300,
    'figure.facecolor':   'white',
    'axes.facecolor':     '#FAFAFA',
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'grid.alpha':         0.3,
    'grid.linestyle':     '--',
})
```

---

## 颜色系统

```python
# 主色调
PRIMARY   = '#2E86AB'   # 蓝色（主数据）
SECONDARY = '#A23B72'   # 紫红（对比数据）
ACCENT    = '#F18F01'   # 橙黄（强调）
DANGER    = '#C73E1D'   # 红色（异常/警告）
SUCCESS   = '#6BAB5E'   # 绿色（正常/达标）

# 数据色谱
SEQUENTIAL  = 'Blues'    # 单变量连续值
DIVERGING   = 'RdYlGn'  # 正负对比（如同比）
QUALITATIVE = 'Set2'    # 类别区分

# 数据质量状态色
STATUS_COLORS = {
    'normal':   '#6BAB5E',   # 正常
    'warning':  '#F18F01',   # 注意
    'critical': '#C73E1D',   # 异常
    'missing':  '#CCCCCC',   # 缺失
}
```

---

## 导出规范

```python
from scripts.viz_engine import export_viz

# 标准导出（HTML 交互 + PNG 静态）
export_viz(fig, "outputs/report", formats=["html", "png"])

# 全格式导出
export_viz(fig, "outputs/report", formats=["html", "png", "pdf"])
```

| 格式 | 用途 | 依赖 |
|---|---|---|
| `.html` | 交互报告，可在浏览器操作 | 无（CDN 加载 Plotly.js） |
| `.png` | 高清静态图，嵌入 PPT/文档 | `kaleido` |
| `.pdf` | 印刷/正式报告 | `kaleido` |
