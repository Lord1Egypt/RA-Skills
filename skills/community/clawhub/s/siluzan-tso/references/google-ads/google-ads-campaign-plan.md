# Google 搜索广告：方案生成与系列创建

> 所属 skill：`siluzan-tso`。**新建/规划搜索系列时 Read 本文件**，再按需打开下表子文档。命令参数与 CRUD 见 `references/google-ads/google-ads.md`。

---

## 常见入口语（路由到本文件，勿走偏）

| 用户说法（示例） | 正确工作流 | **禁止** |
| ---------------- | ---------- | -------- |
| 「根据 www.example.com 官网生成 Google 搜索广告」 | **W3 · 本文件标准流水线** | 只输出一张手写关键词/RSA 表；走 P8 网站诊断 |
| 「要表格格式 / 表格给我」 | 先 JSON → `campaign-validate` → 再按 `google-ads-launch-plan-template.md` **投影 Markdown 表格** | 跳过 JSON 直接填表；把表格当唯一交付物 |
| 「帮我写搜索广告文案/关键词」且未指定已有系列 | **W3**（含官网/RAG 归纳背景） | 与 W5 纯拓词混淆（W5 无系列/组/RSA 结构） |
| 「分析这个网站能不能投广告」 | **P8** 网站诊断 | 本文件建户方案 |

**缺参时**：用户只给官网 URL、未给预算/地域/账户 ID → 先从官网归纳产品/落地页（必要时 `google-ads-landing-page-discovery-via-webfetch.md`），**列出仍缺项并追问**，再进入下表「方案先行」轨；不得因信息不全就降级为「随便写几条广告」。

---

| 轨           | 条件                                     | 动作                                                                     |
| ------------ | ---------------------------------------- | ------------------------------------------------------------------------ |
| **直读直写** | 用户已给账户/预算/组/词/RSA 等结构化数据 | 通过代码转换为 campaign-create直接可用的 JSON → validate → 确认 → create |
| **方案先行** | 无完整结构，或要求「先出方案」           | 读本文件 + 必读规则 → 生成 JSON → validate → Markdown → 确认 → create    |

**硬约束**

- 可执行真相只有 **JSON**（`assets/campaign-create-template.json` 同构）；Markdown 只读投影。
- **Agent Read 顺序（建系列前必做）**：① `assets/campaign-create-template.json`（复制/改写的结构真相源）→ ② `assets/campaign-create-template.md`（字段说明与踩坑）。**禁止**只读 `.md` 凭印象拼 JSON。
- 改需求 **只改 JSON**，再 `campaign-validate`，再刷新 Markdown。
- **PMax 系列创建**走独立流水线（勿用本文件 JSON 模板）：**先 Read `assets/pmax-create-template.json`** + `assets/pmax-create-template.md` + `ad pmax-validate` / `ad pmax-create`；**Lead Gen/B2B 方案默认含 `campaignExtensions.leadForm`**（方案 Markdown 须单列表单）；运营诊断见 `google-ads/rules/google-ads-pmax-guide.md`。
- 搜索网络：仅 Google 搜索（`TargetSearchNetwork`/`TargetContentNetwork`/`TargetPartnerSearchNetwork` 均为 false）。

---

## 标准流水线

| 步 | 动作 | 文档/命令 |
|----|------|-----------|
| 1 | `list-accounts` 锁定 `account` / `customerName` / 币种 | `references/accounts/currency.md` |
| 2 | 可选 `rag query`；`keyword` / `keyword geo-list` 拓词 | `references/analytics/keyword-planner-workflows.md` |
| 3 | 按分层规则写入 `KeywordsForBatchJob`（Exact/Phrase/Broad）；**否词单独写** `NegativeKeywordsForBatchJob`（勿与正向词混放） | `google-ads/rules/google-ads-keyword-taxonomy.md`（参考，非 CLI 强制） |
| 4 | 复制 `campaign-create-template.json` 并填 `campaign`（预算/出价/地域/否词≥20/RSA/附加信息） | **`assets/campaign-create-template.json`** + `assets/campaign-create-template.md` |
| 5 | **`ad campaign-validate --config-file <json>`**（失败只改 JSON；超长见下文「超长人工确认」） | 下文「校验」 |
| 6 | 输出：**JSON 代码块** → **Markdown**（`google-ads-launch-plan-template.md` 正文）→ 待确认 | — |
| 7 | 用户确认后 **`ad campaign-create`** | `google-ads/google-ads.md`|
| 8 | 每隔5s 获取创建结果| `ad batch get --id <taskId> --config-file ./campaign.json` |
| 9 | 创建失败根据失败原因修改json重新走创建流程，部分成功/成功/部分失败：都调用来做最后一步调整 `ad batch diff --batch-id <taskId> --config-file ./campaign.json` | |
| 10 | 输出所有失败的内容与原因，并询问用户是否需要修改后单独添加到系列中如果用户要求是则读取 `references\google-ads/google-ads.md` 来获取对应缺失部分的创建命令 |



