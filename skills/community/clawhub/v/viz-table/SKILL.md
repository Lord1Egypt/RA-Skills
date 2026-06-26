---
name: viz-table
description: 从 CSV/JSON 文件读取数据，使用 ECharts 生成可视化 HTML 图表（柱状图、折线图、饼图、环形图）并自动在浏览器中打开。用户提供文件路径时触发。
argument-hint: <文件路径> [bar|line|pie|donut]
---

## 任务

将用户提供的数据文件可视化为交互式 ECharts HTML 图表，并自动在浏览器中打开。

## 参数解析

- `$0` — 数据文件路径（CSV 或 JSON）
- `$1` — 图表类型（可选）：`bar`（柱状图）、`line`（折线图）、`pie`（饼图）、`donut`（环形图）

如果用户没有提供 `$1`，**必须先询问用户选择图表类型**：
> "请选择图表类型：
> 1. 柱状图 (bar)
> 2. 折线图 (line)
> 3. 饼图 (pie)
> 4. 环形图 (donut)"
等待用户回复后再继续。

## 执行步骤

### 第一步：读取文件

使用 Read 工具读取 `$0` 指定的文件。

- 如果是 `.csv`：解析为二维数组，第一行为表头
- 如果是 `.json`：解析为对象数组，key 为表头

如果文件不存在或格式不支持，告知用户并停止。

### 第二步：分析数据结构

- 识别第一列为**类别/标签列**（X 轴或饼图 name）
- 其余数值列每列生成一个数据系列
- 饼图/环形图：若有多个数值列，默认取第一个数值列；每行的类别列作为 name，数值作为 value

### 第三步：生成 HTML 文件

调用 Write 工具，将生成的 HTML 写入 `/tmp/viz-table-output.html`。

HTML 要求：
- 使用 **ECharts 5**（CDN：`https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js`）
- 图表容器用 `<div id="chart">` 并设置 `width:100%; height:500px`
- 配色使用企业专业色板：`['#4F81BD','#C0504D','#9BBB59','#8064A2','#4BACC6','#F79646']`
- 页面顶部有四个切换按钮（柱状图 / 折线图 / 饼图 / 环形图），点击无需刷新页面
- 图表下方渲染原始数据表格（带斑马纹样式）
- 页面背景 `#f0f2f5`，图表区域白色卡片带阴影

## 计算功能

### 功能一：图表内统计面板

在图表卡片下方（原始数据表格上方）渲染一个统计面板，对每个数值列自动计算：
- 总计、平均值、最大值、最小值
- 环比增长率（最后一行相对倒数第二行）

样式：横向卡片排列，每个数值列一张卡片，卡片内竖向列出各指标。

```html
<div class="stats-panel">
  <!-- 每个数值列一张卡片 -->
  <div class="stat-card">
    <div class="stat-title">销售额</div>
    <div class="stat-row"><span>总计</span><span>2,128,000</span></div>
    <div class="stat-row"><span>平均值</span><span>177,333</span></div>
    <div class="stat-row"><span>最大值</span><span>260,000</span></div>
    <div class="stat-row"><span>最小值</span><span>98,000</span></div>
    <div class="stat-row"><span>环比增长</span><span class="positive">+33.3%</span></div>
  </div>
</div>
```

增长率正数显示绿色（`.positive { color: #52c41a }`），负数显示红色（`.negative { color: #ff4d4f }`）。

### 功能二：自定义公式输入框

在统计面板下方、原始数据表格上方，放置一个公式输入区：

```html
<div class="formula-section">
  <h2>自定义计算列</h2>
  <div class="formula-input-row">
    <input id="colName" placeholder="新列名称（如：利润率）" />
    <input id="formula" placeholder="公式（如：利润 / 销售额 * 100）" />
    <button onclick="applyFormula()">计算并添加</button>
  </div>
  <p class="formula-hint">可用列名：{列名1}、{列名2}... 支持 + - * / ( ) 运算</p>
</div>
```

`applyFormula()` 逻辑：
1. 读取公式字符串，将列名替换为对应行的数值（用 `replace` 逐列替换）
2. 用 `eval()` 计算每行结果，结果保留两位小数
3. 在原始数据表格末尾追加新列（表头 + 每行数据）
4. 同时将新系列追加到 `datasets`，并调用 `chart.setOption` 刷新图表
5. 如果公式非法，在输入框下方显示红色错误提示

各图表类型的 ECharts option 配置要点：

**柱状图 (bar)**：
```js
{ tooltip: { trigger: 'axis' }, legend: {}, color: COLORS,
  xAxis: { type: 'category', data: labels },
  yAxis: { type: 'value' },
  series: datasets.map(d => ({ name: d.name, type: 'bar', data: d.data })) }
```

**折线图 (line)**：
```js
{ tooltip: { trigger: 'axis' }, legend: {}, color: COLORS,
  xAxis: { type: 'category', data: labels },
  yAxis: { type: 'value' },
  series: datasets.map(d => ({ name: d.name, type: 'line', smooth: true, data: d.data })) }
```

**饼图 (pie)**：
```js
{ tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' }, legend: { orient: 'vertical', left: 'left' }, color: COLORS,
  series: [{ name: 系列名, type: 'pie', radius: '60%',
    data: labels.map((l, i) => ({ name: l, value: firstDataset[i] })),
    emphasis: { itemStyle: { shadowBlur: 10 } } }] }
```

**环形图 (donut)**：
```js
// 同饼图，但 radius 改为 ['40%', '65%']，中心显示总计文字
{ ..., series: [{ ..., radius: ['40%', '65%'],
    label: { show: true },
    emphasis: { label: { show: true, fontSize: 16, fontWeight: 'bold' } } }] }
```

切换函数 `switchChart(type)` 调用 `chart.setOption(buildOption(type), true)` 实现无刷新切换。

### 第四步：在浏览器中打开

执行 Bash 命令：
```bash
open /tmp/viz-table-output.html
```

### 第五步：告知用户

输出简短确认：
> "已生成图表并在浏览器中打开：`/tmp/viz-table-output.html`"
> 同时说明数据概况：X 行数据，Y 个数值列。
