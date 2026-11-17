# Trellis 式触发重构设计（trigger-redesign）

> 日期：2026-08-18
> 分支：dev
> 状态：已确认设计，待实施

## 1. 背景与动机

当前 qa-team-skills 是"单技能包 + 逻辑指令"结构：

- 单一 `SKILL.md`（一个巨型 description 描述全部 8 个能力）+ `trigger` 关键词列表
- `/qa` 统一入口 + `intent-rules.md` 规则路由表（单步/多步/自动规划）
- 触发完全依赖 description 语义匹配，误触发与漏触发风险并存

ClawHub 安全审计（SkillSpector）反复点名同类问题：**Vague Triggers**（6 条 findings，如"生成/出一份报告""团队进度""测一下{模块}"过于通用）、**Description-Behavior Mismatch**（记忆自动扫描、自动写入）、**Intent-Code Divergence**（README 措辞矛盾、控制流冲突）。

参考 Trellis 的 **skill-first** 机制：每个能力是独立 skill，各自带精准的触发描述，AI 按上下文自动挑选，用户不用记任何命令名。

## 2. 目标与非目标

### 目标

1. **AI 自动挑选**：用户输入自然语言（如"测一下支付接口""帮我出周报"），AI 按语义自动加载对应 skill，无需用户记命令名
2. **触发精准可量化**：trigger-eval 基线 41 条（38 原始 + 3 条 explore）保持 100%，新增 ≥10 条"免指令名"用例，期望命中正确 skill
3. **跨平台**：基于 agentskills.io 标准 SKILL.md，适配 Claude Code / Cursor / OpenCode / Codex 等 40+ 平台
4. **保留资产**：指令能力内容（11 维度评审、9 方法用例、16 维度 Agent 测试等）、记忆模块、评测 CI、文档体系全部保留并适配

### 非目标

- 不改变 7 个指令各自的输出能力（评审维度、用例格式、缺陷分析流程等保持不变）
- 不引入平台专属机制（如 Claude Code hook / sub-agent 作为唯一入口）——那是可选增强，不是主路径
- 不做记忆 schema 或数据目录结构迁移

## 3. 架构设计

### 3.1 目录结构

从"单技能包 + prompts/ 逻辑指令"改为 **7 个独立 skill**：

```
qa-team-skills/
├── skills/
│   ├── qa-prd/SKILL.md        # 需求评审（11 维度）
│   ├── qa-case/SKILL.md       # 测试用例设计（9 方法 × 6 类型）
│   ├── qa-agent/SKILL.md      # AI Agent 专项测试（16 维度）
│   ├── qa-bug/SKILL.md        # 缺陷分析
│   ├── qa-report/SKILL.md     # 报告生成（5 种）
│   ├── qa-team/SKILL.md       # 团队管理（11 子能力）
│   └── qa-explore/SKILL.md    # 探索性测试
├── memory/                    # 共享记忆库（不变）
├── team/                      # 行业配置（不变）
├── evals/ ci/ docs/ examples/ # 保留并适配
└── SKILL.md                   # 仓库级总览（仅人读说明，不再承载触发）
```

### 3.2 删除项

| 删除 | 原因 |
|---|---|
| `prompts/qa/prompt.md`（/qa 统一入口）| /qa 是入口，方案 A 下无独立存在意义；自动规划/记忆管理能力拆解到各 skill 自身流程 |
| `prompts/qa/intent-rules.md`（路由表）| 路由决策完全交给模型对各 skill description 的语义匹配 |
| 8 个 `/qa-*` 逻辑指令概念 | 变为 7 个物理 skill，独立加载 |

### 3.3 各 skill 与现有指令映射

| 新 skill | 来源 | 能力保留 |
|---|---|---|
| skills/qa-prd | prompts/prd/prompt.md | 11 维度 + 业务分层 + 澄清问题 |
| skills/qa-case | prompts/case/prompt.md | 6 类型 × 9 方法 + 历史缺陷转化 + 规范库联动 |
| skills/qa-agent | prompts/agent/prompt.md | 16 维度（含 RAG）+ Payload |
| skills/qa-bug | prompts/bug/prompt.md | 质量评估 + 根因 + 批量 |
| skills/qa-report | prompts/report/prompt.md | 5 种报告 + 记忆读写 |
| skills/qa-team | prompts/team/prompt.md | 11 子能力 + 路由 |
| skills/qa-explore | prompts/explore/prompt.md | 三阶段 + Session 笔记 + Debrief |

## 4. 触发机制

### 4.1 每个 skill 的 SKILL.md 结构

```yaml
---
name: qa-case
description: >-
  当用户需要设计/生成软件测试用例时使用（如"帮我设计登录功能的测试用例"、
  "这个功能怎么测"、"出一份覆盖边界值和异常场景的用例"）。包含 6 种测试类型
  × 9 种黑盒方法交叉匹配 + 业务分层 + 记忆读写。
  不用于：缺陷根因分析（用 qa-bug）、需求评审（用 qa-prd）。
trigger: ["设计用例", "测试用例", "用例设计", "出份用例"]
---
```

### 4.2 双段式 description 规范（必填）

每份 SKILL.md 的 description 必须包含两段：

1. **何时用**（触发场景 + 2-3 个示例句）
2. **何时不用**（负向排除，引导 AI 去别的 skill）

负向排除是跨 skill 区分度的关键：7 个 skill 各自声明"不做什么"，让 AI 在模糊输入（如"看看这个功能"）时有足够信息分流到 prd/case/bug。

### 4.3 触发优先级约定

当多个 skill 的 description 都与输入匹配时：

