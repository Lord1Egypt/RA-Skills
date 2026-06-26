# 分布图 — 直方图、箱线图、小提琴图、密度图

适用场景：展示数值分布、识别异常值、多组分布对比。

---

## 核心问题：你想展示什么样的分布？

| 问题 | 推荐图表 |
|------|---------|
| 单变量分布频率？ | 直方图 |
| 中位数、四分位、异常值？ | 箱线图 |
| 分布形状 + 密度？ | 小提琴图 / KDE |
| 多组分布对比？ | 箱线图 / 小提琴图 |
| 分布是否正态？ | 直方图 + KDE + QQ图 |

---

## 一、直方图（Histogram）

### 基础直方图

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))

# 自动 bins 或指定
n, bins, patches = ax.hist(df['value'], bins=30,
                           color='#3b82f6', edgecolor='white', alpha=0.8)

ax.set_title('订单金额分布', fontsize=15, fontweight='bold', pad=12)
ax.set_xlabel('金额（元）')
ax.set_ylabel('频数')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('histogram.png', dpi=150, bbox_inches='tight')
```

### Bins 数量选择

```python
# 方法1：Sturges 公式（适合正态分布）
bins_sturges = int(np.log2(len(df)) + 1)

# 方法2：Freedman-Diaconis 公式（适合偏态分布，推荐）
q75, q25 = np.percentile(df['value'], [75, 25])
iqr = q75 - q25
bin_width = 2 * iqr / (len(df) ** (1/3))
bins_fd = int((df['value'].max() - df['value'].min()) / bin_width)

# 方法3：Square root（简单快速）
bins_sqrt = int(np.sqrt(len(df)))

print(f"Sturges: {bins_sturges}, FD: {bins_fd}, Sqrt: {bins_sqrt}")
```

**生产级建议：**
- 数据量 < 100：bins = 10~15
- 数据量 100~10000：使用 FD 公式
- 数据量 > 10000：bins = 50~100，或使用 KDE

### 直方图 + KDE（密度曲线）

```python
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 6))

# 直方图（密度归一化）
sns.histplot(df['value'], bins=30, kde=True,
             color='#3b82f6', edgecolor='white', alpha=0.6, ax=ax)

ax.set_title('用户年龄分布（含密度曲线）', fontsize=15, fontweight='bold')
ax.set_xlabel('年龄')
ax.set_ylabel('密度')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('hist_kde.png', dpi=150, bbox_inches='tight')
```

### 分组直方图对比

```python
fig, ax = plt.subplots(figsize=(12, 6))

# 多组数据叠加
sns.histplot(data=df, x='value', hue='group',
             bins=30, alpha=0.5, edgecolor='white', ax=ax)

