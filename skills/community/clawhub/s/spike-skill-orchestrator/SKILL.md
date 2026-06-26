---
name: skill-orchestrator
homepage: https://github.com/spikesubingrui-design/skill-orchestrator
version: 1.0.1
clawhub_slug: spike-skill-orchestrator
description: Adaptive local skill scheduler for OpenClaw. Use when a task may benefit from multiple installed skills, when the user asks "该用什么 skill", "调度一下", "有没有相关 skill", "搭配使用", or when a multi-step/cross-domain request should first check local skill combos before proceeding.
metadata:
  openclaw:
    emoji: "🧩"
---

# Skill Orchestrator

目标：先判断本地已装 skills 里有没有能提效的组合，再决定是否询问 Spike 搭配使用。

## 何时加载

### 必须先跑

- 多步任务：研究 + 输出、设计 + 文案、调试 + 测试、部署 + 验证
- 跨域任务：UI + 内容、研究 + 汇报、记忆 + 报告、浏览器 + 抓取
- 你不确定该走哪条 workflow，或同类任务历史上常漏调 skill
- 用户明确说：
  - “调度一下”
  - “该用什么 skill”
  - “有没有相关 skill”
  - “这些 skill 能不能搭配”

### 直接跳过

- 纯闲聊、单句问答、无需工具的简单解释
- 明确只要单一 skill，且用户已点名
- 已经在某个成熟 workflow 内部，例如 cron 固定链路

## 流程

### 1. 跑确定性召回

```bash
node skills/skill-orchestrator/scripts/match-skills.mjs "<用户任务>" --json
```

读取：
- `ops/skills/registry.json`
- `ops/skills/trigger-router.json`

输出：
- `candidates`: 相关单 skill 候选
- `combos`: 相关组合候选

### 2. 做 smart 判定

按下面规则决定是否打断用户：

- 只有 1 个高置信单 skill，且很明显：直接加载该 `SKILL.md`
- 命中 2 个以上高分 skill，或命中组合：询问 Spike 是否搭配
- 只有低分噪音候选：静默跳过，直接做任务

经验阈值：
- `candidates[0].score >= 12` 且 `candidates[1]` 差距明显：通常可直接用
- 任一 `combo.score >= 8`：通常值得问一下

## 如何问

当命中组合或多候选时，使用 `AskQuestion`，不要直接替用户决定。

选项建议：
- 组合 A：`UI/设计 + 内容`
- 组合 B：`搜索/研究 + 报告`
- 单独用某个 skill
- 都不用，直接做

问题文案要短：
- “这次任务可搭配这些本地 skills，要一起启用吗？”

## 执行顺序

用户采纳后，按“上游路由 skill → 下游执行 skill”的顺序读 `SKILL.md`：

- 例如：
  - `opencli-usage` → `opencli-browser`
  - `frontend-design-3` → `impeccable-uxui`
  - `smart-search` → `data-research` → `report-ui`

不要一次性把 5 个无关 skill 全读进上下文。最多保留：
- 1 个主 skill
- 1 到 2 个协作 skill

## 记录反馈

每次提议后都记一行日志：

```bash
node skills/skill-orchestrator/scripts/log-decision.mjs \
  --task "<任务>" \
  --proposed "<skill-a,skill-b>" \
  --accepted "<skill-a,skill-b>" \
  --mode "<direct|ask|skip>"
```

如果用户拒绝所有建议：

```bash
node skills/skill-orchestrator/scripts/log-decision.mjs \
  --task "<任务>" \
  --proposed "<skill-a,skill-b>" \
  --accepted "" \
  --mode "reject"
```

日志写到：
- `openclaw-evolution/data/skill-orchestrator-log.jsonl`

## 护栏

- 不要为“看起来相关”就强塞 skill
- 用户拒绝后，本轮静默，不要二次追问
- 不要把外部市场 skill 搜索和本地 skill 调度混在一起
- 不要改已有 workflow 的业务逻辑，只做召回和建议
- 候选过多时，最多展示 3 个单 skill 或 2 个组合

## 示例

### 例 1：设计 + 内容

输入：

```text
帮我做个落地页发小红书
```

期望建议：
- 组合：`UI/设计`
- 组合：`内容`
- 问 Spike 是否搭配启用

### 例 2：AI 新闻

输入：

```text
今天 AI 圈有什么
```

期望建议：
- `aihot`
- `github-trending`
- `trendradar`
- 可直接采用 `早报` 相关组合

### 例 3：简单问答

输入：

```text
解释一下 MCP 是什么
```

行为：
- 若无明显 workflow 优势，跳过 orchestrator，直接回答
