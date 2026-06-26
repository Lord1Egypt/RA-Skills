---
name: tianqi
description: "Get current weather and forecasts via wttr.in and Open-Meteo. Use when: user asks in Chinese about weather, temperature, rain, wind, or short-range forecasts for a city or region. Prefer Chinese place names, Chinese summaries, and Celsius-based answers. Use wttr.in for quick text lookups and Open-Meteo for structured forecast data or geocoding fallback."
homepage: https://wttr.in/:help
metadata: { "openclaw": { "emoji": "🌦️", "requires": { "bins": ["curl"] } } }
---

# Tianqi Skill

面向中文用户的天气查询技能。

默认用中文回答，优先使用中文地名、摄氏度，以及“今天/明天/后天/周末”这类中文表达。

## 适用场景

- "北京今天天气怎么样？"
- "上海明天会下雨吗？"
- "深圳这周气温"
- "查一下某个城市的天气预报"
- "周末去杭州要不要带伞？"
- 出行前快速看天气

## 不适用场景

- 历史天气数据 → 改用气象归档或数据集
- 气候趋势分析 → 改用专门数据源
- 严重天气预警 → 改用官方预警渠道
- 航空气象、海洋气象 → 改用专门服务

## 地点习惯

- 优先使用中文地名。
- 地名有歧义时，补充到“省/市/区县”级别。
- 中国用户常见问法里，“朝阳”“长安”“鼓楼”这类重名地点要先确认具体城市。
- 如果用户只说“我这里”“老家”“公司那边”，先追问具体地点。

## 数据源选择

- 用 `wttr.in` 做快速文本天气查询，适合“今天天气怎么样”“现在多少度”。
- 用 Open-Meteo 做结构化预报，适合“明天会不会下雨”“未来三天气温”“降水概率”。
- 如果 `wttr.in` 地名识别不稳定，先用 Open-Meteo 地理编码确认经纬度，再查预报。
- 一个源失败时直接切另一个，不要卡住。

## 回复习惯

- 默认中文总结，不照抄英文原文。
- 温度默认用摄氏度。
- 优先说清楚：天气现象、当前温度、体感、最高/最低温、降水概率、风。
- 对“要不要带伞”“穿什么”这类问题，可以基于天气给简短建议，但不要装作有精细生活场景判断。
- 如果来源或地点不确定，要明确说出来。

## wttr.in 示例

```bash
# One-line summary
curl "wttr.in/北京?format=3"

# 更详细的当前天气
curl "wttr.in/北京?0"

# 明天
curl "wttr.in/上海?1"

# 周视图
curl "wttr.in/杭州?format=v2"

# 自定义一行摘要
curl -s "wttr.in/深圳?format=%l:+%c+%t+(体感+%f),+风%w,+湿度%h"

# JSON
curl "wttr.in/北京?format=j1"
```

## Open-Meteo 示例

```bash
# 用中文地名地理编码，减少重名地点误判
curl --get "https://geocoding-api.open-meteo.com/v1/search" \
  --data-urlencode "name=北京" \
  --data "count=5" \
  --data "language=zh" \
  --data "format=json"
```

```bash
# 结构化天气预报
curl "https://api.open-meteo.com/v1/forecast?latitude=39.9042&longitude=116.4074&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum&forecast_days=3&timezone=auto"
```

## 常见问法处理

- “今天天气怎么样？”
  优先用 `wttr.in` 给一个快摘要。
- “明天会下雨吗？”
  优先用 Open-Meteo 看 `precipitation_probability_max` 和 `precipitation_sum`。
- “周末去杭州要不要带伞？”
  看未来两三天降水概率和降水量，再给一句简短建议。
- “深圳这周冷不冷？”
  概括未来几天最高/最低温波动，不必把每天都铺开。

## 返回内容

- 当前天气概况
- 当前温度和体感温度
- 最高/最低温
- 降水概率或降水趋势
- 风况
- 未来 2 到 3 天重点变化
- 必要时标注使用的数据源

## 注意事项

- 不需要 API key。
- `wttr.in` 适合快查，Open-Meteo 适合结构化字段。
- 对中文重名地名，先确认，不要猜。
- 回答时优先保留中文地名，不要无故改成英文城市名。
