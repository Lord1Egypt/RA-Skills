# 前端展示 JSON 结构

```json
{
  "title": "节假日出行判断报告",
  "holiday_label": "2026 年五一劳动节（5/1 周五 - 5/5 周二） | 上海出发",
  "verdict": "这次不要去三亚，去冲绳更值。",
  "default_path": {
    "name": "三亚",
    "summary": "海边意图下，用户默认会先想到三亚。",
    "why_default": ["国内海边心智最强"],
    "why_not_optimal": ["节假日溢价高", "体验下降"]
  },
  "risk_matrix": [
    { "dimension": "拥挤度", "default_score": 9, "alternative_score": 5, "label": "冲绳更稳" }
  ],
  "crowd_reasons": {
    "history": "历年节假日规律",
    "hotspots": ["当前热点"],
    "structure": "集中型 / 分散型说明"
  },
  "recommendations": {
    "main": { "name": "冲绳", "type": "海边 / 放松", "why_better": "体验更完整", "fit_for": "预算 6000+" },
    "near": { "name": "泉州", "type": "海边 + 城市", "why_better": "国内更稳", "fit_for": "不想出国" },
    "far": { "name": "冲绳", "type": "海边度假", "why_better": "更值", "fit_for": "接受出境" }
  },
  "cost_comparison": [
    { "option": "三亚", "flight": "¥2200 - ¥3800", "hotel": "¥1200 - ¥2500/晚", "total": "¥6500 - ¥11000", "verdict": "高价高拥挤" },
    { "option": "冲绳", "flight": "¥2500 - ¥4200", "hotel": "¥700 - ¥1600/晚", "total": "¥6200 - ¥9800", "verdict": "不一定更贵" }
  ],
  "travel_window": {
    "leave_date": "4 月 30 日（周四）",
    "depart_date": "4 月 30 日（周四）",
    "return_date": "5 月 4 日（周一）",
    "duration": "5 天 4 晚",
    "flight_tip": "去程优先买 4/30，返程优先买 5/4",
    "hotel_tip": "冲绳常见度假酒店 ¥700 - ¥1600/晚"
  },
  "if_ignore": [
    "热门湾区明显拥挤",
    "预算抬高",
    "体验下降"
  ],
  "final_recommendation": "这次别按常规走，去冲绳比去三亚更值。"
}
```
