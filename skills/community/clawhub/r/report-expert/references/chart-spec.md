# 图表与可视化规范

## Mermaid — 流程图/架构图

```html
<div class="mermaid-wrap"><pre class="mermaid">
flowchart TD
    A["节点A"] --> B["节点B"]
</pre></div>
```

## ECharts — 数据可视化（推荐）

```html
<div class="chart-box">
  <div class="chart-box__title">图表标题</div>
  <div class="chart-box__canvas" id="chart-xxx" data-option='{"xAxis":{"type":"category"}}'></div>
  <div class="chart-box__caption">数据来源</div>
</div>
```

**关键：** 用 `data-option` 声明配置，不需要手写 `<script>`，main.js 自动初始化。每个 `id` 必须唯一。

## Chart.js — 轻量图表

```html
<div class="chart-container">
  <canvas id="chart-xxx" height="300"></canvas>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  new Chart(document.getElementById('chart-xxx'), { ... });
});
</script>
```

**图表优先原则：** 能用图表表达的内容，必须优先使用图表，而非纯文字或表格堆砌。