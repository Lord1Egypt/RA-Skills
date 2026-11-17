# Google 搜索广告：方案生成与系列创建

> **新建/规划搜索系列时 Read 本文件**。写命令见 `google-ads-write.md`；batch 见 `google-ads-batch.md`；查询见 `google-ads-read.md`。
>
> **类型边界**：本文件仅覆盖 **搜索广告（Search）**。PMax 走 `pmax-api.md` / `pmax-create-template`。**不支持展示广告（Display）**——用户要 Display 时须说明不支持，勿用本文件 JSON 伪装。

---

## 常见入口语（路由到本文件，勿走偏）

| 用户说法（示例）                                  | 正确工作流                                                                                                        | **禁止**                                             |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| 「根据 www.example.com 官网生成 Google 搜索广告」 | **W3 · 本文件标准流水线**                                                                                         | 只输出一张手写关键词/RSA 表；走 P8 网站诊断          |
| 「按这份 Excel / 投放方案创建广告」               | **方案源轨**（下表）+ **必读** `rules/google-ads-plan-source-fidelity.md`                                         | 猜 geo id；关键词一律 BROAD；跳过 validate           |
| 「要表格格式 / 表格给我」                         | 先 JSON →（有账户且要创建才 `campaign-validate`）→ 按 `google-ads-launch-plan-template.md` **投影 Markdown 表格** | 跳过 JSON 直接填表；因缺账户不给表格                 |
| 「帮我写搜索广告文案/关键词」且未指定已有系列     | **W3**（含官网/RAG 归纳背景）                                                                                     | 与 W5 纯拓词混淆（W5 无系列/组/RSA 结构）            |
| 「先出方案 / 先别开户 / 先别投钱 / 只要方案」     | **仅出方案**（见下节；**不**索要账户）                                                                            | 卡在 `list-accounts` / 要 mediaCustomerId 才肯出方案 |
| 「分析这个网站能不能投广告」                      | **P8** 网站诊断                                                                                                   | 本文件建户方案                                       |

### 仅出方案 vs 创建（硬门禁）

| 阶段         | 触发（满足其一即可）                                                                                   | 要不要 Google 账户 | Agent 必须做                                                                                                                       | **禁止**                                                                                                    |
| ------------ | ------------------------------------------------------------------------------------------------------ | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **仅出方案** | 「出方案 / 规划 / 先别创建 / 先别开户 / 先别投钱 / 只要表格」；或用户**未**给账户且**未**说要创建/发布 | **不必须**         | 落盘同构 JSON → **写代码**投影完整审查稿（默认 MD；用户指定则 Excel 等）；`account` / geo 数字 id 用占位并标注「待选定账户后补」   | **因缺账户 ID 阻塞交付**；只交概览表；未确认创建就跑 `list-accounts` 逼用户给号；未确认就 `campaign-create` |
| **创建**     | 用户已确认方案并明确要创建/发布，或已提供可用 `mediaCustomerId` 且意图是落地                           | **必须**           | `list-accounts` → `geo resolve` → 填真 id → `campaign-validate` → **写代码投影完整审查稿** → 用户确认 → `campaign-create` → batch… | 编造 geo id；跳过 validate；跳过完整审查稿                                                                  |

**缺参时（仅出方案）**：用户只给官网 URL、未给预算/地域/账户 → 先从官网归纳产品/落地页（必要时 `google-ads-landing-page-discovery-via-webfetch.md`），预算/地域可合理默认并在方案里写明假设；**账户 ID 一律不追问为前置条件**（写 `[PENDING_ACCOUNT]` 即可）。仅当缺官网且无法推断产品时才追问 1 项；不得因信息不全就降级为「随便写几条广告」，也**不得**把「请先提供广告账户」当成第一步。

**占位约定（仅出方案）**：外层 `account` 填 `"[PENDING_ACCOUNT]"`（或 `""`）；`locations` 用国家中英文名；`targetedLocations` 可暂空数组或与 `locations` 同长的占位串——**交付时注明「选定账户后须 `ad geo resolve` 写回真 id，再 validate」**。此阶段**跳过** `list-accounts` / `ad geo resolve|search` / `campaign-validate` / `campaign-create`（无账户时这些命令无法合法完成）。

---

