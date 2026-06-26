---
name: weather
description: "Get current weather and forecasts via 墨迹天气 or MSN Weather. Use when: user asks about weather, temperature, or forecasts for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis."
---

# Weather Skill — 本地覆盖版

⚠️ **本技能覆盖内置 weather 技能，强制使用国内数据源。**

## ⛔ 禁止

- 禁止使用 `wttr.in`、`Open-Meteo` 或任何国外天气 API
- 禁止用 `curl` 直接获取天气数据
- 禁止凭记忆或猜测生成天气数据

## ✅ 唯一允许的数据源

### 1. 墨迹天气（首选）

- 首页：`https://tianqi.moji.com/`
- 城市天气页：`https://tianqi.moji.com/weather/省份/城市/区县`
- 示例：
  - 佛山顺德：`https://tianqi.moji.com/weather/guangdong/foshan/shunde`
  - 上海闵行：`https://tianqi.moji.com/weather/shanghai/shanghai/minhang`
  - 山东日照：`https://tianqi.moji.com/weather/shandong/rizhao/donggang`
- **必须通过 `browser` 工具打开网页，截图或提取数据**

### 2. MSN 天气（备选/交叉验证）

- `https://www.msn.cn/zh-cn/weather/`
- 需要浏览器渲染获取动态内容
- 与墨迹天气交叉验证，差异大时说明

## 操作流程

1. 根据用户提到的城市，构造墨迹天气 URL
2. 用 `browser` 工具打开该 URL
3. 用 `browser snapshot` 或 `screenshot` 获取天气数据
4. 整理后回复用户
5. 如需验证，再用 MSN 天气交叉检查

## 注意事项

- 墨迹天气 URL 中的省份和城市名称使用拼音小写
- 区县名称也要用拼音
- 如果某个城市查不到，尝试只到城市级别
- 回复时注明数据来源
