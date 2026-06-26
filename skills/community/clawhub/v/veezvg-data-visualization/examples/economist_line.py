"""
The Economist 风格 - 折线图（时间序列）
=====================================
核心做法：重点系列上色，其他灰化，末端文字标注代替图例
subplots_adjust(right=0.88) 给末端系列名留空间
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties

font_path = '/System/Library/Fonts/STHeiti Light.ttc'
fp      = FontProperties(fname=font_path)
fp_bold = FontProperties(fname=font_path, weight='bold')

ECON_RED   = '#E3120B'
ECON_BLUE  = '#006BA2'
ECON_GREY  = '#758D99'
ECON_GRID  = '#A8BAC4'
TEXT_DARK  = '#121212'
TEXT_SUB   = '#555555'

LEFT_X     = 0.14
RED_LINE_Y = 0.970
TAG_W, TAG_H = 0.055, 0.030
TITLE_Y    = 0.920
SUBTITLE_Y = 0.860
SOURCE_Y   = 0.025

# ── 数据 ─────────────────────────────────────────────
years    = list(range(2019, 2024))
shanghai = [6.94, 7.24, 7.80, 7.96, 8.48]
beijing  = [6.79, 6.97, 7.50, 7.77, 8.18]
national = [4.24, 4.38, 4.74, 4.93, 5.18]
series = [
    ('上海',     shanghai, ECON_RED),    # 重点
    ('北京',     beijing,  ECON_BLUE),   # 重点
    ('全国均值', national, ECON_GREY),   # 灰化对照
]

# ── 画布 ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
# right=0.88 给末端系列名留空间
fig.subplots_adjust(left=LEFT_X, right=0.88, top=0.76, bottom=0.12)

for name, vals, color in series:
    ax.plot(years, vals, color=color, linewidth=2.5,
            marker='o', markersize=6, markerfacecolor=color,
            markeredgecolor='white', markeredgewidth=1.5, zorder=3)
    # 末端系列名（替代图例）
    ax.text(years[-1] + 0.12, vals[-1], name,
            fontproperties=fp_bold, fontsize=11, color=color,
            va='center', ha='left')

ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], fontsize=11, color=TEXT_DARK)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0f}'))
ax.set_xlim(years[0] - 0.3, years[-1] + 1.2)
ax.set_ylim(3, 10)

# 边框 + 网格
for spine in ax.spines.values():
    spine.set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color('#444444')
ax.spines['bottom'].set_linewidth(1.2)
ax.yaxis.grid(True, color=ECON_GRID, linewidth=1.0, zorder=0)
ax.xaxis.grid(False)
ax.set_axisbelow(True)
ax.tick_params(axis='both', length=0, labelsize=10, labelcolor=ECON_GREY)
ax.tick_params(axis='x', labelsize=11, labelcolor=TEXT_DARK)

# 红线 + 红色方块 tag
ax.plot([LEFT_X, 1.0], [RED_LINE_Y, RED_LINE_Y],
        transform=fig.transFigure, clip_on=False,
        color=ECON_RED, linewidth=2.5, solid_capstyle='butt', zorder=20)
ax.add_patch(mpatches.Rectangle(
    xy=(LEFT_X, RED_LINE_Y - TAG_H), width=TAG_W, height=TAG_H,
    facecolor=ECON_RED, edgecolor='none',
    transform=fig.transFigure, clip_on=False, zorder=20))

# 标题 / 副标题 / 来源
fig.text(LEFT_X, TITLE_Y, '上海、北京收入持续拉开与全国均值差距',
         fontproperties=fp_bold, fontsize=13, color=TEXT_DARK, va='top', ha='left')
fig.text(LEFT_X, SUBTITLE_Y, '城镇居民人均可支配收入，2019–2023，万元',
         fontproperties=fp, fontsize=10.5, color=TEXT_SUB, va='top', ha='left')
fig.text(LEFT_X, SOURCE_Y, '来源：上海/北京市统计局、国家统计局',
         fontproperties=fp, fontsize=9, color=ECON_GREY, va='bottom', ha='left')

plt.savefig('output_economist_line.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
