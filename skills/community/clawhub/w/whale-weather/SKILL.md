---
name: city-weather
description: 全球城市天气查询与对比工具。支持中英文城市名，具备多语言输出、动态数据源切换（Open-Meteo）及精准大城市定位功能。
version: 1.0.0
---

# city-weather 🐳

全球城市天气助手，支持实时天气、温度范围、降水概率及出行建议。

## 特色

- **全球覆盖**：支持中国省会、欧美大城市及全球主要地区的精准定位。
- **多语言支持**：可根据需求输出中文（zh）或英文（en）结果。
- **智能建议**：提供实用的穿衣及带伞建议。
- **高可用性**：内置数据源容错与精准行政区划筛选。

## 适用示例

- `杭州天气` / `London weather`
- `北京和上海天气对比`
- `Los Angeles and New York weather`
- `今天要不要带伞？`

## 工具使用说明

> **注意**：脚本执行时需以本 skill 目录为工作目录。

### 1. 查询单个城市
参数 1 为城市名，参数 2 为语言代码（默认 zh）。
```bash
bash scripts/get_weather.sh "杭州" "zh"
bash scripts/get_weather.sh "Los Angeles" "en"
```

### 2. 对比多个城市
支持多个城市名，若最后一个参数为 2 位语言代码，则按该语言输出。
```bash
bash scripts/compare_weather.sh "北京" "杭州" "zh"
bash scripts/compare_weather.sh "London" "Paris" "en"
```
