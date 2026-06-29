"""
round-robin-allocator  |  HTML 可视化生成器
============================================
生成一个完全自包含的 HTML 文件：
  - 分配明细热力表格（按重复频次着色）
  - 各轮次选项分布柱状图（Chart.js，内联）
  - 覆盖率分布直方图
  - 基本参数摘要卡片

无第三方 Python 依赖，Chart.js 通过 CDN 加载（离线时图表不显示，表格正常）。
"""

from __future__ import annotations
from pathlib import Path
import json


def _build_color_scale_css() -> str:
    """生成热力色阶：低→高 = 浅蓝→深橙红"""
    return ""


def _cell_color(val: float, alpha: float = 0.85) -> str:
    """
    val ∈ [0, 1]，返回 CSS rgba 颜色字符串。
    0 → 淡米白，1 → 深橙红
    """
    # 插值：淡黄 (#FFF8DC) → 橙 (#FF8C00) → 深红 (#8B0000)
    if val <= 0:
        return "rgba(255,248,220,0.4)"
    elif val <= 0.5:
        t = val * 2
        r = int(255)
        g = int(248 - t * (248 - 140))
        b = int(220 - t * 220)
    else:
        t = (val - 0.5) * 2
        r = int(255 - t * (255 - 139))
        g = int(140 - t * 140)
        b = 0
    a = alpha
    return f"rgba({r},{g},{b},{a:.2f})"


def _text_color(val: float) -> str:
    return "#3E2723" if val < 0.55 else "#FFF8E1"


