# Chart Rendering

## :::chart

Use **ECharts** for ALL charts in the report. ECharts covers bar/line/pie/scatter/radar/funnel/heatmap/multi-axis/sankey with a single library, avoiding the pitfalls of mixed-library switching (rotated label clipping, artificial data splits, HTML shell rewrites).

Add `<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>` in `<head>` (or inline if `--bundle`).

**Chart.js is NOT used in the standard template.** Do NOT generate Chart.js chart code.

Body schema by `type`:

| Type | Required body keys | Notes |
|------|--------------------|-------|
| `bar`, `line`, `pie`, `radar` | `labels`, `datasets` | Each dataset must provide `label` and `data`. |
| `scatter` | `datasets` | Each dataset must provide `label` and `points: [[x, y], ...]`. |
| `funnel` | `stages` | Each stage is `{label, value}`. |
| `sankey` | `nodes`, `links` | `links` encode quantified flows. |

- `invalid_syntax`: body keys do not match the selected `type`.
- `invalid_semantics`: chart is parseable but wrong for the content, or all data is placeholder-only decoration.
- `contract_conflict`: prior Chart.js/ECharts split. Resolved here as ECharts-only.
- `auto_downgrade_target`: `table` (preferred) or `callout` when the source has no chartable data.

### ECharts bar chart

    <div data-component="chart" data-type="bar" class="fade-in-up">
      <div id="chart-[unique-id]" style="height:300px"></div>
      <script>
        var chart = echarts.init(document.getElementById('chart-[unique-id]'));
        chart.setOption({
          title: { text: '[title]', textStyle: { color: '#94A3B8', fontSize: 13 } },
          grid: { top: 50, right: 30, bottom: 30, left: 60 },
          xAxis: { type: 'category', data: ['...'], axisLabel: { color: '#94A3B8' }, axisLine: { lineStyle: { color: '#334155' } } },
          yAxis: { type: 'value', axisLabel: { color: '#94A3B8' }, splitLine: { lineStyle: { color: '#334155' } } },
          series: [{ name: '[series]', type: 'bar', data: [...], barWidth: '50%', label: { show: true, position: 'top', color: '#E2E8F0', formatter: '{c}' } }],
          tooltip: { trigger: 'item', backgroundColor: '#1E293B', borderColor: '#334155', textStyle: { color: '#E2E8F0' } }
        });
      </script>
    </div>

**Grid bottom rule (MANDATORY):** If x-axis labels are rotated (`rotate > 0`), `grid.bottom` MUST be ≥ 60. Without rotation, `bottom: 30` is sufficient.

### ECharts radar chart

    <div data-component="chart" data-type="radar" class="fade-in-up">
      <div id="chart-[unique-id]" style="height:300px"></div>
      <script>
        var chart = echarts.init(document.getElementById('chart-[unique-id]'));
        chart.setOption({
          title: { text: '[title]', textStyle: { color: '#94A3B8', fontSize: 13 } },
          legend: { data: ['...'], bottom: 0, textStyle: { color: '#94A3B8', fontSize: 11 } },
          radar: { indicator: [{ name: '...' }], axisName: { color: '#E2E8F0', fontSize: 11 }, splitLine: { lineStyle: { color: '#334155' } }, splitArea: { areaStyle: { color: ['rgba(30,41,59,0.6)', 'rgba(15,23,42,0.8)'] } } },
          series: [{ type: 'radar', data: [{ value: [...], name: '...' }] }],
          tooltip: { trigger: 'item', backgroundColor: '#1E293B', borderColor: '#334155', textStyle: { color: '#E2E8F0' } }
        });
      </script>
    </div>

### ECharts line chart

    <div data-component="chart" data-type="line" class="fade-in-up">
      <div id="chart-[unique-id]" style="height:300px"></div>
      <script>
        var chart = echarts.init(document.getElementById('chart-[unique-id]'));
        chart.setOption({
          title: { text: '[title]', textStyle: { color: '#94A3B8', fontSize: 13 } },
          grid: { top: 50, right: 30, bottom: 50, left: 55 },
          xAxis: { type: 'category', data: ['...'], axisLabel: { color: '#94A3B8', interval: 0 }, axisLine: { lineStyle: { color: '#334155' } } },
          yAxis: { type: 'value', axisLabel: { color: '#94A3B8' }, splitLine: { lineStyle: { color: '#334155' } } },
          series: [{ name: '[series]', type: 'line', data: [...], smooth: true, lineStyle: { color: '#818CF8', width: 2 }, itemStyle: { color: '#818CF8' }, areaStyle: { color: 'rgba(129,140,248,0.1)' } }],
          legend: { data: ['[series]'], bottom: 0, textStyle: { color: '#94A3B8', fontSize: 11 } },
          tooltip: { trigger: 'item', backgroundColor: '#1E293B', borderColor: '#334155', textStyle: { color: '#E2E8F0' } }
        });
      </script>
    </div>