| 轨           | 条件                                                            | 动作                                                                                                                                                                                             |
| ------------ | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **方案源轨** | 用户已给 Excel/表格/结构化投放方案（含地域、词、匹配类型等）    | **先 Read** `rules/google-ads-plan-source-fidelity.md` → Agent **写脚本**转 JSON；**有账户且要创建**时再 `ad geo resolve` → validate → 确认 → create；**仅出方案**则脚本产出后停在 JSON+Markdown |
| **直读直写** | 用户已给账户/预算/组/词/RSA 等结构化数据（非文件，或已是 JSON） | 转为 campaign-create JSON →（要创建则）validate → 确认 → create                                                                                                                                  |
| **方案先行** | 无完整结构，或要求「先出方案」                                  | 读本文件 + 必读规则 → 生成 JSON + Markdown；**仅出方案到此为止**；用户确认创建且已有账户后再 validate → create                                                                                   |

**硬约束**

- 可执行真相只有 **JSON**（`assets/campaign-create-template.json` 同构）；Markdown 只读投影。
- **Agent Read 顺序（建系列 / 出方案前必做）**：① `assets/campaign-create-template.json`（复制/改写的结构真相源）→ ② `assets/campaign-create-template.md`（字段说明与踩坑）。**禁止**只读 `.md` 凭印象拼 JSON。
- **方案文件（Excel 等）额外必读**：`references/google-ads/rules/google-ads-plan-source-fidelity.md`（Agent **写代码**直接转成 campaign-create JSON；禁止对话手填完整 JSON）。
- 改需求 **改转换脚本重跑**；若已进入创建阶段则再 `campaign-validate`，再刷新 Markdown。
- **PMax 系列创建**走独立流水线（勿用本文件 JSON 模板）：**先 Read `assets/pmax-create-template.json`** + `assets/pmax-create-template.md` + `rules/google-ads-pmax-launch-plan-template.md`；落盘 JSON →（创建阶段 `pmax-validate`）→ **写代码投影完整审查稿** → 用户确认 → `pmax-create`；**Lead Gen/B2B 默认含 `campaignExtensions.leadForm`**（审查稿须单列表单节）。运营诊断见 `rules/google-ads-pmax-guide.md`。PMax **仅出方案**同样**禁止**因缺账户阻塞；`account` 占位，跳过 validate/create。
- 搜索网络：仅 Google 搜索（`TargetSearchNetwork`/`TargetContentNetwork`/`TargetPartnerSearchNetwork` 均为 false）。
- **地域 id（创建阶段）**：多国用 **`ad geo resolve`**（单国可用 `ad geo search`）；**禁止**编造 / ISO 心算。外层 `locations` 与 `targetedLocations` 数量必须一致（validate 硬校验）。**仅出方案**可用国家名占位，勿为取 id 而先逼用户给账户。
- **匹配类型**：转换脚本按方案写入 EXACT/PHRASE/BROAD 分块（有方案源时勿压成一律 BROAD）。

---

## 标准流水线

> **仅出方案**：做步 0（若有方案文件）→ **跳过**步 1～3 的账户/geo CLI → 做步 4～5（词与 JSON）→ **跳过**步 6 validate → 做步 7（Markdown，国家名即可）→ **停住等用户确认**；用户确认创建并给出账户后再从步 1 续跑。

