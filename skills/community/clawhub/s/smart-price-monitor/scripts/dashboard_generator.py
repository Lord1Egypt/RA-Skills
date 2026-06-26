#!/usr/bin/env python3
"""
Smart Price Monitor - Interactive HTML Dashboard Generator
Creates a self-contained HTML dashboard for visualizing price monitoring data.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(os.environ.get("PRICE_MONITOR_DATA", "./price-monitor-data"))


def load_all_data() -> dict:
    """Load all monitoring data for dashboard generation."""
    monitors_file = DATA_DIR / "monitors.json"
    if not monitors_file.exists():
        return {"monitors": [], "settings": {}}

    data = json.loads(monitors_file.read_text())
    history_dir = DATA_DIR / "history"

    for m in data["monitors"]:
        history_file = history_dir / f"{m['id']}.json"
        m["history"] = json.loads(history_file.read_text()) if history_file.exists() else []

    return data


def generate_dashboard(output_path: str = None) -> str:
    """Generate an interactive HTML dashboard."""
    data = load_all_data()

    # Prepare chart data for each monitor
    chart_datasets = []
    for m in data["monitors"]:
        if m.get("history"):
            points = [
                {"x": h["timestamp"], "y": h["price"]}
                for h in m["history"] if h.get("price")
            ]
            chart_datasets.append({
                "label": m["name"],
                "data": points
            })

    # Build summary cards data
    cards = []
    for m in data["monitors"]:
        hist = m.get("history", [])
        if hist:
            current = hist[-1].get("price", 0)
            prices = [h["price"] for h in hist if h.get("price")]
            avg = sum(prices) / len(prices) if prices else 0
            low = min(prices) if prices else 0
            high = max(prices) if prices else 0

            if len(hist) >= 2 and hist[-2].get("price"):
                change = current - hist[-2]["price"]
                change_pct = (change / hist[-2]["price"]) * 100
            else:
                change = 0
                change_pct = 0

            # Deal score
            score = max(0, min(100, int(((avg - current) / avg) * 200 + 50))) if avg else 50

            cards.append({
                "name": m["name"],
                "id": m["id"],
                "price": current,
                "change": change,
                "change_pct": change_pct,
                "low": low,
                "high": high,
                "avg": avg,
                "deal_score": score,
                "in_stock": hist[-1].get("in_stock", True),
                "data_points": len(prices),
                "source": m.get("source", "")
            })

    # Build product cards HTML separately to avoid f-string nesting issues
    cards_html = ""
    for c in sorted(cards, key=lambda x: x["deal_score"], reverse=True):
        change_class = "down" if c["change"] < 0 else ("up" if c["change"] > 0 else "flat")
        change_arrow = "\u25bc" if c["change"] < 0 else ("\u25b2" if c["change"] > 0 else "\u2014")
        stock_class = "in-stock" if c["in_stock"] else "out-of-stock"
        stock_text = "In Stock" if c["in_stock"] else "Out of Stock"
        ds = c["deal_score"]
        score_class = "score-hot" if ds >= 90 else ("score-good" if ds >= 70 else ("score-ok" if ds >= 50 else "score-meh"))
        cards_html += (
            f'<div class="product-card" data-score="{ds}" data-change="{c["change"]}" '
            f'data-stock="{"in" if c["in_stock"] else "out"}">\n'
            f'  <div class="name">{c["name"]}</div>\n'
            f'  <div class="price-row">\n'
            f'    <span class="price">${c["price"]:,.2f}</span>\n'
            f'    <span class="change {change_class}">{change_arrow} {abs(c["change_pct"]):.1f}%</span>\n'
            f'    <span class="stock-badge {stock_class}">{stock_text}</span>\n'
            f'  </div>\n'
            f'  <div><span class="deal-score {score_class}">Deal Score: {ds}/100</span></div>\n'
            f'  <div class="meta">\n'
            f'    <span>Low: ${c["low"]:,.2f}</span>\n'
            f'    <span>Avg: ${c["avg"]:,.2f}</span>\n'
            f'    <span>High: ${c["high"]:,.2f}</span>\n'
            f'  </div>\n'
            f'</div>\n'
        )

    no_data_html = "<div class='no-data'><h2>No monitors configured yet</h2><p>Add products to start tracking prices.</p></div>" if not cards else ""
    chart_section = ""
    if chart_datasets:
        chart_section = '<div class="chart-container"><h2>Price History</h2><canvas id="priceChart" height="300"></canvas></div>'

    best_score = max((c["deal_score"] for c in cards), default=0)
    drops_today = sum(1 for c in cards if c["change"] < 0)
    total_points = sum(c["data_points"] for c in cards)
    ts_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    chart_json = json.dumps(chart_datasets)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smart Price Monitor Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
       background: #0f172a; color: #e2e8f0; padding: 24px; }}
.header {{ text-align: center; margin-bottom: 32px; }}
.header h1 {{ font-size: 28px; font-weight: 700; color: #f8fafc;
              background: linear-gradient(135deg, #38bdf8, #818cf8);
              -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.header p {{ color: #94a3b8; margin-top: 8px; }}
.stats-row {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}
.stat-card {{ background: #1e293b; border-radius: 12px; padding: 20px; flex: 1; min-width: 200px;
              border: 1px solid #334155; }}
.stat-card .label {{ color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }}
.stat-card .value {{ font-size: 28px; font-weight: 700; margin-top: 8px; }}
.cards-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
               gap: 16px; margin-bottom: 32px; }}
.product-card {{ background: #1e293b; border-radius: 12px; padding: 20px;
                 border: 1px solid #334155; transition: border-color 0.2s; }}
.product-card:hover {{ border-color: #38bdf8; }}
.product-card .name {{ font-size: 16px; font-weight: 600; margin-bottom: 12px;
                       white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.product-card .price-row {{ display: flex; align-items: baseline; gap: 12px; margin-bottom: 8px; }}
.product-card .price {{ font-size: 24px; font-weight: 700; }}
.product-card .change {{ font-size: 14px; font-weight: 600; padding: 2px 8px;
                         border-radius: 4px; }}
.change.up {{ background: #7f1d1d; color: #fca5a5; }}
.change.down {{ background: #14532d; color: #86efac; }}
.change.flat {{ background: #1e293b; color: #94a3b8; }}
.deal-score {{ display: inline-block; padding: 4px 10px; border-radius: 20px;
               font-size: 13px; font-weight: 600; }}
.score-hot {{ background: #7f1d1d; color: #fca5a5; }}
.score-good {{ background: #14532d; color: #86efac; }}
.score-ok {{ background: #422006; color: #fde68a; }}
.score-meh {{ background: #1e293b; color: #94a3b8; }}
.meta {{ display: flex; gap: 16px; margin-top: 12px; color: #64748b; font-size: 13px; }}
.chart-container {{ background: #1e293b; border-radius: 12px; padding: 24px;
                    border: 1px solid #334155; margin-bottom: 24px; }}
.chart-container h2 {{ margin-bottom: 16px; font-size: 18px; }}
.no-data {{ text-align: center; padding: 60px; color: #64748b; }}
.stock-badge {{ font-size: 12px; padding: 2px 8px; border-radius: 4px; }}
.in-stock {{ background: #14532d; color: #86efac; }}
.out-of-stock {{ background: #7f1d1d; color: #fca5a5; }}
.filter-bar {{ display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; }}
.filter-btn {{ padding: 8px 16px; border-radius: 8px; border: 1px solid #334155;
               background: #1e293b; color: #e2e8f0; cursor: pointer; font-size: 14px; }}
.filter-btn.active {{ background: #38bdf8; color: #0f172a; border-color: #38bdf8; }}
</style>
</head>
<body>
<div class="header">
  <h1>Smart Price Monitor</h1>
  <p>Last updated: {ts_str}</p>
</div>

<div class="stats-row">
  <div class="stat-card">
    <div class="label">Active Monitors</div>
    <div class="value" style="color:#38bdf8">{len(cards):d}</div>
  </div>
  <div class="stat-card">
    <div class="label">Best Deal Score</div>
    <div class="value" style="color:#86efac">{best_score}/100</div>
  </div>
  <div class="stat-card">
    <div class="label">Price Drops Today</div>
    <div class="value" style="color:#fde68a">{drops_today}</div>
  </div>
  <div class="stat-card">
    <div class="label">Total Data Points</div>
    <div class="value">{total_points}</div>
  </div>
</div>

<div class="filter-bar">
  <button class="filter-btn active" onclick="filterCards('all')">All</button>
  <button class="filter-btn" onclick="filterCards('deals')">Best Deals</button>
  <button class="filter-btn" onclick="filterCards('drops')">Price Drops</button>
  <button class="filter-btn" onclick="filterCards('oos')">Out of Stock</button>
</div>

{no_data_html}

<div class="cards-grid" id="cardsGrid">
{cards_html}
</div>

{chart_section}

<script>
const chartData = {chart_json};

if (chartData.length > 0) {{
  const colors = ['#38bdf8', '#818cf8', '#f472b6', '#fbbf24', '#34d399',
                  '#fb923c', '#a78bfa', '#22d3ee', '#f87171', '#a3e635'];
  const ctx = document.getElementById('priceChart').getContext('2d');
  new Chart(ctx, {{
    type: 'line',
    data: {{
      datasets: chartData.map((ds, i) => ({{
        label: ds.label,
        data: ds.data,
        borderColor: colors[i % colors.length],
        backgroundColor: colors[i % colors.length] + '20',
        fill: true,
        tension: 0.3,
        pointRadius: 3
      }}))
    }},
    options: {{
      responsive: true,
      scales: {{
        x: {{ type: 'category', grid: {{ color: '#1e293b' }},
              ticks: {{ color: '#64748b' }} }},
        y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#64748b',
              callback: v => '$' + v.toLocaleString() }} }}
      }},
      plugins: {{
        legend: {{ labels: {{ color: '#e2e8f0' }} }},
        tooltip: {{ callbacks: {{
          label: ctx => ctx.dataset.label + ': $' + ctx.parsed.y.toLocaleString()
        }} }}
      }}
    }}
  }});
}}

function filterCards(type) {{
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  document.querySelectorAll('.product-card').forEach(card => {{
    const show = type === 'all'
      || (type === 'deals' && parseInt(card.dataset.score) >= 70)
      || (type === 'drops' && parseFloat(card.dataset.change) < 0)
      || (type === 'oos' && card.dataset.stock === 'out');
    card.style.display = show ? '' : 'none';
  }});
}}
</script>
</body>
</html>"""

    if output_path:
        Path(output_path).write_text(html)
        print(f"Dashboard saved to: {output_path}")
    else:
        output = DATA_DIR / "reports" / f"dashboard-{datetime.now().strftime('%Y-%m-%d')}.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(html)
        print(f"Dashboard saved to: {output}")

    return html


if __name__ == "__main__":
    import sys
    output = sys.argv[1] if len(sys.argv) > 1 else None
    generate_dashboard(output)
