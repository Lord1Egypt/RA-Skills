# InkOS 深度学习笔记

> 来源：https://github.com/Narcooo/inkos (6.2k Stars, 1.2k Forks, v1.3.12)
> 学习日期：2026-05-17
> 用途：为 Writing Triadic 提供工业级写作系统架构参考

---

## 一、架构概览

InkOS 是一个**10-Agent 接力管线**的自动化小说写作系统，核心思想是"写-审-改"闭环，配合 7 个真相文件（Truth Files）作为长期记忆。

### Agent 管线

```
Radar → Planner → Composer → Architect → Writer → Observer → Reflector → Normalizer → Auditor → Reviser
```

| Agent | 职责 | 对 Writing Triadic 的启示 |
|-------|------|--------------------------|
| Radar | 扫描平台趋势，指导故事方向 | 对应我们的 Phase 1.5 联网调研 |
| Planner | 读取 author_intent + current_focus → 产本章意图 | 可融入 Phase 1 需求挖掘 |
| Composer | 从真相文件按相关性选上下文，编译规则栈 | 对应 Phase 2 规则制定 |
| Architect | 规划章节结构：大纲、场景节拍 | 对应写作计划.md |
| Writer | 两阶段：高温创意写作 → 低温状态结算 | **核心启示：双温分层** |
| Observer | 过度提取 9 类事实（角色/位置/资源/关系/情感/信息/伏笔/时间/物理状态） | 审计精细化思路 |
| Reflector | 输出 JSON delta + Zod 校验 → immutable 写入 | 可靠性设计模式 |
| Normalizer | 单 pass 压缩/扩展，将字数拉入允许区间 | 对应字数治理 |
| Auditor | 33 维度质检，对照 7 个真相文件 | 对应 Reader 评审 |
| Reviser | 修复审计问题，auto-fix critical → 人工审核其余 | 对应 Mode A/B/C 迭代 |

---

## 二、核心方法论（可迁移到 Writing Triadic）

### 1. 双阶段 Writer 架构

**InkOS 做法**：
- Phase 1（Creative, temp=0.7）：自由创作正文
- Phase 2（Settlement, temp=0.3）：精密更新所有真相文件

**可迁移方向**：
→ Writing Triadic 的 Executor 可以引入**双温分写**：
  - 第一遍（高温度）：自由创作，允许 creativity
  - 第二遍（低温度）：结构校准、AI 痕迹自查、偏好对齐

### 2. 7 真相文件系统 + Zod Schema 校验

**InkOS 做法**：
- `current_state.md`：世界状态
- `particle_ledger.md`：资源账本
- `pending_hooks.md`：未闭合伏笔
- `chapter_summaries.md`：各章摘要
- `subplot_board.md`：支线进度板
- `emotional_arcs.md`：情感弧线
- `character_matrix.md`：角色交互矩阵

所有文件从 v0.6.0 起迁移到 `story/state/*.json`（Zod schema 校验），LLM 输出 JSON delta → 代码层 immutable apply + 结构校验后写入。

**可迁移方向**：
→ Writing Triadic 的 MEMORY.md 未来可考虑结构化（JSON + schema），提升可靠性
→ 当前 MEMORY.md 的 Markdown 格式在人类可读性上更优，但在"坏数据不滚雪球"上不如结构化方案

### 3. 输入治理控制面（Input Governance）

**InkOS 做法**：
- `story/author_intent.md`：长期作者意图
- `story/current_focus.md`：近期关注点
- `plan chapter` → `compose chapter` → `write` 三级链路
- 每章生成 `intent.md`（人读）、`context.json`、`rule-stack.yaml`、`trace.json`（机读）

**可迁移方向**：
→ Writing Triadic 可以在"即兴写作"模式中引入**轻量级意图卡**（1 轮即出），类似 InkOS 的 chapter intent.md
→ `plan` + `compose` 不需要在线 LLM → Writing Triadic 的 Phase 0/1 也可以有离线预处理环节

### 4. De-AI-ification（去 AI 味）体系

**InkOS 做法**：
- **词汇疲劳词表**：按题材维护高频 AI 词汇（如 LitRPG 的 "delve", "tapestry", "testament"）
- **11 条硬规则**：段落等长检测、套话密度、公式化转折、列表式结构检测（纯规则，不走 LLM）
- **33 维审计中包含 AI 痕迹维度**
- **`revise --mode anti-detect`**：专门的反检测改写
- Writer agent prompt 层内置去 AI 味规则

