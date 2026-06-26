#!/usr/bin/env python3
"""生成月度支出报表 HTML - 暖可可风格"""

import json
import math
import os
from datetime import datetime, timedelta
from collections import defaultdict

from module import CAT_CONFIG, load_data

# 脚本所在目录（用于默认输出路径）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')

def _get_month_data(expenses, month=None):
    """提取指定月份数据，默认最新月份"""
    by_month = defaultdict(list)
    for e in expenses:
        by_month[e['date'][:7]].append(e)
    target_month = month or max(by_month.keys())
    if target_month not in by_month:
        print(f"{target_month} 没有数据")
        return target_month, []
    return target_month, sorted(by_month[target_month], key=lambda x: x['date'])

def generate_report(expenses_file, config_file, output_file=None, month=None, _skip_adjacent=False, force=False):
    expenses = load_data(expenses_file)

    with open(config_file, 'r') as f:
        config = json.load(f)
    
    budget = config.get('monthly_budget', 2000)
    
    if not expenses:
        print("暂无数据")
        return
    
    import html as html_mod
    esc = html_mod.escape
    
    latest_month, month_expenses = _get_month_data(expenses, month)
    
    if not month_expenses:
        print(f"{latest_month} 没有数据")
        return
    
    total = sum(e['amount'] for e in month_expenses)
    by_cat = defaultdict(float)
    for e in month_expenses:
        by_cat[e['category']] += e['amount']
    
    # 按日统计
    by_day = defaultdict(float)
    for e in month_expenses:
        by_day[e['date']] += e['amount']
    day_dates = sorted(by_day.keys())
    max_day = max(by_day.values()) if by_day else 1
    
    # 统计数据
    count = len(month_expenses)
    avg_daily = total / len(set(e['date'] for e in month_expenses)) if month_expenses else 0
    max_single = max(month_expenses, key=lambda x: x['amount']) if month_expenses else None
    min_day = min(by_day, key=by_day.get) if by_day else None
    max_day_date = max(by_day, key=by_day.get) if by_day else None
    most_cat = max(by_cat, key=by_cat.get) if by_cat else None
    
    budget_pct = min((total / budget) * 100, 100) if budget > 0 else 0
    over_budget = total > budget
    budget_remain = budget - total

    # 与上月对比
    by_month_all = defaultdict(list)
    for e in expenses:
        by_month_all[e['date'][:7]].append(e)
    all_months = sorted(by_month_all.keys())
    prev_month = None
    prev_total = None
    prev_by_cat = None
    compare_html = ""
    idx = all_months.index(latest_month) if latest_month in all_months else -1
    if idx > 0:
        prev_month = all_months[idx - 1]
        prev_expenses = by_month_all[prev_month]
        prev_total = sum(e['amount'] for e in prev_expenses)
        prev_by_cat = defaultdict(float)
        for e in prev_expenses:
            prev_by_cat[e['category']] += e['amount']
        total_diff = total - prev_total
        total_pct = (total_diff / prev_total * 100) if prev_total > 0 else 0

        all_cats = sorted(set(list(by_cat.keys()) + list(prev_by_cat.keys())),
                         key=lambda c: by_cat.get(c, 0), reverse=True)
        cat_rows = ""
        for cat in all_cats:
            cur = by_cat.get(cat, 0)
            pre = prev_by_cat.get(cat, 0)
            diff = cur - pre
            pct = (diff / pre * 100) if pre > 0 else (100 if cur > 0 else 0)
            cfg = CAT_CONFIG.get(cat, CAT_CONFIG['其他'])
            if diff > 0:
                arrow = '<span class="cmp-up">+' + f'{pct:.0f}' + '%</span>'
            elif diff < 0:
                arrow = '<span class="cmp-down">' + f'{pct:.0f}' + '%</span>'
            else:
                arrow = '<span class="cmp-same">--</span>'
            cat_rows += f'''<div class="cmp-row">
                <span class="cmp-cat"><span class="cmp-dot" style="background:{cfg['color']}"></span>{cfg['emoji']} {esc(cat)}</span>
                <span class="cmp-cur">¥{cur:.2f}</span>
                <span class="cmp-prev">¥{pre:.2f}</span>
                {arrow}
            </div>'''

        prev_display = datetime.strptime(prev_month, "%Y-%m").strftime("%m月")
        total_arrow_cls = "cmp-up" if total_diff > 0 else ("cmp-down" if total_diff < 0 else "cmp-same")
        total_arrow_sign = "+" if total_diff > 0 else ""
        compare_html = f'''<section class="card">
  <div class="card-label">环比对比 <small style="font-weight:400;color:var(--text-light);letter-spacing:0">vs {prev_display}</small></div>
  <div class="cmp-header">
    <div class="cmp-total-row">
      <span class="cmp-total-label">本月 ¥{total:.2f}</span>
      <span class="cmp-total-diff {total_arrow_cls}">{total_arrow_sign}¥{abs(total_diff):.2f}（{total_arrow_sign}{total_pct:.1f}%）</span>
    </div>
  </div>
  <div class="cmp-table">
    <div class="cmp-table-head">
      <span>分类</span><span>本月</span><span>上月</span><span>变化</span>
    </div>
    {cat_rows}
  </div>
</section>'''

    # 月份导航
    nav_prev = all_months[idx - 1] if idx > 0 else None
    nav_next = all_months[idx + 1] if idx < len(all_months) - 1 else None
    nav_prev_file = f"report-{nav_prev}.html" if nav_prev else None
    nav_next_file = f"report-{nav_next}.html" if nav_next else None
    nav_prev_display = datetime.strptime(nav_prev, "%Y-%m").strftime("%m月") if nav_prev else None
    nav_next_display = datetime.strptime(nav_next, "%Y-%m").strftime("%m月") if nav_next else None
    
    # 饼图（SVG 可交互分段）
    sorted_cats = sorted(by_cat.items(), key=lambda x: x[1], reverse=True)
    pie_svg_parts = []
    cx, cy, r = 80, 80, 75
    cum_pct = 0
    for i, (cat, amount) in enumerate(sorted_cats):
        pct = (amount / total * 100) if total > 0 else 0
        cfg = CAT_CONFIG.get(cat, CAT_CONFIG['其他'])
        start_rad = cum_pct / 100 * 2 * math.pi - math.pi / 2
        end_pct = 100 if i == len(sorted_cats) - 1 else cum_pct + pct
        end_rad = end_pct / 100 * 2 * math.pi - math.pi / 2
        mid_rad = (start_rad + end_rad) / 2
        x1 = cx + r * math.cos(start_rad)
        y1 = cy + r * math.sin(start_rad)
        x2 = cx + r * math.cos(end_rad)
        y2 = cy + r * math.sin(end_rad)
        large = 1 if pct > 50 else 0
        tx = round(6 * math.cos(mid_rad), 2)
        ty = round(6 * math.sin(mid_rad), 2)
        d = f'M {cx} {cy} L {x1:.2f} {y1:.2f} A {r} {r} 0 {large} 1 {x2:.2f} {y2:.2f} Z'
        pie_svg_parts.append(
            f'<path class="pie-seg" d="{d}" fill="{cfg["color"]}" '
            f'data-cat="{cat}" data-amount="{amount:.2f}" data-pct="{pct:.1f}" '
            f'style="--tx:{tx}px;--ty:{ty}px"/>'
        )
        cum_pct += pct
    pie_svg = ''.join(pie_svg_parts)
    
    # 趋势柱状图 SVG
    if len(day_dates) > 1:
        w, h = 600, 170
        pad_l, pad_r, pad_t, pad_b = 45, 20, 20, 30
        chart_w = w - pad_l - pad_r
        chart_h = h - pad_t - pad_b

        # 网格线
        grid_lines = ""
        for i in range(5):
            gy = pad_t + chart_h * i / 4
            gv = max_day * (1 - i / 4)
            grid_lines += f'<line x1="{pad_l}" y1="{gy:.1f}" x2="{w - pad_r}" y2="{gy:.1f}" stroke="rgba(0,0,0,0.05)" stroke-width="1"/>'
            grid_lines += f'<text x="{pad_l - 6}" y="{gy + 3:.1f}" text-anchor="end" fill="#b5a48c" font-size="9">¥{gv:.0f}</text>'

        # 日均参考线
        avg_day_amt = total / len(day_dates) if day_dates else 0
        avg_y = pad_t + chart_h - (avg_day_amt / max_day * chart_h) if max_day > 0 else pad_t + chart_h
        avg_line = f'<line x1="{pad_l}" y1="{avg_y:.1f}" x2="{w - pad_r}" y2="{avg_y:.1f}" stroke="#c8956c" stroke-width="1" stroke-dasharray="4 3" opacity=".5"/>'
        avg_line += f'<text x="{w - pad_r + 4}" y="{avg_y + 3:.1f}" fill="#c8956c" font-size="8" opacity=".7">均值</text>'

        # 柱子
        bar_gap = max(2, chart_w / len(day_dates) * 0.3)
        bar_w = (chart_w - bar_gap * (len(day_dates) + 1)) / len(day_dates)
        bar_w = max(bar_w, 6)
        bars = ""
        for i, d in enumerate(day_dates):
            amt = by_day[d]
            bh = (amt / max_day) * chart_h if max_day > 0 else 0
            bh = max(bh, 2)
            bx = pad_l + bar_gap + i * (bar_w + bar_gap)
            by = pad_t + chart_h - bh
            rx = min(bar_w / 2, 4)
            bars += f'<rect class="trend-bar" x="{bx:.1f}" y="{by:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="{rx}" data-date="{d}" data-amount="{amt:.2f}"/>'
            bars += f'<text class="trend-label" x="{bx + bar_w/2:.1f}" y="{h - 8}" text-anchor="middle">{d[8:]}</text>'

        trend_svg = f'''<div class="trend-wrap">
        <svg viewBox="0 0 {w} {h}" class="trend-svg">
            <defs>
                <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#c8956c"/>
                    <stop offset="100%" stop-color="#d4a87a"/>
                </linearGradient>
            </defs>
            {grid_lines}
            {avg_line}
            {bars}
        </svg>
        <div class="trend-tooltip" id="trendTip">
            <div class="trend-tip-date" id="trendTipDate"></div>
            <div class="trend-tip-amount" id="trendTipAmt"></div>
        </div>
        </div>'''
    else:
        trend_svg = '<p style="text-align:center;color:#aaa;padding:20px">数据太少，暂无趋势图</p>'
    
    # 明细
    rows_html = ""
    for e in reversed(month_expenses):
        cfg = CAT_CONFIG.get(e['category'], CAT_CONFIG['其他'])
        rows_html += f'''
        <div class="detail-item" data-category="{esc(e['category'])}" data-date="{e['date']}">
            <div class="detail-left">
                <span class="detail-emoji">{cfg['emoji']}</span>
                <div class="detail-info">
                    <div class="detail-desc">{html_mod.escape(e.get('description', ''))}</div>
                    <div class="detail-sub">{e['date']} · {esc(e['category'])}</div>
                </div>
            </div>
            <div class="detail-amount">-¥{e['amount']:.2f}</div>
        </div>'''
    
    # 分类卡片
    cat_cards = ""
    for cat, amount in sorted_cats:
        cfg = CAT_CONFIG.get(cat, CAT_CONFIG['其他'])
        pct = (amount / total * 100) if total > 0 else 0
        cat_cards += f'''
        <div class="cat-card" data-cat="{esc(cat)}" style="background:{cfg['bg']}">
            <div class="cat-emoji">{cfg['emoji']}</div>
            <div class="cat-name">{esc(cat)}</div>
            <div class="cat-amount">¥{amount:.2f}</div>
            <div class="cat-bar-bg">
                <div class="cat-bar" style="width:{pct}%;background:{cfg['color']}"></div>
            </div>
            <div class="cat-pct">{pct:.1f}%</div>
        </div>'''
    
    month_display = datetime.strptime(latest_month, "%Y-%m").strftime("%Y年%m月")
    
    if min_day and max_day_date and max_single and most_cat:
        summary = f"最省的一天是{min_day[8:]}号（¥{by_day[min_day]:.2f}），最贵的一笔是{esc(max_single['category'])}¥{max_single['amount']:.2f}，{esc(most_cat)}是最大开销"
    else:
        summary = f"共{count}笔支出"
    
    ring_pct = budget_pct if not over_budget else 100
    ring_color = "#c8956c" if not over_budget else "#c97070"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{month_display} 支出报表</title>
