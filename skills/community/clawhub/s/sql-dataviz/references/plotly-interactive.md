# 交互式图表（Plotly）

适用场景：需要 hover 查看详情、zoom/pan 探索数据、输出为可分享的 HTML。

---

## 安装
```bash
pip install plotly kaleido  # kaleido 用于导出静态图片
```

---

## 交互式折线图

```python
import plotly.express as px
import plotly.graph_objects as go

# 基础折线图
fig = px.line(df, x='date', y='value',
              title='每日订单量趋势',
              labels={'date': '日期', 'value': '订单量'},
              template='plotly_white')

fig.update_traces(line_color='#3b82f6', line_width=2)
fig.update_layout(
    hovermode='x unified',
    title_font_size=16,
    font_family='Microsoft YaHei, SimHei, Arial'
)

# 保存
fig.write_html('trend.html')          # 交互式 HTML
fig.write_image('trend.png', scale=2) # 静态图（需 kaleido）
fig.show()
```

---

## 交互式条形图

```python
fig = px.bar(df, x='category', y='value',
             title='各品类销售额',
             labels={'category': '品类', 'value': '销售额'},
             color='value',
             color_continuous_scale='Blues',
             template='plotly_white')

fig.update_layout(showlegend=False)
fig.write_html('bar.html')
```

---

## 多系列对比（分组条形）

```python
fig = px.bar(df_long, x='month', y='value', color='channel',
             barmode='group',
             title='各渠道月度订单量对比',
             color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b'],
             template='plotly_white')

fig.update_layout(
    legend_title_text='渠道',
    hovermode='x unified'
)
fig.write_html('grouped_bar.html')
```

---

## 散点图（相关性探索）

```python
fig = px.scatter(df, x='price', y='sales',
                 size='revenue',        # 气泡大小
                 color='category',      # 颜色分类
                 hover_name='product',  # hover 显示名称
                 hover_data=['discount'],
                 title='价格 vs 销量（气泡大小=营收）',
                 template='plotly_white')

fig.update_traces(marker_opacity=0.7)
fig.write_html('scatter.html')
```

---

## 热力图（Cohort 留存）

```python
import plotly.graph_objects as go

fig = go.Figure(data=go.Heatmap(
    z=retention_matrix.values,
    x=[f'第{i}周' for i in range(retention_matrix.shape[1])],
    y=retention_matrix.index.astype(str),
    colorscale='Blues',
    text=retention_matrix.values.round(1),
    texttemplate='%{text}%',
    hovertemplate='注册周: %{y}<br>留存周: %{x}<br>留存率: %{z:.1f}%<extra></extra>'
))

fig.update_layout(
    title='用户 Cohort 留存率热力图',
    xaxis_title='留存周期',
    yaxis_title='注册周',
    template='plotly_white',
    font_family='Microsoft YaHei, SimHei'
)
fig.write_html('cohort.html')
```

---

## 漏斗图（转化分析）

```python
fig = go.Figure(go.Funnel(
    y=['曝光', '点击', '加购', '下单', '支付'],
    x=[100000, 35000, 12000, 5000, 4200],
    textinfo='value+percent initial',
    marker_color=['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#10b981']
))

fig.update_layout(
    title='购买转化漏斗',
    template='plotly_white',
    font_family='Microsoft YaHei, SimHei'
)
fig.write_html('funnel.html')
```

---

## 多图面板（Subplots）

```python
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('订单趋势', '品类分布', '金额分布', '渠道对比'),
    specs=[[{'type': 'scatter'}, {'type': 'bar'}],
           [{'type': 'histogram'}, {'type': 'bar'}]]
)

# 左上：折线
fig.add_trace(go.Scatter(x=df_trend['date'], y=df_trend['orders'],
                          line_color='#3b82f6', name='订单量'), row=1, col=1)

# 右上：条形
fig.add_trace(go.Bar(x=df_cat['category'], y=df_cat['value'],
                      marker_color='#10b981', name='销售额'), row=1, col=2)

# 左下：直方图
fig.add_trace(go.Histogram(x=df_orders['amount'],
                            marker_color='#f59e0b', name='金额分布'), row=2, col=1)

# 右下：分组条形
fig.add_trace(go.Bar(x=df_channel['month'], y=df_channel['pc'],
                      name='PC', marker_color='#3b82f6'), row=2, col=2)
fig.add_trace(go.Bar(x=df_channel['month'], y=df_channel['mobile'],
                      name='移动', marker_color='#ef4444'), row=2, col=2)

fig.update_layout(
    title_text='业务数据概览 Dashboard',
    height=700,
    template='plotly_white',
    font_family='Microsoft YaHei, SimHei',
    showlegend=False
)
fig.write_html('dashboard.html')
fig.show()
```

---

## 导出说明

| 格式 | 命令 | 说明 |
|------|------|------|
| 交互式 HTML | `fig.write_html('out.html')` | 可分享，支持 hover/zoom |
| 静态 PNG | `fig.write_image('out.png', scale=2)` | 需安装 kaleido |
| 静态 SVG | `fig.write_image('out.svg')` | 矢量，适合汇报 |
| 静态 PDF | `fig.write_image('out.pdf')` | 打印用 |
