"""
世纪茗家天猫旗舰店 第20周周报 - 终极版图表生成脚本
共12张图表，统一品牌绿色系配色
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib import rcParams
from matplotlib.ticker import FuncFormatter
import matplotlib.patheffects as pe
import numpy as np
import warnings
warnings.filterwarnings('ignore')

rcParams['font.family'] = 'Noto Sans CJK SC'
rcParams['axes.unicode_minus'] = False
rcParams['figure.facecolor'] = 'white'

OUT = '/home/ubuntu/weekly_report_v3/charts'

# ── 配色系统 ──────────────────────────────────────────────────
C = {
    'primary':  '#1B5E20',   # 深绿
    'sec':      '#388E3C',   # 中绿
    'light':    '#81C784',   # 浅绿
    'pale':     '#C8E6C9',   # 极浅绿
    'accent':   '#F57F17',   # 橙黄
    'accent2':  '#FDD835',   # 亮黄
    'red':      '#C62828',   # 红
    'red_lt':   '#EF9A9A',   # 浅红
    'blue':     '#1565C0',   # 蓝
    'blue_lt':  '#90CAF9',   # 浅蓝
    'gray':     '#616161',   # 灰
    'gray_lt':  '#EEEEEE',   # 浅灰
    'dark':     '#212121',   # 深黑
    'bg':       '#FAFAFA',   # 背景
    'white':    '#FFFFFF',
}

def money(x, pos=None): return f'¥{x:,.0f}'
def pct(x, pos=None):   return f'{x:.1f}%'

def styled_ax(ax, title='', xlabel='', ylabel='', grid_axis='y'):
    ax.set_facecolor(C['bg'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(C['gray_lt'])
    ax.spines['bottom'].set_color(C['gray_lt'])
    ax.tick_params(colors=C['dark'], labelsize=9.5)
    if title:  ax.set_title(title, fontsize=12, fontweight='bold', pad=10, color=C['dark'])
    if xlabel: ax.set_xlabel(xlabel, fontsize=10, color=C['gray'])
    if ylabel: ax.set_ylabel(ylabel, fontsize=10, color=C['gray'])
    if grid_axis:
        ax.grid(axis=grid_axis, linestyle='--', alpha=0.4, color=C['gray_lt'], zorder=0)

# ══════════════════════════════════════════════════════════════
# 图1：本周经营总览 — 净销售额拆解 + 核心指标环比
# ══════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(16, 5.5))
gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.42)

# 左：净销售额瀑布图
ax1 = fig.add_subplot(gs[0])
labels = ['支付金额', '成功退款', '净销售额']
vals   = [22060.16, -6384.45, 15675.71]
bottoms = [0, 22060.16, 0]
colors  = [C['primary'], C['red'], C['sec']]
for i,(l,v,b,c) in enumerate(zip(labels,vals,bottoms,colors)):
    h = abs(v)
    ax1.bar(i, h, bottom=b if v>0 else b+v, color=c, width=0.55,
            edgecolor='white', linewidth=1.5, zorder=3)
    ypos = b + v/2 if v > 0 else b + v/2
    ax1.text(i, b + v + (300 if v>0 else -1200),
             f'¥{abs(v):,.2f}', ha='center', fontsize=11,
             fontweight='bold', color=c)
# 连接线
ax1.plot([0.28, 0.72], [22060.16, 22060.16], color=C['gray'], lw=1.2, ls='--', alpha=0.6)
ax1.plot([1.28, 1.72], [15675.71, 15675.71], color=C['gray'], lw=1.2, ls='--', alpha=0.6)
ax1.set_xticks([0,1,2]); ax1.set_xticklabels(labels, fontsize=11)
ax1.yaxis.set_major_formatter(FuncFormatter(money))
ax1.set_ylim(0, 28000)
styled_ax(ax1, title='净销售额拆解（支付 → 退款 → 净收）', ylabel='金额（元）')
# 退款率标注
ax1.text(1.5, 19000, f'退款率\n28.9%', ha='center', fontsize=10,
         color=C['red'], fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=C['red_lt'], alpha=0.4))

# 右：核心指标环比卡片
ax2 = fig.add_subplot(gs[1])
ax2.axis('off')
metrics = [
    ('支付金额',    '¥22,060', '¥18,472', '+19.4%', True),
    ('净销售额',    '¥15,676', '—',        '退款侵蚀', False),
    ('成功退款额',  '¥6,384',  '¥4,290',  '+48.8%', False),
    ('访客数',      '7,073人', '7,707人',  '-8.2%',  False),
    ('支付买家数',  '61人',    '61人',     '+0.0%',  True),
    ('支付转化率',  '0.86%',   '0.79%',   '+8.96%', True),
    ('客单价',      '¥361.64', '¥302.82', '+19.4%', True),
    ('老客支付额',  '¥10,842', '¥7,754',  '+39.8%', True),
]
col_x = [0.02, 0.38, 0.62, 0.85]
col_headers = ['指标', '本周', '上周', '环比']
for j,h in enumerate(col_headers):
    ax2.text(col_x[j], 0.97, h, transform=ax2.transAxes,
             fontsize=10, fontweight='bold', color=C['gray'], va='top')
ax2.axhline(y=0.93, xmin=0, xmax=1, color=C['gray_lt'], lw=1.5)
row_h = 0.093
for i,(name,cur,prev,chg,pos) in enumerate(metrics):
    y = 0.91 - i*row_h
    bg = C['pale'] if i%2==0 else C['white']
    ax2.add_patch(mpatches.FancyBboxPatch((0, y-0.01), 1, row_h-0.005,
        boxstyle='round,pad=0.005', facecolor=bg, edgecolor='none',
        transform=ax2.transAxes, zorder=1))
    chg_color = C['primary'] if pos else C['red']
    ax2.text(col_x[0], y+0.03, name, transform=ax2.transAxes,
             fontsize=9.5, color=C['dark'], va='center', fontweight='bold')
    ax2.text(col_x[1], y+0.03, cur,  transform=ax2.transAxes,
             fontsize=9.5, color=C['primary'], va='center', fontweight='bold')
    ax2.text(col_x[2], y+0.03, prev, transform=ax2.transAxes,
             fontsize=9.5, color=C['gray'], va='center')
    ax2.text(col_x[3], y+0.03, chg,  transform=ax2.transAxes,
             fontsize=9.5, color=chg_color, va='center', fontweight='bold')
ax2.set_title('核心指标周环比', fontsize=12, fontweight='bold', pad=10, color=C['dark'])

plt.suptitle('一、本周经营总览', fontsize=14, fontweight='bold', y=1.02, color=C['primary'])
plt.tight_layout()
plt.savefig(f'{OUT}/fig01_overview.png', dpi=150, bbox_inches='tight')
plt.close()
print("图01 ✓")

# ══════════════════════════════════════════════════════════════
# 图2：退款专项诊断 — 商品退款率 + 每日退款趋势
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 5.5))

# 左：商品退款率气泡图（支付金额 vs 退款率，气泡=访客数）
products = ['5年陈皮\n散装100g', '流金岁月\n陈皮罐装', '橘红片\n化州罐装', '十年醇\n袋装', '特级小青柑\n268g', '大红柑\n180g', '大红柑\n醇香']
pay_amt  = [7060.80, 1976.80, 408.00, 484.00, 616.00, 1548.16, 1467.70]
refund_r = [22.37, 157.69, 100.00, 39.67, 35.71, 16.34, 11.58]
visitors = [692, 224, 60, 682, 2222, 1013, 49]
colors_p = [C['accent'] if r<30 else C['red'] if r>100 else C['red_lt'] for r in refund_r]

for i,(p,pa,rr,v,c) in enumerate(zip(products,pay_amt,refund_r,visitors,colors_p)):
    sc = axes[0].scatter(pa, rr, s=np.sqrt(v)*18+60, c=c, alpha=0.82,
                         edgecolors='white', linewidth=2, zorder=3)
    offset_y = 8 if rr < 120 else -15
    axes[0].text(pa, rr+offset_y, p, ha='center', fontsize=8.5,
                 color=C['dark'], fontweight='bold' if rr>50 else 'normal')
axes[0].axhline(30, color=C['accent'], lw=1.5, ls='--', alpha=0.7, label='30%警戒线')
axes[0].axhline(100, color=C['red'], lw=1.8, ls='--', alpha=0.8, label='100%极危线')
axes[0].set_xlabel('支付金额（元）', fontsize=10)
axes[0].set_ylabel('退款率（%）', fontsize=10)
axes[0].xaxis.set_major_formatter(FuncFormatter(money))
axes[0].legend(fontsize=9.5, loc='upper right')
axes[0].text(0.02, 0.97, '气泡大小 = 访客数', transform=axes[0].transAxes,
             fontsize=8.5, color=C['gray'], style='italic', va='top')
styled_ax(axes[0], title='商品退款率诊断（气泡=访客数）', grid_axis='both')
# 标注异常
axes[0].annotate('退款额超过\n当周成交额！', xy=(1976.80, 157.69),
                 xytext=(3500, 140), fontsize=9, color=C['red'], fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color=C['red'], lw=1.5))

# 右：每日销售额 vs 退款金额
dates = ['5/11\n(日)', '5/12\n(一)', '5/13\n(二)', '5/14\n(三)', '5/15\n(四)', '5/16\n(五)', '5/17\n(六)']
sales_d  = [3621.51, 3078.50, 5748.08, 2016.85, 2117.18, 2661.95, 2816.09]
refund_d = [2438.59, 220.00, 2817.88, 0.00, 404.24, 230.44, 273.30]
net_d    = [s-r for s,r in zip(sales_d,refund_d)]
x = np.arange(7); w = 0.32

b1 = axes[1].bar(x-w/2, sales_d, w, label='支付金额', color=C['sec'], edgecolor='white', zorder=3)
b2 = axes[1].bar(x+w/2, refund_d, w, label='退款金额', color=C['red_lt'], edgecolor='white', zorder=3)
axes[1].plot(x, net_d, 'D-', color=C['primary'], lw=2.5, ms=8, label='净销售额', zorder=4)
for i,(n,r) in enumerate(zip(net_d,refund_d)):
    if r > 0:
        axes[1].text(i+w/2, r+50, f'¥{r:.0f}', ha='center', fontsize=8, color=C['red'])
    axes[1].text(i, n+80, f'¥{n:.0f}', ha='center', fontsize=8, color=C['primary'], fontweight='bold')
axes[1].set_xticks(x); axes[1].set_xticklabels(dates, fontsize=10)
axes[1].yaxis.set_major_formatter(FuncFormatter(money))
axes[1].legend(fontsize=9.5, loc='upper right')
# 5/11和5/13高退款标注
axes[1].annotate('高退款日\n(¥2,439)', xy=(0+w/2, 2438.59), xytext=(0.8, 3800),
                 fontsize=8.5, color=C['red'],
                 arrowprops=dict(arrowstyle='->', color=C['red'], lw=1.2))
axes[1].annotate('高退款日\n(¥2,818)', xy=(2+w/2, 2817.88), xytext=(3, 4200),
                 fontsize=8.5, color=C['red'],
                 arrowprops=dict(arrowstyle='->', color=C['red'], lw=1.2))
styled_ax(axes[1], title='每日支付金额 / 退款金额 / 净销售额', ylabel='金额（元）')

plt.suptitle('二、退款专项诊断', fontsize=14, fontweight='bold', y=1.02, color=C['primary'])
plt.tight_layout()
plt.savefig(f'{OUT}/fig02_refund.png', dpi=150, bbox_inches='tight')
plt.close()
print("图02 ✓")

# ══════════════════════════════════════════════════════════════
# 图3：流量结构与推广效率 — 三级来源UV价值 + 流量漏斗
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 5.5))

# 左：三级流量来源 UV价值横向排行
sources = ['购物车', '我的淘宝', '站内沟通汇总', '手淘拍立淘',
           '淘宝客', '店铺运营(无界)', '搜索', '推荐', '站外沟通汇总', '付费推广(无界)']
uv_vals = [70.12, 50.23, 45.35, 11.48, 19.60, 7.98, 4.74, 2.24, 6.74, 0.60]
visitors_s = [134, 116, 271, 145, 69, 210, 277, 809, 313, 4773]
# 按UV价值排序
order = sorted(range(len(uv_vals)), key=lambda i: uv_vals[i])
src_sorted = [sources[i] for i in order]
uv_sorted  = [uv_vals[i] for i in order]
vis_sorted = [visitors_s[i] for i in order]
bar_colors = [C['primary'] if u>10 else C['sec'] if u>2 else C['red_lt'] for u in uv_sorted]
bars = axes[0].barh(range(len(src_sorted)), uv_sorted, color=bar_colors,
                    height=0.65, edgecolor='white', zorder=3)
for i,(v,vis) in enumerate(zip(uv_sorted,vis_sorted)):
    axes[0].text(v+0.5, i, f'¥{v:.2f}  ({vis}人)', va='center', fontsize=9, color=C['dark'])
axes[0].set_yticks(range(len(src_sorted))); axes[0].set_yticks(range(len(src_sorted)))
axes[0].set_yticklabels(src_sorted, fontsize=9.5)
axes[0].set_xlabel('UV价值（元/人）', fontsize=10)
axes[0].set_xlim(0, 90)
axes[0].axvline(10, color=C['accent'], lw=1.5, ls='--', alpha=0.7, label='UV价值=10参考线')
axes[0].legend(fontsize=9, loc='lower right')
styled_ax(axes[0], title='流量来源UV价值排行（括号内为访客数）', grid_axis='x')

# 右：三大流量来源漏斗对比
cats = ['付费推广', '经营优势', '主动回访']
visitors_3 = [4798, 2437, 561]
buyers_3   = [13, 28, 31]
pay_3      = [4213.66, 6594.06, 14397.55]
uv_3       = [0.88, 2.71, 25.66]
cvr_3      = [0.27, 1.15, 5.53]
x3 = np.arange(3)
ax_r = axes[1]; ax_rr = ax_r.twinx()
w3 = 0.3
b_v = ax_r.bar(x3-w3/2, visitors_3, w3, label='访客数', color=C['blue_lt'], edgecolor='white', zorder=3)
b_p = ax_r.bar(x3+w3/2, pay_3, w3, label='支付金额', color=C['primary'], edgecolor='white', zorder=3)
ax_rr.plot(x3, uv_3, 'D-', color=C['accent'], lw=2.5, ms=10, label='UV价值', zorder=4)
for i,(v,p,u,c) in enumerate(zip(visitors_3,pay_3,uv_3,cvr_3)):
    ax_r.text(i-w3/2, v+50, f'{v:,}', ha='center', fontsize=9, color=C['blue'])
    ax_r.text(i+w3/2, p+100, f'¥{p:,.0f}', ha='center', fontsize=9, color=C['primary'], fontweight='bold')
    ax_rr.text(i, u+1.5, f'UV={u:.2f}\nCVR={c:.2f}%', ha='center', fontsize=8.5,
               color=C['accent'], fontweight='bold')
ax_r.set_xticks(x3); ax_r.set_xticklabels(cats, fontsize=11)
ax_r.set_ylabel('访客数 / 支付金额（元）', fontsize=10)
ax_rr.set_ylabel('UV价值（元/人）', fontsize=10, color=C['accent'])
ax_r.yaxis.set_major_formatter(FuncFormatter(money))
ax_r.set_ylim(0, 22000); ax_rr.set_ylim(0, 40)
h1,l1 = ax_r.get_legend_handles_labels(); h2,l2 = ax_rr.get_legend_handles_labels()
ax_r.legend(h1+h2, l1+l2, fontsize=9.5, loc='upper left')
styled_ax(ax_r, title='三大流量来源：访客 / 支付金额 / UV价值')

plt.suptitle('三、流量结构与推广效率', fontsize=14, fontweight='bold', y=1.02, color=C['primary'])
plt.tight_layout()
plt.savefig(f'{OUT}/fig03_traffic.png', dpi=150, bbox_inches='tight')
plt.close()
print("图03 ✓")

# ══════════════════════════════════════════════════════════════
# 图4：老客价值与主动回访 — 新老客结构 + 老客复购趋势
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 5.5))

# 左：新老客支付金额饼图
labels_pie = ['老买家\n¥10,842\n(49.1%)', '新买家\n¥11,218\n(50.9%)']
sizes_pie  = [10842.30, 11217.86]
explode    = (0.06, 0)
colors_pie = [C['primary'], C['pale']]
wedges, texts = axes[0].pie(sizes_pie, explode=explode, labels=labels_pie,
                             colors=colors_pie, startangle=90,
                             wedgeprops=dict(edgecolor='white', linewidth=2),
                             textprops=dict(fontsize=11, fontweight='bold'))
texts[0].set_color(C['primary'])
texts[1].set_color(C['gray'])
axes[0].set_title('新老客支付金额占比', fontsize=12, fontweight='bold', pad=10, color=C['dark'])
# 中心标注
axes[0].text(0, -0.08, '老客复购\n环比+39.8%', ha='center', fontsize=10,
             color=C['primary'], fontweight='bold')

# 右：客户结构变化对比
cat_cust = ['店铺客户数', '客户新访', '未购客户\n回访', '已购客户\n回访']
this_w   = [7099, 5212, 1953, 375]
last_w   = [7732, 5486, 2431, 355]
x4 = np.arange(4); w4 = 0.32
b_t = axes[1].bar(x4-w4/2, this_w, w4, label='本周', color=C['primary'], edgecolor='white', zorder=3)
b_l = axes[1].bar(x4+w4/2, last_w, w4, label='上周', color=C['pale'], edgecolor=C['sec'], linewidth=1, zorder=3)
for i,(t,l) in enumerate(zip(this_w,last_w)):
    chg = (t-l)/l*100
    col = C['primary'] if chg>0 else C['red']
    axes[1].text(i, max(t,l)+80, f'{chg:+.1f}%', ha='center', fontsize=9.5,
                 color=col, fontweight='bold')
    axes[1].text(i-w4/2, t+30, f'{t:,}', ha='center', fontsize=8.5, color=C['dark'])
    axes[1].text(i+w4/2, l+30, f'{l:,}', ha='center', fontsize=8.5, color=C['gray'])
axes[1].set_xticks(x4); axes[1].set_xticklabels(cat_cust, fontsize=10)
axes[1].legend(fontsize=10)
axes[1].set_ylim(0, 10000)
styled_ax(axes[1], title='客户结构本周 vs 上周', ylabel='人数')

plt.suptitle('四、老客价值与主动回访', fontsize=14, fontweight='bold', y=1.02, color=C['primary'])
plt.tight_layout()
plt.savefig(f'{OUT}/fig04_customers.png', dpi=150, bbox_inches='tight')
plt.close()
print("图04 ✓")

# ══════════════════════════════════════════════════════════════
# 图5：直播效率复盘 — 转化漏斗 + 播中/播后成交趋势
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 5.5))

# 左：直播转化漏斗
funnel_labels = ['直播观看\n1,188人', '商品点击\n106人\n(8.92%)', '成交\n2单\n(1.89%)']
funnel_vals   = [1188, 106, 2]
funnel_pct    = [100, 8.92, 1.89]
funnel_w      = [0.9, 0.55, 0.25]
funnel_colors = [C['primary'], C['sec'], C['accent']]
for i,(l,v,w_f,c) in enumerate(zip(funnel_labels,funnel_vals,funnel_w,funnel_colors)):
    axes[0].barh(2-i, w_f, color=c, height=0.55, align='center',
                 edgecolor='white', linewidth=2, zorder=3)
    axes[0].text(w_f/2, 2-i, l, ha='center', va='center',
                 fontsize=10.5, color='white', fontweight='bold')
# 环比对比
prev_pct = [100, 13.85, 6.98]
for i,(cur,pre) in enumerate(zip(funnel_pct,prev_pct)):
    if i > 0:
        diff = cur - pre
        col = C['primary'] if diff>0 else C['red']
        axes[0].text(0.95, 2-i, f'上周:{pre:.2f}%\n本周:{cur:.2f}%\n({diff:+.2f}%)',
                     ha='right', va='center', fontsize=8.5, color=col, fontweight='bold')
axes[0].set_xlim(0, 1.1); axes[0].set_ylim(-0.5, 2.8)
axes[0].axis('off')
axes[0].set_title('直播转化漏斗（对比上周）', fontsize=12, fontweight='bold', pad=10, color=C['dark'])

# 右：播中 vs 播后成交金额
live_dates = ['5/11', '5/12', '5/13', '5/14', '5/15', '5/16', '5/17']
during = [0, 0, 358.67, 0, 0, 0, 0]
after  = [0, 0, 985.00, 0, 0, 0, 0]
# 注：本周仅5/13有直播数据
x5 = np.arange(7); w5 = 0.32
b_d = axes[1].bar(x5-w5/2, during, w5, label='播中成交', color=C['sec'], edgecolor='white', zorder=3)
b_a = axes[1].bar(x5+w5/2, after,  w5, label='播后成交', color=C['accent'], edgecolor='white', zorder=3)
axes[1].text(2-w5/2, 358.67+20, '¥358.67', ha='center', fontsize=9, color=C['sec'], fontweight='bold')
axes[1].text(2+w5/2, 985.00+20, '¥985.00', ha='center', fontsize=9, color=C['accent'], fontweight='bold')
axes[1].set_xticks(x5); axes[1].set_xticklabels(live_dates, fontsize=10)
axes[1].yaxis.set_major_formatter(FuncFormatter(money))
axes[1].legend(fontsize=10)
axes[1].set_ylim(0, 1400)
# 关键洞察
axes[1].text(0.5, 0.85, '关键洞察：播后成交(¥985)>\n播中成交(¥358)，直播蓄水\n价值不可忽视',
             transform=axes[1].transAxes, ha='center', fontsize=9.5,
             color=C['accent'], fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=C['accent2'], alpha=0.3))
styled_ax(axes[1], title='直播播中 vs 播后成交金额', ylabel='成交金额（元）')

plt.suptitle('五、直播效率复盘', fontsize=14, fontweight='bold', y=1.02, color=C['primary'])
plt.tight_layout()
plt.savefig(f'{OUT}/fig05_live.png', dpi=150, bbox_inches='tight')
plt.close()
print("图05 ✓")

# ══════════════════════════════════════════════════════════════
# 图6：客服承接表现 — 绩效对比 + 每日响应时长
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# 左：客服绩效对比
cs_names = ['泽彬', '小青']
cs_consult = [11, 39]
cs_valid   = [11, 24]
cs_order   = [4, 4]
cs_sales   = [1135.92, 4111.00]
cs_refund  = [0, 404.24]
cs_net     = [1135.92, 3706.76]
x6 = np.arange(2); w6 = 0.2
axes[0].bar(x6-w6, cs_consult, w6, label='咨询人数', color=C['blue_lt'], edgecolor='white', zorder=3)
axes[0].bar(x6,    cs_valid,   w6, label='有效接待', color=C['sec'],     edgecolor='white', zorder=3)
axes[0].bar(x6+w6, cs_order,   w6, label='下单人数', color=C['primary'], edgecolor='white', zorder=3)
for i,(c,v,o) in enumerate(zip(cs_consult,cs_valid,cs_order)):
    axes[0].text(i-w6, c+0.3, str(c), ha='center', fontsize=9.5, color=C['blue'])
    axes[0].text(i,    v+0.3, str(v), ha='center', fontsize=9.5, color=C['sec'])
    axes[0].text(i+w6, o+0.3, str(o), ha='center', fontsize=9.5, color=C['primary'], fontweight='bold')
ax6r = axes[0].twinx()
ax6r.plot(x6, cs_net, 'D-', color=C['accent'], lw=2.5, ms=12, label='净销售额', zorder=4)
for i,n in enumerate(cs_net):
    ax6r.text(i, n+80, f'¥{n:,.0f}', ha='center', fontsize=9.5,
              color=C['accent'], fontweight='bold')
axes[0].set_xticks(x6); axes[0].set_xticklabels(cs_names, fontsize=12, fontweight='bold')
axes[0].set_ylabel('人数', fontsize=10); ax6r.set_ylabel('净销售额（元）', fontsize=10, color=C['accent'])
ax6r.yaxis.set_major_formatter(FuncFormatter(money))
axes[0].set_ylim(0, 55); ax6r.set_ylim(0, 6000)
h1,l1 = axes[0].get_legend_handles_labels(); h2,l2 = ax6r.get_legend_handles_labels()
axes[0].legend(h1+h2, l1+l2, fontsize=9, loc='upper left')
styled_ax(axes[0], title='客服绩效：咨询→接待→下单→净销售额')

# 右：每日平均响应时长
resp_dates = ['5/11', '5/12', '5/13', '5/14', '5/15', '5/16', '5/17']
resp_times = [134, 42, 38, 128, 35, 29, 54]
bar_colors_r = [C['red'] if t>120 else C['accent'] if t>60 else C['primary'] for t in resp_times]
axes[1].bar(range(7), resp_times, color=bar_colors_r, width=0.6, edgecolor='white', zorder=3)
for i,t in enumerate(resp_times):
    axes[1].text(i, t+2, f'{t}秒', ha='center', fontsize=9.5,
                 color=C['red'] if t>120 else C['dark'], fontweight='bold' if t>120 else 'normal')
axes[1].axhline(120, color=C['red'], lw=2, ls='--', alpha=0.8, label='120秒预警线')
axes[1].axhline(60,  color=C['accent'], lw=1.5, ls=':', alpha=0.7, label='60秒参考线')
axes[1].set_xticks(range(7)); axes[1].set_xticklabels(resp_dates, fontsize=10)
axes[1].set_ylabel('平均响应时长（秒）', fontsize=10)
axes[1].legend(fontsize=9.5)
axes[1].set_ylim(0, 180)
# 标注超时日
for i,t in enumerate(resp_times):
    if t > 120:
        axes[1].annotate('超预警！', xy=(i, t), xytext=(i+0.5, t+10),
                         fontsize=9, color=C['red'], fontweight='bold',
                         arrowprops=dict(arrowstyle='->', color=C['red'], lw=1.2))
styled_ax(axes[1], title='每日客服平均响应时长（秒）')

plt.suptitle('六、客服承接表现', fontsize=14, fontweight='bold', y=1.02, color=C['primary'])
plt.tight_layout()
plt.savefig(f'{OUT}/fig06_cs.png', dpi=150, bbox_inches='tight')
plt.close()
print("图06 ✓")

# ══════════════════════════════════════════════════════════════
# 图7：商品销售TOP10 — 支付金额 + 转化率
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 6))
prods = ['5年陈皮散装100g', '特级小青柑散装', '青韵小青柑袋装',
         '流金岁月陈皮罐装', '大红柑180g', '大红柑醇香',
         '大红柑印级', '特级小青柑268g', '十年醇袋装', '橘红片化州罐装']
pay_p = [7060.80, 4076.80, 2321.50, 1976.80, 1548.16, 1467.70, 784.00, 616.00, 484.00, 408.00]
cvr_p = [3.76, 5.36, 7.69, 0.45, 0.39, 6.12, 2.00, 0.14, 0.44, 1.67]
ref_p = [22.37, 0, 0, 157.69, 16.34, 11.58, 0, 35.71, 39.67, 100.00]

y_pos = range(len(prods)-1, -1, -1)
bar_c = [C['red'] if r>100 else C['accent'] if r>30 else C['primary'] for r in ref_p]
bars = ax.barh(list(y_pos), pay_p, color=bar_c, height=0.65, edgecolor='white', zorder=3)
axr = ax.twinx()
axr.plot(cvr_p, list(y_pos), 'D', color=C['accent'], ms=10, zorder=4, label='转化率')
for i,(p,c,r) in enumerate(zip(pay_p,cvr_p,ref_p)):
    yp = list(y_pos)[i]
    ax.text(p+50, yp, f'¥{p:,.0f}', va='center', fontsize=9.5, color=C['dark'], fontweight='bold')
    ref_str = f'  退款率{r:.0f}%' if r>0 else ''
    ref_col = C['red'] if r>100 else C['accent'] if r>30 else C['gray']
    if r > 0:
        ax.text(p+50, yp-0.28, ref_str, va='center', fontsize=8.5, color=ref_col)
    axr.text(c+0.1, yp, f'{c:.2f}%', va='center', fontsize=8.5, color=C['accent'])
ax.set_yticks(list(y_pos)); ax.set_yticklabels(prods, fontsize=10)
ax.xaxis.set_major_formatter(FuncFormatter(money))
ax.set_xlabel('支付金额（元）', fontsize=10)
axr.set_ylabel('支付转化率（%）', fontsize=10, color=C['accent'])
axr.set_ylim(-0.5, 9.5)
# 图例
legend_patches = [
    mpatches.Patch(color=C['primary'], label='退款率<30%（健康）'),
    mpatches.Patch(color=C['accent'],  label='退款率30-100%（警戒）'),
    mpatches.Patch(color=C['red'],     label='退款率>100%（危险）'),
]
ax.legend(handles=legend_patches, fontsize=9, loc='lower right')
ax.set_xlim(0, 11000)
styled_ax(ax, title='商品销售TOP10（颜色=退款风险等级，菱形=转化率）', grid_axis='x')
plt.suptitle('七、商品销售表现', fontsize=14, fontweight='bold', y=1.02, color=C['primary'])
plt.tight_layout()
plt.savefig(f'{OUT}/fig07_products.png', dpi=150, bbox_inches='tight')
plt.close()
print("图07 ✓")

# ══════════════════════════════════════════════════════════════
# 图8：推广场景效率全面对比
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 5.5))

scenes      = ['货品全站推广', '超级短视频', '关键词推广', '店铺直达']
cost_s      = [2023.24, 700.00, 638.52, 375.35]
revenue_s   = [4206.91, 1507.30, 418.00, 2054.44]
roi_s       = [2.08, 2.15, 0.65, 5.47]
ctr_s       = [2.40, 2.93, 2.42, 49.12]
cvr_s       = [2.20, 1.32, 0.45, 4.40]
x8 = np.arange(4); w8 = 0.32

# 左：花费 vs 成交金额 + ROI
ax8l = axes[0]; ax8lr = ax8l.twinx()
b1 = ax8l.bar(x8-w8/2, cost_s,    w8, label='花费',    color=C['blue_lt'], edgecolor='white', zorder=3)
b2 = ax8l.bar(x8+w8/2, revenue_s, w8, label='成交金额', color=C['primary'], edgecolor='white', zorder=3)
for bar,v in zip(b1,cost_s):
    ax8l.text(bar.get_x()+bar.get_width()/2, bar.get_height()+40,
              f'¥{v:,.0f}', ha='center', fontsize=8.5, color=C['blue'])
for bar,v in zip(b2,revenue_s):
    ax8l.text(bar.get_x()+bar.get_width()/2, bar.get_height()+40,
              f'¥{v:,.0f}', ha='center', fontsize=8.5, color=C['primary'], fontweight='bold')
ax8lr.plot(x8, roi_s, 'D-', color=C['accent'], lw=2.5, ms=10, label='ROI', zorder=4)
ax8lr.axhline(1, color=C['red'], lw=1.5, ls='--', alpha=0.7, label='ROI=1盈亏线')
for i,r in enumerate(roi_s):
    ax8lr.text(i, r+0.3, f'{r:.2f}', ha='center', fontsize=10.5,
               color=C['red'] if r<1 else C['accent'], fontweight='bold')
ax8l.set_xticks(x8); ax8l.set_xticklabels(scenes, fontsize=10)
ax8l.set_ylabel('金额（元）', fontsize=10); ax8lr.set_ylabel('ROI', fontsize=10, color=C['accent'])
ax8l.yaxis.set_major_formatter(FuncFormatter(money))
ax8l.set_ylim(0, 3200); ax8lr.set_ylim(0, 8)
h1,l1 = ax8l.get_legend_handles_labels(); h2,l2 = ax8lr.get_legend_handles_labels()
ax8l.legend(h1+h2, l1+l2, fontsize=9.5, loc='upper right')
styled_ax(ax8l, title='各场景：花费 / 成交金额 / ROI')

# 右：CTR vs CVR
b3 = axes[1].bar(x8-w8/2, ctr_s, w8, label='点击率CTR（%）', color=C['blue_lt'], edgecolor='white', zorder=3)
b4 = axes[1].bar(x8+w8/2, cvr_s, w8, label='点击转化率CVR（%）', color=C['sec'], edgecolor='white', zorder=3)
for bar,v in zip(b3,ctr_s):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                 f'{v:.2f}%', ha='center', fontsize=9, color=C['blue'])
for bar,v in zip(b4,cvr_s):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                 f'{v:.2f}%', ha='center', fontsize=9, color=C['primary'], fontweight='bold')
axes[1].set_xticks(x8); axes[1].set_xticklabels(scenes, fontsize=10)
axes[1].set_ylabel('比率（%）', fontsize=10)
axes[1].legend(fontsize=10); axes[1].set_ylim(0, 60)
axes[1].annotate('CTR 49.12%异常高\n（精准回访人群）',
                 xy=(3-w8/2, 49.12), xytext=(1.8, 53),
                 fontsize=8.5, color=C['red'],
                 arrowprops=dict(arrowstyle='->', color=C['red'], lw=1.2))
styled_ax(axes[1], title='各场景：点击率CTR vs 点击转化率CVR')

plt.suptitle('八、推广场景效率对比（生意参谋口径）', fontsize=14, fontweight='bold', y=1.02, color=C['primary'])
plt.tight_layout()
plt.savefig(f'{OUT}/fig08_ads_scene.png', dpi=150, bbox_inches='tight')
plt.close()
print("图08 ✓")

# ══════════════════════════════════════════════════════════════
# 图9：推广计划绩效详细分析（计划报表口径）
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 5.5))

plans      = ['5年陈皮\n(货品全站)', '超级短视频\n(续投)', '关键词推广\n(无线)', '六粒全站推广\n(货品全站)', '店铺直达']
cost_p     = [1620.53, 700.00, 638.52, 402.71, 375.35]
revenue_p  = [2984.11, 1507.30, 418.00, 1222.80, 2054.44]
roi_p      = [1.84, 2.15, 0.65, 3.04, 5.47]
orders_p   = [13, 6, 2, 5, 11]
cart_p     = [73, 32, 10, 26, 77]
y_pos9 = range(len(plans)-1, -1, -1)
bar_c9 = [C['red'] if r<1 else C['accent'] if r<2 else C['sec'] if r<4 else C['primary'] for r in roi_p]

# 左：横向花费 vs 成交金额
axes[0].barh([y-0.18 for y in y_pos9], cost_p, height=0.32,
             color=C['blue_lt'], edgecolor='white', zorder=3, label='花费')
axes[0].barh([y+0.18 for y in y_pos9], revenue_p, height=0.32,
             color=bar_c9, edgecolor='white', zorder=3, label='成交金额（颜色=ROI）', alpha=0.9)
for i,(c,r,rev,o,cart) in enumerate(zip(cost_p,roi_p,revenue_p,orders_p,cart_p)):
    yp = list(y_pos9)[i]
    axes[0].text(max(c,rev)+60, yp,
                 f'ROI {r:.2f} | {o}单 | 购物车{cart}',
                 va='center', fontsize=8.5,
                 color=C['red'] if r<1 else C['primary'], fontweight='bold' if r<1 else 'normal')
axes[0].set_yticks(list(y_pos9)); axes[0].set_yticklabels(plans, fontsize=10)
axes[0].xaxis.set_major_formatter(FuncFormatter(money))
axes[0].set_xlabel('金额（元）', fontsize=10)
axes[0].legend(fontsize=9.5, loc='lower right')
axes[0].set_xlim(0, 5500)
styled_ax(axes[0], title='各推广计划：花费 vs 成交金额\n（右侧标注ROI/成交单数/购物车数）', grid_axis='x')

# 右：气泡图
scatter_colors9 = bar_c9
plan_short = ['5年陈皮\n全站', '超级\n短视频', '关键词\n推广', '六粒\n全站', '店铺\n直达']
for i,(c,r,o,col,lbl) in enumerate(zip(cost_p,roi_p,orders_p,scatter_colors9,plan_short)):
    axes[1].scatter(c, r, s=o*70+120, c=col, alpha=0.85, edgecolors='white', linewidth=2, zorder=3)
    axes[1].text(c, r+0.22, lbl, ha='center', fontsize=9, color=C['dark'], fontweight='bold')
axes[1].axhline(1, color=C['red'], lw=1.8, ls='--', alpha=0.7, label='ROI=1 盈亏线')
axes[1].axhline(2, color=C['accent'], lw=1.5, ls=':', alpha=0.7, label='ROI=2 参考线')
axes[1].set_xlabel('花费（元）', fontsize=10); axes[1].set_ylabel('ROI', fontsize=10)
axes[1].xaxis.set_major_formatter(FuncFormatter(money))
axes[1].legend(fontsize=10); axes[1].set_ylim(-0.5, 7.5)
axes[1].text(0.02, 0.02, '气泡大小 = 成交笔数', transform=axes[1].transAxes,
             fontsize=9, color=C['gray'], style='italic')
styled_ax(axes[1], title='推广计划效率气泡图\n（气泡大小=成交笔数，颜色：绿>4，橙2-4，红<1）', grid_axis='both')

plt.suptitle('九、推广计划绩效详细分析（计划报表口径）', fontsize=14, fontweight='bold', y=1.02, color=C['primary'])
plt.tight_layout()
plt.savefig(f'{OUT}/fig09_ads_plan.png', dpi=150, bbox_inches='tight')
plt.close()
print("图09 ✓")

# ══════════════════════════════════════════════════════════════
# 图10：每日推广趋势（含5/14异常标注）
# ══════════════════════════════════════════════════════════════
dates_d  = ['5/11\n(日)', '5/12\n(一)', '5/13\n(二)', '5/14\n(三)', '5/15\n(四)', '5/16\n(五)', '5/17\n(六)']
cost_d   = [573.63, 486.34, 644.18, 579.56, 434.19, 525.31, 493.90]
rev_d    = [1165.64, 2335.58, 1214.00, 20.57, 1001.30, 1711.86, 737.70]
roi_d    = [2.03, 4.80, 1.88, 0.04, 2.31, 3.26, 1.49]
imp_d    = [10828, 10685, 10757, 10740, 8181, 9001, 9484]
clk_d    = [307, 320, 290, 261, 259, 272, 286]
ctr_d    = [r/i*100 for r,i in zip(clk_d,imp_d)]

x10 = np.arange(7); w10 = 0.32
fig, axes = plt.subplots(1, 2, figsize=(16, 5.5))

# 左：每日花费 vs 成交金额 + ROI
ax10l = axes[0]; ax10lr = ax10l.twinx()
b1 = ax10l.bar(x10-w10/2, cost_d, w10, label='花费',    color=C['blue_lt'], edgecolor='white', zorder=3)
b2 = ax10l.bar(x10+w10/2, rev_d,  w10, label='成交金额', color=C['primary'], edgecolor='white', zorder=3)
for bar,v in zip(b1,cost_d):
    ax10l.text(bar.get_x()+bar.get_width()/2, bar.get_height()+20,
               f'¥{v:.0f}', ha='center', fontsize=8, color=C['blue'])
for i,(bar,v) in enumerate(zip(b2,rev_d)):
    ax10l.text(bar.get_x()+bar.get_width()/2, bar.get_height()+20,
               f'¥{v:.0f}', ha='center', fontsize=8,
               color=C['red'] if v<100 else C['primary'],
               fontweight='bold' if v<100 else 'normal')
ax10lr.plot(x10, roi_d, 'o-', color=C['accent'], lw=2.5, ms=8, label='ROI', zorder=4)
ax10lr.axhline(1, color=C['red'], lw=1.5, ls='--', alpha=0.7)
for i,r in enumerate(roi_d):
    ax10lr.text(i, r+0.25, f'{r:.2f}', ha='center', fontsize=9.5,
                color=C['red'] if r<1 else C['accent'], fontweight='bold')
ax10l.annotate('5/14严重异常\nROI=0.04\n需重点排查！', xy=(3+w10/2, 20.57),
               xytext=(4.3, 700), fontsize=8.5, color=C['red'], fontweight='bold',
               arrowprops=dict(arrowstyle='->', color=C['red'], lw=1.5))
ax10l.set_xticks(x10); ax10l.set_xticklabels(dates_d, fontsize=10)
ax10l.set_ylabel('金额（元）', fontsize=10); ax10lr.set_ylabel('ROI', fontsize=10, color=C['accent'])
ax10l.yaxis.set_major_formatter(FuncFormatter(money))
ax10l.set_ylim(0, 3200); ax10lr.set_ylim(-0.5, 7)
h1,l1 = ax10l.get_legend_handles_labels(); h2,l2 = ax10lr.get_legend_handles_labels()
ax10l.legend(h1+h2, l1+l2, fontsize=9.5, loc='upper right')
styled_ax(ax10l, title='每日推广花费 vs 成交金额 vs ROI')

# 右：每日展现量 & 点击量 & CTR
ax10r = axes[1]; ax10rr = ax10r.twinx()
ax10r.bar(x10, imp_d, color=C['pale'], width=0.6, edgecolor='white', zorder=3, label='展现量')
ax10rr.plot(x10, clk_d, 's--', color=C['primary'], lw=2.2, ms=8, label='点击量', zorder=4)
ax10rr.plot(x10, [c*100 for c in ctr_d], 'o-', color=C['accent'], lw=2, ms=7, label='CTR×100', zorder=4)
for i,(imp,clk,ctr) in enumerate(zip(imp_d,clk_d,ctr_d)):
    ax10r.text(i, imp+100, f'{imp:,}', ha='center', fontsize=8, color=C['gray'])
    ax10rr.text(i, clk+5, str(clk), ha='center', fontsize=8.5, color=C['primary'], fontweight='bold')
    ax10rr.text(i, clk+18, f'{ctr:.2f}%', ha='center', fontsize=7.5, color=C['accent'])
ax10r.set_xticks(x10); ax10r.set_xticklabels(dates_d, fontsize=10)
ax10r.set_ylabel('展现量（次）', fontsize=10); ax10rr.set_ylabel('点击量（次）', fontsize=10, color=C['primary'])
ax10r.set_ylim(0, 15000); ax10rr.set_ylim(0, 500)
h3,l3 = ax10r.get_legend_handles_labels(); h4,l4 = ax10rr.get_legend_handles_labels()
ax10r.legend(h3+h4, l3+l4, fontsize=9.5, loc='upper right')
styled_ax(ax10r, title='每日展现量 / 点击量 / 点击率（CTR）')

plt.suptitle('十、推广投放每日趋势（计划报表口径）', fontsize=14, fontweight='bold', y=1.02, color=C['primary'])
plt.tight_layout()
plt.savefig(f'{OUT}/fig10_ads_daily.png', dpi=150, bbox_inches='tight')
plt.close()
print("图10 ✓")

# ══════════════════════════════════════════════════════════════
# 图11：光合内容种草漏斗
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# 左：漏斗图
funnel2_labels = ['内容查看\n5,659人', '商品引导点击\n187人\n(3.30%)', '商品加购\n6人\n(3.21%)', '种草成交\n5人\n(2.67%)']
funnel2_vals   = [5659, 187, 6, 5]
funnel2_w      = [0.9, 0.55, 0.28, 0.22]
funnel2_colors = [C['primary'], C['sec'], C['light'], C['accent']]
for i,(l,v,w_f,c) in enumerate(zip(funnel2_labels,funnel2_vals,funnel2_w,funnel2_colors)):
    axes[0].barh(3-i, w_f, color=c, height=0.55, align='center',
                 edgecolor='white', linewidth=2, zorder=3)
    axes[0].text(w_f/2, 3-i, l, ha='center', va='center',
                 fontsize=10, color='white', fontweight='bold')
axes[0].set_xlim(0, 1.1); axes[0].set_ylim(-0.5, 3.8)
axes[0].axis('off')
axes[0].set_title('光合内容种草转化漏斗', fontsize=12, fontweight='bold', pad=10, color=C['dark'])

# 右：光合核心指标卡
ax11r = axes[1]; ax11r.axis('off')
metrics11 = [
    ('内容查看人数', '5,659人', C['primary']),
    ('内容互动人数', '30人',    C['sec']),
    ('商品引导点击', '187人',   C['sec']),
    ('商品加购人数', '6人',     C['accent']),
    ('种草成交人数', '5人',     C['accent']),
    ('种草成交金额', '¥497.28', C['accent']),
]
for i,(name,val,col) in enumerate(metrics11):
    x_pos = (i%3)*0.35 + 0.05
    y_pos11 = 0.85 - (i//3)*0.45
    ax11r.add_patch(mpatches.FancyBboxPatch((x_pos, y_pos11-0.15), 0.28, 0.38,
        boxstyle='round,pad=0.02', facecolor=C['pale'], edgecolor=col,
        linewidth=2, transform=ax11r.transAxes, zorder=1))
    ax11r.text(x_pos+0.14, y_pos11+0.1, val, transform=ax11r.transAxes,
               ha='center', fontsize=14, fontweight='bold', color=col, va='center')
    ax11r.text(x_pos+0.14, y_pos11-0.07, name, transform=ax11r.transAxes,
               ha='center', fontsize=9, color=C['gray'], va='center')
ax11r.set_title('光合内容核心指标', fontsize=12, fontweight='bold', pad=10, color=C['dark'])
ax11r.text(0.5, 0.02, '内容现阶段重点作为蓄水入口，需绑定高转化商品和主动回访承接',
           transform=ax11r.transAxes, ha='center', fontsize=9.5, color=C['gray'], style='italic')

plt.suptitle('十一、光合内容种草表现', fontsize=14, fontweight='bold', y=1.02, color=C['primary'])
plt.tight_layout()
plt.savefig(f'{OUT}/fig11_content.png', dpi=150, bbox_inches='tight')
plt.close()
print("图11 ✓")

# ══════════════════════════════════════════════════════════════
# 图12：下周工作优先级矩阵
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 7))
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.set_facecolor(C['bg'])

# 四象限背景
ax.fill_between([5,10],[5,5],[10,10], color=C['pale'], alpha=0.5, zorder=1)
ax.fill_between([0,5],[5,5],[10,10], color=C['blue_lt'], alpha=0.3, zorder=1)
ax.fill_between([5,10],[0,0],[5,5], color=C['accent2'], alpha=0.25, zorder=1)
ax.fill_between([0,5],[0,0],[5,5], color=C['gray_lt'], alpha=0.5, zorder=1)
ax.axvline(5, color=C['gray'], lw=1.5, ls='--', alpha=0.6)
ax.axhline(5, color=C['gray'], lw=1.5, ls='--', alpha=0.6)

# 象限标签
ax.text(7.5, 9.5, '第一优先级\n（高影响×高紧迫）', ha='center', fontsize=10,
        color=C['primary'], fontweight='bold', alpha=0.7)
ax.text(2.5, 9.5, '第二优先级\n（低影响×高紧迫）', ha='center', fontsize=10,
        color=C['blue'], fontweight='bold', alpha=0.7)
ax.text(7.5, 0.5, '第三优先级\n（高影响×低紧迫）', ha='center', fontsize=10,
        color=C['accent'], fontweight='bold', alpha=0.7)
ax.text(2.5, 0.5, '暂缓\n（低影响×低紧迫）', ha='center', fontsize=10,
        color=C['gray'], fontweight='bold', alpha=0.7)

# 工作项气泡（影响度, 紧迫度, 标签, 颜色）
tasks = [
    (8.5, 8.5, '退款治理\n(高退款商品页面优化)', C['red'],     200),
    (7.5, 7.5, '主推商品承接\n(5年陈皮详情页)', C['primary'], 180),
    (3.5, 8.0, '客服响应超时\n排班优化',          C['blue'],    140),
    (2.5, 7.0, '5/14推广异常\n排查',              C['blue'],    130),
    (8.0, 4.5, '主动回访SOP\n建立',               C['accent'],  170),
    (7.0, 3.5, '直播成交链路\n优化',              C['accent'],  160),
    (6.5, 4.0, '关键词推广\n词包收窄',            C['accent'],  140),
    (2.0, 3.0, '光合内容\n素材测试',              C['gray'],    120),
]
for (ix, iy, label, col, sz) in tasks:
    ax.scatter(ix, iy, s=sz*3, c=col, alpha=0.75, edgecolors='white', linewidth=2, zorder=3)
    ax.text(ix, iy, label, ha='center', va='center', fontsize=8.5,
            color='white', fontweight='bold', zorder=4)

ax.set_xlabel('影响度（对净销售额的影响）', fontsize=11, color=C['dark'])
ax.set_ylabel('紧迫度（需要本周内完成）', fontsize=11, color=C['dark'])
ax.set_xticks([]); ax.set_yticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(C['gray_lt']); ax.spines['bottom'].set_color(C['gray_lt'])
ax.set_title('下周工作优先级矩阵', fontsize=13, fontweight='bold', pad=12, color=C['dark'])

plt.suptitle('十二、下周工作优先级', fontsize=14, fontweight='bold', y=1.02, color=C['primary'])
plt.tight_layout()
plt.savefig(f'{OUT}/fig12_priority.png', dpi=150, bbox_inches='tight')
plt.close()
print("图12 ✓")

print("\n✅ 全部12张图表生成完成！")
