---
name: weather-query-zrr
description: 查询全球城市实时天气信息，支持当前天气、未来预报和空气质量查询。基于 wttr.in 和 Open-Meteo API，无需 API Key。Use this skill when user asks about weather, temperature, forecast, or air quality for any city.
tags: [weather, forecast, api, query]
---

# Weather Query

## 概述

查询全球城市天气信息的技能。支持三种查询模式：当前天气、未来3天预报、空气质量。默认使用 wttr.in（无需 API Key），也支持 Open-Meteo API 作为备选数据源。

## 前置条件

- Python 3.10+（系统自带）
- `requests` 库（`pip install requests`）
- 网络可访问 wttr.in 或 api.open-meteo.com

## 核心命令

### 查询当前天气

```bash
python3 scripts/weather.py --city "Beijing" --mode current
```

### 查询未来预报

```bash
python3 scripts/weather.py --city "Shanghai" --mode forecast
```

### 查询空气质量

```bash
python3 scripts/weather.py --city "Guangzhou" --mode air
```

### 指定数据源

```bash
python3 scripts/weather.py --city "Tokyo" --source open-meteo
```

## 参数确认

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| --city | 是 | - | 城市名（支持中英文，如 "北京" / "Beijing"） |
| --mode | 否 | current | 查询模式: current / forecast / air |
| --source | 否 | wttr | 数据源: wttr / open-meteo |
| --lang | 否 | zh | 输出语言: zh / en |
| --format | 否 | text | 输出格式: text / json |

## 输出格式

### current 模式

```
🏙️ 北京 (Beijing)
🌡️ 温度: 28°C (体感 30°C)
💧 湿度: 65%
🌬️ 风速: 12 km/h 东南风
☁️ 天气: 多云
👁️ 能见度: 10 km
```

### forecast 模式

```
🏙️ 上海 未来3天预报:
📅 今天: 30°C / 22°C ☀️ 晴
📅 明天: 28°C / 21°C ⛅ 多云
📅 后天: 25°C / 19°C 🌧️ 小雨
```

### air 模式

```
🏙️ 广州 空气质量:
🟢 AQI: 52 (良)
PM2.5: 35 μg/m³
PM10: 58 μg/m³
O₃: 42 μg/m³
```

## 验证方法

```bash
# 验证脚本可执行
python3 scripts/weather.py --city "Beijing" --mode current

# 验证 JSON 输出
python3 scripts/weather.py --city "Beijing" --format json

# 验证中文名查询
python3 scripts/weather.py --city "深圳" --mode forecast
```

## 最佳实践

- 城市名优先使用英文，中文城市名会自动转换
- wttr.in 对中国城市支持较好，Open-Meteo 对欧美城市更精确
- 批量查询时建议加 `--format json` 方便程序解析
- wttr.in 有频率限制，批量查询建议间隔 1 秒

## 参考文档

- [wttr.in](https://wttr.in/) — 基于终端的天气服务
- [Open-Meteo API](https://open-meteo.com/en/docs) — 免费天气 API
- [城市名映射](https://github.com/chubin/wttr.in#internationalization) — wttr.in 多语言支持

## 注意事项

- wttr.in 为公共服务，偶尔不稳定，可切换 `--source open-meteo`
- 空气质量数据仅 Open-Meteo 支持，wttr.in 的 air 模式会自动切换数据源
- 中国部分小城市可能无法查询，建议使用地级市名称
