---
name: text2echart
name-zh: Data to Chart
provider: openclaw
description: >
  Chart generator skill. When triggered:
  - Default: CONSTRUCT ECharts option JSON and output HTML string directly and render by mermaid and support preview.
  - Image / vector (图片/矢量图): use CLI with --svg-output (or --svg --embed for offline).
  - Screenshot (截图): use CLI with --screenshot (needs Playwright).
  - Fine-tuning (微调/修改): open browser for interactive adjustment.
  Supports 6 chart types: bar, line, pie, scatter, radar, wordcloud (via JSON).
  Trigger words: chart, graph, visualize, plot, draw, wordcloud, vent draw图表, 画图, 可视化, 图片, 矢量图, 词云.
metadata:
  version: "2.3.2"
  launch: "text2echarts.html"
  trigger-keywords:
    - chart
    - graph
    - visualize
    - plot
    - make a chart
    - draw a graph
    - 图表
    - 画图
    - 可视化
    - 柱状图
    - 饼图
    - 图片
    - 矢量图
    - wordcloud
    - vent draw
    - 词云
  tags:
    - visualization
    - echarts
    - chart
    - data-viz
    - svg
---

# text2echart — Data to Chart

## ⚡ Routing

case when: user asks for a chart / graph / visualization (default):
  - Construct ECharts option JSON
  - Output HTML string directly, render with ```html code block
  - Support preview by opening in browser or screenshot

  **Default route — direct HTML generation in chat.**
  Example prompt: *"Give me a pie chart of browser market share — Chrome 65%, Safari 18%, Edge 8%, Firefox 5%, Other 4%"*
  → The model outputs a complete HTML file with an interactive ECharts pie chart.

case when: user asks for an image / picture / vector graphic (图片/矢量图):
  - Use CLI with SVG output: `node cli.js data.json --svg-output -o chart.svg`
  - `--svg-output` extracts standalone .svg file (requires Playwright)
  - Add `--embed` to bundle ECharts lib for fully offline use
  - SVG is vector format — sharp at any resolution, ideal for documents
  - Also send PNG screenshot for instant preview

case when: user asks for a screenshot / snapshot (截图):
  - Use CLI with screenshot: `node cli.js data.json --screenshot -o chart.png`
  - This generates high-quality raster PNG via Playwright
  - If Playwright is not installed, falls back with clear error + install instructions

case when: user wants to fine-tune / adjust / modify the chart (微调/修改):
  - Open browser: `node cli.js data.json --open`
  - Or open the generated HTML directly for interactive editing

case when: user asks to save to file / run locally:
  - Use CLI: `node cli.js data.json -o chart.html` (CDN mode, ~1KB)
  - For offline use: add `--embed` (~1MB)
  - Can combine with --open or --screenshot

case when: user asks for word cloud (词云):
  - Need word frequency data first (分词 + 词频统计)
  - Generate ECharts wordcloud option JSON with type:'wordCloud'
  - Then follow image/vector or html/web route based on output format request
  - Point to `text2echarts.html`
  - Open in browser, use templates and export

---

## Output Format

```html
<!DOCTYPE html><html lang="en"><head>...echarts CDN...<style>...</style></head><body><div id="chart"></div><script>...echarts option...</script></body></html>
```

---

## Overview

Generate ECharts SVG charts from JSON/CSV. Two entry points:

**Web App**: Open `text2echarts.html` in browser for interactive GUI with templates, live preview, theme switching, and PNG/JPG/SVG export.

**CLI**: `node cli.js` for scripted/batch generation.

## When to Use / When Not to Use

| Scenario | Use text2echart? |
|----------|-----------------|
| "Make a bar chart from this CSV" | ✅ Best fit |
| "Visualize my sales data" | ✅ Natural language input works |
| "Compare trends across months" | ✅ Line chart, multi-series |
| "Show market share distribution" | ✅ Pie chart with % labels |
| "I need an interactive chart dashboard" | ⚠️ Open text2echarts.html instead |
| "Animate this chart frame by frame" | ❌ ECharts not designed for animation frames |
| "Generate 100 charts in batch" | ✅ Use CLI: `for f in *.csv; do node cli.js \$f; done` |
| "Real-time streaming data" | ❌ Use ECharts live update API directly |

## Quick Start

```bash
# Web App — open interactive GUI
open text2echarts.html

# CLI — CSV → chart
node cli.js data.csv --open

