# Agent 执行规范（唯一规则真相源）

> 本文件是 siluzan-tso Skill 下 AI 助手的**全部通用纪律**：加载纪律、数据处理协议、时间/币种、批量约束、交付自检。
> 其他文档（SKILL.md、playbooks、workflows、各域 reference）**不再重复**这些规则，只在需要处单行指向本文件。
> CLI 参数细节见各域 reference；脚本示例见 `references/core/tips.md`（食谱，按需查）。

---

## 一、文档加载纪律

本 Skill 采用 **SKILL 路由 + references 按需加载**；**「按需」= 每个用户任务都要按需，不是整段对话只读一次**。

| 触发                                                                                               | 动作                                                                                                                                                                      |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **新的用户任务 / 同对话内换话题**（新需求、新账户、新媒体、新报告类型；例：刚查余额 → 改问建系列） | 按 `SKILL.md` 路由表 **重新 Read** 该任务的「必读文档」与工作流卡片后再执行 CLI；**禁止**沿用上一任务的参数记忆——对话会被压缩，「读过」≠ 当前上下文仍含正确字段名与 flags |
| **工作流编号不同**（P1→P3、P4→P5）                                                                 | 即使刚做过 P1，仍须 Read 新卡片及其必读文档                                                                                                                               |
| **专用 report-templates**（OKKI / 询盘分析 / 周期报告纲要）                                        | Read `references/report-templates/<名>.md` **全文**（与 `report-templates/<名>.md` 同源）；勿只凭 SKILL 摘要                                                              |
| **上下文被压缩 / 记不清字段或命令**                                                                | 重读 `SKILL.md` 路由表 + 当次任务 references                                                                                                                              |
| **CLI 返回 400 / 字段对不上**                                                                      | 回到对应 reference 核对参数名与口径，勿猜                                                                                                                                 |
| **JSON 契约模板**（建搜索系列、PMax 等）                                                           | **必须先 Read** `assets/*-template.json`（结构真相源），再 Read 同目录 `.md`（字段说明与踩坑）；**禁止**只读 `.md` 凭印象拼 JSON |

所有 ID、金额、命令 flags 以**当次 Read 的文档 + 当次 CLI 输出**为准；数值只来自本次 stdout 或脚本读盘结果，不引用对话记忆里的示例值。

### Skill 内 Read 路径约定

| 类型 | 正确路径（相对 Skill 根目录） | 说明 |
| ---- | ----------------------------- | ---- |
| 命令 reference | `references/<域>/<文件>.md` | 如 `references/analytics/account-analytics.md` |
| 报告纲要 | `references/report-templates/<文件>.md` | 如 `references/report-templates/google-period-report.md` |
| JSON 契约模板（结构） | `assets/*-template.json`、`assets/*.schema.json` 等 | **先 Read**；如 `assets/campaign-create-template.json` |
| 契约说明 / 规则 | `assets/<文件>.md` | 与上表 JSON **成对** Read；如 `assets/campaign-create-template.md` |
| HTML 终稿模板 | `report-templates/*.html` | 由 CLI `render` 使用，Agent 通常只 Read 对应 `.md` 纲要 |

路由表若写 `analytics/…` 或 `report-templates/…` 而无 `references/` 前缀，**Read 时仍须加上 `references/`**（`assets/`、`report-templates/*.html` 除外）。

---

## 二、执行流程

**计划 → 确认 → 执行 → 验证 → 推测下一步**：

1. 按上表 Read 当次任务 references → 用 `-h` 确认命令 → 向用户输出操作计划。
2. 涉及写入/修改/删除的操作必须与用户确认；多数破坏性操作还需 `--commit`。
3. 按计划执行，说明每步意图。
4. 用成对的读命令复核写入结果；异步任务每 5s 轮询直到完成。
5. 报告/Excel/含金额话术交付前，按本文件 **§七 交付前自检** 审阅最终产物。
6. 全部完成后预测用户下一步操作。

### 执行模式速查

| 模式              | 说明                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| **数据交付类**    | `google-analysis` / `stats` / `ad campaigns` 等带 `--json-out`：必须按 §三 协议脚本读盘转换      |
| **客户/产品背景** | 拓词、方案、报告背景段：先 `rag list` + `rag query`，再衔接 `keyword` / `ad` / `google-analysis` |
| **仅调接口**      | 优化记录、线索表单、预警、财务命令：无需输出转换                                                 |

