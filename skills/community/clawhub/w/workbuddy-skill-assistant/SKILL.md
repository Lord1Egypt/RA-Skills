---
name: workbuddy-skill-assistant
slug: workbuddy-assistant
version: 6.8.1
displayName: WorkBuddy skill 使用管理指南
summary: 帮你装对、会用、用好、高效地使用 skill。
description: >
  WorkBuddy skill 使用管理指南：围绕真实任务帮助用户选择、安装、调用、组合和维护 skill。
  积木式管理：已装/自建 skill 登记进积木注册表统一调用；验证过的 skill 组合固化为工作流卡片接力执行复杂任务。
  分类标准：采纳七类基础分类（编程开发/智能体/写作创作/数据分析/设计创意/效率工具/教育学习）并可积木式扩展。
  外部来源：找优秀 skill 优先检索阿里 SkillsHub（含检索脚本），再适配安装到 WorkBuddy 目录。
  先理解目标，再给最小可行的 skill 方案；执行后验证结果，并把可复用经验沉淀下来。
author: 积木
license: MIT
tags: [workbuddy assistant, skill assistant, how to use skill, skill guidance]
category: productivity
updated: "2026-09-20T16:26"
triggers: [使用助理, 如何使用skill, 怎么用skill, skill最佳实践, 推荐skill, skill使用效率, skill管家, workbuddy skill怎么用, skill组合，skill工作流, skill没生效, skill不触发, skill太多想整理]
agent_created: true
allowed-tools: [Read, Write, Edit, Grep, Glob, Skill, conversation_search, automation_update]
---

# WorkBuddy skill 使用管理指南

> **一句话定位**：帮用户把 skill **装对、会用、用好、高效组合skill**，skill专业使用助理。不做skill创建及开发、升级等，不替用户管理所有 WorkBuddy 配置。

## 先判断是否该用

适合：

- 不知道该选哪个 优质skill，或已经装了太多 skill；
- 想学会某个 skill 的正确触发、输入、组合和验收方式；
- skill 没按预期工作，需要最小范围排查；
- 想把已经验证有效的 skill 用法沉淀成工作流或自动化。

不适合：

- 直接执行一个与 skill 无关的单一动作；
- 开发、发布或深度体检别人的 skill；
- 代替 `skill-check-pro` 做 skill 本身的质量审计。

## 唯一工作路径

无论用户主动提问还是自动化触发，都走同一条路径；区别只在于自动化不能替用户确认外部写入。

```text
理解目标 → 选择最小 skill 组合 → 给出/执行一次真实任务
       → 验证产出 → 记录可复用做法 → 必要时维护或关闭
```

### 1. 理解目标

先问或读取已有上下文，明确：

- 要完成什么真实产出；
- 输入资料在哪里、允许使用哪些工具；
- 结果格式、边界和验收标准；
- 是一次任务，还是会重复的工作流。

**只在缺口上问**：上下文已能推断的项不重复问；三项（产出／输入／验收）都推断不出时，才升级到逐项追问。多数请求上下文已经够——过度追问的代价大于猜错的代价。

**澄清上限（可触线）**：同一意图**至多澄清 2 轮**；第 3 轮起不再追问，改用最可能的默认假设继续，并在回答顶部显式声明「以下基于假设 X」。

**小结 → 确认**：追问结束、给方案之前，先三句话回读——「我理解你要的是 ①…… ②…… ③……，对吗？」有偏差就改。**不替用户默认正确。**

不要先跑全量扫描。只有用户明确要“检查我的 skill / 推荐 skill / 为什么不生效”时，才调用 `scripts/usage_diag.py` 做针对性事实检查。

### 2. 选择最小方案

- **选择**：先查 [积木注册表](references/skill-registry.md)（已装/自建积木名册），优先复用已装 skill；缺失时只推荐 1–3 个最相关项。
- **分类**：候选 skill 按 [基础分类标准](references/skill-taxonomy.md) 归位（七类 + 可扩展），推荐时先对齐任务域，避免跨类乱推。
- **安装**：SkillHub 托管项直接使用 `references/best-practices/toolbox.md` 的安装 prompt；需要从外部找**优秀 skill** 时先查 [skill-sources.md](references/skill-sources.md)——**优先阿里 SkillsHub**（107 个精选、中文分类可核验），未命中再退 SkillHub 与 skills.sh 全生态。
- **使用**：给出可以直接复制的触发话术、输入模板和预期产出。
- **组合**：只有当单个 skill 的边界明确、组合能减少重复劳动时才组合；不要为了“完整”堆三件套。同类组合重复出现且验收稳定时，固化为 [工作流卡片](references/workflows/README.md)，下次直接照卡执行；**照卡跑完必须把运行记录与接口修订写回卡片**（首次运行几乎总会暴露纸面接口与现实的偏差，不回写则卡片会持续失真）。

**推荐话术三件套**（给建议，不抛开放式问题）：

