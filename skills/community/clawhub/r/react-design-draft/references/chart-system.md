# Chart System

14 chart types with auto-selection decision tree. All charts implemented with pure CSS + inline SVG (no external libraries).

## Chart Type Decision Tree

```
What is the data relationship?
│
├─ Comparison between categories
│   ├─ Few categories (2-6) → bar-chart
│   └─ Many categories (7+) → horizontal-bar-chart
│
├─ Change over time
│   ├─ Few data points (2-8) → bar-chart
│   ├─ Many data points (8+) → line-chart
│   └─ Stock/financial → candlestick-chart
│
├─ Part of whole
│   ├─ Few segments (2-5) → donut-chart
│   └─ Many segments (6+) → treemap
│
├─ Relationship / Correlation
│   ├─ 2 variables → scatter-plot (quadrant-chart if thresholds exist)
│   └─ 3+ variables → bubble-chart
│
├─ Process / Flow
│   ├─ Sequential steps → flow-chart
│   ├─ Parallel lanes → swimlane-chart
│   └─ State transitions → state-machine
│
├─ Hierarchy
│   ├─ Tree structure → tree-chart
│   ├─ Layered/nested → layered-diagram
│   └─ Organizational → tree-chart (horizontal)
│
├─ Overlap / Set relationship
│   └─ 2-3 sets → venn-diagram
│
└─ Cumulative change
    └─ Positive/negative contributions → waterfall-chart
```

## 14 Chart Types

### 1. Bar Chart (bar-chart)

**When**: Compare 2-6 categories with numeric values

```jsx
// Component: components/BarChart.jsx
// Data shape: [{ label: string, value: number, color?: string }]
// Implementation: CSS flexbox bars with transition on height
// Max bars: 8 (beyond this, use horizontal-bar)
```

CSS spec:
```css
.bar-chart { display: flex; align-items: flex-end; gap: var(--sp-2); height: 200px; }
.bar-chart__bar {
  flex: 1; border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  background: var(--chart-bar-color, var(--color-accent-1));
  transition: height 0.3s ease;
  position: relative;
}
.bar-chart__label {
  position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%);
  font-size: var(--text-caption); white-space: nowrap;
}
.bar-chart__value {
  position: absolute; top: -18px; left: 50%; transform: translateX(-50%);
  font-size: var(--text-small); font-weight: 600; font-variant-numeric: tabular-nums;
}
```

### 2. Horizontal Bar Chart (horizontal-bar-chart)

**When**: Compare 7+ categories or long labels

```jsx
// Data shape: [{ label: string, value: number, color?: string }]
// Implementation: CSS grid rows, width % based on max value
// Max bars: 15 (beyond this, use treemap)
```

### 3. Line Chart (line-chart)

**When**: Show trend over 8+ time points

```jsx
// Data shape: { labels: string[], series: [{ name: string, values: number[], color?: string }] }
// Implementation: inline SVG polyline + CSS grid for axes
// Max series: 3 (beyond this, data becomes unreadable)
// SVG viewBox: "0 0 600 200" with 40px left margin for Y-axis labels
```

SVG template:
```html
<svg viewBox="0 0 600 200" class="line-chart">
  <!-- Grid lines -->
  <line x1="40" y1="0" x2="40" y2="180" stroke="var(--color-border)" />
  <!-- Data line -->
  <polyline fill="none" stroke="var(--color-accent-1)" stroke-width="2"
    points="40,160 120,140 200,100 280,120 360,60 440,80 520,40 600,50" />
  <!-- Data points -->
  <circle cx="40" cy="160" r="3" fill="var(--color-accent-1)" />
</svg>
```

### 4. Donut Chart (donut-chart)

**When**: Show 2-5 segments of a whole

```jsx
// Data shape: [{ label: string, value: number, color: string }]
// Implementation: SVG circle with stroke-dasharray/stroke-dashoffset
// Max segments: 5 (beyond this, use treemap)
// SVG: two circles — background ring + segment arcs
```

SVG template:
```html
<svg viewBox="0 0 120 120" class="donut-chart">
  <circle cx="60" cy="60" r="50" fill="none" stroke="var(--color-border)" stroke-width="12" />
  <circle cx="60" cy="60" r="50" fill="none" stroke="var(--color-accent-1)" stroke-width="12"
    stroke-dasharray="125.6 314.16" stroke-dashoffset="0"
    transform="rotate(-90 60 60)" />
  <!-- Center text -->
  <text x="60" y="55" text-anchor="middle" font-size="20" font-weight="600">40%</text>
  <text x="60" y="72" text-anchor="middle" font-size="10" fill="var(--color-text-muted)">label</text>
</svg>
```

### 5. Quadrant Chart (quadrant-chart)

**When**: Plot items on 2 axes with threshold lines

```jsx
// Data shape: { xLabel: string, yLabel: string, items: [{ name: string, x: number, y: number, quadrant?: string }] }
// Implementation: SVG with 4 quadrants via cross lines
// Thresholds: auto-calculate median or accept user-defined
```

### 6. Flow Chart (flow-chart)

**When**: Show sequential process with 3-8 steps

```jsx
// Data shape: { steps: [{ id: string, label: string, type?: 'start'|'process'|'decision'|'end' }], connections: [{ from: string, to: string, label?: string }] }
// Implementation: CSS grid + SVG arrows
// Max steps: 8 (beyond this, use swimlane)
```

