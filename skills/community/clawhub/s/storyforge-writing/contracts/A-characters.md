# A 类子契约 · 角色卡 / 人设（storyforge-writing）

> 归属：A 开发创作。对应 StoryForge `characters` / `characterRelations` / `characterDrivenPlans` / `knowledgeLedger`。
> 角色卡是 IP 设定资产；角色聊天（character chat）上层产品**只读引用冻结世界版本**。

## 1. 角色卡字段闭集

> **单一来源**：`references/field-registry.md` 的 `characters` 节（45 项可写字段）。本节只列**最常用**字段与
> **枚举闭集**；枚举一律写**英文闭集值**（禁中文描述，如"主角·核心"）。v0.4.0 及以前本节的中文释义
> 与登记表不符（如把 `orderAxis` 写成"叙事顺序轴"），已于 v0.5.0 更正。

| 字段 | 类型 / 闭集 | 含义 | 生成来源 |
|---|---|---|---|
| `name` | string | 角色名 | 项目角色图谱 |
| `roleWeight` | `main` · `secondary` · `npc` · `extra` | 叙事权重（主角 / 重要配角 / NPC / 群演） | 人设 / 角色表 |
| `moralAxis` | `good` · `neutral` · `evil` | 阵营·道德轴（善 / 中立 / 恶） | 人设 |
| `orderAxis` | `lawful` · `neutral` · `chaotic` | 阵营·秩序轴（守序 / 中立 / 混乱）—— **不是**出场顺序 | 人设 |
| `narrativeStatus` | `planned` · `active` · `inactive` · `retired` · `deceased` | 叙事生命周期状态 | 大纲 / 状态卡 |
| `firstAppearChapterId` / `exitChapterId` | number（FK → `chapters`） | 登场 / 退场章节 | 细纲 |
| `statusEvidenceChapterId` | number（FK → `chapters`） | 状态证据章节 | 状态卡回指 |
| `motivation` / `goals` / `fears` / `innerConflict` / `arc` | longtext | 动机 / 目标 / 恐惧 / 内在冲突 / 弧光 | 角色卡正文 |
| `personality` / `speechStyle` / `habits` / `appearance` | longtext | 性格 / 说话风格 / 习惯 / 外貌 | 角色卡正文 |
| `abilities` / `powerLevel` | longtext / string | 能力 / 力量等级 | 设定 |

> 出场顺序用 `firstAppearChapterId`（及章节 `order`）表达；不要借用 `orderAxis`。

## 2. 角色关系（characterRelations）

`fromCharacterId → toCharacterId` + 关系语义（夫妻/救命/仇敌/同僚/主从）。
生成时成对输出，带方向，避免双向重复。

## 3. 角色聊天（character chat）生成边界

- 生成**角色卡 + 说话风格 + 记忆约束 + 禁区（禁止事项）**，供聊天产品引用
- 该产品**只读引用**已封存 WorldRelease；**私域演化不回写**世界引擎
- 本 skill 出的是"人设语料"，不是活体聊天 runtime

## 4. 角色补全纪律（来自 LONGFORM 9.3）

- 角色补全必须**冻结明确角色和字段**；指定不存在的章节不得偷偷回退到其他章节
- 补全的**禁止字段**不进入冻结写入范围
- 世界设定里"用于说明规则的角色提及"**不等价于**创建/修改角色的授权
- 角色请求引用已有世界**不等价于**补齐/修改世界
- 过滤模型擅加任务时，同时清理其依赖与误导性计划摘要

## 5. 生命周期扩展（ADOPTION_EXTENSIONS）

- `character-merge-lifecycle`：角色合并
- `knowledge-ledger`：角色知识台账（characterId + knowledgeKey + factId + sourceChapterId）
- 角色状态卡（stateCards）随章节推进：`category / entityName / lastChapterId`

## 6. 所有权 · 不变量 · 禁止项（v0.4.0）

**所有权**：本技能 owns 角色卡与关系的**字段闭集与生成纪律**；上游 owns `characters` /
`characterRelations` / `characterDrivenPlans` / `knowledgeLedger` 表与 `ADOPTION_EXTENSIONS`；
**作者** owns 角色设定本身与采纳决定。

**不变量**
- `INV-C-1` 每条记录的字段必须 ∈ `references/field-registry.md` 的 `characters` 登记集。
- `INV-C-2` `roleWeight` / `moralAxis` / `orderAxis` / `narrativeStatus` 必须取**闭集枚举值**
  （禁中文长描述，如"主角·核心"）。
- `INV-C-3` 关系的两端必须解析到**同一语料内已存在**的角色 id（或按 `A-longform.md` §8 显式留痕）。

**禁止项**
- 不得替作者决定角色的命运、关系走向或生死。
- 不得把 `INFERRED` / `UNKNOWN` 的角色设定当作 `OBSERVED` 事实交付。
