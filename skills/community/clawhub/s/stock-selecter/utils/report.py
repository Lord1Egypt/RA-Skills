#!/usr/bin/env python3
"""
选股结果报告生成器
生成可交互的 HTML 报告，包含：
  - 执行摘要（策略配置、各策略命中数、耗时）
  - 股票表格（可排序、筛选）
  - 各策略评分雷达图（文本版）
  - 下载 CSV 按钮
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any


def generate_html_report(results: Dict[str, Any],
                         output_path: str = None,
                         title: str = "选股结果报告") -> str:
    """
    将 execute() 的返回结果渲染为 HTML 报告

    Args:
        results: execute() 返回的完整结果字典
        output_path: 保存路径（不含文件名）
        title: 报告标题

    Returns:
        HTML 文件的完整路径
    """
    meta  = results.get("metadata", {})
    items = results.get("results", [])
    strategies = meta.get("strategies_used", [])
    mode      = meta.get("mode", "and")
    elapsed   = meta.get("execution_time", 0)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── 表格行 ─────────────────────────────────────────────────
    rows = _build_rows(items, strategies)

    # ── 各策略命中统计 ──────────────────────────────────────────
    per_counts = meta.get("per_strategy_counts", {})
    strategy_stats_html = _build_strategy_stats(per_counts)

    # ── HTML ───────────────────────────────────────────────────
    html = HTML_TEMPLATE.format(
        title=title,
        timestamp=timestamp,
        mode=mode.upper(),
        strategies=", ".join(strategies),
        elapsed=f"{elapsed:.1f}",
        total_count=results.get("count", 0),
        strategy_stats=strategy_stats_html,
        rows_html=rows,
        row_count=len(items),
    )

    if output_path:
        os.makedirs(output_path, exist_ok=True)
        filename = f"选股报告_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
        filepath = os.path.join(output_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[report] HTML 报告已生成: {filepath}")
        return filepath
    return html


# ── 内部函数 ────────────────────────────────────────────────────────

def _build_rows(items: List[Dict], strategies: List[str]) -> str:
    """生成表格行 HTML"""
    if not items:
        return "<tr><td colspan='20' style='text-align:center;color:#999'>暂无数据</td></tr>"

    lines = []
    for i, r in enumerate(items, 1):
        ts_code   = r.get("ts_code", "")
        name      = r.get("name", ts_code)
        score     = r.get("score", 0)
        strategies_hit = r.get("strategies_hit", [])
        industries = r.get("industry", "")

        # 评分色阶（绿涨红跌，A 股惯例）
        score_color = _score_color(score)
        strategies_label = ", ".join(strategies_hit) if strategies_hit else r.get("strategy", "")

        # 动态列：根据命中策略生成对应字段
        extra_cells = _build_extra_cells(r, strategies_hit)

        lines.append(
            f"<tr>"
            f"<td>{i}</td>"
            f"<td class='code'>{ts_code}</td>"
            f"<td class='name'>{name}</td>"
            f"<td>{industries}</td>"
            f"<td class='score' style='color:{score_color}'>{score:.1f}</td>"
            f"<td class='strategies'>{strategies_label}</td>"
            f"{extra_cells}"
            f"</tr>"
        )
    return "\n".join(lines)


def _build_extra_cells(r: Dict, strategies_hit: List[str]) -> str:
    """根据命中的策略动态生成指标列"""
    cells = []
    for s in strategies_hit:
        if s == "roe":
            cells.append(f"<td>{r.get('roe', '-')}</td>")
        elif s == "dividend":
            cells.append(f"<td>{r.get('dv_ratio', '-')}%</td>")
        elif s == "valuation":
            cells.append(f"<td>PE {r.get('pe_ttm', '-')}</td>")
            cells.append(f"<td>PB {r.get('pb', '-')}</td>")
        elif s == "growth":
            cells.append(f"<td>营收↑{r.get('revenue_growth', '-')}%</td>")
        elif s == "macd":
            cells.append(f"<td>放量{r.get('surge_ratio', '-')}x</td>")
        elif s == "low_position_surge":
            cells.append(f"<td>分位{r.get('price_pct_rank', '-')}%</td>")
        elif s == "trend":
            cells.append(f"<td>ADX {r.get('adx', '-')}</td>")
        elif s == "pattern":
            patterns = r.get("patterns", [])
            cells.append(f"<td>{', '.join(patterns) if patterns else '-'}</td>")
    return "".join(cells)


def _score_color(score: float) -> str:
    if score >= 80: return "#1a5f2a"
    if score >= 60: return "#2e8b57"
    if score >= 40: return "#b8860b"
    if score >= 20: return "#cd5c5c"
    return "#8b0000"


def _build_strategy_stats(per_counts: Dict[str, int]) -> str:
    if not per_counts:
        return "<span>无</span>"
    return "".join(
        f"<span class='stat-chip'>{k}: <b>{v}</b></span>"
        for k, v in per_counts.items()
    )


# ── HTML 模板 ────────────────────────────────────────────────────────

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang='zh-CN'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
         background: #f5f7fa; color: #333; padding: 20px; }}
  .container {{ max-width: 1400px; margin: 0 auto; }}

  /* 摘要卡片 */
  .summary-bar { display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }
  .card {{ background: white; border-radius: 10px; padding: 18px 24px;
           box-shadow: 0 2px 8px rgba(0,0,0,.08); flex: 1; min-width: 160px; }}
  .card .label {{ font-size: 12px; color: #888; text-transform: uppercase;
                  letter-spacing: .5px; margin-bottom: 6px; }}
  .card .value {{ font-size: 24px; font-weight: 700; color: #1a1a2e; }}
  .card .sub    {{ font-size: 11px; color: #aaa; margin-top: 2px; }}

  /* 策略统计 */
  .strategy-stats {{ background: white; border-radius: 10px; padding: 16px 20px;
                     margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,.06); }}
  .stat-chip {{ display: inline-block; background: #e8f4fd; color: #1a6fa8;
                border-radius: 6px; padding: 4px 12px; margin: 4px 4px 4px 0;
                font-size: 13px; }}
  .stat-chip b {{ color: #0d4f8a; }}

  /* 表格 */
  .table-wrap {{ background: white; border-radius: 10px; overflow: hidden;
                 box-shadow: 0 2px 12px rgba(0,0,0,.08); }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  thead {{ background: #1a1a2e; color: white; }}
  th {{ padding: 12px 10px; text-align: left; font-weight: 500;
        white-space: nowrap; cursor: pointer; user-select: none; }}
  th:hover {{ background: #2a2a4e; }}
  td {{ padding: 10px; border-bottom: 1px solid #f0f0f0; }}
  tr:hover {{ background: #f8fbff; }}
  tr:last-child td {{ border-bottom: none; }}
  .code {{ font-family: 'Monaco', 'Menlo', monospace; color: #1a6fa8; font-size: 12px; }}
  .name {{ font-weight: 500; color: #222; }}
  .score {{ font-weight: 700; font-size: 14px; }}
  .strategies {{ font-size: 11px; color: #666; }}
  tbody tr:nth-child(even) {{ background: #fafbfc; }}
  tbody tr:nth-child(even):hover {{ background: #f0f6ff; }}

  /* 标题区 */
  h1 {{ font-size: 22px; margin-bottom: 6px; color: #1a1a2e; }}
  .meta {{ font-size: 12px; color: #999; margin-bottom: 20px; }}
  h2 {{ font-size: 15px; margin-bottom: 12px; color: #555; border-left: 3px solid #1a6fa8;
        padding-left: 8px; }}
</style>
</head>
<body>
<div class='container'>

  <h1>{title}</h1>
  <div class='meta'>生成时间: {timestamp} &nbsp;|&nbsp; 模式: <b>{mode}</b>
    &nbsp;|&nbsp; 策略: {strategies}</div>

  <div class='summary-bar'>
    <div class='card'>
      <div class='label'>最终命中</div>
      <div class='value'>{total_count}</div>
      <div class='sub'>只股票</div>
    </div>
    <div class='card'>
      <div class='label'>耗时</div>
      <div class='value'>{elapsed}s</div>
      <div class='sub'>分析完成</div>
    </div>
    <div class='card'>
      <div class='label'>显示</div>
      <div class='value'>{row_count}</div>
      <div class='sub'>条记录</div>
    </div>
  </div>

  <div class='strategy-stats'>
    <h2 style='display:inline-block;border:none;padding:0;margin-bottom:10px;'>
      各策略命中统计
    </h2>
    <br>{strategy_stats}
  </div>

  <div class='table-wrap'>
    <table id='stockTable'>
      <thead>
        <tr>
          <th>#</th>
          <th>代码</th>
          <th>名称</th>
          <th>行业</th>
          <th>评分</th>
          <th>命中策略</th>
        </tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>
  </div>

</div>
<script>
// 简单客户端排序
document.querySelectorAll('th').forEach((th, colIdx) => {{
  th.addEventListener('click', () => {{
    const tbl = document.getElementById('stockTable');
    const rows = Array.from(tbl.tBodies[0].rows);
    const dir = th.dataset.dir == 'asc' ? -1 : 1;
    th.dataset.dir = dir === 1 ? 'asc' : 'desc';
    rows.sort((a, b) => {{
      const A = a.cells[colIdx].innerText.trim();
      const B = b.cells[colIdx].innerText.trim();
      const A_num = parseFloat(A.replace(/[^0-9.-]/g,''));
      const B_num = parseFloat(B.replace(/[^0-9.-]/g,''));
      if (!isNaN(A_num) && !isNaN(B_num)) return (A_num - B_num) * dir;
      return A.localeCompare(B, 'zh') * dir;
    }});
    rows.forEach(r => tbl.tBodies[0].appendChild(r));
  }});
}});
</script>
</body>
</html>"""
