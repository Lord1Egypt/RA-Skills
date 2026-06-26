#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VectorBT 批量回测报告生成器
读取 summary.csv 中的股票列表，逐一生成 VBT 回测报告 + HTML 索引页

Usage:
    python batch_report.py --csv D:/nginx/work/fx/test_a/summary.csv --output D:/nginx/work/vbtr [--data-dir F:/new_tdx64]
"""
import sys, os, warnings, io, argparse, time, traceback
from multiprocessing import Pool

# 先 import report.py（它的 import 副作用会设置 sys.stdout = TextIOWrapper），
# 但我们随后重新设置回可靠的 stdout
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import pandas as pd
import numpy as np

# 重新设置 stdout 以支持 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
warnings.filterwarnings('ignore')

# ==============================================================================
# 从 CSV/XLS/XLSX 读取股票列表（自适应格式）
# ==============================================================================
def _is_valid_code(v):
    """判断是否为A股6位代码：0/3/6开头，或92开头(北交所)"""
    s = str(v).strip()
    return len(s) == 6 and s.isdigit() and (s[0] in ('0', '3', '6') or s[:2] == '92')


def _detect_stocks_in_rows(rows_iter):
    """遍历行数据（每行为list），智能识别股票代码和名称"""
    stocks = []
    for row in rows_iter:
        code = None
        name = None
        for i, v in enumerate(row):
            # 6位字符串代码
            if isinstance(v, str) and v.strip().isdigit():
                candidate = v.strip()
                if _is_valid_code(candidate):
                    code = candidate
                    # 下一列为名称
                    if i + 1 < len(row) and row[i+1] and not str(row[i+1]).strip().isdigit():
                        name = str(row[i+1]).strip()
                    break
            # 数字类型（Excel 000001存为1）
            elif isinstance(v, (int, float)) and v > 0:
                candidate = str(int(v)).zfill(6)
                if _is_valid_code(candidate):
                    code = candidate
                    if i + 1 < len(row) and row[i+1] and not isinstance(row[i+1], (int, float)):
                        name = str(row[i+1]).strip()
                    break
        if code:
            stocks.append({'code': code, 'name': name or code,
                           'signal': '', 'score': 0, 'advice': ''})
    return stocks


def read_stock_list(path):
    """读取 CSV/XLS/XLSX 文件，返回 [{'code','name','signal',...}]

    第一策略：列头识别（"代码"/"名称"/"信号"/"评分"）
    第二策略：智能扫描（无列头时按内容识别6位股票代码）
    """
    ext = os.path.splitext(path)[1].lower()

    # 加载DataFrame
    if ext in ('.xlsx', '.xls'):
        if ext == '.xlsx':
            try:
                import openpyxl
            except ImportError:
                print("[ERROR] 请安装 openpyxl: pip install openpyxl")
                return []
        else:
            try:
                import xlrd
            except ImportError:
                print("[ERROR] 请安装 xlrd: pip install xlrd")
                return []
        df = pd.read_excel(path)
    elif ext == '.csv':
        df = pd.read_csv(path, encoding='utf-8')
    else:
        print(f"[ERROR] 不支持的文件格式: {ext}（支持 .csv/.xlsx/.xls）")
        return []

    # 策略1: 列头识别
    col_map = {}
    for c in df.columns:
        cl = str(c).strip()
        if '代码' in cl or 'code' in cl.lower():
            col_map['code'] = c
        elif '名称' in cl or 'name' in cl.lower():
            col_map['name'] = c
        elif '信号' in cl or 'signal' in cl.lower():
            col_map['signal'] = c
        elif '评分' in cl:
            col_map['score'] = c
        elif '操作' in cl or '建议' in cl:
            col_map['advice'] = c

    stocks = []
    if 'code' in col_map:
        # 列头模式
        for _, row in df.iterrows():
            code = str(row.get(col_map['code'], '')).strip().zfill(6)
            name = str(row.get(col_map.get('name', ''), '')).strip()
            signal = str(row.get(col_map.get('signal', ''), '')).strip()
            score = row.get(col_map.get('score', ''), 0)
            advice = str(row.get(col_map.get('advice', ''), '')).strip()
            try:
                score = float(score) if score != '' else 0.0
            except:
                score = 0.0
            if code and _is_valid_code(code):
                stocks.append({'code': code, 'name': name or code,
                               'signal': signal, 'score': score, 'advice': advice})
    else:
        # 策略2: 内容智能扫描（兼容券商持仓导出格式）
        rows = []
        for _, row in df.iterrows():
            rows.append([str(v).strip() if not isinstance(v, (int, float)) else v for v in row])
        stocks = _detect_stocks_in_rows(rows)

    print(f"  识别到 {len(stocks)} 只股票")
    return stocks


# ==============================================================================
# 单只股票回测
# ==============================================================================
def backtest_single(ticker, stock_name, data_dir):
    """对单只股票运行完整回测，返回 (results, all_pfs, df)"""
    from report import get_data, BacktestEngine
    df = get_data(ticker, data_dir)
    price = df['Close'].astype(float)
    high = df['High'].astype(float)
    low = df['Low'].astype(float)
    be = BacktestEngine(price, high, low)
    results = be.run_all()
    return results, be.all_pfs, df


def _run_stock_worker(params):
    """Pool.map worker: 单只股票完整处理（回测→报告→指标提取）"""
    code, name, signal, score, advice, data_dir, output_dir = params
    report_file = f"{code}_{name}_vbt_report.html" if name else f"{code}_vbt_report.html"
    report_path = os.path.join(output_dir, report_file)

    try:
        from report import get_data, BacktestEngine, generate_report, guess_stock_name

        # 回测
        results, all_pfs, df = backtest_single(code, name, data_dir)
        best = results[0]

        # 生成报告
        stock_name_zh = guess_stock_name(code)
        generate_report(code, stock_name_zh, df, results, all_pfs, report_path)

        # 提取VBT综合判定
        import re
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                html = f.read()
            m = re.search(r'<span class="status-label" style="color:var\(([\w-]+)\)">(.*?)</span>', html)
            vbt_vcolor = m.group(1).lstrip('-') if m else 'yellow'
            vbt_verdict = m.group(2).strip() if m else ''
        except Exception:
            vbt_vcolor = 'yellow'
            vbt_verdict = ''

        return {
            'code': code, 'name': name, 'signal': signal, 'score': score,
            'advice': advice, 'success': True,
            'report_file': report_file,
            'best_name': best['name'],
            'best_ret': f"{best['ret']*100:+.2f}%",
            'best_ret_val': best['ret'] * 100,
            'best_nt': best['nt'],
            'best_wr': best['wr'] * 100,
            'best_sharpe': best['sharpe'],
            'best_mdd': best['mdd'] * 100,
            'vbt_verdict': vbt_verdict,
            'vbt_vcolor': vbt_vcolor,
        }
    except Exception as e:
        return {
            'code': code, 'name': name, 'signal': signal, 'score': score,
            'advice': advice, 'success': False,
            'report_file': '', 'best_name': '', 'best_ret': '',
            'best_nt': 0, 'best_wr': 0, 'best_sharpe': 0, 'best_mdd': 0,
            'best_ret_val': 0, 'vbt_verdict': '', 'vbt_vcolor': 'yellow',
            'error': str(e),
        }


# ==============================================================================
# 提取信号分类
# ==============================================================================
def classify_vbt_verdict(vbt_verdict):
    """将VBT综合判定归类: 看多/中性区间/看空"""
    if not vbt_verdict or not vbt_verdict.strip():
        return 'neutral'
    if vbt_verdict in ('看多',):
        return 'bullish'
    if vbt_verdict in ('看空',):
        return 'bearish'
    return 'neutral'


VBTCATS = {
    'bullish':  {'label': '看多', 'color': 'var(--green)', 'css': 'sig-buy'},
    'neutral':  {'label': '中性区间', 'color': 'var(--yellow)', 'css': 'sig-neutral'},
    'bearish':  {'label': '看空', 'color': 'var(--red)', 'css': 'sig-sell'},
}


VBTCAT_ORDER = {'bullish': 0, 'neutral': 1, 'bearish': 2}


def parse_report_snapshot(report_path):
    """从已有HTML报告中提取回测关键数据"""
    import re
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            html = f.read()
        # 提取最佳策略名称 (h2)
        m = re.search(r'最佳策略净值曲线 — ([^<]+)', html)
        best_name = m.group(1).strip() if m else ''
        # 提取总收益
        m = re.search(r'总收益<[^>]*>.*?<[^>]*>([+\-][\d.]+)%<', html)
        best_ret = m.group(1) + '%' if m else ''
        best_ret_val = float(m.group(1)) if m else 0
        # 提取胜率
        m = re.search(r'胜率<[^>]*>.*?<[^>]*>([\d.]+)%<', html)
        best_wr = float(m.group(1)) if m else 0
        # 提取夏普
        m = re.search(r'夏普比率<[^>]*>.*?<[^>]*>([+\-][\d.]+)<', html)
        best_sharpe = float(m.group(1)) if m else 0
        # 提取最大回撤
        m = re.search(r'最大回撤<[^>]*>.*?<[^>]*>([+\-]?[\d.]+)%<', html)
        best_mdd = float(m.group(1)) if m else 0
        # 提取 VBT 综合判定 (看多/看空/中性区间)
        # 用 status-label class 定位（唯一出现在综合判定行）
        m = re.search(r'<span class="status-label" style="color:var\(([\w-]+)\)">(.*?)</span>', html)
        if m:
            vbt_vcolor = m.group(1).lstrip('-')
            vbt_verdict = m.group(2).strip()
        else:
            vbt_vcolor = 'yellow'
            vbt_verdict = ''
        # 提取交易次数
        m = re.search(r'交易次数[^>]*>.*?<[^>]*>(\d+)<', html)
        best_nt = int(m.group(1)) if m else 0
        return best_name, best_ret, best_ret_val, best_nt, best_wr, best_sharpe, best_mdd, vbt_verdict, vbt_vcolor
    except:
        return '', '', 0, 0, 0, 0, 0, '', 'yellow'


# ==============================================================================
# 生成索引 HTML 页
# ==============================================================================
def gen_index_html(stock_results, output_dir):
    """生成包含所有股票回测摘要的索引页面（支持信号分类、排序）"""
    now = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')

    rows_data = []
    for sr in stock_results:
        code = sr['code']
        name = sr['name']
        signal = sr.get('signal', '')
        score = sr.get('score', 0)
        advice = sr.get('advice', '')
        ok = sr.get('success', False)
        best_name = sr.get('best_name', '')
        best_ret_val = sr.get('best_ret_val', 0)
        best_ret_str = sr.get('best_ret', '')
        best_nt = sr.get('best_nt', 0)
        best_wr = sr.get('best_wr', 0)
        best_sharpe = sr.get('best_sharpe', 0)
        best_mdd = sr.get('best_mdd', 0)
        report_file = sr.get('report_file', '')
        vbt_verdict = sr.get('vbt_verdict', '')
        vbt_vcolor = sr.get('vbt_vcolor', 'yellow')

        # VBT综合判定作为信号分类依据
        vbt_cat = classify_vbt_verdict(vbt_verdict)
        rows_data.append({
            'code': code, 'name': name, 'signal': signal, 'sig_cat': vbt_cat,
            'best_ret_val': best_ret_val, 'best_ret_str': best_ret_str,
            'best_nt': best_nt,
            'best_wr': best_wr, 'best_sharpe': best_sharpe, 'best_mdd': best_mdd,
            'best_name': best_name, 'ok': ok, 'report_file': report_file,
            'vbt_verdict': vbt_verdict, 'vbt_vcolor': vbt_vcolor,
        })

    # 统计
    total = len(stock_results)
    success = sum(1 for sr in stock_results if sr.get('success'))
    failed = total - success
    buy_signals = sum(1 for sr in stock_results if "买入" in sr.get('signal', ''))
    sell_signals = sum(1 for sr in stock_results if "卖出" in sr.get('signal', ''))

    # 各分类数量
    cat_counts = {}
    for cat in VBTCATS:
        cat_counts[cat] = sum(1 for r in rows_data if r['sig_cat'] == cat)

    # 生成行 JSON 数据（含 data-sort 属性，供JS排序）
    import json
    rows_json = json.dumps(rows_data, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VBT 批量回测报告索引</title>
<style>
  :root {{ --bg:#0d1117;--card:#161b22;--border:#30363d;--text:#c9d1d9;--text-dim:#8b949e;--text-bright:#f0f6fc;
    --green:#3fb950;--red:#f85149;--yellow:#d29922;--blue:#58a6ff;--purple:#bc8cff; }}
  * {{ margin:0;padding:0;box-sizing:border-box; }}
  body {{ background:var(--bg);color:var(--text);font-family:-apple-system,'Segoe UI',sans-serif;padding:20px;max-width:1400px;margin:0 auto; }}
  .header {{ text-align:center;padding:30px 0;border-bottom:1px solid var(--border);margin-bottom:30px; }}
  .header h1 {{ font-size:28px;color:var(--text-bright); }}
  .card {{ background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px;margin-bottom:20px; }}
  .card h2 {{ font-size:16px;color:var(--text-bright);margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid var(--border); }}
  table {{ width:100%;border-collapse:collapse;font-size:13px;table-layout:auto; }}
  th,td {{ padding:8px 10px;border-bottom:1px solid rgba(48,54,61,0.5);text-align:left;white-space:nowrap; }}
  th {{ color:var(--text-dim);font-weight:500;font-size:12px;position:sticky;top:0;background:#1a1f29;z-index:2;cursor:pointer;user-select:none; }}
  th:hover {{ color:var(--text-bright); }}
  th .sort-arrow {{ margin-left:4px;font-size:10px;opacity:0.4; }}
  th.sorted .sort-arrow {{ opacity:1;color:var(--blue); }}
  tr:hover {{ background:rgba(255,255,255,0.03); }}
  a {{ color:var(--blue);text-decoration:none; }}
  a:hover {{ text-decoration:underline; }}
  .stats {{ display:flex;gap:16px;flex-wrap:wrap;margin-bottom:12px; }}
  .stat-box {{ background:rgba(255,255,255,0.03);border-radius:8px;padding:14px 20px;text-align:center;flex:1;min-width:100px;cursor:pointer;transition:all 0.15s;border:1px solid transparent; }}
  .stat-box:hover {{ background:rgba(255,255,255,0.06); }}
  .stat-box.active {{ border-color:var(--blue);background:rgba(88,166,255,0.08); }}
  .stat-box .num {{ font-size:26px;font-weight:700; }}
  .stat-box .lbl {{ font-size:11px;color:var(--text-dim);margin-top:4px; }}
  .filter-bar {{ display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px;align-items:center; }}
  .filter-bar .search-box {{ flex:1;min-width:200px; }}
  .filter-bar input {{ background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:8px 12px;color:var(--text);width:100%;font-size:14px; }}
  .filter-bar input:focus {{ outline:none;border-color:var(--blue); }}
  .sig-btn {{ padding:6px 14px;border-radius:6px;border:1px solid var(--border);background:transparent;color:var(--text-dim);font-size:12px;cursor:pointer;white-space:nowrap;transition:all 0.15s; }}
  .sig-btn:hover {{ color:var(--text-bright);border-color:var(--text-dim); }}
  .sig-btn.active {{ background:rgba(88,166,255,0.1);border-color:var(--blue);color:var(--blue);font-weight:600; }}
  .sig-btn.all {{ border-color:var(--border); }}
  .sig-buy {{ color:var(--green);font-weight:600; }} .sig-neutral {{ color:var(--yellow); }}
  .sig-sell {{ color:var(--red);font-weight:600; }}
  .cell-ret {{ font-weight:600; }}
  .cell-num {{ font-family:'SF Mono','Cascadia Code',monospace;font-size:12px; }}
  .footer {{ text-align:center;padding:30px 0;color:var(--text-dim);font-size:12px;border-top:1px solid var(--border);margin-top:30px; }}
  .count-badge {{ font-size:10px;margin-left:4px;opacity:0.6; }}
  .table-container {{ overflow-x:auto;max-height:75vh;overflow-y:auto; }}
</style>
</head>
<body>

<div class="header">
  <h1>VBT 向量化回测批量报告</h1>
  <div style="color:var(--text-dim);margin-top:8px">生成时间: {now} | 数据源: 通达信/网络 | VectorBT v2.2.0</div>
</div>

<div class="stats">
  <div class="stat-box" onclick="filterSignal('all')" id="stat-all">
    <div class="num" style="color:var(--blue)">{total}</div><div class="lbl">股票总数</div>
  </div>
  <div class="stat-box" onclick="filterSignal('bullish')" id="stat-bullish">
    <div class="num" style="color:var(--green)">{cat_counts.get('bullish', 0)}</div><div class="lbl">看多</div>
  </div>
  <div class="stat-box" onclick="filterSignal('neutral')" id="stat-neutral">
    <div class="num" style="color:var(--yellow)">{cat_counts.get('neutral', 0)}</div><div class="lbl">中性区间</div>
  </div>
  <div class="stat-box" onclick="filterSignal('bearish')" id="stat-bearish">
    <div class="num" style="color:var(--red)">{cat_counts.get('bearish', 0)}</div><div class="lbl">看空</div>
  </div>
  <div class="stat-box" id="stat-status" style="cursor:default">
    <div class="num"><span style="color:var(--green)">{success}</span> / <span style="color:var(--red)">{failed}</span></div>
    <div class="lbl">成功 / 失败</div>
  </div>
</div>

<div class="card">
  <h2>股票回测列表 <span id="filtered-count" style="font-weight:400;font-size:13px;color:var(--text-dim);"></span></h2>
  <div class="filter-bar">
    <button class="sig-btn all active" onclick="filterSignal('all')" id="btn-all">全部<span class="count-badge">{total}</span></button>
    <button class="sig-btn" onclick="filterSignal('bullish')" id="btn-bullish">▲ 看多<span class="count-badge">{cat_counts.get('bullish', 0)}</span></button>
    <button class="sig-btn" onclick="filterSignal('neutral')" id="btn-neutral">— 中性区间<span class="count-badge">{cat_counts.get('neutral', 0)}</span></button>
    <button class="sig-btn" onclick="filterSignal('bearish')" id="btn-bearish">▼ 看空<span class="count-badge">{cat_counts.get('bearish', 0)}</span></button>
    <div class="search-box">
      <input type="text" id="search" placeholder="搜索代码/名称..." onkeyup="applyFilters()">
    </div>
  </div>
  <div class="table-container">
  <table id="stock-table">
    <thead>
    <tr>
      <th data-sort="code" style="width:80px">代码 <span class="sort-arrow">▲</span></th>
      <th data-sort="name" style="width:90px">名称 <span class="sort-arrow">▲</span></th>
      <th data-sort="sig_order" style="width:75px">tdx3信号 <span class="sort-arrow">▲</span></th>
      <th data-sort="vbt_verdict" style="width:55px">VBT判定 <span class="sort-arrow">▲</span></th>
      <th data-sort="best_ret_val" style="width:85px">最佳收益 <span class="sort-arrow">▲</span></th>
      <th data-sort="best_nt" style="width:45px">交易次数 <span class="sort-arrow">▲</span></th>
      <th data-sort="best_wr" style="width:50px">胜率 <span class="sort-arrow">▲</span></th>
      <th data-sort="best_sharpe" style="width:50px">夏普 <span class="sort-arrow">▲</span></th>
      <th data-sort="best_mdd" style="width:70px">最大回撤 <span class="sort-arrow">▲</span></th>
      <th data-sort="best_name" style="width:120px">最佳策略 <span class="sort-arrow">▲</span></th>
      <th data-sort="code" style="width:60px">报告 <span class="sort-arrow">▲</span></th>
    </tr>
    </thead>
    <tbody id="table-body"></tbody>
  </table>
  </div>
</div>

<div class="footer">
  <p>VectorBT v2.2.0 | 报告生成: {now}</p>
  <p style="margin-top:8px;color:var(--text-dim);font-size:12px">⚠️ 本报告仅供参考，不构成投资建议。回测结果不代表未来收益。</p>
</div>

<script>
// ======= 数据 =======
var ROWS = {rows_json};

// ======= 状态 =======
var currentFilter = 'all';
var currentSort = {{key: 'code', asc: true}};

// ======= 信号分类 =======
var SIG_ORDER = {{'bullish':0,'neutral':1,'bearish':2}};
var SIG_CSS = {{
    'bullish': 'sig-buy', 'neutral': 'sig-neutral', 'bearish': 'sig-sell'
}};

function colorRet(v) {{ return v >= 0 ? 'var(--green)' : 'var(--red)'; }}
function colorMdd(v) {{ return v <= -15 ? 'var(--red)' : v <= -5 ? 'var(--yellow)' : 'var(--green)'; }}
function colorSharpe(v) {{ return v >= 0.5 ? 'var(--green)' : v >= 0 ? 'var(--yellow)' : 'var(--red)'; }}
function colorWr(v) {{ return v >= 50 ? 'var(--green)' : 'var(--red)'; }}

function renderTable() {{
    var searchText = document.getElementById('search').value.toUpperCase();

    // 过滤
    var filtered = ROWS.filter(function(r) {{
        // 信号过滤
        if (currentFilter !== 'all' && r.sig_cat !== currentFilter) return false;
        // 搜索
        if (searchText) {{
            var txt = (r.code + r.name + r.signal + r.best_name).toUpperCase();
            if (txt.indexOf(searchText) === -1) return false;
        }}
        return true;
    }});

    // 排序
    var key = currentSort.key;
    var asc = currentSort.asc;
    filtered.sort(function(a, b) {{
        var va = a[key], vb = b[key];
        if (key === 'sig_order') {{ va = SIG_ORDER[a.sig_cat] || 99; vb = SIG_ORDER[b.sig_cat] || 99; }}
        if (typeof va === 'string') {{ va = va.toLowerCase(); vb = (vb||'').toLowerCase(); }}
        if (va < vb) return asc ? -1 : 1;
        if (va > vb) return asc ? 1 : -1;
        return 0;
    }});

    // 渲染
    var html = '';
    for (var i = 0; i < filtered.length; i++) {{
        var r = filtered[i];
        var sigCss = SIG_CSS[r.sig_cat] || '';
        var ok = r.ok;
        var statusCell = ok
            ? '<a href="' + r.report_file + '" target="_blank" style="color:var(--green);font-weight:600;">✓ 查看</a>'
            : '<span style="color:var(--red)">✗ 失败</span>';
        var retStr = r.best_ret_str || '';
        var wrStr = ok ? r.best_wr.toFixed(0) + '%' : '-';
        var sharpeStr = ok ? (r.best_sharpe >= 0 ? '+' : '') + r.best_sharpe.toFixed(2) : '-';
	var ntStr = ok ? r.best_nt : '-';
        var mddStr = ok ? r.best_mdd.toFixed(0) + '%' : '-';
        var vbtV = r.vbt_verdict || '';
        var vbtC = 'var(--' + (r.vbt_vcolor || 'yellow') + ')';
        var sigText = r.signal || '';
        var sigDisplay = sigText ? ('<td class="' + sigCss + '">' + sigText + '</td>') : '<td style="color:var(--text-dim)">-</td>';
        html += '<tr style="display:table-row" data-sig="' + (r.sig_cat || '') + '">'
            + '<td><strong>' + r.code + '</strong></td>'
            + '<td>' + r.name + '</td>'
            + sigDisplay
            + '<td style="color:' + vbtC + ';font-weight:600;">' + vbtV + '</td>'
            + '<td class="cell-num cell-ret" style="color:' + (ok ? colorRet(r.best_ret_val) : 'var(--text-dim)') + '">' + retStr
            + (r.best_ret_val > 1000 ? ' <span title="复利满仓操作，极端回测值" style="color:var(--yellow);font-size:10px;cursor:help">⚠</span>' : '') + '</td>'
            + '<td class="cell-num">' + ntStr + '</td>'
            + '<td class="cell-num" style="color:' + (ok ? colorWr(r.best_wr) : 'var(--text-dim)') + '">' + wrStr + '</td>'
            + '<td class="cell-num" style="color:' + (ok ? colorSharpe(r.best_sharpe) : 'var(--text-dim)') + '">' + sharpeStr + '</td>'
            + '<td class="cell-num" style="color:' + (ok ? colorMdd(r.best_mdd) : 'var(--text-dim)') + '">' + mddStr + '</td>'
            + '<td>' + r.best_name + '</td>'
            + '<td>' + statusCell + '</td>'
            + '</tr>';
    }}
    document.getElementById('table-body').innerHTML = html;
    document.getElementById('filtered-count').textContent = '(显示 ' + filtered.length + ' / ' + ROWS.length + ')';

    // 更新排序箭头
    document.querySelectorAll('th').forEach(function(th) {{
        var sk = th.getAttribute('data-sort');
        th.classList.toggle('sorted', sk === currentSort.key);
    }});
}}

// ======= 信号筛选 =======
function filterSignal(cat) {{
    currentFilter = cat;
    // 高亮按钮
    document.querySelectorAll('.sig-btn').forEach(function(b) {{ b.classList.remove('active'); }});
    var btn = document.getElementById('btn-' + cat);
    if (btn) btn.classList.add('active');
    // 高亮统计盒
    document.querySelectorAll('.stat-box').forEach(function(b) {{ b.classList.remove('active'); }});
    var stat = document.getElementById('stat-' + cat);
    if (stat) stat.classList.add('active');
    renderTable();
}}

// ======= 列排序 =======
document.querySelectorAll('th').forEach(function(th) {{
    th.addEventListener('click', function() {{
        var key = this.getAttribute('data-sort');
        if (!key) return;
        if (currentSort.key === key) {{
            currentSort.asc = !currentSort.asc;
        }} else {{
            currentSort.key = key;
            currentSort.asc = true;
        }}
        // 更新箭头方向
        document.querySelectorAll('th .sort-arrow').forEach(function(a) {{ a.textContent = '▲'; }});
        this.querySelector('.sort-arrow').textContent = currentSort.asc ? '▲' : '▼';
        renderTable();
    }});
}});

// ======= 搜索过滤 =======
function applyFilters() {{
    renderTable();
}}

// 初始渲染
renderTable();
</script>

</body>
</html>"""

    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\n索引页生成: {index_path} ({len(html)} bytes)")
    return index_path


