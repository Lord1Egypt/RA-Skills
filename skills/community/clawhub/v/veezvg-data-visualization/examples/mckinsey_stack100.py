"""
McKinsey 风格 - 100% 单条堆叠（Likert-scale / 分布）
====================================================
参考：McKinsey Exhibit 1
展示占比分布，颜色用亮青的渐变层级（越右越深）
"""
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font_path = '/System/Library/Fonts/STHeiti Light.ttc'
fp      = FontProperties(fname=font_path)
fp_bold = FontProperties(fname=font_path, weight='bold')

MCK_DARK = '#051C2C'; MCK_META = '#8C8C8C'; MCK_LINE = '#D4D4D4'

LEFT_X = 0.08; EXHIBIT_Y = 0.96; SEP_LINE_Y = 0.935
TITLE_Y = 0.90; SUBTITLE_Y = 0.76; SOURCE_Y = 0.04


def apply_mckinsey_frame(fig, ax, exhibit_label, title, subtitle, source):
    fig.text(LEFT_X, EXHIBIT_Y, exhibit_label,
             fontproperties=fp, fontsize=10, color=MCK_META, va='top', ha='left')
    ax.plot([LEFT_X, 0.96], [SEP_LINE_Y, SEP_LINE_Y],
            transform=fig.transFigure, clip_on=False,
            color=MCK_LINE, linewidth=0.8, zorder=20)
    fig.text(LEFT_X, TITLE_Y, title,
             fontproperties=fp_bold, fontsize=16, color=MCK_DARK, va='top', ha='left')
    fig.text(LEFT_X, SUBTITLE_Y, subtitle,
             fontproperties=fp_bold, fontsize=11.5, color=MCK_DARK, va='top', ha='left')
    fig.text(LEFT_X, SOURCE_Y, f'Source: {source}',
             fontproperties=fp, fontsize=9, color=MCK_DARK, va='bottom', ha='left')


# ── 数据 ─────────────────────────────────────────
segments = ['No clear\nperspective', 'Minimally', 'Somewhat', 'Significantly', 'Completely']
values   = [11, 17, 39, 30, 3]
# 亮青渐变：从白到最深
palette  = ['#FFFFFF', '#C3ECFA', '#7BD4ED', '#2CBDEF', '#0088CE']

fig, ax = plt.subplots(figsize=(12, 5.5))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=LEFT_X, right=0.96, top=0.56, bottom=0.30)

left_cursor = 0
for i, (seg, val, color) in enumerate(zip(segments, values, palette)):
    edge = MCK_LINE if i == 0 else color
    ax.barh(0, val, left=left_cursor, height=0.5,
            color=color, edgecolor=edge,
            linewidth=0.8 if i == 0 else 0, zorder=3)
    # 段内数字
    ax.text(left_cursor + val / 2, 0, f'{val}',
            ha='center', va='center',
            fontproperties=fp_bold, fontsize=14, color=MCK_DARK)
    # 段上方标签
    ax.text(left_cursor + val / 2, 0.55, seg,
            ha='center', va='bottom',
            fontproperties=fp, fontsize=10, color=MCK_DARK)
    left_cursor += val

ax.set_xlim(0, 100)
ax.set_ylim(-0.8, 1.2)
ax.axis('off')

# 底部斜体 "100%" 标注
fig.text(0.5, 0.26, '100%',
         fontproperties=fp, fontsize=10, color=MCK_META,
         va='top', ha='center', style='italic')

apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 1',
    title='One-third of executives believe there will be significant changes\nto the nature of their competitive advantage over the next five years.',
    subtitle='Extent of expected change in the competitive advantages of respondents\' companies,\nnext 5 years, % of respondents',
    source='McKinsey Global Survey on competitive advantage, 1,257 participants')

plt.savefig('output_mckinsey_stack100.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
