#!/usr/bin/env python3.11
"""Generate static UI scaffold from dashboard spec."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


INDEX_HTML = """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>SQL BI Studio</title>
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
  <link href=\"https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap\" rel=\"stylesheet\">
  <link rel=\"stylesheet\" href=\"style.css\" />
</head>
<body>
  <header class=\"top-toolbar\">
    <div class=\"toolbar-left\">
      <div class=\"brand\">SQL2BI Studio</div>
      <div class=\"view-tabs\">
        <button class=\"tab-btn active\" data-view=\"worksheet\">Worksheet</button>
        <button class=\"tab-btn\" data-view=\"dashboard\">Dashboard</button>
        <button class=\"tab-btn\" data-view=\"data\">Data</button>
      </div>
    </div>
    <div class=\"toolbar-right\">
      <button class=\"tool-btn\" id=\"undo-btn\">Undo</button>
      <button class=\"tool-btn\" id=\"redo-btn\">Redo</button>
      <button class=\"tool-btn\" id=\"refresh-btn\">Refresh</button>
      <button class=\"tool-btn primary\">Export</button>
    </div>
  </header>

  <div class=\"workbench\">
    <aside class=\"data-pane\">
      <div class=\"pane-title\">Data</div>
      <section class=\"field-group\">
        <h3>Dimensions</h3>
        <ul id=\"dimensions-list\" class=\"field-list\"></ul>
      </section>
      <section class=\"field-group\">
        <h3>Measures</h3>
        <ul id=\"measures-list\" class=\"field-list\"></ul>
      </section>
    </aside>

    <main class=\"workspace\">
      <div class=\"workspace-head\">
        <h1 id=\"dashboard-title\">SQL Generated Dashboard</h1>
        <div class=\"status\" id=\"status-summary\"></div>
      </div>

      <section class=\"shelves\">
        <div class=\"shelf\"><span>Columns</span><div class=\"shelf-drop\" id=\"shelf-columns\"></div></div>
        <div class=\"shelf\"><span>Rows</span><div class=\"shelf-drop\" id=\"shelf-rows\"></div></div>
        <div class=\"shelf\"><span>Marks</span><div class=\"shelf-drop\" id=\"shelf-marks\"></div></div>
        <div class=\"shelf\"><span>Filters</span><div class=\"shelf-drop\" id=\"shelf-filters\"></div></div>
      </section>

      <section class=\"viz-canvas\">
        <div id=\"grid\" class=\"grid\"></div>
      </section>

      <section class=\"data-preview\">
        <div class=\"preview-head\">
          <h2>Data Preview</h2>
          <span id=\"preview-widget\">No widget selected</span>
        </div>
        <div class=\"preview-table-wrap\">
          <table class=\"preview-table\" id=\"preview-table\"></table>
        </div>
      </section>
    </main>

    <aside class=\"inspector\">
      <section class=\"panel\">
        <div class=\"panel-head\">
          <h2>Global Filters</h2>
          <button class=\"tool-btn\" id=\"clear-global\">Clear</button>
        </div>
        <div id=\"global-filters\" class=\"filter-stack\"></div>
      </section>

      <section class=\"panel\">
        <h2>Worksheet Filters</h2>
        <div id=\"worksheet-filters\" class=\"filter-stack\"></div>
      </section>

      <section class=\"panel\">
        <h2>Query Status</h2>
        <ul id=\"query-status\" class=\"status-list\"></ul>
      </section>
    </aside>
  </div>

  <script src=\"https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js\"></script>
  <script src=\"app.js\"></script>
</body>
</html>
"""

STYLE_CSS = """:root {
  --bg-app: #f5f6f8;
  --bg-panel: #ffffff;
  --bg-canvas: #fcfcfd;
  --line-soft: #e6e8ec;
  --line-strong: #d0d5dd;
  --text-main: #101828;
  --text-sub: #475467;
  --text-mute: #667085;
  --brand: #2f6fed;
  --brand-weak: #e8f0ff;
  --accent: #f59e0b;
  --ok: #039855;
  --radius-sm: 6px;
  --radius-md: 10px;
  --shadow-panel: 0 1px 2px rgba(16, 24, 40, 0.06);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--bg-app);
  color: var(--text-main);
  font-family: "Source Sans 3", "Noto Sans SC", sans-serif;
}

