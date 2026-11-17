# 方案文件 → campaign-create JSON

> **主路径**：Agent **编写并执行代码**，把方案文件直接转成与 `assets/campaign-create-template.json` 同构的 JSON → `ad campaign-validate` → 用户确认 → `ad campaign-create`。
> 版式不固定没关系——**认列、认匹配类型、认国家列表就是 Agent 的活**；脚本只负责落盘，避免在对话里手填大 JSON。

---

## 流水线

```text
方案文件（Excel 等）
        │
        │  Agent 写转换脚本（openpyxl / exceljs 等）
        │  + ad geo resolve 取地域 id（勿编造）
        ▼
   campaign.json  （campaign-create 契约）
        │
        ▼
 ad campaign-validate
        │
        ├─ 有不合规 → 【必问】用户自己改，还是 Agent 代改？（见下文）
        │
        └─ 通过 → 确认摘要 → ad campaign-create
```

| 步  | 谁做         | 动作                                                                                                                                    |
| --- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Agent + 脚本 | 读全 Sheet，按语义抽出预算/组/词+匹配类型/RSA/否词/国家等，写出 `campaign.json`（**先忠实落盘，勿静默改用户方案**）                     |
| 2   | CLI          | 国家列表 → `ad geo resolve -a <id> --from-file … --json-out …`，把返回的 `locations` / `targetedLocations` 写入 JSON（**禁止**编造 id）。落盘的 `unserved[]`（Google 不支持投放的地区）、`needsReview[]`（无精确同名，附 `topCandidates`）须在步 3b 一并问用户，禁止自行挑候选 |
| 3   | CLI          | `ad campaign-validate --config-file ./campaign.json`                                                                                    |
| 3b  | Agent → 用户 | **若有不合规**：列出问题清单 → **询问**「您自己改方案/文件，还是我帮您改？」→ 按用户选择处理后再 validate（见下节）                     |
| 4   | Agent → 用户 | 摘要确认：国家↔id、Exact/Phrase/Broad 条数（可抽样几条），**勿**贴整份 JSON                                                             |
| 5   | CLI          | 用户确认后 `ad campaign-create` → `batch get` / `batch diff`                                                                            |

---

## 用户方案不合规时：必须二选一询问（Agent 必遵）

**适用**：计划来源是用户提供的（Excel / 表格 / 粘贴方案 / 用户自写的 JSON），且出现下列任一情况：

| 类型                                | 示例                                                                                         |
| ----------------------------------- | -------------------------------------------------------------------------------------------- |
| `campaign-validate` error / warning | 词面非法字符、嵌套引号、RSA 跨组标题重复、超长、匹配类型与符号不一致、locations 数量不一致等 |
| 政策 / 合规明显风险                 | 违禁宣称、落地页与文案严重不符等（见 `google-ads-compliance.md`）                            |
| 转换时发现方案自相矛盾              | 同组同词多匹配类型冲突、必填块缺失、否词会屏蔽正向关键词（validate warning 列出被屏蔽词）等  |
| 出价/设备口径存疑                   | CPC 上限 ≥ 日预算；方案要求排除某设备但 `targetedPlatforms` 未写 `-100`                      |
| 地域无法解析                        | `geo resolve` 的 `unserved` / `needs_review` / `not_found` 项                                |

**禁止**：未询问就替用户改方案内容（改词面、改标题消重、截断、删词、改匹配类型等）然后直接 create。  
**禁止**：只丢一句「校验失败」就停住，不给选项。

**必做话术结构**（业务语言，勿贴整段 CLI）：

1. 说明：方案里有 **N 处**不合规（可表格：位置 / 原文要点 / 原因）。
2. **明确二选一**（一次问清）：
   - **A. 您自己改**：改 Excel/原文后发我，或告诉我改哪几处；我再重新转换/校验。
   - **B. 我帮您改**：您同意后，我按建议改 `campaign.json`，再 validate → 请您确认 → create；**创建完成后必须出「创建与修改报告」**（见下节）。
