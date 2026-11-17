# Thesis Tracker — 投资论点追踪与验证 Skill

投资论点全生命周期管理工具：录入 → 追踪 → 验证 → 归档。

## 功能

- 📝 论点录入：结构化存储投资逻辑、核心假设、触发条件、时间窗口
- 🔍 定期验证：对照触发条件自动检查数据，更新论点状态
- 📊 状态管理：pending / partial / confirmed / negated 四态追踪
- 💾 持久化：论点数据保存至 `thesis-tracker/theses.json`
- 🧠 IMA 同步：新论点自动创建知识库笔记

## 触发方式

- 说 "论点追踪" / "投资逻辑" / "thesis tracker"
- 说 "验证XX观点" / "跟踪XX判断"
- 说 "帮我记一下这个投资逻辑"

## 依赖

- `neodata-financial-search` skill（触发条件数据验证）
- IMA 知识库（可选，用于论点归档）

## 数据结构

```json
{
  "id": "T001",
  "title": "2026H2地产见底",
  "assumptions": ["政策放松", "销售拐点", "估值极低"],
  "triggers_positive": ["..."],
  "triggers_negative": ["..."],
  "status": "pending",
  "checks": [...]
}
```

## 版本

v1.0.0 — 初始版本
