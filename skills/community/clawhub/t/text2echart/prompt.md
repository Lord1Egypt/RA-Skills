# Prompt Engineering Guide — text2echart

> 指导 LLM 将用户自然语言需求转化为 ECharts 配置项，最终生成图表。
> Target: conversational LLMs (Claude, GPT, Kimi)

---

## Core Prompt Pattern

```
You are a chart configuration expert. Given a user's data and visualization request,
output a valid ECharts option JSON that can be rendered by:
  - CLI: node cli.js <option.json>
  - Web: paste into text2echarts.html

Rules:
1. Output ONLY valid JSON, no markdown code fences unless asked
2. Include all necessary fields (title, xAxis, yAxis, series, tooltip)
3. Use double quotes for strings
4. Strings containing function code must be wrapped in quotes
5. Test your output: the JSON.parse result must be a valid ECharts option
```

---

## Chain-of-Thought for Chart Selection

When the user describes their data, reason step by step:

```
User data description: [user input]

1. DATA STRUCTURE: What dimensions? (categories, values, time series?)
   - Categories + single value → bar or pie
   - Time + value → line
   - Multi-dimension → radar
   - x,y pairs → scatter
   - Words + frequency → wordcloud

2. COMPARISON TYPE:
   - Compare categories → bar
   - Show distribution → pie
   - Show trend → line
   - Show correlation → scatter
   - Multi-faceted → radar
   - Keywords → wordcloud

3. DECIDE chart type: [type]

4. CONSTRUCT option JSON
```

---

## ECharts Option Template

### Complete Structure

```json
{
  "title": {"text": "Chart Title", "left": "center"},
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["Series1"], "bottom": "0"},
  "grid": {"left": "3%", "right": "4%", "bottom": "10%", "containLabel": true},
  "xAxis": {"type": "category", "data": ["Cat1", "Cat2"]},
  "yAxis": {"type": "value", "name": "Unit"},
  "series": [
    {"name": "Series1", "type": "bar", "data": [30, 80]}
  ]
}
```

### Example 1: Bar Chart

User: *"Show me monthly sales: Jan 1200, Feb 900, Mar 1600"*

```json
{
  "title": {"text": "Monthly Sales", "left": "center"},
  "tooltip": {"trigger": "axis"},
  "grid": {"left": "3%", "right": "4%", "bottom": "10%", "containLabel": true},
  "xAxis": {"type": "category", "data": ["Jan", "Feb", "Mar"]},
  "yAxis": {"type": "value", "name": "Revenue"},
  "series": [{
    "type": "bar", "data": [1200, 900, 1600],
    "itemStyle": {"borderRadius": [4, 4, 0, 0]},
    "label": {"show": true, "position": "top"}
  }]
}
```

### Example 2: Donut Pie

User: *"Market share: Chrome 48%, Firefox 22%, Safari 18%"*

```json
{
  "title": {"text": "Market Share", "left": "center"},
  "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
  "series": [{
    "type": "pie",
    "radius": ["40%", "70%"],
    "data": [
      {"value": 48, "name": "Chrome"},
      {"value": 22, "name": "Firefox"},
      {"value": 18, "name": "Safari"}
    ],
    "label": {"show": true, "formatter": "{b}\\n{d}%", "fontSize": 13},
    "emphasis": {"label": {"fontSize": 16, "fontWeight": "bold"}},
    "itemStyle": {"borderRadius": 8, "borderWidth": 2}
  }]
}
```

### Example 3: Multi-series Line

User: *"Temperature trend: Mon 22°, Tue 25°, Wed 23°"*

```json
{
  "title": {"text": "Temperature", "left": "center"},
  "tooltip": {"trigger": "axis"},
  "grid": {"left": "3%", "right": "4%", "bottom": "10%", "containLabel": true},
  "xAxis": {"type": "category", "data": ["Mon", "Tue", "Wed"]},
  "yAxis": {"type": "value", "name": "°C"},
  "series": [{
    "type": "line", "data": [22, 25, 23],
    "smooth": true,
    "areaStyle": {"opacity": 0.1},
    "lineStyle": {"width": 3, "shadowBlur": 10}
  }]
}
```

---

## Common Mistakes to Avoid

