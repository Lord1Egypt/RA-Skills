---
name: worldcup26-api
description: "2026 World Cup Data Center API — 实时比分、赛程、积分榜数据接口，覆盖世界杯、欧冠、五大联赛等 34+ 赛事。"
read_when:
  - 需要查询足球实时比分
  - 获取世界杯赛程和积分榜
  - 为 AI Agent 集成体育数据 API
metadata:
  source: https://www.26worldcup.cn
  author: betfullstar
  contact: support@26worldcup.cn
  license: MIT
  tags:
    - worldcup
    - football
    - sports
    - api
    - data
    - 2026
---

# 🏆 2026 World Cup Data Center API

**实时足球数据 API**，覆盖 34+ 顶级赛事，适合 AI Agent、自媒体、开发者、体育数据分析。

## 快速开始

```bash
# 实时比分
curl -X GET "https://www.26worldcup.cn/api/v1/live" \
  -H "Authorization: Bearer YOUR_API_KEY"

# 赛程查询
curl -X GET "https://www.26worldcup.cn/api/v1/schedule?date=2026-06-12" \
  -H "Authorization: Bearer YOUR_API_KEY"

# 小组积分榜
curl -X GET "https://www.26worldcup.cn/api/v1/standings?group=A" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 定价

| 方案 | 价格 | 日调用量 | 月调用量 |
|------|------|----------|----------|
| 🆓 体验版 | 免费 | 100 次 | 3,000 次 |
| ⭐ 基础版 | HK$99/月 | 10,000 次 | 300,000 次 |
| 🔥 专业版 | HK$299/月 | 100,000 次 | 3,000,000 次 |
| 🏢 企业版 | HK$999/月 | 无限 | 无限 |

## 覆盖赛事

### 🌍 国家队顶级赛事
世界杯 · 欧洲杯 · 美洲杯 · 亚洲杯 · 非洲杯 · 欧美杯

### ⭐ 欧洲俱乐部顶级赛事
欧冠 · 欧联杯 · 欧协联 · 欧洲超级杯

### 🔥 欧洲五大联赛
英超 · 西甲 · 德甲 · 意甲 · 法甲

### 🌏 亚洲及南美赛事
亚冠 · 沙特联赛 · J联赛 · K联赛 · 中超 · 解放者杯 · 巴甲

## AI Agent 应用场景

- 🤖 **体育预测机器人** — 实时数据驱动的比分预测
- 📊 **自动赛事报告** — 用 LLM 生成英文/中文战报
- 🔔 **实时比分通知** — 对接消息推送系统
- 🏆 ** Fantasy Football 数据源** — 球员/球队数据聚合

## 获取 API Key

注册领取免费 Key：**https://www.26worldcup.cn**

**技术支持**: support@26worldcup.cn
