# Canvas 内嵌渲染

在对话中直接渲染图表，无需保存文件，用户即时看到结果。

---

## 什么时候用 Canvas 渲染

- 用户想在对话里直接看图，不想保存文件
- 快速验证图表效果
- 演示/汇报场景，需要即时展示

---

## 使用方式

通过 `canvas` 工具的 `eval` action 执行 JavaScript，渲染 Chart.js 图表。

### 折线图示例

```javascript
// canvas eval 内容
const ctx = document.getElementById('chart').getContext('2d');
new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
    datasets: [{
      label: '订单量',
      data: [1200, 1900, 1500, 2100, 2400, 2800],
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59,130,246,0.1)',
      borderWidth: 2,
      fill: true,
      tension: 0.4,
      pointRadius: 4
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: { display: true, text: '月度订单量趋势', font: { size: 16 } },
      legend: { position: 'top' }
    },
    scales: {
      y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } }
    }
  }
});
```

### Canvas HTML 模板

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body { font-family: 'Microsoft YaHei', sans-serif; padding: 20px; background: #fff; }
    .chart-container { max-width: 800px; margin: 0 auto; }
  </style>
</head>
<body>
  <div class="chart-container">
    <canvas id="chart"></canvas>
  </div>
  <script>
    // 在这里放图表代码
  </script>
</body>
</html>
```

---

## Chart.js 常用图表类型

| type 值 | 图表类型 |
|---------|---------|
| `'line'` | 折线图 |
| `'bar'` | 条形图（纵向） |
| `'bar'` + `indexAxis: 'y'` | 横向条形图 |
| `'pie'` | 饼图（慎用） |
| `'doughnut'` | 环形图 |
| `'scatter'` | 散点图 |
| `'bubble'` | 气泡图 |
| `'radar'` | 雷达图 |

---

## 多系列条形图示例

```javascript
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    datasets: [
      {
        label: 'PC端',
        data: [3200, 4100, 3800, 5200],
        backgroundColor: '#3b82f6'
      },
      {
        label: '移动端',
        data: [5100, 6200, 7100, 8900],
        backgroundColor: '#10b981'
      }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      title: { display: true, text: '各渠道季度订单量' }
    },
    scales: { y: { beginAtZero: true } }
  }
});
```

---

## 注意事项

- Canvas 渲染依赖网络加载 Chart.js CDN，离线环境需本地引入
- 数据量大时（>1000 点），建议先聚合再渲染，避免卡顿
- 中文字体在 Canvas 中需要系统已安装对应字体
- 复杂统计图（箱线图、小提琴图）建议用 Python matplotlib 生成图片，再展示
