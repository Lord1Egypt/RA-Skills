#!/usr/bin/env python3
"""
WHOOP Chart Generator — produces self-contained HTML charts using Chart.js.

Usage:
  python3 chart.py --chart recovery --days 30
  python3 chart.py --chart dashboard --days 30 --output ~/whoop-dashboard.html
  python3 chart.py --chart hrv --days 90 --no-open
  python3 chart.py --chart sleep --days 14
  python3 chart.py --chart strain --days 21
"""

import argparse
import json
import math
import subprocess
import sys
import webbrowser
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
FETCH_SCRIPT = SCRIPT_DIR / "fetch.py"


def fetch(endpoint, days=30, start=None, end=None, limit=None):
    """Call fetch.py and return parsed JSON."""
    cmd = [sys.executable, str(FETCH_SCRIPT), endpoint]
    if limit is not None:
        cmd += ["--limit", str(limit)]
    elif days:
        end_dt = datetime.now(timezone.utc)
        start_dt = end_dt - timedelta(days=days)
        cmd += ["--start", start_dt.strftime("%Y-%m-%d")]
        cmd += ["--end", end_dt.strftime("%Y-%m-%d")]
        cmd += ["--limit", str(days + 5)]
    if start:
        cmd += ["--start", start]
    if end:
        cmd += ["--end", end]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def get_recovery_data(days):
    data = fetch("/recovery", days=days)
    records = data.get("records", [])
    out = []
    for r in records:
        score = r.get("score", {})
        hrv = score.get("hrv_rmssd_milli")
        recovery = score.get("recovery_score")
        rhr = score.get("resting_heart_rate")
        ts = r.get("created_at", "")
        if ts:
            date = ts[:10]
        else:
            continue
        out.append({"date": date, "recovery": recovery, "hrv": hrv, "rhr": rhr})
    out.sort(key=lambda x: x["date"])
    return out


def get_sleep_data(days):
    data = fetch("/activity/sleep", days=days)
    records = data.get("records", [])
    out = []
    for r in records:
        if r.get("nap"):
            continue
        score = r.get("score", {})
        stage_summary = score.get("stage_summary", {})
        total_in_bed = r.get("end", "")
        start_ts = r.get("start", "")
        end_ts = r.get("end", "")
        if not start_ts:
            continue
        date = start_ts[:10]

        def to_min(ms):
            return round((ms or 0) / 60000, 1)

        out.append({
            "date": date,
            "sleep_performance": score.get("sleep_performance_percentage"),
            "deep_min": to_min(stage_summary.get("total_slow_wave_sleep_time_milli")),
            "rem_min": to_min(stage_summary.get("total_rem_sleep_time_milli")),
            "light_min": to_min(stage_summary.get("total_light_sleep_time_milli")),
            "awake_min": to_min(stage_summary.get("total_awake_time_milli")),
        })
    out.sort(key=lambda x: x["date"])
    return out


def get_strain_data(days):
    data = fetch("/cycle", days=days)
    records = data.get("records", [])
    out = []
    for r in records:
        score = r.get("score", {})
        ts = r.get("created_at", "")
        if not ts:
            continue
        date = ts[:10]
        out.append({
            "date": date,
            "strain": score.get("strain"),
            "kilojoule": score.get("kilojoule"),
            "avg_hr": score.get("average_heart_rate"),
        })
    out.sort(key=lambda x: x["date"])
    return out


def rolling_avg(values, window=7):
    result = []
    for i, v in enumerate(values):
        window_vals = [x for x in values[max(0, i - window + 1):i + 1] if x is not None]
        result.append(round(sum(window_vals) / len(window_vals), 1) if window_vals else None)
    return result


def stat_cards(values, label, fmt=lambda x: str(x)):
    clean = [v for v in values if v is not None]
    if not clean:
        return {"avg": "N/A", "min": "N/A", "max": "N/A", "trend": "→"}
    avg = sum(clean) / len(clean)
    mn = min(clean)
    mx = max(clean)
    # trend: compare last 7 to first 7
    first7 = [v for v in clean[:7] if v is not None]
    last7 = [v for v in clean[-7:] if v is not None]
    if first7 and last7:
        delta = (sum(last7) / len(last7)) - (sum(first7) / len(first7))
        trend = "↑" if delta > 0.5 else ("↓" if delta < -0.5 else "→")
    else:
        trend = "→"
    return {"avg": fmt(avg), "min": fmt(mn), "max": fmt(mx), "trend": trend}


