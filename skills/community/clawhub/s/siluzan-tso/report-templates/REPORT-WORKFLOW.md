# 报告生成流程

---

## 分析报告生成步骤

适用于：`google-analysis *`、`facebook-analysis *`、`report tiktok-*`、`report bing-*`、`report meta-overview` 等 CLI 拉数后由 Agent 撰写的报告。

**不适用**于 TSO 优化报告（`report create` / `report push` 等），那类报告由平台生成，不走此流程。

---

### 步骤 1：确认账户与区间

- 账户 ID 须来自 `siluzan-tso list-accounts -m <媒体>` 的实际输出，不能凭印象猜测。
- 明确起止日期（`--start` / `--end`）。

---

### 步骤 2：选定内容模板

根据媒体与用户意图，选择 `report-templates/` 下对应的 `*.md`：

| 意图                                                                                  | Google                                                                                             | Meta                               | TikTok                    | Bing                    |
| ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------- | ------------------------- | ----------------------- |
| 周期分析 / 月报 / 周报                                                                | `google-period-report.md`                                                                          | `meta-period-report.md`            | `tiktok-period-report.md` | `bing-period-report.md` |
| OKKI 周报 / 固定话术发客户（Google）                                                  | `okki-weekly-google-client.md`                                                                     | —                                  | —                         | —                       |
| **询盘分析** / 固定运营触发（Goog账户询盘分析 / 我给你询盘信息分析Google账号XXX效果） | `google-inquiry-analysis.md`（**严格 3 个月** + 用户上传询盘资料 + 8 Sheet xlsx；见 SKILL **P7**） | —                                  | —                         | —                       |
| 深度诊断 / 健康检查                                                                   | `google-account-diagnosis-report.md`                                                               | `meta-account-diagnosis-report.md` | 同周期，注明能力受限      | 同周期                  |

无精确匹配时，用最接近媒体的同类 `*.md`，并在报告开头注明。

---

### 步骤 3：展示默认维度 + 询问追加

**例外**：模板为 `okki-weekly-google-client.md` 或 `google-inquiry-analysis.md` 时**跳过**本节「追问可选追加」，按该文件固定维度拉数即可。`google-inquiry-analysis.md` 还要求**严格 3 个月**时间窗（分析月份 + 向前 2 个完整自然月），不可扩展。

1. 按选定 `*.md` 的**默认维度**开始拉数（**不必等用户回复后再拉**，可并行）。
2. 同时向用户发一条消息，说明本次默认包含哪些维度，并列出当前平台支持的**可选追加维度**，询问是否需要添加。
3. 报告正文按默认维度写；若用户追加了维度，数据回来后在末尾补充对应章节。

---

### 步骤 3b：Google Excel 门禁（用户要 xlsx 时必做）

在步骤 4 拉数完成、步骤 5 写脚本**之前**：

1. `list-accounts -m Google -k <用户 ID> --json-out` 核验账户（**禁止**全表 grep 换 ID）。
2. Read 本次每个 section 的 **`*.outline.txt`**（见 `google-period-report-excel.md` §执行门禁）。
3. **禁止** `cat|json.tool|head` 或 Read 业务 `*.json` 探字段；**禁止**加载宿主第三方 xlsx Skill。

### 步骤 4：拉取数据

- **`google-analysis` / `report …` 账户分析子命令**：统一 **`--json-out <目录>`** 落盘，再由脚本读 **`manifest-<accountId>.json` / `report-manifest-<accountId>.json`**（清单文件名见 stdout 摘要的 `manifestFile`）与各 **`<section>-<accountId>.json`**（见 `references/analytics/account-analytics.md`）。
- **`stats`、`ad campaigns` 等辅助命令**：按 `references/core/tips.md` 与各命令文档做结构化拉数。
- 仅执行与**本次报告维度**对应的命令（默认 + 用户追加）。
- 数据失败/缺失：在对应章节写 `[ 数据不可用：{原因} ]`，不写推测。

