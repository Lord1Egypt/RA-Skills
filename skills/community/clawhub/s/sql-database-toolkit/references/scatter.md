# 散点图 — 相关性、趋势、异常识别

适用场景：展示两变量关系、回归分析、聚类识别、异常值发现。

---

## 核心问题：你想分析什么？

| 问题 | 推荐图表 |
|------|---------|
| 两个变量是否相关？ | 散点图 |
| 相关强度和方向？ | 散点图 + 回归线 |
| 第三维度的影响？ | 气泡图（大小表示第三维） |
| 多变量两两关系？ | 散点图矩阵（Pair Plot） |
| 识别异常点？ | 散点图 + 标注 |
| 时间序列的关系？ | 滞后散点图（Lag Plot） |

---

## 一、基础散点图

### 标准散点图

```python
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 8))

ax.scatter(df['x'], df['y'],
           c='#3b82f6', alpha=0.6, s=50, edgecolors='white', linewidth=0.5)

ax.set_title('广告投入 vs 销售额', fontsize=15, fontweight='bold', pad=12)
ax.set_xlabel('广告投入（万元）')
ax.set_ylabel('销售额（万元）')
ax.grid(alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('scatter_basic.png', dpi=150, bbox_inches='tight')
```

### 散点图 + 回归线

```python
fig, ax = plt.subplots(figsize=(10, 8))

# 散点
ax.scatter(df['x'], df['y'],
           c='#3b82f6', alpha=0.6, s=50, edgecolors='white', label='数据点')

# 回归线
z = np.polyfit(df['x'], df['y'], 1)  # 一元线性回归
p = np.poly1d(z)
x_line = np.linspace(df['x'].min(), df['x'].max(), 100)
ax.plot(x_line, p(x_line), 'r--', linewidth=2, label=f'趋势线: y={z[0]:.2f}x+{z[1]:.2f}')

# 相关系数
corr = df['x'].corr(df['y'])
ax.text(0.05, 0.95, f'相关系数 r = {corr:.3f}',
        transform=ax.transAxes, fontsize=12,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.legend()
ax.set_title('广告投入 vs 销售额（含趋势线）', fontsize=15, fontweight='bold')
ax.set_xlabel('广告投入（万元）')
ax.set_ylabel('销售额（万元）')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('scatter_regression.png', dpi=150, bbox_inches='tight')
```

### 使用 Seaborn 简化

```python
fig, ax = plt.subplots(figsize=(10, 8))

sns.regplot(data=df, x='x', y='y',
            scatter_kws={'alpha': 0.6, 's': 50, 'color': '#3b82f6'},
            line_kws={'color': '#ef4444', 'linewidth': 2},
            ax=ax)

ax.set_title('广告投入 vs 销售额', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('scatter_regplot.png', dpi=150, bbox_inches='tight')
```

---

## 二、分组散点图

### 按类别着色

```python
fig, ax = plt.subplots(figsize=(10, 8))

PALETTE = ['#3b82f6', '#10b981', '#ef4444', '#f59e0b']
groups = df['category'].unique()

for i, group in enumerate(groups):
    subset = df[df['category'] == group]
    ax.scatter(subset['x'], subset['y'],
               c=PALETTE[i], alpha=0.6, s=50, label=group,
               edgecolors='white', linewidth=0.5)

ax.legend(title='类别')
ax.set_title('各渠道广告投入 vs 销售额', fontsize=15, fontweight='bold')
ax.set_xlabel('广告投入（万元）')
ax.set_ylabel('销售额（万元）')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('scatter_grouped.png', dpi=150, bbox_inches='tight')
```

### 使用 Seaborn 分组

```python
fig, ax = plt.subplots(figsize=(10, 8))

sns.scatterplot(data=df, x='x', y='y', hue='category',
                palette=PALETTE, alpha=0.6, s=80, ax=ax)

ax.legend(title='类别', loc='upper left')
ax.set_title('各渠道广告投入 vs 销售额', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('scatter_hue.png', dpi=150, bbox_inches='tight')
```

### 分组回归线

```python
fig, ax = plt.subplots(figsize=(10, 8))

sns.lmplot(data=df, x='x', y='y', hue='category',
           palette=PALETTE, height=6, aspect=1.3,
           scatter_kws={'alpha': 0.5, 's': 50})

plt.title('各渠道广告投入 vs 销售额（分组回归）', fontsize=15, fontweight='bold')
plt.savefig('scatter_lmplot.png', dpi=150, bbox_inches='tight')
plt.close()  # lmplot 创建新 Figure，需关闭
```

---

## 三、气泡图（三变量）

