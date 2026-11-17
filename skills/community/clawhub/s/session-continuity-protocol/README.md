[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

# session-continuity-protocol · 跨会话连续性协议 / Cross-Session Continuity Protocol

## English

Cross-workspace / cross-session memory continuity protocol (first published by Buda Pan). Triggers: session start; the user says "pick up the context / do you remember / you've lost your memory"; or before any continuity-sensitive task (official-account publishing, brand assets, publishing blocks, key delivery, project status). Once loaded, strictly run the "opening four steps" to re-load settled facts — never re-ask the user for finalized items, never go amnesiac. Source of truth = file layer (`_ACTIVE_PROJECTS.md` + account MEMORY.md), with the localmem semantic layer as fallback.

### Usage
- **AI agent**: read `SKILL.md` (frontmatter name/description decides applicability; body is the execution steps).
- **Human reader**: read `SKILL.md` and `AGENTS.md`.

### Files
- `SKILL.md` — main specification
- `AGENTS.md` — agent instructions
- `llms.txt` — machine-readable index
- `LICENSE` / `LICENSE.md` — license

## 中文

跨工作区 / 跨会话记忆连续性协议（潘布达首发）。触发场景：新会话开局、用户说「续上上下文 / 你还记得吗 / 你失忆了」、或要做任何连续性敏感任务（公众号发稿、品牌资产、发布阻塞、密钥投递、项目状态）之前。加载后严格跑「开局四步」把已固化事实回灌，避免在已定稿事项上重复问用户、避免失忆。真源 = 文件层（_ACTIVE_PROJECTS.md + 账号 MEMORY.md）优先于 localmem 语义层兜底。

### 使用
- **AI 代理**：读取 `SKILL.md`（frontmatter 的 name/description 决定是否适用；正文为执行步骤）。
- **人类读者**：读取 `SKILL.md` 与 `AGENTS.md`。

### 文件
- `SKILL.md` — 主说明书
- `AGENTS.md` — AI 代理说明书
- `llms.txt` — AI 可读索引
- `LICENSE` / `LICENSE.md` — 许可声明

<!-- 生成：2026-10-15 · 技能骨架批量升级；双语化：2026-10-17 -->
