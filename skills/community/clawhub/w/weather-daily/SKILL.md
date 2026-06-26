---
name: weather-daily
description: "Daily weather briefing for any city — morning conditions, what to wear, umbrella forecast, evening preview, extreme weather alerts. No API key. Works worldwide."
keywords: 
  - 天气
  - 今天天气
  - 明天天气
  - 天气预报
  - 本周天气
  - 一周天气
  - 穿衣建议
  - 穿衣指数
  - 下雨吗
  - 带伞吗
  - 空气质量
  - AQI
  - 空气污染
  - 极端天气
  - 台风
  - 暴雨
  - 寒潮
  - 高温
  - 下雪
  - 每日推送
  - 天气提醒
  - weather
  - forecast
  - today weather
  - tomorrow weather
  - daily weather
  - weather forecast
  - weekly forecast
  - weather alert
  - air quality
  - AQI
  - temperature
  - rain
  - snow
  - typhoon
  - extreme weather
metadata:
  openclaw:
    runtime:
      node: ">=18"
    tags:
      - weather
      - 天气
      - 天气预报
      - 推送
      - daily
---

# weather-daily

> 私人天气助手 — 早间实况 · 晚间预告 · 一周预报 · 极端预警

## 何时使用

- 用户说"今天天气""天气怎么样""下雨吗""穿什么"
- 用户问"明天天气""明天冷吗""要带伞吗"
- 用户说"本周天气""天气预报""这周有雨吗"
- 用户问"空气质量""AQI""今天适合出门吗"
- 用户说"开启天气推送""订阅天气""每天推天气"
- 用户说"下周天气""这周末出去玩合适吗"
- 用户说"下个月天气""下个月适合旅游吗"

---

## 📋 功能说明

| 指令 | 脚本 | 说明 |
|------|------|------|
| 今日天气 | `morning-push.js <userId>` | 今日温度/湿度/风力/分时预报/穿衣/出行建议 |
| 明日预告 | `evening-push.js <userId>` | 明日天气预告 + 提醒 + 后天预览 |
| 一周预报 | `forecast.js <userId>` | 未来7天逐日天气 + 趋势 + 穿衣建议 |
| 下周周报 | `weekly-push.js <userId>` | 每周六推送下周天气 + 最佳出行日 |
| 月度概况 | `monthly-push.js <userId>` | 每月末推送下月气候 + 分旬预测 |
| 开启推送 | `push-toggle.js on <userId>` | 定时推送（早/晚/周报/月报） |
| 关闭推送 | `push-toggle.js off <userId>` | 停止全部推送 |
| 推送状态 | `push-toggle.js status <userId>` | 查看当前推送配置 |

---

## 🌤️ 早间天气内容

每日早间推送（默认 07:00），包含：

- 今日温度区间、天气状况、湿度、风力风向
- 日出/日落时间
- 分时预报（早晨/上午/下午/夜间）
- 空气质量（AQI + 等级）
- 穿衣建议、出行建议
- 极端天气提醒

---

## 🌙 晚间天气内容

每日晚间推送（默认 21:00），包含：

- 明日温度、天气状况、湿度、风力
- 出行/穿衣/雨伞等具体提醒
- 极端天气预警（如有）
- 后天天气一句话预览

---

## ⚠️ 支持的预警类型

| 类型 | 说明 |
|------|------|
| 🌧️ 降雨 | 中雨/大雨/暴雨预警 |
| ❄️ 降雪 | 小雪/大雪/暴雪预警 |
| 💨 大风 | 6级以上大风预警 |
| 🌀 台风 | 台风路径与影响范围 |
| 🥶 寒潮 | 大幅降温预警 |
| 🔥 高温 | 35°C+ 高温预警 |
| 🌫️ 空气质量 | AQI 重度污染预警 |

---

## 🔧 脚本说明

### 注册用户

```bash
node scripts/register.js <userId> <city> [units] [morningTime] [eveningTime]
# 示例：
node scripts/register.js alice 上海
node scripts/register.js bob Beijing imperial 08:00 22:00
```

### 推送管理

```bash
node scripts/push-toggle.js on <userId> [--morning 07:00] [--evening 21:00] [--channel telegram]
node scripts/push-toggle.js off <userId>
node scripts/push-toggle.js status <userId>
```

支持渠道：`telegram` / `feishu` / `slack` / `discord`

---

## ⚠️ 注意事项

1. 使用前须先注册：`node scripts/register.js <userId> <city>`
2. 无需 API Key，天气数据通过 WebSearch 实时搜索获取
3. 用户偏好存储在 `data/users/<userId>.json`，仅含城市/单位/时间等配置，不含天气内容
4. 搜索结果受 WebSearch 实时性限制，极端天气预警以官方气象部门发布为准
