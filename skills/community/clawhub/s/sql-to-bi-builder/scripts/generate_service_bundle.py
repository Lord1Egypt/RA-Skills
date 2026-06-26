#!/usr/bin/env python3.11
"""Generate backend and frontend services from pipeline outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

BACKEND_APP = '''from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

app = FastAPI(title="SQL2BI Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_json(name: str) -> dict[str, Any]:
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing data file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_state() -> dict[str, Any]:
    dashboard = load_json("dashboard.json")
    query_catalog = load_json("query_catalog.json")
    semantic_catalog = load_json("semantic_catalog.json")

    page = (dashboard.get("pages") or [{}])[0]
    widgets = page.get("widgets", [])
    widget_by_query = {w.get("query_id"): w for w in widgets}

    queries = query_catalog.get("queries", [])
    query_by_id = {q.get("id"): q for q in queries}

    semantic_by_id = {q.get("id"): q for q in semantic_catalog.get("queries", [])}

    return {
        "dashboard": dashboard,
        "page": page,
        "widgets": widgets,
        "widget_by_query": widget_by_query,
        "query_by_id": query_by_id,
        "semantic_by_id": semantic_by_id,
    }


def stable_seed(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)


def build_rows(query_id: str, widget: dict[str, Any], semantic: dict[str, Any], filters: dict[str, str]) -> dict[str, Any]:
    dim_candidates = (semantic.get("time_fields") or []) + (semantic.get("dimensions") or [])
    metric_candidates = semantic.get("metrics") or ["value"]

    dimension = dim_candidates[0] if dim_candidates else "category"
    metric_primary = metric_candidates[0]
    metric_secondary = metric_candidates[1] if len(metric_candidates) > 1 else f"{metric_primary}_2"

    filter_text = "|".join(f"{k}={v}" for k, v in sorted(filters.items()))
    seed = stable_seed(f"{query_id}|{filter_text}")

    base = 80 + (seed % 17)
    boost = 1 + min(len(filter_text), 32) / 120

    labels = []
    if semantic.get("time_fields"):
        labels = [f"2024-01-{str(i).zfill(2)}" for i in range(1, 13)]
    else:
        labels = [f"{dimension}_{i}" for i in range(1, 13)]

    rows = []
    for i, label in enumerate(labels):
        v1 = int((base + ((seed + i * 13) % 40) + i * 2) * boost)
        v2 = int((base * 0.7 + ((seed + i * 7) % 30) + i) * boost)
        rows.append({
            dimension: label,
            metric_primary: v1,
            metric_secondary: v2,
        })

    return {
        "dimension": dimension,
        "metrics": [metric_primary, metric_secondary],
        "rows": rows,
        "chart": (widget or {}).get("chart", "table"),
    }


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.get("/api/dashboard")
def get_dashboard() -> dict[str, Any]:
    state = load_state()
    return state["dashboard"]


@app.get("/api/filters")
def get_filters() -> dict[str, Any]:
    state = load_state()
    page = state["page"]
    return {
        "global_filters": page.get("global_filters", []),
        "widget_filters": {
            w.get("query_id"): w.get("dsl_filters", []) for w in state["widgets"]
        },
    }


@app.get("/api/query/{query_id}/data")
def get_query_data(query_id: str, request: Request) -> dict[str, Any]:
    state = load_state()
    widget = state["widget_by_query"].get(query_id)
    if not widget:
        raise HTTPException(status_code=404, detail=f"Unknown query_id: {query_id}")

    semantic = state["semantic_by_id"].get(query_id, {})

    filters = {k: v for k, v in request.query_params.items() if v is not None and str(v).strip()}
    data = build_rows(query_id, widget, semantic, filters)

    return {
        "query_id": query_id,
        "filters": filters,
        "chart": data["chart"],
        "dimension": data["dimension"],
        "metrics": data["metrics"],
        "rows": data["rows"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
'''

FRONTEND_INDEX = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SQL2BI Frontend</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <header class="topbar">
    <div class="brand">SQL2BI Frontend Service</div>
    <div class="backend-config">
      <label for="backend-url">Backend:</label>
      <input id="backend-url" value="http://127.0.0.1:8000" />
      <button id="apply-backend">Apply</button>
      <button id="refresh">Refresh</button>
    </div>
  </header>

  <div class="layout">
    <aside class="filters-panel">
      <h2>Global Filters</h2>
      <div id="global-filters"></div>
    </aside>
    <main>
      <h1 id="dashboard-title">Loading...</h1>
      <div id="grid" class="grid"></div>
    </main>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <script src="app.js"></script>
</body>
</html>
'''

FRONTEND_STYLE = ''':root {
  --bg: #f5f6f8;
  --panel: #ffffff;
  --line: #e6e8ec;
  --text: #101828;
  --muted: #667085;
  --brand: #2f6fed;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: "Source Sans 3", "Noto Sans SC", sans-serif;
}
.topbar {
  height: 52px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 12px;
  border-bottom: 1px solid var(--line);
  background: var(--panel);
}
.brand { font-weight: 700; }
.backend-config {
  display: flex;
  align-items: center;
  gap: 8px;
}
.backend-config input {
  min-width: 220px;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 6px 8px;
}
.backend-config button {
  border: 1px solid var(--line);
  border-radius: 6px;
  background: #fff;
  padding: 6px 10px;
  cursor: pointer;
}
.layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: calc(100vh - 52px);
}
.filters-panel {
  border-right: 1px solid var(--line);
  background: var(--panel);
  padding: 12px;
}
.filters-panel h2 {
  margin: 0 0 10px;
  font-size: 13px;
  text-transform: uppercase;
  color: var(--muted);
}
.filter-item { margin-bottom: 10px; }
.filter-item label {
  display: block;
  font-size: 12px;
  margin-bottom: 4px;
  font-weight: 700;
}
.filter-item input, .filter-item select {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 6px 8px;
}
main { padding: 12px; }
#dashboard-title {
  margin: 0 0 10px;
  font-size: 20px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  grid-auto-rows: 64px;
  gap: 10px;
}
.widget {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 8px;
  display: grid;
  grid-template-rows: auto 1fr;
  gap: 8px;
}
.widget-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.widget-title { font-weight: 700; font-size: 13px; }
.widget-type { color: var(--muted); font-size: 11px; text-transform: uppercase; }
.chart {
  width: 100%;
  height: 100%;
  min-height: 140px;
}
.table-wrap {
  overflow: auto;
  border: 1px solid var(--line);
  border-radius: 6px;
}
.table-wrap table {
  width: 100%;
  border-collapse: collapse;
}
.table-wrap th, .table-wrap td {
  border: 1px solid var(--line);
  padding: 6px;
  font-size: 11px;
  text-align: left;
}
@media (max-width: 960px) {
  .layout { grid-template-columns: 1fr; }
  .filters-panel { border-right: none; border-bottom: 1px solid var(--line); }
}
'''

FRONTEND_APP = '''(function () {
  const state = {
    backend: localStorage.getItem('sql2bi_backend') || 'http://127.0.0.1:8000',
    dashboard: null,
    globalFilters: {},
    charts: {},
  };

  function $(id) {
    return document.getElementById(id);
  }

  function unique(items) {
    return [...new Set((items || []).filter(Boolean))];
  }

  function qsFromFilters(filters) {
    const p = new URLSearchParams();
    Object.entries(filters || {}).forEach(([k, v]) => {
      if (v !== null && v !== undefined && String(v).trim()) p.set(k, String(v));
    });
    return p.toString();
  }

  async function fetchJson(path) {
    const res = await fetch(`${state.backend}${path}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  function renderGlobalFilters(page) {
    const root = $('global-filters');
    root.innerHTML = '';
    const defs = (page.global_filters && page.global_filters.length)
      ? page.global_filters
      : unique((page.widgets || []).flatMap((w) => w.filters || [])).map((f) => ({ field: f, suggested_widget: 'select' }));

    if (defs.length === 0) {
      root.innerHTML = '<div>No filters</div>';
      return;
    }

    defs.forEach((f) => {
      const wrap = document.createElement('div');
      wrap.className = 'filter-item';
      const label = document.createElement('label');
      label.textContent = f.field;
      wrap.appendChild(label);

      if (f.suggested_widget === 'date_range' || f.suggested_widget === 'number_range') {
        const from = document.createElement('input');
        from.placeholder = 'from';
        const to = document.createElement('input');
        to.placeholder = 'to';
        from.addEventListener('change', () => {
          state.globalFilters[f.field] = `${from.value || ''}..${to.value || ''}`;
          renderWidgets(page);
        });
        to.addEventListener('change', () => {
          state.globalFilters[f.field] = `${from.value || ''}..${to.value || ''}`;
          renderWidgets(page);
        });
        wrap.appendChild(from);
        wrap.appendChild(to);
      } else {
        const input = document.createElement('input');
        input.placeholder = f.suggested_widget || 'value';
        input.addEventListener('change', () => {
          state.globalFilters[f.field] = input.value;
          renderWidgets(page);
        });
        wrap.appendChild(input);
      }

      root.appendChild(wrap);
    });
  }

  function tableHtml(rows) {
    const cols = Object.keys(rows[0] || {});
    let html = '<div class="table-wrap"><table><thead><tr>';
    cols.forEach((c) => { html += `<th>${c}</th>`; });
    html += '</tr></thead><tbody>';
    rows.slice(0, 8).forEach((r) => {
      html += '<tr>';
      cols.forEach((c) => { html += `<td>${r[c]}</td>`; });
      html += '</tr>';
    });
    html += '</tbody></table></div>';
    return html;
  }

  function makeOption(payload) {
    const chart = (payload.chart || 'table').toLowerCase();
    const x = payload.rows.map((r) => r[payload.dimension]);
    const m1 = payload.metrics[0];
    const m2 = payload.metrics[1];
    const y1 = payload.rows.map((r) => r[m1]);
    const y2 = payload.rows.map((r) => r[m2]);

    if (chart === 'line') {
      return {
        tooltip: { trigger: 'axis' },
        grid: { left: 36, right: 12, top: 20, bottom: 24 },
        xAxis: { type: 'category', data: x },
        yAxis: { type: 'value' },
        series: [{ type: 'line', smooth: true, data: y1 }],
      };
    }

    if (chart === 'bar') {
      return {
        tooltip: { trigger: 'axis' },
        grid: { left: 36, right: 12, top: 20, bottom: 24 },
        xAxis: { type: 'category', data: x },
        yAxis: { type: 'value' },
        series: [{ type: 'bar', data: y1 }],
      };
    }

    if (chart === 'grouped_bar') {
      return {
        tooltip: { trigger: 'axis' },
        legend: { top: 0 },
        grid: { left: 36, right: 12, top: 24, bottom: 24 },
        xAxis: { type: 'category', data: x },
        yAxis: { type: 'value' },
        series: [
          { name: m1, type: 'bar', data: y1 },
          { name: m2, type: 'bar', data: y2 },
        ],
      };
    }

    if (chart === 'kpi') {
      const total = y1.reduce((a, b) => a + b, 0);
      return {
        xAxis: { show: false, type: 'value' },
        yAxis: { show: false, type: 'value' },
        series: [{ type: 'bar', data: [total], barWidth: 80 }],
        graphic: [
          {
            type: 'text',
            left: 'center',
            top: '45%',
            style: { text: String(total), font: '700 24px "JetBrains Mono"', fill: '#101828' },
          },
        ],
      };
    }

    return null;
  }

  async function renderWidget(widget, page) {
    const host = document.querySelector(`[data-widget-id="${widget.query_id}"] .widget-body`);
    if (!host) return;

    const q = qsFromFilters(state.globalFilters);
    const payload = await fetchJson(`/api/query/${widget.query_id}/data${q ? `?${q}` : ''}`);

    if ((widget.chart || '').toLowerCase() === 'table') {
      host.innerHTML = tableHtml(payload.rows);
      return;
    }

    host.innerHTML = '<div class="chart"></div>';
    const chartNode = host.querySelector('.chart');
    if (!chartNode || !window.echarts) return;

    if (!state.charts[widget.query_id]) {
      state.charts[widget.query_id] = window.echarts.init(chartNode);
    }
    const option = makeOption(payload);
    if (option) state.charts[widget.query_id].setOption(option, true);
  }

  async function renderWidgets(page) {
    const grid = $('grid');
    grid.innerHTML = '';

    for (const w of page.widgets || []) {
      const node = document.createElement('article');
      node.className = 'widget';
      node.setAttribute('data-widget-id', w.query_id);
      node.style.gridColumn = `${(w.position?.x || 0) + 1} / span ${w.position?.w || 6}`;
      node.style.gridRow = `${(w.position?.y || 0) + 1} / span ${w.position?.h || 4}`;
      node.innerHTML = `
        <div class="widget-head">
          <div class="widget-title">${w.title || w.query_id}</div>
          <div class="widget-type">${w.chart || 'table'}</div>
        </div>
        <div class="widget-body"></div>
      `;
      grid.appendChild(node);
      await renderWidget(w, page);
    }
  }

  async function bootstrap() {
    $('backend-url').value = state.backend;
    const dashboard = await fetchJson('/api/dashboard');
    state.dashboard = dashboard;

    const page = (dashboard.pages || [])[0] || { widgets: [] };
    $('dashboard-title').textContent = dashboard.name || page.title || 'SQL2BI Dashboard';

    renderGlobalFilters(page);
    await renderWidgets(page);
  }

  $('apply-backend').addEventListener('click', () => {
    const url = $('backend-url').value.trim();
    state.backend = url || 'http://127.0.0.1:8000';
    localStorage.setItem('sql2bi_backend', state.backend);
    bootstrap().catch((err) => {
      console.error(err);
      alert(`Failed to connect backend: ${err.message}`);
    });
  });

  $('refresh').addEventListener('click', () => {
    if (!state.dashboard) return;
    const page = (state.dashboard.pages || [])[0] || { widgets: [] };
    renderWidgets(page).catch((err) => {
      console.error(err);
      alert(`Refresh failed: ${err.message}`);
    });
  });

  bootstrap().catch((err) => {
    console.error(err);
    $('dashboard-title').textContent = `Backend unavailable: ${err.message}`;
  });
})();
'''

FRONTEND_SERVER = '''#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 5173), Handler)
    print("Frontend service running at http://127.0.0.1:5173")
    server.serve_forever()
'''

BACKEND_REQUIREMENTS = '''fastapi==0.115.12
uvicorn==0.34.2
pydantic==2.11.4
duckdb==1.2.2
polars==1.29.0
pandas==2.2.3
'''

BACKEND_RUN = '''#!/usr/bin/env bash
set -euo pipefail

python3 -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
'''

START_BACKEND = '''#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT/backend"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
bash run.sh
'''

START_FRONTEND = '''#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT/frontend"
python3 server.py
'''


def write_file(path: Path, content: str, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(0o755)


def copy_artifact(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate backend/frontend service bundle")
    parser.add_argument("--artifacts", required=True, help="Directory containing pipeline outputs")
    parser.add_argument("--output", required=True, help="Output directory for service bundle")
    args = parser.parse_args()

    artifacts_dir = Path(args.artifacts)
    out_dir = Path(args.output)

    required = ["query_catalog.json", "semantic_catalog.json", "chart_plan.json", "dashboard.json"]
    missing = [name for name in required if not (artifacts_dir / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing artifacts in {artifacts_dir}: {', '.join(missing)}")

    data_dir = out_dir / "data"
    backend_dir = out_dir / "backend"
    frontend_dir = out_dir / "frontend"

    for name in required:
        copy_artifact(artifacts_dir / name, data_dir / name)

    write_file(backend_dir / "app.py", BACKEND_APP)
    write_file(backend_dir / "requirements.txt", BACKEND_REQUIREMENTS)
    write_file(backend_dir / "run.sh", BACKEND_RUN, executable=True)

    write_file(frontend_dir / "index.html", FRONTEND_INDEX)
    write_file(frontend_dir / "style.css", FRONTEND_STYLE)
    write_file(frontend_dir / "app.js", FRONTEND_APP)
    write_file(frontend_dir / "server.py", FRONTEND_SERVER, executable=True)

    write_file(out_dir / "start_backend.sh", START_BACKEND, executable=True)
    write_file(out_dir / "start_frontend.sh", START_FRONTEND, executable=True)

    print(f"Generated service bundle -> {out_dir}")
    print(f"Backend start:  {out_dir / 'start_backend.sh'}")
    print(f"Frontend start: {out_dir / 'start_frontend.sh'}")


if __name__ == "__main__":
    main()
