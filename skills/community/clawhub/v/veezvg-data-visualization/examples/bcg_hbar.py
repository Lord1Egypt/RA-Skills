"""
BCG 风格 - 水平柱状图
=====================
适用：调研报告、类别排行比较
标题含样本量 (N=X)，主色绿色 #2ca02c，无网格
"""
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# ── 字体 ──────────────────────────────────────────────
font_path = '/System/Library/Fonts/STHeiti Light.ttc'
fp = FontProperties(fname=font_path)

# ── 配色 ──────────────────────────────────────────────
COLOR_MAIN = '#2ca02c'

# ── 数据（替换为实际数据）──────────────────────────────
labels = ['上海', '北京', '杭州', '广州', '深圳', '武汉']
values = [8.48, 8.18, 8.06, 8.05, 7.69, 6.17]
N = 6

# ── 画布 ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('white')
fig.subplots_adjust(left=0.10, right=0.92, top=0.88, bottom=0.12)

# ── 绘图 ──────────────────────────────────────────────
bars = ax.barh(range(len(labels)), values, color=COLOR_MAIN, height=0.58)
ax.set_yticks(range(len(labels)))
ax.set_yticklabels(labels, fontproperties=fp, fontsize=14)
ax.set_xlabel('人均可支配收入（万元）', fontproperties=fp, fontsize=12)
ax.set_xlim(0, max(values) * 1.25)
ax.tick_params(axis='x', labelsize=11)
ax.set_title(f'2023年六城市城镇居民人均可支配收入 (N={N})',
             fontproperties=fp, fontsize=17, fontweight='bold', pad=14)

# ── 边框：去除上、右、下，仅保留左轴 ────────────────────
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['left'].set_linewidth(1)
ax.grid(False)

# ── 数据标签 ───────────────────────────────────────────
for bar, val in zip(bars, values):
    ax.text(val + max(values) * 0.015, bar.get_y() + bar.get_height() / 2,
            f'{val:.2f}万元', va='center', fontproperties=fp, fontsize=12)

# ── 来源注脚 ───────────────────────────────────────────
fig.text(0.10, 0.02, '来源：各城市2023年国民经济和社会发展统计公报',
         fontproperties=fp, fontsize=9, color='#888888', va='bottom')

plt.savefig('output_bcg_hbar.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
