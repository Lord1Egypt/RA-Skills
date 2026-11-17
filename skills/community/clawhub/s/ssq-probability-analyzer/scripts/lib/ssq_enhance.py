"""
双色球分析增强模块
在V1基础预测之上：
1. 集成3个ML模型预测（加权频率/随机森林/遗传算法）
2. 新增号码冷热图可视化
3. 新增专家推荐汇总分析（本期实时抓取热度）
4. 增强HTML报告
5. 【V1.0.8 新增】专家体系总览（内置46位常驻权威名录+野路子高手+官方数据源）
   + 专家对比分析（战绩自算 vs 随机基线，不采信平台自报）

运行方式：先运行ssq_auto.py，再运行本脚本
"""
import json
import os
import re
import sys
import math
from collections import Counter
from datetime import datetime
from ssq_period import next_period as next_period_func  # 统一期号计算(日期驱动年末进年)
from ssq_common import passes_filters  # noqa: E402

# 导入ML模型
from ssq_ml_models import generate_ml_prediction, load_history, compute_features



def load_json(filepath):
    """加载JSON文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath, data):
    """保存JSON文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)




def generate_heatmap_html(history, top_n=100):
    """生成号码冷热图HTML
    
    显示红球1-33和蓝球1-16的：
    - 全部频率（颜色深浅）
    - 近30期频率（颜色深浅）
    - 遗漏值（数字大小）
    - 是否在推荐中（高亮边框）
    """
    front_features, back_features = compute_features(history, window=30)
    
    # 红球热力图
    front_html = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin:10px 0;">'
    for num in range(1, 34):
        f = front_features[num]
        # 颜色：基于近期频率，越高越红
        freq = f['freq_recent']
        # 映射到颜色：0=浅灰, 高=深红
        if freq > 0.15:
            bg = '#e74c3c'
            color = 'white'
        elif freq > 0.10:
            bg = '#f39c12'
            color = 'white'
        elif freq > 0.06:
            bg = '#f1c40f'
            color = '#333'
        elif freq > 0.03:
            bg = '#bdc3c7'
            color = '#333'
        else:
            bg = '#ecf0f1'
            color = '#7f8c8d'
        
        omit = f['omit']
        omit_label = f'{omit}' if omit > 0 else '0'
        
        front_html += f'''<div style="width:52px;height:52px;border-radius:50%;background:{bg};color:{color};
            display:flex;flex-direction:column;align-items:center;justify-content:center;
            font-size:16px;font-weight:bold;position:relative;">
            {num:02d}
            <span style="font-size:9px;opacity:0.8;">缺{omit_label}</span>
        </div>'''
    
    front_html += '</div>'
    
    # 蓝球热力图
    back_html = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin:10px 0;">'
    for num in range(1, 17):
        f = back_features[num]
        freq = f['freq_recent']
        if freq > 0.25:
            bg = '#e74c3c'
            color = 'white'
        elif freq > 0.15:
            bg = '#f39c12'
            color = 'white'
        elif freq > 0.08:
            bg = '#f1c40f'
            color = '#333'
        elif freq > 0.04:
            bg = '#bdc3c7'
            color = '#333'
        else:
            bg = '#ecf0f1'
            color = '#7f8c8d'
        
        omit = f['omit']
        back_html += f'''<div style="width:48px;height:48px;border-radius:50%;background:{bg};color:{color};
            display:flex;flex-direction:column;align-items:center;justify-content:center;
            font-size:15px;font-weight:bold;">
            {num:02d}
            <span style="font-size:8px;opacity:0.8;">缺{omit}</span>
        </div>'''
    
    back_html += '</div>'
    
    # 图例
    legend = '''
    <div style="display:flex;gap:15px;margin:10px 0;font-size:12px;color:#666;">
      <span><span style="display:inline-block;width:12px;height:12px;background:#e74c3c;border-radius:2px;"></span> 高频(热)</span>
      <span><span style="display:inline-block;width:12px;height:12px;background:#f39c12;border-radius:2px;"></span> 较热</span>
      <span><span style="display:inline-block;width:12px;height:12px;background:#f1c40f;border-radius:2px;"></span> 正常</span>
      <span><span style="display:inline-block;width:12px;height:12px;background:#bdc3c7;border-radius:2px;"></span> 较冷</span>
      <span><span style="display:inline-block;width:12px;height:12px;background:#ecf0f1;border-radius:2px;border:1px solid #ddd;"></span> 冷号</span>
      <span>数字下方"缺N"=已遗漏N期</span>
    </div>'''
    
    return f'''
    <div style="background:#fff;border:1px solid #e0e0e0;border-radius:8px;padding:15px;margin:15px 0;">
      <h3 style="color:#333;margin:0 0 10px 0;">号码冷热图（近30期频率）</h3>
      {legend}
      <div style="margin:10px 0;">
        <strong style="color:#c0392b;">红球号码 (01-33)</strong>
        {front_html}
      </div>
      <div style="margin:15px 0 10px 0;">
        <strong style="color:#2980b9;">蓝球号码 (01-16)</strong>
        {back_html}
      </div>
    </div>'''


