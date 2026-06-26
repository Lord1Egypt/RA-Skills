"""
The Economist 风格 - 水平条形图
===============================
标志元素：顶部红线 + 左上红色方块 tag + 左对齐基准 + 底部 Source

关键技术：
- 红线/tag 用 fig.transFigure + clip_on=False 绘制（禁用 fig.add_axes）
- 分类标签用 blended_transform 对齐到 LEFT_X（避免伸出红线左端）
- 标题/副标题/来源全部左对齐到 LEFT_X = 0.14
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import blended_transform_factory

# ── 字体 ──────────────────────────────────────────────
font_path = '/System/Library/Fonts/STHeiti Light.ttc'
fp      = FontProperties(fname=font_path)
fp_bold = FontProperties(fname=font_path, weight='bold')

# ── Economist 配色 ───────────────────────────────────
ECON_RED   = '#E3120B'   # 顶部红线 + tag
ECON_BLUE  = '#006BA2'   # 主数据系列
ECON_GREY  = '#758D99'   # 来源注脚
ECON_GRID  = '#A8BAC4'   # 网格线
TEXT_DARK  = '#121212'
TEXT_SUB   = '#555555'

# ── 布局常量 ──────────────────────────────────────────
LEFT_X     = 0.14   # 左对齐基准，所有文字元素共用
RED_LINE_Y = 0.970
TAG_W, TAG_H = 0.055, 0.030
TITLE_Y    = 0.920
SUBTITLE_Y = 0.860
SOURCE_Y   = 0.025

# ── 数据 ──────────────────────────────────────────────
cities = ['上海', '北京', '杭州', '广州', '深圳', '武汉']
values = [8.48, 8.18, 8.06, 8.05, 7.69, 6.17]

# ── 画布 ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
# left=0.24 给外部分类标签留空间；标签本身 x=LEFT_X=0.14
fig.subplots_adjust(left=0.24, right=0.94, top=0.76, bottom=0.10)

# ── 绘图 ──────────────────────────────────────────────
y_pos = list(range(len(cities)))
bars  = ax.barh(y_pos, values, color=ECON_BLUE, height=0.55, zorder=3)

ax.set_yticks(y_pos)
ax.set_yticklabels([])   # ⚠️ 必须清空默认标签（会伸出 LEFT_X）
ax.set_xlim(0, max(values) * 1.25)
ax.tick_params(axis='both', length=0)
ax.tick_params(axis='x', labelsize=10, labelcolor=ECON_GREY)
ax.set_xlabel('（万元）', fontproperties=fp, fontsize=11, color=ECON_GREY, labelpad=8)

# ── 分类标签：blended_transform 让 x 用 figure 坐标对齐 LEFT_X ──
trans_label = blended_transform_factory(fig.transFigure, ax.transData)
for i, city in enumerate(cities):
    ax.text(LEFT_X, i, city, transform=trans_label,
            ha='left', va='center',
            fontproperties=fp, fontsize=13, color=TEXT_DARK, clip_on=False)

# ── 数据标签（条形右端）────────────────────────────────
for i, val in enumerate(values):
    ax.text(val + max(values) * 0.015, i, f'{val:.2f}万',
            va='center', fontproperties=fp, fontsize=11, color=TEXT_DARK)

# ── 边框：仅保留底部 ──────────────────────────────────
for spine in ax.spines.values():
    spine.set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color('#444444')
ax.spines['bottom'].set_linewidth(1.2)

# ── 网格：仅 x 方向（垂直网格）─────────────────────────
ax.xaxis.grid(True, color=ECON_GRID, linewidth=1.0, zorder=0)
ax.yaxis.grid(False)
ax.set_axisbelow(True)

# ════════════════════════════════════════════════════════
# 标志元素：红线 + 红色方块 tag
# ════════════════════════════════════════════════════════
# ① 红色横线：从 LEFT_X 到 figure 右边缘
ax.plot([LEFT_X, 1.0], [RED_LINE_Y, RED_LINE_Y],
        transform=fig.transFigure, clip_on=False,
        color=ECON_RED, linewidth=2.5, solid_capstyle='butt', zorder=20)

# ② 红色方块 tag：左边缘对齐 LEFT_X
ax.add_patch(mpatches.Rectangle(
    xy=(LEFT_X, RED_LINE_Y - TAG_H), width=TAG_W, height=TAG_H,
    facecolor=ECON_RED, edgecolor='none',
    transform=fig.transFigure, clip_on=False, zorder=20))

# ── 标题、副标题、来源（全部对齐 LEFT_X）────────────────
fig.text(LEFT_X, TITLE_Y,
         '上海、北京、杭州收入相近，均超全国均值逾五成',
         fontproperties=fp_bold, fontsize=13,
         color=TEXT_DARK, va='top', ha='left')
fig.text(LEFT_X, SUBTITLE_Y,
         '2023年城镇居民人均可支配收入，单位：万元',
         fontproperties=fp, fontsize=10.5,
         color=TEXT_SUB, va='top', ha='left')
fig.text(LEFT_X, SOURCE_Y,
         '来源：各城市2023年国民经济和社会发展统计公报',
         fontproperties=fp, fontsize=9,
         color=ECON_GREY, va='bottom', ha='left')

plt.savefig('output_economist_hbar.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
