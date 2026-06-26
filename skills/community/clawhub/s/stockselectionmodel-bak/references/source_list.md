# 数据源优先级

> 目标：兼顾开箱即用、真实性、低配置依赖、低 token 成本。

## 一级数据源（增强模式）

当用户配置了 `TAVILY_API_KEY` 时，优先使用：

- Tavily Search
  - 优点：覆盖广、结果结构化、去重方便
  - 适合：晨报、盘中快讯、海外 AI 巨头动态

## 二级数据源（免配置模式）

当用户未配置 Tavily 时，使用公开网页/RSS/API 兜底：

- Reuters / AP / CNBC / Yahoo Finance 等公开新闻页
- 公司官方 newsroom / blog（如 OpenAI, NVIDIA, Google, Microsoft）
- 可公开访问的 RSS / feed / JSON endpoints（若可用）

## 使用原则

1. 优先抓“标题 + 链接 + 100~200 字摘要”，避免抓整篇全文
2. 单次分析只保留 5~8 条最高相关内容
3. 若多个来源重复报道同一事件，只保留 1 条主来源 + 1 条补充来源
4. 对于明显公关稿、广告稿、低信息量内容，直接降权或丢弃

## 推荐关键词

- OpenAI / NVIDIA / Google / Microsoft / Meta / Anthropic
- AI chip / GPU / datacenter / inference / model / agent / robotics
- 大模型 / 算力 / 光模块 / AI应用 / 机器人 / 自动驾驶