def render_html(
    results: list[dict],
    stats: dict,
    params: dict,
    outpath: Path,
    labels: dict | None = None,
) -> None:
    if labels is None:
        labels = {}
    obj_name  = labels.get("obj",    "对象")
    slot_name = labels.get("slot",   "轮次")
    opt_name  = labels.get("option", "选项")

    N = params["N"]
    T = params["T"]
    K = params["K"]
    ratios = params["ratios"]

    # ── 预计算热力值 ──
    period_dist = stats["period_dist"]
    # 全局最大频次
    max_freq = max(
        (cnt for t_dist in period_dist.values() for cnt in t_dist.values()),
        default=1,
    ) or 1

    # ── 构建表格行 HTML ──
    rows_html = []
    for obj in results:
        cov = obj["coverage"]
        cov_color = _cell_color(cov)
        cov_text  = _text_color(cov)
        row = f'<tr><td class="id-cell">{obj["id"]}</td>'
        for t, opt in enumerate(obj["slots"]):
            freq = period_dist[t].get(opt, 0)
            val  = freq / max_freq
            bg   = _cell_color(val)
            tc   = _text_color(val)
            row += (f'<td style="background:{bg};color:{tc}" '
                    f'title="{slot_name}{t+1}：{opt_name}{opt}（此轮{freq}人选）">'
                    f'{opt_name}{opt}</td>')
        row += (f'<td style="background:{cov_color};color:{cov_text}">'
                f'{cov:.0%}</td></tr>')
        rows_html.append(row)

    # ── Chart.js 数据 ──
    chart_labels_slots = [f"{slot_name}{t+1}" for t in range(T)]
    chart_datasets = []
    colors = [
        "#4E79A7", "#F28E2B", "#E15759", "#76B7B2",
        "#59A14F", "#EDC948", "#B07AA1", "#FF9DA7",
        "#9C755F", "#BAB0AC",
    ]
    for k in range(1, K + 1):
        data = [period_dist[t].get(k, 0) for t in range(T)]
        chart_datasets.append({
            "label": f"{opt_name}{k}",
            "data": data,
            "backgroundColor": colors[(k - 1) % len(colors)],
        })

    # 覆盖率分布（直方图分箱）
    coverages = [obj["coverage"] for obj in results]
    bins = [0, 0.25, 0.5, 0.75, 1.0, 1.01]
    bin_labels = ["0–25%", "25–50%", "50–75%", "75–99%", "100%"]
    bin_counts = [0] * 5
    for c in coverages:
        for i, b in enumerate(bins[:-1]):
            if b <= c < bins[i + 1]:
                bin_counts[i] += 1
                break

    chart_data_json  = json.dumps(chart_datasets,   ensure_ascii=False)
    slot_labels_json = json.dumps(chart_labels_slots, ensure_ascii=False)
    cov_counts_json  = json.dumps(bin_counts)
    cov_labels_json  = json.dumps(bin_labels)

    # ── 3D 散点图数据：XYZ 三轴分配空间映射 ──
    # x=对象ID, y=方案编号, z=轮次, color=该对象的覆盖率
    trace_x, trace_y, trace_z, trace_c, trace_t = [], [], [], [], []
    for obj in results:
        cov = obj["coverage"]
        for t, opt in enumerate(obj["slots"]):
            trace_x.append(obj["id"])
            trace_y.append(opt)
            trace_z.append(t + 1)
            trace_c.append(cov)
            trace_t.append(f"对象{obj['id']} 方案{opt} 轮次{t+1}")
    trace3d_json = json.dumps({
        "x": trace_x, "y": trace_y, "z": trace_z,
        "c": trace_c, "t": trace_t,
    }, ensure_ascii=False)

    # ── 参数摘要卡片 ──
    ratio_str = " : ".join(str(int(r) if r == int(r) else r) for r in ratios)

    # ── 完整 HTML ──
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>均匀轮转分配结果</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/plotly.js@2.35.2/dist/plotly.min.js"></script>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    background: #F5F6FA;
    color: #1A1A2E;
    padding: 24px;
  }}
  h1 {{ font-size: 1.6rem; margin-bottom: 6px; color: #2C3E50; }}
  .subtitle {{ color: #7F8C8D; margin-bottom: 24px; font-size: 0.9rem; }}

  /* 摘要卡片 */
  .summary {{
    display: flex; flex-wrap: wrap; gap: 12px;
    margin-bottom: 28px;
  }}
  .card {{
    background: white;
    border-radius: 10px;
    padding: 14px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,.06);
    min-width: 120px;
    text-align: center;
  }}
  .card .val {{ font-size: 1.8rem; font-weight: 700; color: #E67E22; }}
  .card .lbl {{ font-size: 0.78rem; color: #95A5A6; margin-top: 4px; }}

  /* 分页表格 */
  .table-section {{ background: white; border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,.07); padding: 20px; margin-bottom: 28px; }}
  .table-section h2 {{ font-size: 1.1rem; margin-bottom: 14px; color: #2C3E50; }}
  .tbl-wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; }}
  th {{
    background: #FFF3E0; color: #6D4C41;
    padding: 8px 10px; font-weight: 600;
    border-bottom: 2px solid #FFCC80;
  }}
  td {{ padding: 7px 10px; text-align: center; border-bottom: 1px solid #F0F0F0; }}
  tr:hover td {{ filter: brightness(0.95); }}
  .id-cell {{ font-weight: 600; color: #5D6D7E; background: #FAFAFA; }}

  /* 分页控件 */
  .pagination {{ display:flex; align-items:center; justify-content:center; gap:10px; margin-top:14px; }}
  .pagination button {{
    background: #E67E22; color: white; border: none;
    border-radius: 6px; padding: 6px 16px; cursor: pointer; font-size: 0.9rem;
  }}
  .pagination button:disabled {{ background: #BDC3C7; cursor: default; }}
  .pagination span {{ font-size: 0.88rem; color: #7F8C8D; }}

  /* 搜索框 */
  .search-bar {{ margin-bottom: 12px; }}
  .search-bar input {{
    padding: 7px 12px; border: 1px solid #DDD; border-radius: 6px;
    width: 220px; font-size: 0.88rem;
  }}

  /* 图表区域 */
  .charts {{ display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 28px; }}
  @media (max-width: 700px) {{ .charts {{ grid-template-columns: 1fr; }} }}
  .chart-card {{
    background: white; border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,.07); padding: 20px;
  }}
  .chart-card h2 {{ font-size: 1.05rem; margin-bottom: 14px; color: #2C3E50; }}
  canvas {{ max-height: 280px; }}

  /* 颜色图例 */
  .legend {{ display:flex; align-items:center; gap:8px; font-size:0.8rem; color:#7F8C8D; margin-top:10px; }}
  .legend-bar {{
    height: 14px; width: 160px; border-radius: 3px;
    background: linear-gradient(to right,
      rgba(255,248,220,0.4), rgba(255,140,0,0.85), rgba(139,0,0,0.85));
  }}
  footer {{ text-align:center; color:#BDC3C7; font-size:0.78rem; margin-top:10px; }}
</style>
</head>
<body>

<h1>均匀轮转分配结果</h1>
<p class="subtitle">均匀轮转分配 · 贪心算法 + 迭代优化</p>

<!-- 摘要卡片 -->
<div class="summary">
  <div class="card"><div class="val">{N}</div><div class="lbl">{obj_name}数量</div></div>
  <div class="card"><div class="val">{T}</div><div class="lbl">{slot_name}数量</div></div>
  <div class="card"><div class="val">{K}</div><div class="lbl">{opt_name}数量</div></div>
  <div class="card"><div class="val">{ratio_str}</div><div class="lbl">分配比例</div></div>
  <div class="card"><div class="val">{stats['avg_coverage']:.1%}</div><div class="lbl">平均覆盖率</div></div>
  <div class="card"><div class="val">{stats['full_coverage']}</div><div class="lbl">全覆盖{obj_name}数</div></div>
</div>

<!-- 分配明细表 -->
<div class="table-section">
  <h2>📋 分配明细（热力着色按轮次频次）</h2>
  <div class="search-bar">
    <input id="searchInput" type="text" placeholder="搜索 {obj_name}ID…" oninput="filterTable()">
  </div>
  <div class="tbl-wrap">
    <table id="mainTable">
      <thead>
        <tr>
          <th>{obj_name}ID</th>
          {"".join(f"<th>{slot_name}{t+1}</th>" for t in range(T))}
          <th>覆盖率</th>
        </tr>
      </thead>
      <tbody id="tableBody">
        {"".join(rows_html)}
      </tbody>
    </table>
  </div>
  <div class="pagination">
    <button id="prevBtn" onclick="changePage(-1)" disabled>&#8249; 上一页</button>
    <span id="pageInfo"></span>
    <button id="nextBtn" onclick="changePage(1)">下一页 &#8250;</button>
  </div>
  <div class="legend">
    <span>频次低</span>
    <div class="legend-bar"></div>
    <span>频次高</span>
  </div>
</div>

<!-- 图表区域 -->
<div class="charts">
  <div class="chart-card">
    <h2>{slot_name}选项分布</h2>
    <canvas id="distChart"></canvas>
  </div>
  <div class="chart-card">
    <h2>覆盖率分布</h2>
    <canvas id="covChart"></canvas>
  </div>
</div>

<!-- 3D 空间映射散点图 -->
<div class="chart-card" style="margin-bottom:28px;">
  <h2>分配空间映射（XYZ三轴）</h2>
  <p style="font-size:0.82rem;color:#7F8C8D;margin-bottom:12px;">
    X=对象ID, Y=方案编号, Z=轮次, 颜色=覆盖率。
    可拖拽旋转查看分配的三维空间分布。同一X-Y-Z坐标若有重叠点表示同一方案在某对象中多次出现。
  </p>
  <div id="scatter3d" style="height:500px;"></div>
</div>

<footer>由「均匀轮转分配工具」生成 · 纯静态 HTML，无需服务器</footer>

<script>
// ── 分页逻辑 ──
const PAGE_SIZE = 15;
let allRows = [];
let filteredRows = [];
let currentPage = 0;

function initPagination() {{
  allRows = Array.from(document.querySelectorAll('#tableBody tr'));
  filteredRows = [...allRows];
  renderPage(0);
}}

function renderPage(page) {{
  currentPage = page;
  const total = Math.ceil(filteredRows.length / PAGE_SIZE) || 1;
  allRows.forEach(r => r.style.display = 'none');
  const start = page * PAGE_SIZE;
  filteredRows.slice(start, start + PAGE_SIZE).forEach(r => r.style.display = '');
  document.getElementById('pageInfo').textContent =
    `第 ${{page+1}} / ${{total}} 页（共 ${{filteredRows.length}} 条）`;
  document.getElementById('prevBtn').disabled = page === 0;
  document.getElementById('nextBtn').disabled = page >= total - 1;
}}

function changePage(delta) {{
  const total = Math.ceil(filteredRows.length / PAGE_SIZE) || 1;
  const np = Math.max(0, Math.min(currentPage + delta, total - 1));
  renderPage(np);
}}

function filterTable() {{
  const q = document.getElementById('searchInput').value.trim().toLowerCase();
  filteredRows = allRows.filter(r => r.cells[0].textContent.toLowerCase().includes(q));
  renderPage(0);
}}

document.addEventListener('DOMContentLoaded', initPagination);

// ── Chart.js 图表 ──
const slotLabels  = {slot_labels_json};
const datasets    = {chart_data_json};
const covCounts   = {cov_counts_json};
const covLabels   = {cov_labels_json};

// 分布柱状图
new Chart(document.getElementById('distChart'), {{
  type: 'bar',
  data: {{ labels: slotLabels, datasets: datasets }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 12 }} }} }},
    scales: {{
      x: {{ stacked: false }},
      y: {{ beginAtZero: true, title: {{ display: true, text: '数量' }} }}
    }}
  }}
}});

// 覆盖率直方图
new Chart(document.getElementById('covChart'), {{
  type: 'bar',
  data: {{
    labels: covLabels,
    datasets: [{{
      label: '{obj_name}数',
      data: covCounts,
      backgroundColor: ['#E74C3C','#E67E22','#F1C40F','#2ECC71','#27AE60'],
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      y: {{ beginAtZero: true, title: {{ display: true, text: '{obj_name}数' }} }}
    }}
  }}
}});

// ── 3D 散点图（Plotly） ──
const d3 = {trace3d_json};
Plotly.newPlot('scatter3d', [{{
  x: d3.x, y: d3.y, z: d3.z,
  mode: 'markers',
  type: 'scatter3d',
  text: d3.t,
  hoverinfo: 'text',
  marker: {{
    size: 3,
    color: d3.c,
    colorscale: [['0.0','#FFF8DC'],['0.5','#FF8C00'],['1.0','#8B0000']],
    cmin: 0, cmax: 1,
    colorbar: {{title: '覆盖率', len: 0.6, x: 0.85}},
    line: {{width: 0}}
  }}
}}], {{
  margin: {{l:40, r:40, b:40, t:20}},
  scene: {{
    xaxis: {{title: '{obj_name}ID', dtick: Math.max(1, Math.floor({N}/10))}},
    yaxis: {{title: '{opt_name}编号', dtick: 1}},
    zaxis: {{title: '{slot_name}', dtick: 1}}
  }},
  paper_bgcolor: '#F5F6FA',
  plot_bgcolor: '#F5F6FA'
}});
</script>
</body>
</html>
"""

    outpath.write_text(html, encoding="utf-8")
    print(f"  🌐 HTML   → {outpath}")
