# 条形图 & 横向条形图

适用场景：分类比较、排名展示。

---

## 纵向条形图（类别 ≤ 10）

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(df['category'], df['value'],
              color='#3b82f6', width=0.6, edgecolor='white')

# 柱顶标注数值
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + max(df['value'])*0.01,
            f'{h:,.0f}', ha='center', va='bottom', fontsize=10)

ax.set_title('各品类销售额', fontsize=15, fontweight='bold', pad=12)
ax.set_xlabel('品类')
ax.set_ylabel('销售额（万元）')
ax.set_ylim(0, max(df['value']) * 1.15)  # 留出标注空间
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('bar_chart.png', dpi=150, bbox_inches='tight')
```

---

## 横向条形图（排名 / 类别多 / 名称长）

```python
# 按值排序，最大值在顶部
df_sorted = df.sort_values('value', ascending=True)

fig, ax = plt.subplots(figsize=(10, max(6, len(df_sorted) * 0.4)))

# 高亮 Top 1
colors = ['#ef4444' if i == len(df_sorted)-1 else '#3b82f6'
          for i in range(len(df_sorted))]

bars = ax.barh(df_sorted['name'], df_sorted['value'],
               color=colors, height=0.6)

# 右侧标注数值
for bar in bars:
    w = bar.get_width()
    ax.text(w + max(df_sorted['value'])*0.01, bar.get_y() + bar.get_height()/2,
            f'{w:,.0f}', va='center', fontsize=10)

ax.set_title('Top 用户消费排名', fontsize=15, fontweight='bold', pad=12)
ax.set_xlabel('消费金额（元）')
ax.set_xlim(0, max(df_sorted['value']) * 1.12)
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('bar_horizontal.png', dpi=150, bbox_inches='tight')
```

---

## 分组条形图（多系列对比）

```python
# df 列：month, group_a, group_b, group_c
categories = df['month'].tolist()
x = np.arange(len(categories))
width = 0.25
PALETTE = ['#3b82f6', '#10b981', '#f59e0b']

fig, ax = plt.subplots(figsize=(12, 6))

for i, (col, label) in enumerate([('group_a', 'PC端'), ('group_b', '移动端'), ('group_c', '小程序')]):
    offset = (i - 1) * width
    bars = ax.bar(x + offset, df[col], width, label=label,
                  color=PALETTE[i], edgecolor='white')

ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
ax.set_title('各渠道月度订单量对比', fontsize=15, fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('grouped_bar.png', dpi=150, bbox_inches='tight')
```

---

## 堆叠条形图（占比构成）

```python
fig, ax = plt.subplots(figsize=(12, 6))
PALETTE = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']

bottom = np.zeros(len(df))
for i, col in enumerate(['cat_a', 'cat_b', 'cat_c', 'cat_d']):
    ax.bar(df['month'], df[col], bottom=bottom,
           label=col, color=PALETTE[i], edgecolor='white', linewidth=0.5)
    bottom += df[col].values

ax.legend(loc='upper left')
ax.set_title('各品类月度销售额构成', fontsize=15, fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('stacked_bar.png', dpi=150, bbox_inches='tight')
```

---

## 百分比堆叠条形图

```python
# 先计算百分比
cols = ['cat_a', 'cat_b', 'cat_c']
df_pct = df[cols].div(df[cols].sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(12, 6))
bottom = np.zeros(len(df_pct))

for i, col in enumerate(cols):
    ax.bar(df['month'], df_pct[col], bottom=bottom,
           label=col, color=PALETTE[i], edgecolor='white')
    bottom += df_pct[col].values

ax.set_ylim(0, 100)
ax.set_ylabel('占比（%）')
ax.legend(loc='upper left')
ax.set_title('各品类月度销售额占比', fontsize=15, fontweight='bold')

plt.tight_layout()
plt.savefig('stacked_pct.png', dpi=150, bbox_inches='tight')
```
