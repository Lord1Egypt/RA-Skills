# 多图面板 / Dashboard

适用场景：需要在一张图里展示多个维度，或生成完整的数据报告。

---

## matplotlib 多图面板

```python
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import pandas as pd
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(16, 10))
fig.suptitle('业务数据周报', fontsize=20, fontweight='bold', y=0.98)

# 使用 GridSpec 灵活布局
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

# ── 左上（跨2列）：趋势折线图 ──
ax1 = fig.add_subplot(gs[0, :2])
ax1.plot(df_trend['date'], df_trend['orders'], color='#3b82f6', linewidth=2)
ax1.fill_between(df_trend['date'], df_trend['orders'], alpha=0.1, color='#3b82f6')
ax1.set_title('近30天订单量趋势', fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(axis='x', rotation=45)

# ── 右上：KPI 卡片 ──
ax2 = fig.add_subplot(gs[0, 2])
ax2.axis('off')
kpis = [
    ('总订单量', '12,450', '+8.3%', '#10b981'),
    ('总营收', '¥234万', '+12.1%', '#10b981'),
    ('客单价', '¥188', '-2.4%', '#ef4444'),
]
for i, (label, value, change, color) in enumerate(kpis):
    y_pos = 0.85 - i * 0.3
    ax2.text(0.1, y_pos, label, fontsize=10, color='#6b7280', transform=ax2.transAxes)
    ax2.text(0.1, y_pos - 0.1, value, fontsize=18, fontweight='bold', transform=ax2.transAxes)
    ax2.text(0.7, y_pos - 0.1, change, fontsize=12, color=color, transform=ax2.transAxes)
ax2.set_title('核心指标', fontweight='bold')

# ── 左下：品类条形图 ──
ax3 = fig.add_subplot(gs[1, 0])
df_cat_sorted = df_cat.sort_values('value', ascending=True)
ax3.barh(df_cat_sorted['name'], df_cat_sorted['value'], color='#3b82f6', height=0.6)
ax3.set_title('品类销售额 Top 5', fontweight='bold')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# ── 中下：金额分布直方图 ──
ax4 = fig.add_subplot(gs[1, 1])
ax4.hist(df_orders['amount'], bins=20, color='#f59e0b', edgecolor='white')
ax4.set_title('订单金额分布', fontweight='bold')
ax4.set_xlabel('金额（元）')
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

# ── 右下：渠道占比堆叠 ──
ax5 = fig.add_subplot(gs[1, 2])
bottom = np.zeros(len(df_channel))
for col, color in zip(['pc', 'mobile', 'mini'], ['#3b82f6', '#10b981', '#f59e0b']):
    ax5.bar(df_channel['month'], df_channel[col], bottom=bottom,
            label=col, color=color, edgecolor='white')
    bottom += df_channel[col].values
ax5.legend(fontsize=8)
ax5.set_title('渠道构成', fontweight='bold')
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)

plt.savefig('weekly_report.png', dpi=150, bbox_inches='tight')
print("报告已保存：weekly_report.png")
```

---

## 自动化报告生成（SQL → 图表 → PDF）

```python
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sqlite3
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

conn = sqlite3.connect('mydb.sqlite')

# 查询数据
df_trend = pd.read_sql("""
    SELECT DATE(created_at) as date, COUNT(*) as orders, SUM(amount) as revenue
    FROM orders WHERE created_at >= DATE('now', '-30 days')
    GROUP BY DATE(created_at) ORDER BY date
""", conn)

df_cat = pd.read_sql("""
    SELECT category, SUM(amount) as revenue
    FROM orders WHERE created_at >= DATE('now', '-30 days')
    GROUP BY category ORDER BY revenue DESC LIMIT 10
""", conn)

conn.close()

# 生成 PDF 报告
with PdfPages(f'report_{datetime.now().strftime("%Y%m%d")}.pdf') as pdf:

    # 第1页：趋势
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(pd.to_datetime(df_trend['date']), df_trend['revenue'],
            color='#3b82f6', linewidth=2)
    ax.set_title('近30天营收趋势', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    pdf.savefig(fig)
    plt.close()

    # 第2页：品类排名
    fig, ax = plt.subplots(figsize=(10, 7))
    df_sorted = df_cat.sort_values('revenue', ascending=True)
    ax.barh(df_sorted['category'], df_sorted['revenue'], color='#10b981')
    ax.set_title('品类营收排名', fontsize=14, fontweight='bold')
    plt.tight_layout()
    pdf.savefig(fig)
    plt.close()

    # PDF 元数据
    d = pdf.infodict()
    d['Title'] = '业务数据报告'
    d['Author'] = 'SQL DataViz'
    d['CreationDate'] = datetime.now()

print(f"PDF 报告已生成：report_{datetime.now().strftime('%Y%m%d')}.pdf")
```

---

## 布局建议

| 图表数量 | 推荐布局 | figsize |
|---------|---------|---------|
| 2 张 | 1×2 或 2×1 | (14, 5) 或 (8, 10) |
| 4 张 | 2×2 | (14, 10) |
| 6 张 | 2×3 或 3×2 | (16, 10) |
| 混合（大+小） | GridSpec 自定义 | 按需 |

**原则：** 最重要的图放左上角（视线自然落点），KPI 卡片放右上角，细节图放下方。
