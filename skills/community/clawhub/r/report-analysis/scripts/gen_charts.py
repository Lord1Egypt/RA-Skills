# -*- coding: utf-8 -*-
'''《评优激励通报》图表可视化（功能E）
生成 6 张分析图（PNG）+ 自包含 HTML 看板（base64 内嵌图片，无需联网可打开）
用法：python gen_charts.py
'''
import os
import base64
import io

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

from analyzer import load_analyzed, summarize, by_county, load_county_summary, fmt_wan
from gen_warn import level_of

# ---------- 字体（跨平台动态探测，避免其他机器中文显示为方框） ----------
def setup_cn_font():
    '''优先按常见中文字体名匹配；都不存在时扫描系统字体文件注册首个中文字体'''
    names = ('Microsoft YaHei', 'SimHei', 'PingFang SC', 'Hiragino Sans GB',
             'Noto Sans CJK SC', 'Noto Sans SC', 'Source Han Sans SC',
             'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Droid Sans Fallback')
    for n in names:
        try:
            font_manager.findfont(n, fallback_to_default=False)
            plt.rcParams['font.sans-serif'] = [n]
            return n
        except Exception:
            continue
    keys = ('yahei', 'msyh', 'simhei', 'pingfang', 'hiragino', 'noto',
            'sourcehan', 'wqy', 'wenquanyi', 'heiti', 'cjk',
            'droidsansfallback')
    picked = None
    try:
        for fp in font_manager.findSystemFonts():
            b = os.path.basename(fp).lower()
            if any(k in b for k in keys):
                try:
                    font_manager.fontManager.addfont(fp)
                    picked = font_manager.FontProperties(fname=fp).get_name()
                    break
                except Exception:
                    continue
    except Exception:
        pass
    if picked:
        plt.rcParams['font.sans-serif'] = [picked]
        return picked
    print('警告：未找到可用的中文字体，图表中的中文可能显示为方框。')
    print('可安装 Noto Sans CJK / 文泉驿等中文字体后重试，或删除 ~/.matplotlib 缓存目录。')
    return None


setup_cn_font()
plt.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.abspath(__file__))
CHART_DIR = os.path.join(BASE, 'charts')
os.makedirs(CHART_DIR, exist_ok=True)
OUT_HTML = os.environ.get('YJ_CHART_OUT', '') or os.path.join(
    BASE, '2026年3季度评优激励-可视化看板.html')

RED = '#C00000'
DARKRED = '#8B0000'
ORANGE = '#ED7D31'
YELLOW = '#FFC000'
GREEN = '#70AD47'
BLUE = '#4472C4'
GRAY = '#A5A5A5'


def save(fig, name):
    p = os.path.join(CHART_DIR, name)
    fig.savefig(p, dpi=130, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return p


def chart_county_loss(chans, cs):
    '''图1 县市损收对比（原始/最终/损收）'''
    ct = by_county(chans)
    names = [x['county'] for x in ct] + ['全州']
    raws = [x['raw'] for x in ct] + [sum(x['raw'] for x in ct)]
    finals = [x['final'] for x in ct] + [sum(x['final'] for x in ct)]
    losses = [r - f for r, f in zip(raws, finals)]
    import numpy as np
    x = np.arange(len(names))
    w = 0.26
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    b1 = ax.bar(x - w, [v / 10000 for v in raws], w, label='原始金额', color=BLUE)
    b2 = ax.bar(x, [v / 10000 for v in finals], w, label='最终金额', color=GRAY)
    b3 = ax.bar(x + w, [v / 10000 for v in losses], w, label='损收', color=RED)
    for bars in (b1, b2, b3):
        ax.bar_label(bars, fmt='%.1f', fontsize=8, padding=2)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=10)
    ax.set_ylabel('金额（万元）')
    ax.set_title('各县（市）激励金额：原始 vs 最终 vs 损收', fontsize=12)
    ax.legend(fontsize=9)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=0.25)
    return save(fig, '1_county_loss.png')


