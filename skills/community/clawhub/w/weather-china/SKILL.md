---
name: weather-china
description: 中国天气预报查询 - 基于中国天气网(weather.com.cn)获取7天天气预报和生活指数数据。纯 Python 实现，无需 API Key。
version: 1.0.2
tags: [weather, china, forecast, chinese, weather-cn, life-index, 7day-forecast]
metadata: {"openclaw":{"emoji":"🌤️","requires":{"bins":["python3"]}}}
allowed-tools: [exec]
---

# 中国天气预报查询 (China Weather)

基于 [中国天气网](https://www.weather.com.cn) 获取 7 天天气预报和生活指数数据。纯 Python 实现，无需 API Key。

## Quick Usage

```bash
# 查询天气（格式化文本输出）
python3 skills/weather-china/lib/weather_cn.py query 南京
python3 skills/weather-china/lib/weather_cn.py query 北京
python3 skills/weather-china/lib/weather_cn.py query 成都

# JSON 输出（结构化数据）
python3 skills/weather-china/lib/weather_cn.py json 上海
```

## Example Output

```text
城市: 南京 (代码: 101190101)
数据来源: weather.com.cn
查询时间: 2026-03-04 16:31:55

[4日（今天）] 阴转多云, 10℃/5℃, 东风 4-5级转3-4级
  感冒指数: 易发 - 风较大，易发生感冒，注意防护。
  运动指数: 较适宜 - 风力较强且气温较低，请进行室内运动。
  过敏指数: 较易发 - 外出需远离过敏源，适当采取防护措施。
  穿衣指数: 冷 - 建议着棉衣加羊毛衫等冬季服装。
  洗车指数: 较不宜 - 风力较大，洗车后会蒙上灰尘。
  紫外线指数: 最弱 - 辐射弱，涂擦SPF8-12防晒护肤品。

[5日（明天）] 阴转多云, 11℃/4℃, 北风 3-4级
  感冒指数: 少发 - 无明显降温，感冒机率较低。
  ...
```

## Supported Cities

支持查询中国天气网覆盖的所有城市和地区。输入城市名称即可自动搜索匹配，无需手动配置。

常见城市（如北京、上海、广州、深圳、成都、杭州、南京等 60+ 城市）已内置代码，查询更快。其他城市会通过搜索接口自动查找城市代码。

## Data Available

- **7天预报**: 日期、天气状况、高/低温度、风向风力
- **生活指数**: 感冒、运动、过敏、穿衣、洗车、紫外线等

## Use Cases

当用户询问以下问题时使用本 skill：

- "今天天气怎么样"
- "明天会下雨吗"
- "[城市名]天气预报"
- "南京这周天气如何"
- "出门需要带伞吗"
- "穿什么衣服合适"

## Notes

1. **数据来源**: 中国天气网，数据可能略有延迟
2. **城市名称**: 使用标准城市名，如"成都"、"南京"
3. **网络依赖**: 需要能访问 <www.weather.com.cn>
4. **无需 API Key**: 直接解析天气网页面数据
