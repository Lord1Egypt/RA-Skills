"""
McKinsey 风格 - 分组水平条形图
==============================
参考：McKinsey Exhibit 4
特征：类别名在左侧，x 轴在顶部（0~100%），双系列对照
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties

font_path = '/System/Library/Fonts/STHeiti Light.ttc'
fp      = FontProperties(fname=font_path)
fp_bold = FontProperties(fname=font_path, weight='bold')

MCK_CYAN = '#2CBDEF'; MCK_GRAY = '#D4D4D4'
MCK_DARK = '#051C2C'; MCK_META = '#8C8C8C'; MCK_LINE = '#D4D4D4'

LEFT_X = 0.08; EXHIBIT_Y = 0.96; SEP_LINE_Y = 0.935
TITLE_Y = 0.90; SUBTITLE_Y = 0.78; LEGEND_RIGHT = 0.82; SOURCE_Y = 0.04


def apply_mckinsey_frame(fig, ax, exhibit_label, title, subtitle,
                         legend_items, source):
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


def style_mckinsey_axes(ax):
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(False)
    ax.tick_params(axis='both', length=0, labelsize=10, labelcolor=MCK_DARK)


# ── 数据 ──────────────────────────────────────
categories = ['Review industry findings', 'Track competitor launches',
              'Monitor competitor acquisitions', 'Conduct customer interviews',
              'Scan start-up trends', 'Use AI for trend discovery',
              'Use AI to explore new uses', 'Track outside-set launches',
              'Monitor noncompetitor acquisitions', 'None of the above']
top_perf = [63, 57, 44, 42, 37, 35, 33, 34, 27, 4]
others   = [53, 50, 37, 31, 24, 24, 22, 21, 19, 4]

fig, ax = plt.subplots(figsize=(11, 8.5))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
# ⚠️ left=0.30 给类别标签留空间
fig.subplots_adjust(left=0.30, right=0.96, top=0.72, bottom=0.10)

y = list(range(len(categories)))
height = 0.35   # 窄条
ax.barh([i - height/2 for i in y], top_perf, height=height, color=MCK_CYAN, zorder=3)
ax.barh([i + height/2 for i in y], others,   height=height, color=MCK_GRAY, zorder=3)

ax.set_yticks(y)
ax.set_yticklabels(categories, fontproperties=fp, fontsize=10, color=MCK_DARK)
ax.invert_yaxis()
ax.set_xlim(0, 100)
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.xaxis.tick_top()   # ⚠️ x 轴放在顶部（麦肯锡横向条形的标志）

style_mckinsey_axes(ax)

apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 4',
    title='Top economic performers track the signs of shifting advantage\nmore than others.',
    subtitle='Actions that respondents\' companies take at least quarterly\nto explore new growth opportunities, % of respondents',
    legend_items=[('Top performers', MCK_CYAN), ('Others', MCK_GRAY)],
    source='McKinsey Global Survey on competitive advantage, 1,257 participants')

plt.savefig('output_mckinsey_grouped_hbar.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
