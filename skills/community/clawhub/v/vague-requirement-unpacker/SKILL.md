---
name: vague-requirement-unpacker
description: >-
  Cold-start unpacker for vague boss/business requirements. Use when the user says
  "老板/业务只给了一个模糊方向", "帮我接一下这个需求", "信息不全先拆一下",
  "我还没 PRD 先给方案骨架", or needs a 30-minute to 2-hour PM alignment pack with
  confirmation questions, scenario narrowing, scope skeleton, readiness score, risk flags, and reply script.
---

# 模糊需求接招器 · Vague Requirement Unpacker

> **EN** From vague ask -> PM alignment pack.  
> **中文** 模糊指令 -> 可对齐的产品行动包。

不是 PRD 生成器，也不是需求评审器，而是 PM 面对“信息不完整但必须推进”的冷启动拆解工具。它先帮用户判断该问什么、怎么回、一期怎么收边界、哪些风险不能承诺。

**When / 何时用：** 老板或业务方只给了一个模糊方向、口头任务、微信截图、会议纪要短句；需要在 30 分钟到 2 小时内拿出能回老板或能开会对齐的材料；PRD 还没开始写，需要先搭骨架。  
**Not / 不用：** 已有完整 PRD -> 用 `pm-requirement-review-simulator`；纯竞品调研 -> 用 `competitive-product-research`；替用户拍板做不做；承诺可直接给研发排期的终稿。

```text
老板说：最近新客转化不太好，看看能不能搞点权益激励。
我现在只有这句话，帮我先拆成能跟老板确认的问题和方案骨架。
```

## 可直接触发的说法

以下输入都应触发本技能，不要要求用户先补完整 PRD：
- 老板/业务只给了一个模糊方向，帮我拆一下
- 这个需求现在信息不全，先帮我接住
- 我只有一句会议纪要，帮我拆成对齐问题
- 我还没 PRD，先给我需求冷启动骨架
- 帮我判断这个需求该先问什么
- 帮我把这个模糊需求拆成能开会对齐的材料
- 业务说想提升 XX，但没说清楚怎么做
- 一句话需求，先出接招包

## 典型输入

```text
老板说：最近新客转化不太好，看看能不能搞点权益激励。
我现在只有这句话，帮我先拆成能跟老板确认的问题和方案骨架。
```

```text
业务说：能不能给新用户做一个进阶引导，别一上来就流失。
我还没拿到完整需求，先帮我拆成对齐问题、核心场景和一期方案骨架。
```

```text
会议纪要里只有一句：投顾服务要提升触达后的承接效率。
帮我先拆一下，这到底要确认什么、可能做哪些方向、怎么跟业务对齐。
```

## 最小可用输入

**最低可启动：** 老板原话、业务口头方向、会议纪要短句或截图摘要。缺失信息必须标注为「待确认」，不可脑补成事实。

**推荐输入：** 老板/业务原话、紧急程度、已知目标或意图、目标用户、核心场景、已知约束、明确不做什么、交付档位、输出格式、后续动作。

**可兼容输入：**

- 只有一句方向：先提炼可能意图和关键缺口，再展示采集清单。
- 只有会议纪要或截图：先提取可见信息，无法确认的内容保持「待确认」。
- 用户说「直接生成」：只跳过业务信息追问，默认建议 L2；**不视为跳过输出格式确认**。用户明确委托默认格式时才使用 Markdown。

推荐输入和示例见 [references/user_templates.md](references/user_templates.md)。

## 交付档位

| 档位 | 适用场景 | 输出重点 |
|---|---|---|
| L1 回话包 | 30 分钟内要先回应 | 意图还原、关键问题、回话话术、风险红旗 |
| L2 对齐包（默认） | 1-2 小时内要开会对齐 | L1 + 场景收敛、能力骨架、MoSCoW、主流程 |
| L3 开写包 | 要开始写 PRD 草稿 | L2 + 异常分支、埋点指标、非功能、评审交接 |

## 工作流