### Subagent（可选）

宿主支持 Task / 子会话时：**P5 / P6 / P7** 或预计 CLI 日志很长 → Read `references/core/subagent-orchestration.md`，按决策矩阵选择主会话或委派。子会话不替代 §一 加载纪律；handoff 只传路径与命令块。写入/修改/删除、`--commit`、对用户确认与最终交付始终留在**主 Agent**。

---

## 三、数据处理协议（最高优先级）

所有业务数据以 CLI `--json-out`（或用户提供的同构 JSON）落盘为唯一真相源。每条 `--json-out` 命令成功后**必须按顺序**处理，不要跳步：

1. **解析 stdout 一行摘要 JSON**：拿到 `outlineFile`、`writtenFiles[0]`、`manifestFile`、`agentHint`。摘要里**没有** `total` / `items` 等业务字段——**禁止**对 stdout 写翻页循环，业务数据只在 `writtenFiles[0]` 落盘文件里；**不要**硬编码 `<section>.json` 文件名。
2. **【outline 门禁·先读完再动手】Read 当次产出的*每一个* `*.outline.txt`**（`*.outline.txt`，通常 <2KB，schema-only）确认字段树后**才可**写脚本。类型字面量是**最后一个不以 `//` 开头的行**（提取写法 `outlineRaw.trimEnd().split('\n').filter(l => !l.startsWith('//')).pop()`，勿用 `lines[lines.length-1]`）。outline 是结构描述，**不是数据**，勿当 JSON `require`、勿贴给用户。
   - **多 section / 多账户必须逐一读全**：`google-analysis` 拉 N 个 `--sections`、`google-analysis-batch` 产出 N 维 × M 账户时，**每个维度至少 Read 一次它自己的 outline**（同结构的多账户文件读其一即可代表该维度）；用**一批并行 Read** 把当次所有维度 outline 一次读完，再开始写脚本。
   - **唯一字段真相源 = 当次 outline**：SKILL.md / playbooks / report-templates / 本文件里出现的字段名都是**说明性示例**，**不是**字段真相源；凡 outline 未确认的字段路径，**禁止**凭模板印象、凭上一任务记忆、凭"通用命名"直接写进脚本。
   - **禁止边写边猜、用空值/全 0 当反馈**：不得"先按猜测写一版脚本跑出来，发现字段空了再回头读 outline 重写"。outline 没读全就开写 = 违规。
3. **编写并执行脚本**（`node -e` / `.mjs` / `python`）`readFileSync` 读 `writtenFiles[0]` 做筛选、聚合、计算，字段路径**逐一对照第 2 步确认的 outline**；**永远不得**用宿主 Read / `cat` / `type` / `Get-Content` 打开落盘业务 `*.json`（常为 MB 级，会撑爆上下文）。
4. **交付物用代码写出**（HTML / Excel / PDF / Markdown 等）；向用户展示的数字须来自**脚本 stdout**，不在对话里手填、改数、心算汇总。**交付前**若某章/表为空或全 0，先怀疑"字段路径猜错（漏读该维度 outline）"，回第 2 步核对，**不要**直接当作"接口无数据"交付。

| 允许 Read 的文件                                                                 | 必须用代码读取的文件                       |
| -------------------------------------------------------------------------------- | ------------------------------------------ |
| `references/**/*.md`、`assets/**/*.md`（Skill 文档）                             | 所有 `--json-out` 落盘业务 `*.json`（常为 MB 级） |
| `assets/*-template.json`、`assets/*.schema.json`、`analytics/geo-continents.json` 等**小体积契约/映射** | manifest 中的路径索引（脚本 `JSON.parse`） |
| 当次 `*.outline.txt`                                                             | 用户提供的同构大 JSON                      |
| stdout 一行摘要、你刚写出的最终产物文件                                          | —                                          |

**字面量纪律**：字段路径以 `outlineFile` + 当次 manifest 为准，禁止跳过 \*.outline.txt 猜字段名。常见踩坑（均因没逐维读 outline）：