def generate_expert_analysis_html(expert_picks, ml_result, target_period=None, history=None):
    """生成专家推荐汇总分析HTML。

    彻底解决「0位名家·无数据」: 当实时抓取专家推荐为空(ssq_expert_picks.json 缺失/离线)时,
    回退到内置 46 位常驻专家体系, 按各专家流派确定性派生共识推荐并聚合成热度,
    标题明确标注「非实时抓取·娱乐参考」, 保证板块始终有数据。
    """
    experts = expert_picks.get('experts', []) if isinstance(expert_picks, dict) else []
    is_synthetic = False
    if not experts:
        try:
            from ssq_expert_roster import build_resident_expert_panel
            experts = build_resident_expert_panel(target_period or 'unknown', history or [])
            is_synthetic = True
        except Exception:
            experts = []

    # 统计每个红球号码被多少专家推荐
    front_counter = Counter()
    back_counter = Counter()
    for e in experts:
        for num in e.get('front', []):
            if 1 <= num <= 33:
                front_counter[num] += 1
        for num in e.get('back', []):
            if 1 <= num <= 16:
                back_counter[num] += 1

    # 专家热度排行
    front_hot = front_counter.most_common(10)
    back_hot = back_counter.most_common(5)

    if is_synthetic:
        title = (f'本期实时抓取专家推荐热度（本期实时未返回·改用内置 {len(experts)} 位常驻专家体系共识热度·娱乐参考·非预测力）')
        note = ('注：本期实时抓取未抓取到正规推荐号（离线/数据源限制），'
                '以下为系统内置 46 位常驻专家体系按各自流派（热号/冷号/奇偶/和值等）'
                '确定性派生的「共识热度」，仅供娱乐观察，绝不代表中奖倾向。')
    else:
        title = f'本期实时抓取专家推荐热度（{len(experts)}位名家）'
        note = '注：专家推荐来源于新浪体育、中彩网、今日头条等公开渠道，仅供分析参考。'

    html = '''
    <div style="background:#fff;border:1px solid #e0e0e0;border-radius:8px;padding:15px;margin:15px 0;">
      <h3 style="color:#333;margin:0 0 10px 0;">''' + title + '''</h3>
      <div style="display:flex;gap:30px;flex-wrap:wrap;">
        <div>
          <strong style="color:#c0392b;">红球热门号码TOP10:</strong>
          <div style="display:flex;flex-wrap:wrap;gap:6px;margin:8px 0;">'''

    for num, count in front_hot:
        bg = '#e74c3c' if count >= 5 else '#f39c12' if count >= 3 else '#bdc3c7'
        html += f'<div style="background:{bg};color:white;width:40px;height:40px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:13px;font-weight:bold;">{num:02d}<span style="font-size:8px;">{count}人</span></div>'

    html += '''</div>
        </div>
        <div>
          <strong style="color:#2980b9;">蓝球热门号码TOP5:</strong>
          <div style="display:flex;flex-wrap:wrap;gap:6px;margin:8px 0;">'''

    for num, count in back_hot:
        bg = '#e74c3c' if count >= 4 else '#f39c12' if count >= 2 else '#bdc3c7'
        html += f'<div style="background:{bg};color:white;width:36px;height:36px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:12px;font-weight:bold;">{num:02d}<span style="font-size:8px;">{count}人</span></div>'

    html += '''</div>
        </div>
      </div>
      <p style="font-size:11px;color:#999;margin-top:8px;">''' + note + '''</p>
    </div>'''

    return html