| Mistake | Wrong | Right |
|---------|-------|-------|
| title as string | `"title": "Sales"` | `"title": {"text": "Sales"}` |
| Missing xAxis type | `"xAxis": {"data": [...]}` | `"xAxis": {"type": "category", "data": [...]}` |
| Missing containLabel | `"grid": {"left": "3%"}` | `"grid": {"left": "3%", "containLabel": true}` |
| Pie without % formatter | No tooltip formatter | `"formatter": "{b}: {c} ({d}%)"` |
| Bar without xAxis category | Missing xAxis type | `"xAxis": {"type": "category", ...}` |
| Scatter wrong data format | `"data": [{"x":1,"y":2}]` | `"data": [[1, 2]]` |
| Invalid JSON (trailing comma) | `{"a": 1,}` | `{"a": 1}` |
| Single quotes | `{"a": 'hello'}` | `{"a": "hello"}` |

---

## Advanced: Data Transformation

For complex data that needs pre-processing before charting:

```
Step 1: Parse the raw data (CSV, text, table)
Step 2: Transform to ECharts series format
Step 3: Choose appropriate chart type
Step 4: Generate option JSON
```

**CSV Input Example:**
```
Month,Revenue,Cost
Jan,1200,800
Feb,1500,900
```

→ Multiple series:
```json
{
  "xAxis": {"type": "category", "data": ["Jan", "Feb"]},
  "series": [
    {"name": "Revenue", "type": "bar", "data": [1200, 1500]},
    {"name": "Cost", "type": "bar", "data": [800, 900]}
  ]
}
```

---

## Prompt Template for End Users

Copy this into your chat with any LLM:

```
You are an ECharts chart generator.
I will describe data and a chart type. You output ONLY valid ECharts option JSON.

Chart types available: bar, line, pie, scatter, radar, wordcloud.
- bar: needs xAxis(type:category) + yAxis + series(type:bar)
- line: same as bar + series(type:line), smooth recommended
- pie: needs series(type:pie, radius:["40%","70%"]), data as [{value,n}]
- scatter: needs xAxis(type:value) + yAxis(type:value), data as [[x,y]]
- radar: needs radar.indicator + series(type:radar)
- wordcloud: needs series(type:wordCloud, data:[{name,value}])

Always include: title, tooltip, grid({containLabel:true}).

My request: [USER INPUT HERE]
```

---

## Workflow Integration

```
User: "帮我画个柱状图显示销量"
  1. LLM applies prompt.md
  2. Constructs ECharts option JSON
  3. Output 1: JSON for CLI (node cli.js)
     Output 2: Full HTML for web
     Output 3: Direct HTML string (save as .html)

Best path for end users:
  User → LLM (with this prompt) → HTML string → save as .html → open in browser
```



## Few-Shot Examples

### Example 1: Bar Chart

User: *"Show me monthly sales: Jan 1200, Feb 900, Mar 1600"*

```json
{
  "title": {"text": "Monthly Sales", "left": "center"},
  "tooltip": {"trigger": "axis"},
  "grid": {"left": "3%", "right": "4%", "bottom": "10%", "containLabel": true},
  "xAxis": {"type": "category", "data": ["Jan", "Feb", "Mar"]},
  "yAxis": {"type": "value", "name": "Revenue"},
  "series": [{
    "type": "bar", "data": [1200, 900, 1600],
    "itemStyle": {"borderRadius": [4, 4, 0, 0]},
    "label": {"show": true, "position": "top"}
  }]
}
```

### Example 2: Donut Pie

User: *"Market share: Chrome 48%, Firefox 22%, Safari 18%"*

```json
{
  "title": {"text": "Market Share", "left": "center"},
  "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
  "series": [{
    "type": "pie", "radius": ["40%", "70%"],
    "data": [
      {"value": 48, "name": "Chrome"},
      {"value": 22, "name": "Firefox"},
      {"value": 18, "name": "Safari"}
    ],
    "label": {"show": true, "formatter": "{b}\
{d}%", "fontSize": 13},
    "emphasis": {"label": {"fontSize": 16, "fontWeight": "bold"}},
    "itemStyle": {"borderRadius": 8, "borderWidth": 2}
  }]
}
```

### Example 3: Multi-series Line

User: *"Temperature trend: Mon 22°, Tue 25°, Wed 23°"*

```json
{
  "title": {"text": "Temperature", "left": "center"},
  "tooltip": {"trigger": "axis"},
  "grid": {"left": "3%", "right": "4%", "bottom": "10%", "containLabel": true},
  "xAxis": {"type": "category", "data": ["Mon", "Tue", "Wed"]},
  "yAxis": {"type": "value", "name": "°C"},
  "series": [{
    "type": "line", "data": [22, 25, 23],
    "smooth": true,
    "areaStyle": {"opacity": 0.1},
    "lineStyle": {"width": 3, "shadowBlur": 10}
  }]
}
```