# ==============================================================================
# Main
# ==============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='VBTR Batch Report Generator')
    parser.add_argument('--csv', default=None, help='CSV/XLSX/XLS文件路径（含代码列和可选的名称/信号/评分列）')
    parser.add_argument('--stocks', default=None, help='股票列表字符串，如 "000001,平安银行;688711,宏微科技"')
    parser.add_argument('--output', default=r'D:\nginx\work\vbtr', help='输出目录')
    parser.add_argument('--data-dir', default=r'F:\new_tdx64', help='通达信数据目录')
    parser.add_argument('--skip-existing', action='store_true', help='跳过已生成的报告')
    args = parser.parse_args()

    if not args.csv and not args.stocks:
        print("[ERROR] 请指定 --csv（文件路径）或 --stocks（股票列表字符串）")
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)

    # 从 report.py 导入函数
    # report.py 模块级代码会设置 sys.stdout = TextIOWrapper，导入后恢复
    _saved_stdout = sys.stdout
    from report import get_data, BacktestEngine, generate_report, guess_stock_name
    sys.stdout = _saved_stdout

    # 读取股票列表
    if args.csv:
        print(f"读取股票列表: {args.csv}")
        stocks = read_stock_list(args.csv)
    else:
        stocks = []
        for item in args.stocks.split(";"):
            item = item.strip()
            if not item:
                continue
            if "," in item:
                parts = item.split(",", 1)
                stocks.append({'code': parts[0].strip().zfill(6),
                              'name': parts[1].strip(),
                              'signal': '', 'score': 0, 'advice': ''})
            else:
                stocks.append({'code': item.strip().zfill(6),
                              'name': item.strip(),
                              'signal': '', 'score': 0, 'advice': ''})
    print(f"共 {len(stocks)} 只股票")

    stock_results = []
    start_time = time.time()

    # === Step 1: 检查 --skip-existing（主线程串行，只读文件不计算） ===
    to_process = []
    for st in stocks:
        code = st['code']
        name = st['name']
        signal = st.get('signal', '')
        score = st.get('score', 0)
        advice = st.get('advice', '')
        report_file = f"{code}_{name}_vbt_report.html" if name else f"{code}_vbt_report.html"
        report_path = os.path.join(args.output, report_file)

        if args.skip_existing and os.path.exists(report_path):
            best_name, best_ret, best_ret_val, best_nt, best_wr, best_sharpe, best_mdd, vbt_verdict, vbt_vcolor = parse_report_snapshot(report_path)
            sr = st.copy()
            sr['success'] = True
            sr['report_file'] = report_file
            sr['best_name'] = best_name
            sr['best_ret'] = best_ret
            sr['best_ret_val'] = best_ret_val
            sr['best_nt'] = best_nt
            sr['best_wr'] = best_wr
            sr['best_sharpe'] = best_sharpe
            sr['best_mdd'] = best_mdd
            sr['vbt_verdict'] = vbt_verdict
            sr['vbt_vcolor'] = vbt_vcolor
            stock_results.append(sr)
            print(f"[{len(stock_results)}/{len(stocks)}] {code} {name} ⏭ 跳过 (从HTML提取: {best_name} {best_ret})")
        else:
            to_process.append((code, name, signal, score, advice, args.data_dir, args.output))

    # === Step 2: 并行回测未跳过的股票 ===
    if to_process:
        n_workers = min(4, len(to_process))
        print(f"\n并行处理 {len(to_process)} 只股票 (进程数={n_workers})...\n")
        with Pool(processes=n_workers) as pool:
            parallel_results = pool.map(_run_stock_worker, to_process)
        stock_results.extend(parallel_results)

        # 打印结果摘要
        for pr in parallel_results:
            if pr['success']:
                print(f"✓ {pr['code']} {pr['name']}: {pr['best_name']} ({pr['best_ret']})")
            else:
                print(f"✗ {pr['code']} {pr['name']}: 失败 - {pr.get('error', '')}")

    # === Step 3: 统计 ===
    elapsed = time.time() - start_time
    success_cnt = sum(1 for sr in stock_results if sr.get('success'))
    failed_cnt = len(stock_results) - success_cnt

    print(f"\n{'='*60}")
    print(f"处理完成! 成功: {success_cnt}, 失败: {failed_cnt}, 耗时: {elapsed:.0f}s")
    print(f"{'='*60}")

    # 生成索引页
    gen_index_html(stock_results, args.output)
    print(f"\n所有报告已输出至: {os.path.abspath(args.output)}")