# CLI — JSON → SVG
node cli.js chart.json -o report.html
```

## Supported Inputs

| Format | Example | Auto-detected |
|--------|---------|---------------|
| **CSV** | `Month,Sales\nJan,1200\nFeb,900` | ✅ yes (comma in first line) |
| **JSON** | `{"series":[{"type":"bar","data":[30,80]}]}` | ✅ yes (starts with `{`) |
| **JSON (simple)** | `{"type":"bar","data":[{"name":"A","value":30}]}` | ✅ yes |
| **Stdin pipe** | `cat data.csv \| node cli.js -` | ✅ use `-` |

## CLI Reference

```bash
node cli.js <input> [options]

Options:
  -o, --out <file>   Output file name
  --type <type>      Chart type for CSV: bar|line|pie|radar|wordcloud
  --theme <name>     dark|infographic|macarons|roma|shine|vintage
  --width / --height Chart dimensions
  --svg              SVG renderer (default)
  --svg-output       Output standalone .svg file (needs Playwright)
  --screenshot       Output PNG screenshot (needs Playwright)
  --open             Open in browser after generation
  --cdn              Use CDN for ECharts lib (default)
  --embed            Embed ECharts lib for offline (~1MB)
  --slide            960x540 PPT slide mode
```

## Chart Types

| Type | CSV columns | Auto features |
|------|-------------|---------------|
| bar | col1=labels, col2+=values | Rounded corners, top labels |
| line | col1=labels, col2+=values | Smooth curves, area fill |
| pie | col1=name, col2=value | Donut chart, % labels |
| scatter | col1=x, col2=y | Bubble symbols |
| radar | col1=dimension, col2+=values | Polygon shape |
| wordcloud | col1=word, col2=frequency | Diamond shape |

## Themes

| Theme | Style | Background |
|-------|-------|------------|
| dark | Tech, deep blue | #1a1a2e |
| infographic | Clean report | #f5f5f5 |
| macarons | Soft, business | #f5f5f5 |
| vintage | Nostalgic | #f5f5f5 |
| shine | Bright, vivid | #f5f5f5 |
| roma | Professional | #f5f5f5 |

## Few-Shot Examples

### 1. CSV → Bar Chart

User: *"Chart these monthly sales"*

```csv
Month,Sales
Jan,1200
Feb,900
Mar,1600
```

→ CLI auto-detects CSV, generates bar chart with labels, tooltips, rounded corners.

### 2. JSON → Pie with Percentages

```json
{
  "series": [{
    "type": "pie",
    "radius": ["40%", "70%"],
    "data": [
      {"value": 48, "name": "Chrome"},
      {"value": 22, "name": "Firefox"},
      {"value": 18, "name": "Safari"}
    ],
    "label": {"formatter": "{b}\n{d}%"}
  }],
  "title": {"text": "Market Share"}
}
```

### 3. CSV → Multi-series Line

```csv
Date,Revenue,Cost
Jan,1200,800
Feb,1500,900
Mar,1800,1100
```

`node cli.js data.csv --type line --theme dark --open`

## Architecture

```
Input (JSON/CSV)
  → cli.js parses & converts to ECharts option
  → Option JSON injected into HTML template
  → echarts.init(dom, theme, {renderer:"svg"})
  → Output: self-contained .html with CDN references (~1KB)
  → --embed flag: inline ECharts lib (~1MB, offline)
  → --screenshot flag: PNG via Playwright
  → --svg-output flag: standalone SVG via Playwright
```

## Dependencies

- **CLI**: Node.js only (stdlib, no npm packages)
- **Runtime**: Internet for ECharts CDN (or `--embed` for offline)
- **Zero npm install required**

## References

| File | Content |
|------|---------|
| `prompt.md` | Prompt engineering guide: core pattern, chain-of-thought, 3 few-shot examples, 16 option references, end-user template |
| `references/echarts-option-reference.md` | Full ECharts option API (EN, from official site) |
| `references/echarts-option-zh.md` | Full ECharts option API (中文) |
| `references/echarts-wordcloud.md` | Wordcloud extension docs |
| `references/echarts-zh-title.md` | title 选项详细说明 |
| `references/echarts-zh-grid.md` | grid 选项详细说明 |
| `references/echarts-zh-xAxis.md` | xAxis 选项详细说明 |
| `references/echarts-zh-yAxis.md` | yAxis 选项详细说明 |
| `references/echarts-zh-series-bar.md` | series.bar 柱状图配置 |
| `references/echarts-zh-series-line.md` | series.line 折线图配置 |
| `references/echarts-zh-series-pie.md` | series.pie 饼图配置 |
| `references/echarts-zh-series-scatter.md` | series.scatter 散点图 |
| `references/echarts-zh-series-radar.md` | series.radar 雷达图 |
| `references/echarts-zh-tooltip.md` | tooltip 提示框配置 |
| `references/echarts-zh-legend.md` | legend 图例配置 |
| `references/echarts-zh-color.md` | color 调色盘 |
| `references/echarts-zh-label.md` | label 数据标签 |
| `references/echarts-zh-emphasis.md` | emphasis 高亮状态 |
| `references/echarts-zh-smooth.md` | smooth 平滑曲线 |
| `references/echarts-zh-axisLabel.md` | axisLabel 坐标轴标签 |

## Prompt Guide

For LLM-based chart generation, see `prompt.md` — a complete prompt engineering guide with:
- Core prompt pattern for ECharts option generation
- Chain-of-thought reasoning for chart type selection
- 3 Few-Shot examples (bar, pie, line)
- 16 detailed option references with JSON examples
- Common mistakes checklist
- Copyable end-user prompt template

## Interactive Web App

For a full GUI experience, open `text2echarts.html` in your browser.
Features: live preview, templates, theme switching, export PNG/JPG/SVG.

```
web/
├── text2echarts.html    # English (default, lang toggle)
├── app.js               # Core logic (i18n via JSON)
├── styles.css           # Shared styles
├── templates.js         # Chart templates (CN/EN)
└── lang/                # JSON language packs
```

## Key ECharts Options Reference

Refer to these when constructing chart configurations. Official docs:

| Option | What it does | Concrete example | Link |
|--------|-------------|-----------------|------|
| `title` | Chart title | `{"text":"Sales","left":"center","textStyle":{"fontSize":18}}` | [→ docs](https://echarts.apache.org/en/option.html#title) |
| `grid` | Chart margins | `{"left":"3%","right":"4%","bottom":"10%","containLabel":true}` — `containLabel` prevents axis labels from being clipped | [→ docs](https://echarts.apache.org/en/option.html#grid) |
| `xAxis` | X axis | `{"type":"category","data":["Jan","Feb"],"axisLabel":{"rotate":45}}` — `type` must be `category` or `value` | [→ docs](https://echarts.apache.org/en/option.html#xAxis) |
| `yAxis` | Y axis | `{"type":"value","name":"Units"}` — add `name` for axis label text | [→ docs](https://echarts.apache.org/en/option.html#yAxis) |
| `series.type:'bar'` | Bar chart | `{"type":"bar","data":[30,80],"itemStyle":{"borderRadius":[4,4,0,0]},"label":{"show":true,"position":"top"}}` | [→ docs](https://echarts.apache.org/en/option.html#series-bar) |
| `series.type:'line'` | Line chart | `{"type":"line","data":[22,25,23],"smooth":true,"areaStyle":{"opacity":0.1},"lineStyle":{"width":3,"shadowBlur":10}}` | [→ docs](https://echarts.apache.org/en/option.html#series-line) |
| `series.type:'pie'` | Pie/donut | `{"type":"pie","radius":["40%","70%"],"data":[{"value":48,"name":"A"}],"label":{"formatter":"{b}\
{d}%"},"emphasis":{"label":{"fontSize":16}}}` | [→ docs](https://echarts.apache.org/en/option.html#series-pie) |
| `series.type:'scatter'` | Scatter | `{"type":"scatter","data":[[160,55],[170,65]],"symbolSize":12}` | [→ docs](https://echarts.apache.org/en/option.html#series-scatter) |
| `series.type:'radar'` | Radar | `{"type":"radar","data":[{"value":[90,75],"name":"Score"}]}` + `radar.indicator` | [→ docs](https://echarts.apache.org/en/option.html#series-radar) |
| `tooltip` | Hover info | `{"trigger":"axis"}` for bar/line (axis-level), `{"trigger":"item","formatter":"{b}:{c}"}` for pie | [→ docs](https://echarts.apache.org/en/option.html#tooltip) |
| `legend` | Series names | `{"data":["Sales","Profit"],"bottom":"0"}` — `data` must match series `name` | [→ docs](https://echarts.apache.org/en/option.html#legend) |
| `color` | Color palette | `["#5470c6","#91cc75","#fac858","#ee6666","#73c0de"]` — ECharts default 5-color palette | [→ docs](https://echarts.apache.org/en/option.html#color) |
| `label` | Data labels | `{"show":true,"position":"top","formatter":"{c}","fontSize":14}` — `position`: top/inside/outside/bottom | [→ docs](https://echarts.apache.org/en/option.html#series-bar.label) |
| `emphasis` | Highlight state | `{"label":{"fontSize":16,"fontWeight":"bold"}}` — triggered on hover | [→ docs](https://echarts.apache.org/en/option.html#series-pie.emphasis) |
| `smooth` | Curve lines | `true` for curved line chart, `false` (default) for polyline | [→ docs](https://echarts.apache.org/en/option.html#series-line.smooth) |
| `itemStyle.borderRadius` | Rounded bars | `[4,4,0,0]` — top-left, top-right, bottom-right, bottom-left | [→ docs](https://echarts.apache.org/en/option.html#series-bar.itemStyle) |
| `axisLabel.rotate` | Rotate X labels | `45` degrees — useful when labels overlap (10+ categories) | [→ docs](https://echarts.apache.org/en/option.html#xAxis.axisLabel) |

See also: `references/echarts-option-reference.md` (EN) and `references/echarts-option-zh.md` (CN)

## Common Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Blank chart | CDN blocked or no internet | Use `--embed` flag for local libs (~1MB) |
| SVG not rendering | Old browser version | Chrome/Firefox 2020+ required |
| Wordcloud missing | Missing wordcloud extension | Included in `--embed` mode; CDN auto-loads |
| Chinese garbled | File saved in wrong encoding | Save as UTF-8; `--embed` embeds correct charset |
| CLI not found | Node.js not installed | Install from nodejs.org |
| Screenshot fails | Playwright not installed | `npm install playwright && npx playwright install chromium`, or use `--svg-output` for vector format |

## Verification

After generating a chart:

1. Open the .html file in a browser
2. Confirm chart canvas/SVG renders
3. Hover over data points — tooltip should appear
4. Resize browser — chart should adapt
5. Test with `--theme` to confirm theme switching

## Other Advanced Capabilities

### 1. Multi-Pattern Generation

The model can generate multiple chart configurations in a single response — combining different chart types, color palettes, shapes, and styles all at once. For example, you can request a bar chart with 3 different themes, a word cloud with 5 shapes, or a side-by-side comparison of line vs bar for the same dataset — all produced in one go.

**Bar Chart with multiple styles and palettes:**

Prompt: *"Give me a bar chart of monthly sales/profit, with buttons to switch between 6 styles (default, rounded, horizontal, stacked, dark, gradient) and 8 color palettes (default, warm, cool, pastel, vivid, forest, sunset, ocean)"*

**Word Cloud with multiple shapes and palettes:**

Prompt: *"Make a word cloud of AI/ML terms, with buttons to switch between 6 shapes (circle, heart, diamond, star, pentagon, triangle) and 8 color palettes"*

### 2. Full ECharts Series Support

This skill documents the 6 most common chart types (bar, line, pie, scatter, radar, wordcloud), but the underlying LLM can theoretically generate **any** ECharts series type. The following chart types are supported by ECharts and can be generated by the model, though they are not explicitly documented in this skill — accuracy may be slightly lower for undocumented types, but modern LLMs handle them reliably:

**Additional Series Types:**
- **Candlestick** — financial OHLC (Open-High-Low-Close) charts, also known as K-line charts
- **Boxplot** — statistical distribution visualization with quartiles and outliers
- **Heatmap** — matrix-based heatmap and calendar heatmap
- **Treemap** — hierarchical data displayed as nested rectangles
- **Sunburst** — multi-level radial hierarchy chart
- **Sankey** — flow diagrams for energy, budget, traffic, etc.
- **Funnel** — conversion funnel for marketing and sales analytics
- **Gauge** — dashboard-style speedometer gauges
- **Graph** — force-directed node-edge network graphs
- **Tree** — tree diagrams (left-to-right, top-to-bottom, radial)
- **PictorialBar** — bars rendered using SVG symbols or icons
- **ThemeRiver** — streamgraph / ribbon-style time series
- **Lines** — flight/migration path lines (typically used with maps)
- **EffectScatter** — scatter plot with ripple animation effects
- **Map** — geo-map charts with region shading

**Additional Components & Extensions:**
- **Parallel** — parallel coordinates for multi-dimensional data
- **Custom** — fully custom renderers via callback functions
- **dataZoom** — interactive scrollable/zoomable axis (slider + inside)
- **visualMap** — continuous or piecewise color mapping component
- **brush** — rectangular/polygon region selection tool
- **timeline** — animated time playback between chart states
- **dataset** — declarative data transform pipeline (filter, sort, aggregate)
- **markLine / markArea / markPoint** — annotation markers on series
- **aria** — accessibility labels and descriptions
- **3D Charts** — via echarts-gl extension: scatter3D, bar3D, surface, globe, lines3D