---

### 步骤 4b：交付前审阅最终产物（**必做**）

- 按 `references/core/agent-conventions.md` §七 自检表 A/B/C 审阅。
- **Read 刚生成的报告文件**（HTML/Markdown 等），对照当次 `report-templates/*.md` 逐项确认章节与币种。
- 未通过：**修改产物或补拉数据后重新生成**，再次 Read 审阅；不得在未审阅时交付。

---

### 步骤 5：分析并撰写中间产物

- 用 **node/python 脚本**读落盘 JSON，完成聚合与洞察（禁止 Read 业务 JSON、禁止对话手填数）。
- 按 `*.md` 章节结构组织叙事与建议；所有数字可追溯到 JSON 字段。
- **Meta/Facebook**：产出 `meta-period-report.json`（见 `meta-period-report.md`）。
- **Google 等**：可直接组织 Markdown/HTML 正文。

### 步骤 5b：生成终稿（按媒体与格式）

| 媒体              | 用户未指定格式                                                    | 用户指定 Excel                                                                                            |
| ----------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Meta/Facebook** | `facebook-analysis render` → **HTML**（必做）                     | Agent 脚本按 `meta-period-report-excel.md` 写 xlsx；**不**默认 `render`                                   |
| **Google**        | 按 `report-template*.html` 写 HTML（默认 `report-template.html`） | **周期/定制 Sheet**：`google-period-report-excel.md`（P4，先 outline 后脚本）；**OKKI**：P6；**询盘**：P7 |
| **网站诊断**      | `website-diagnosis render` → HTML                                 | —                                                                                                         |

**禁止**：Meta 周期报告默认只交 Markdown/JSON；禁止 Agent 手写 Meta HTML。

**Google 广告诊断报告**（`google-ads-diagnosis.md` / `google-account-diagnosis-report.md`）额外必遵：

1. **每日趋势**（`daily-metrics` / `conversionCost`）：金额、CPA **2 位小数**；转化/点击/展示为整数；图表轴与 tooltip 同规则。
2. **每个模块**在表/图后写 **分析**（≥2 条，有数据依据）+ **建议**（≥1 条）；禁止只贴表不写分析。详见 `google-ads-diagnosis.md` § 撰写硬约束。

---

### 步骤 6：末尾附数据来源（可选）

```
📌 数据来源：
- siluzan-tso google-analysis -a <id> --sections overview --start <s> --end <e>
- ...
```

---

## 未知报告名处理

| 用户措辞                                                                                                                                              | 映射                                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 月报、周报、投放总结、效果回顾                                                                                                                        | 周期分析 → 对应媒体 `*-period-report.md`                                                                                                                                                             |
| **使用 okki 周报模板 / OKKI 周报 / okki 周报**（Google + 区间）                                                                                       | **固定话术 + 精简表 +（按需）Excel** → `okki-weekly-google-client.md`（见 SKILL **P6**）；Excel **仅**由 Agent 脚本生成，**无** CLI 内置写表子命令                                                   |
| **Goog账户询盘分析 / Google 账户询盘分析 / 分析XXX Google账号的询盘效果 / 我给你询盘信息分析Google账号XXX效果**（或含「询盘 + 账户 + Google」三要素） | **询盘 + 账户合并分析 + 严格 3 个月 + 8 Sheet xlsx** → `google-inquiry-analysis.md`（见 SKILL **P7**）；询盘资料用户上传任意载体，宿主 Agent 解析落盘 `inquiries.json`，xlsx **仅**由 Agent 脚本生成 |
| 健康检查、诊断、账户分析                                                                                                                              | 诊断 → `google-account-diagnosis-report.md`（Google）或周期型降级                                                                                                                                    |
| 对比、汇报、给客户看                                                                                                                                  | 以周期型为骨架，简化版本                                                                                                                                                                             |

无法识别时，默认按**周期分析**处理，并在报告开头注明推断。
