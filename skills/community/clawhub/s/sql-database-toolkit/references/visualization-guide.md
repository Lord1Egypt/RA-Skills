# SQL 查询结果可视化指南

当用户需要将 SQL 查询结果转化为图表时，加载本文件。

---

## 1. 图表选型决策树

拿到查询结果后，先问：**我想表达什么关系？**

| 数据关系 | 推荐图表 | 避免使用 |
|---------|---------|---------|
| 随时间变化的趋势 | 折线图 | 饼图 |
| 分类之间的比较 | 条形图（横向：类别多；纵向：类别少） | 折线图 |
| 整体中各部分占比 | 堆叠条形图、矩形树图 | 饼图（>5类时尤其避免） |
| 数值分布 | 直方图、箱线图、小提琴图 | 条形图 |
| 两变量相关性 | 散点图、回归图 | 条形图 |
| 排名 | 横向条形图 | 纵向条形图、饼图 |
| 地理分布 | 地图（Choropleth） | 条形图 |
| 多维度对比 | 热力图、雷达图 | 单一折线图 |
| 流向/转化漏斗 | 桑基图、漏斗图 | 折线图 |
| 单一关键指标 | 大数字 KPI 卡片 | 任何图表（过度设计） |

### 关于饼图
饼图几乎总是错误的选择：
- ❌ 难以比较相近大小的扇区
- ❌ 超过 5 个类别就无法阅读
- ❌ 3D 饼图永远是错的
- ✅ 替代方案：横向条形图（比较清晰）、堆叠条形图（占比）、矩形树图（层级占比）

---

## 2. Python 可视化代码模板

### 环境准备
```bash
pip install matplotlib seaborn plotly pandas
```

### 折线图（时间趋势）
```python
import matplotlib.pyplot as plt
import pandas as pd

# 假设 df 是 SQL 查询结果
# df = pd.read_sql(query, conn)
df['date'] = pd.to_datetime(df['date'])

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['date'], df['value'], linewidth=2, color='#3b82f6', marker='o', markersize=4)

ax.set_title('每日订单量趋势', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('日期')
ax.set_ylabel('订单量')
ax.grid(axis='y', alpha=0.3)
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('trend.png', dpi=150, bbox_inches='tight')
plt.show()
```

### 条形图（分类比较）
```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df['category'], df['value'], color='#3b82f6', width=0.6)

# 在柱顶标注数值
for bar, val in zip(bars, df['value']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:,.0f}', ha='center', va='bottom', fontsize=10)

ax.set_title('各品类销售额', fontsize=16, fontweight='bold')
ax.set_xlabel('品类')
ax.set_ylabel('销售额（万元）')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('bar.png', dpi=150, bbox_inches='tight')
```

### 横向条形图（排名）
```python
# 适合类别名称较长，或需要展示排名
df_sorted = df.sort_values('value', ascending=True)  # 升序让最大值在顶部

fig, ax = plt.subplots(figsize=(10, 8))
colors = ['#ef4444' if v == df_sorted['value'].max() else '#3b82f6'
          for v in df_sorted['value']]
ax.barh(df_sorted['name'], df_sorted['value'], color=colors)

ax.set_title('Top 10 用户消费排名', fontsize=16, fontweight='bold')
ax.set_xlabel('消费金额')
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('ranking.png', dpi=150, bbox_inches='tight')
```

### 热力图（相关性矩阵）
```python
import seaborn as sns

corr = df[['col1', 'col2', 'col3', 'col4']].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, vmin=-1, vmax=1, ax=ax,
            linewidths=0.5)

ax.set_title('指标相关性矩阵', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('heatmap.png', dpi=150, bbox_inches='tight')
```

### 交互式图表（Plotly）
```python
import plotly.express as px
import plotly.graph_objects as go

# 折线图（交互式，支持 hover/zoom）
fig = px.line(df, x='date', y='value', title='每日订单量趋势',
              labels={'date': '日期', 'value': '订单量'})
fig.update_traces(line_color='#3b82f6', line_width=2)
fig.update_layout(hovermode='x unified')
fig.write_html('trend_interactive.html')  # 保存为可交互 HTML
fig.show()

# 多系列对比
fig = px.bar(df, x='month', y='revenue', color='region',
             barmode='group', title='各区域月度营收对比')
fig.write_html('comparison.html')
```

### 多图面板（Dashboard 风格）
```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('业务数据概览', fontsize=18, fontweight='bold', y=1.02)

# 左上：趋势
axes[0, 0].plot(df_trend['date'], df_trend['orders'], color='#3b82f6')
axes[0, 0].set_title('订单趋势')

# 右上：分类占比
axes[0, 1].barh(df_cat['name'], df_cat['value'], color='#10b981')
axes[0, 1].set_title('品类分布')

# 左下：分布
axes[1, 0].hist(df_dist['amount'], bins=30, color='#f59e0b', edgecolor='white')
axes[1, 0].set_title('订单金额分布')

# 右下：相关性
sns.heatmap(df_corr.corr(), annot=True, fmt='.2f', ax=axes[1, 1], cmap='coolwarm')
axes[1, 1].set_title('指标相关性')

plt.tight_layout()
plt.savefig('dashboard.png', dpi=150, bbox_inches='tight')
```

---

## 3. SQL → 可视化完整流程

```python
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3  # 或 psycopg2 / mysql.connector

# Step 1: 执行 SQL 查询，结果转 DataFrame
conn = sqlite3.connect('mydb.sqlite')
# conn = psycopg2.connect("host=localhost dbname=mydb user=myuser password=xxx")

query = """
    SELECT
        DATE(created_at) AS date,
        COUNT(*) AS orders,
        SUM(amount) AS revenue
    FROM orders
    WHERE created_at >= DATE('now', '-30 days')
    GROUP BY DATE(created_at)
    ORDER BY date
"""
df = pd.read_sql(query, conn)
conn.close()

# Step 2: 数据预处理
df['date'] = pd.to_datetime(df['date'])
df['revenue'] = df['revenue'].fillna(0)

# Step 3: 选择图表类型并绘制
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(df['date'], df['orders'], color='#3b82f6', linewidth=2)
ax1.set_title('近 30 天订单量')
ax1.tick_params(axis='x', rotation=45)

ax2.bar(df['date'], df['revenue'], color='#10b981', width=0.8)
ax2.set_title('近 30 天营收')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('report.png', dpi=150, bbox_inches='tight')
print("图表已保存：report.png")
```

---

## 4. 设计原则（来自 data-visualization-2）

### 必须遵守
- **Y 轴从 0 开始**（条形图）：避免视觉误导
- **每张图只传达一个信息**：不要在一张图里塞太多
- **标注轴标签和标题**：图表要能独立理解，不依赖上下文
- **颜色有目的**：用颜色高亮重点，不是装饰
- **精确数据用表格**，规律趋势用图表

### 颜色推荐
```python
# 主色调（单系列）
PRIMARY = '#3b82f6'   # 蓝色

# 多系列配色（色盲友好）
PALETTE = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']

# 发散色（正负对比，如同比增减）
DIVERGING = 'RdYlGn'  # seaborn/matplotlib colormap

# 设置全局字体（中文支持）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
```

---

## 5. 可视化意图识别

当用户说以下话时，加载本文件并给出图表方案：
- "帮我画个图" / "出个图表" / "可视化一下"
- "这个查询结果怎么展示"
- "做个报表" / "做个 dashboard"
- "趋势图" / "对比图" / "分布图"
- "用 Python 画" / "用 matplotlib/seaborn/plotly"

同时推荐用户参考独立的 `sql-dataviz` skill 获取更深入的可视化能力。