```text
1) 接收模糊原话
2) 确认信息采集清单（预填 + 待确认 / 可跳过）
3) Layer 0 模糊度判定 -> 选择 L1 / L2 / L3
4) 按五层接招法展开
5) 计算接招就绪度 + 风险红旗
6) 输出报告 + 可选 handoff 到 pm-requirement-review-simulator
```

执行细节见 [references/unpacking-playbook.md](references/unpacking-playbook.md)。

### 信息采集清单（第 2 步）

先预填上下文中的已知事实；未确认值统一标记「待确认」，不得以推断替代用户确认。

```text
1️⃣ 老板/业务原话  2️⃣ 紧急程度  3️⃣ 已知目标或可能意图  4️⃣ 目标用户/角色  5️⃣ 核心场景
6️⃣ 已知约束  7️⃣ 明确不做什么  8️⃣ 交付档位（L1 / L2 / L3）  9️⃣ 输出格式（Markdown / HTML）  🔟 后续动作（仅接招包 / 继续评审预演）
```

**采集交互（优先使用可操作表单）：**

- **必须复用** [assets/intake-form.html](assets/intake-form.html)，不得由 Agent 临时重写表单 UI；该文件是跨 Agent 稳定展示的唯一实现。
- 通过 `prefill` URL 参数注入 URI 编码 JSON；原话、交付档位、输出格式为提交门槛，输出格式保持未选。紧急程度可预填；后续动作默认“仅接招包”。
- 原话、意图、用户、场景、约束和不做范围允许编辑；档位、格式与后续动作使用单选。文本清单中的推断值必须标记 `[推断]`；表单预填内容在提交前不得视为已确认。
- 宿主支持时内嵌表单并读取结构化回传；否则复制资产并用浏览器打开，用户粘贴结构化参数后继续。回传统一使用 `{schema_version:"1.0", skill, action, data}`；优先 `window.codex.submitForm`，兼容 `window.openai.sendFollowUpMessage`，最后复制 JSON。仅当 HTML 无法使用时，才退回 [references/user_templates.md](references/user_templates.md) 文本清单。
- 提交按钮使用“确认清单并开始拆解”；确认后执行 Layer 0 判定，再按已选档位与格式生成。格式未确认不得生成；用户明确委托默认时使用 Markdown。

### 逐层门控

默认直接生成完整选定档位；如果用户要求互动式推进，则每层结束询问：
```text
继续 / 停在这里 / 回老板或业务确认
```

不要在用户明显赶时间时强制逐层确认。可以先输出完整接招包，再把需要确认的问题放到最前面。

## 五层接招法

| 层级 | 名称 | 要解决的问题 | 必出内容 |
|---|---|---|---|
| Layer 0 | 模糊度判定 | 信息缺口有多大？紧急度？出哪档材料？ | 需求状态、紧急度、交付档位、保守假设 |
| Layer 1 | 意图还原 | 老板/业务真正想解决什么、不要什么、怎么算交差 | 可能意图、交差标准、确认问题、回话话术 |
| Layer 2 | 场景收敛 | 谁在什么情况下用，核心场景是否收敛 | 角色、核心场景 <=3、验收口径 |
| Layer 3 | 边界骨架 | 需要哪些模块，边界在哪里 | 模块清单、权限边界、MoSCoW |
| Layer 4 | 流程状态 | 主路径怎么走，关键状态是什么 | 主流程、状态表、卡点 |
| Layer 5 | 风险补丁 | 哪些补丁现在必须补 | 异常分支、埋点指标、非功能要求（L3 默认全开） |

L1 默认输出 Layer 0-1；L2 默认输出 Layer 0-4；L3 默认输出 Layer 0-5。

## 接招就绪度

按 5 个维度给 0/1/2 分，总分换算为百分制。读取 [references/scoring-engine-deterministic.md](references/scoring-engine-deterministic.md) 后执行。

