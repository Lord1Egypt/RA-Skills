# Dashboard Examples — Code Reference

Read this file when building dashboards and you need concrete code templates.

## Chart.js — Basic Usage

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<canvas id="myChart"></canvas>
<script>
const chart = new Chart(document.getElementById('myChart').getContext('2d'), {
  type: 'line',  // line, bar, pie, doughnut, radar, polarArea
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: 'Revenue',
      data: [12, 19, 3, 5, 2],
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.1)',
      tension: 0.1,
      fill: true
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } }
  }
});

// Update dynamically
function updateChart(newData) {
  chart.data.datasets[0].data = newData;
  chart.update();
}
</script>
```

## ApexCharts — Real-time Area Chart

```html
<script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
<div id="chart"></div>
<script>
const options = {
  chart: {
    type: 'area', height: 350,
    animations: { enabled: true, dynamicAnimation: { speed: 1000 } }
  },
  series: [{ name: 'Value', data: [31, 40, 28, 51, 42, 109, 100] }],
  xaxis: { categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'] }
};
const chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();

// Append data in real-time
function addDataPoint(value) {
  chart.appendData([{ data: [value] }]);
}
</script>
```

## D3.js — Custom Bar Chart

```html
<script src="https://d3js.org/d3.v7.min.js"></script>
<svg id="chart" width="600" height="400"></svg>
<script>
const data = [30, 86, 168, 281, 303, 365];
const svg = d3.select("#chart");
const margin = {top: 20, right: 20, bottom: 30, left: 40};
const width = 600 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

const x = d3.scaleBand().domain(d3.range(data.length)).range([0, width]).padding(0.1);
const y = d3.scaleLinear().domain([0, d3.max(data)]).range([height, 0]);

const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
g.selectAll(".bar").data(data).join("rect")
  .attr("x", (d, i) => x(i)).attr("y", d => y(d))
  .attr("width", x.bandwidth()).attr("height", d => height - y(d))
  .attr("fill", "steelblue");
</script>
```

## SSE (Server-Sent Events) — Client + Server

**Client:**
```javascript
const eventSource = new EventSource('api/stream');
eventSource.addEventListener('update', (event) => {
  const data = JSON.parse(event.data);
  updateDashboard(data);
});
eventSource.onerror = () => {
  console.log('SSE failed, falling back to polling');
  eventSource.close();
  setInterval(() => fetch('api/data').then(r => r.json()).then(updateDashboard), 10000);
};
```

**Server (FastAPI):**
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio, json

app = FastAPI()

async def event_stream():
    while True:
        data = get_metrics()  # your data source
        yield f"event: update\ndata: {json.dumps(data)}\n\n"
        await asyncio.sleep(5)

@app.get("/api/stream")
async def stream():
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

## WebSocket — Client

```javascript
const ws = new WebSocket('wss://api.example.com/ws');
ws.onopen = () => ws.send(JSON.stringify({ type: 'subscribe', channel: 'metrics' }));
ws.onmessage = (event) => updateDashboard(JSON.parse(event.data));
ws.onclose = () => setTimeout(connectWebSocket, 5000);  // auto-reconnect
```

## Responsive Grid Layout

```html
<div class="grid">
  <!-- Top: Key metrics row -->
  <div class="card full">
    <div class="metrics-row">
      <div class="metric">
        <span class="metric-label">Total Revenue</span>
        <span class="metric-value">$142,592</span>
        <span class="metric-change positive">+12.5%</span>
      </div>
    </div>
  </div>
  <!-- Middle: Charts -->
  <div class="card wide"><canvas id="revenueChart"></canvas></div>
  <div class="card"><canvas id="usersChart"></canvas></div>
  <!-- Bottom: Table -->
  <div class="card full"><table class="data-table">...</table></div>
</div>
```

```css
/* Mobile-first responsive */
.metrics-row { display: flex; flex-direction: column; gap: 1rem; }
@media (min-width: 768px) {
  .metrics-row { flex-direction: row; flex-wrap: wrap; }
  .metric { flex: 1 1 calc(50% - 0.5rem); }
}
@media (min-width: 1024px) {
  .metric { flex: 1 1 calc(25% - 0.75rem); }
}
.button { min-height: 44px; min-width: 44px; }  /* Touch-friendly */
```

## Dark Mode

```css
:root {
  --bg-primary: #ffffff; --bg-secondary: #f8f9fa;
  --text-primary: #212529; --text-secondary: #6c757d;
  --border-color: #dee2e6;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #1a1a1a; --bg-secondary: #2d2d2d;
    --text-primary: #e9ecef; --text-secondary: #adb5bd;
    --border-color: #495057;
  }
}
body { background: var(--bg-primary); color: var(--text-primary); }
.card { background: var(--bg-secondary); border: 1px solid var(--border-color); }
```

## Performance Patterns

```javascript
// Debounce resize
let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(() => chart.resize(), 250); });

// Limit data points
function decimateData(data, max = 100) {
  if (data.length <= max) return data;
  const step = Math.ceil(data.length / max);
  return data.filter((_, i) => i % step === 0);
}

// Lazy load charts (Intersection Observer)
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { initChart(e.target); observer.unobserve(e.target); } });
});
document.querySelectorAll('.chart-container').forEach(el => observer.observe(el));
```

## Accessibility

```html
<div class="chart-container" role="img" aria-label="Revenue trend showing 12% growth">
  <canvas id="chart"></canvas>
  <table class="sr-only"><caption>Revenue Data</caption>
    <thead><tr><th>Month</th><th>Revenue</th></tr></thead>
    <tbody><tr><td>January</td><td>$12,000</td></tr></tbody>
  </table>
</div>
```
```css
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); }
```

Color-blind safe palette: `#0066CC` (blue), `#28A745` (green), `#FFC107` (amber), `#DC3545` (red), `#17A2B8` (cyan)

## Multi-source Data Fetching

```javascript
async function fetchAllData() {
  const [crypto, stocks, weather] = await Promise.all([
    fetch('api/crypto').then(r => r.json()),
    fetch('api/stocks').then(r => r.json()),
    fetch('api/weather').then(r => r.json()),
  ]);
  return { crypto, stocks, weather, timestamp: new Date().toISOString() };
}
```

## Caching Pattern

```javascript
const cache = new Map();
async function cachedFetch(url, ttlMs = 60000) {
  const cached = cache.get(url);
  if (cached && Date.now() - cached.time < ttlMs) return cached.data;
  const data = await fetch(url).then(r => r.json());
  cache.set(url, { data, time: Date.now() });
  return data;
}
```