.top-toolbar {
  height: 52px;
  border-bottom: 1px solid var(--line-soft);
  background: var(--bg-panel);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 12px;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand {
  font-weight: 700;
  font-size: 16px;
  color: var(--text-main);
  padding-right: 6px;
}

.view-tabs {
  display: flex;
  gap: 4px;
}

.tab-btn,
.tool-btn {
  border: 1px solid var(--line-soft);
  background: #fff;
  border-radius: var(--radius-sm);
  padding: 6px 10px;
  font-size: 12px;
  color: var(--text-sub);
  cursor: pointer;
}

.tab-btn.active {
  border-color: var(--brand);
  background: var(--brand-weak);
  color: var(--brand);
  font-weight: 700;
}

.tool-btn.primary {
  background: var(--brand);
  color: #fff;
  border-color: var(--brand);
}

.workbench {
  display: grid;
  grid-template-columns: 280px 1fr 320px;
  min-height: calc(100vh - 52px);
}

.data-pane,
.inspector {
  border-right: 1px solid var(--line-soft);
  background: var(--bg-panel);
  padding: 12px;
  overflow: auto;
}

.inspector {
  border-right: none;
  border-left: 1px solid var(--line-soft);
}

.workspace {
  padding: 12px;
  overflow: auto;
}

.workspace-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 10px;
}

.workspace-head h1 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
}

.status {
  color: var(--text-mute);
  font-size: 12px;
}

.pane-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-sub);
  margin-bottom: 8px;
}

.field-group {
  margin-bottom: 12px;
}

.field-group h3,
.panel h2 {
  margin: 0 0 8px;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-sub);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.field-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 6px;
}

.field-list li {
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-sm);
  padding: 6px 8px;
  font-size: 12px;
  background: #fff;
}

.field-list li.measure {
  font-family: "JetBrains Mono", monospace;
}

.shelves {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  margin-bottom: 10px;
}

.shelf {
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-sm);
  background: #fff;
  padding: 8px;
}

.shelf span {
  display: block;
  font-size: 11px;
  color: var(--text-mute);
  margin-bottom: 6px;
  text-transform: uppercase;
}

.shelf-drop {
  min-height: 30px;
  border: 1px dashed var(--line-strong);
  border-radius: var(--radius-sm);
  padding: 4px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.pill {
  background: var(--brand-weak);
  color: var(--brand);
  border-radius: 999px;
  padding: 3px 8px;
  font-size: 11px;
  font-weight: 700;
}

.viz-canvas {
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-md);
  background: var(--bg-canvas);
  padding: 10px;
  box-shadow: var(--shadow-panel);
}

.grid {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  grid-auto-rows: 64px;
  gap: 10px;
}

.widget {
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-sm);
  background: #fff;
  padding: 8px;
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 6px;
  cursor: pointer;
}

.widget.active {
  border-color: var(--brand);
  box-shadow: 0 0 0 2px rgba(47, 111, 237, 0.18);
}

.widget-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.widget-title {
  font-size: 13px;
  font-weight: 700;
}

.widget-type {
  font-size: 10px;
  text-transform: uppercase;
  color: var(--text-mute);
}

.chart-host,
.table-host {
  border: 1px solid var(--line-soft);
  border-radius: 4px;
  background: #fff;
  overflow: hidden;
}

.chart-host {
  min-height: 140px;
}

.table-host {
  min-height: 120px;
}

.table-host table {
  width: 100%;
  border-collapse: collapse;
}

.table-host th,
.table-host td {
  border-bottom: 1px solid var(--line-soft);
  padding: 6px;
  font-size: 11px;
  text-align: left;
}

