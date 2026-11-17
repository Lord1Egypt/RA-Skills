---
name: tech-doc
description: "技术方案文档智能体：输入技术选型要点，自动生成方案对比、架构图和评审检查清单"
user-invocable: true
allowed-tools:
  - web_search
  - web_fetch
  - read
  - write
  - exec
  - sessions_spawn
  - sessions_yield
---

# 技术方案文档智能体

面向云手机研发的技术方案生成 Skill，支持技术选型对比、架构图生成、评审检查清单输出。

## 触发场景

用户提到以下意图时触发：
- "写个技术方案"、"做一下技术选型"
- "对比一下 XX 和 YY 方案"
- "生成架构图"、"画个架构图"
- "评审一下这个方案"

## 工作流程

### 1. 理解方案目标

明确：
- 要解决的业务/技术问题
- 候选方案（已有/需调研）
- 关键评估维度（性能、成本、兼容性、安全性、可维护性等）
- 是否需要生成架构图

### 2. 方案调研与对比

如果候选方案信息不足：
- 使用 `web_search` + `web_fetch` 检索候选方案资料
- 用 `exec` 执行 curl 调用 Dify 检索 API：
  ```bash
  curl -s -X POST "${DIFY_API_BASE}/v1/datasets/${DIFY_DATASET_ID}/retrieve" \
    -H "Authorization: Bearer ${DIFY_API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{"query":"<方案关键词> 技术方案 架构","top_k":5}'
  ```
  检索历史方案/架构文档
  > 如果 Dify 不可用，降级到本地 `memory_search`。
- 并行调研多个候选方案（`sessions_spawn` + `sessions_yield`）

按评估维度生成对比表：
- 方案 A / B / C 横向对比
- 每个维度打分或标注优劣势
- 给出推荐方案及理由

### 3. 生成架构图

调用 `diagram-maker` skill 或输出 Mermaid/SVG 描述：
- 系统整体架构
- 关键模块交互
- 数据流/控制流
- 与云手机现有系统的集成点

### 4. 生成评审检查清单

在方案文档末尾输出评审 Checklist：
- 需求对齐性
- 技术可行性
- 风险识别
- 性能/安全/可运维性
- 依赖与排期
- 验收标准

### 5. 归档

- 保存到 `memory/knowledge-base/samples/tech-docs/`
- 文件名：`YYYY-MM-DD-<方案名>-tech-doc.md`
- 更新 `memory/knowledge-base/INDEX.md`

## 输出规范

- 方案对比必须用表格，至少包含 3 个评估维度
- 架构图优先用 Mermaid 或 SVG 描述
- 推荐方案必须给出明确理由和落地步骤
- 评审检查清单条目必须可执行、可验证
