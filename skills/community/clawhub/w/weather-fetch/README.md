# 🌤️ Weather Fetch - 中国天气抓取工具

从 weathercn.com 抓取中国城市实时天气数据，支持全国城市。

## 功能

- 支持全国城市天气查询（苍南、梧州等）
- 提取温度、湿度、气压、能见度等数据
- 日出日落时间
- AQI空气质量指数
- 使用 Playwright 自动化抓取

## 使用方法

```bash
python3 scripts/weather_fetch.py 城市名
```

## 示例

```bash
python3 scripts/weather_fetch.py 苍南
python3 scripts/weather_fetch.py 梧州
```

## 输出格式

```json
{
  "city": "苍南县",
  "temp": "20",
  "temp_high": "26",
  "temp_low": "18",
  "weather": "阴",
  "humidity": "66",
  "feels_like": "19",
  "pressure": "1011",
  "visibility": "22.0",
  "wind": "西南风3级",
  "sunrise": "05:19",
  "sunset": "18:32",
  "aqi": "41",
  "aqi_level": "优"
}
```

## 打赏支持

如果觉得好用，欢迎支持米米的服务器费用！

GitHub: https://github.com/wNDAGG/mimi-scripts
