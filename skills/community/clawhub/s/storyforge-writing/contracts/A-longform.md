# A 类子契约 · 长篇 / 短篇（storyforge-writing）

> 归属：A 开发创作。字段闭集来自 storyforge schema v10 + LONGFORM-AND-NODE v1.6.0。
> 生成时遵守总入口的"数据契约 + 写作 SOP + 治理红线"，本文件只补长篇专属规则。

## 1. 完整长篇覆盖范围（9 块，全部要能生成）

1. 项目：名称、创作目标、题材、规模、作者约束
2. 世界观：起源/自然/人文/种族/势力/地点/历史/规则/多世界关系
3. 故事：主题、核心冲突、叙事策略、主线和支线
4. 角色：角色卡、关系、物品、状态、知识和生命周期
5. 大纲：全书 / 卷 / 章
6. 细纲：场景、目标、节拍、视角、承接、伏笔
7. 正文：生成、续写、选择编辑、扩写、重写、润色、审校、采纳、版本
8. 长程工程：事实、事件、关系、时间线、主支线进度、伏笔、原文、摘要、索引、影响分析
9. durable 运行：候选、刷新恢复、stale、拒绝/采纳、post-state、下游生效

## 2. 字段 → 语料映射（以长铗传为例；项目目录约定见 `references/local-environment.md`）