| 步  | 动作                                                                                                                                                                                                             | 文档/命令                                                                                   |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 0   | **方案源轨**：Agent 写转换脚本：方案文件 → `campaign.json`；**创建阶段**地域用 **`ad geo resolve --json-out`** 写入（**勿**对话手填）                                                                            | **`rules/google-ads-plan-source-fidelity.md`** + **`assets/campaign-create-template.json`** |
| 1   | **创建阶段**：`list-accounts` 锁定 `account` / `customerName` / 币种；**仅出方案且无账户 → 跳过**                                                                                                                | `references/accounts/currency.md`                                                           |
| 2   | 可选 `rag query`；无现成词表时再 `keyword` / `keyword geo-list` 拓词（`keyword` **可不传** `-a`）                                                                                                                | `references/analytics/keyword-planner-workflows.md`                                         |
| 3   | **创建阶段**：无方案文件时多国 **`ad geo resolve`**（或单国 `ad geo search`）写入 `locations` + `targetedLocations`；**仅出方案 → 跳过，国家名占位**                                                             | **禁止编造 id**                                                                             |
| 4   | 无方案文件时：按分层写入 `KeywordsForBatchJob`（EXACT/PHRASE/BROAD）；否词进 `NegativeKeywordsForBatchJob`                                                                                                       | 参考 `google-ads-keyword-taxonomy.md`；有方案源则走步骤 0                                   |
| 5   | 得到与模板同构的 `campaign-create` JSON（仅出方案时 `account`=`[PENDING_ACCOUNT]`）                                                                                                                              | **`assets/campaign-create-template.json`**                                                  |
| 6   | **创建阶段**：`ad campaign-validate --config-file <json>`；**仅出方案 → 跳过**，交付时说明「有账户后再 validate」                                                                                                | 下文「校验」                                                                                |
| 6b  | **方案来自用户且不合规**（创建前）：列出问题 → **询问**「您自己改还是我帮您改？」→ 按选择处理后再 validate（**禁止**未问就静默改方案）                                                                           | **`rules/google-ads-plan-source-fidelity.md`** § 用户方案不合规                             |
| 6c  | 用户选「我帮您改」：改 JSON 时**同步落盘变更账本**（from → to + reason）                                                                                                                                         | 同上 § 创建完成报告                                                                         |
| 7   | **审查稿（必做）**：Agent **写代码**读 JSON，按 `google-ads-launch-plan-template.md` 投影完整文件（默认 MD；用户要 Excel 等则改格式）；须含全部关键词与 RSA 正文；**禁止**概览表代替；**勿**贴整份 JSON 当主交付 | `google-ads-launch-plan-template.md`                                                        |
| 8   | 用户确认后 **`ad campaign-create`**                                                                                                                                                                              | `references/google-ads/google-ads-write.md`                                                 |
| 9   | 每隔5s 获取创建结果                                                                                                                                                                                              | `ad batch get --id <taskId> --config-file ./campaign.json`                                  |
| 10  | 成功或部分成功后 **`ad batch diff`** 对照 JSON 与账户实况                                                                                                                                                        |                                                                                             |
| 11  | **立刻交付创建详情**：把 diff stdout 中 `BEGIN_USER_DELIVERY_MARKDOWN`…`END` 全文原样发给用户（先于补建；禁止只贴汇总表）                                                                                        | `agent-conventions.md` §四                                                                  |
| 12  | **自动补建缺失项**（见下文）：扩展/地域等执行 `remediateCommand`；补建后再 diff 时可再发更新版详情。**勿**仅反问用户是否补建                                                                                     | `references/google-ads/google-ads-batch.md` § batch diff 后自动补建                         |
| 13  | 代改过方案时**另附**修改表（从 xxx → xxx + 原因）                                                                                                                                                                | **`rules/google-ads-plan-source-fidelity.md`** § 创建完成报告                               |

多系列：每系列一个 JSON；可选 `campaign-manifest.json`（`role: brand|competitor|generic`）仅作文件组织参考。

---

## 规则文档：分层阅读（勿一次读 12 份）

### 必读（出方案前）

| 文档                                                                              | 用途                                                            |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `references/google-ads/rules/google-ads-plan-source-fidelity.md`                  | **有 Excel/表格方案时必读**：地域 geo search、匹配类型分块保真  |
| `references/google-ads/rules/google-ads-keyword-taxonomy.md`                      | 无方案源时的核心/长尾与匹配块**建议**                           |
| `references/google-ads/rules/google-ads-compliance.md`                            | 词与文案合规                                                    |
| `references/google-ads/rules/sensitive-industries.md`                             | 敏感行业（若相关）                                              |
| `references/google-ads/rules/google-ads-launch-plan-template.md`                  | 搜索审查稿结构；Agent 写代码从 JSON 投影                        |
| `references/google-ads/rules/google-ads-pmax-launch-plan-template.md`             | PMax 审查稿结构；Agent 写代码从 JSON 投影                       |
| `references/google-ads/rules/google-ads-creative-optimization.md`                 | RSA **B2B/B2C 满 15+4 配方**；`campaign-validate` 强制 **15** 标题 + **4** 描述 |
| **`assets/campaign-create-template.json`** + `assets/campaign-create-template.md` | JSON 结构（先 Read `.json`）+ 字段说明                          |

### 按需（触及时再读）