用气泡大小表示第三个变量。

```python
fig, ax = plt.subplots(figsize=(12, 8))

# 气泡大小映射到第三变量
sizes = (df['z'] - df['z'].min()) / (df['z'].max() - df['z'].min()) * 500 + 50

scatter = ax.scatter(df['x'], df['y'], s=sizes,
                     c=df['category'].map(dict(zip(df['category'].unique(), PALETTE))),
                     alpha=0.6, edgecolors='white', linewidth=1)

ax.set_title('广告投入 vs 销售额（气泡大小 = 用户数）', fontsize=15, fontweight='bold')
ax.set_xlabel('广告投入（万元）')
ax.set_ylabel('销售额（万元）')

# 图例（气泡大小）
for size_label, size_val in [('小', 100), ('中', 300), ('大', 500)]:
    ax.scatter([], [], s=size_val, c='gray', alpha=0.5, label=size_label)
ax.legend(title='用户规模', loc='upper left')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('bubble.png', dpi=150, bbox_inches='tight')
```

### 四变量散点图（颜色 + 大小）

```python
fig, ax = plt.subplots(figsize=(12, 8))

scatter = ax.scatter(df['x'], df['y'],
                     s=df['size'] / df['size'].max() * 500 + 30,  # 大小
                     c=df['color'],  # 颜色映射到第四变量
                     cmap='RdYlGn', alpha=0.6, edgecolors='white')

# 颜色条
cbar = plt.colorbar(scatter, ax=ax, shrink=0.8)
cbar.set_label('增长率（%）')

ax.set_title('广告投入 vs 销售额（大小=用户数，颜色=增长率）', fontsize=15, fontweight='bold')
ax.set_xlabel('广告投入（万元）')
ax.set_ylabel('销售额（万元）')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('scatter_4d.png', dpi=150, bbox_inches='tight')
```

---

## 四、散点图矩阵（Pair Plot）

用于探索多变量两两关系。

### 基础散点图矩阵

```python
# 选取数值列
cols = ['ad_spend', 'sales', 'users', 'conversion_rate']
sns.pairplot(df[cols], diag_kind='kde',
             plot_kws={'alpha': 0.6, 's': 30},
             diag_kws={'fill': True})

plt.suptitle('多变量关系矩阵', fontsize=15, fontweight='bold', y=1.02)
plt.savefig('pairplot.png', dpi=150, bbox_inches='tight')
plt.close()
```

### 分组散点图矩阵

```python
sns.pairplot(df[cols + ['category']], hue='category',
             palette=PALETTE[:len(df['category'].unique())],
             diag_kind='kde',
             plot_kws={'alpha': 0.6, 's': 30})

plt.suptitle('各渠道多变量关系矩阵', fontsize=15, fontweight='bold', y=1.02)
plt.savefig('pairplot_hue.png', dpi=150, bbox_inches='tight')
plt.close()
```

---

## 五、处理数据重叠（Overplotting）

当数据点过多时，散点图会重叠，影响判断。

### 方法1：透明度

```python
fig, ax = plt.subplots(figsize=(10, 8))

ax.scatter(df['x'], df['y'], alpha=0.1, s=20, c='#3b82f6')

ax.set_title('大数据量散点图（高透明度）', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('scatter_alpha.png', dpi=150, bbox_inches='tight')
```

### 方法2：Hexbin 图

```python
fig, ax = plt.subplots(figsize=(10, 8))

hb = ax.hexbin(df['x'], df['y'], gridsize=30, cmap='Blues', mincnt=1)
cb = plt.colorbar(hb, ax=ax, shrink=0.8)
cb.set_label('点数')

ax.set_title('大数据量散点图（Hexbin）', fontsize=15, fontweight='bold')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('hexbin.png', dpi=150, bbox_inches='tight')
```

### 方法3：2D 直方图

```python
fig, ax = plt.subplots(figsize=(10, 8))

h = ax.hist2d(df['x'], df['y'], bins=50, cmap='Blues', cmin=1)
plt.colorbar(h[3], ax=ax, shrink=0.8, label='点数')

ax.set_title('大数据量散点图（2D 直方图）', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('hist2d.png', dpi=150, bbox_inches='tight')
```

### 方法4：KDE 等高线

```python
fig, ax = plt.subplots(figsize=(10, 8))

# 散点背景
ax.scatter(df['x'], df['y'], alpha=0.2, s=10, c='gray')

# KDE 等高线
sns.kdeplot(data=df, x='x', y='y', levels=10, cmap='Blues', ax=ax)

ax.set_title('大数据量散点图（KDE 等高线）', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('scatter_kde.png', dpi=150, bbox_inches='tight')
```

