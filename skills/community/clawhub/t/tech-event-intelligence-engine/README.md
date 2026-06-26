# 🔍 技术活动情报解析引擎 (tech-event-intelligence-parser)

> 每日定时检索 → 智能去重过滤 → 结构化日报推送 | OpenClaw 工作流核心组件

## 🎯 功能简介
专为技术从业者、售前架构师、市场运营设计的 AI 情报过滤引擎。接收搜索引擎原始结果后，自动完成：
- 🕒 **时效校验**：拦截过期/时间模糊活动
- 🔍 **智能去重**：名称+时间+地点三元组匹配，防重复推送
- 📊 **相关性打分**：按技术匹配度/主办方权威性/嘉宾含金量分级
- 📤 **标准化输出**：生成可直接推送至飞书/企微/邮件的 Markdown 日报

## 🚀 快速使用
### 1. 接入搜索节点
在 OpenClaw/Dify 中先用 `tavily-search` 或 `Web Search` 获取原始摘要列表。
### 2. 调用本技能
```json
{
  "skill": "tech_event_intelligence_parser",
  "inputs": {
    "raw_search_data": "<搜索返回的JSON/Markdown列表>",
    "config": { "max_results": 15, "min_score": 0.55, "region_filter": "全国" }
  }
}
