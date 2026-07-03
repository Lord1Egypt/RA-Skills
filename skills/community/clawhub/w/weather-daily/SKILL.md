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
license: MIT-0
compatibility:
  platforms:
    - claude-code
    - claude-ai
    - api
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

> 城市/单位/语言等资料由 Agent 从 MEMORY.md 读出后作为 `--city/--units/--lang` 参数传入（见下方「用户资料」）。

| 指令 | 脚本 | 说明 |
|------|------|------|
| 今日天气 | `morning-push.js <userId> --city <城市> --units <..> --lang <..>` | 今日温度/湿度/风力/分时预报/穿衣/出行建议 |
| 明日预告 | `evening-push.js <userId> --city <城市> ...` | 明日天气预告 + 提醒 + 后天预览 |
| 一周预报 | `forecast.js <userId> --city <城市> ...` | 未来7天逐日天气 + 趋势 + 穿衣建议 |
| 下周周报 | `weekly-push.js <userId> --city <城市> ...` | 每周六推送下周天气 + 最佳出行日 |
| 月度概况 | `monthly-push.js <userId> --city <城市> ...` | 每月末推送下月气候 + 分旬预测 |
| 开启推送 | `push-toggle.js on <userId> --city <城市> ...` | 定时推送（早/晚/周报/月报），资料烘焙进 cron |
| 关闭推送 | `push-toggle.js off <userId>` | 停止全部推送 |
| 推送状态 | `push-toggle.js status <userId>` | 提示从 MEMORY.md 查看推送配置 |

---

## 📇 用户资料 (存于原生 MEMORY.md，脚本不落盘)

本 skill **不向磁盘写任何用户数据**。用户的城市、单位、语言、推送时间、时区全部保存在 OpenClaw 原生 **MEMORY.md** 中，由 Agent 读写、跨会话保留。

**流程：**

1. 新用户 → 运行 `register.js`，它会输出一段 `<!-- weather-daily:profile:<userId> -->` markdown 区块。**把该区块写入 MEMORY.md。**
2. 后续会话 / 手动查询 → 先**读取 MEMORY.md** 中该区块拿到城市/单位/语言，作为 `--city/--units/--lang` 参数传给推送脚本。
3. 开启推送 → 把城市/单位/语言作为参数传给 `push-toggle.js on`，这些字段会被**烘焙进 cron 任务命令**，使无头定时推送无需读取任何文件。
4. 修改城市 / 单位 → 更新 MEMORY.md 区块，并重新运行 `push-toggle.js on` 覆盖 cron。

资料区块格式示例：

```markdown
<!-- weather-daily:profile:alice -->
## Weather profile · alice
- userId: alice
- city: 上海
- units: °C / metric
- language: 中文 (zh)
- morningTime: 07:00
- eveningTime: 21:00
- timezone: Asia/Shanghai
- push: enabled telegram 07:00/21:00
<!-- /weather-daily:profile -->
```

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

## 🔧 脚本说明（全部纯计算，无文件写入）

### 注册用户（输出 MEMORY.md 资料区块，由 Agent 写入原生记忆）

```bash
node scripts/register.js <userId> <city> [units] [morningTime] [eveningTime] [language] [timezone]
# 示例：
node scripts/register.js alice 上海
node scripts/register.js bob "New York" imperial 08:00 22:00 en America/New_York
```

register 不写任何文件；它打印一段 `<!-- weather-daily:profile:<userId> -->` 区块，请存入 MEMORY.md。

### 推送管理（城市/单位/语言从 MEMORY.md 读出作为参数；cron 由运行时管理）

```bash
node scripts/push-toggle.js on <userId> --city <城市> [--units metric|imperial] [--lang zh|en] \
     [--morning 07:00] [--evening 21:00] [--channel telegram] [--timezone Asia/Shanghai]
node scripts/push-toggle.js off <userId>
node scripts/push-toggle.js status <userId>
```

支持渠道：`telegram` / `feishu` / `slack` / `discord`

### 手动查询（同样从 MEMORY.md 传入城市/单位/语言）

```bash
node scripts/morning-push.js <userId> --city <城市> --units <metric|imperial> --lang <zh|en>
node scripts/forecast.js     <userId> --city <城市> --units <..> --lang <..>
```

---

## 📁 数据与隐私 (Data & Privacy)

- **无文件写入**：所有脚本都是纯计算（构建搜索/推送 prompt、生成资料区块、发出 cron 协议），**不向磁盘写入任何用户数据**，也**不读取任何用户文件**，符合 clawhub 无 `fs` 写入规范。
- **原生记忆**：用户的城市、单位、语言、推送时间与时区保存在 OpenClaw 原生 `MEMORY.md`，由你本机的 Agent 管理，不经过任何外部服务。
- **推送隔离**：`telegram`/`feishu`/`slack`/`discord` 由 openclaw 运行时投递，skill 不调用任何渠道 API、不持有 token。
- **删除资料**：删除 MEMORY.md 中对应的 `<!-- weather-daily:profile:<userId> -->` 区块即清除该用户的全部配置。

---

## ⚠️ 注意事项

1. 使用前须先注册：`node scripts/register.js <userId> <city>`，并把输出的资料区块存入 MEMORY.md
2. 无需 API Key，天气数据通过 WebSearch 实时搜索获取
3. 城市/单位/语言等配置存于原生 MEMORY.md（脚本不落盘），推送时作为参数传入并烘焙进 cron
4. 搜索结果受 WebSearch 实时性限制，极端天气预警以官方气象部门发布为准

---

*Version: 1.1.0 · Updated: 2026-07-02*