### 方法5：采样

```python
# 随机采样 10%
df_sample = df.sample(frac=0.1, random_state=42)

fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(df_sample['x'], df_sample['y'], alpha=0.5, s=30, c='#3b82f6')
ax.set_title('采样散点图（10% 数据）', fontsize=15, fontweight='bold')

plt.tight_layout()
plt.savefig('scatter_sampled.png', dpi=150, bbox_inches='tight')
```

---

## 六、异常值标注

### 标注特定点

```python
fig, ax = plt.subplots(figsize=(10, 8))

ax.scatter(df['x'], df['y'], c='#3b82f6', alpha=0.6, s=50)

# 标注异常点（如超过 2 个标准差）
x_mean, x_std = df['x'].mean(), df['x'].std()
y_mean, y_std = df['y'].mean(), df['y'].std()

outliers = df[(np.abs(df['x'] - x_mean) > 2 * x_std) |
              (np.abs(df['y'] - y_mean) > 2 * y_std)]

ax.scatter(outliers['x'], outliers['y'], c='#ef4444', s=100, label='异常点', zorder=5)

# 标注文字
for _, row in outliers.iterrows():
    ax.annotate(row['name'], (row['x'], row['y']),
                xytext=(5, 5), textcoords='offset points', fontsize=9,
                color='#ef4444')

ax.legend()
ax.set_title('异常点识别', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('scatter_outliers.png', dpi=150, bbox_inches='tight')
```

### 使用 DBSCAN 聚类识别异常

```python
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

fig, ax = plt.subplots(figsize=(10, 8))

# 标准化
X = StandardScaler().fit_transform(df[['x', 'y']])

# DBSCAN 聚类
db = DBSCAN(eps=0.5, min_samples=10).fit(X)
labels = db.labels_

# -1 表示噪声点（异常）
colors = ['#ef4444' if l == -1 else '#3b82f6' for l in labels]

ax.scatter(df['x'], df['y'], c=colors, alpha=0.6, s=50)

# 统计
n_outliers = (labels == -1).sum()
ax.text(0.95, 0.95, f'异常点: {n_outliers} ({n_outliers/len(df)*100:.1f}%)',
        transform=ax.transAxes, ha='right', va='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.set_title('DBSCAN 异常检测', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('scatter_dbscan.png', dpi=150, bbox_inches='tight')
```

---

## 七、高级场景