DARK_STYLE = """
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #0f1117;
    color: #e2e8f0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    padding: 24px;
  }
  h1 { font-size: 1.6rem; margin-bottom: 16px; color: #f8fafc; }
  h2 { font-size: 1.1rem; margin-bottom: 12px; color: #cbd5e1; font-weight: 600; }
  .chart-wrap { background: #1e2130; border-radius: 12px; padding: 20px; margin-bottom: 24px; }
  .stat-cards { display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }
  .card {
    background: #2a2f45;
    border-radius: 8px;
    padding: 10px 16px;
    flex: 1;
    min-width: 80px;
    text-align: center;
  }
  .card .label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }
  .card .value { font-size: 1.3rem; font-weight: 700; color: #f1f5f9; }
  .card .trend { font-size: 1.1rem; }
  .trend-up { color: #4ade80; }
  .trend-down { color: #f87171; }
  .trend-flat { color: #94a3b8; }
  .dashboard-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  canvas { max-height: 300px; }
  @media (max-width: 768px) { .dashboard-grid { grid-template-columns: 1fr; } }
</style>
"""

CHARTJS_CDN = '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'


def trend_class(t):
    return {"↑": "trend-up", "↓": "trend-down", "→": "trend-flat"}.get(t, "trend-flat")


def stat_cards_html(stats_dict):
    """Render stat cards HTML from dict of {label: stats_obj}."""
    cards = ""
    for label, s in stats_dict.items():
        tc = trend_class(s["trend"])
        cards += f"""
        <div class="card">
          <div class="label">{label}</div>
          <div class="value">{s['avg']}</div>
          <div class="trend {tc}">{s['trend']}</div>
          <div class="label">avg &bull; {s['min']}–{s['max']}</div>
        </div>"""
    return f'<div class="stat-cards">{cards}</div>'


def build_recovery_chart(recovery_data, canvas_id="recoveryChart"):
    labels = [r["date"][5:] for r in recovery_data]
    scores = [r["recovery"] for r in recovery_data]
    colors = []
    for s in scores:
        if s is None:
            colors.append("#4a5568")
        elif s >= 67:
            colors.append("#4ade80")
        elif s >= 34:
            colors.append("#facc15")
        else:
            colors.append("#f87171")

    stats = stat_cards_html({
        "Avg Recovery": stat_cards(scores, "Recovery", lambda x: f"{x:.0f}%"),
        "HRV": stat_cards([r["hrv"] for r in recovery_data], "HRV", lambda x: f"{x:.0f}ms"),
        "RHR": stat_cards([r["rhr"] for r in recovery_data], "RHR", lambda x: f"{x:.0f}bpm"),
    })

    chart_js = f"""
    new Chart(document.getElementById('{canvas_id}'), {{
      type: 'bar',
      data: {{
        labels: {json.dumps(labels)},
        datasets: [{{
          label: 'Recovery %',
          data: {json.dumps(scores)},
          backgroundColor: {json.dumps(colors)},
          borderRadius: 4,
        }}]
      }},
      options: {{
        responsive: true,
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{ callbacks: {{ label: ctx => ctx.raw + '%' }} }}
        }},
        scales: {{
          x: {{ grid: {{ color: '#2a2f45' }}, ticks: {{ color: '#94a3b8', maxTicksLimit: 10 }} }},
          y: {{ min: 0, max: 100, grid: {{ color: '#2a2f45' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }}
        }}
      }}
    }});"""
    return stats, f'<canvas id="{canvas_id}"></canvas>', chart_js


def build_sleep_chart(sleep_data, canvas_id="sleepChart"):
    labels = [r["date"][5:] for r in sleep_data]

    def safe(r, k):
        return r.get(k) or 0

    deep = [safe(r, "deep_min") for r in sleep_data]
    rem = [safe(r, "rem_min") for r in sleep_data]
    light = [safe(r, "light_min") for r in sleep_data]
    awake = [safe(r, "awake_min") for r in sleep_data]
    perf = [r.get("sleep_performance") for r in sleep_data]

    stats = stat_cards_html({
        "Sleep Perf": stat_cards(perf, "Perf", lambda x: f"{x:.0f}%"),
        "Deep (min)": stat_cards(deep, "Deep", lambda x: f"{x:.0f}"),
        "REM (min)": stat_cards(rem, "REM", lambda x: f"{x:.0f}"),
    })

    chart_js = f"""
    new Chart(document.getElementById('{canvas_id}'), {{
      type: 'bar',
      data: {{
        labels: {json.dumps(labels)},
        datasets: [
          {{ label: 'Deep', data: {json.dumps(deep)}, backgroundColor: '#6366f1', borderRadius: 2 }},
          {{ label: 'REM', data: {json.dumps(rem)}, backgroundColor: '#8b5cf6', borderRadius: 2 }},
          {{ label: 'Light', data: {json.dumps(light)}, backgroundColor: '#3b82f6', borderRadius: 2 }},
          {{ label: 'Awake', data: {json.dumps(awake)}, backgroundColor: '#475569', borderRadius: 2 }}
        ]
      }},
      options: {{
        responsive: true,
        plugins: {{
          legend: {{ labels: {{ color: '#94a3b8' }} }},
          tooltip: {{ callbacks: {{ label: ctx => ctx.dataset.label + ': ' + ctx.raw + ' min' }} }}
        }},
        scales: {{
          x: {{ stacked: true, grid: {{ color: '#2a2f45' }}, ticks: {{ color: '#94a3b8', maxTicksLimit: 10 }} }},
          y: {{ stacked: true, grid: {{ color: '#2a2f45' }}, ticks: {{ color: '#94a3b8', callback: v => v + 'm' }} }}
        }}
      }}
    }});"""
    return stats, f'<canvas id="{canvas_id}"></canvas>', chart_js