| 凭印象写错的            | 当次 outline 的真实字段                        |
| ----------------------- | ---------------------------------------------- |
| `ov.spend`              | `cp.spend`（消耗在 `record.currentPeriod` 下） |
| `g.countryName`         | `g.countryOrRegion`                            |
| `s.searchTerm`          | `s.searchTermText`                             |
| `ctRecord.typesSummary` | 记录本身即 `{ PerformanceMax: {…} }` 结构      |
| `ga.items[]`            | `ga` 的键直接是布尔字段，无 `items` 数组       |
| `keywordText`           | `keyword`                                      |
| `query`                 | `searchTermText`                               |

国家名、ID、金额、词表等**业务值**禁止写成源码字面量；映射表/模板契约运行时加载（`analytics/geo-continents.json`、`campaign-create-template.json`）。允许的字面量：输出目录、Sheet/列标题、技术格式、用户当轮明确给出的配置（建议落盘 `config.json` 再脚本读）。

**报告/Excel 全流程走本 Skill**：按工作流卡片与 `report-templates/*.md` 拉数、落盘、脚本转换；**禁止**加载宿主第三方 xlsx/Excel Skill 代劳（不知 TSO 字段口径与账户核验）。

**中间结果一律落盘**：跨步骤数据不靠对话记忆；Windows 避免管道传 JSON，优先 `--json-out` + `node -e` 读文件。

---

## 四、硬规范

- **账户状态 ≠ 系列状态**：`stats` / `balance` / `list-accounts` 的 `status` 只表示账户是否可用；系列状态必须来自 `ad campaigns`。
- **数据时效性**：涉及「今天/当天/今日消耗」「实时消耗排行」前，必读 `references/analytics/account-analytics.md` 顶部「数据时效性」表。TikTok / Yandex / BingV2 / Kwai 是 `accountsoverview` 同步昨天数据，**不能查今天**。
- **先查账户再操作**：`list-accounts -m [mediaType] -k [mediaCustomerId]`；用户给出的 `mediaCustomerId` 必须 `-k` 核验，无结果则告知用户并停止，**禁止**翻页 grep 自行换 ID（会导致报告错户）；拉数、脚本、报告文件名全链路用同一 ID（以 stdout `accountId` 为准）。
- **不猜测账户 ID**：`entityId` ≠ `mediaCustomerId`，两者均来自 `list-accounts`；**禁止**把 `entityId` 传给 `stats -a` / `balance -a`。
- **媒体类型区分大小写**：`Google`、`TikTok`、`MetaAd`、`BingV2`、`Kwai`。
- **CLI 输出忠实**：数值与 ID 须与本次落盘 JSON / stdout 一致，不编造示例 ID；`data` 为空时只说「当前返回无记录」并附 JSON 路径。
- **破坏性操作必须确认 + `--commit`**：账户解绑/关闭/取消分享、BC/MCC 解绑、删除预警/报告/广告/关键词、发票申请、广告发布等。
- **不确定时读文档**：先读对应 references 或用 `-h`，不要猜参数。
- **跨账号 / 企业管家手机号**：用户消息中出现**中国大陆 11 位手机号**（常见语境：「企业管家」「管家账户」「账号 xxx」）且意图是查**该手机号名下**的账户数据时，**必须先**执行 `siluzan-tso account me --check-phone <手机号> --json-out ./snap-me`。**禁止**在未校验通过前用当前凭据拉他户数据。
  - `matched: true`（或 CLI exit 0）→ 按原工作流继续（如 P3 `accounts-digest` 查 TOP 消耗）。
  - `matched: false`（CLI exit 1）→ **停止拉数**，告知用户并询问是否切换登录，话术示例：
    > 暂时不支持查询其他丝路赞账号下的数据。您指定的是 **{phone}**，当前登录的是 **{currentPhone}**。
    > 如需查询该账号，请使用该手机号重新登录：`send-login-code --phone {phone}` → `login --phone {phone} --code <验证码>`。
    > 需要我帮您切换登录吗？
  - 用户**未指定手机号** → 不校验，按当前凭据正常执行。
  - 当前凭据未返回手机号且用户指定了手机号 → 视同未校验通过，引导重新用手机号登录。