多系列：每系列一个 JSON；可选 `campaign-manifest.json`（`role: brand|competitor|generic`）仅作文件组织参考。

---

## 规则文档：分层阅读（勿一次读 12 份）

### 必读（出方案前）

| 文档                                                   | 用途                                                            |
| ------------------------------------------------------ | --------------------------------------------------------------- |
| `google-ads/rules/google-ads-keyword-taxonomy.md`      | 核心/长尾与匹配块**建议**（Agent 参考，CLI 不强制）             |
| `google-ads/rules/google-ads-compliance.md`            | 词与文案合规                                                    |
| `google-ads/rules/sensitive-industries.md`             | 敏感行业（若相关）                                              |
| `google-ads/rules/google-ads-launch-plan-template.md`  | 用户可见 Markdown 结构与 RSA/否词表                             |
| `google-ads/rules/google-ads-creative-optimization.md` | RSA 创意主题；`campaign-validate` 强制 **15** 标题 + **4** 描述 |
| **`assets/campaign-create-template.json`** + `assets/campaign-create-template.md` | JSON 结构（先 Read `.json`）+ 字段说明 |

### 按需（触及时再读）

| 文档                                                                 | 何时                                                        |
| -------------------------------------------------------------------- | ----------------------------------------------------------- |
| `google-ads/rules/google-ads-keyword-strategy.md`                    | 分组/匹配/否定词策略争议                                    |
| `google-ads/rules/google-ads-campaign-optimization.md`               | 出价策略、预算、学习期                                      |
| `google-ads/rules/google-ads-landing-page-discovery-via-webfetch.md` | 仅首页、需推断 PDP/PLP                                      |
| `google-ads/rules/google-ads-conversion-architecture.md`             | 转化/EC/归因说明                                            |
| `google-ads/rules/google-ads-keyword-optimization.md`                | 上线后优化，非首建                                          |
| `google-ads/rules/google-ads-account-audit.md`                       | 账户诊断，非首建                                            |
| `google-ads/rules/google-ads-audience-strategy.md`                   | 受众/RLSA                                                   |
| `google-ads/rules/google-ads-pmax-guide.md`                          | PMax 运营/诊断；**创建**见 `assets/pmax-create-template.md` |
| `references/google-ads/pmax-api.md`                                  | PMax 网关路径与 Search API 边界                             |

复述给用户：**3–5 条**与本次任务相关的合规/策略要点即可，无需罗列全部文件名。

---

## 校验与创建（命令速查）

```bash
siluzan-tso ad campaign-validate --config-file ./campaign.json --json-out ./snap-campaign
siluzan-tso ad campaign-validate --config-file ./campaign.json [--json-out ./snap] [--write-normalized <path>]
siluzan-tso ad campaign-create --config-file ./campaign.json
siluzan-tso ad batch get --id <taskId> --config-file ./campaign.json
siluzan-tso ad batch diff --batch-id <taskId> --config-file ./campaign.json
siluzan-tso ad geo search
```

validate 与 create **共用** `runCampaignCreateValidation`：词面规范化 + 后端/Google 硬约束（预算、RSA、匹配符号与 `MatchTypeV2` 对齐、搜索网络等）。**不含**关键词分层数量、匹配占比、否词条数下限。

### 超长内容：禁止 Agent 自动截断

标题/描述/Path/关键词/Sitelink 超限时 CLI **报错阻断**，不会在 JSON 里静默改短。

1. 使用 **`ad campaign-validate --config-file <json> --json-out <dir>`**（与 create/batch 同一落盘目录），读落盘文件中的 `lengthViolations`（每项含 `path`、`limit`、`actual`、**完整** `text`）。
2. Agent 将 **全部** 超长条目整理成表（路径、原文、上限、超出量），并为每条给出 **1–2 个改写方案**（保留卖点、符合字符计数；CJK 按 2 计见 `google-ads-compliance.md` §3.2.1）。
3. **用户确认**选用方案后，Agent **只改 JSON 对应字段**，再执行 `campaign-validate`；通过后再 `campaign-create`。
4. **禁止**：未确认前 `slice`/省略号截断、仅改 `--write-normalized` 而不经用户确认。

人读模式失败时 CLI 会额外打印「📏 超长内容清单」；`--json-out` 时见 `lengthViolations` + `agentHint`。

---

## 已上线后的修改

- **勿**用 `campaign-create` 覆盖已有系列；用 `ad campaign-edit` / `adgroup-*` / `keyword-*` / `ad-edit` 等（见 `google-ads/google-ads.md`）。
- 若属「推倒重建」：更新 JSON → validate → 新系列 `campaign-create` 或删系列后重提。
