# 账户币种（CNY / USD）— Agent 硬规范

> **WorkBuddy 及所有编排本 Skill 的 Agent**：回答金额、写报告/Excel、对比多账户前，**必须先确定每个账户的 `currencyCode`**，再选符号与汇总方式。**禁止**凭媒体或「Google 账户」默认美金。

---

## 常见误区（必须避免）

| 错误做法                        | 正确做法                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------ |
| Google 账户一律用 `$`           | 同一媒体下既有 **USD** 也有 **CNY**，以接口 `currencyCode` 为准                |
| 多账户消耗直接相加              | 先按 `currencyCode` **分表/分币种小计**，禁止跨币种求和                        |
| 报告只写 `$1,234` 不写币种      | 首行写 `统计区间：…（货币：CNY）` 或 `（货币：USD）`；每笔金额带代码           |
| CNY 用 `$` 或 USD 用 `￥`       | **CNY → ￥**；**USD → $**（见下表）                                            |
| 开户选了 USD 但拉数用人民币话术 | 开户币种见 `open-account … --currency`；拉数币种见 `list-accounts` / `balance` |

---

## 符号与格式

| `currencyCode` | 用户可见符号    | 示例             |
| -------------- | --------------- | ---------------- |
| `CNY`          | **￥**（全角）  | `￥1,234.56 CNY` |
| `USD`          | **$**           | `$1,234.56 USD`  |
| 其他           | 用 ISO 代码前缀 | `EUR 100.00`     |

- 数值保留 **2 位小数**；表格/话术中的金额与 CLI JSON **同源**，不手填。
- 同一段落、同一 Sheet **只使用一种主币种**；多币种必须分块说明。

---

## 从哪里读 `currencyCode`（按优先级）

1. **`list-accounts`**（推荐第一步）：`items[].ma.currencyCode`；表格有 **「币种」** 列。
2. **`balance` / `balance-scan` / `accounts-digest`**：`items[].currencyCode` 或行内已格式化的金额（含代码）。
3. **`stats`**：`items[].currencyCode`（Google 含今天窗口时可能无币种，见 `references/accounts/accounts.md` 时效性说明）。
4. **`google-analysis --sections overview`**：`overview-*.json` 的 `record.currencyCode`（汇总维度，`schemaVersion 3` 起整块在 `record`）。
5. **`ad campaigns` / `ad groups`**：JSON 内 `currencyCode`（与账户主币种一致）。
6. **发票/充值**：`invoice billable` 的 `currencyCode`；人民币订单与美金订单开票类型不同，见 `references/accounts/finance.md`。

**单账户任务**：在 `list-accounts -k <id>` 或 `balance -a <id>` 之后，把解析到的 `currencyCode` 记入报告首行与脚本常量（从 JSON 读取，勿写死 `USD`）。

**多账户任务**：拉 `list-accounts --json-out` 建 `mediaCustomerId → currencyCode` 映射，后续所有金额展示经此映射格式化。

---

## 金额单位约定

- **CLI 出口的大多数 JSON / 表格金额以「元」为单位**：`budget`、`*Yuan` 后缀（`budgetAmountYuan`、`maxCPCAmountYuan` 等）、`spend` / `averageCpc` / `costPerConversion` 等。**`keyword suggest`**：`averageCpc` / `lowTopOfPageBid` / `highTopOfPageBid` 的币种见根级与每条 **`bidAmountCurrency`**（传 `-a` 时为账户 `currencyCode`；无 `-a` 时为 **USD**）。
- **写 CLI 参数**（`--budget`、`--max-cpc`、`--target-cpa`、`--amount` 等）：同样传**主币种元**，与账户 `currencyCode` 一致；CLI 内部按需 ×100 / ×1_000_000 写后端。
- 旧版网关字段（`budgetAmount` 分、`*Micros` 微元、`maxCPCAmountDisplay` 等）**已不再落盘到 CLI 输出**，下游脚本无需做单位换算。

详见 `references/analytics/account-analytics.md`「金额单位」。

---

## 报告 / Excel 检查清单

- [ ] 首行或封面有 `统计区间` + `（货币：CNY|USD）`
- [ ] 每个账户区块的币种与 `list-accounts` 一致
- [ ] 无跨币种合计（或明确标注「不可直接相加」）
- [ ] 全文未出现与 `currencyCode` 矛盾的 `$` / `￥`
- [ ] OKKI 周报、询盘分析等模板中的「币种」列来自 `list-accounts`，非臆造

---

## 相关文档

- 账户命令与字段：`references/accounts/accounts.md`
- 报告金额口径：`references/analytics/account-analytics.md`
- 开户选币：`references/accounts/open-account-google-ui.md`、`references/core/workflows.md`
- 开票币种：`references/accounts/finance.md`
