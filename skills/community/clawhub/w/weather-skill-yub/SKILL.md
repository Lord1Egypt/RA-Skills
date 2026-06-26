---
name: weather-query
version: 1.0.0
description: 查询全球任意城市天气，支持中文城市名
author: AIStudio
homepage: https://example.com/weather-query-skill
---

# Weather Query Skill

基于 wttr.in 的天气查询技能，支持离线测试模式。

## 功能

- 查询指定城市天气
- 支持中文城市名
- 返回温度、湿度、天气状况
- 支持 `--offline` 演示模式，便于无网验证

## 使用

```powershell
python scripts/weather.py 北京
python scripts/weather.py 北京 --offline
```

## 安装

```bash
clawhub install your-name/weather-query
```
