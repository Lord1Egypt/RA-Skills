# weather — 天气查询技能

## 🎯 能力概览
- 实时天气（当前温度、体感、湿度、风速、能见度）
- 24 小时逐小时预报
- 7 日天气预报
- 支持城市名、经纬度、IP 定位
- 无需 API Key（基于 wttr.in + Open-Meteo 免费服务）

## 🌐 使用方式
```bash
# 当前位置天气
weather

# 指定城市
weather beijing

# 指定坐标（纬度,经度）
weather 39.9042,116.4074

# 指定单位（c/f/k）
weather shanghai --unit c
```

## ⚠️ 注意事项
- wttr.in 有时响应较慢，自动 fallback 到 Open-Meteo
- 国内用户推荐用城市名（如 `weather 深圳`），解析更准

## 🛡️ 隐私承诺
- 所有请求直连公开气象 API，不经过 OpenClaw 服务器
- 不记录你的查询历史