<style>
  :root {{
    --bg: #faf8f5;
    --card: #ffffff;
    --accent: #c8956c;
    --accent-hover: #a87a55;
    --accent-light: rgba(200,149,108,0.1);
    --accent-glow: rgba(200,149,108,0.25);
    --heading: #3d2c22;
    --text: #3d2c22;
    --text-mid: #8b7355;
    --text-light: #b5a48c;
    --border: #e8e0d6;
    --shadow-card: rgba(61,44,34,0.06) 0px 12px 24px -12px, rgba(61,44,34,0.04) 0px 8px 16px -8px;
    --shadow-hover: rgba(61,44,34,0.1) 0px 20px 36px -16px, rgba(61,44,34,0.06) 0px 12px 24px -12px;
    --radius: 12px;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
    background: var(--bg);
    color: var(--text);
    padding: 24px 16px 48px;
    margin: 0 auto;
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
    position: relative;
    overflow-x: hidden;
    scroll-behavior: smooth;
  }}

  /* ---- 背景装饰 ---- */
  .orb {{
    position: fixed; border-radius: 50%; pointer-events: none; z-index: 0;
    filter: blur(100px); opacity: .45;
  }}
  .orb-1 {{ width: 380px; height: 380px; background: rgba(200,149,108,0.12); top: -80px; right: -80px; }}
  .orb-2 {{ width: 280px; height: 280px; background: rgba(201,112,112,0.08); bottom: 15%; left: -60px; }}

  /* ---- 入场动画 ---- */
  @media (prefers-reduced-motion: reduce) {{
    .orb {{ animation: none; }}
  }}

  @keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  /* ---- Header ---- */
  .header {{ text-align: center; padding: 24px 0 12px; position: relative; z-index: 1; }}
  .header h1 {{
    font-size: 22px; font-weight: 600; color: var(--text);
    letter-spacing: -.5px; display: inline-flex; align-items: center; gap: 10px;
  }}
  .header .subtitle {{ font-size: 12px; color: var(--text-mid); margin-top: 4px; }}

  /* ---- 卡片 ---- */
  .card {{
    background: var(--card); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 20px 18px; margin-bottom: 12px;
    box-shadow: var(--shadow-card);
    position: relative; z-index: 1;
    transition: box-shadow .25s ease;
  }}
  .card:hover {{
    box-shadow: var(--shadow-hover);
  }}
  .card-overflow {{ overflow: visible; z-index: 2; }}
  .card-label {{
    font-size: 12px; font-weight: 600; color: var(--text);
    letter-spacing: -.2px; margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
    flex-shrink: 0;
  }}
  .card-label::before {{
    content: ''; width: 3px; height: 14px;
    background: var(--accent); border-radius: 2px; flex-shrink: 0;
  }}

  /* ---- 总览 ---- */
  .overview {{  }}
  .overview-top {{
    display: flex; align-items: center; justify-content: center; gap: 24px;
    margin: 8px 0 4px;
  }}
  .overview-left {{ display: flex; flex-direction: column; align-items: flex-start; min-width: 0; }}
  .total-amount {{
    font-size: 42px; font-weight: 300; color: var(--text);
    letter-spacing: -1.5px; margin: 0; font-variant-numeric: tabular-nums;
    line-height: 1.1;
  }}
  .total-amount small {{ font-size: 14px; font-weight: 400; color: var(--text-light); }}
  .budget-summary {{
    display: flex; gap: 16px; margin-top: 8px; font-size: 12px;
  }}
  .budget-summary span {{ color: var(--text-mid); }}
  .budget-summary strong {{ color: var(--text); font-weight: 500; font-variant-numeric: tabular-nums; }}

  /* 环形进度 */
  .ring {{
    position: relative; width: 100px; height: 100px; flex-shrink: 0;
  }}
  .ring svg {{ display: block; width: 100%; height: 100%; transform: rotate(-90deg); }}
  .ring-text {{
    position: absolute; inset: 0; display: flex; flex-direction: column;
    align-items: center; justify-content: center; text-align: center;
  }}
  .ring-pct {{
    font-size: 20px; font-weight: 600; color: {ring_color};
    font-variant-numeric: tabular-nums; line-height: 1;
  }}
  .ring-label {{
    font-size: 10px; color: var(--text-light); margin-top: 3px;
  }}
  .ring-info {{
    position: absolute; inset: 0; display: flex; flex-direction: column;
    align-items: center; justify-content: center; text-align: center;
    opacity: 0; transition: opacity .2s ease; pointer-events: none;
  }}
  .ring:hover .ring-text {{ opacity: 0; }}
  .ring:hover .ring-info {{ opacity: 1; }}
  .ring-info-line {{
    font-size: 12px; font-weight: 500; color: var(--text);
    font-variant-numeric: tabular-nums; line-height: 1.6;
  }}
  .ring-info-line.warn {{ color: #c97070; }}

  /* 预算进度条 */
  .budget-bar-wrap {{ margin-top: 18px; text-align: left; }}
  .budget-bar-head {{
    display: flex; justify-content: space-between; align-items: baseline;
    font-size: 11px; margin-bottom: 6px;
  }}
  .budget-bar-label {{ color: var(--text-light); }}
  .budget-bar-pct {{ color: {ring_color}; font-weight: 500; font-variant-numeric: tabular-nums; }}
  .budget-bar {{
    height: 5px; background: #f0ebe5; border-radius: 3px; overflow: hidden;
  }}
  .budget-bar-fill {{
    height: 100%; border-radius: 3px; background: {ring_color};
    transition: width 1s cubic-bezier(.22,1,.36,1);
  }}

  /* 统计条 */
  .stats-row {{ display: flex; gap: 10px; margin-top: 20px; justify-content: center; }}
  .stat-item {{
    flex: 1; text-align: center; padding: 14px 8px;
    background: #f7f3ee; border-radius: 10px;
    border: 1px solid var(--border);
    transition: all .2s ease; position: relative; cursor: default;
  }}
  .stat-item:hover {{
    box-shadow: rgba(61,44,34,0.06) 0px 6px 12px -4px;
    transform: translateY(-1px);
  }}
  .stat-num {{ font-size: 20px; font-weight: 600; color: var(--accent); font-variant-numeric: tabular-nums; }}
  .stat-desc {{ font-size: 10px; color: var(--text-mid); margin-top: 3px; }}
  .stat-tip {{
    position: absolute; bottom: calc(100% + 6px); left: 50%; transform: translateX(-50%);
    background: #fff; border: 1px solid var(--border); border-radius: 6px;
    padding: 6px 10px; font-size: 11px; color: var(--text-mid);
    box-shadow: var(--shadow-hover); white-space: nowrap;
    opacity: 0; pointer-events: none; transition: opacity .15s ease;
    z-index: 5;
  }}
  .stat-item:hover .stat-tip {{ opacity: 1; }}

  /* ---- 饼图 ---- */
  .chart-section {{ display: flex; flex-direction: column; align-items: center; position: relative; overflow: visible; }}
  .pie-wrap {{ position: relative; margin: 8px 0 24px; overflow: visible; }}
  .pie-svg {{ width: 170px; height: 170px; cursor: pointer; }}
  .pie-seg {{
    stroke: #fff; stroke-width: 1.5; transform-origin: 80px 80px;
    transition: transform .2s ease, filter .2s ease;
  }}
  .pie-seg:hover, .pie-seg.active {{
    transform: translate(var(--tx), var(--ty)) scale(1.05);
    filter: brightness(1.05) drop-shadow(0 2px 6px rgba(61,44,34,0.15));
  }}
  .pie-center-abs {{
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    width: 80px; height: 80px;
    background: #fff; border-radius: 50%;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    transition: all .2s ease; cursor: default;
  }}
  .pie-center-num {{ font-size: 18px; font-weight: 600; color: var(--text); font-variant-numeric: tabular-nums; transition: all .2s ease; }}
  .pie-center-label {{ font-size: 10px; color: var(--text-mid); margin-top: 2px; transition: all .2s ease; }}
  .pie-tooltip {{
    position: absolute;
    background: #fff; border: 1px solid var(--border);
    border-radius: 6px; padding: 10px 14px; font-size: 12px;
    box-shadow: var(--shadow-hover); pointer-events: none;
    opacity: 0; transform: translateY(4px); transition: opacity .15s ease, transform .15s ease;
    z-index: 10; white-space: nowrap;
  }}
  .pie-tooltip.show {{ opacity: 1; transform: translateY(0); }}
  .pie-tip-cat {{ font-weight: 600; color: var(--text); margin-bottom: 4px; }}
  .pie-tip-row {{ color: var(--text-mid); }}
  .pie-tip-row b {{ color: var(--accent); font-weight: 500; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 6px 16px; justify-content: center; margin-top: 8px; }}
  .legend-item {{ display: flex; align-items: center; gap: 5px; font-size: 12px; color: var(--text-mid); cursor: pointer; transition: opacity .2s; }}
  .legend-item:hover {{ opacity: .7; }}
  .legend-dot {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}

  /* ---- 分类卡片 ---- */
  .cat-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}
  .cat-card {{
    padding: 16px 10px; border-radius: 10px; text-align: center; cursor: pointer;
    border: 1px solid var(--border);
    transition: all .2s ease;
  }}
  .cat-card:hover {{
    border-color: #d4b89a;
    box-shadow: rgba(61,44,34,0.06) 0px 6px 16px -6px;
  }}
  .cat-card.active {{
    border-color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent);
  }}
  .cat-emoji {{ font-size: 22px; margin-bottom: 4px; }}
  .cat-name {{ font-size: 11px; color: var(--text-mid); }}
  .cat-amount {{ font-size: 16px; font-weight: 500; color: var(--text); margin: 6px 0; font-variant-numeric: tabular-nums; }}
  .cat-bar-bg {{ width: 100%; height: 4px; background: rgba(0,0,0,0.06); border-radius: 2px; margin: 8px 0; overflow: hidden; }}
  .cat-bar {{ height: 100%; border-radius: 2px; transition: width .6s ease; }}
  .cat-pct {{ font-size: 10px; color: var(--text-light); }}

  /* ---- 趋势柱状图 ---- */
  .trend-wrap {{ position: relative; overflow: visible; }}
  .trend-svg {{ width: 100%; height: auto; }}
  .trend-bar {{
    fill: url(#barGrad); cursor: pointer;
    transition: opacity .2s ease, filter .2s ease;
  }}
  .trend-svg:hover .trend-bar {{ opacity: .35; }}
  .trend-svg:hover .trend-bar:hover, .trend-bar.active {{
    opacity: 1 !important;
    filter: brightness(1.1) drop-shadow(0 2px 6px rgba(200,149,108,0.4));
  }}
  .trend-label {{ font-size: 9px; fill: var(--text-light); }}
  .trend-tooltip {{
    position: absolute;
    background: #fff; border: 1px solid var(--border);
    border-radius: 6px; padding: 10px 14px; font-size: 12px;
    box-shadow: var(--shadow-hover); pointer-events: none;
    opacity: 0; transform: translateY(4px); transition: opacity .15s ease, transform .15s ease;
    z-index: 10; white-space: nowrap; text-align: center;
  }}
  .trend-tooltip.show {{ opacity: 1; transform: translateY(0); }}
  .trend-tip-date {{ font-size: 11px; color: var(--text-mid); margin-bottom: 4px; }}
  .trend-tip-amount {{ font-size: 16px; font-weight: 600; color: var(--accent); font-variant-numeric: tabular-nums; }}

  /* ---- 月份导航 ---- */
  .month-nav {{ display: flex; align-items: center; justify-content: center; gap: 16px; margin-bottom: 4px; }}
  .month-arrow {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 32px; height: 32px; border-radius: 6px;
    border: 1px solid var(--border); background: #fff;
    color: var(--heading); font-size: 16px; cursor: pointer;
    transition: all .15s ease; text-decoration: none;
  }}
  .month-arrow:hover {{
    background: var(--accent-light); border-color: #d4b89a;
  }}
  .month-arrow.disabled {{ opacity: .25; pointer-events: none; }}

  /* ---- 环比对比 ---- */
  .cmp-header {{ margin-bottom: 16px; }}
  .cmp-total-row {{ display: flex; justify-content: space-between; align-items: baseline; padding: 0 4px; }}
  .cmp-total-label {{ font-size: 14px; color: var(--text); font-weight: 600; }}
  .cmp-total-diff {{ font-size: 13px; font-weight: 500; font-variant-numeric: tabular-nums; }}
  .cmp-up {{ color: #D92D20; font-weight: 500; }}
  .cmp-down {{ color: #12B76A; font-weight: 500; }}
  .cmp-same {{ color: var(--text-light); }}
  .cmp-table {{ font-size: 12px; }}
  .cmp-table-head {{
    display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 4px;
    padding: 8px 4px; color: var(--text-light); font-size: 11px;
    border-bottom: 1px solid rgba(0,0,0,0.06); margin-bottom: 4px;
  }}
  .cmp-row {{
    display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 4px;
    padding: 8px 4px; align-items: center; border-radius: 10px; transition: background .15s ease;
  }}
  .cmp-row:hover {{ background: #f7f3ee; }}
  .cmp-cat {{ display: flex; align-items: center; gap: 6px; }}
  .cmp-dot {{ width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }}
  .cmp-cur, .cmp-prev {{ font-variant-numeric: tabular-nums; color: var(--text); text-align: left; }}
  .cmp-row span:last-child {{ text-align: left; font-size: 12px; }}

  /* ---- 筛选栏 ---- */
  .filter-row {{
    display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 8px;
  }}
  .filter-row-label {{
    font-size: 11px; color: var(--text-light); white-space: nowrap; margin-right: 4px;
  }}
  .filter-chip {{
    display: inline-flex; align-items: center; gap: 4px;
    padding: 6px 14px; border-radius: 20px; border: 1px solid var(--border);
    background: #fff; color: var(--text-mid); font-size: 12px; font-family: inherit;
    cursor: pointer; transition: all .2s ease; white-space: nowrap;
  }}
  .filter-chip:hover {{
    background: var(--accent-light); border-color: #d4b89a;
  }}
  .filter-chip.active {{
    background: var(--accent-light); border-color: var(--accent);
    color: var(--accent); font-weight: 500;
  }}
  .filter-select {{
    padding: 6px 28px 6px 12px; border-radius: 20px;
    border: 1px solid var(--border); background: #fff;
    color: var(--text-mid); font-size: 12px; font-family: inherit;
    cursor: pointer; transition: all .2s ease;
    -webkit-appearance: none; -moz-appearance: none; appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg width='10' height='6' viewBox='0 0 10 6' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1L5 5L9 1' stroke='%2394a3b8' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: right 10px center;
  }}
  .filter-select:hover {{
    border-color: #d4b89a; background: var(--accent-light);
  }}
  .filter-select option {{ background: #fff; color: var(--text); }}
  .filter-count {{
    font-size: 11px; color: var(--text-light); margin-left: auto;
    white-space: nowrap;
  }}
  .filter-clear {{
    display: none; width: 22px; height: 22px; border-radius: 50%;
    border: 1px solid var(--border); background: #fff;
    color: var(--text-mid); font-size: 12px; cursor: pointer;
    align-items: center; justify-content: center;
    transition: all .2s ease;
  }}
  .filter-clear:hover {{ background: rgba(201,112,112,0.08); border-color: #c97070; color: #c97070; }}
  .filter-clear.show {{ display: inline-flex; }}

  /* ---- 明细 ---- */
  .detail-toggle {{
    display: block; margin: 12px auto 0; padding: 8px 24px;
    border: 1px solid var(--border); border-radius: 20px;
    background: #fff; color: var(--accent); font-size: 12px;
    font-family: inherit; cursor: pointer; transition: all .2s ease;
  }}
  .detail-toggle:hover {{
    background: var(--accent-light); border-color: #d4b89a;
  }}
  .detail-list {{ overflow-y: hidden; transition: max-height .4s ease; }}
  .detail-list.collapsed {{ max-height: 500px; }}

  .detail-item {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 14px 8px; border-bottom: 1px solid rgba(0,0,0,0.04);
    border-radius: 10px; transition: all .25s ease;
  }}
  .detail-item:hover {{ background: #f7f3ee; }}
  .detail-item:last-child {{ border-bottom: none; }}
  .detail-item.hidden {{ display: none; }}
  .detail-item.highlight {{
    animation: fadeInUp .3s ease both;
    background: var(--accent-light);
  }}
  .detail-left {{ display: flex; align-items: center; gap: 14px; flex: 1; min-width: 0; }}
  .detail-emoji {{ font-size: 22px; }}
  .detail-desc {{ font-size: 14px; color: var(--text); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .detail-sub {{ font-size: 11px; color: var(--text-light); margin-top: 3px; }}
  .detail-amount {{
    font-size: 15px; font-weight: 500; color: #a8604c;
    white-space: nowrap; font-variant-numeric: tabular-nums; flex-shrink: 0; margin-left: 12px;
  }}

  /* ---- Footer ---- */
  .footer {{
    text-align: center; margin-top: 32px; padding: 16px;
    color: var(--text-light); font-size: 11px;
    position: relative; z-index: 1;
  }}

  /* ---- 超支提醒 ---- */
  .over-alert {{
    background: #fff; border: 1px solid #e8c8c8;
    border-radius: var(--radius); padding: 14px 20px; margin-bottom: 16px;
    text-align: center; font-size: 13px; color: #c97070;
    position: relative; z-index: 1;
  }}

  /* ---- 回到顶部 ---- */
  .back-top {{
    position: fixed; bottom: 24px; right: 24px;
    width: 40px; height: 40px; border-radius: 50%;
    background: var(--card); border: 1px solid var(--border);
    box-shadow: var(--shadow-card);
    color: var(--text-mid); font-size: 18px;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; z-index: 99;
    opacity: 0; transform: translateY(10px);
    transition: all .3s ease; pointer-events: none;
  }}
  .back-top.show {{ opacity: 1; transform: translateY(0); pointer-events: auto; }}
  .back-top:hover {{ background: var(--accent-light); border-color: #d4b89a; color: var(--accent); }}

  /* ---- 响应式：小屏手机 ---- */
  @media (max-width: 374px) {{
    .cat-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .stats-row {{ flex-wrap: wrap; }}
    .stat-item {{ min-width: 45%; }}
    .total-amount {{ font-size: 32px; }}
    .card {{ padding: 20px 16px; }}
    .header h1 {{ font-size: 20px; }}
    .orb-1 {{ width: 200px; height: 200px; }}
    .orb-2 {{ width: 180px; height: 180px; }}
  }}
  @media (min-width: 420px) {{
    body {{ padding: 28px 20px 56px; }}
    .card {{ padding: 28px 24px; margin-bottom: 18px; }}
    .header {{ padding: 36px 0 12px; }}
    .header h1 {{ font-size: 26px; }}
    .total-amount {{ font-size: 44px; }}
    .pie-svg {{ width: 180px; height: 180px; }}
    .pie-center-abs {{ width: 88px; height: 88px; }}
  }}
  @media (min-width: 640px) {{
    body {{ max-width: 560px; padding: 40px 32px 72px; }}
    .card {{ padding: 32px 28px; margin-bottom: 20px; }}
    .header h1 {{ font-size: 28px; }}
    .cat-grid {{ grid-template-columns: repeat(3, 1fr); gap: 12px; }}
    .cat-card {{ padding: 18px 12px; }}
    .total-amount {{ font-size: 48px; }}
    .overview-top {{ gap: 32px; }}
    .ring {{ width: 110px; height: 110px; }}
    .ring-pct {{ font-size: 22px; }}
    .stat-item {{ padding: 16px 10px; }}
    .stat-num {{ font-size: 22px; }}
    .pie-svg {{ width: 200px; height: 200px; }}
    .pie-center-abs {{ width: 100px; height: 100px; }}
    .pie-center-num {{ font-size: 20px; }}
    .detail-item {{ padding: 16px 4px; }}
    .detail-amount {{ font-size: 16px; }}
  }}
  @media (min-width: 1024px) {{
    body {{ max-width: 600px; }}
    .card {{ padding: 36px 32px; }}
    .cat-grid {{ grid-template-columns: repeat(4, 1fr); }}
  }}
</style>
</head>
<body>

<div class="orb orb-1"></div>
<div class="orb orb-2"></div>

<header class="header">
  <div class="month-nav">
    <a href="{'' if not nav_prev else nav_prev_file}" class="month-arrow {'disabled' if not nav_prev else ''}" {'title="上一月：' + nav_prev_display + '"' if nav_prev else ''}>‹</a>
    <h1>{month_display}</h1>
    <a href="{'' if not nav_next else nav_next_file}" class="month-arrow {'disabled' if not nav_next else ''}" {'title="下一月：' + nav_next_display + '"' if nav_next else ''}>›</a>
  </div>
  <div class="subtitle">{summary}</div>
</header>

{'<div class="over-alert">本月已超支 ¥' + f'{abs(budget_remain):.2f}' + '，下个月要加油控制哦～</div>' if over_budget else ''}

<section class="card overview">
  <div class="card-label">本月总览</div>
  <div class="overview-top">
    <div class="overview-left">
      <div class="total-amount">¥{total:.2f} <small>/ ¥{budget:.0f}</small></div>
      <div class="budget-summary">
        <span>剩余 <strong>{'-¥' + f'{abs(budget_remain):.0f}' if over_budget else '¥' + f'{budget_remain:.0f}'}</strong></span>
        <span>日均 <strong>¥{avg_daily:.0f}</strong></span>
      </div>
    </div>
    <div class="ring">
      <svg viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="42" fill="none" stroke="#e8e0d6" stroke-width="4.5"/>
        <circle cx="50" cy="50" r="42" fill="none" stroke="{ring_color}" stroke-width="4.5"
                stroke-dasharray="{2 * 3.14159 * 42 * ring_pct / 100:.1f} {2 * 3.14159 * 42:.1f}"
                stroke-linecap="round"/>
      </svg>
      <div class="ring-text">
        <div class="ring-pct">{budget_pct:.0f}%</div>
        <div class="ring-label">已使用</div>
      </div>
      <div class="ring-info">
        <div class="ring-info-line {'warn' if over_budget else ''}">{'-¥' + f'{abs(budget_remain):.0f}' if over_budget else '¥' + f'{budget_remain:.0f}'}</div>
        <div class="ring-info-line">¥{avg_daily:.0f}/天</div>
      </div>
    </div>
  </div>
  <div class="budget-bar-wrap">
    <div class="budget-bar-head">
      <span class="budget-bar-label">预算进度</span>
      <span class="budget-bar-pct">{budget_pct:.0f}%</span>
    </div>
    <div class="budget-bar"><div class="budget-bar-fill" style="width:{min(budget_pct, 100):.1f}%"></div></div>
  </div>
  <div class="stats-row">
    <div class="stat-item"><div class="stat-num">{count}</div><div class="stat-desc">记账笔数</div><div class="stat-tip">本月共记录 {count} 笔消费</div></div>
    <div class="stat-item"><div class="stat-num">¥{max_single['amount']:.0f}</div><div class="stat-desc">最高单笔</div><div class="stat-tip">最高消费: {esc(max_single.get('description',''))} ({max_single['category']})</div></div>
    <div class="stat-item"><div class="stat-num">¥{by_day[max_day_date]:.0f}</div><div class="stat-desc">最高消费</div><div class="stat-tip">{max_day_date[5:7]}月{max_day_date[8:]}号消费 ¥{by_day[max_day_date]:.2f}，花费最多的一天</div></div>
  </div>
</section>

{compare_html}

<section class="card card-overflow">
  <div class="card-label">支出分布</div>
  <div class="chart-section">
    <div class="pie-wrap">
      <svg class="pie-svg" viewBox="0 0 160 160" overflow="visible">{pie_svg}</svg>
      <div class="pie-center-abs">
        <div class="pie-center-num" id="pieNum">¥{total:.0f}</div>
        <div class="pie-center-label" id="pieLabel">总支出</div>
      </div>
    </div>
    <div class="legend">
      {''.join(f'<div class="legend-item" data-cat="{esc(c)}"><span class="legend-dot" style="background:{CAT_CONFIG.get(c, CAT_CONFIG["其他"])["color"]}"></span>{esc(c)}</div>' for c, _ in sorted_cats)}
    </div>
    <div class="pie-tooltip" id="pieTip">
      <div class="pie-tip-cat" id="pieTipCat"></div>
      <div class="pie-tip-row">金额：<b id="pieTipAmt"></b></div>
      <div class="pie-tip-row">占比：<b id="pieTipPct"></b></div>
    </div>
  </div>
</section>

<section class="card">
  <div class="card-label">分类详情</div>
  <div class="cat-grid">{cat_cards}</div>
</section>

<section class="card">
  <div class="card-label">每日趋势</div>
  {trend_svg}
</section>

<section class="card" id="detailSection">
  <div class="card-label">
    消费明细
    <span class="filter-count" id="filterCount"></span>
    <button class="filter-clear" id="filterClear" title="清除筛选">&times;</button>
  </div>
  <div class="filter-row">
    <span class="filter-row-label">分类</span>
    <button class="filter-chip active" data-filter="category" data-value="">全部</button>
    {''.join(f'<button class="filter-chip" data-filter="category" data-value="{esc(c)}">{CAT_CONFIG.get(c, CAT_CONFIG["其他"])["emoji"]} {esc(c)}</button>' for c, _ in sorted_cats)}
  </div>
  <div class="filter-row">
    <span class="filter-row-label">日期</span>
    <select class="filter-select" id="dateSelect" data-filter="date">
      <option value="">全部日期</option>
      {''.join(f'<option value="{d}">{int(d[5:7])}月{int(d[8:])}日</option>' for d in day_dates)}
    </select>
  </div>
  <div class="detail-list{' collapsed' if count > 5 else ''}" id="detailList">
    {rows_html}
  </div>
  <div class="detail-empty" id="detailEmpty" style="display:none;text-align:center;padding:24px 0;color:var(--text-light);font-size:13px">无匹配的消费记录</div>
  {'<button class="detail-toggle" id="detailToggle">展开全部（' + str(count) + '笔）</button>' if count > 5 else ''}
</section>

<footer class="footer">
  <div>生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
</footer>

<div class="back-top" id="backTop" title="回到顶部">&#8593;</div>

<script>
/* ---- 入场动画 ---- */
(function(){{
  /* 卡片交错淡入 */
  const cards=document.querySelectorAll('.card,.over-alert');
  cards.forEach(function(c,i){{
    c.style.opacity='0';c.style.transform='translateY(18px)';
    c.style.transition='opacity .5s ease,transform .5s ease';
    setTimeout(function(){{c.style.opacity='1';c.style.transform='translateY(0)';}},80+i*90);
  }});
  /* 预算条动画 */
  const bar=document.querySelector('.budget-bar-fill');
  if(bar){{
    const w=bar.style.width;bar.style.width='0%';
    setTimeout(function(){{bar.style.width=w;}},400);
  }}
  /* 总金额 count-up */
  const ta=document.querySelector('.total-amount');
  if(ta){{
    const full=ta.innerHTML;
    const match=full.match(/¥([\\d,.]+)/);
    if(match){{
      const target=parseFloat(match[1].replace(',',''));
      const small=full.replace(match[0],'');
      const dur=800;let start=null;
      function step(ts){{
        if(!start)start=ts;
        const p=Math.min((ts-start)/dur,1);
        const ease=1-Math.pow(1-p,3);
        const v=target*ease;
        ta.innerHTML='¥'+v.toFixed(2)+' <small>/ ¥{budget:.0f}</small>';
        if(p<1)requestAnimationFrame(step);
        else ta.innerHTML=full;
      }}
      setTimeout(function(){{requestAnimationFrame(step);}},300);
    }}
  }}
}})();
/* 回到顶部 */
(function(){{
  const btn=document.getElementById('backTop');
  if(!btn) return;
  window.addEventListener('scroll',function(){{
    btn.classList.toggle('show',window.scrollY>400);
  }});
  btn.addEventListener('click',function(){{
    window.scrollTo({{top:0,behavior:'smooth'}});
  }});
}})();
</script>
<script>
(function(){{
  const tip=document.getElementById('pieTip');
  const tipCat=document.getElementById('pieTipCat');
  const tipAmt=document.getElementById('pieTipAmt');
  const tipPct=document.getElementById('pieTipPct');
  const centerNum=document.getElementById('pieNum');
  const centerLabel=document.getElementById('pieLabel');
  const defaultNum=centerNum.textContent;
  const defaultLabel=centerLabel.textContent;
  const wrap=tip.parentElement;
  const center=document.querySelector('.pie-center-abs');

  /* 鼠标进入饼图中心 → 恢复默认 */
  if(center){{
    center.addEventListener('mouseenter',function(){{
      tip.classList.remove('show');
      centerNum.textContent=defaultNum;
      centerLabel.textContent=defaultLabel;
    }});
  }}

  document.querySelectorAll('.pie-seg').forEach(function(seg){{
    seg.addEventListener('mouseenter',function(){{
      tipCat.textContent=seg.dataset.cat;
      tipAmt.textContent='¥'+seg.dataset.amount;
      tipPct.textContent=seg.dataset.pct+'%';
      tip.classList.add('show');
      centerNum.textContent='¥'+seg.dataset.amount;
      centerLabel.textContent=seg.dataset.cat;
    }});
    seg.addEventListener('mousemove',function(e){{
      const r=wrap.getBoundingClientRect();
      let x=e.clientX-r.left+14;
      let y=e.clientY-r.top-50;
      if(x+140>r.width) x=e.clientX-r.left-150;
      if(y<0) y=e.clientY-r.top+20;
      tip.style.left=x+'px';
      tip.style.top=y+'px';
    }});
    seg.addEventListener('mouseleave',function(){{
      tip.classList.remove('show');
      centerNum.textContent=defaultNum;
      centerLabel.textContent=defaultLabel;
    }});
    seg.addEventListener('touchstart',function(e){{
      e.preventDefault();
      const active=document.querySelector('.pie-seg.active');
      if(active&&active!==seg) active.classList.remove('active');
      seg.classList.toggle('active');
      if(seg.classList.contains('active')){{
        tipCat.textContent=seg.dataset.cat;
        tipAmt.textContent='¥'+seg.dataset.amount;
        tipPct.textContent=seg.dataset.pct+'%';
        centerNum.textContent='¥'+seg.dataset.amount;
        centerLabel.textContent=seg.dataset.cat;
        const r=wrap.getBoundingClientRect();
        const rect=seg.getBoundingClientRect();
        let tx=rect.left-r.left+rect.width/2-60;
        let ty=rect.top-r.top-70;
        if(ty<0) ty=rect.top-r.top+rect.height+10;
        tip.style.left=tx+'px';
        tip.style.top=ty+'px';
        tip.classList.add('show');
      }}else{{
        tip.classList.remove('show');
        centerNum.textContent=defaultNum;
        centerLabel.textContent=defaultLabel;
      }}
    }},{{passive:false}});
    seg.addEventListener('click',function(){{
      if(typeof window._filterDetail==='function'){{
        window._filterDetail('category',seg.dataset.cat);
      }}
    }});
  }});
  document.addEventListener('click',function(e){{
    if(!e.target.classList.contains('pie-seg')){{
      const a=document.querySelector('.pie-seg.active');
      if(a){{a.classList.remove('active');tip.classList.remove('show');centerNum.textContent=defaultNum;centerLabel.textContent=defaultLabel;}}
    }}
  }});
  /* 图例点击筛选 */
  document.querySelectorAll('.legend-item').forEach(function(item){{
    item.addEventListener('click',function(){{
      if(typeof window._filterDetail==='function'){{
        window._filterDetail('category',item.getAttribute('data-cat'));
      }}
    }});
  }});
}})();

(function(){{
  const tip=document.getElementById('trendTip');
  const tipDate=document.getElementById('trendTipDate');
  const tipAmt=document.getElementById('trendTipAmt');
  if(!tip) return;
  const wrap=tip.parentElement;
  function showTip(bar){{
    const d=bar.dataset.date;
    tipDate.textContent=d.slice(5).replace('-','月')+'日';
    tipAmt.textContent='¥'+bar.dataset.amount;
    const r=wrap.getBoundingClientRect();
    const rect=bar.getBoundingClientRect();
    const x=rect.left-r.left+rect.width/2;
    const y=rect.top-r.top-10;
    tip.style.left=x+'px';
    tip.style.top=y+'px';
    tip.style.transform='translate(-50%,-100%)';
    tip.classList.add('show');
  }}
  document.querySelectorAll('.trend-bar').forEach(function(bar){{
    bar.addEventListener('mouseenter',function(){{ showTip(bar); }});
    bar.addEventListener('mouseleave',function(){{ tip.classList.remove('show'); tip.style.transform=''; }});
    bar.addEventListener('click',function(){{
      if(typeof window._filterDetail==='function'){{
        window._filterDetail('date',bar.dataset.date);
      }}
    }});
  }});
  document.addEventListener('click',function(e){{
    if(!e.target.classList.contains('trend-bar')){{
      tip.classList.remove('show'); tip.style.transform='';
    }}
  }});
}})();

(function(){{
  const btn=document.getElementById('detailToggle');
  const list=document.getElementById('detailList');
  if(!btn||!list) return;
  const total={count};
  btn.addEventListener('click',function(){{
    if(list.classList.contains('collapsed')){{
      list.classList.remove('collapsed');
      btn.textContent='收起明细';
    }}else{{
      list.classList.add('collapsed');
      btn.textContent='展开全部（'+total+'笔）';
      list.scrollIntoView({{behavior:'smooth',block:'start'}});
    }}
  }});
}})();

/* ---- 筛选功能（分类 AND 日期交叉筛选） ---- */
(function(){{
  const items=document.querySelectorAll('.detail-item');
  const filterCount=document.getElementById('filterCount');
  const filterClear=document.getElementById('filterClear');
  const detailSection=document.getElementById('detailSection');
  const detailList=document.getElementById('detailList');
  const detailEmpty=document.getElementById('detailEmpty');
  const toggleBtn=document.getElementById('detailToggle');
  const catCards=document.querySelectorAll('.cat-card');
  const chips=document.querySelectorAll('.filter-chip');
  const dateSelect=document.getElementById('dateSelect');
  const totalCount=items.length;
  let catFilter='';
  let dateFilter='';

  function applyFilter(){{
    let shown=0;
    items.forEach(function(item){{
      const cat=item.getAttribute('data-category');
      const dt=item.getAttribute('data-date');
      const catOk=!catFilter||cat===catFilter;
      const dtOk=!dateFilter||dt===dateFilter;
      if(catOk&&dtOk){{
        item.classList.remove('hidden');
        item.classList.add('highlight');
        shown++;
        setTimeout(function(){{item.classList.remove('highlight');}},500);
      }}else{{
        item.classList.add('hidden');
        item.classList.remove('highlight');
      }}
    }});
    /* 空状态 */
    if(detailEmpty){{
      detailEmpty.style.display=(shown===0&&!catFilter&&!dateFilter)?'none':(shown===0?'block':'none');
    }}
    /* 更新计数 */
    if(filterCount){{
      if(!catFilter&&!dateFilter){{
        filterCount.textContent='';
      }}else{{
        filterCount.textContent=shown+' / '+totalCount+' 笔';
      }}
    }}
    /* 清除按钮 */
    if(filterClear){{
      if(!catFilter&&!dateFilter) filterClear.classList.remove('show');
      else filterClear.classList.add('show');
    }}
    /* 分类 chips 高亮 */
    chips.forEach(function(c){{
      const v=c.getAttribute('data-value');
      if(v===catFilter) c.classList.add('active');
      else c.classList.remove('active');
    }});
    /* 分类卡片高亮 */
    catCards.forEach(function(card){{
      if(catFilter&&card.getAttribute('data-cat')===catFilter) card.classList.add('active');
      else card.classList.remove('active');
    }});
    /* 日期下拉框同步 */
    if(dateSelect){{
      dateSelect.value=dateFilter||'';
    }}
  }}

  function clearAll(){{
    catFilter='';
    dateFilter='';
    applyFilter();
  }}

  /* 点击分类 chip */
  chips.forEach(function(chip){{
    chip.addEventListener('click',function(){{
      const v=chip.getAttribute('data-value');
      catFilter=(catFilter===v)?'':v;
      applyFilter();
    }});
  }});

  /* 日期下拉框 */
  if(dateSelect){{
    dateSelect.addEventListener('change',function(){{
      dateFilter=dateSelect.value;
      applyFilter();
    }});
  }}

  /* 清除筛选 */
  if(filterClear){{
    filterClear.addEventListener('click',function(e){{
      e.stopPropagation();
      clearAll();
    }});
  }}

  /* 点击分类卡片 → 重置日期 + 设置分类筛选 */
  catCards.forEach(function(card){{
    card.addEventListener('click',function(){{
      const cat=card.getAttribute('data-cat');
      dateFilter='';
      catFilter=(catFilter===cat)?'':cat;
      applyFilter();
      /* 展开明细 */
      if(detailList&&detailList.classList.contains('collapsed')){{
        detailList.classList.remove('collapsed');
        if(toggleBtn) toggleBtn.textContent='收起明细';
      }}
      /* 滚动到明细区 */
      if(detailSection){{
        setTimeout(function(){{
          detailSection.scrollIntoView({{behavior:'smooth',block:'start'}});
        }},100);
      }}
    }});
  }});

  /* 趋势柱子点击 → 重置分类 + 设置日期筛选 */
  window._filterDetail=function(type,value){{
    if(type==='date'){{
      catFilter='';
      dateFilter=(dateFilter===value)?'':value;
    }}else if(type==='category'){{
      dateFilter='';
      catFilter=(catFilter===value)?'':value;
    }}
    applyFilter();
    /* 展开明细 */
    if(detailList&&detailList.classList.contains('collapsed')){{
      detailList.classList.remove('collapsed');
      if(toggleBtn) toggleBtn.textContent='收起明细';
    }}
    if(detailSection){{
      setTimeout(function(){{
        detailSection.scrollIntoView({{behavior:'smooth',block:'start'}});
      }},100);
    }}
  }};
}})();
</script>

</body></html>"""
    
    if not output_file:
        os.makedirs(DATA_DIR, exist_ok=True)
        output_file = os.path.join(DATA_DIR, f"report-{latest_month}.html")

    if not force and os.path.exists(output_file):
        print(f"报表已存在: {output_file}（使用 --force 覆盖）")
        return output_file

    with open(output_file, 'w') as f:
        f.write(html)
    print(f"报表已生成: {output_file}")

    if not _skip_adjacent:
        for m in all_months:
            if m == latest_month:
                continue
            adj_output = os.path.join(DATA_DIR, f"report-{m}.html")
            if force or not os.path.exists(adj_output):
                generate_report(expenses_file, config_file, adj_output, m, _skip_adjacent=True, force=force)

    return output_file

def export_csv(expenses_file, config_file, output_file=None, month=None):
    """导出当月支出为CSV"""
    import csv

    expenses = load_data(expenses_file)
    
    if not expenses:
        print("暂无数据")
        return
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    budget = config.get('monthly_budget', 2000)
    
    latest_month, month_expenses = _get_month_data(expenses, month)
    
    if not month_expenses:
        print(f"{latest_month} 没有数据")
        return
    
    by_cat = defaultdict(float)
    for e in month_expenses:
        by_cat[e['category']] += e['amount']
    
    if not output_file:
        os.makedirs(DATA_DIR, exist_ok=True)
        output_file = os.path.join(DATA_DIR, f"report-{latest_month}.csv")
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['日期', '分类', '描述', '金额(元)'])
        for e in month_expenses:
            writer.writerow([e['date'], e['category'], e.get('description', ''), f"{e['amount']:.2f}"])
        writer.writerow([])
        writer.writerow(['--- 分类小计 ---', '', '', ''])
        for cat, amount in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
            cfg = CAT_CONFIG.get(cat, CAT_CONFIG['其他'])
            writer.writerow(['', cat, '', f"{amount:.2f}"])
        writer.writerow([])
        total = sum(e['amount'] for e in month_expenses)
        writer.writerow(['💰 合计', f"{len(month_expenses)}笔", f'预算 ¥{budget}', f"{total:.2f}"])
        writer.writerow([f'📊 预算剩余', '', '', f"{budget - total:.2f}"])
    
    print(f"CSV已导出: {output_file}")
    return output_file

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='支出报表生成/导出')
    parser.add_argument('--file', default='data/expenses.json', help='数据文件路径')
    parser.add_argument('--config', default='data/config.json', help='配置文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--month', help='指定月份 YYYY-MM（默认最新月）')
    parser.add_argument('--csv', action='store_true', help='导出CSV格式')
    parser.add_argument('--force', action='store_true', help='强制重新生成已有报表')
    args = parser.parse_args()
    
    if args.csv:
        export_csv(args.file, args.config, args.output, args.month)
    else:
        generate_report(args.file, args.config, args.output, args.month, force=args.force)