1. 用户显式提到 skill 能力名（如"测试用例"）→ 命中对应 skill
2. 涉及缺陷/问题的输入 → qa-bug 优先于 qa-case（bug 表"分析问题原因"，case 表"设计用例"）
3. 涉及需求文档的输入 → qa-prd 优先于 qa-case
4. 仍无法区分 → 列出候选 skill 让用户选择

### 4.4 跨平台行为

| 平台 | 触发方式 |
|---|---|
| Claude Code / Cursor / OpenCode / Codex 等 | 标准 SKILL.md 目录自动发现，AI 按 description 语义自动加载 |
| 各平台命令面板 | 无斜杠命令，纯自然语言触发 |

多步任务（原 /qa 的"先评审再出用例"）：由 AI 在单个会话内顺序调用多个 skill 完成，skill 间通过共享 `memory/` 传递上下文（prd 写 reviews/ → case 读 reviews/）。

## 5. 记忆模块改造

### 5.1 能力归属

| 能力 | 现状归属 | 改造后归属 |
|---|---|---|
| 跨会话历史加载 | /qa Step 0 统一扫描 | **各 skill 执行前自检**：启动时读自己相关的记忆文件，注入"记忆简报" |
| 记忆写入 | 各指令 prompt 尾部 | 不变，但写入前确认规则统一收敛到 `memory/README.md` 共享约定 |
| 多步数据传递 | /qa 编排 | **skill 间通过文件系统传递**：prd 写 reviews/ → case 启动时自动读取同模块最新评审 |

### 5.2 各 skill 记忆读写映射

| skill | 读取 | 写入 |
|---|---|---|
| qa-prd | reviews/ + 历史评审 | reviews/ |
| qa-case | reviews/ + bugs/ + standards/ + test-cases/latest | test-cases/ + summary |
| qa-agent | test-cases/（同类型 Agent 历史）| test-cases/ |
| qa-bug | bugs/（复发检测）+ standards/ | bugs/ + standards/（确认后）|
| qa-report | reports/ + bugs/ + test-cases/ | reports/ |
| qa-team | reports/ + bugs/ | standards/（确认后）|
| qa-explore | bugs/ + standards/（生成探索起点）| — |

### 5.3 保留的写入确认规则（不丢）

以下写操作仍必须先问用户（继承 SKILL.md 人工校验规则）：

- latest.json 合并
- 版本清理（保留最近 5 个）
- 规范沉淀（standards.json 追加）

### 5.4 加载确认（承接审计修复）

各 skill 启动时**先询问用户**是否加载该模块历史记忆，用户确认后才扫描目录并读取——延续 ClawHub 审计 B 类修复后的行为（`prompts/qa/prompt.md` 第零步的"先问后扫"规则下沉到各 skill）。

## 6. 评测体系与文档适配

### 6.1 评测集适配

| 评测集 | 现状 | 适配后 |
|---|---|---|
| trigger-eval.json | 41 条，期望路由到 /qa-prd 等逻辑指令 | 保留 41 条 + 新增 ≥10 条免指令名用例，期望改为路由到对应 skill（qa-prd / qa-case…）|
| functional-eval.json | 8 条，prompt↔eval 契约断言 | 断言目标从 prompts/*/prompt.md 改为 skills/*/SKILL.md，检查每份必含触发描述/负向排除/防注入/自检 |
| security-eval.json | 8 条 7 种攻击 | 攻击提示词里 /qa-prd 改为自然语言触发 |
| ci/validate.sh | 检查 prompts/ 结构 | 改查 skills/ 目录、各 SKILL.md frontmatter 必填字段（name/description/trigger/负向段）、版本一致性 |

### 6.2 新增评测断言（支撑"触发准确率可量化"）

- 每份 SKILL.md description 必须含"何时用 + 何时不用"双段（脚本级检查）
- 7 个 skill 触发描述**互斥性检查**：对同一输入，不应有 2 个 skill 都声称该用自己（静态检查）
- trigger-eval 新增 ≥10 条免指令名用例（"测一下支付接口""帮我出周报""这个 Bug 什么原因"），期望命中正确 skill

### 6.3 文档适配

| 文档 | 变更 |
|---|---|
| README | 安装章节改为"7 个独立 skill 的安装方式"；使用章节改为"直接说人话，AI 自动挑"示例 |
| docs/user-manual.md | 指令详解保留，去掉 /qa 统一入口章节，改述为 skill 清单 |
| docs/process-integration.md | 流程嵌入图去掉 /qa，改述各 skill 触发场景 |
| SKILL.md（仓库级） | 降级为仓库总览（人读），不再承载触发 |

## 7. 实施要点（供 writing-plans 细化）

1. 按映射表逐个创建 `skills/*/SKILL.md`（内容从对应 prompts/*/prompt.md 迁移 + 双段式 description + 记忆加载自检流程）
2. 更新 ci/validate.sh、ci/run-evals.sh 的路径与断言
3. 更新 trigger-eval.json / functional-eval.json / security-eval.json
4. 更新 README / user-manual / process-integration / 仓库级 SKILL.md
5. 删除 prompts/ 目录（qa/ 入口 + intent-rules + 8 个 prompt 文件）
6. 跑全套 CI 验证（validate / run-evals / memory e2e / stress）

## 8. 风险与缓解

| 风险 | 缓解 |
|---|---|
| 7 个独立 skill 各自加载，上下文碎片化 | 双段式 description + 触发优先级约定；共享 memory/ 传递上下文 |
| 触发准确率依赖模型语义理解 | trigger-eval 免指令名用例 + 互斥性静态检查 + 规则路由基线对照 |
| 记忆加载行为不一致（原 /qa 统一）| 记忆加载/写入确认规则收敛到 memory/README.md 共享约定，各 skill 引用 |
| 迁移遗漏能力 | 保留 functional-eval 契约断言，逐 skill 对照现有 prompt 内容 |