**可迁移方向**：
→ Writing Triadic 的 ai-traces-guide.md 已有词汇/结构分类，可进一步：
  - 按模板体裁维护专属疲劳词表（如技术博客的 "在当今"、朋友圈的 "遇见更好的自己"）
  - 将去 AI 味规则从"参考指南"升级为"自动注入到 Executor prompt"

### 5. 字数治理（Length Governance）

**InkOS 做法**：
- `--words` 指定目标字数 → 自动推导允许区间
- 中文默认 `zh_chars`，英文默认 `en_words`
- 超出 > 1 次纠偏归一化（压缩或补足）
- 仍超出 → 保存但留 warning + telemetry

**可迁移方向**：
→ Writing Triadic 可以在 Phase 2 规则制定时引入**字数柔区**（而非硬性数字），Executor 有 ±20% 弹性

### 6. 多模型路由

**InkOS 做法**：
- Writer → 强创意模型（如 Claude）
- Auditor → 快速便宜模型（如 GPT-4o）
- Radar → 本地模型（零成本）
- 支持 `inkos config set-model <agent> <model>` 按 Agent 粒度配置

**可迁移方向**：
→ Writing Triadic 已有 model-config.md 做多模型配置，可进一步引入"按角色默认配模型"的自动检测

### 7. 可靠性保障

**InkOS 做法**：
- 每章自动创建状态快照 → `inkos write rewrite` 回滚
- Writer 动笔前输出自检表 + 写完输出结算表
- 文件锁防并发写入
- 跨章重复检测
- Zod schema 校验 JSON delta，坏数据直接拒绝

**可迁移方向**：
→ Writing Triadic 的 v2/v3 版本管理可以借鉴快照回滚机制
→ 当前 v2.6 的 Mode A/B 迭代已有"原版可回溯"规则，可强化

### 8. SQLite 时序记忆数据库

**InkOS 做法**：
- Node 22+ 自动启用 `story/memory.db`
- 按相关性检索历史事实、伏笔、章节摘要
- 避免全量注入导致的上下文膨胀

**可迁移方向**：
→ Writing Triadic 的 MEMORY.md 目前是全量读取（Phase 0），随积累增长可能面临膨胀
→ 可考虑引入"相关性搜索"而非"全量读取"（当前 memory_search 已部分支持）

---

## 三、交互架构启示

### 共享交互内核

InkOS 的 CLI / TUI / Studio / OpenClaw Skill 共享同一套交互执行内核（15+ 意图、18 个工具）。

**启示**：Writing Triadic 作为 OpenClaw Skill 时，内部协议（Phase 0-5.5）就是它的"交互内核"。未来如果有 Web UI 或其他入口，复用这套协议即可。

### 自然语言 Agent 模式

`inkos agent "写一部都市修仙小说"` → LLM 通过 tool-use 自动决定调用哪些底层命令。

**启示**：Writing Triadic 已经通过 session_spawn 实现了类似的"调度层"——Creator 在主会话中决定何时 spawn Executor/Reader/EvolutionAnalyst。如果未来需要原子化工具，可参考 InkOS 的 tool-use 模式。

---

## 四、不宜直接引入的部分

| InkOS 特性 | 原因 |
|-----------|------|
| 多章节连续性管理 | Writing Triadic 是通用写作 skill，非长篇小说专用 |
| 平台格式导出（起点/番茄等） | 不属于通用写作范畴 |
| 守护进程 + 通知推送 | Writing Triadic 是交互式写作，非后台自动运行 |
| 同人创作正典边界管理 | 写作类型过窄 |
| 封面生成 | 非写作核心 |

---

## 五、已吸收并应用于 v2.7 的要点

1. **即兴写作的轻量级意图卡** ← 借鉴 InkOS 的 chapter intent + input governance
2. **双温分写（高创意 + 低校准）** ← 借鉴 InkOS Writer 两阶段架构
3. **按模板维护 AI 疲劳词表** ← 借鉴 InkOS 按题材维护 fatigue word lists
4. **字数柔区（±20%）** ← 借鉴 InkOS 长度治理的 soft band
5. **去 AI 味规则自动注入 Executor prompt** ← 借鉴 InkOS Writer prompt 层内置去 AI 味规则
