# API 参考（用于编程调用）

如果你希望将 Scenario Forecaster 集成到自己的应用（如 Python 脚本、Web 服务），可以使用以下接口规范。

## 请求格式（JSON）

```json
{
  "event_description": "string (required)",
  "time_horizon": "string (default: '3 months')",
  "focus_dimensions": ["economic", "political", "social", "technological", "environmental", "legal"],
  "confidence_threshold": 0.1,
  "num_paths": 5
}
```

## 响应格式（JSON）

```json
{
  "summary": "事件摘要",
  "data_sources": [
    {"name": "Reuters", "credibility": "high", "key_facts": ["..."]}
  ],
  "drivers": [
    {"name": "通胀数据", "current_state": "2.8%", "uncertainty": "high"}
  ],
  "paths": [
    {
      "name": "软着陆降息",
      "probability": 0.45,
      "trigger_conditions": ["核心PCE降至2.5%以下"],
      "milestones": [{"time": "6月", "event": "首次降息25bp"}],
      "impact": "科技股上涨8~12%"
    }
  ],
  "outcomes": [...],
  "risk_opportunity": {...},
  "recommendations": {...}
}
```

## Python 调用示例

```python
import requests

url = "https://your-api.com/scenario-forecaster"
payload = {
    "event_description": "未来6个月美联储降息对全球科技股的影响",
    "time_horizon": "6 months",
    "focus_dimensions": ["economic", "technological"]
}
response = requests.post(url, json=payload)
report = response.json()
print(report["paths"][0]["name"])
```

## 注意

- 实际部署时需要实现真实的数据抓取模块（新闻API、Twitter API等）。
- 推荐使用 serpapi、newsdata.io、gnews 等聚合服务。