### 7. Swimlane Chart (swimlane-chart)

**When**: Show parallel process across 2-4 actors/teams

```jsx
// Data shape: { lanes: [{ name: string, steps: [{ label: string, connectsTo?: { lane: number, step: number } }] }] }
// Implementation: CSS grid rows per lane + SVG arrows for cross-lane connections
// Max lanes: 4, max steps per lane: 6
```

### 8. State Machine (state-machine)

**When**: Show state transitions with conditions

```jsx
// Data shape: { states: [{ id: string, label: string, initial?: boolean }], transitions: [{ from: string, to: string, label?: string }] }
// Implementation: SVG circles (states) + SVG paths with markers (transitions)
// Max states: 6, max transitions: 10
```

### 9. Tree Chart (tree-chart)

**When**: Show hierarchical structure (org chart, file tree, taxonomy)

```jsx
// Data shape: { root: { label: string, children: [{ label: string, children?: [...] }] } }
// Implementation: CSS flexbox with connector lines via ::before/::after
// Max depth: 3, max children per node: 6
```

### 10. Layered Diagram (layered-diagram)

**When**: Show nested/layered architecture (tech stack, OSI model)

```jsx
// Data shape: { layers: [{ name: string, items: string[], color?: string }] }
// Implementation: CSS stacked rectangles with rounded corners
// Max layers: 6
```

### 11. Venn Diagram (venn-diagram)

**When**: Show overlap between 2-3 sets

```jsx
// Data shape: { sets: [{ label: string, color: string }], overlap: [{ sets: number[], label: string }] }
// Implementation: SVG circles with mix-blend-mode: multiply
// Max sets: 3
```

### 12. Candlestick Chart (candlestick-chart)

**When**: Show financial data (open/high/low/close)

```jsx
// Data shape: [{ date: string, open: number, high: number, low: number, close: number }]
// Implementation: SVG rect (body) + SVG line (wick)
// Max data points: 30
```

### 13. Waterfall Chart (waterfall-chart)

**When**: Show cumulative positive/negative contributions

```jsx
// Data shape: [{ label: string, value: number, type: 'positive'|'negative'|'total' }]
// Implementation: CSS flexbox with stacked bars, total bars anchored to bottom
// Max items: 10
```

### 14. Treemap (treemap)

**When**: Show hierarchical proportions (many categories)

```jsx
// Data shape: [{ label: string, value: number, color?: string, children?: [...] }]
// Implementation: CSS grid with calculated grid-area based on value proportions
// Max top-level items: 12
```

## Chart Styling Rules

### Color Rules
- Chart bars/lines use `--color-accent-1` through `--color-accent-4` by default
- When style = kami-editorial: use ink-blue `#1B365D` as primary, warm grays for secondary
- When palette = dark: increase stroke-width to 2.5px for visibility
- Never use > 4 colors in a single chart

### Typography in Charts
- Axis labels: `var(--text-caption)`, `var(--color-text-muted)`
- Data labels: `var(--text-small)`, `font-variant-numeric: tabular-nums`
- Chart title: `var(--text-h3)`, `var(--font-display)`
- Value annotations: `font-weight: 600`, `font-variant-numeric: tabular-nums`

### Spacing
- Chart padding: `var(--sp-4)` on all sides
- Gap between chart and legend: `var(--sp-3)`
- Legend item gap: `var(--sp-2)`
- Axis tick gap: `var(--sp-1)`

### Responsive
- Charts must work at 320px minimum width
- SVG charts: use `viewBox` + `width: 100%` + `height: auto`
- CSS charts: use `min-width: 0` on flex children to allow shrinking
- On mobile (< 640px): horizontal-bar preferred over vertical-bar

### Accessibility
- Every chart must have a `role="img"` and `aria-label` describing the data
- Don't rely solely on color — add patterns or labels for differentiation
- Data tables as `<details>` fallback for complex charts

## Chart Component Granularity

Each chart type is a single component file:

```
components/
├── charts/
│   ├── BarChart.jsx
│   ├── HorizontalBarChart.jsx
│   ├── LineChart.jsx
│   ├── DonutChart.jsx
│   ├── QuadrantChart.jsx
│   ├── FlowChart.jsx
│   ├── SwimlaneChart.jsx
│   ├── StateMachine.jsx
│   ├── TreeChart.jsx
│   ├── LayeredDiagram.jsx
│   ├── VennDiagram.jsx
│   ├── CandlestickChart.jsx
│   ├── WaterfallChart.jsx
│   └── Treemap.jsx
```

Each chart component ≤ 80 lines. If implementation exceeds 80 lines, extract sub-components (e.g., `ChartAxis.jsx`, `ChartLegend.jsx`).

## Auto-Selection Integration

In Step 1 Parse & Match, after determining content structure:

1. If content contains **numeric comparisons** → suggest bar-chart or horizontal-bar-chart
2. If content contains **time-series data** → suggest line-chart
3. If content contains **parts-of-whole** → suggest donut-chart
4. If content contains **process/flow** → suggest flow-chart
5. If content contains **hierarchy** → suggest tree-chart or layered-diagram
6. If content contains **comparison across actors** → suggest swimlane-chart

Present chart suggestion in Step 2 Confirm & Advise alongside layout/style/palette.