| 件 | 内容 | 示例（`<…>` 为占位，填真实积木名） |
|----|------|------|
| ① 建议值 | 先给一个默认答案 | “我建议用 `<A 积木>`” |
| ② 一句理由 | 说清依据 | “它已装、名册内已验证，且输入正好是你要的 `<输入形态>`” |
| ③ 备选项 | 2–3 个替代及代价 | “或 `<B 积木>`（更轻，但不做 `<缺的那步>`）” |
| 快捷键 | 统一收尾 | “回‘按建议’即可，或告诉我改哪。” |

**建议 ≠ 代填**：安装、升级、停用等写操作仍必须等用户明确确认；建议错了坦然改口重给，不硬撑。

命中“怎么用 skill / 推荐 skill / skill 没生效”时，按需加载：

- [skill 使用速览](references/skill-usage-guide.md)
- [skill 生态与选择](references/skill-ecosystem.md)
- [12 条核心检查](references/best-practices/checklist.md)

### 3. 执行、验证、沉淀

执行时先做最小真实任务，不先做大规模改造。完成后验证：

- 是否产出了用户要的结果；
- 是否满足格式、来源和边界；
- 是否比手工做更快、更准或更可复用；
- 下次是否应改成组合工作流或自动化。

验证有效后，才建议写入记忆、建立自动化或关闭低频 skill。任何安装、升级、停用、写外部文件操作都必须先得到用户确认。

## 分类与来源（两个基础契约）

- **分类标准**：任何 skill 归属七类基础分类之一——编程开发 / 智能体 / 写作创作 / 数据分析 / 设计创意 / 效率工具 / 教育学习；专业场景按需**积木式追加扩展类**（当前：`finance` / `knowledge` / `meta` / `workbuddy`）。七类固定不变。细则与判定规则见 [skill-taxonomy.md](references/skill-taxonomy.md)。
- **来源优先级**：找**优秀 skill** 一律**先查阿里 SkillsHub**（107 个精选、中文分类、可在 skills.sh 核验），未命中再退 SkillHub 与 skills.sh 全生态。检索用 `python scripts/skillhub_alibaba.py search "<关键词>"`；安装与 WorkBuddy 适配见 [skill-sources.md](references/skill-sources.md)。

## 针对性诊断（需要时才做）

`python scripts/usage_diag.py --offline --json` 只提供两类事实：

- `health_score`：环境异常的扣分制提示；
- `checklist`：12 条核心项的 pass/fail/na 与证据。

不要合成综合分、成熟度、雷达或“四支柱”。报告由 `scripts/report_builder.py` 输出“事实 + 最多 3 条建议动作”；无问题时可以静默。

## 自动化与交互边界

- 自动化与用户主动调用都走上面的唯一工作路径。
- 自动化可以读取、诊断、生成建议并入队，但不自动安装、升级、停用 skill，不写用户记忆。
- 用户确认后，才执行外部写入；执行完必须重新验证。
- 状态只保留 `state.md` 的健康分、达标比、生态采纳记录和待确认动作。状态 schema 见 [state-schema.md](references/state-schema.md)。

## 运行时参考

按需加载，不要全量阅读：

- [execution.md](references/execution.md)：一次运行的操作顺序；
- [skill-registry.md](references/skill-registry.md)：积木注册表（已装/自建积木名册），选方案先查这里；
- [skill-sources.md](references/skill-sources.md)：外部来源优先级与检索安装（优秀 skill 优先查阿里 SkillsHub）；
- [skill-taxonomy.md](references/skill-taxonomy.md)：skill 基础分类标准（七类 + 可扩展）；
- [workflows/README.md](references/workflows/README.md)：工作流卡片库（重复复杂任务的 skill 接力定义）；
- [skill-usage-guide.md](references/skill-usage-guide.md)：安装、调用、维护的用户话术；
- [skill-ecosystem.md](references/skill-ecosystem.md)：核心 skill 与主题 skill 的选择；
- [best-practices/checklist.md](references/best-practices/checklist.md)：12 条核心检查；
- [best-practices/checklist-details.md](references/best-practices/checklist-details.md)：单条未达标项说明；
- [retry-policy.md](references/retry-policy.md)：外部调用重试；
- [state-schema.md](references/state-schema.md)：状态字段与迁移。

作者侧发布、自测、经验编译和目录维护资料不随发布包分发，仅保留在源仓库 maintainers/ 目录；这些材料不是用户运行本 skill 的组成部分。

## 输出标准

每次回答尽量包含：

1. 结论：推荐哪个最小方案，为什么；
2. 立即可复制的话术或操作；
3. 验收标准：怎样算成功；
4. 下一步：只给一个最有价值的后续动作。

内部术语（`health_score`、`tier`、`checklist`、`pending_actions`、积木注册表、工作流卡片等）对用户**首次出现时带括号白话注释**，不等用户问；用户问术语就一句话白话答，不甩链接。