| StoryForge 表 | 长铗传来源 md | 生成内容 |
|---|---|---|
| works | project-baseline.md | code=长铗传、status、创作目标、规模（**90 集**，原 70 集扩展）×1 分钟、文风 |
| worldviews | p1-world-characters.md + knowledge/*.md | 唐代长安/天宝/安史之乱世界观、势力（保皇/太子党/杨国忠/叛军）、地点 |
| storyCores | p2-story-structure.md | 主题（理想主义幻灭）、核心冲突、主支线（复仇线/灭门真相线/游侠信念线） |
| characters | p1-world-characters.md | 裴行/游侠/裴守义/阿鸾/王怀远/卢征… 各卡（roleWeight/moralAxis） |
| characterRelations | p1-world-characters.md | 裴行↔阿鸾(夫妻)、裴行↔游侠(救命)、裴行↔卢征(仇) |
| outlineNodes | p3-scene-breakdown.md | 全书→幕→卷→章 树（第一幕长安落日 3-20…） |
| chapters | scripts/**episode-01..04** | 逐章状态（v0.1 曾写 act1-4，实际路径已变） |
| detailedOutlines | p3-scene-breakdown.md | 场景/目标/节拍/视角/承接/伏笔 |
| foreshadows | 各幕剧本 | 伏笔卡（阿鸾存活/灭门幕后/游侠身份） |
| storyTimelineEvents | 剧本时间线 | 天宝十四载末→至德二载 事件序 |
| stateCards | 角色状态 | 裴行(巡吏→游侠→远走敦煌) 等 |
| codexEntries | knowledge/*.md | 考据条目（官制/刑狱/游侠/市坊） |
| knowledgeLedger | knowledge/*.md | 角色知识台账（`factId` 指向只读表 `temporalFacts`，通常留 `null`；不要填 `0`，`0` 会被判悬空） |
| ~~temporalFacts~~ / ~~narrativeSummaryNodes~~ | — | **只读表，AI 不写**（系统从章节/大纲推导，见 `references/field-registry.md` §4）；需要摘要时写 `chapters.summary` |

## 3. 长篇写作 SOP 细化

- **创作顺序自由**：作者可先写世界/角色/故事；生成时按当前已确认内容联动，留白允许自主创造。
- **单任务单 Skill 单写入目标**：以作者原话确定 Skill 和写入字段；规划解读不得覆盖人物/时间/数量/禁止事项。
- **每阶段至多推进一份正文候选**：后续任务留会谈，终验后恢复为待确认计划。
- **跨章节前**：检查上一章章后运行状态。
- **全书进度**：来自实际设定/人物/卷章/细纲/正文，不能由"某次运行完成"推算。
- **完稿检查**：章纲覆盖、空正文、结构异常、待处理运行；作者核对目标/结局后确认完成并备份。

## 4. 百万字 / 长程一致性

- 原文永久可回查；事实/实体/关系/事件/主支线结构化
- 章节/卷/全局摘要可重建；Context Gateway 先目录后详情
- 伏笔、锁定约束高优先级但仍留原文来源
- 规模/召回/时间/预算/真实文学一致性分开验收

## 5. 显式派生世界（可选）

长篇保持独立 owner；作者可"基于当前作品创建世界草稿"或"封存为世界版本"。
派生保存来源作品/revision/选取范围/contentHash；原长篇后续修改不自动改写旧世界。

## 6. 节点模式合同（同源，不复制）

节点 = 同一长篇能力的 DAG 表达。可拆解/替换/连接中间产物，但**不复制第二套生成/记忆/数据体系**。
官方分步骤流程可**导出为官方节点模板**；节点调用领域 action/Skill，**不复制 UI 组件内部逻辑**；节点产物走同一候选/采纳链。

**每个节点至少声明**（字段闭集，源：LONGFORM-AND-NODE §7）：

```
type / version      节点类型与版本
owner               责任 owner
输入/输出类型       I/O 的显式类型
required sources    必读来源（对应 CONTEXT_SOURCES key）
allowed writes      允许写入的目标（对应 FIELD_REGISTRY）
作用域              scope（项目/世界/作品/实例）
依赖                dependsOn
资源预算            budget
运行证据            run evidence（可回查）
```

**图执行前必须检查**：① 循环 ② 缺输入 ③ 类型不匹配 ④ 作用域越界 ⑤ **未登记权限**。
运行图与 checkpoint 可独立保存。

**跨模式验收（5 条，缺一不可）**：

1. 分步骤创建的数据可被节点读取；
2. 节点生成并采纳的数据在分步骤 UI 显示；
3. 版本、stale、导入导出与删除一致；
4. 同一动作**无第二套** Prompt、AI 请求、DB 表清单或字段映射；
5. 非法连线在**调用模型之前**被阻断。

> 验收证据（上游，引用不代跑）：`R-LONGFORM-*` 系列 + 上游 `tests/e2e/` 下的 `longform-integration.spec.ts`、
> `longform-agent-experience.spec.ts`。注意：模拟模型回归**只证明工程流程**，
> 不证明真实模型的文学质量、整书无人值守生产或在线社区可用性。

## 7. 短篇（子集）

短篇独立创作（INDEPENDENT-CREATION）：故事核 / 角色 / 单线大纲 / 正文；**可显式派生世界草稿或封存世界版本**。
（v0.1.0 曾写「不提供『封装为世界』完整路径」，与源文档矛盾 —— 「不提供封装为世界」指的是**剧本 / 漫画**等改造类产品，见 `INDEPENDENT-CREATION.md:11`。）

## 8. 章节编号与引用完整性（v0.4.0）

**上游事实（不得凭直觉改，源 `src/lib/types/outline.ts`）**：
`chapters` 以**数字 `id`** 标识、以 **`order`:number** 排序；
`ChapterStatus` 闭集 = `outline`·`draft`·`revised`·`polished`·`final`。

**硬规则**：

1. **不得用字符串代号充当章节标识**：语料里 `chapters` 记录的 `id` 必须是**整数**。
   `ep30` / `第3章` / `EP-12` 这类代号**只能**出现在 `title`、文件名等**展示位**，
   **不得**出现在 `id` 或任何外键字段里。
2. **代号的映射必须唯一**：若正文产物或文件名使用章节代号，必须能唯一解析回 `chapters.id`；
   `order` 若存在必须是整数且**不重复**（章序可唯一映射）。
3. **外键必须可解析，或显式留痕** —— 任何指向其它表的外键值，必须能在**同一语料**内解析到。
   **解析不到时**只允许两种做法之一：
   - 置 `null` 并在该记录的对应字段留痕；且
   - 在**旁车**（`*.provenance.json`）登记一条 `unresolvedRefs`：
     `{"table": "<表>", "field": "<字段>", "value": <原值>, "reason": "<为什么尚未生成>"}`
   > **禁止静默悬空**：既不可解析、又未登记的引用 = **契约违规**。
   > 这对应上游语义「**缺失 ≠ 空**」：缺失必须**显式**，不能表现为一个"看起来正常"的值。

**校验（`scripts/check_framework_artifact.py`）**：

| 情形 | 判定 |
| --- | --- |
| `chapters` 的 `id` 是字符串 | **ERROR** `CHAPTER_ID_NOT_INT` |
| `chapters` 的 `order` 非整数或重复 | **ERROR** `CHAPTER_ORDER` |
| 外键悬空且**未**登记 | **ERROR** `FK_DANGLING` |
| 外键悬空但**已**登记 `unresolvedRefs` | **WARN** `FK_DANGLING_DECLARED`（留痕可见，不阻塞） |

## 9. 章节后验与有界回环（v0.4.0）

**依据（上游既有原语，不是外来设计）**：`chapters.continuityHandoff`（`ChapterContinuityHandoff`）
与 `chapters.planReconciliation`（`ChapterPlanReconciliation`，含
`reviewStatus ∈ {pending, confirmed-constraint, applied-outline, dismissed}`）。
⚠️ 这两个字段在 `references/field-registry.md` 里**已登记为可写字段**，却在本技能文档中长期
**0 次提及** —— 即「**可写但不指导**」：AI 看到 `object | —` 根本不知道填什么。本节补上。

**规则**：

1. **后验必须先于下一章**：每章正文完成后、**进入下一章之前**，产出/更新该章的
   `continuityHandoff` —— `finalScene{location, storyTime, activeCharacters, lastAction}`、
   `stateChanges`、`knowledgeChanges`、`commitments`、**`openLoops`**、`immediateNextIntent`、
   `evidenceQuotes`。**理由**：下一章会读取上一章的世界/角色/叙事差异。
2. **计划对账**：`planReconciliation` 记录 `completedGoals` / `unfinishedGoals` / `deviations` /
   `newConstraints` / `nextChapterImpacts`，以及 `foreshadowingRevealed`（伏笔提前暴露）/
   `delayedPlot`（情节推迟）。**未经作者确认不得视为已成立** —— `reviewStatus` 起于 `pending`，
   只有作者确认后才转 `confirmed-constraint` / `applied-outline`（**未确认 ≠ 已确认**）。
3. **有界回环**：后验若发现**事实性冲突**（与已确立的世界/角色状态矛盾），可打回上游重写该章，
   **上界 3 次**；超限**停下转人工**，不得无限重试。（对标 DeterminFlow 的
   `enable_reject_upstream` + `max_reject_count`。）
4. **措辞 ≠ 事实**：纯措辞调整**不必**重跑后验；一旦润色**改变了情节事实**，**必须重跑该章后验**，
   否则连续性状态与最终正文不一致。
5. **证据形态**：`evidenceQuotes` 必须是**原文引用 + 偏移**（`quote`/`startOffset`/`endOffset`），
   不得只写结论；两者缺一即视为证据不足。

### 9.1 字段级结构（v0.4.0；源 `src/lib/types/outline.ts`，逐字对齐）

> 这两个字段在 `field-registry.md` 里登记为 `object` 类型 —— **可写但此前无指导**。
> 以下为**上游权威结构**，语料若写入必须按此形状；`?` = 可选。

**`continuityHandoff`（必填 7 项 + 2 可选）**

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `chapterId` | number | 所属章节 |
| `sourceTextHash` | string | 正文哈希（证据锚点） |
| `finalScene` | object | **必填** `activeCharacters: string[]`；可选 `location` / `storyTime` / `lastAction` |
| `stateChanges` | string[] | 世界/角色**状态**变化 |
| `knowledgeChanges` | string[] | **认知**变化（谁知道/误信什么） |
| `commitments` | string[] | 本章做出的**承诺**（须兑现） |
| `openLoops` | string[] | **未闭合环**（伏笔/悬念） |
| `immediateNextIntent?` | string | 紧接的下一意图 |
| `evidenceQuotes` | array | **非空**；每项 `{quote, startOffset, endOffset}` —— 原文引用 + 偏移，**不得只写结论** |
| `schemaVersion` / `extractorVersion` / `textNormalizationVersion` / `generatedAt` | number/string | 抽取器元数据 |

**`planReconciliation`（必填 5 类对账 + `reviewStatus`）**

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `chapterId` / `sourceTextHash` / `planSourceHash` | number/string | 章 + 正文哈希 + **计划哈希**（对账基准） |
| `completedGoals` / `unfinishedGoals` / `deviations` / `newConstraints` / `nextChapterImpacts` | `Item[]` | 五类对账 |
| `foreshadowingRevealed?` / `delayedPlot?` | `Item[]` | 伏笔**提前暴露** / 情节**推迟** |
| `reviewStatus` | enum | **`pending`** · `confirmed-constraint` · `applied-outline` · `dismissed` —— **起于 `pending`** |
| `confirmedActualProgress?` / `reviewedAt?` / `generatedAt` / `actions?` | — | 作者对账记录 |

`Item` = `{ text: string, evidenceQuotes: Array<{quote, startOffset, endOffset}> }` —— **每一项对账都要带原文证据**。

**机器校验**（`check_framework_artifact.py`，问题码 `HANDOFF_SHAPE` / `RECONCILIATION_SHAPE` / `RECONCILIATION_UNCONFIRMED`）：
`continuityHandoff` 必填 7 项、`finalScene.activeCharacters` 为数组、`evidenceQuotes` 非空且带偏移；
`planReconciliation` 五类对账齐备、每个 Item 带原文证据、`reviewStatus` 取闭集且非 `pending` 时必须有 `reviewedAt`。

## 10. 所有权 · 不变量 · 禁止项（v0.4.0）

**所有权**：本技能 owns 长篇产物的**生成顺序、字段闭集与后验纪律**；上游 owns
`chapters` / `outlineNodes` / `detailedOutlines` / `storyArcs` 等表与节点运行时；**作者** owns 剧情决定与采纳。

**不变量**
- `INV-L-1` §1 的**九块覆盖范围**必须全部可生成（缺块须显式说明，不得静默省略）。
- `INV-L-2` `chapters` 的 `id` 为**整数**、`order` 为整数且**唯一**（§8）。
- `INV-L-3` 任何外键必须可解析，或按 §8 在旁车 `unresolvedRefs` **显式留痕**。
- `INV-L-4` 每章**后验先于下一章**；`continuityHandoff` / `planReconciliation` 按 §9 产出。
- `INV-L-5` provenance 与证据分级**只在旁车**（`S-data-envelope.md` §3）。
- `INV-L-6` 写入的 `continuityHandoff` / `planReconciliation` 必须符合 §9.1 形状；`planReconciliation.reviewStatus` 生成时为 `pending`，非 `pending` 必须带 `reviewedAt`。
- `INV-L-7` 不写只读表（`temporalFacts` / `narrativeSummaryNodes`，见 §2）。

**禁止项**
- 不得跳过上游阶段直接产出正文（前置不足须先补上游）。
- 不得无限回环：打回重写**上界 3 次**，超限转人工。
- 不得把未确认的 `planReconciliation` 当作已成立（`reviewStatus` 起于 `pending`）。