def chart_gate(chans):
    '''图2 门槛完成情况（达档/有量未达档/完全无业务）'''
    gate_ok = [c for c in chans if c['gate_level'] != '门槛未完成']
    notdone = [c for c in chans if c['gate_level'] == '门槛未完成']
    zero_biz = [c for c in notdone if c['tiger'] + c['ai5'] + c['rights_up'] + c['member88'] <= 0]
    has_biz = [c for c in notdone if c not in zero_biz]
    labels = ['门槛达档', '有量未达档', '完全无业务']
    vals = [len(gate_ok), len(has_biz), len(zero_biz)]
    colors = [GREEN, YELLOW, RED]
    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    wedges, texts, autotexts = ax.pie(
        vals, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=90, counterclock=False, radius=0.75,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2},
        textprops={'fontsize': 11})
    for t in autotexts:
        t.set_color('white')
        t.set_fontsize(10)
    ax.set_title(f'门槛完成情况（共 {len(chans)} 家）', fontsize=12)
    ax.legend(wedges, [f'{l}：{v}家' for l, v in zip(labels, vals)],
              loc='lower right', bbox_to_anchor=(1.25, 0), fontsize=9)
    return save(fig, '2_gate.png')


def chart_warn_by_county(chans):
    '''图3 预警分级分布（按县堆叠）'''
    from collections import defaultdict
    d = defaultdict(lambda: {'红牌': 0, '黄牌': 0, '绿牌': 0})
    for c in chans:
        lv, _ = level_of(c)
        d[c['county']][lv] += 1
    counties = list(d.keys())
    order = ['红牌', '黄牌', '绿牌']
    colors = [RED, YELLOW, GREEN]
    bottom = [0] * len(counties)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for lv, col in zip(order, colors):
        vals = [d[cnt][lv] for cnt in counties]
        ax.bar(counties, vals, bottom=bottom, label=lv, color=col, width=0.5)
        for i, v in enumerate(vals):
            if v:
                ax.text(i, bottom[i] + v / 2, str(v), ha='center', va='center',
                        fontsize=9, color='white' if lv == '红牌' else '#404040')
        bottom = [b + v for b, v in zip(bottom, vals)]
    ax.set_ylabel('渠道数（家）')
    ax.set_title('预警分级分布（按县）', fontsize=12)
    ax.legend(fontsize=9)
    ax.spines[['top', 'right']].set_visible(False)
    return save(fig, '3_warn_county.png')


def chart_top_loss(chans):
    '''图4 TOP10 损失渠道'''
    top = sorted(chans, key=lambda c: -c['loss'])[:10]
    names = [c['name'].replace('西双版纳', '').replace('景洪市', '').replace('勐腊县', '').replace('勐海县', '')
             for c in top]
    losses = [c['loss'] / 10000 for c in top]
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    y = range(len(top))
    bars = ax.barh(list(y), losses, color=[RED if c['final'] < 0 else ORANGE for c in top])
    ax.set_yticks(list(y))
    ax.set_yticklabels(names, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlabel('损收（万元）')
    ax.set_title('损收 TOP10 渠道', fontsize=12)
    for b, v in zip(bars, losses):
        ax.text(v + 0.03, b.get_y() + b.get_height() / 2, f'{v:.2f}万', va='center', fontsize=8.5)
    ax.set_xlim(0, max(losses) * 1.18)
    ax.spines[['top', 'right']].set_visible(False)
    return save(fig, '4_top_loss.png')


def chart_loss_dist(chans):
    '''图5 渠道损失率分布'''
    rates = [c['loss_rate'] for c in chans if c['raw'] > 0]
    bins = [0, 20, 40, 60, 80, 100]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    n, _, patches = ax.hist(rates, bins=bins, color=ORANGE, edgecolor='white', align='left')
    for p, cnt in zip(patches, n):
        ax.text(p.get_x() + p.get_width() / 2, cnt + 2, f'{int(cnt)}家',
                ha='center', fontsize=9)
    ax.set_xticks(bins)
    ax.set_xlabel('损收率区间（%）')
    ax.set_ylabel('渠道数（家）')
    ax.set_title('渠道损收率分布', fontsize=12)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=0.25)
    return save(fig, '5_loss_dist.png')


