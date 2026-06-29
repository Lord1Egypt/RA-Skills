# series.radar - 雷达图
Source: https://echarts.apache.org/zh/option.html#series-radar

雷达图配置。

示例:
```json
{"radar": {"indicator": [{"name": "技术", "max": 100}]},
 "series": [{"type": "radar",
   "data": [{"value": [90, 75], "name": "Score"}]}]}
```

radar.indicator: 维度定义 {name, max}
series.data.value: 各维度数值数组