### 滞后散点图（时间序列相关性）

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, lag in enumerate([1, 7, 30]):
    ax = axes[i]
    ax.scatter(df['value'].shift(lag), df['value'],
               alpha=0.5, s=30, c='#3b82f6')
    ax.set_title(f'滞后 {lag} 天')
    ax.set_xlabel(f'值(t-{lag})')
    ax.set_ylabel('值(t)')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.suptitle('销售滞后相关性分析', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('lag_scatter.png', dpi=150, bbox_inches='tight')
```

### 边际分布图（Marginal Plot）

```python
# 使用 seaborn 的 jointplot
g = sns.jointplot(data=df, x='x', y='y',
                  kind='scatter', alpha=0.6, s=50,
                  marginal_kws=dict(bins=30, fill=True, alpha=0.6))

g.fig.suptitle('广告投入 vs 销售额（含边际分布）', fontsize=15, fontweight='bold', y=1.02)
g.savefig('jointplot.png', dpi=150, bbox_inches='tight')
plt.close()
```

### 回归 + 置信区间

```python
fig, ax = plt.subplots(figsize=(10, 8))

sns.regplot(data=df, x='x', y='y',
            scatter_kws={'alpha': 0.5, 's': 50, 'color': '#3b82f6'},
            line_kws={'color': '#ef4444', 'linewidth': 2},
            ci=95,  # 95% 置信区间
            ax=ax)

ax.set_title('回归分析（95% 置信区间）', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('regplot_ci.png', dpi=150, bbox_inches='tight')
```

### 多项式回归

```python
from numpy.polynomial import polynomial as P

fig, ax = plt.subplots(figsize=(10, 8))

ax.scatter(df['x'], df['y'], c='#3b82f6', alpha=0.6, s=50, label='数据点')

# 二次多项式拟合
coeffs = np.polyfit(df['x'], df['y'], 2)
p = np.poly1d(coeffs)
x_line = np.linspace(df['x'].min(), df['x'].max(), 100)
ax.plot(x_line, p(x_line), 'r-', linewidth=2, label='二次拟合')

# 线性对比
z = np.polyfit(df['x'], df['y'], 1)
ax.plot(x_line, np.poly1d(z)(x_line), 'g--', linewidth=2, label='线性拟合')

ax.legend()
ax.set_title('多项式回归对比', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('poly_fit.png', dpi=150, bbox_inches='tight')
```

---

## 八、强制规范

### ✅ MUST DO

- **散点图必须有轴标签和单位**
- **大数据量（>10000）必须处理重叠**：透明度、hexbin、采样、KDE
- **回归线必须标注方程或相关系数**
- **颜色映射必须有图例或色条**
- **异常点标注必须清晰可辨**
- **气泡图必须提供大小图例**

### ❌ MUST NOT

- 不在无标签的情况下使用颜色/大小映射
- 不在散点图上省略趋势信息（当存在明显趋势时）
- 不在数据点过密时使用默认透明度（看不清）
- 不在 X 或 Y 轴使用不连续刻度
- 不忽略异常值的影响（需说明是否排除）
- 不在非线性关系上强行画直线回归

---

## 九、行业最佳实践

### 电商：价格 vs 销量

```python
fig, ax = plt.subplots(figsize=(10, 8))

# 通常呈负相关
ax.scatter(df['price'], df['sales'], c='#3b82f6', alpha=0.6, s=50)

sns.regplot(data=df, x='price', y='sales',
            scatter=False, line_kws={'color': '#ef4444'}, ax=ax)

ax.set_title('价格 vs 销量（需求曲线）', fontsize=15, fontweight='bold')
ax.set_xlabel('价格（元）')
ax.set_ylabel('销量（件）')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('price_sales.png', dpi=150, bbox_inches='tight')
```

### 金融：风险 vs 收益

```python
fig, ax = plt.subplots(figsize=(12, 8))

# 气泡大小 = 资产规模
sizes = df['aum'] / df['aum'].max() * 500 + 50

scatter = ax.scatter(df['volatility'], df['return'],
                     s=sizes, c='#3b82f6', alpha=0.6)

# 有效前沿参考线
ax.plot([0.1, 0.2, 0.3, 0.4], [0.05, 0.08, 0.12, 0.15], 'r--', label='有效前沿')

# 添加资产标签
for _, row in df.iterrows():
    ax.annotate(row['asset'], (row['volatility'], row['return']),
                xytext=(5, 5), textcoords='offset points', fontsize=8)

ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
ax.axvline(x=0, color='gray', linestyle='-', alpha=0.3)

ax.set_title('风险收益散点图（气泡=资产规模）', fontsize=15, fontweight='bold')
ax.set_xlabel('波动率（风险）')
ax.set_ylabel('收益率')
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('risk_return.png', dpi=150, bbox_inches='tight')
```

### 运营：用户行为聚类

```python
from sklearn.cluster import KMeans

fig, ax = plt.subplots(figsize=(10, 8))

# KMeans 聚类
X = df[['frequency', 'monetary']].values
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)

# 按聚类着色
scatter = ax.scatter(df['frequency'], df['monetary'],
                     c=labels, cmap='viridis', alpha=0.6, s=50)

# 聚类中心
centers = kmeans.cluster_centers_
ax.scatter(centers[:, 0], centers[:, 1], c='red', s=200, marker='X', label='聚类中心')

ax.legend()
ax.set_title('用户行为聚类（频率 vs 金额）', fontsize=15, fontweight='bold')
ax.set_xlabel('购买频率')
ax.set_ylabel('消费金额')

plt.colorbar(scatter, ax=ax, shrink=0.8, label='聚类')
plt.tight_layout()
plt.savefig('user_clustering.png', dpi=150, bbox_inches='tight')
```

---

## 十、相关性分析速查

| 相关系数范围 | 强度 | 可视化建议 |
|-------------|------|-----------|
| 0.0 - 0.3 | 弱相关 | 散点图 + 回归线，标注 r |
| 0.3 - 0.6 | 中等相关 | 散点图 + 回归线，标注 r |
| 0.6 - 1.0 | 强相关 | 散点图 + 回归线 + 置信区间 |
| -0.3 - 0.0 | 弱负相关 | 同上 |
| -0.6 - -0.3 | 中等负相关 | 同上 |
| -1.0 - -0.6 | 强负相关 | 同上 |

```python
# 快速计算并解释相关性
def interpret_correlation(r):
    r_abs = abs(r)
    direction = "正" if r > 0 else "负"
    if r_abs < 0.3:
        strength = "弱"
    elif r_abs < 0.6:
        strength = "中等"
    else:
        strength = "强"
    return f"{strength}{direction}相关"

r = df['x'].corr(df['y'])
print(f"r = {r:.3f}, {interpret_correlation(r)}")
```
