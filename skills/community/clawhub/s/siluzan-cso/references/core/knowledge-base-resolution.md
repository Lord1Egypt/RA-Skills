# 知识库确定（通用）

> **唯一真相源**：凡任务需要锁定「用哪个企业知识库」（RAG 的 `--folder-id`、规划的 `--enterprise-id` / `--enterprise-name`、三库写稿前的 RAG 等），**先读本文件**，再决定是否调用 `rag list` / `planning enterprises`。
>
> 数据处理纪律见 `references/core/agent-conventions.md`。RAG 检索策略见 `references/rag.md`。规划域「知识库企业 ID vs 组织归属 ID」见 `references/planning.md`「两种企业 ID 勿混用」。

---

## `<knowledge_base_selection>` 是什么

DeerFlow / CSO 宿主在对话 system prompt 中注入的 XML 块，表达本轮知识库状态。可能是两种语义之一：

### A. 已选具体库（可用）

用户**已在界面「知识库」popover 选定具体企业知识库**（非「全部」、非「关闭」）。

典型一行内容类似：

```text
The user has selected a specific enterprise knowledge base for this turn: 「品牌资料库」(comid=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx).
```

从该段可解析：

| 字段  | 来源            | 含义                                                                                                   |
| ----- | --------------- | ------------------------------------------------------------------------------------------------------ |
| comid | `comid=…`       | 知识库企业目录 ID（与 `rag list` 的 `id`、`planning enterprises` 的 `id` / `folders[].id` **同口径**） |
| 库名  | 「…」中的展示名 | 向用户确认摘要、对话中称呼该库时用                                                                     |

> **术语**：业务上常叫 comid / 知识库企业 ID / folder id——在本 Skill 中指向**同一 UUID**，只是不同 CLI 命令的参数名不同（见下文映射表）。

### B. 知识库未开启（不可用）

块内出现类似文案（中英文皆可）：

```text
知识库功能未开启，不可使用。Do NOT call any enterprise KB tools …
```

表示本轮**知识库能力未开启**，**不可**走 RAG / 企业知识库检索路径。见下方「知识库未开启时」。

---

## 知识库未开启时（selection 含「不可使用」提示）

**识别**：`<knowledge_base_selection>` 存在，且内容含「知识库功能未开启」「不可使用」或等价英文（`Do NOT call any enterprise KB tools` 等）。

**强制动作**：

1. **禁止**调用一切 RAG / 知识库相关 CLI，包括但不限于：
   - `siluzan-cso rag list` / `rag query`
   - `siluzan-cso planning enterprises`（以及依赖企业知识库 ID 的 planning 检索路径）
   - 其他会打企业知识库 / KB 工具的命令
2. **先向用户说明**：本轮知识库不可用（界面未开启或未选库），因此无法做贴库检索 / 无法按知识库锁定企业。
3. **再按任务是否依赖知识库分支**：

| 任务性质       | 判定示例                                                                                           | 动作                                                                                                           |
| -------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **必须知识库** | 用户明确要求按知识库作答、三库写稿须贴库拆素材、品牌事实必须以 RAG 为准、planning 必须锁定企业库等 | **终止**当前依赖知识库的步骤；告知用户需在界面开启并选定知识库后重试；**禁止**用联网搜索、模型通识或猜 ID 顶替 |
| **非必须**     | 纯文案润色、人设闲聊、发布/账号操作、不依赖企业素材的通用问答等                                    | 告知知识库不可用后，**继续**用不依赖 RAG 的路径完成任务                                                        |

**禁止**：把「未开启」当成「无已选库」去走 `rag list` / 全库检索回退；也禁止静默跳过而不告知用户。

---

## 默认动作（有已选库且可用时）

仅当 selection 为 **A（含 `comid=`）** 时适用：

1. **直接使用**解析出的 `comid` 与库名。
2. **跳过**列表解析命令：
   - RAG → **跳过** `rag list`（不要再说「请先选知识库」或按名称重新匹配 ID）
   - 规划 → **跳过** `planning enterprises`（不要再说「请先选企业」）
3. **禁止**：声称用户未选择、反复索要 comid、或按名称重解析 ID（用户明确要换库时除外，见「例外」）。

---

## 语义对齐

- 用户说「我选的知识库 / 这个知识库 / the knowledge base I picked」→ **始终指** `<knowledge_base_selection>` 里**这一条**库（仅 A 态）。
- 用户**已经选过**；勿与「全部知识库检索」（无 selection、RAG 不传 `--folder-id`）混淆。
- 若为 **B 态（未开启）**，即使用户口头说「查知识库」，也按「知识库未开启时」处理，不可假装已选库。