**Line data rule (MANDATORY):** If the IR provides a single `data` array, render as a **single series**. Do NOT split into multiple series with `null` values unless the IR explicitly defines separate series via `series:` YAML key.

### ECharts pie chart

    <div data-component="chart" data-type="pie" class="fade-in-up">
      <div id="chart-[unique-id]" style="height:300px"></div>
      <script>
        var chart = echarts.init(document.getElementById('chart-[unique-id]'));
        chart.setOption({
          title: { text: '[title]', textStyle: { color: '#94A3B8', fontSize: 13 } },
          series: [{ type: 'pie', radius: ['40%', '70%'], data: [{ name: 'A', value: 10 }, ...], label: { formatter: '{b}: {d}%' }, emphasis: { itemStyle: { shadowBlur: 10 } } }],
          tooltip: { trigger: 'item', backgroundColor: '#1E293B', borderColor: '#334155', textStyle: { color: '#E2E8F0' } }
        });
      </script>
    </div>

### ECharts sankey rendering (triggered by `type=sankey`)

IR input format:
```
:::chart type=sankey title=资金流向
nodes: [A, B, C, D]
links: [A->B:120, A->C:80, B->D:90, C->D:110]
:::
```

Parse `nodes` as `[{name: "A"}, ...]` and `links` as `[{source: "A", target: "B", value: 120}, ...]`.

**Label display rule (mandatory):** Node labels MUST show both name and value. Use ECharts `rich` text to give them distinct visual weight — name in muted small text, value in bold primary-color larger text. Never show name-only labels; a Sankey without numbers loses its core meaning.

    <div data-component="chart" data-type="sankey" class="fade-in-up">
      <div id="chart-[unique-id]" style="height:380px"></div>
      <script>
        // Pre-compute node totals for label display
        var nodeTotal = {};
        var links = [{ source: 'A', target: 'B', value: 120 }, ...];
        links.forEach(function(l) { nodeTotal[l.target] = (nodeTotal[l.target]||0) + l.value; });
        links.forEach(function(l) { if (!nodeTotal[l.source]) nodeTotal[l.source] = links.filter(function(x){return x.source===l.source;}).reduce(function(s,x){return s+x.value;},0); });

        var chart = echarts.init(document.getElementById('chart-[unique-id]'));
        chart.setOption({
          tooltip: {
            trigger: 'item', triggerOn: 'mousemove',
            formatter: function(p) {
              if (p.dataType === 'edge') {
                var pct = (p.data.value / (nodeTotal[p.data.source]||1) * 100).toFixed(1);
                return p.data.source + ' → ' + p.data.target + '<br/>' + p.data.value.toLocaleString() + ' (' + pct + '%)';
              }
              return p.name + '<br/>' + (nodeTotal[p.name]||0).toLocaleString();
            }
          },
          series: [{
            type: 'sankey',
            layout: 'none',
            emphasis: { focus: 'adjacency' },
            nodeWidth: 18,
            nodeGap: 14,
            lineStyle: { color: 'gradient', opacity: 0.4 },
            label: {
              fontFamily: '-apple-system, BlinkMacSystemFont, sans-serif',
              formatter: function(p) {
                var v = nodeTotal[p.name] || 0;
                return '{name|' + p.name + '}\n{val|' + v.toLocaleString() + '}';
              },
              rich: {
                name: { fontSize: 12, color: '#555', fontWeight: 'normal', lineHeight: 18 },
                val:  { fontSize: 15, color: '#0B6E6E', fontWeight: '700', lineHeight: 20 }
              }
            },
            edgeLabel: {
              show: true, fontSize: 11, color: '#555',
              formatter: function(p) { return p.data.value.toLocaleString(); }
            },
            data: [{ name: 'A' }, { name: 'B' }, ...],
            links: links
          }]
        });
      </script>
    </div>

**val color rule:** Use theme's `--primary` color for the value text (default `#0B6E6E`). For dark themes substitute the theme accent color.

Use cases: budget flows, conversion funnels (multi-step), resource allocation, supply chain. Height default 380px; increase to 500px for 8+ nodes.