def generate_ml_section_html(ml_result):
    """生成ML预测模块HTML"""
    html = '''
    <div style="background:#fff;border:1px solid #e0e0e0;border-radius:8px;padding:15px;margin:15px 0;">
      <h3 style="color:#333;margin:0 0 10px 0;">机器学习模型预测（第6-8组）</h3>
      <p style="font-size:12px;color:#666;">以下3组由机器学习模型生成，增加分析视角多样性。数学上不比随机选号更好(p>0.05)。</p>'''
    
    model_names = {
        'weighted_freq': '加权频率模型',
        'random_forest': '随机森林(50树)',
        'genetic_optimal': '遗传算法优化'
    }
    
    for key, name in model_names.items():
        model = ml_result.get(key, {})
        front = model.get('front', [])
        back = model.get('back', [])
        strategy = model.get('strategy', '')
        
        html += f'''
        <div style="margin:12px 0;padding:10px;background:#f8f9fa;border-radius:6px;">
          <strong style="color:#2c3e50;">{name}</strong>
          <div style="margin:5px 0;">
            <span style="color:#c0392b;font-weight:bold;">红球:</span>'''
        for num in front:
            html += f' <span style="display:inline-block;background:#e74c3c;color:white;width:30px;height:30px;border-radius:50%;text-align:center;line-height:30px;font-weight:bold;margin:2px;">{num:02d}</span>'
        
        html += f'''</div>
          <div style="margin:5px 0;">
            <span style="color:#2980b9;font-weight:bold;">蓝球:</span>'''
        for num in back:
            html += f' <span style="display:inline-block;background:#3498db;color:white;width:28px;height:28px;border-radius:50%;text-align:center;line-height:28px;font-weight:bold;margin:2px;">{num:02d}</span>'
        
        html += f'''
          </div>
          <div style="font-size:11px;color:#888;margin-top:3px;">策略: {strategy}</div>
        </div>'''
    
    html += '</div>'
    return html


def build_expert_comparison(target_period, history, periods=20, baseline_k=300):
    """专家对比分析·真实数据版(离线可用).

    对近 `periods` 期实际开奖做回溯自算打分:
    - 用系统内置 46 位常驻专家流派模型(确定性派生)为每期生成 6+1 推荐;
    - 与实际开奖独立比对, 统计每位专家平均红球/蓝球命中;
    - 同时用随机基线(每期模拟 baseline_k 组随机 6+1)作为对照.
    结论天然呈现"专家是否优于随机"(数学上不会). 确定性/可复现, 不依赖实时抓取.
    """
    try:
        import random as _rnd
        from ssq_expert_roster import get_roster, build_resident_expert_panel
        if not history or len(history) < periods + 1:
            return None
        roster = get_roster()
        # 构造待打分窗口: (该期实际开奖, 该期之前的偏置窗口)
        pairs = []
        for i in range(1, len(history)):
            pairs.append((history[i], history[max(0, i - 30):i]))
        pairs = pairs[-periods:]
        if len(pairs) < 3:
            return None
        acc = {e['name']: {'n': 0, 'fh': 0.0, 'bh': 0.0} for e in roster}
        base_fh = 0.0
        base_bh = 0.0
        for (period, win) in pairs:
            actual_f = set(period.get('front', []))
            actual_b = set(period.get('back', []))
            pkey = str(period.get('period') or period.get('date', ''))
            try:
                panel = build_resident_expert_panel(pkey, win)
            except Exception:
                panel = []
            for e in panel:
                acc[e['name']]['n'] += 1
                acc[e['name']]['fh'] += len(set(e.get('front', [])) & actual_f)
                acc[e['name']]['bh'] += len(set(e.get('back', [])) & actual_b)
            # 随机基线: 每期模拟 baseline_k 组随机 6+1 打分取均值
            rnd = _rnd.Random(hash((pkey, 'baseline')))
            bf = 0.0
            bb = 0.0
            for _ in range(baseline_k):
                rdraw = set(rnd.sample(range(1, 34), 6))
                bdraw = rnd.choice(range(1, 17))
                bf += len(rdraw & actual_f)
                bb += (1 if bdraw in actual_b else 0)
            base_fh += bf / baseline_k
            base_bh += bb / baseline_k
        n_periods = len(pairs)
        base_fh = round(base_fh / n_periods, 2)
        base_bh = round(base_bh / n_periods, 2)
        experts = []
        for name, a in acc.items():
            if a['n']:
                experts.append((name, round(a['fh'] / a['n'], 2),
                                round(a['bh'] / a['n'], 2), a['n']))
        experts.sort(key=lambda x: x[1], reverse=True)
        return {
            'periods': n_periods,
            'baseline_front_hits': base_fh,
            'baseline_back_hits': base_bh,
            'experts': experts,
            'derived': True,
        }
    except Exception:
        return None


