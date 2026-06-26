# 图表选型指南

根据数据类型和报告目标选择最合适的图表。

---

## 核心原则

**图表存在的意义是传达信息，不是展示数据。**

选择图表前先问自己：
1. 我想传达什么信息？
2. 读者最关心什么？
3. 这个图表能让读者快速理解吗？

---

## 决策矩阵

### 按数据关系选图

| 数据关系 | 推荐图表 | 适用场景 | 避免使用 |
|---------|---------|---------|---------|
| **时间趋势** | 折线图 | 销售趋势、用户增长 | 饼图、散点图 |
| **分类比较** | 横向条形图 | 品类排名、区域对比 | 折线图（类别少时） |
| **占比构成** | 堆叠条形图 | 渠道占比、成本构成 | 饼图（>5类时） |
| **数值分布** | 直方图/箱线图 | 订单金额分布、薪资分布 | 条形图 |
| **两变量关系** | 散点图 | 价格vs销量、投入vs产出 | 折线图 |
| **流程转化** | 漏斗图 | 购买漏斗、招聘漏斗 | 条形图 |
| **多维对比** | 热力图 | Cohort留存、相关性矩阵 | 多个折线图 |
| **地理分布** | 地图 | 区域销售、用户分布 | 条形图 |
| **进度达成** | 进度条/仪表盘 | 目标达成率、KPI进度 | 折线图 |
| **单一指标** | 大数字卡片 | 总营收、总用户数 | 任何图表 |

---

## 报告类型 vs 图表组合

### 周报/月报
```
┌─────────────────────────────────────┐
│  KPI 卡片（4个核心指标）              │
├─────────────────────────────────────┤
│  折线图（趋势）+ 洞察文字             │
├────────────────────┬────────────────┤
│  横向条形图（排名） │  堆叠图（构成）  │
├────────────────────┼────────────────┤
│  漏斗图（转化）     │  表格（明细）    │
└────────────────────┴────────────────┘
```

### 财务报表
```
┌─────────────────────────────────────┐
│  KPI 卡片（收入/利润/成本/费用）      │
├─────────────────────────────────────┤
│  环形图（成本构成）                  │
├────────────────────┬────────────────┤
│  堆叠条形图（收入构成）│  折线图（趋势）│
├────────────────────┴────────────────┤
│  表格（明细科目）                    │
└─────────────────────────────────────┘
```

### 漏斗报告
```
┌─────────────────────────────────────┐
│  KPI 卡片（整体转化率/各阶段转化率）  │
├─────────────────────────────────────┤
│  漏斗图（全宽）                      │
├────────────────────┬────────────────┤
│  分组漏斗（渠道对比）│  条形图（流失原因）│
├────────────────────┴────────────────┤
│  洞察 + 优化建议                     │
└─────────────────────────────────────┘
```

### 留存报告
```
┌─────────────────────────────────────┐
│  KPI 卡片（次日留存/7日留存/30日留存）│
├─────────────────────────────────────┤
│  Cohort 热力图（全宽）               │
├────────────────────┬────────────────┤
│  折线图（留存曲线） │  条形图（渠道对比）│
└────────────────────┴────────────────┘
```

---

## 图表设计规范

### 折线图
```python
# 最佳实践
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(df['date'], df['value'], linewidth=2.2, color='#3b82f6')
ax.fill_between(df['date'], df['value'], alpha=0.1, color='#3b82f6')  # 填充区域

# 7日均线
ma7 = df['value'].rolling(7).mean()
ax.plot(df['date'], ma7, linewidth=1.5, linestyle='--', color='#f59e0b')

# 峰值标注
max_idx = df['value'].idxmax()
ax.annotate(f"峰值 {df.loc[max_idx, 'value']:,}",
            xy=(df.loc[max_idx, 'date'], df.loc[max_idx, 'value']),
            xytext=(5, 5), textcoords='offset points')

# 设计规范
ax.grid(axis='y', alpha=0.2, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

**何时使用：**
- 数据点 > 10 个
- 需要展示趋势
- 需要比较多条线（≤5条）

**避免：**
- 数据点 < 5 个（用条形图）
- 多条线交叉严重（分图展示）

### 条形图
```python
# 横向条形图（推荐，适合类别名称较长）
df_sorted = df.sort_values('value', ascending=True)
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.barh(df_sorted['category'], df_sorted['value'],
               color='#3b82f6', height=0.6)

# 数值标注
for bar in bars:
    width = bar.get_width()
    ax.text(width + max_val*0.02, bar.get_y() + bar.get_height()/2,
            f'{width:,.0f}', va='center')

# Y轴从0开始（必须）
ax.set_xlim(0, max_val * 1.15)
```

**何时使用：**
- 分类比较
- 排名展示
- 类别名称较长（横向）

**避免：**
- Y轴不从0开始
- 类别超过15个（合并"其他"）

### 饼图/环形图
```python
# 环形图（比饼图更好）
fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(
    df['value'], labels=df['category'],
    autopct='%1.1f%%', pctdistance=0.75,
    colors=PALETTE[:len(df)]
)
# 中心留白
centre_circle = plt.Circle((0, 0), 0.5, fc='white')
ax.add_artist(centre_circle)
```

**何时使用：**
- 类别 ≤ 5 个
- 需要展示"占比"概念
- 一眼看清构成

**避免：**
- 类别 > 5 个（用堆叠条形图）
- 3D 饼图（永远不要用）
- 需要精确比较数值

### 漏斗图
```python
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(5, 4))
ax.set_xlim(0, 1)
ax.set_ylim(0, len(labels))
ax.axis('off')

for i, (label, val) in enumerate(zip(reversed(labels), reversed(values))):
    pct = val / values[0]
    width = 0.2 + 0.8 * pct
    left = (1 - width) / 2
    
    rect = FancyBboxPatch(
        (left, i*0.18+0.02), width, 0.15,
        boxstyle="round,pad=0.01",
        facecolor=colors[i]
    )
    ax.add_patch(rect)
    ax.text(0.5, i*0.18+0.095,
            f'{label}  {val:,}  ({pct*100:.1f}%)',
            ha='center', va='center',
            color='white', fontweight='bold')
```

### 热力图（Cohort）
```python
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(
    cohort_matrix,
    annot=True, fmt='.1f',
    cmap='Blues',
    cbar_kws={'label': '留存率(%)'},
    ax=ax
)
ax.set_xlabel('留存周期')
ax.set_ylabel('注册周')
```

---

## 颜色使用规范

### 单系列
```python
PRIMARY = '#3b82f6'  # 主色
```

### 多系列（色盲友好）
```python
PALETTE = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']
```

### 正负对比
```python
# 国内股市风格：绿涨红跌
UP   = '#10b981'
DOWN = '#ef4444'

# 欧美股市风格：红涨绿跌
UP   = '#ef4444'
DOWN = '#10b981'
```

### 渐变色
```python
import matplotlib.cm as cm
cmap = cm.get_cmap('Blues')
colors = [cmap(0.3 + 0.7 * i/len(df)) for i in range(len(df))]
```