| 维度 | 问什么 |
|---|---|
| 意图清晰度 | 知道老板/业务要结果、方案还是试点 |
| 场景收敛度 | 核心场景是否 <=3 且可验收 |
| 边界明确度 | 做什么 / 不做什么是否说清 |
| 约束可见度 | 时间、人力、合规、技术是否已知 |
| 对齐准备度 | 确认问题和回话话术是否 ready |

## 输出

按采集表确认的格式输出 `Markdown` 或 `HTML`；格式已明确时不重复询问。用户明确委托默认时使用 `Markdown`。

Markdown 直接按以下结构输出：
```text
1. 一页结论卡
2. 原话复述
3. 待确认问题（必须先问 / 可以后问）
4. Layer 0-5 接招展开（按档位裁剪）
5. MoSCoW 范围
6. 主流程与关键状态
7. 接招就绪度
8. 风险红旗
9. 回老板/业务话术
10. 下一步 / handoff
```

HTML 输出必须使用本技能自己的 [references/report-template-pro.html](references/report-template-pro.html)。模板视觉可以与 HammerRoom 其他技能同源，但文件必须在本技能内独立存在，避免跨技能依赖。

必含：
- 一页结论卡：这是个什么需求、现在能交付到哪一档、最大风险是什么
- 原话复述，不改写原意
- 待确认问题：最多 7 个，按必须问 / 可以后问分组
- 五层接招展开：按档位输出
- MoSCoW 范围：必须做、应该做、可以做、不做
- 回话话术：30 秒版 + 稍正式版
- 接招就绪度：分数、扣分原因、下一步补齐动作
- 风险红旗：合规、资源、范围、交付承诺、跨部门依赖
- 可选 handoff：如果用户要评审预演，交给 `pm-requirement-review-simulator`

## 硬约束

- **信息优先**：禁止把缺失信息编成事实；所有推断必须标注「假设」。
- **格式锁**：未确认输出格式不得生成完整接招包；仅用户明确委托默认时使用 Markdown。
- **冷启动定位**：不要输出“可直接给研发排期”的终稿承诺。
- **问题克制**：确认问题最多 7 个，先问能改变方向的问题。
- **场景收敛**：核心场景最多 3 个；超过 3 个必须建议分期或收敛。
- **边界清晰**：必须写「不做什么」；未知也要列为待确认项。
- **金融/合规敏感**：涉及金融、投顾、营销、隐私、未成年人、医疗、法律时，必须单列合规风险，不替代专业合规结论。

**Rigid（不可跳过）：**
- 原话复述
- Layer 0 模糊度判定
- 至少 5 个待确认项或明确说明为什么少于 5 个
- 接招就绪度评分
- 风险红旗
- 回话话术

**Flexible（可按场景调整）：**
- 是否逐层门控
- HTML 或 Markdown
- 模块清单颗粒度
- 流程图详细程度
- 是否继续 handoff 评审模拟器

## 验收与失败路径

- **只有一句方向**：可以启动，输出接招包，但要把关键事实标为待确认。
- **只有产品名或口号**：先追问“解决谁的什么问题”；用户仍要求直接生成时，只能输出低置信度接招包。
- **要求过度紧急**：必须给出“今天能回什么、不能承诺什么”的话术。
- **需求明显是竞品研究**：转 `competitive-product-research`。
- **已有完整 PRD 且目标是过会**：转 `pm-requirement-review-simulator`。
- **用户要求直接开写终稿 PRD**：先输出 L3 开写包，再建议接 `create-prd` 或 PM PRD 技能。

## 参考文件

| 文件 | 内容 |
|---|---|
| [references/scoring-engine-deterministic.md](references/scoring-engine-deterministic.md) | 接招就绪度评分规则 |
| [references/unpacking-playbook.md](references/unpacking-playbook.md) | 模糊需求接招方法手册：五层展开 · 档位裁剪 · 输出细则 |
| [references/report-template-pro.html](references/report-template-pro.html) | HTML 专业报告模板 |
| [references/user_templates.md](references/user_templates.md) | 输入模板与示例 |
| [assets/intake-form.html](assets/intake-form.html) | 跨 Agent 可复用采集表 UI |
