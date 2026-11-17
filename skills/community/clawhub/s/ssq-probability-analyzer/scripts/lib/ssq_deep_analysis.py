# -*- coding: utf-8 -*-
"""
双色球 · 深度号码分析（学习增强版）  (V2.1.35-升级 新增)

目的: 把全网研究得到的「彩票特征工程」思路落地为一组**描述性统计观察**，
      用于让用户更深入地理解号码的冷热与结构特征，提升系统的信息价值。

诚实边界（与全站打假基调一致）:
  - 本模块**只做统计描述**，不预测、不宣称任何号码更可能开出。
  - 双色球每期独立随机，历史统计无法预示未来；以下观察仅供「理解数据趣味」。
  - 所有数值均来自 ssq_history.json 的真实历史开奖，可复现、可核对。

增量维度（相对 compute_models 已有的 CDM/马尔可夫/近30频率/当前遗漏）:
  1. 多窗口频率 Z-score 冷热 (30/50/100/200 期)
  2. 历史均值/中位数间隔 (overdue) → 统计极冷判定
  3. 近期结构特征 (三区比/奇偶比/大小比/012路/连号/和值/跨度)
  4. 分布健康度 (香农熵)
"""

import math
from collections import Counter, defaultdict


def _expected_appear(draws_n, slots=6, nums=33):
    """W 期内某号理论出现次数与二项标准差。"""
    p = slots / nums
    exp = draws_n * p
    std = math.sqrt(draws_n * p * (1 - p))
    return exp, std


def _gaps_for(num, draws):
    """返回某红球在历史中出现位置的间隔列表（相邻两次出现的期数差）。"""
    idxs = [i for i, d in enumerate(draws) if num in d.get('front', [])]
    gaps = []
    for a, b in zip(idxs, idxs[1:]):
        gaps.append(b - a)
    return gaps