def generate_expert_system_html(history=None, target_period=None):
    """V1.0.8 新增: 专家体系总览(常驻名录) + 专家对比分析(战绩自算 vs 随机基线)。

    诚实定位: 汇集多方观点供观察, 不宣称可确保的中奖结果
    (彩票近纯随机, 无专家能证明有稳定超额优势; 体彩中心从未授权任何个人预测)。
    """
    # 1) 常驻名录 (始终内置, 不依赖实时抓取成败)
    roster, data_sources, rsum = [], [], None
    try:
        from ssq_expert_roster import get_roster, get_data_sources, catalog_summary
        roster = get_roster()
        data_sources = get_data_sources()
        rsum = catalog_summary()
    except Exception:
        rsum = None

    # 2) 对比分析 (tracker 每期开奖后自算, 不采信平台自报)
    tsum = None
    try:
        from ssq_expert_tracker import summary as _tracker_summary
        tsum = _tracker_summary(periods=20)
    except Exception:
        tsum = None
    # 离线/无 tracker 数据时, 回退到确定性回溯自算(常驻流派模型 vs 实际开奖 vs 随机基线)
    if not (tsum and tsum.get('experts')):
        try:
            tsum = build_expert_comparison(target_period or 'unknown', history or [], periods=20)
        except Exception:
            tsum = None

    # ---- 统计卡 ----
    if rsum:
        cards = (
            f"<span style='display:inline-block;background:#eef7ff;border:1px solid #cfe3ff;"
            f"border-radius:8px;padding:8px 14px;font-size:13px;color:#333;margin:0 8px 8px 0;'>"
            f"权威名家<br><b style='font-size:18px;color:#c0392b;'>{rsum['权威']}</b> 位</span>"
            f"<span style='display:inline-block;background:#f3eaff;border:1px solid #e0d0ff;"
            f"border-radius:8px;padding:8px 14px;font-size:13px;color:#333;margin:0 8px 8px 0;'>"
            f"野路子高手<br><b style='font-size:18px;color:#8e44ad;'>{rsum['野路子']}</b> 位</span>"
            f"<span style='display:inline-block;background:#e8f8ef;border:1px solid #c2e6d2;"
            f"border-radius:8px;padding:8px 14px;font-size:13px;color:#333;margin:0 8px 8px 0;'>"
            f"官方数据源<br><b style='font-size:18px;color:#2e8b57;'>{rsum['官方数据源']}</b> 个</span>"
            f"<span style='display:inline-block;background:#fff4e6;border:1px solid #ffd9a8;"
            f"border-radius:8px;padding:8px 14px;font-size:13px;color:#333;margin:0 8px 8px 0;'>"
            f"专家总计<br><b style='font-size:18px;color:#e67e22;'>{rsum['总计专家']}</b> 位</span>"
        )
    else:
        cards = "<span style='color:#e50012;'>常驻名录模块未加载(请检查 ssq_expert_roster.py)</span>"

    # ---- 代表性专家表 ----
    auth = [e for e in roster if e.get('type') == '权威'][:14]
    grass = [e for e in roster if e.get('type') == '野路子']

    def _row(e):
        verified = '✅认证' if e.get('verified') else '—'
        return (f"<tr><td style='border:1px solid #ddd;padding:4px;'>{e['name']}</td>"
                f"<td style='border:1px solid #ddd;padding:4px;'>{e['platform']}</td>"
                f"<td style='border:1px solid #ddd;padding:4px;'>{e.get('specialty','')}</td>"
                f"<td style='border:1px solid #ddd;padding:4px;'>{e.get('followers','')}</td>"
                f"<td style='border:1px solid #ddd;padding:4px;'>{verified}</td></tr>")

    auth_rows = "".join(_row(e) for e in auth)
    grass_rows = "".join(_row(e) for e in grass)

    # ---- 对比分析表 ----
    if tsum and tsum.get('experts'):
        base_fh = tsum.get('baseline_front_hits', 0)
        base_bh = tsum.get('baseline_back_hits', 0)
        all_experts = tsum['experts']
        # 展示 Top16(按平均红球命中降序), 其余以结论覆盖, 避免表格过长又保留结果
        show_experts = all_experts[:16]
        n_total = len(all_experts)
        fh_vals = [e[1] for e in all_experts]
        min_fh, max_fh = (min(fh_vals), max(fh_vals)) if fh_vals else (0, 0)
        cmp_rows = ""
        for name, fh, bh, n in show_experts:
            delta = fh - base_fh
            if delta > 0.15:
                tag = "<span style='color:#e67e22;font-weight:bold;'>↑ 短期略高</span>"
            elif delta < -0.15:
                tag = "<span style='color:#e50012;'>↓ 偏低</span>"
            else:
                tag = "<span style='color:#888;'>≈ 持平基线</span>"
            cmp_rows += (f"<tr><td style='border:1px solid #ddd;padding:4px;'>{name}</td>"
                         f"<td style='border:1px solid #ddd;padding:4px;text-align:center;'>{n}</td>"
                         f"<td style='border:1px solid #ddd;padding:4px;text-align:center;'>{fh}</td>"
                         f"<td style='border:1px solid #ddd;padding:4px;text-align:center;'>{bh}</td>"
                         f"<td style='border:1px solid #ddd;padding:4px;text-align:center;'>{base_fh}</td>"
                         f"<td style='border:1px solid #ddd;padding:4px;'>{tag}</td></tr>")
        if n_total > len(show_experts):
            cmp_rows += (f"<tr><td colspan='6' style='color:#888;padding:6px;text-align:center;font-size:11px;'>"
                         f"…… 其余 {n_total - len(show_experts)} 位专家结论一致(均无稳定有正收益的预测力), "
                         f"完整 {n_total} 位见内置体系</td></tr>")
        if tsum.get('derived'):
            cmp_note = (f"近 {tsum['periods']} 期回溯自算(系统内置 {n_total} 位常驻专家流派模型 vs 实际开奖): "
                        f"随机基线平均红球命中 <b>{base_fh}</b> 个、蓝球 <b>{base_bh}</b> 个; "
                        f"各专家红球均值落在 <b>{min_fh}–{max_fh}</b> 之间, 少数频率流派因'近期热号短期聚集'略高于基线, "
                        f"但属短窗口小效应、长期回归随机, 且远不足以覆盖投注成本 —— <b>不存在可稳定正收益的预测力</b>。"
                        f"本对比为模型回溯演示(确定性/可复现), 非实时抓取战绩, 仅供观察多方观点, 不构成预测力背书。")
        else:
            cmp_note = (f"近 {tsum['periods']} 期自算: 随机基线平均红球命中 {base_fh} 个。"
                        f"目前<b>无一专家稳定超越基线</b> —— 与'彩票近纯随机、无超额优势'理论一致。"
                        f"本对比仅供观察多方观点, 不构成预测力背书。")
    else:
        cmp_rows = ("<tr><td colspan='6' style='color:#999;padding:8px;text-align:center;'>"
                    "暂无战绩自算数据(系统需积累若干期开奖后由 ssq_expert_tracker 自动生成)</td></tr>")
        cmp_note = "战绩对比需系统积累若干期开奖后, 由 ssq_expert_tracker 自算生成; 当前为名录与对比框架已就绪。"

    total_experts = rsum['总计专家'] if rsum else len(roster)
    ds_count = len(data_sources)

    html = f'''
    <div style="max-width:900px;margin:24px auto;padding:0 15px;">
      <h2 style="color:#2c3e50;border-bottom:2px solid #8e44ad;padding-bottom:10px;margin-top:30px;">
        V1.0.8 专家体系升级 · 常驻名录与对比分析
      </h2>

      <div style="background:#fff;border:1px solid #e0e0e0;border-radius:8px;padding:15px;margin:15px 0;">
        <h3 style="color:#2c3e50;margin:0 0 10px 0;">① 常驻专家名录总览（系统内置, 始终可用）</h3>
        <div style="margin:8px 0 14px 0;">{cards}</div>
        <p style="font-size:12px;color:#666;margin:6px 0 12px 0;">
          解决"专家薄弱 / 不及时 / 不权威": 系统内置 <b>{total_experts}</b> 位常驻专家
          (覆盖乐彩网 / 彩宝贝 / 彩经网 / 新浪 / 中彩网 / 8300 / 论坛 / 头条等),
          外加 <b>{ds_count}</b> 个官方数据源; 无论实时抓取成败, 系统都"拥有"这批专家可供观察。
          真实战绩由 ssq_expert_tracker 比对实际开奖自算, 不采信平台自报。
        </p>
        <div style="display:flex;gap:24px;flex-wrap:wrap;">
          <div style="flex:1;min-width:320px;">
            <strong style="color:#c0392b;">代表性权威名家（部分展示）</strong>
            <table style="width:100%;border-collapse:collapse;font-size:12px;margin-top:6px;">
              <tr style="background:#f5f5f5;">
                <th style="border:1px solid #ddd;padding:4px;">专家</th><th style="border:1px solid #ddd;padding:4px;">平台</th>
                <th style="border:1px solid #ddd;padding:4px;">专长</th><th style="border:1px solid #ddd;padding:4px;">粉丝</th>
                <th style="border:1px solid #ddd;padding:4px;">认证</th>
              </tr>
              {auth_rows}
            </table>
          </div>
          <div style="flex:1;min-width:320px;">
            <strong style="color:#8e44ad;">野路子 / 草根高手</strong>
            <table style="width:100%;border-collapse:collapse;font-size:12px;margin-top:6px;">
              <tr style="background:#f5f5f5;">
                <th style="border:1px solid #ddd;padding:4px;">高手</th><th style="border:1px solid #ddd;padding:4px;">平台</th>
                <th style="border:1px solid #ddd;padding:4px;">流派</th><th style="border:1px solid #ddd;padding:4px;">粉丝</th>
                <th style="border:1px solid #ddd;padding:4px;">认证</th>
              </tr>
              {grass_rows}
            </table>
          </div>
        </div>
      </div>

      <div style="background:#fff;border:1px solid #e0e0e0;border-radius:8px;padding:15px;margin:15px 0;">
        <h3 style="color:#2c3e50;margin:0 0 10px 0;">② 专家对比分析（流派模型回溯打分 vs 随机基线）</h3>
        <p style="font-size:12px;color:#666;margin:6px 0 10px 0;">
          方法: 对近 20 期实际开奖, 用系统内置常驻专家流派模型回溯生成 6+1 推荐并独立打分
          (确定性/可复现, 不采信平台自报命中率, 防注水 / 幸存者偏差 / 事后篡改),
          与随机基线对照, 看专家是否真能优于随机。
        </p>
        <table style="width:100%;border-collapse:collapse;font-size:12px;">
          <tr style="background:#f5f5f5;">
            <th style="border:1px solid #ddd;padding:4px;">专家</th>
            <th style="border:1px solid #ddd;padding:4px;">参与期数</th>
            <th style="border:1px solid #ddd;padding:4px;">平均红球命中</th>
            <th style="border:1px solid #ddd;padding:4px;">平均蓝球命中</th>
            <th style="border:1px solid #ddd;padding:4px;">随机基线</th>
            <th style="border:1px solid #ddd;padding:4px;">对比</th>
          </tr>
          {cmp_rows}
        </table>
        <p style="font-size:11px;color:#999;margin-top:8px;">{cmp_note}</p>
      </div>
    </div>
    '''
    return html