3. **停等用户回复**；选 B 时再动手改；选 A 时不要擅自改 JSON。
4. **选 B 时立刻落盘变更账本**（见下节「变更账本」）：每改一处就记一行「原值 → 新值 + 原因」，勿等创建完再凭记忆补写。

**例外（仍可静默做，不算「改方案」，也不进修改报告主表）**：`ad geo resolve` 取地域 id、剥 `_` 注解键、提交前金额元→分——这些是契约/网关要求，不是改用户业务内容。

**与「创建后自动补建」的区别**：用户已确认过 JSON 并 `campaign-create` 之后，BatchJob 漏掉的 Sitelink/地域用 `batch diff` **自动补建**（见 `google-ads-campaign-plan.md`）；那是执行层补洞，不是改用户方案。不合规询问发生在 **create 之前**。补建条数可写在报告「创建结果」里，但**不要**混进「相对原方案的修改」表。

---

## 创建失败后：只改报错项，禁止整类删减（Agent 必遵）

`campaign-create` 后 `batch get` 为 `Failed` / `HasFailed` 时，上节「先问再改」**同样适用**。真实事故：Agent 把 `negative … immutable` 误判为否词问题删光 163 个否词，又删光 36 个排除国家，最终系列与方案严重不符却向用户声称「已按方案排除」。

1. **先定位再动手**：带提交时的 `--config-file` 跑 `ad batch get --json-out`，读 `agentWorkflow.failedOperations[]`——CLI 已把 `mutate_operations[N]` 映射到 JSON 路径（如 `campaign.excludedLocations[12]`）。`cascade=true` 的「Resource was not found」是父资源（多为广告组）没建成的连带失败，修根因即可。
2. **只改映射到的那几项**，且改前告诉用户「哪一项、为什么、准备怎么改」；涉及方案业务内容（否词、排除/投放国家、关键词、文案）须用户同意。
3. **禁止**为了让创建通过而整类清空 `NegativeKeywordsForBatchJob` / `excludedLocations` / `targetedLocations` 或批量删词——即使「只是先建起来，之后再补」，也须先征得同意，并在交付报告里列出未补回的内容。
4. **禁止**猜测式试错（删 A 重提 → 不行再删 B 重提）。定位不到具体项时停下，把 `reason` 原文要点和可选方案给用户。
5. **交付前对照原方案**：`ad batch diff` 只能对照你传入的 JSON。若 JSON 相对原方案删减过（否词/排除地域/国家），交付时必须如实写出「原方案有 X，实际未设置」，**禁止**写「已按方案排除/已设置否词」。

### 政策违规（PolicyViolation）

- 创建前无法预检：网关没有 `validate_only` / 政策预检接口。`campaign-validate` 只对跨行业高拒审词面给 warning，地域相关政策只有创建后才知道。
- `failedOperations[]` 中带 `policyName`（如 `LEGAL_REQUIREMENTS`）与 `isExemptible`；路径指向具体关键词或文案。
- 地域相关政策（Legal requirements 等）**不会告诉你是哪个国家**触发——**禁止**用测试系列逐地域二分排查。
- 停下向用户报告：触发的词/文案清单 + 政策名 + 是否可豁免，给出选项：**去掉这些词** / **改写词面或文案** / **申请政策豁免**（`isExemptible=true` 时；需在 Google Ads 后台或由优化师处理）/ **由用户指定缩减投放国家**。按用户选择执行。

---

## 创建完成报告（必出）

**何时必出系列创建详情**：凡最终完成了 `campaign-create`（含 `batch get` / `batch diff` / 必要补建）之后——**无论是否代改方案**。结构见下节「创建了哪些」；多系列按系列分节。总纪律见 `agent-conventions.md` §四。

