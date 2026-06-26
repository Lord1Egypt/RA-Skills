"""
McKinsey 风格 - 分组垂直柱状图（Top performers vs Others）
========================================================
参考：McKinsey Global Survey Exhibit 7
最常用的麦肯锡图表类型：双系列用亮青 vs 浅灰对照
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties

font_path = '/System/Library/Fonts/STHeiti Light.ttc'
fp      = FontProperties(fname=font_path)
fp_bold = FontProperties(fname=font_path, weight='bold')

# ── McKinsey 配色（2025 真实报告提取）──────────────
MCK_CYAN = '#2CBDEF'   # Top performers
MCK_GRAY = '#D4D4D4'   # Others
MCK_DARK = '#051C2C'
MCK_META = '#8C8C8C'
MCK_LINE = '#D4D4D4'

# ── 布局常量 ──────────────────────────────────────────
LEFT_X       = 0.08
EXHIBIT_Y    = 0.96
SEP_LINE_Y   = 0.935
TITLE_Y      = 0.90
SUBTITLE_Y   = 0.78
LEGEND_RIGHT = 0.82
SOURCE_Y     = 0.04


def apply_mckinsey_frame(fig, ax, exhibit_label, title, subtitle,
                         legend_items, source):
    """套用麦肯锡风格的外框：Exhibit 标签、分隔线、标题、图例、来源。"""
    fig.text(LEFT_X, EXHIBIT_Y, exhibit_label,
             fontproperties=fp, fontsize=10, color=MCK_META, va='top', ha='left')
    ax.plot([LEFT_X, 0.96], [SEP_LINE_Y, SEP_LINE_Y],
            transform=fig.transFigure, clip_on=False,
            color=MCK_LINE, linewidth=0.8, zorder=20)
    fig.text(LEFT_X, TITLE_Y, title,
             fontproperties=fp_bold, fontsize=16, color=MCK_DARK, va='top', ha='left')
    fig.text(LEFT_X, SUBTITLE_Y, subtitle,
             fontproperties=fp_bold, fontsize=11.5, color=MCK_DARK, va='top', ha='left')
    legend_y = SUBTITLE_Y + 0.02
    for name, color in legend_items:
        ax.add_patch(mpatches.Rectangle(
            xy=(LEGEND_RIGHT, legend_y - 0.018), width=0.02, height=0.016,
            facecolor=color, edgecolor='none',
            transform=fig.transFigure, clip_on=False, zorder=20))
        fig.text(LEGEND_RIGHT + 0.026, legend_y - 0.010, name,
                 fontproperties=fp, fontsize=10, color=MCK_DARK, va='center', ha='left')
        legend_y -= 0.028
    fig.text(LEFT_X, SOURCE_Y, f'Source: {source}',
             fontproperties=fp, fontsize=9, color=MCK_DARK, va='bottom', ha='left')


def style_mckinsey_axes(ax, show_bottom=True):
    """通用轴处理：去除所有边框、关闭网格、隐藏 y 轴刻度。"""
    for spine in ax.spines.values():
        spine.set_visible(False)
    if show_bottom:
        ax.spines['bottom'].set_visible(True)
        ax.spines['bottom'].set_color(MCK_LINE)
        ax.spines['bottom'].set_linewidth(0.8)
    ax.grid(False)
    ax.tick_params(axis='both', length=0, labelsize=10, labelcolor=MCK_DARK)
    ax.set_yticks([])


# ── 数据 ───────────────────────────────────────────
categories = ['Less than\n5% changed', '5% to less\nthan 10%', '10% to less\nthan 20%',
              '20% to less\nthan 30%', '30% to less\nthan 50%', '50% to less\nthan 75%',
              '75% or\nmore']
top_perf = [8, 16, 23, 17, 9, 7, 12]
others   = [20, 30, 26, 11, 5, 2, 0]

fig, ax = plt.subplots(figsize=(11, 7.5))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=LEFT_X, right=0.96, top=0.70, bottom=0.20)

x = list(range(len(categories)))
width = 0.35   # ⚠️ 窄柱（0.32~0.38），不要用 matplotlib 默认 0.8
ax.bar([i - width/2 for i in x], top_perf, width=width, color=MCK_CYAN, zorder=3)
ax.bar([i + width/2 for i in x], others,   width=width, color=MCK_GRAY, zorder=3)

# 柱顶数字（粗体深色）
for i, (t, o) in enumerate(zip(top_perf, others)):
    ax.text(i - width/2, t + 1, f'{t}', ha='center', va='bottom',
            fontproperties=fp_bold, fontsize=11, color=MCK_DARK)
    ax.text(i + width/2, o + 1, f'{o}', ha='center', va='bottom',
            fontproperties=fp_bold, fontsize=11, color=MCK_DARK)

ax.set_xticks(x)
ax.set_xticklabels(categories, fontproperties=fp, fontsize=10, color=MCK_DARK)
ax.set_ylim(0, max(max(top_perf), max(others)) * 1.3)

style_mckinsey_axes(ax)
apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 7',
    title='Top economic performers are much more likely than their peers\nto significantly reallocate resources from year to year.',
    subtitle='Share of annual budget that was reallocated to different\nbusiness areas this year, % of respondents',
    legend_items=[('Top performers', MCK_CYAN), ('Others', MCK_GRAY)],
    source='McKinsey Global Survey on competitive advantage, 1,257 participants')

plt.savefig('output_mckinsey_grouped_vbar.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