.widget-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.meta-chip {
  font-size: 10px;
  color: var(--text-sub);
  border: 1px solid var(--line-soft);
  border-radius: 999px;
  padding: 2px 6px;
}

.panel {
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-sm);
  background: #fff;
  padding: 10px;
  margin-bottom: 10px;
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.panel-head h2 {
  margin-bottom: 0;
}

.filter-stack {
  display: grid;
  gap: 8px;
}

.filter-card {
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-sm);
  padding: 8px;
}

.filter-card .head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.filter-card .field {
  font-weight: 700;
  font-size: 12px;
}

.filter-card .mode {
  font-size: 10px;
  color: var(--text-mute);
  text-transform: uppercase;
}

.filter-card .hint {
  font-size: 11px;
  color: var(--text-sub);
  margin-bottom: 6px;
}

.control {
  width: 100%;
  border: 1px solid var(--line-strong);
  border-radius: 6px;
  min-height: 28px;
  padding: 4px 8px;
  font-size: 12px;
  font-family: inherit;
  background: #fff;
}

.status-list {
  margin: 0;
  padding-left: 16px;
  color: var(--text-sub);
  font-size: 12px;
}

.data-preview {
  margin-top: 10px;
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-md);
  background: #fff;
  padding: 10px;
}

.preview-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 6px;
}

.preview-head h2 {
  margin: 0;
  font-size: 14px;
}

#preview-widget {
  font-size: 12px;
  color: var(--text-mute);
}

.preview-table-wrap {
  overflow: auto;
}

.preview-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 520px;
}

.preview-table th,
.preview-table td {
  border: 1px solid var(--line-soft);
  padding: 6px 8px;
  font-size: 12px;
  text-align: left;
}

.preview-table th {
  background: #f9fafb;
  position: sticky;
  top: 0;
}

.preview-table tbody tr:nth-child(even) {
  background: #fcfcfd;
}

.hint {
  color: var(--text-mute);
  font-size: 12px;
}

@media (max-width: 1280px) {
  .workbench {
    grid-template-columns: 240px 1fr;
  }

  .inspector {
    position: fixed;
    right: 0;
    top: 52px;
    bottom: 0;
    width: 320px;
    transform: translateX(100%);
    transition: transform 0.2s ease;
    box-shadow: -6px 0 16px rgba(16, 24, 40, 0.12);
    z-index: 20;
  }

  body.inspector-open .inspector {
    transform: translateX(0);
  }
}

