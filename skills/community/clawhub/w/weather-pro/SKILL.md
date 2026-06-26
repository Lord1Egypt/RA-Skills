---
name: weather
description: "Get weather, air quality, sunrise/sunset, golden/blue hour times, and sunrise/sunset glow quality forecasts (朝霞晚霞预测). Perfect for photographers and outdoor planning."
homepage: https://wttr.in/:help
metadata:
  openclaw:
    emoji: "☔"
    requires:
      bins: ["curl", "jq"]
      env_optional: ["WEATHERAPI_KEY", "SUNSETHUE_KEY"]
---

# Weather Pro

天气查询 + 朝霞晚霞预测

## 快速使用

**查天气（含霞光预测）**

```bash
~/.openclaw/workspace/skills/weather-pro/scripts/weather-full.sh 北京
```

**参数说明**
- 第一个参数：城市名（英文，如 Beijing, Shanghai）
- 第二个参数（可选）：预报天数，默认 1

## 支持城市

| 城市 | 英文名 |
|------|--------|
| 北京 | Beijing |
| 上海 | Shanghai |
| 秦皇岛 | Qinhuangdao |
| 广州 | Guangzhou |
| 深圳 | Shenzhen |
| 杭州 | Hangzhou |
| 成都 | Chengdu |
| 苏州 | Suzhou |
| 南京 | Nanjing |

## 输出格式

```
[城市]天气 [日期]

🌡️ 温度：最低 ~ 最高
🌬️ 风力：风向 风级
☁️ 天况：晴/多云/雨
💧 湿度：百分比
🌫️ 空气质量：PM2.5 数值

🌅 日出：HH:MM
🌇 日落：HH:MM

🌅 朝霞质量：分数 (等级)
🌇 晚霞质量：分数 (等级)
```

## 霞光评分参考

| 分数 | 等级 | 建议 |
|-----|------|------|
| 80-100 | Excellent | 强烈推荐 🌟 |
| 60-79 | Good | 值得去 ✨ |
| 40-59 | Fair | 可能有色彩 |
| 0-39 | Poor | 不建议 |

## API 来源

- **WeatherAPI** — 天气数据
- **Sunsethue** — 朝霞晚霞质量预测

## 原始命令（不使用脚本）

<details>
<summary>点击展开</summary>

### 当前天气

```bash
source ~/.openclaw/.env && curl -s "https://api.weatherapi.com/v1/forecast.json?key=${WEATHERAPI_KEY}&q=Beijing&days=1&lang=zh&aqi=yes" | jq '{
  location: .location.name,
  temp: .current.temp_c,
  condition: .current.condition.text,
  humidity: .current.humidity,
  pm25: .current.air_quality.pm2_5
}'
```

### 晚霞预测

```bash
source ~/.openclaw/.env && curl -s "https://api.sunsethue.com/event?latitude=39.90&longitude=116.41&date=$(date +%Y-%m-%d)&type=sunset&key=${SUNSETHUE_KEY}" | jq '{
  quality: (.data.quality * 100 | floor),
  rating: .data.quality_text
}'
```

</details>
