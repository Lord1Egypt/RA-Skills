# series.bar - 柱状图
Source: https://echarts.apache.org/zh/option.html#series-bar

柱状图配置。

示例:
```json
{"type": "bar", "data": [30, 80, 45],
 "itemStyle": {"borderRadius": [4,4,0,0]},
 "label": {"show": true, "position": "top"}}
```

需要同时配置 xAxis(type:category) 和 yAxis(type:value)
itemStyle.borderRadius: [上左, 上右, 下右, 下左]
