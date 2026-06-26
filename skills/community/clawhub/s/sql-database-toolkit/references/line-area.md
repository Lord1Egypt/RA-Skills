# 折线图 & 面积图

适用场景：时间序列趋势、连续变量变化。

---

## 基础折线图

```python
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# df 列：date（datetime）, value（数值）
fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(df['date'], df['value'],
        color='#3b82f6', linewidth=2,
        marker='o', markersize=4, markerfacecolor='white', markeredgewidth=2)

# 标注最大值和最小值
max_idx = df['value'].idxmax()
min_idx = df['value'].idxmin()
ax.annotate(f"最高: {df.loc[max_idx,'value']:,.0f}",
            xy=(df.loc[max_idx,'date'], df.loc[max_idx,'value']),
            xytext=(10, 10), textcoords='offset points',
            fontsize=9, color='#10b981')
ax.annotate(f"最低: {df.loc[min_idx,'value']:,.0f}",
            xy=(df.loc[min_idx,'date'], df.loc[min_idx,'value']),
            xytext=(10, -15), textcoords='offset points',
            fontsize=9, color='#ef4444')

ax.set_title('每日订单量趋势', fontsize=15, fontweight='bold', pad=12)
ax.set_xlabel('日期', fontsize=11)
ax.set_ylabel('订单量', fontsize=11)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('line_chart.png', dpi=150, bbox_inches='tight')
```

---

## 多系列折线图（对比）

```python
PALETTE = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']

fig, ax = plt.subplots(figsize=(12, 5))

for i, col in enumerate(['series_a', 'series_b', 'series_c']):
    ax.plot(df['date'], df[col],
            label=col, color=PALETTE[i], linewidth=2)

ax.legend(loc='upper left', framealpha=0.9)
ax.set_title('多渠道订单量对比', fontsize=15, fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('multi_line.png', dpi=150, bbox_inches='tight')
```

---

## 面积图（强调累计/量级）

```python
fig, ax = plt.subplots(figsize=(12, 5))

ax.fill_between(df['date'], df['value'],
                alpha=0.3, color='#3b82f6')
ax.plot(df['date'], df['value'],
        color='#3b82f6', linewidth=2)

ax.set_title('累计用户增长', fontsize=15, fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('area_chart.png', dpi=150, bbox_inches='tight')
```

---

## 折线图 + 柱状图组合（双轴）

适用：同时展示绝对值（柱）和比率（线），如销售额 + 增长率。

```python
fig, ax1 = plt.subplots(figsize=(12, 5))
ax2 = ax1.twinx()

# 柱状图（左轴）
bars = ax1.bar(df['month'], df['revenue'],
               color='#3b82f6', alpha=0.7, width=0.6, label='销售额')
ax1.set_ylabel('销售额（万元）', color='#3b82f6')
ax1.tick_params(axis='y', labelcolor='#3b82f6')

# 折线图（右轴）
line = ax2.plot(df['month'], df['growth_rate'],
                color='#ef4444', linewidth=2, marker='o',
                markersize=5, label='增长率')
ax2.set_ylabel('增长率（%）', color='#ef4444')
ax2.tick_params(axis='y', labelcolor='#ef4444')
ax2.axhline(y=0, color='#ef4444', linestyle='--', alpha=0.3)

# 合并图例
lines = [bars] + line
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

ax1.set_title('月度销售额与增长率', fontsize=15, fontweight='bold')
ax1.spines['top'].set_visible(False)

plt.tight_layout()
plt.savefig('combo_chart.png', dpi=150, bbox_inches='tight')
```

---

## 注意事项
- 时间轴数据点超过 60 个时，去掉 `marker`，避免密集
- 多系列超过 5 条时，考虑用小多图（facet）代替
- 双 Y 轴要谨慎：确保两个指标有真实业务关联，并在标题中说明