@media (max-width: 960px) {
  .workbench {
    grid-template-columns: 1fr;
  }

  .data-pane {
    display: none;
  }

  .shelves {
    grid-template-columns: 1fr;
  }
}
"""

APP_JS = """(async function () {
  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function uniqueOrdered(items) {
    const seen = new Set();
    const out = [];
    items.forEach((item) => {
      if (!item || seen.has(item)) return;
      seen.add(item);
      out.push(item);
    });
    return out;
  }

  function hashCode(input) {
    let h = 2166136261;
    for (let i = 0; i < input.length; i += 1) {
      h ^= input.charCodeAt(i);
      h += (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24);
    }
    return Math.abs(h >>> 0);
  }

  function seededSeries(seed, size, base) {
    const out = [];
    let v = seed % 997;
    for (let i = 0; i < size; i += 1) {
      v = (v * 37 + 17) % 997;
      out.push(base + (v % 60) + i * 2);
    }
    return out;
  }

  function normalizeFilterValue(raw) {
    if (raw === null || raw === undefined) return null;
    if (Array.isArray(raw)) {
      const cleaned = raw.filter(Boolean);
      return cleaned.length > 0 ? cleaned : null;
    }
    if (typeof raw === 'object' && raw.from !== undefined && raw.to !== undefined) {
      if (!raw.from && !raw.to) return null;
      return { from: raw.from || '', to: raw.to || '' };
    }
    const text = String(raw).trim();
    return text ? text : null;
  }

  function serializeFilterValue(v) {
    if (v === null || v === undefined) return '';
    if (Array.isArray(v)) return v.join(',');
    if (typeof v === 'object') return `${v.from || ''}-${v.to || ''}`;
    return String(v);
  }

  function deriveOptionsForField(field) {
    return [
      `${field}_A`,
      `${field}_B`,
      `${field}_C`,
      `${field}_D`
    ];
  }

  function computeFilterBoost(activeFilters) {
    const values = Object.values(activeFilters || {}).filter((v) => normalizeFilterValue(v) !== null);
    if (values.length === 0) return 1;
    let total = 0;
    values.forEach((v) => {
      total += serializeFilterValue(v).length;
    });
    return 1 + (Math.min(total, 40) / 120);
  }

  function getWidgetFields(widget) {
    return {
      dims: uniqueOrdered([...(widget.fields?.dimensions || []), ...(widget.fields?.time_fields || [])]),
      metrics: uniqueOrdered(widget.fields?.metrics || []),
      time: uniqueOrdered(widget.fields?.time_fields || [])
    };
  }

  function generateWidgetDataset(widget, filterState) {
    const fields = getWidgetFields(widget);
    const dimension = fields.time[0] || fields.dims[0] || 'category';
    const metric = fields.metrics[0] || 'value';
    const secondaryMetric = fields.metrics[1] || `${metric}_2`;

    const seed = hashCode(`${widget.id}|${serializeFilterValue(filterState)}`);
    const boost = computeFilterBoost(filterState);

    const x = [];
    for (let i = 1; i <= 12; i += 1) {
      if (fields.time.length > 0) {
        x.push(`2024-01-${String(i).padStart(2, '0')}`);
      } else {
        x.push(`${dimension}_${i}`);
      }
    }

    const s1 = seededSeries(seed, x.length, 80).map((n) => Math.round(n * boost));
    const s2 = seededSeries(seed + 91, x.length, 50).map((n) => Math.round(n * (boost * 0.9)));

    const rows = x.map((name, idx) => ({
      [dimension]: name,
      [metric]: s1[idx],
      [secondaryMetric]: s2[idx]
    }));

    return { rows, dimension, metric, secondaryMetric, seriesA: s1, seriesB: s2, x };
  }

  function makeChartOption(widget, dataset) {
    const chartType = (widget.chart || 'table').toLowerCase();
    const palette = ['#2f6fed', '#f59e0b', '#0ea5e9', '#039855'];

    if (chartType === 'line') {
      return {
        color: palette,
        tooltip: { trigger: 'axis' },
        grid: { left: 36, right: 16, top: 24, bottom: 30 },
        xAxis: { type: 'category', data: dataset.x, axisLabel: { fontSize: 10 } },
        yAxis: { type: 'value', axisLabel: { fontSize: 10 } },
        series: [{ type: 'line', smooth: true, data: dataset.seriesA }]
      };
    }

    if (chartType === 'bar') {
      return {
        color: palette,
        tooltip: { trigger: 'axis' },
        grid: { left: 36, right: 16, top: 24, bottom: 30 },
        xAxis: { type: 'category', data: dataset.x, axisLabel: { fontSize: 10, rotate: 30 } },
        yAxis: { type: 'value', axisLabel: { fontSize: 10 } },
        series: [{ type: 'bar', data: dataset.seriesA, barWidth: '52%' }]
      };
    }

    if (chartType === 'grouped_bar') {
      return {
        color: palette,
        tooltip: { trigger: 'axis' },
        legend: { top: 0, textStyle: { fontSize: 10 } },
        grid: { left: 36, right: 16, top: 28, bottom: 30 },
        xAxis: { type: 'category', data: dataset.x, axisLabel: { fontSize: 10, rotate: 25 } },
        yAxis: { type: 'value', axisLabel: { fontSize: 10 } },
        series: [
          { name: dataset.metric, type: 'bar', data: dataset.seriesA },
          { name: dataset.secondaryMetric, type: 'bar', data: dataset.seriesB }
        ]
      };
    }

    if (chartType === 'kpi') {
      const value = dataset.seriesA.reduce((a, b) => a + b, 0);
      return {
        xAxis: { show: false, type: 'value' },
        yAxis: { show: false, type: 'value' },
        series: [{ type: 'bar', data: [value], barWidth: 80, itemStyle: { color: '#2f6fed' } }],
        graphic: [
          {
            type: 'text',
            left: 'center',
            top: '42%',
            style: {
              text: value.toLocaleString(),
              font: '700 24px "JetBrains Mono"',
              fill: '#101828'
            }
          },
          {
            type: 'text',
            left: 'center',
            top: '64%',
            style: {
              text: dataset.metric,
              font: '12px "Source Sans 3"',
              fill: '#667085'
            }
          }
        ]
      };
    }

    return null;
  }

  function renderTableHost(host, dataset) {
    const cols = Object.keys(dataset.rows[0] || {});
    let html = '<table><thead><tr>';
    cols.forEach((c) => {
      html += `<th>${c}</th>`;
    });
    html += '</tr></thead><tbody>';
    dataset.rows.slice(0, 8).forEach((r) => {
      html += '<tr>';
      cols.forEach((c) => {
        html += `<td>${r[c]}</td>`;
      });
      html += '</tr>';
    });
    html += '</tbody></table>';
    host.innerHTML = html;
  }

  const res = await fetch('dashboard.json');
  const spec = await res.json();
  const page = (spec.pages && spec.pages[0]) || { widgets: [], global_filters: [] };

  const state = {
    selectedWidgetId: null,
    globalFilters: {},
    worksheetFilters: {},
    charts: {},
    widgetsById: {}
  };

  const grid = document.getElementById('grid');
  const globalFiltersRoot = document.getElementById('global-filters');
  const worksheetFiltersRoot = document.getElementById('worksheet-filters');
  const statusList = document.getElementById('query-status');
  const previewWidget = document.getElementById('preview-widget');
  const previewTable = document.getElementById('preview-table');

  document.getElementById('dashboard-title').textContent = spec.name || page.title || 'SQL Generated Dashboard';
  document.getElementById('status-summary').textContent = `${(page.widgets || []).length} worksheets`;

  const dimensions = [];
  const measures = [];

  function getGlobalFilterDefs() {
    if (Array.isArray(page.global_filters) && page.global_filters.length > 0) {
      return page.global_filters;
    }

    const fallback = uniqueOrdered((page.widgets || []).flatMap((w) => w.filters || []));
    return fallback.map((f) => ({
      id: `gf_${f}`,
      field: f,
      suggested_widget: 'select',
      operators: [],
      source_queries: []
    }));
  }

  function getActiveFiltersForWidget(widgetId) {
    const local = state.worksheetFilters[widgetId] || {};
    return { ...state.globalFilters, ...local };
  }

  function renderPreview(widgetId) {
    const widget = state.widgetsById[widgetId];
    previewTable.innerHTML = '';

    if (!widget) {
      previewWidget.textContent = 'No widget selected';
      return;
    }

    previewWidget.textContent = `Selected: ${widget.title}`;

    const dataset = generateWidgetDataset(widget, getActiveFiltersForWidget(widgetId));
    const cols = Object.keys(dataset.rows[0] || {});

    const thead = el('thead');
    const hr = el('tr');
    cols.forEach((c) => hr.appendChild(el('th', '', c)));
    thead.appendChild(hr);

    const tbody = el('tbody');
    dataset.rows.slice(0, 10).forEach((rowData) => {
      const row = el('tr');
      cols.forEach((c) => row.appendChild(el('td', '', String(rowData[c]))));
      tbody.appendChild(row);
    });

    previewTable.appendChild(thead);
    previewTable.appendChild(tbody);
  }

  function syncStatusText() {
    const activeGlobal = Object.values(state.globalFilters).filter((v) => normalizeFilterValue(v) !== null).length;
    const selected = state.selectedWidgetId ? ` | selected: ${state.selectedWidgetId}` : '';
    document.getElementById('status-summary').textContent = `${(page.widgets || []).length} worksheets | global filters: ${activeGlobal}${selected}`;
  }

  function updateShelfFilters() {
    const filtersShelf = document.getElementById('shelf-filters');
    filtersShelf.innerHTML = '';
    const defs = getGlobalFilterDefs();
    defs.forEach((f) => {
      const value = normalizeFilterValue(state.globalFilters[f.field]);
      if (value === null) return;
      const tag = `${f.field}: ${serializeFilterValue(value)}`;
      filtersShelf.appendChild(el('span', 'pill', tag));
    });
    if (filtersShelf.childElementCount === 0) {
      filtersShelf.appendChild(el('span', 'pill', 'No active filters'));
    }
  }

  function renderWidgetFilters(widget) {
    worksheetFiltersRoot.innerHTML = '';

    if (!widget) {
      worksheetFiltersRoot.appendChild(el('div', 'hint', 'No widget selected'));
      return;
    }

    const dsl = widget.dsl_filters || [];
    if (dsl.length === 0) {
      worksheetFiltersRoot.appendChild(el('div', 'hint', 'No worksheet-level DSL filters'));
      return;
    }

    dsl.forEach((f) => {
      renderFilterCard(f, worksheetFiltersRoot, state.worksheetFilters[widget.query_id]?.[f.field], (value) => {
        if (!state.worksheetFilters[widget.query_id]) state.worksheetFilters[widget.query_id] = {};
        state.worksheetFilters[widget.query_id][f.field] = normalizeFilterValue(value);
        renderWidgetViz(widget.query_id);
        renderPreview(widget.query_id);
        syncStatusText();
      });
    });
  }

  function renderFilterCard(filter, root, currentValue, onChange) {
    const card = el('div', 'filter-card');
    const head = el('div', 'head');
    head.appendChild(el('div', 'field', filter.field || 'unknown_field'));
    head.appendChild(el('div', 'mode', filter.suggested_widget || 'select'));
    card.appendChild(head);

    const ops = (filter.operators || []).join(', ');
    const format = filter.value_format ? ` | format: ${filter.value_format}` : '';
    const hintText = ops ? `ops: ${ops}${format}` : (format || 'ops: auto');
    card.appendChild(el('div', 'hint', hintText));

    const widgetType = (filter.suggested_widget || 'select').toLowerCase();

    if (widgetType === 'date_range' || widgetType === 'number_range') {
      const wrap = el('div');
      wrap.style.display = 'grid';
      wrap.style.gridTemplateColumns = '1fr 1fr';
      wrap.style.gap = '6px';
      const from = el('input', 'control');
      const to = el('input', 'control');
      from.placeholder = 'From';
      to.placeholder = 'To';
      if (currentValue && typeof currentValue === 'object') {
        from.value = currentValue.from || '';
        to.value = currentValue.to || '';
      }
      const emit = () => onChange({ from: from.value, to: to.value });
      from.addEventListener('change', emit);
      to.addEventListener('change', emit);
      wrap.appendChild(from);
      wrap.appendChild(to);
      card.appendChild(wrap);
      root.appendChild(card);
      return;
    }

    if (widgetType === 'search') {
      const input = el('input', 'control');
      input.placeholder = 'Search...';
      input.value = typeof currentValue === 'string' ? currentValue : '';
      input.addEventListener('change', () => onChange(input.value));
      card.appendChild(input);
      root.appendChild(card);
      return;
    }

    const options = deriveOptionsForField(filter.field || 'value');

    if (widgetType === 'multi_select') {
      const select = el('select', 'control');
      select.multiple = true;
      options.forEach((v) => {
        const op = el('option', '', v);
        if (Array.isArray(currentValue) && currentValue.includes(v)) op.selected = true;
        select.appendChild(op);
      });
      select.addEventListener('change', () => {
        const values = Array.from(select.selectedOptions || []).map((o) => o.value);
        onChange(values);
      });
      card.appendChild(select);
      root.appendChild(card);
      return;
    }

    const single = el('select', 'control');
    [''].concat(options).forEach((v) => {
      const op = el('option', '', v || 'All');
      op.value = v;
      if (String(currentValue || '') === String(v)) op.selected = true;
      single.appendChild(op);
    });
    single.addEventListener('change', () => onChange(single.value));
    card.appendChild(single);
    root.appendChild(card);
  }

  function renderGlobalFilters() {
    globalFiltersRoot.innerHTML = '';
    const defs = getGlobalFilterDefs();

    if (defs.length === 0) {
      globalFiltersRoot.appendChild(el('div', 'hint', 'No global filters'));
      return;
    }

    defs.forEach((f) => {
      renderFilterCard(f, globalFiltersRoot, state.globalFilters[f.field], (value) => {
        state.globalFilters[f.field] = normalizeFilterValue(value);
        renderAllWidgets();
        if (state.selectedWidgetId) {
          renderPreview(state.selectedWidgetId);
          renderWidgetFilters(state.widgetsById[state.selectedWidgetId]);
        }
        updateShelfFilters();
        syncStatusText();
      });
    });
  }

  function renderWidgetViz(widgetId) {
    const widget = state.widgetsById[widgetId];
    if (!widget) return;

    const widgetNode = document.querySelector(`[data-widget-id="${widgetId}"]`);
    if (!widgetNode) return;

    const dataset = generateWidgetDataset(widget, getActiveFiltersForWidget(widgetId));
    const chartType = (widget.chart || 'table').toLowerCase();

    const chartHost = widgetNode.querySelector('.chart-host');
    const tableHost = widgetNode.querySelector('.table-host');

    if (chartType === 'table') {
      if (chartHost) chartHost.style.display = 'none';
      if (tableHost) {
        tableHost.style.display = 'block';
        renderTableHost(tableHost, dataset);
      }
      return;
    }

    if (tableHost) tableHost.style.display = 'none';
    if (!chartHost) return;
    chartHost.style.display = 'block';

    if (!window.echarts) {
      chartHost.innerHTML = '<div class="hint" style="padding:8px">ECharts is not available</div>';
      return;
    }

    const option = makeChartOption(widget, dataset);
    if (!option) return;

    if (!state.charts[widgetId]) {
      state.charts[widgetId] = window.echarts.init(chartHost);
      state.charts[widgetId].on('click', (params) => {
        const defs = getGlobalFilterDefs();
        if (defs.length === 0 || !params || !params.name) return;
        const target = defs[0];
        state.globalFilters[target.field] = params.name;
        renderGlobalFilters();
        renderAllWidgets();
        updateShelfFilters();
        syncStatusText();
      });
    }

    state.charts[widgetId].setOption(option, true);
    state.charts[widgetId].resize();
  }

  function renderAllWidgets() {
    (page.widgets || []).forEach((w) => renderWidgetViz(w.query_id));
  }

  function selectWidget(widgetId) {
    state.selectedWidgetId = widgetId;
    grid.querySelectorAll('.widget').forEach((n) => n.classList.remove('active'));
    const node = grid.querySelector(`[data-widget-id="${widgetId}"]`);
    if (node) node.classList.add('active');

    renderWidgetFilters(state.widgetsById[widgetId]);
    renderPreview(widgetId);
    syncStatusText();
  }

  (page.widgets || []).forEach((w, idx) => {
    state.widgetsById[w.query_id] = w;

    const fields = getWidgetFields(w);
    dimensions.push(...fields.dims);
    measures.push(...fields.metrics);

    const node = el('article', 'widget');
    node.setAttribute('data-widget-id', w.query_id);
    node.style.gridColumn = `${(w.position?.x || 0) + 1} / span ${w.position?.w || 6}`;
    node.style.gridRow = `${(w.position?.y || 0) + 1} / span ${w.position?.h || 4}`;

    const head = el('div', 'widget-head');
    head.appendChild(el('div', 'widget-title', w.title || w.query_id || `Widget ${idx + 1}`));
    head.appendChild(el('div', 'widget-type', w.chart || 'table'));
    node.appendChild(head);

    const chartHost = el('div', 'chart-host');
    node.appendChild(chartHost);

    const tableHost = el('div', 'table-host');
    tableHost.style.display = 'none';
    node.appendChild(tableHost);

    const meta = el('div', 'widget-meta');
    uniqueOrdered([...(fields.metrics || []).slice(0, 2), ...(fields.dims || []).slice(0, 2)]).forEach((name) => {
      meta.appendChild(el('span', 'meta-chip', name));
    });
    node.appendChild(meta);

    node.addEventListener('click', () => selectWidget(w.query_id));
    grid.appendChild(node);

    const status = el('li', '', `${w.query_id} | ${w.datasource || 'default'} | ${w.refresh || 'manual'}`);
    statusList.appendChild(status);
  });

  const dimRoot = document.getElementById('dimensions-list');
  uniqueOrdered(dimensions).forEach((name) => dimRoot.appendChild(el('li', '', name)));
  if (dimRoot.childElementCount === 0) dimRoot.appendChild(el('li', '', 'No dimensions'));

  const meaRoot = document.getElementById('measures-list');
  uniqueOrdered(measures).forEach((name) => meaRoot.appendChild(el('li', 'measure', name)));
  if (meaRoot.childElementCount === 0) meaRoot.appendChild(el('li', 'measure', 'No measures'));

  const rowsShelf = document.getElementById('shelf-rows');
  const colsShelf = document.getElementById('shelf-columns');
  const marksShelf = document.getElementById('shelf-marks');

  uniqueOrdered(dimensions).slice(0, 2).forEach((f) => rowsShelf.appendChild(el('span', 'pill', f)));
  uniqueOrdered(measures).slice(0, 2).forEach((f) => colsShelf.appendChild(el('span', 'pill', f)));
  marksShelf.appendChild(el('span', 'pill', ((page.widgets || [])[0]?.chart || 'table').toUpperCase()));

  document.getElementById('clear-global').addEventListener('click', () => {
    state.globalFilters = {};
    renderGlobalFilters();
    renderAllWidgets();
    updateShelfFilters();
    if (state.selectedWidgetId) {
      renderPreview(state.selectedWidgetId);
      renderWidgetFilters(state.widgetsById[state.selectedWidgetId]);
    }
    syncStatusText();
  });

  document.getElementById('refresh-btn').addEventListener('click', () => {
    renderAllWidgets();
    if (state.selectedWidgetId) renderPreview(state.selectedWidgetId);
  });

  document.getElementById('undo-btn').addEventListener('click', () => {
    alert('Undo is a placeholder in scaffold V2.');
  });

  document.getElementById('redo-btn').addEventListener('click', () => {
    alert('Redo is a placeholder in scaffold V2.');
  });

  renderGlobalFilters();
  updateShelfFilters();
  renderAllWidgets();

  if ((page.widgets || []).length > 0) {
    selectWidget(page.widgets[0].query_id);
  } else {
    renderWidgetFilters(null);
    renderPreview(null);
    syncStatusText();
  }

  window.addEventListener('resize', () => {
    Object.values(state.charts).forEach((chart) => {
      if (chart && typeof chart.resize === 'function') chart.resize();
    });
  });
})();
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate static UI scaffold")
    parser.add_argument("--dashboard", required=True, help="Path to dashboard.json")
    parser.add_argument("--out", required=True, help="Output directory for UI files")
    args = parser.parse_args()

    dashboard_path = Path(args.dashboard)
    out_dir = Path(args.out)

    spec = json.loads(dashboard_path.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "index.html").write_text(INDEX_HTML, encoding="utf-8")
    (out_dir / "style.css").write_text(STYLE_CSS, encoding="utf-8")
    (out_dir / "app.js").write_text(APP_JS, encoding="utf-8")
    (out_dir / "dashboard.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Generated UI scaffold -> {out_dir}")


if __name__ == "__main__":
    main()
