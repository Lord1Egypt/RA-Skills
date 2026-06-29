# series.pie - 饼图
Source: https://echarts.apache.org/zh/option.html#series-pie

饼图/环形图配置。

示例:
```json
{"type": "pie", "radius": ["40%", "70%"],
 "data": [{"value": 48, "name": "Chrome"}],
 "label": {"formatter": "{b}\n{d}%"},
 "emphasis": {"label": {"fontSize": 16}},
 "itemStyle": {"borderRadius": 8, "borderWidth": 2}}
```

radius: ["内圈%", "外圈%"] - 设置成环形
label.formatter: {b}=名称 {c}=值 {d}=百分比