def analyze_deep(draws):
    """计算全部深度特征，返回结构化 dict。draws 为历史开奖列表(含最新一期)。"""
    if not draws:
        return {}
    red_nums = list(range(1, 34))
    blue_nums = list(range(1, 17))

    # ---------- 1. 多窗口频率 Z-score 冷热 ----------
    windows = [30, 50, 100, 200]
    win_freq = {}
    for w in windows:
        sub = draws[-w:]
        c = Counter()
        for d in sub:
            for n in d.get('front', []):
                c[n] += 1
        win_freq[w] = c

    z_by_window = {}
    for w in windows:
        exp, std = _expected_appear(w)
        std = std or 1e-9
        z = {}
        for n in red_nums:
            obs = win_freq[w].get(n, 0)
            z[n] = (obs - exp) / std
        z_by_window[w] = z

    # 取最近窗口(30)做 Top 热/冷展示；同时给每号一个"综合冷热分"(多窗口 Z 均值)
    composite = {n: sum(z_by_window[w][n] for w in windows) / len(windows) for n in red_nums}
    hot = sorted(red_nums, key=lambda n: composite[n], reverse=True)[:6]
    cold = sorted(red_nums, key=lambda n: composite[n])[:6]

    # ---------- 2. 历史均值/中位数间隔 (overdue) ----------
    gap_stats = {}
    current_omit = {}
    for num in red_nums:
        gaps = _gaps_for(num, draws)
        if gaps:
            gap_stats[num] = (sum(gaps) / len(gaps), sorted(gaps)[len(gaps) // 2])
        else:
            gap_stats[num] = (0, 0)
        # 当前遗漏：从最新一期往前数连续未出
        omit = 0
        for i in range(len(draws) - 1, -1, -1):
            if num in draws[i].get('front', []):
                break
            omit += 1
        current_omit[num] = omit

    # 统计极冷: 当前遗漏 > 1.5 × 历史均值间隔
    stat_cold = [n for n in red_nums
                 if gap_stats[n][0] > 0 and current_omit[n] > 1.5 * gap_stats[n][0]]

    # ---------- 3. 近期结构特征 (近30期) ----------
    recent = draws[-30:]
    zone = lambda n: 0 if n <= 11 else (1 if n <= 22 else 2)
    struct = {
        'zone': Counter(), 'odd': 0, 'even': 0, 'big': 0, 'small': 0,
        'mod': Counter(), 'sums': [], 'spans': [], 'consecutive': 0,
    }
    for d in recent:
        fr = d.get('front', [])
        for n in fr:
            struct['zone'][zone(n)] += 1
            if n % 2 == 0:
                struct['even'] += 1
            else:
                struct['odd'] += 1
            if n > 17:
                struct['big'] += 1
            else:
                struct['small'] += 1
            struct['mod'][n % 3] += 1
        s = sum(fr)
        struct['sums'].append(s)
        struct['spans'].append(max(fr) - min(fr))
        # 连号: 存在相邻差1
        sf = sorted(fr)
        if any(sf[i + 1] - sf[i] == 1 for i in range(len(sf) - 1)):
            struct['consecutive'] += 1

    n_red = len(recent) * 6
    avg_sum = sum(struct['sums']) / len(struct['sums']) if struct['sums'] else 0
    avg_span = sum(struct['spans']) / len(struct['spans']) if struct['spans'] else 0
    conj_rate = struct['consecutive'] / len(recent) if recent else 0

    # ---------- 4. 分布健康度 (香农熵) ----------
    cnt = Counter()
    for d in draws:
        for n in d.get('front', []):
            cnt[n] += 1
    total_obs = sum(cnt.values()) or 1
    entropy = -sum((c / total_obs) * math.log2(c / total_obs) for c in cnt.values() if c > 0)
    max_entropy = math.log2(33)
    entropy_ratio = entropy / max_entropy if max_entropy else 0

    return {
        'windows': windows,
        'z_by_window': z_by_window,
        'composite': composite,
        'hot': hot,
        'cold': cold,
        'current_omit': current_omit,
        'gap_stats': gap_stats,
        'stat_cold': stat_cold,
        'struct': {
            'zone': dict(struct['zone']),
            'odd': struct['odd'], 'even': struct['even'],
            'big': struct['big'], 'small': struct['small'],
            'mod': dict(struct['mod']),
            'avg_sum': avg_sum, 'avg_span': avg_span, 'conj_rate': conj_rate,
        },
        'entropy': entropy,
        'entropy_ratio': entropy_ratio,
    }


def _ball(n, cls='ball-red'):
    return f'<span class="ball {cls}" style="width:26px;height:26px;line-height:26px;font-size:12px;">{n:02d}</span>'


def render_deep_analysis_html(draws):
    """返回「深度号码分析」面板 HTML（只做描述，不改预测）。"""
    try:
        a = analyze_deep(draws)
    except Exception as e:
        return f'<div class="section"><div class="section-title">深度号码分析</div>' \
               f'<div class="info" style="border-color:#ff5555;">⚠ 深度分析计算异常: {e}</div></div>'

    if not a:
        return ''

    hot_html = ' '.join(_ball(n) for n in a['hot'])
    cold_html = ' '.join(_ball(n) for n in a['cold'])
    stat_cold_html = ' '.join(_ball(n) for n in a['stat_cold']) if a['stat_cold'] else '<span style="color:#888;">（当前无统计极冷号）</span>'

    # 多窗口 Z 表（取 Top 热与 Top 冷 各 6 号，展示 30/50/100/200 期 Z）
    show_nums = a['hot'] + a['cold']
    rows = ''
    for n in show_nums:
        zcells = ''.join(
            f'<td style="text-align:center;color:{"#ff7b00" if a["z_by_window"][w][n] > 1 else ("#4aa3ff" if a["z_by_window"][w][n] < -1 else "#bbb")};">'
            f'{a["z_by_window"][w][n]:+.2f}</td>'
            for w in a['windows'])
        rows += f'<tr><td style="text-align:center;">{_ball(n)}</td>{zcells}' \
                f'<td style="text-align:center;color:#999;">遗漏 {a["current_omit"][n]} 期</td></tr>'

    s = a['struct']
    total_zone = sum(s['zone'].values()) or 1
    total_oe = (s['odd'] + s['even']) or 1
    total_mod = sum(s['mod'].values()) or 1

    html = f"""
<div class="section">
<div class="section-title">📊 深度号码分析（学习增强版 · 描述性观察，不预示未来）</div>
<div class="info" style="border-color:#5577ff; background:#10122a;">
<p style="color:#aab4ff; font-size:12.5px; line-height:1.7; margin:6px 0;">
本栏基于 {len(draws)} 期真实历史开奖，用「多窗口频率 Z-score / 历史间隔 / 结构特征 / 香农熵」四个维度刻画号码的冷热与分布。
<b style="color:#ffd9a0;">双色球每期独立随机，以下观察仅供理解数据趣味，不构成任何选号建议。</b>
</p>
</div>

<div class="sub" style="margin-top:14px;">① 红球冷热（综合 Z-score：多窗口均值）</div>
<table>
<tr><th>类型</th><th>号码</th><th>说明</th></tr>
<tr><td style="color:#ff7b00;">🔥 近期偏热</td><td>{hot_html}</td><td style="color:#888;">综合 Z&gt;0，近 30/50/100/200 期出现频率高于理论</td></tr>
<tr><td style="color:#4aa3ff;">❄️ 近期偏冷</td><td>{cold_html}</td><td style="color:#888;">综合 Z&lt;0，出现频率低于理论</td></tr>
<tr><td style="color:#ff5577;">📉 统计极冷</td><td>{stat_cold_html}</td><td style="color:#888;">当前遗漏 &gt; 1.5×历史均值间隔，回补概率略高（仍随机）</td></tr>
</table>

<div class="sub" style="margin-top:14px;">② 多窗口 Z-score 明细（红=偏热 / 蓝=偏冷）</div>
<table>
<tr><th>号码</th><th>近30期</th><th>近50期</th><th>近100期</th><th>近200期</th><th>当前遗漏</th></tr>
{rows}
</table>

<div class="sub" style="margin-top:14px;">③ 近期结构特征（近 30 期均值）</div>
<table>
<tr><th>维度</th><th>观测值</th><th>经验常态</th></tr>
<tr><td>三区比 (01-11 / 12-22 / 23-33)</td><td>{s['zone'].get(0,0)} / {s['zone'].get(1,0)} / {s['zone'].get(2,0)}</td><td>≈ 2:2:2</td></tr>
<tr><td>奇偶比</td><td>{s['odd']} : {s['even']}（{(s['odd']/total_oe*100):.0f}% 奇）</td><td>3:3 / 4:2 为主</td></tr>
<tr><td>大小比（18及以上为大）</td><td>{s['small']} : {s['big']}</td><td>3:3 均衡</td></tr>
<tr><td>012 路分布</td><td>0路 {s['mod'].get(0,0)} / 1路 {s['mod'].get(1,0)} / 2路 {s['mod'].get(2,0)}</td><td>三路趋均</td></tr>
<tr><td>平均和值</td><td>{s['avg_sum']:.1f}</td><td>理论均值 ≈ 102</td></tr>
<tr><td>平均跨度</td><td>{s['avg_span']:.1f}</td><td>多在 18-28</td></tr>
<tr><td>连号出现率</td><td>{s['conj_rate']*100:.0f}%</td><td>历史约 60-70%</td></tr>
</table>

<div class="sub" style="margin-top:14px;">④ 分布健康度</div>
<div class="info" style="border-color:#00dd88;">
<p style="color:#aaf0c8; font-size:13px; line-height:1.8; margin:6px 0;">
红球出现分布的香农熵 = <b>{a['entropy']:.3f}</b> / 理论最大 {math.log2(33):.3f}
（均匀度 <b>{a['entropy_ratio']*100:.1f}%</b>）。
熵越接近理论上限，说明历史号码分布越均匀、无显著偏倚——这也从侧面印证了开奖的随机性。
</p>
</div>
</div>
"""
    return html


if __name__ == '__main__':
    import json
    d = json.load(open('ssq_history.json', encoding='utf-8'))
    print(render_deep_analysis_html(d))
