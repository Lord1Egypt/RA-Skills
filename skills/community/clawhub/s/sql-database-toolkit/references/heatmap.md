# 热力图 — 相关性矩阵、时间热图、表格热图

适用场景：相关性分析、时间序列密度、分类数据对比、矩阵数据可视化。

---

## 核心问题：你想展示什么类型的热力图？

| 场景 | 推荐类型 |
|------|---------|
| 特征之间的相关性？ | 相关性矩阵热力图 |
| 随时间变化的强度？ | 时间热力图（Calendar/Activity） |
| 分类数据对比？ | 分类热力图 |
| 表格数据可视化？ | 表格热力图 |
| 地理位置密度？ | 地理热力图（需地图数据，见地理图表） |

---

## 一、相关性矩阵热力图

相关性热力图是最常用的场景，用于发现变量之间的关系。

### 基础相关性热力图

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(12, 10))

# 计算相关性矩阵
corr = df[['col1', 'col2', 'col3', 'col4', 'col5']].corr()

# 绘制热力图
mask = np.zeros_like(corr)  # 可选：只显示下三角 mask = np.triu(np.ones_like(corr, dtype=bool))

sns.heatmap(corr,
            annot=True,          # 显示数值
            fmt='.2f',           # 数值格式
            cmap='RdYlGn',       # 颜色映射：红-黄-绿（正相关绿，负相关红）
            center=0,             # 0 为中心
            square=True,         # 正方形格子
            linewidths=0.5,      # 格子间隔线
            cbar_kws={'shrink': 0.8, 'label': '相关系数'},
            ax=ax)

ax.set_title('特征相关性矩阵', fontsize=15, fontweight='bold', pad=15)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('corr_heatmap.png', dpi=150, bbox_inches='tight')
```

### 只显示下三角（避免重复信息）

```python
fig, ax = plt.subplots(figsize=(12, 10))

# 上三角遮罩
mask = np.triu(np.ones_like(corr, dtype=bool))

sns.heatmap(corr, mask=mask,
            annot=True, fmt='.2f',
            cmap='RdYlGn', center=0,
            square=True, linewidths=0.5,
            cbar_kws={'shrink': 0.8},
            ax=ax)

ax.set_title('特征相关性矩阵（下三角）', fontsize=15, fontweight='bold', pad=15)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('corr_heatmap_lower.png', dpi=150, bbox_inches='tight')
```

### 高级：带聚类的相关性热力图

```python
# 使用 clustermap 进行层次聚类排序
g = sns.clustermap(corr,
                    method='ward',        # 聚类方法
                    cmap='RdYlGn',
                    center=0,
                    annot=True,
                    fmt='.2f',
                    linewidths=0.5,
                    figsize=(12, 10),
                    dendrogram_ratio=(.1, .1),
                    cbar_pos=(0.02, 0.8, 0.03, 0.15))

g.fig.suptitle('特征相关性矩阵（含聚类）', fontsize=15, fontweight='bold', y=1.02)
g.savefig('corr_clustermap.png', dpi=150, bbox_inches='tight')
plt.close()
```

### 标注显著性（p-value）

```python
from scipy import stats

def corr_with_pvalue(df):
    cols = df.columns
    n = len(cols)
    corr = np.zeros((n, n))
    pval = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                corr[i, j] = 1.0
                pval[i, j] = 0
            else:
                r, p = stats.pearsonr(df.iloc[:, i], df.iloc[:, j])
                corr[i, j] = r
                pval[i, j] = p
    return pd.DataFrame(corr, index=cols, columns=cols), pd.DataFrame(pval, index=cols, columns=cols)

corr_matrix, pval_matrix = corr_with_pvalue(df)

fig, ax = plt.subplots(figsize=(12, 10))

# 显著性标注（* p<0.05, ** p<0.01, *** p<0.001）
annot = corr_matrix.round(2).copy()
for i in range(len(pval_matrix)):
    for j in range(len(pval_matrix)):
        p = pval_matrix.iloc[i, j]
        if p < 0.001:
            annot.iloc[i, j] = f'{corr_matrix.iloc[i, j]:.2f}***'
        elif p < 0.01:
            annot.iloc[i, j] = f'{corr_matrix.iloc[i, j]:.2f}**'
        elif p < 0.05:
            annot.iloc[i, j] = f'{corr_matrix.iloc[i, j]:.2f}*'

sns.heatmap(corr_matrix, annot=annot, fmt='',
            cmap='RdYlGn', center=0,
            square=True, linewidths=0.5,
            ax=ax)

