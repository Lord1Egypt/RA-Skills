# Visualization Patterns Reference

## 图表选型决策矩阵

| 分析目标 | 首选图表 | 备选 | Plotly 函数 |
|---|---|---|---|
| 时间趋势 | 折线图 | 面积图 | `px.line` / `px.area` |
| 类别比较 | 柱状图 | 条形图 | `px.bar` |
| 部分与整体 | 环形图 | 旭日图 | `px.pie` / `px.sunburst` |
| 数值分布 | 箱线图 | 直方图 | `px.box` / `px.histogram` |
| 两变量相关 | 散点图 | 气泡图 | `px.scatter` |
| 多变量相关 | 热力图 | 平行坐标 | `px.imshow` / `px.parallel_coordinates` |
| 地理分布 | Choropleth | 气泡地图 | `px.choropleth` |
| 流量/转化 | 桑基图 | 漏斗图 | `go.Sankey` / `px.funnel` |

---

## Plotly 全局样式配置

```python
STYLE_CONFIG = {
    'font_family': 'Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif',
    'bg_color': '#FAFAFA',
    'grid_color': '#E8E8E8',
    'primary_colors': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B4A6B', '#6BAB5E'],
    'title_size': 18,
    'axis_size': 12,
}

def apply_global_style(fig):
    fig.update_layout(
        font=dict(family=STYLE_CONFIG['font_family'], size=STYLE_CONFIG['axis_size']),
        paper_bgcolor=STYLE_CONFIG['bg_color'],
        plot_bgcolor=STYLE_CONFIG['bg_color'],
        colorway=STYLE_CONFIG['primary_colors'],
    )
    fig.update_xaxes(gridcolor=STYLE_CONFIG['grid_color'], showgrid=True)
    fig.update_yaxes(gridcolor=STYLE_CONFIG['grid_color'], showgrid=True)
    return fig
```

---

## 仪表盘布局模板

### 2×2 标准仪表盘

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=['趋势分析', '类别分布', '异常检测', '相关矩阵'],
    specs=[
        [{"type": "scatter"}, {"type": "bar"}],
        [{"type": "scatter"}, {"type": "heatmap"}]
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.08,
)
fig.update_layout(height=800, showlegend=True)
```

### KPI 卡片行

```python
def add_kpi_card(fig, value, title, delta=None, row=1, col=1):
    fig.add_trace(
        go.Indicator(
            mode="number+delta" if delta else "number",
            value=value,
            delta={"reference": delta, "relative": True} if delta else None,
            title={"text": title, "font": {"size": 14}},
            number={"font": {"size": 32}},
        ),
        row=row, col=col
    )
```

---

## Matplotlib 报告级配置

```python
import matplotlib.pyplot as plt

CJK_FONTS = ['Microsoft YaHei', 'SimHei', 'PingFang SC', 'Noto Sans CJK SC']
plt.rcParams.update({
    'font.sans-serif': CJK_FONTS,
    'axes.unicode_minus': False,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'figure.facecolor': 'white',
    'axes.facecolor': '#FAFAFA',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
})
```

---

## 颜色系统

```python
# 主色调（适合深色/浅色背景）
PRIMARY   = '#2E86AB'  # 蓝色
SECONDARY = '#A23B72'  # 紫红
ACCENT    = '#F18F01'  # 橙黄
DANGER    = '#C73E1D'  # 红色
SUCCESS   = '#6BAB5E'  # 绿色

# 数据密度色谱
SEQUENTIAL = 'Blues'    # 单变量连续
DIVERGING  = 'RdYlGn'   # 正负对比
QUALITATIVE = 'Set2'    # 类别区分

# 状态色（数据质量标注）
STATUS_COLORS = {
    'normal': '#6BAB5E',
    'warning': '#F18F01',
    'critical': '#C73E1D',
    'missing': '#CCCCCC',
}
```

---

## 导出规范

```python
def export_all_formats(fig, base_path: str):
    """导出 HTML + PNG + PDF"""
    # 交互版（含完整 JS）
    fig.write_html(f"{base_path}.html", include_plotlyjs='cdn')
    # 静态高清版
    fig.write_image(f"{base_path}.png", scale=2, width=1200, height=800)
    # PDF（需要 kaleido）
    fig.write_image(f"{base_path}.pdf", width=1200, height=800)
```