| 文档                                                                            | 何时                                                                                                    |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `references/google-ads/rules/google-ads-keyword-strategy.md`                    | 分组/匹配/否定词策略争议                                                                                |
| `references/google-ads/rules/google-ads-campaign-optimization.md`               | 出价策略、预算、学习期                                                                                  |
| `references/google-ads/rules/google-ads-landing-page-discovery-via-webfetch.md` | 仅首页、需推断 PDP/PLP                                                                                  |
| `references/google-ads/rules/google-ads-conversion-architecture.md`             | 转化/EC/归因说明                                                                                        |
| `references/google-ads/rules/google-ads-keyword-optimization.md`                | 上线后优化，非首建                                                                                      |
| `references/google-ads/rules/google-ads-account-audit.md`                       | 账户诊断，非首建                                                                                        |
| `references/google-ads/rules/google-ads-audience-strategy.md`                   | 受众/RLSA                                                                                               |
| `references/google-ads/rules/google-ads-pmax-guide.md`                          | PMax 运营/诊断；**创建**见 `assets/pmax-create-template.md` + `google-ads-pmax-launch-plan-template.md` |
| `references/google-ads/pmax-api.md`                                             | PMax 网关路径与 Search API 边界                                                                         |

复述给用户：**3–5 条**与本次任务相关的合规/策略要点即可，无需罗列全部文件名。

---

## 创建前最小命令清单（Search / PMax 落地）

> **禁止**臆造命令名：列表是 `ad campaigns`，**不是** `ad-campaigns` / `campaign list`。`balance`/`stats` **必须** `-m Google`。geo/ad 的 403/500 **禁止**臆测授权过期 → `account check-access`（套餐已激活时）。

1. `list-accounts -m Google -k <mediaCustomerId> --json-out ./snap`（核验存在 / 套餐 / `invalidOAuthToken`）
2. 套餐已激活 → `account check-access -a <mediaCustomerId> --json-out ./snap`（以 `status` 为准）
3. 地域：单国 `ad geo search -a <id> -q "United States" --json-out ./snap-geo`；多国 `ad geo resolve … --json-out`（读 `picked` / `targetedLocations`，**禁止**编造 id）
4. 落盘同构 JSON → `ad campaign-validate` / `ad pmax-validate --json-out …`（修到 `ok:true`）
5. **写代码**投影完整审查稿 → 用户确认
6. `ad campaign-create` / `ad pmax-create --commit "…"`
7. `ad batch get --id <taskId> --config-file … --json-out …` → **读 `agentWorkflow`**：无 `campaignId` 时**不要**跑 `batch diff`，按 `agentHint` 改 JSON 重提；有 `campaignId` 且 `nextCommand` 含 diff 再跑
8. 仅当有 `campaignId`：`ad batch diff` → 有 `remediateCommand` 则补建

## 校验与创建（命令速查）

```bash
siluzan-tso ad campaign-validate --config-file ./campaign.json --json-out ./snap-campaign
siluzan-tso ad campaign-validate --config-file ./campaign.json [--json-out ./snap] [--write-normalized [path]]   # 不带 path 时原地覆盖
siluzan-tso ad campaign-create --config-file ./campaign.json
siluzan-tso ad batch get --id <taskId> --config-file ./campaign.json
siluzan-tso ad batch diff --batch-id <taskId> --config-file ./campaign.json
siluzan-tso ad geo resolve -a <accountId> --from-file ./locations.json --json-out ./snap-geo
siluzan-tso ad geo search -a <accountId> -q "United States" --json-out ./snap-geo
siluzan-tso ad campaigns -a <accountId> --json-out ./snap
siluzan-tso ad extension snippet-headers --json-out ./snap
```

validate 与 create **共用** `runCampaignCreateValidation`：词面规范化 + 后端/Google 硬约束（预算、RSA、匹配符号与 `MatchTypeV2` 对齐、搜索网络、`locations`/`targetedLocations` 数量一致、STRUCTURED_SNIPPET 合法英文标头等）。**不含**关键词分层数量建议、否词条数下限（策略表仍见 taxonomy）。`BudgetBudgetDeliveryMethodV2=ACCELERATED` 多数账户会被 Google 拒 → validate **警告**，建议 `STANDARD`。

### 超长内容：禁止 Agent 自动截断

标题/描述/Path/关键词/Sitelink 超限时 CLI **报错阻断**，不会在 JSON 里静默改短。