def build_hrv_chart(recovery_data, canvas_id="hrvChart"):
    labels = [r["date"][5:] for r in recovery_data]
    hrv_vals = [r["hrv"] for r in recovery_data]
    rolling = rolling_avg(hrv_vals, 7)

    stats = stat_cards_html({
        "HRV": stat_cards(hrv_vals, "HRV", lambda x: f"{x:.0f}ms"),
        "7d Avg": stat_cards(rolling, "7d Avg", lambda x: f"{x:.0f}ms"),
    })

    chart_js = f"""
    new Chart(document.getElementById('{canvas_id}'), {{
      type: 'line',
      data: {{
        labels: {json.dumps(labels)},
        datasets: [
          {{
            label: 'HRV (ms)',
            data: {json.dumps(hrv_vals)},
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56,189,248,0.1)',
            pointRadius: 3,
            tension: 0.3,
            fill: true,
          }},
          {{
            label: '7-day Avg',
            data: {json.dumps(rolling)},
            borderColor: '#f472b6',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.4,
            borderDash: [5, 5],
          }}
        ]
      }},
      options: {{
        responsive: true,
        plugins: {{
          legend: {{ labels: {{ color: '#94a3b8' }} }},
          tooltip: {{ callbacks: {{ label: ctx => ctx.dataset.label + ': ' + ctx.raw + 'ms' }} }}
        }},
        scales: {{
          x: {{ grid: {{ color: '#2a2f45' }}, ticks: {{ color: '#94a3b8', maxTicksLimit: 10 }} }},
          y: {{ grid: {{ color: '#2a2f45' }}, ticks: {{ color: '#94a3b8', callback: v => v + 'ms' }} }}
        }}
      }}
    }});"""
    return stats, f'<canvas id="{canvas_id}"></canvas>', chart_js


def build_strain_chart(strain_data, canvas_id="strainChart"):
    labels = [r["date"][5:] for r in strain_data]
    strains = [r.get("strain") for r in strain_data]
    # Convert kJ to kcal approximately (1 kJ ≈ 0.239 kcal)
    cals = [round((r.get("kilojoule") or 0) * 0.239) for r in strain_data]

    stats = stat_cards_html({
        "Strain": stat_cards(strains, "Strain", lambda x: f"{x:.1f}"),
        "Calories": stat_cards(cals, "Cal", lambda x: f"{x:.0f}"),
    })

    chart_js = f"""
    new Chart(document.getElementById('{canvas_id}'), {{
      type: 'bar',
      data: {{
        labels: {json.dumps(labels)},
        datasets: [
          {{
            label: 'Strain',
            data: {json.dumps(strains)},
            backgroundColor: 'rgba(251,146,60,0.85)',
            borderRadius: 4,
            yAxisID: 'y',
          }},
          {{
            label: 'Calories',
            data: {json.dumps(cals)},
            type: 'line',
            borderColor: '#e879f9',
            pointRadius: 2,
            tension: 0.3,
            yAxisID: 'y2',
          }}
        ]
      }},
      options: {{
        responsive: true,
        plugins: {{
          legend: {{ labels: {{ color: '#94a3b8' }} }}
        }},
        scales: {{
          x: {{ grid: {{ color: '#2a2f45' }}, ticks: {{ color: '#94a3b8', maxTicksLimit: 10 }} }},
          y: {{
            min: 0, max: 21,
            position: 'left',
            grid: {{ color: '#2a2f45' }},
            ticks: {{ color: '#94a3b8' }}
          }},
          y2: {{
            position: 'right',
            grid: {{ drawOnChartArea: false }},
            ticks: {{ color: '#e879f9' }}
          }}
        }}
      }}
    }});"""
    return stats, f'<canvas id="{canvas_id}"></canvas>', chart_js


