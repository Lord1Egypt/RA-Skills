# 图表类型指南

本指南详细介绍 PyThesisPlot 支持的各种图表类型及其适用场景。

## 目录

- [折线图 (Line)](#折线图-line)
- [柱状图 (Bar)](#柱状图-bar)
- [散点图 (Scatter)](#散点图-scatter)
- [箱线图 (Box)](#箱线图-box)
- [热力图 (Heatmap)](#热力图-heatmap)
- [面积图 (Area)](#面积图-area)
- [饼图 (Pie)](#饼图-pie)
- [直方图 (Histogram)](#直方图-histogram)
- [组合图 (Combo)](#组合图-combo)

---

## 折线图 (Line)

### 适用场景

- 展示数据随时间的变化趋势
- 比较多个数据系列的趋势
- 显示连续数据的波动

### 代码示例

```python
import numpy as np
import matplotlib.pyplot as plt
from pythesisplot import setup_thesis_style

setup_thesis_style()

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y1, linewidth=2, label='Series 1', color='#2E5AAC')
ax.plot(x, y2, linewidth=2, label='Series 2', color='#D9534F', linestyle='--')

ax.set_xlabel('Time (s)', fontsize=12)
ax.set_ylabel('Amplitude', fontsize=12)
ax.legend(loc='best')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('line_chart.pdf', bbox_inches='tight')
```

### 最佳实践

- 线宽建议 1.5-2.5
- 多线图使用不同线型区分（实线、虚线、点划线）
- 避免超过 5 条数据线
- 添加标记点突出关键数据

---

## 柱状图 (Bar)

### 适用场景

- 比较不同类别的数据大小
- 展示离散数据的分布
- 显示计数或百分比

### 代码示例

```python
import numpy as np
import matplotlib.pyplot as plt
from pythesisplot import setup_thesis_style

setup_thesis_style()

categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(categories, values, color='#2E5AAC', edgecolor='black', linewidth=0.5)

# 添加数值标签
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

ax.set_xlabel('Category', fontsize=12)
ax.set_ylabel('Value', fontsize=12)
ax.set_title('Bar Chart Example', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('bar_chart.pdf', bbox_inches='tight')
```

### 分组柱状图

```python
x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x - width/2, values1, width, label='Group 1', color='#2E5AAC')
ax.bar(x + width/2, values2, width, label='Group 2', color='#5CB85C')

ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
```

### 最佳实践

- 柱子宽度适中，不要太细或太粗
- 分组柱状图保持适当间距
- 数值标签清晰可读
- 考虑使用水平柱状图当类别名称较长

---

## 散点图 (Scatter)

### 适用场景

- 展示两个变量的相关性
- 发现数据中的聚类或异常值
- 显示数据分布密度

### 代码示例

```python
import numpy as np
import matplotlib.pyplot as plt
from pythesisplot import setup_thesis_style

setup_thesis_style()

np.random.seed(42)
n = 100
x = np.random.randn(n)
y = 2 * x + np.random.randn(n) * 0.5

fig, ax = plt.subplots(figsize=(7, 6))
scatter = ax.scatter(x, y, alpha=0.6, s=50, c='#2E5AAC', 
                     edgecolors='black', linewidth=0.5)

ax.set_xlabel('Variable X', fontsize=12)
ax.set_ylabel('Variable Y', fontsize=12)
ax.set_title('Scatter Plot', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('scatter.pdf', bbox_inches='tight')
```

### 带颜色映射的散点图

```python
colors = np.random.rand(n)
sizes = 100 * np.random.rand(n)

scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.6, 
                     cmap='viridis', edgecolors='black', linewidth=0.5)
plt.colorbar(scatter, ax=ax, label='Color Scale')
```

### 最佳实践

- 点的大小适中，避免重叠
- 使用透明度(alpha)处理密集数据
- 添加趋势线展示相关性
- 颜色映射选择色盲友好的配色

---

## 箱线图 (Box)

### 适用场景

- 展示数据分布特征
- 比较多组数据的统计特性
- 识别异常值

### 代码示例

```python
import numpy as np
import matplotlib.pyplot as plt
from pythesisplot import setup_thesis_style

setup_thesis_style()

np.random.seed(42)
data = [
    np.random.normal(100, 10, 200),
    np.random.normal(90, 20, 200),
    np.random.normal(95, 15, 200),
    np.random.normal(110, 12, 200)
]
labels = ['Group A', 'Group B', 'Group C', 'Group D']

fig, ax = plt.subplots(figsize=(8, 6))
bp = ax.boxplot(data, labels=labels, patch_artist=True, notch=True)

colors = ['#2E5AAC', '#5CB85C', '#F0AD4E', '#D9534F']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_ylabel('Value', fontsize=12)
ax.set_title('Box Plot', fontsize=14, fontweight='bold')
ax.yaxis.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('boxplot.pdf', bbox_inches='tight')
```

### 最佳实践

- 使用不同颜色区分组
- 添加 notch 显示中位数置信区间
- 保持箱体透明度避免遮挡
- 添加网格线便于读数

---

## 热力图 (Heatmap)

### 适用场景

- 展示相关性矩阵
- 显示二维数据的密度分布
- 展示表格数据的数值大小

### 代码示例

```python
import numpy as np
import matplotlib.pyplot as plt
from pythesisplot import setup_thesis_style

setup_thesis_style()

# 生成相关性矩阵
np.random.seed(42)
data = np.random.randn(8, 8)
corr_matrix = np.corrcoef(data)

labels = [f'Var{i+1}' for i in range(8)]

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(corr_matrix, cmap='RdYlBu_r', aspect='auto', vmin=-1, vmax=1)

# 添加颜色条
cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Correlation', fontsize=11)

# 设置刻度
ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.set_yticklabels(labels)

# 添加数值
for i in range(len(labels)):
    for j in range(len(labels)):
        text = ax.text(j, i, f'{corr_matrix[i, j]:.2f}',
                      ha="center", va="center", 
                      color="white" if abs(corr_matrix[i, j]) > 0.5 else "black",
                      fontsize=9)

ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('heatmap.pdf', bbox_inches='tight')
```

### 最佳实践

- 选择合适的 colormap（RdYlBu_r 适合相关性）
- 添加数值标签便于精确读数
- 根据数值大小调整标签颜色
- 设置合适的 colorbar 范围

---

## 面积图 (Area)

### 适用场景

- 展示累积数据
- 显示部分与整体的关系
- 强调数量随时间的变化

### 代码示例

```python
import numpy as np
import matplotlib.pyplot as plt
from pythesisplot import setup_thesis_style

setup_thesis_style()

x = np.arange(10)
y1 = np.array([1, 3, 2, 4, 3, 5, 4, 6, 5, 7])
y2 = np.array([2, 2, 3, 3, 4, 4, 5, 5, 6, 6])

fig, ax = plt.subplots(figsize=(8, 5))
ax.fill_between(x, y1, alpha=0.5, color='#2E5AAC', label='Series 1')
ax.fill_between(x, y2, alpha=0.5, color='#5CB85C', label='Series 2')
ax.plot(x, y1, color='#2E5AAC', linewidth=2)
ax.plot(x, y2, color='#5CB85C', linewidth=2)

ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.legend(loc='best')

plt.tight_layout()
plt.savefig('area_chart.pdf', bbox_inches='tight')
```

---

## 饼图 (Pie)

### 适用场景

- 展示部分占整体的比例
- 强调简单构成（建议不超过 6 个类别）

### 代码示例

```python
import matplotlib.pyplot as plt
from pythesisplot import setup_thesis_style

setup_thesis_style()

sizes = [30, 25, 20, 15, 10]
labels = ['A', 'B', 'C', 'D', 'E']
colors = ['#2E5AAC', '#5CB85C', '#F0AD4E', '#D9534F', '#6C757D']

fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                    autopct='%1.1f%%', startangle=90,
                                    explode=[0.05 if i == 0 else 0 for i in range(5)])

ax.set_title('Pie Chart', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('pie_chart.pdf', bbox_inches='tight')
```

### 最佳实践

- 类别不超过 6 个
- 突出显示重要部分
- 添加百分比标签
- 考虑使用柱状图替代（更清晰）

---

## 直方图 (Histogram)

### 适用场景

- 展示数据分布
- 估计概率密度

### 代码示例

```python
import numpy as np
import matplotlib.pyplot as plt
from pythesisplot import setup_thesis_style

setup_thesis_style()

np.random.seed(42)
data = np.random.randn(1000)

fig, ax = plt.subplots(figsize=(8, 5))
n, bins, patches = ax.hist(data, bins=30, color='#2E5AAC', 
                           edgecolor='black', alpha=0.7, density=True)

# 添加核密度估计曲线
from scipy import stats
kde = stats.gaussian_kde(data)
x_range = np.linspace(data.min(), data.max(), 100)
ax.plot(x_range, kde(x_range), color='#D9534F', linewidth=2, label='KDE')

ax.set_xlabel('Value', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.legend()

plt.tight_layout()
plt.savefig('histogram.pdf', bbox_inches='tight')
```

---

## 组合图 (Combo)

### 适用场景

- 同时展示不同量纲的数据
- 比较多维度的关系

### 代码示例

```python
import numpy as np
import matplotlib.pyplot as plt
from pythesisplot import setup_thesis_style

setup_thesis_style()

x = np.arange(1, 6)
bar_data = [20, 35, 30, 35, 27]
line_data = [25, 32, 34, 20, 25]

fig, ax1 = plt.subplots(figsize=(8, 5))

# 柱状图
bars = ax1.bar(x, bar_data, color='#2E5AAC', alpha=0.7, label='Bar Data')
ax1.set_xlabel('Category', fontsize=12)
ax1.set_ylabel('Bar Values', fontsize=12, color='#2E5AAC')
ax1.tick_params(axis='y', labelcolor='#2E5AAC')

# 折线图
ax2 = ax1.twinx()
line = ax2.plot(x, line_data, color='#D9534F', marker='o', 
                linewidth=2, label='Line Data')
ax2.set_ylabel('Line Values', fontsize=12, color='#D9534F')
ax2.tick_params(axis='y', labelcolor='#D9534F')

# 合并图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')

ax1.set_title('Combo Chart', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('combo_chart.pdf', bbox_inches='tight')
```

---

## 图表选择决策树

```
数据类型
├── 时间序列/趋势 → 折线图
├── 分类对比
│   ├── 单变量 → 柱状图
│   └── 多变量 → 分组柱状图/堆叠柱状图
├── 相关性
│   ├── 两变量 → 散点图
│   └── 多变量 → 热力图/散点图矩阵
├── 分布
│   ├── 单组 → 直方图/箱线图
│   └── 多组比较 → 箱线图/小提琴图
├── 构成/占比
│   ├── 静态 → 饼图/堆叠柱状图
│   └── 动态变化 → 堆叠面积图
└── 复杂关系 → 组合图
```