1. 使用 **`ad campaign-validate --config-file <json> --json-out <dir>`**（与 create/batch 同一落盘目录），读落盘文件中的 `lengthViolations`（每项含 `path`、`limit`、`actual`、**完整** `text`）。
2. Agent 将 **全部** 超长条目整理成表（路径、原文、上限、超出量），并为每条给出 **1–2 个改写方案**（保留卖点、符合字符计数；CJK 按 2 计见 `google-ads-compliance.md` §3.2.1）。
3. **方案来自用户时**：先按 `google-ads-plan-source-fidelity.md` 询问「您自己改还是我帮您改？」；选「我帮您改」并确认改写方案后，再改 JSON。
4. **用户确认**选用方案后，Agent **只改 JSON 对应字段**，再执行 `campaign-validate`；通过后再 `campaign-create`。
5. **禁止**：未确认前 `slice`/省略号截断、仅改 `--write-normalized` 而不经用户确认。

人读模式失败时 CLI 会额外打印「📏 超长内容清单」；`--json-out` 时见 `lengthViolations` + `agentHint`。

---

## batch diff 后自动补建（Agent 必遵）

`campaign-create` BatchJob **常漏附加信息**（Sitelink）与 **投放国家**；系列/组/关键词/RSA 已创建成功时，**不要**停在「需要我现在补上吗？」——用户确认 JSON 时已包含这些内容，Agent **应自动补建**。

| 步骤 | 动作                                                                                                                                                                                               |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | `ad batch get --id <taskId> --config-file ./campaign.json --json-out ./snap-campaign` 直至终端态（Creating 时每 5s 轮询；**读落盘 `agentWorkflow.nextCommand`**，勿只看人读提示）                  |
| 2    | `Successfully` / `HasFailed`：执行 `agentWorkflow.nextCommand`（即 `ad batch diff … --json-out`）；**Failed** 勿 diff                                                                              |
| 3    | **立刻交付**：把本次 diff stdout 中 `BEGIN_USER_DELIVERY_MARKDOWN`…`END_USER_DELIVERY_MARKDOWN` 全文原样发给用户（即 `reportMarkdown`）。**禁止**只贴系列 ID/counts 摘要，**禁止**等补建结束再交付 |
| 4    | 读落盘 `ok` / `missing[]`；`layer=location` → `ad geo add`；`layer=extension` → 执行 `remediateCommand`                                                                                            |
| 5    | 无 `remediateCommand` 时，按 JSON 路径映射 `ad extension *` / `adgroup-create` / `keyword-create` / `ad-create` / `keyword-negative-create`                                                        |
| 6    | 有缺失时 CLI **exit 2**；补建后再 `ad batch diff`，直到 `ok===true`；每次 diff 后若状态有变可再发更新版详情                                                                                        |
| 7    | 可简短补充「已自动补上 N 个投放国家 / M 条 Sitelink」（**不能代替**步骤 3 的 Markdown 全文）                                                                                                       |
| 8    | 仅当补建命令也失败时，才向用户说明原因并给改写方案；代改方案另附修改表见 `google-ads-plan-source-fidelity.md`                                                                                      |

**Agent 易漏点**：`--json-out` 时人读「下一步」不会打印——**必须以落盘 `agentWorkflow` 为准**；`campaign-create` 落盘同样带 `agentWorkflow.nextCommand`（首轮 `batch get`）。

**Sitelink 单条示例**（字段来自 `ExtensionsForBatchJob[i].Properties`）：

```bash
siluzan-tso ad extension sitelink -a <accountId> \
  --level Campaign --campaign-id <campaignId> \
  --text "<Properties.Text>" --url "<Properties.DestinationUrl>" \
  [--line2 "<Line2>"] [--line3 "<Line3>"] \
  --json-out ./snap
```

**禁止**：系列主体已按计划建成，却因 Sitelink batch 失败就结束任务、等用户二次确认（除非用户明确说「先不要挂扩展」）。

---

## 已上线后的修改

- **勿**用 `campaign-create` 覆盖已有系列；用 `ad campaign-edit` / `adgroup-*` / `keyword-*` / `ad-edit` 等（见 `references/google-ads/google-ads-write.md`）。
- 若属「推倒重建」：更新 JSON → validate → 新系列 `campaign-create` 或删系列后重提。