- **Google 新建搜索系列**：流程在 `references/google-ads/google-ads-campaign-plan.md`；填 JSON 前**必须先 Read** `assets/campaign-create-template.json`，再 Read `assets/campaign-create-template.md`。**禁止**只读 `.md` 手写 JSON。
- **「根据官网生成 Google 搜索广告 / 表格格式」**：仍属新建搜索系列 → **W3 + 本文件上条**；用户要的「表格」是 `google-ads-launch-plan-template.md` 对 JSON 的投影，**不是**可跳过 JSON/`campaign-validate` 的独立交付物。**禁止**与 P8 网站诊断、P9 市场分析、W5 仅拓词混用。
- **开户首次响应**：对话内首次进入开户话题时，**必须先**按 `references/accounts/open-account-by-media.md` §「首次响应硬规范」输出**完整必填清单**（未指明媒体则列全平台六表），再收集资料；**禁止**未列清单就执行 `open-account` 或零散追问。
- **Google 开户**：`open-account google-wizard` 仅限真实 TTY；Agent/自动化用非交互 `open-account google ...`，审核进度用 `account-history`。
- **主动更新**：详见 `references/core/setup.md`。

---

## 五、时间范围

涉及「投放数据 / 消耗 / 报告 / 周报 / 月报 / 优化建议」且用户未给明确起止日期时**必须反问**（示例：A) 最近完整自然周 B) 本月 1 号到昨天 C) 自定义 YYYY-MM-DD）。给出范围后，报告首行标注 `统计区间：YYYY-MM-DD ~ YYYY-MM-DD（货币：XXX）`。

**例外**（不反问）：

- `list-accounts` 列全部 / 数个数：一次 `list-accounts -m <媒体> --page-size 999 --json-out <dir>`，脚本读落盘 `total` / `items[]`；**禁止**默认 page-size 20 再翻页（详见 `accounts/accounts.md` § Agent 意图速查）。
- 「昨天」单日 stats：默认 `Asia/Shanghai` 日历日；先 `list-accounts` 再 `stats`。
- `forewarning records`、`invoice list`「本月」、TikTok `clue`「最近一周」：见对应 references。

**默认值白名单**（仅用户明确授权「你决定」时使用）：

| 场景                   | 默认窗口                        |
| ---------------------- | ------------------------------- |
| 日常巡检 / 余额扫描    | `now - 7d` ~ `now - 1d`         |
| 周报                   | 上一个完整自然周（周一 ~ 周日） |
| 月报                   | 上一个完整自然月                |
| Google 关键词/系列分析 | `now - 30d` ~ `now - 1d`        |
| MetaAd 账户分析        | 不得默认，必须问                |

---

## 六、币种与金额

完整字段来源与符号表见 `references/accounts/currency.md`。三条硬规则：

1. **币种只认接口字段** `currencyCode`（首选 `list-accounts` → `items[].ma.currencyCode`）；同媒体可同时有 CNY 与 USD，**禁止**默认 Google=美金。`CNY` → **￥**、`USD` → **$**。
2. **禁止跨币种求和**：多账户按 `currencyCode` 分表或分币种小计。
3. **金额单位统一为「元」**（CLI 出口已换算，`budgetAmountYuan`、`spend` 等直接展示），报告保留 2 位小数。

**品牌名优先级**：(1) 用户明确提供 → (2) `list-accounts.mag.advertiserName` → (3) 网址域名占位 `[待确认品牌名]`。**严禁**把英文域名翻译为虚构中文品牌。

---

## 七、交付前自检（报告 / Excel / 含金额话术）

> 在产物文件已写入磁盘**之后、发给用户之前**执行；不靠外部校验脚本，由 Agent **亲自 Read 最终产物文件**（HTML / Markdown 等；二进制 xlsx 无法 Read 时在对话贴自检表逐条勾选，依据为生成脚本的 stdout 摘要）。审阅阶段只看最终产物 + 已掌握的账户元数据，**不**回头 Read 落盘业务 JSON。

**A · 币种**：首行含 `统计区间：…（货币：CNY|USD）`；全文符号与 `currencyCode` 一致（CNY=￥、USD=$，未混用）；与当次 `list-accounts -k` 结果相同；多账户分币种分表、无跨币种「总计」行。

