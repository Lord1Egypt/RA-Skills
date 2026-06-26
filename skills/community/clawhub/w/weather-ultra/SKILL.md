---
name: weather-ultra
description: "天气查询，含空气质量、日出日落、Golden/Blue Hour、朝霞晚霞预测。触发词：天气、天气预报、几点日落、霞光、朝霞、晚霞、golden hour、blue hour。适合摄影师和户外活动规划。"
---

# Weather Ultra

天气查询 + 朝霞晚霞预测

## 使用

```bash
~/.openclaw/workspace/skills/weather-ultra/scripts/weather-full.sh <城市> [天数]
```

- **城市**：英文城市名（Beijing, Shanghai, Tokyo 等，支持任意城市）
- **天数**：可选，默认 1

## 输出格式

```
[城市]天气 [日期]

🌡️ 温度：最低 ~ 最高 °C
🌬️ 风力：风向 风速
☁️ 天况：晴/多云/雨
💧 湿度：百分比
🌫️ 空气质量：PM2.5 数值

🌅 日出：HH:MM AM/PM
🌇 日落：HH:MM AM/PM

✨ 早晨 Golden Hour：HH:MM - HH:MM
✨ 傍晚 Golden Hour：HH:MM - HH:MM
💙 早晨 Blue Hour：HH:MM - HH:MM
💙 傍晚 Blue Hour：HH:MM - HH:MM

🌅 朝霞质量：百分比 (等级)
🌇 晚霞质量：百分比 (等级)
```

## 霞光评分参考

| 分数 | 等级 | 建议 |
|-----|------|------|
| 80-100 | Excellent | 强烈推荐 🌟 |
| 60-79 | Good | 值得去 ✨ |
| 40-59 | Fair | 可能有色彩 |
| 0-39 | Poor | 不建议 |