ax.set_title('不同渠道订单金额分布对比', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('hist_grouped.png', dpi=150, bbox_inches='tight')
```

---

## 二、箱线图（Box Plot）

### 标准箱线图

```python
fig, ax = plt.subplots(figsize=(10, 6))

bp = ax.boxplot(df['value'],
                patch_artist=True,
                widths=0.5,
                showfliers=True,  # 显示异常值
                flierprops=dict(marker='o', markerfacecolor='#ef4444',
                               markersize=6, alpha=0.6))

# 美化
bp['boxes'][0].set_facecolor('#3b82f6')
bp['boxes'][0].set_alpha(0.7)
bp['medians'][0].set_color('#ef4444')
bp['medians'][0].set_linewidth(2)

ax.set_title('响应时间分布', fontsize=15, fontweight='bold', pad=12)
ax.set_ylabel('响应时间（ms）')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('boxplot.png', dpi=150, bbox_inches='tight')
```

### 多组箱线图对比（最常用）

```python
fig, ax = plt.subplots(figsize=(12, 6))

# 按类别分组
groups = df.groupby('category')['value'].apply(list).to_dict()
labels = list(groups.keys())
data = [groups[k] for k in labels]

bp = ax.boxplot(data, patch_artist=True, labels=labels,
                showfliers=True, widths=0.6)

# 多色填充
PALETTE = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
for i, box in enumerate(bp['boxes']):
    box.set_facecolor(PALETTE[i % len(PALETTE)])
    box.set_alpha(0.7)
for median in bp['medians']:
    median.set_color('#1f2937')
    median.set_linewidth(2)

ax.set_title('各品类订单金额分布', fontsize=15, fontweight='bold')
ax.set_xlabel('品类')
ax.set_ylabel('金额（元）')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('boxplot_grouped.png', dpi=150, bbox_inches='tight')
```

### 使用 Seaborn 简化

```python
fig, ax = plt.subplots(figsize=(12, 6))

sns.boxplot(data=df, x='category', y='value',
            palette=PALETTE, width=0.6, ax=ax)

ax.set_title('各区域用户消费分布', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('boxplot_seaborn.png', dpi=150, bbox_inches='tight')
```

### 横向箱线图

```python
fig, ax = plt.subplots(figsize=(10, 8))

sns.boxplot(data=df, y='category', x='value',
            palette=PALETTE, width=0.6, ax=ax)

ax.set_title('各区域用户消费分布', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('boxplot_horizontal.png', dpi=150, bbox_inches='tight')
```

### 隐藏异常值

```python
# 场景：异常值过多影响主分布展示
fig, ax = plt.subplots(figsize=(12, 6))

sns.boxplot(data=df, x='category', y='value',
            showfliers=False,  # 隐藏异常值
            palette=PALETTE, ax=ax)

ax.set_title('各品类订单金额分布（隐藏极端值）', fontsize=15, fontweight='bold')

plt.tight_layout()
plt.savefig('boxplot_no_fliers.png', dpi=150, bbox_inches='tight')
```

---

## 三、小提琴图（Violin Plot）

小提琴图 = 箱线图 + KDE，同时展示分布形状和统计量。

### 标准小提琴图

```python
fig, ax = plt.subplots(figsize=(12, 6))

sns.violinplot(data=df, x='category', y='value',
               palette=PALETTE, inner='box', ax=ax)
# inner: 'box', 'quartile', 'point', 'stick', None

ax.set_title('各渠道用户年龄分布', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('violin.png', dpi=150, bbox_inches='tight')
```

### 小提琴图 + 箱线图叠加

```python
fig, ax = plt.subplots(figsize=(12, 6))

# 小提琴（半透明）
sns.violinplot(data=df, x='category', y='value',
               palette=PALETTE, inner=None, alpha=0.4, ax=ax)

# 箱线图叠加
sns.boxplot(data=df, x='category', y='value',
            width=0.2, color='white', ax=ax,
            boxprops=dict(zorder=10))

ax.set_title('各渠道用户年龄分布（小提琴+箱线）', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('violin_box.png', dpi=150, bbox_inches='tight')
```

### 分组小提琴图

```python
fig, ax = plt.subplots(figsize=(14, 6))

sns.violinplot(data=df, x='region', y='value', hue='gender',
               split=True,  # 左右分割
               palette=['#3b82f6', '#ef4444'], ax=ax)

ax.set_title('各地区男女消费分布对比', fontsize=15, fontweight='bold')
ax.legend(title='性别')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('violin_grouped.png', dpi=150, bbox_inches='tight')
```

---

## 四、核密度图（KDE）

### 单变量 KDE

```python
fig, ax = plt.subplots(figsize=(10, 6))

sns.kdeplot(df['value'], fill=True, color='#3b82f6', alpha=0.6, ax=ax)

ax.set_title('用户年龄密度分布', fontsize=15, fontweight='bold')
ax.set_xlabel('年龄')
ax.set_ylabel('密度')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('kde.png', dpi=150, bbox_inches='tight')
```

### 多组 KDE 对比

```python
fig, ax = plt.subplots(figsize=(12, 6))

for group, color in zip(['A', 'B', 'C'], PALETTE[:3]):
    subset = df[df['group'] == group]['value']
    sns.kdeplot(subset, fill=True, alpha=0.4, label=group, color=color, ax=ax)

ax.legend(title='渠道')
ax.set_title('各渠道订单金额密度对比', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('kde_grouped.png', dpi=150, bbox_inches='tight')
```

### 双变量 KDE（2D 密度图）

```python
fig, ax = plt.subplots(figsize=(10, 8))

sns.kdeplot(data=df, x='feature_a', y='feature_b',
            fill=True, cmap='Blues', thresh=0.1, levels=10, ax=ax)

ax.set_title('用户行为特征二维密度分布', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('kde_2d.png', dpi=150, bbox_inches='tight')
```

---

## 五、高级场景

### 直方图 + 统计线（均值/中位数）

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(df['value'], bins=30, color='#3b82f6', edgecolor='white', alpha=0.7)

mean_val = df['value'].mean()
median_val = df['value'].median()

ax.axvline(mean_val, color='#ef4444', linestyle='--', linewidth=2, label=f'均值: {mean_val:.1f}')
ax.axvline(median_val, color='#10b981', linestyle='-.', linewidth=2, label=f'中位数: {median_val:.1f}')

ax.legend()
ax.set_title('订单金额分布（含统计线）', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('hist_stats.png', dpi=150, bbox_inches='tight')
```

### 箱线图 + 散点叠加（展示原始数据）

```python
fig, ax = plt.subplots(figsize=(12, 6))

# 箱线图
sns.boxplot(data=df, x='category', y='value',
            palette=PALETTE, width=0.5, ax=ax)

# 散点叠加（带抖动）
sns.stripplot(data=df, x='category', y='value',
              size=3, alpha=0.3, color='#1f2937', ax=ax)

ax.set_title('各品类订单金额分布（含原始数据点）', fontsize=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('box_strip.png', dpi=150, bbox_inches='tight')
```

### 分布对比：直方图 vs 箱线图 vs 小提琴图

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 直方图
axes[0].hist(df['value'], bins=30, color='#3b82f6', edgecolor='white', alpha=0.7)
axes[0].set_title('直方图')
axes[0].set_xlabel('值')
axes[0].set_ylabel('频数')

# 箱线图
axes[1].boxplot(df['value'], patch_artist=True)
axes[1].set_title('箱线图')
axes[1].set_ylabel('值')

# 小提琴图
sns.violinplot(y=df['value'], ax=axes[2], color='#3b82f6')
axes[2].set_title('小提琴图')
axes[2].set_ylabel('值')

for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('distribution_compare.png', dpi=150, bbox_inches='tight')
```

---

## 六、强制规范

### ✅ MUST DO

- **直方图必须指定 bins 或让算法自动选择**，避免使用默认值
- **箱线图必须标注异常值定义**（默认 1.5×IQR，可调整）
- **多组分布对比时，使用相同的 Y 轴范围**
- **中位数线必须清晰可见**（颜色对比、线宽）
- **直方图柱子之间必须有白色边框**（避免视觉混淆）
- **KDE 曲线必须有标签说明**（密度 vs 概率）

### ❌ MUST NOT

- 不在直方图上省略 X 轴标签（值范围）
- 不用箱线图展示类别 > 20 的数据（改为聚合或筛选）
- 不在小提琴图中隐藏统计量（至少显示中位数）
- 不用 3D 直方图
- 不忽略异常值的解释（是什么原因？是否需要排除？）
- 不在密度图中使用 fill=False（无法直观比较）

---

## 七、行业最佳实践

### 电商：订单金额分布

```python
# 典型电商订单金额呈长尾分布，用对数 X 轴
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(df['order_amount'], bins=50, color='#3b82f6', edgecolor='white', alpha=0.7)
ax.set_xscale('log')  # 对数轴

ax.set_title('订单金额分布（对数轴）', fontsize=15, fontweight='bold')
ax.set_xlabel('金额（元，对数刻度）')
ax.set_ylabel('订单数')

plt.tight_layout()
plt.savefig('order_amount_log.png', dpi=150, bbox_inches='tight')
```

### 金融：收益率分布

```python
# 收益率通常接近正态，检查肥尾
fig, ax = plt.subplots(figsize=(10, 6))

sns.histplot(df['return'], bins=50, kde=True, color='#3b82f6', ax=ax)

# 添加正态分布参考
from scipy import stats
x = np.linspace(df['return'].min(), df['return'].max(), 100)
y = stats.norm.pdf(x, df['return'].mean(), df['return'].std())
ax.plot(x, y * len(df) * (x[1] - x[0]), 'r--', label='正态分布参考')

ax.legend()
ax.set_title('日收益率分布 vs 正态分布', fontsize=15, fontweight='bold')

plt.tight_layout()
plt.savefig('return_distribution.png', dpi=150, bbox_inches='tight')
```

### 运维：响应时间分布

```python
# P50, P90, P99 分位线
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(df['response_time'], bins=50, color='#3b82f6', edgecolor='white', alpha=0.7)

p50 = df['response_time'].quantile(0.5)
p90 = df['response_time'].quantile(0.9)
p99 = df['response_time'].quantile(0.99)

ax.axvline(p50, color='#10b981', linestyle='--', linewidth=2, label=f'P50: {p50:.0f}ms')
ax.axvline(p90, color='#f59e0b', linestyle='--', linewidth=2, label=f'P90: {p90:.0f}ms')
ax.axvline(p99, color='#ef4444', linestyle='--', linewidth=2, label=f'P99: {p99:.0f}ms')

ax.legend()
ax.set_title('API 响应时间分布', fontsize=15, fontweight='bold')
ax.set_xlabel('响应时间（ms）')
ax.set_ylabel('请求数')

plt.tight_layout()
plt.savefig('response_time_p99.png', dpi=150, bbox_inches='tight')
```

---

## 八、常见问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 直方图柱子太少/太多 | bins 不合适 | 使用 FD 公式或手动调整 |
| 箱线图异常值过多 | 数据本身有极端值 | 检查数据质量；可调高异常阈值 |
| 多组分布无法比较 | Y 轴范围不同 | 设置 `sharey=True` 或手动统一 |
| KDE 曲线超出数据范围 | 核密度估计外推 | 设置 `clip=(min, max)` |
| 小提琴图太拥挤 | 类别太多 | 改用箱线图或分面展示 |
| 直方图右偏严重 | 长尾分布 | 使用对数 X 轴 |