## Detailed Option Reference

Each option includes its official docs URL and concrete JSON example.

### title
URL: https://echarts.apache.org/zh/option.html#title
```json
{"text": "销售额", "left": "center", "textStyle": {"fontSize": 18}}
```
Properties: text(string), subtext(string), left/right/top/bottom, textStyle({fontSize,color,fontWeight})

### grid
URL: https://echarts.apache.org/zh/option.html#grid
```json
{"left": "3%", "right": "4%", "bottom": "10%", "containLabel": true}
```
⚠️ containLabel: true prevents axis labels from being clipped.

### xAxis
URL: https://echarts.apache.org/zh/option.html#xAxis
```json
{"type": "category", "data": ["Jan", "Feb"], "axisLabel": {"rotate": 45}}
```
type: category(分类) | value(数值) | time(时间). axisLabel.rotate: 旋转角度(>10类建议45°).

### yAxis
URL: https://echarts.apache.org/zh/option.html#yAxis
```json
{"type": "value", "name": "万元"}
```
name: 坐标轴名称文字.

### series.bar
URL: https://echarts.apache.org/zh/option.html#series-bar
```json
{"type": "bar", "data": [30,80,45], "itemStyle": {"borderRadius": [4,4,0,0]}, "label": {"show":true, "position":"top"}}
```
Requires xAxis(type:category) + yAxis(type:value). borderRadius: [topL, topR, bottomR, bottomL].

### series.line
URL: https://echarts.apache.org/zh/option.html#series-line
```json
{"type": "line", "data": [22,25,23], "smooth":true, "areaStyle":{"opacity":0.1}, "lineStyle":{"width":3,"shadowBlur":10}}
```
smooth: true=曲线. areaStyle: 填充区域.

### series.pie
URL: https://echarts.apache.org/zh/option.html#series-pie
```json
{"type":"pie","radius":["40%","70%"],"data":[{"value":48,"name":"Chrome"}],"label":{"formatter":"{b}\
{d}%"},"emphasis":{"label":{"fontSize":16}}}
```
radius: ["内圈%","外圈%"]→环形. label.formatter: {b}=名称 {c}=值 {d}=百分比.

### series.scatter
URL: https://echarts.apache.org/zh/option.html#series-scatter
```json
{"type":"scatter","data":[[160,55],[170,65]],"symbolSize":12}
```
data format: [[x1,y1], [x2,y2], ...]

### series.radar
URL: https://echarts.apache.org/zh/option.html#series-radar
```json
{"radar":{"indicator":[{"name":"技术","max":100}]},"series":[{"type":"radar","data":[{"value":[90,75],"name":"Score"}]}]}
```
radar.indicator: 维度定义{name,max}. series.data.value: 各维度数值数组.

### tooltip
URL: https://echarts.apache.org/zh/option.html#tooltip
```json
{"trigger":"axis","formatter":"{b}: {c}"}
```
trigger: axis(bar/line) | item(pie/scatter). formatter: {a}=系列名 {b}=数据名 {c}=数值 {d}=%.

### legend
URL: https://echarts.apache.org/zh/option.html#legend
```json
{"data":["销售额","利润"],"bottom":"0"}
```
data must match series[].name values.

### color
URL: https://echarts.apache.org/zh/option.html#color
```json
["#5470c6","#91cc75","#fac858","#ee6666","#73c0de"]
```
Default 5-color palette. Cycles when series > 5.

### label
URL: https://echarts.apache.org/zh/option.html#series-bar.label
```json
{"show":true,"position":"top","formatter":"{c}","fontSize":14}
```
position: top | inside | outside.

### emphasis
URL: https://echarts.apache.org/zh/option.html#series-pie.emphasis
```json
{"label":{"fontSize":16,"fontWeight":"bold"},"itemStyle":{"shadowBlur":10}}
```
Hover highlight state. Supports label/itemStyle/lineStyle.

### smooth
URL: https://echarts.apache.org/zh/option.html#series-line.smooth
```json
true
```
Line chart only. true=curved, false=polyline.

### axisLabel
URL: https://echarts.apache.org/zh/option.html#xAxis.axisLabel
```json
{"rotate":45,"interval":0,"fontSize":12}
```
rotate:防重叠. interval:0=全部显示.