---

## 无已选库时的回退

**触发条件**（满足其一即走回退；**不含**「未开启」B 态——B 态走上一节，禁止回退到 list）：

- 上下文中**没有** `<knowledge_base_selection>`，且用户也**未**给出可核验的知识库 ID（comid / folder id / enterprise-id）；或
- 用户只给了企业/库**名称**、未给 ID。

此时按场景解析：

| 场景     | 命令                                                       | 产出用途                                             |
| -------- | ---------------------------------------------------------- | ---------------------------------------------------- |
| RAG 检索 | `siluzan-cso rag list --rag-only --json-out ./snap-cso`    | 按名称语义匹配 → `--folder-id`                       |
| 内容规划 | `siluzan-cso planning enterprises [--json-out ./snap-cso]` | 按名称匹配 → `--enterprise-id` + `--enterprise-name` |

**匹配规则**：语义近似 > 包含关键词；多个近似匹配时让用户选择；**无匹配时如实说明并停止，禁止猜测 ID**（见 `agent-conventions.md`「无结果即停」）。

RAG **全库检索**（不传 `--folder-id`）仅当用户意图明确为跨库/公共素材且**未**指定品牌时。

### 人设默认知识库（写稿场景兜底）

三库写稿前解析 `--folder-id` 时，若**没有** `<knowledge_base_selection>`、用户本轮也**未**指定知识库，但当前已加载人设的 `knowledgeBaseId` 字段非空 → **默认用它作 `--folder-id`**（该字段即知识库 comid，与本文件其他 ID 同口径），无需再 `rag list`。

- 若 selection 为 **B 态（未开启）** → **不适用**本兜底：仍按「知识库未开启时」处理（写稿贴库属必须知识库时终止）。
- 用户本轮明确指定了别的库 / 明确要换库 → 以用户为准，忽略人设默认。
- 人设 `knowledgeBaseId` 为空 → 回到上方按名称 `rag list` / 全库检索的常规回退。

---

## 仍须 list / enterprises 的例外

| 情况                                                      | 动作                                                                                                                    |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 用户**明确要换**另一家企业/库，与已选不一致               | 重新 `rag list` 或 `planning enterprises` 解析新目标                                                                    |
| selection 里只有 `comid=`、无库名，且对话中也取不到展示名 | 只读 `planning enterprises --json-out` 或 `rag list --json-out` **核对名称**（ID 仍用 selection 的 comid，勿重解析 ID） |
| 无 `<knowledge_base_selection>`，用户只给了名称、未给 ID  | **必须**走上方「回退」列表命令                                                                                          |
| selection 含「知识库功能未开启 / 不可使用」               | **禁止** list / query；告知用户后按是否必须知识库继续或终止（见「知识库未开启时」）                                     |

---

## CLI 参数映射

| 从 selection / list 取得 | RAG（`rag query`）    | 规划（`planning generate` / `list` / …） |
| ------------------------ | --------------------- | ---------------------------------------- |
| comid（知识库企业 ID）   | `--folder-id <comid>` | `--enterprise-id <comid>`                |
| 库名 / list 的 `name`    | 向用户确认摘要时用    | `--enterprise-name`                      |

**禁止混用**：组织 `belong-to-id`、RAG 查询链路上的 `belongToId` / `companyId` **不是** `--enterprise-id` 或 `--folder-id`；规划域细节见 `references/planning.md`「两种企业 ID 勿混用」。

---

## 决策流程（速查）

```text
上下文有 <knowledge_base_selection>？
  ├─ 是 → 内容含「未开启 / 不可使用」？
  │       ├─ 是 → 禁止 rag / KB 相关命令 → 告知用户知识库不可用
  │       │       ├─ 任务必须知识库 → 终止依赖步骤，请用户开启并选定后再试
  │       │       └─ 任务非必须 → 用不依赖 RAG 的路径继续
  │       └─ 否（含 comid=）→ 取 comid + 库名 → 映射到 --folder-id / --enterprise-id+name → 跳过 list/enterprises
  │               └─ 用户明确换库？→ 是：走 list/enterprises 解析新目标
  └─ 否 → 用户给了可核验 ID？
          ├─ 是：直接用
          └─ 否 →（写稿场景）当前人设 knowledgeBaseId 非空？
                  ├─ 是：用它作 --folder-id
                  └─ 否：rag list 或 planning enterprises 按名称解析 → 无匹配则停止
```