def build_single_page(title, stats_html, canvas_html, chart_js):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>WHOOP — {title}</title>
  {DARK_STYLE}
</head>
<body>
  <h1>WHOOP — {title}</h1>
  <div class="chart-wrap">
    <h2>{title}</h2>
    {stats_html}
    {canvas_html}
  </div>
  {CHARTJS_CDN}
  <script>
    {chart_js}
  </script>
</body>
</html>"""


def build_dashboard_page(sections):
    """sections: list of (title, stats_html, canvas_html, chart_js)"""
    grid_items = ""
    all_js = ""
    for title, stats_html, canvas_html, chart_js in sections:
        grid_items += f"""
        <div class="chart-wrap">
          <h2>{title}</h2>
          {stats_html}
          {canvas_html}
        </div>"""
        all_js += chart_js + "\n"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>WHOOP Dashboard</title>
  {DARK_STYLE}
</head>
<body>
  <h1>WHOOP Dashboard</h1>
  <div class="dashboard-grid">
    {grid_items}
  </div>
  {CHARTJS_CDN}
  <script>
    {all_js}
  </script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="WHOOP HTML chart generator")
    parser.add_argument("--chart", required=True,
                        choices=["recovery", "sleep", "hrv", "strain", "dashboard"],
                        help="Chart type to generate")
    parser.add_argument("--days", type=int, default=30, help="Days of history to fetch")
    parser.add_argument("--output", help="Output HTML file path (default: /tmp/whoop-<chart>.html)")
    parser.add_argument("--no-open", action="store_true", help="Don't open in browser")
    args = parser.parse_args()

    output = Path(args.output).expanduser() if args.output else Path(f"/tmp/whoop-{args.chart}.html")
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Fetching {args.days} days of WHOOP data...", file=sys.stderr)

    chart = args.chart

    if chart == "recovery":
        data = get_recovery_data(args.days)
        if not data:
            print("ERROR: No recovery data returned. Check your token.", file=sys.stderr)
            sys.exit(1)
        stats_html, canvas_html, chart_js = build_recovery_chart(data)
        html = build_single_page("Recovery", stats_html, canvas_html, chart_js)

    elif chart == "sleep":
        data = get_sleep_data(args.days)
        if not data:
            print("ERROR: No sleep data returned.", file=sys.stderr)
            sys.exit(1)
        stats_html, canvas_html, chart_js = build_sleep_chart(data)
        html = build_single_page("Sleep Stages", stats_html, canvas_html, chart_js)

    elif chart == "hrv":
        data = get_recovery_data(args.days)
        if not data:
            print("ERROR: No recovery/HRV data returned.", file=sys.stderr)
            sys.exit(1)
        stats_html, canvas_html, chart_js = build_hrv_chart(data)
        html = build_single_page("HRV Trend", stats_html, canvas_html, chart_js)

    elif chart == "strain":
        data = get_strain_data(args.days)
        if not data:
            print("ERROR: No cycle/strain data returned.", file=sys.stderr)
            sys.exit(1)
        stats_html, canvas_html, chart_js = build_strain_chart(data)
        html = build_single_page("Daily Strain", stats_html, canvas_html, chart_js)

    elif chart == "dashboard":
        recovery_data = get_recovery_data(args.days)
        sleep_data = get_sleep_data(args.days)
        strain_data = get_strain_data(args.days)

        sections = []
        if recovery_data:
            sections.append(("Recovery", *build_recovery_chart(recovery_data, "recoveryChart")))
            sections.append(("HRV Trend", *build_hrv_chart(recovery_data, "hrvChart")))
        if sleep_data:
            sections.append(("Sleep Stages", *build_sleep_chart(sleep_data, "sleepChart")))
        if strain_data:
            sections.append(("Daily Strain", *build_strain_chart(strain_data, "strainChart")))

        if not sections:
            print("ERROR: No data returned for dashboard.", file=sys.stderr)
            sys.exit(1)

        html = build_dashboard_page(sections)

    output.write_text(html, encoding="utf-8")
    print(f"Chart saved: {output}", file=sys.stderr)

    if not args.no_open:
        webbrowser.open(f"file://{output.resolve()}")
        print("Opened in browser.", file=sys.stderr)

    # Always print the output path to stdout so the agent can attach it to chat
    print(str(output.resolve()))


if __name__ == "__main__":
    main()