def chart_loss_compose(cs):
    '''图6 逐道损收构成（以县汇总表为准，单位万元）'''
    items = [('门槛未完成', cs['全州']['gate_loss']),
             ('终端合约搭载', cs['全州']['term_loss']),
             ('重点业务牵引', cs['全州']['focus_loss']),
             ('投诉', cs['全州']['complaint_loss']),
             ('弱势网格', cs['全州']['weakgrid_loss']),
             ('APP融合', cs['全州']['app_loss'])]
    items = [(l, abs(v)) for l, v in items]
    items.sort(key=lambda x: x[1])
    labels = [l for l, _ in items]
    vals = [v for _, v in items]
    maxv = max(vals) if vals else 1
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    colors = [RED if v == maxv and v > 0.001 else (GRAY if v <= 0.001 else ORANGE) for v in vals]
    bars = ax.barh(labels, vals, color=colors)
    for b, v in zip(bars, vals):
        text = f'{v:.2f}万' if v > 0.001 else '0.00万（无损失）'
        offset = maxv * 0.02 if v <= 0.001 else v + 0.1
        ax.text(offset, b.get_y() + b.get_height() / 2, text, va='center', fontsize=9)
    ax.set_xlabel('损收（万元）')
    ax.set_title('逐道核算损收构成（全州，县汇总表口径）', fontsize=12)
    ax.set_xlim(0, maxv * 1.22)
    ax.spines[['top', 'right']].set_visible(False)
    return save(fig, '6_loss_compose.png')


def img_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')


def build_html(charts, s, rows):
    '''自包含 HTML 看板'''
    red = sum(1 for r in rows if r['level'] == '红牌')
    yellow = sum(1 for r in rows if r['level'] == '黄牌')
    green = sum(1 for r in rows if r['level'] == '绿牌')
    cards = [
        ('渠道总数', f"{s['n']} 家", BLUE),
        ('原始激励金额', fmt_wan(s['raw_total']), BLUE),
        ('最终核算金额', fmt_wan(s['final_total']), GRAY),
        ('损收合计', fmt_wan(s['loss_total']) + f"（{s['loss_rate']:.1f}%）", RED),
        ('门槛未完成', f"{s['gate_notdone']} 家（{s['gate_notdone_rate']:.1f}%）", RED),
        ('红牌渠道', f'{red} 家', RED),
        ('黄牌渠道', f'{yellow} 家', YELLOW),
        ('绿牌渠道', f'{green} 家', GREEN),
    ]
    card_html = ''.join(
        f'<div style="background:{col};color:#fff;border-radius:10px;padding:14px 8px;'
        f'text-align:center;min-width:110px;flex:1">'
        f'<div style="font-size:12px;opacity:.9">{t}</div>'
        f'<div style="font-size:20px;font-weight:700;margin-top:4px">{v}</div></div>'
        for t, v, col in cards)
    imgs = ''.join(
        f'<figure style="margin:0 0 26px"><img src="data:image/png;base64,{img_b64(p)}" '
        f'style="width:100%;border:1px solid #e5e5e5;border-radius:8px"/></figure>'
        for p in charts)
    html = ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"/>'
            '<title>2026年3季度评优激励-可视化看板</title></head>'
            '<body style="margin:0;background:#f5f6f8;font-family:Microsoft YaHei,SimHei,PingFang SC,Noto Sans CJK SC,sans-serif">'
            '<div style="max-width:1080px;margin:0 auto;padding:28px 20px">'
            '<h1 style="font-size:22px;margin:0 0 6px">2026年3季度合作伙伴评优激励 · 可视化看板</h1>'
            '<div style="color:#888;font-size:13px;margin-bottom:20px">数据来源：2026年3季度合作伙伴评优激励通报20260811 · 渠道完成情况通报表</div>'
            f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:28px">{card_html}</div>'
            f'{imgs}</div></body></html>')
    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    return OUT_HTML


def main():
    chans = load_analyzed()
    s = summarize(chans)
    cs = load_county_summary()
    charts = [
        chart_county_loss(chans, cs),
        chart_gate(chans),
        chart_warn_by_county(chans),
        chart_top_loss(chans),
        chart_loss_dist(chans),
        chart_loss_compose(cs),
    ]
    rows = []
    for c in chans:
        lv, note = level_of(c)
        rows.append(dict(level=lv, note=note))
    html = build_html(charts, s, rows)
    print(f'图表已生成: {CHART_DIR}/ (6张)')
    print(f'看板已生成: {html}')


if __name__ == '__main__':
    main()