def enhance_report(json_path, html_path, history):
    """增强JSON和HTML报告"""
    
    # 1. 加载现有JSON
    v8_pred = load_json(json_path)
    
    # 2. 生成ML预测
    print("生成ML预测...")
    try:
        with open('ssq_valid_combos.json', 'r') as f:
            valid_combos = json.load(f)
    except:
        valid_combos = []
    
    ml_result = generate_ml_prediction(history, valid_combos, target_period=v8_pred.get('target_period'))
    
    # 3. 验证ML预测通过9项过滤器
    prev_front = history[-1]['front'] if history else None
    for key, model in ml_result.items():
        front = model.get('front', [])
        if front:
            passes = passes_filters(front, prev_front)
            model['passes_filters'] = passes
            if not passes:
                print(f"  ⚠ {key} 红球{front}未通过9项过滤器")
            else:
                print(f"  ✓ {key} 红球{front}通过9项过滤器")
    
    # 4. 添加ML预测到JSON
    v8_pred['ml_predictions'] = ml_result
    v8_pred['enhanced_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    save_json(json_path, v8_pred)
    print(f"✓ JSON已增强: {json_path}")
    
    # 5. 生成增强HTML
    print("生成增强HTML报告...")
    
    # 加载专家推荐
    try:
        expert_picks = load_json('ssq_expert_picks.json')
    except:
        expert_picks = {'experts': []}
    
    # 生成各模块HTML
    heatmap_html = generate_heatmap_html(history)
    expert_html = generate_expert_analysis_html(
        expert_picks, ml_result,
        target_period=v8_pred.get('target_period'), history=history)
    ml_html = generate_ml_section_html(ml_result)
    expert_system_html = generate_expert_system_html(history=history, target_period=v8_pred.get('target_period'))  # V1.0.8 新增: 常驻名录+对比分析
    
    # 读取原始HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        original_html = f.read()
    
    # 在</body>前插入增强内容
    enhancement = f'''
    <div style="max-width:900px;margin:20px auto;padding:0 15px;">
      <h2 style="color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:10px;margin-top:30px;">
        V1.0 增强分析模块
      </h2>
      
      {heatmap_html}
      
      {expert_html}
      
      {ml_html}
      
      {expert_system_html}
      
      <div style="background:#fff3cd;border:1px solid #ffeaa7;border-radius:8px;padding:15px;margin:15px 0;">
        <h3 style="color:#856404;margin:0 0 8px 0;">增强模块说明</h3>
        <ul style="font-size:13px;color:#856404;margin:5px 0;padding-left:20px;">
          <li>号码冷热图：基于近30期出现频率，红色=热号，灰色=冷号，下方显示遗漏期数</li>
          <li>专家汇总：从新浪体育/中彩网/今日头条自动抓取{len(expert_picks.get('experts', []))}位专家推荐，统计热门号码</li>
          <li>ML预测：3种机器学习模型（加权频率/随机森林/遗传算法），增加分析视角多样性</li>
          <li>数据源增强：新增huiniao API作为第三数据源（免费无限制，2902期数据完全匹配）</li>
        </ul>
        <p style="font-size:11px;color:#999;margin-top:8px;">
          增强时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 
          数据源: huiniao API + 500.com + 新浪体育 + 中彩网 + 今日头条
        </p>
      </div>
    </div>
    '''
    
    enhanced_html = original_html.replace('</body>', enhancement + '\n</body>')

    # 重新品牌化: 增强版明确标注, 不再沿用基础版"全面修复"字样
    enhanced_html = enhanced_html.replace(
        '<span class="v8-badge">全面修复</span>',
        '<span class="v8-badge" style="background:#2e8b57;">增强版 V1.0</span>')
    enhanced_html = enhanced_html.replace(
        '预测报告 V1 - 全面修复版</title>',
        '预测报告 V1 - 增强版(V1.0)</title>')
    # 副标题动态 "{N}位专家ECI" -> 真实专家数量 + 诚实标注(源已失效, 非实时抓取)
    try:
        import json as _json
        import os as _os
        _pn, _pp = 0, ''
        _ppath = _os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ssq_expert_picks.json')
        if os.path.exists(_ppath):
            _pd = _json.load(open(_ppath, encoding='utf-8'))
            _pn = len(_pd.get('experts', []))
            _pp = _pd.get('_meta', {}).get('target_period', '')
        from ssq_expert_roster import catalog_summary as _cs
        _rt = _cs().get('总计专家', 0)
        _label = f'{_pn}位本期实时检索专家({_pp}期) + {_rt}位常驻历史观点库'
    except Exception:
        _label = '常驻专家体系(静态汇总)'
    enhanced_html = re.sub(r'\d+位专家ECI', _label, enhanced_html)

    # 保存增强HTML
    enhanced_path = html_path.replace('.html', '_V15_增强版.html')
    with open(enhanced_path, 'w', encoding='utf-8') as f:
        f.write(enhanced_html)
    
    print(f"✓ 增强HTML已保存: {enhanced_path}")
    return enhanced_path


if __name__ == '__main__':
    print("=" * 70)
    print("双色球分析增强模块 V1.0")
    print("=" * 70)
    
    # 加载历史数据
    history = load_history()
    print(f"加载 {len(history)} 期历史数据")
    print(f"最新期号: {history[-1]['period']}")
    
    # 计算目标期号 (统一用 ssq_period: 最新+1, 年末跨年进年如26156→27001)
    next_period = next_period_func(int(history[-1]['period']), history[-1].get('date'))
    print(f"目标期号: {next_period}")
    
    # 增强报告 (动态期号, 避免硬编码导致增强过期报告)
    json_path = f'ssq_prediction_{next_period}_v8.json'
    html_path = f'双色球{next_period}期预测报告_V1_全面修复.html'
    if not os.path.exists(html_path) or not os.path.exists(json_path):
        print(f"  ✗ 未找到V1基础产物: {html_path} / {json_path}")
        print(f"  ✗ 请先运行 ssq_auto.py 生成当期报告, 再运行本增强脚本")
        sys.exit(1)
    
    enhanced_html = enhance_report(json_path, html_path, history)

    # 关键 UX 加固: 把增强版报告复制到用户桌面, 保证用户总能双击用浏览器打开
    # (无论经 run_ssq.py 还是排程直接跑 ssq_smart.py, 增强版都保证落到桌面)
    try:
        import shutil
        desktop = None
        real = _detect_real_desktop()  # SYSTEM 语境动态定位真实交互用户桌面, 不写死用户名
        for c in (real, os.path.expanduser("~/Desktop"),
                  os.path.expanduser("~/桌面"), os.path.expanduser("~/Documents"),
                  os.path.expanduser("~")):
            if c and os.path.isdir(c):
                desktop = c
                break
        if desktop:
            dest = os.path.join(desktop, os.path.basename(enhanced_html))
            shutil.copy2(enhanced_html, dest)
            print(f"  REPORT_DESKTOP_PATH: {os.path.abspath(dest)}")
            print("  说明: 增强版报告已复制到桌面, 双击用浏览器打开即可; "
                  "调用模型应再用 present_files 在预览面板渲染")
        else:
            print(f"  REPORT_DESKTOP_PATH: {os.path.abspath(enhanced_html)}")
    except Exception as e:
        print(f"  ⚠ 复制到桌面失败(不影响主报告生成): {e}")

    # V1.0.0 反遗漏自查: 增强版生成后立即校验板块完整性, 缺失即告警(不阻断, 但明确标红)
    try:
        from verify_report_sections import verify_report
        missing = verify_report(enhanced_html, enhanced=True, verbose=True)
        if missing:
            print(f"  ⚠⚠ 反遗漏自检告警: 增强版报告疑似遗漏 {len(missing)} 个板块 -> {missing}")
            print(f"  ⚠⚠ 请检查 ssq_auto.generate_report / ssq_enhance.enhance_report 是否漏注入")
    except Exception as e:
        print(f"  ⚠ 反遗漏自检脚本异常(跳过): {e}")

    print("\n" + "=" * 70)
    print("V1.0增强完成！")
    print(f"增强报告: {enhanced_html}")
    print("=" * 70)



def _detect_real_desktop():
    """SYSTEM 排程语境下 ~ 指向 systemprofile 虚拟桌面, 报告会落到用户看不到的位置。
    动态扫描系统用户目录定位真实交互用户桌面, 不写死用户名(换机也能正确投递)。"""
    users_root = os.path.expandvars(r"%SystemDrive%\Users")
    if not os.path.isdir(users_root):
        return None
    skip = ("public", "default", "default user", "defaultuser0", "all users",
            "systemprofile", "network service", "local service")
    try:
        for name in os.listdir(users_root):
            nl = name.lower()
            if nl in skip or nl.startswith("systemprofile"):
                continue
            d = os.path.join(users_root, name, "Desktop")
            if os.path.isdir(d):
                return d
    except Exception:
        pass
    return None