ax.set_title('相关性矩阵（* p<0.05, ** p<0.01, *** p<0.001）', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('corr_pvalue.png', dpi=150, bbox_inches='tight')
```

---

## 二、时间热力图

### GitHub 风格贡献热力图

```python
fig, ax = plt.subplots(figsize=(14, 6))

# 重塑为周×天的矩阵（周一=0，周日=6）
df['date'] = pd.to_datetime(df['date'])
df['week'] = df['date'].dt.isocalendar().week
df['dayofweek'] = df['date'].dt.dayofweek

# 按周和星期聚合
pivot = df.groupby(['week', 'dayofweek'])['value'].sum().unstack(fill_value=0)

# 绘制热力图
sns.heatmap(pivot, cmap='YlGnBu', linewidths=0.5,
             square=False, cbar_kws={'label': '活跃度'},
             ax=ax)

# Y 轴标签改为星期
ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
ax.set_xticklabels([f'W{int(w)}' for w in ax.get_xticks()], rotation=45, ha='right', fontsize=8)
ax.set_title('每日活跃热力图', fontsize=15, fontweight='bold')
ax.set_xlabel('周数')
ax.set_ylabel('')

plt.tight_layout()
plt.savefig('calendar_heatmap.png', dpi=150, bbox_inches='tight')
```

### Seaborn 内置 Calendar Heatmap（年视图）

```python
# 使用 calmap 库（更专业）
import calmap

fig, ax = plt.subplots(figsize=(15, 6))

# 设置日期索引
df_indexed = df.set_index('date')['value']

calmap.yearplot(df_indexed, year=2026, ax=ax, cmap='YlGnBu')

ax.set_title('2026 年度活跃热力图', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('year_heatmap.png', dpi=150, bbox_inches='tight')
```

### 月度时间热力图（小时 × 天）

```python
# 场景：用户活跃时间段分析
fig, ax = plt.subplots(figsize=(14, 8))

# 创建小时×星期的矩阵
df['hour'] = df['timestamp'].dt.hour
df['weekday'] = df['timestamp'].dt.dayofweek
pivot = df.groupby(['weekday', 'hour'])['value'].sum().unstack(fill_value=0)

# 绘制
sns.heatmap(pivot, cmap='Blues', linewidths=0.5,
             xticklabels=range(24), yticklabels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
             cbar_kws={'label': '活动量'}, ax=ax)

ax.set_title('用户活跃时段分布（小时 × 星期）', fontsize=15, fontweight='bold')
ax.set_xlabel('小时')
ax.set_ylabel('星期')
plt.xticks(rotation=0)
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('hour_weekday_heatmap.png', dpi=150, bbox_inches='tight')
```

---

## 三、分类热力图

### 分组数据热力图

```python
fig, ax = plt.subplots(figsize=(14, 8))

# 创建 品类×月份 的数据矩阵
pivot = df.pivot_table(values='sales',
                        index='category',
                        columns='month',
                        aggfunc='sum',
                        fill_value=0)

sns.heatmap(pivot, cmap='Blues', linewidths=0.5,
             annot=True, fmt=',.0f',
             cbar_kws={'label': '销售额（万元）'},
             ax=ax)

ax.set_title('各品类月度销售额', fontsize=15, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('category_month_heatmap.png', dpi=150, bbox_inches='tight')
```

### 百分比热力图（按行归一化）

```python
fig, ax = plt.subplots(figsize=(14, 8))

# 按行归一化（每行之和为 100%）
pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

sns.heatmap(pivot_pct, cmap='Blues', linewidths=0.5,
             annot=True, fmt='.1f',
             cbar_kws={'label': '占比（%）'},
             ax=ax)

ax.set_title('各品类月度销售额占比（%）', fontsize=15, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('category_month_pct.png', dpi=150, bbox_inches='tight')
```

### 发散型热力图（展示增减变化）

```python
fig, ax = plt.subplots(figsize=(14, 8))

# 计算环比变化
pivot_diff = pivot.pct_change(axis=1) * 100  # 月度环比增长率

# 发散型 colormap（正=绿，负=红）
cmap = sns.diverging_palette(10, 130, as_cmap=True)  # 红-白-绿

sns.heatmap(pivot_diff, cmap=cmap, center=0,
             linewidths=0.5, fmt='+.1f',
             annot=True, vmin=-50, vmax=50,
             cbar_kws={'label': '环比增长率（%）'},
             ax=ax)

ax.set_title('各品类月度销售额环比变化（%）', fontsize=15, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('pivot_diverging.png', dpi=150, bbox_inches='tight')
```

---

## 四、Cohort 留存热力图

用户留存分析的标准可视化。

```python
def cohort_heatmap(df, cohort_col, period_col, value_col='user_id', metric='count'):
    """
    生成 Cohort 留存热力图
    df: 包含用户首次行为日期和当前行为日期的数据
    cohort_col: 首次行为日期列
    period_col: 当前行为日期列
    """
    df = df.copy()
    df[cohort_col] = pd.to_datetime(df[cohort_col])
    df[period_col] = pd.to_datetime(df[period_col])

    # Cohort 周期（月份）
    df['cohort_month'] = df[cohort_col].dt.to_period('M')
    df['period_month'] = df[period_col].dt.to_period('M')

    # 计算相对月份
    df['period_number'] = (df['period_month'].astype(int) - df['cohort_month'].astype(int))

    # 统计每个 Cohort × Period 的用户数
    cohort_data = df.groupby(['cohort_month', 'period_number'])[value_col].nunique().reset_index()
    cohort_table = cohort_data.pivot(index='cohort_month', columns='period_number', values=value_col)

    # 计算留存率
    cohort_size = cohort_table.iloc[:, 0]
    retention_table = cohort_table.divide(cohort_size, axis=0) * 100

    return cohort_table, retention_table

# 生成数据
cohort_table, retention_table = cohort_heatmap(df, 'first_date', 'activity_date')

# 绘制热力图
fig, ax = plt.subplots(figsize=(16, 10))

sns.heatmap(retention_table, cmap='YlGnBu', linewidths=0.5,
             annot=True, fmt='.0f', vmin=0, vmax=100,
             cbar_kws={'label': '留存率（%）'},
             ax=ax)

ax.set_title('Cohort 用户留存率（%）', fontsize=15, fontweight='bold')
ax.set_xlabel('距首次活跃月数')
ax.set_ylabel('Cohort（首次活跃月份）')
plt.xticks(rotation=0)
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('cohort_retention.png', dpi=150, bbox_inches='tight')
```

### Cohort 热力图进阶：同时显示人数和留存率

```python
# 创建双层热力图：人数 + 留存率
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

# 左图：绝对人数
sns.heatmap(cohort_table, cmap='Blues', linewidths=0.5,
             annot=True, fmt=',.0f', ax=axes[0])
axes[0].set_title('Cohort 用户数', fontsize=14, fontweight='bold')
axes[0].set_xlabel('距首次活跃月数')

# 右图：留存率
sns.heatmap(retention_table, cmap='YlGnBu', linewidths=0.5,
             annot=True, fmt='.0f', vmin=0, vmax=100, ax=axes[1])
axes[1].set_title('Cohort 留存率（%）', fontsize=14, fontweight='bold')
axes[1].set_xlabel('距首次活跃月数')

for ax in axes:
    ax.set_ylabel('')

plt.suptitle('用户 Cohort 分析', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('cohort_combined.png', dpi=150, bbox_inches='tight')
```

---

## 五、表格热力图

### 普通表格热力图

```python
fig, ax = plt.subplots(figsize=(14, 8))

# 创建表格数据
table_data = df.pivot_table(values='sales',
                             index='region',
                             columns='product',
                             aggfunc='sum',
                             fill_value=0)

sns.heatmap(table_data, cmap='Oranges', linewidths=1,
             annot=True, fmt=',.0f',
             cbar_kws={'label': '销售额（万元）'},
             ax=ax, annot_kws={'size': 10})

ax.set_title('各区域各产品销售额', fontsize=15, fontweight='bold')
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(rotation=0, fontsize=10)

plt.tight_layout()
plt.savefig('table_heatmap.png', dpi=150, bbox_inches='tight')
```

### 带格式化文本的热力图

```python
fig, ax = plt.subplots(figsize=(14, 8))

# 自定义格式化函数
def fmt(val):
    if val == 0:
        return '-'
    elif val >= 10000:
        return f'{val/10000:.1f}万'
    elif val >= 1000:
        return f'{val/1000:.0f}千'
    else:
        return f'{val:.0f}'

annot = table_data.applymap(fmt)

sns.heatmap(table_data, cmap='YlOrRd', linewidths=1,
             annot=annot, fmt='', cbar=False, ax=ax)

ax.set_title('各区域各产品销售额', fontsize=15, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('table_heatmap_fmt.png', dpi=150, bbox_inches='tight')
```

---

## 六、颜色映射选择指南

### 何时用哪种 Colormap

| Colormap | 类型 | 适用场景 |
|----------|------|---------|
| `RdYlGn` | 发散型 | 相关性、变化率（中心=0） |
| `RdBu` | 发散型 | 正负对比（金融涨跌） |
| `seismic` | 发散型 | 地震/极端正负值 |
| `Blues` / `YlGnBu` | 顺序型 | 单向递增（销售额、用户数） |
| `Oranges` / `Reds` | 顺序型 | 热度、风险、强度 |
| `viridis` / `plasma` | 顺序型 | 科学数据、色盲友好 |
| `coolwarm` | 发散型 | 温度、情感分析 |
| `cubehelix` | 顺序型 | 亮度渐变、打印友好 |

### 发散型 vs 顺序型

```python
# 发散型：数据有正负对比
cmap_div = sns.diverging_palette(10, 130, as_cmap=True)  # 红-白-绿

# 顺序型：数据单向递增
cmap_seq = sns.color_palette('Blues', as_cmap=True)

# 自定义边界
import matplotlib.colors as mcolors
cmap_custom = mcolors.LinearSegmentedColormap.from_list(
    'custom', ['#f7fbff', '#3b82f6', '#1e3a5f'])
```

### 色盲友好建议

```python
# 推荐色盲友好的 colormap
cbar_kws={'label': '值', 'cmap': 'viridis'}  # 默认最优
cbar_kws={'label': '值', 'cmap': 'cividis'}   # 更深的对比
```

---

## 七、高级场景

### 热力图 + 树状图（层次聚类排序）

```python
g = sns.clustermap(df.corr(),
                   method='average',
                   metric='correlation',
                   cmap='RdYlGn',
                   center=0,
                   annot=True,
                   fmt='.2f',
                   linewidths=0.5,
                   figsize=(12, 10),
                   dendrogram_ratio=(0.2, 0.2),
                   cbar_pos=(0.02, 0.8, 0.03, 0.15),
                   tree_kws={'linewidths': 0.5})

g.fig.suptitle('相关性矩阵（层次聚类）', fontsize=15, fontweight='bold', y=1.02)
plt.savefig('heatmap_clustered.png', dpi=150, bbox_inches='tight')
plt.close()
```

### 带缺失值的热力图

```python
fig, ax = plt.subplots(figsize=(14, 8))

# NaN 显示为灰色
cmap = sns.diverging_palette(10, 130, as_cmap=True)

sns.heatmap(table_data, cmap=cmap, center=0,
             linewidths=0.5, fmt='.1f',
             annot=True, ax=ax,
             mask=table_data.isna(),  # 遮罩缺失值
             na_rep='N/A')

ax.set_title('数据热力图（含缺失值显示为 N/A）', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('heatmap_na.png', dpi=150, bbox_inches='tight')
```

### 热力图边框和单元格大小控制

```python
fig, ax = plt.subplots(figsize=(14, 8))

# 调整单元格比例
sns.heatmap(table_data, cmap='Blues',
             linewidths=2,          # 加粗边框
             linecolor='white',     # 白色分隔线
             square=True,            # 正方形格子
             ax=ax)

ax.set_title('单元格热力图', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('heatmap_square.png', dpi=150, bbox_inches='tight')
```

### 热力图 + 散点叠加（双层信息）

```python
fig, ax = plt.subplots(figsize=(14, 8))

# 底色热力图
sns.heatmap(table_data, cmap='Blues', alpha=0.3,
             annot=False, linewidths=0, ax=ax)

# 叠加数值散点
for i, row_idx in enumerate(table_data.index):
    for j, col_idx in enumerate(table_data.columns):
        val = table_data.loc[row_idx, col_idx]
        if pd.notna(val):
            ax.scatter(j + 0.5, i + 0.5, s=val/10,
                       c='red' if val > table_data.median().median() else 'blue',
                       alpha=0.6, zorder=10)

ax.set_title('热力图 + 散点叠加', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('heatmap_scatter.png', dpi=150, bbox_inches='tight')
```

---

## 八、强制规范

### ✅ MUST DO

- **相关性热力图必须标注数值**（annot=True）
- **发散型 colormap 必须设置 center=0**
- **colormap 必须有 colorbar 和标签**
- **长标签必须旋转**（rotation=45）保证可读
- **单元格大小应与数据量匹配**：数据多格子小，数据少格子大
- **缺失值必须处理**：mask 或 na_rep

### ❌ MUST NOT

- 不用 `jet` / `rainbow` 等非色盲友好 colormap
- 不在正负数据上使用单向 colormap（如 Blues）
- 不省略 colorbar（无法判断颜色对应数值）
- 不在过小的格子里显示长数字（改用颜色深浅）
- 不用 3D 热力图（无法准确读值）
- 不在类别过多时使用热力图（改用条形图或表格）

---

## 九、行业最佳实践

### 电商：品类×时间 销售热力图

```python
# 月度销售趋势热力图
fig, ax = plt.subplots(figsize=(16, 10))

pivot = df.pivot_table(values='gmv',
                       index='category',
                       columns='month',
                       aggfunc='sum',
                       fill_value=0)

# 使用聚类排序
g = sns.clustermap(pivot, cmap='YlGnBu',
                    annot=True, fmt=',.0f',
                    linewidths=0.5,
                    figsize=(16, 10),
                    dendrogram_ratio=0.15,
                    cbar_pos=(0.02, 0.8, 0.03, 0.15))

g.fig.suptitle('各品类月度销售额（聚类排序）', fontsize=15, fontweight='bold', y=1.02)
plt.savefig('sales_heatmap_clustered.png', dpi=150, bbox_inches='tight')
plt.close()
```

### 金融：资产相关性矩阵

```python
fig, ax = plt.subplots(figsize=(12, 10))

# 计算收益率相关性
returns = df[['stock_a', 'stock_b', 'bond', 'gold', 'commodity']].pct_change().dropna()
corr = returns.corr()

# 使用 seaborn 内置 clustermap 排序
g = sns.clustermap(corr, method='single',
                   cmap='RdYlGn', center=0,
                   annot=True, fmt='.2f',
                   linewidths=0.5,
                   figsize=(10, 8),
                   vmin=-1, vmax=1,
                   dendrogram_ratio=0.1)

g.fig.suptitle('资产收益率相关性矩阵', fontsize=15, fontweight='bold', y=1.02)
plt.savefig('asset_correlation.png', dpi=150, bbox_inches='tight')
plt.close()
```

### 运营：客服响应时效热力图

```python
fig, ax = plt.subplots(figsize=(14, 8))

# 按客服×时段 统计平均响应时间
pivot = df.pivot_table(values='response_time',
                       index='agent',
                       columns='time_slot',
                       aggfunc='mean',
                       fill_value=0)

# 发散型：快=绿，慢=红
cmap = sns.diverging_palette(10, 130, as_cmap=True)

sns.heatmap(pivot, cmap=cmap, center=pivot.values.mean(),
             annot=True, fmt='.0f', vmin=0,
             linewidths=0.5,
             cbar_kws={'label': '平均响应时间（分钟）'},
             ax=ax)

ax.set_title('各客服不同时段平均响应时间（分钟）', fontsize=15, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('response_time_heatmap.png', dpi=150, bbox_inches='tight')
```

### 营销：广告效果对比热力图

```python
fig, ax = plt.subplots(figsize=(14, 8))

# 创意维度：渠道×指标
pivot = df.pivot_table(values='value',
                       index='channel',
                       columns='metric',
                       aggfunc='mean')

# 归一化（按列）便于跨指标对比
pivot_norm = pivot.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=0)

sns.heatmap(pivot_norm, cmap='RdYlGn', vmin=0, vmax=1,
             annot=pivot.round(1), fmt='', linewidths=0.5,
             cbar_kws={'label': '归一化得分'},
             ax=ax)

ax.set_title('各渠道广告效果对比（数值=原始值，颜色=归一化得分）', fontsize=15, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('ad_effectiveness_heatmap.png', dpi=150, bbox_inches='tight')
```

---

## 十、常见问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 热力图颜色对比不明显 | 中心值设置不当 | 调整 center 或 vmin/vmax |
| 长标签重叠 | 列太多 | rotation=45 或改为横向热力图 |
| 数据差异太大（极端值） | 数值跨度大 | 使用对数刻度或分箱 |
| 类别标签无法显示 | 列宽太小 | 调整 figsize 或使用横向热力图 |
| 相关性 0.01 和 0.99 颜色相同 | 没设置 center=0 | 改用 RdYlGn 等发散型 colormap |
| 色盲无法区分 | 用了红绿对比 | 改用 viridis、cividis、Blues |