**B · 结构完整**（对照当次 `report-templates/*.md`）：模板要求的每一章/Sheet 都存在；无整章空白（缺数据章节写 `[ 数据不可用：… ]`，禁止编造数字填坑）；优化建议独立成节、引用当次数字（Meta：4 条建议各 ≥150 字 + 7 维补充；Google 诊断：每模块除表格外有「分析」+「建议」）；Excel 的表头列须能在当次 `*.outline.txt` 找到对应字段、产物内账户 ID = 用户当轮给出的 `mediaCustomerId`。

**C · 数字可信**（抽样，不读大 JSON）：总消耗/CPA 数量级与生成过程中脚本 stdout 打印的汇总一致（若无，补跑一次极小 `node -e` 只打印 totals）；账户 ID、区间与用户需求一致；无「示例账户」「占位 123456」等模板残留；表格行数符合预期（如 P3 每个 `-a` ID 占一行）。

任一项不通过 → 修正产物后**重新 Read 再审**，不得交付、不得手改数字糊弄。通过后，交付消息附简短自检结论：

```text
交付前自检（已通过）：
- 产物：./out/report-xxx.html
- 币种：CNY（来自 list-accounts，与报告首行一致）
- 章节：8/8 默认维度齐全；关键词章 [ 数据不可用：接口超时 ] 已标注
- 区间：2026-04-01 ~ 2026-04-30
```

---

## 八、批量任务硬约束

| 任务                        | 推荐命令                                                                               | 禁止                             |
| --------------------------- | -------------------------------------------------------------------------------------- | -------------------------------- |
| 多账户余额 / 预算不足预警   | `balance-scan -m <媒体> --threshold-days 7`                                            | 逐账户 `balance --accounts ...`  |
| 多账户投放画像              | `accounts-digest -m <媒体> [-a ...] --start --end --json-out`                          | 逐账户 `stats`                   |
| 多账户 × 多维度 Google 数据 | 全量：`google-analysis-batch run`（省略 `-a`）；2~10：`google-analysis -a id1,id2,...` | 外层 for-loop；先 list 再拼 `-a` |
| 多系列诊断                  | `ad campaigns --json-out` + node 读文件过滤                                            | 逐系列 `ad campaign-get`         |

**`google-analysis-batch` 纪律**（详见 `references/analytics/google-analysis-batch.md`）：拉全量时省略 `-a`；中断后**必须** `resume --run-id <id>`，**禁止**重新 `run`；stdout 始终单行 JSON（`kind=siluzan-tso-batch-summary`）；退出码 `0` 全成功 / `2` 部分成功 / `3` 全失败或 Token 失效 / `4` 用法错误；401 → 整批终止，按 `references/core/setup.md` 重登录后 `resume`。

---

## 九、运行时长与进度

预估超 2 分钟的任务先告知预计耗时；超 5 分钟未完成时主动检查并告知用户。长任务中断后用对应 `resume` 入口续跑，**禁止**直接重跑 `run`。

---

## 十、账户 ID 示例

先用位数判断类型，不确定再 `list-accounts -m [mediaType] -k [id]`：

- Google: `454xxx5137` 或 `270-xxx-0720`（去掉 `-`）
- TikTok: `70083497xxx59820033`
- Meta(Facebook): `1716030xxx734076`
- Bing: `138xxx763`
- Yandex: `porg-uthxxxrk`
- Kwai: `act_1716030xxx734076`

---

## 十一、常见 HTTP 状态码

- **400**：参数错误，查看对应 reference 或 `-h`
- **401**：平台方返回则需用户重新授权；**我方凭据失效**则优先 `send-login-code` + `login --phone --code`，见 `references/core/setup.md`
- **500**：服务可能正在部署/升级，建议反馈 Siluzan 相关人员

---

## 十二、风险预警与自动化（主动介绍）

加载本 skill 时须向用户介绍 `references/operations/hosted-automation-user-catalog.md` 中的能力：

- **预算 & ROI 控制**：单日预算熔断、CPA 飙升自动降价、连续空耗自动暂停
- **异常监控与报警**：账户封禁检测、落地页死链强停、素材拒审提醒、花费异动、余额枯竭预警
- **自动优化**：差广告降价/关停、高转化提价扩量、A/B 测试自动决出胜者

---

## 十三、消息平台语法

需 webhook 发送消息时，先阅读对应平台文档：

- 企业微信：https://developer.work.weixin.qq.com/document/path/99110
- 飞书：https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot
- 其他平台默认 markdown 输出