**何时另出完整修改表**：仅当用户选择「我帮您改」且 Agent 改过业务内容。用户全程自己改方案、Agent 未改业务内容 → **不必**出修改表，但仍须出系列创建详情。

### 变更账本（代改过程中维护）

落盘建议：`./snap-campaign/plan-edits.json`（或同目录 Markdown）。每条至少：

| 字段     | 说明                                                  |
| -------- | ----------------------------------------------------- |
| `path`   | JSON 路径或业务位置（如组名 + 关键词 / RSA 标题序号） |
| `from`   | 用户原方案中的值（改前）                              |
| `to`     | 实际写入并创建的值（改后）                            |
| `reason` | 修改原因（对应哪条 validate/合规规则，一句话）        |

**禁止**：创建结束后凭印象写「改了一些标题」；必须以账本为准。

### 面向用户的报告结构（业务语言）

创建与核对结束后，用一份短报告回复用户：

1. **创建了哪些（每个系列必有）**  
   **直接发送** `ad batch diff` 生成的 **`reportMarkdown` 全文**（Markdown；亦见 `reportMarkdownFile`）。报告已含账户/系列/`campaignId`、数量汇总、按组展开的关键词与 RSA 文案状态、仍未创建项。若有自动补建可在文末补一句。**禁止**只汇总条数或不发 Markdown。

2. **修改了哪些（相对您的原方案）**——**仅代改时必出**  
   表格逐条：**位置 | 从（原值） | 改成（新值） | 原因**。
   - `from` / `to` 写清原文，勿只写「已优化」。
   - 无业务修改则写「相对您的原方案无业务内容修改」（仅 geo id 解析等不写进此表）。

3. **未改动的说明（可选一句）**  
   如：匹配类型/国家列表按您的方案保留。

**禁止**：只说「已创建成功 / 未发现缺失」而不列系列详情；代改时**禁止**省略修改表；**禁止**把创建结果与修改混成一团让用户自己猜改了啥。

可选脚手架（非必须）：`assets/plan-extract.example.json` + `assets/scripts/assemble-campaign-from-plan.mjs`——若 Agent 更习惯先抽中间件再组装，可以用；**不强制**。

---

## Agent 转换脚本须守住的点

1. **匹配类型**：方案里有「完全/词组/广泛」列或 `[词]` / `"词"` / 裸词时，写入对应 `MatchTypeV2` 块（EXACT / PHRASE / BROAD），**不要**图省事压成一律 BROAD。
2. **地域 id**：只来自 `ad geo resolve`（或多国一次 resolve；单国也可用 `ad geo search`）。`locations` 与 `targetedLocations` 同序同量。
3. **结构**：先 Read `assets/campaign-create-template.json`，脚本输出同构；RSA 15 标题 + 4 描述；否词只进 `NegativeKeywordsForBatchJob`。
4. **落盘**：用脚本 `--out` / `writeFile`，**禁止**在对话里手写完整 campaign JSON。

---

## CLI 硬校验（兜底）

| 条件                                                | `campaign-validate` |
| --------------------------------------------------- | ------------------- |
| `locations` 非空且与 `targetedLocations` 数量不一致 | error               |
| location `id` 非数字                                | error               |
| 同一 id 同时在 `targetedLocations` 与 `excludedLocations` | error（多为 geo resolve 把「刚果」等歧义地名解析到同一国家，用 `ad geo search` 核对该条） |
| 广告组 `MaxCPCAmount` 缺省或 ≤ 0（任何出价策略）     | error（后端恒写 `cpc_bid_micros`，0 会被 Google 拒「Too low」） |

匹配类型是否与方案一致，靠 Agent 转换脚本 + 确认摘要；validate 负责契约与词面/`MatchTypeV2` 对齐。

---

## 相关文档

- `google-ads-campaign-plan.md` — W3 总流程
- `assets/campaign-create-template.json` — JSON 结构真相源
- `google-ads.md` — `ad geo resolve` / `campaign-create` 命令
