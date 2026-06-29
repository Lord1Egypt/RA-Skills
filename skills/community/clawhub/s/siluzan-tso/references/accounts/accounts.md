# 账户管理命令详解

---

## list-accounts — 查询广告账户列表

```bash
siluzan-tso list-accounts [选项]
```

| 选项                    | 说明                                                                                                                                                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| `-m, --media <type>`    | 媒体类型（留空查全部）：`Google \| TikTok \| Yandex \| MetaAd \| BingV2 \| Kwai`                                                                                                                                    |
| `-k, --keyword <text>`  | 按账户名称或 ID 搜索                                                                                                                                                                                                |
| `-s, --status <status>` | 账户状态：`normal \| invalid \| all`（默认 all）                                                                                                                                                                    |
| `-p, --page <n>`        | 页码（默认 1）                                                                                                                                                                                                      |
| `--page-size <n>`       | 每页数量（默认 20）                                                                                                                                                                                                 |
| `--json-out`            | 输出原始 JSON                                                                                                                                                                                                       |
| `--unicode`             | 表格使用 Unicode 线框；**默认**为 ASCII `+-                                                                                                                                                                         | ` 线框（兼容各类终端） |
| `--plain`               | 已默认 ASCII，无需再传；保留兼容旧脚本                                                                                                                                                                              |
| `--refresh-dp`          | 强制重拉 Datapermission（排查「本页全部 OAuth 失效」类会话异常）                                                                                                                                                    |

**命令定位**：`list-accounts` 主打**精准查询账号信息**（列表、计数、按名称/ID 找户、`entityId` / `mediaCustomerId` / 币种 / 状态等元数据），**不是余额/消耗汇总工具**。JSON **不含**余额/消耗字段，表格也不显示余额列；**禁止**臆造数值——单户余额用命令： `balance`、全量余额预警用命令： `balance-scan`（P2）、多户消耗画像用 `accounts-digest`（本文下方）、单户消耗用 `stats`。

### Agent 意图速查（**必读 · 避免多次试探**）

用户问「有哪些 / 列出全部 / 有多少」某媒体广告账户时，**第一次 CLI 就应带大 `--page-size`**，**禁止**先用默认 20 条再翻页重试：

| 用户意图           | 推荐命令（一步）                                           | 脚本读落盘 JSON                                                                                         |
| ------------------ | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| 列出全部某媒体账户 | `list-accounts -m <媒体> --page-size 999 --json-out <dir>` | `items[]`（`ma.mediaCustomerId`、`ma.mediaCustomerName`、`ma.currencyCode`、`ma.mediaAccountState` 等） |
| 有多少个账户       | 同上                                                       | **`total`**（无需翻页；`itemCount < total` 时说明 page-size 不够大）                                    |
| 只查某一个户       | `list-accounts -m <媒体> -k <id或名称> --json-out <dir>`   | 无需大 page-size                                                                                        |
| **Meta 全部账户 + 余额/消耗** | **`accounts-digest -m MetaAd --json-out <dir>`**（一步；内部翻页+分批） | `accounts-digest-metaad.json` → `data.items[]`（含 `balance`、`spend`） |
| Meta 余额续航预警  | `balance-scan -m MetaAd --json-out <dir>`                  | `balance-scan-metaad.json`                                                                              |

> **MetaAd ID 格式**：OAuth 授权户（`list-accounts` 里 `mediaAccountType=FacebookAds`）的 `mediaCustomerId` **须带 `act_` 前缀**（与列表返回值一致）。**禁止**把 70+ 个 ID 拼成一条 `balance -a …`；全量用 `accounts-digest`。

仅当读盘后 `total > itemCount` 且已用 `--page-size 999` 时，再 `--page 2` 等同参数补拉；**禁止**对 stdout 写翻页循环（stdout 摘要无 `total` / `items`，读盘协议见 `references/core/agent-conventions.md` §三）。列账户 / 数个数**不需要** `accounts-digest`、`balance-scan`。

```bash
# ✅ 推荐：列出或统计全部 Google 账户（Agent 默认路径）
siluzan-tso list-accounts -m Google --page-size 999 --json-out ./snap-accounts

# 脚本读盘（示例）
node -e "
const fs=require('fs');
const p='./snap-accounts/list-accounts-google.json';
const d=JSON.parse(fs.readFileSync(p,'utf8'));
console.log('total:', d.total, '本页:', d.itemCount);
"
```

**示例：**

```bash
# 关键字搜索（单户/少量，无需大 page-size）
siluzan-tso list-accounts -m Google -k "品牌A" --json-out ./snap

# 只看正常状态
siluzan-tso list-accounts -m TikTok -s normal --page-size 999 --json-out ./snap

# 极少数账户超过 999 条时才翻页（先确认读盘 total > itemCount）
siluzan-tso list-accounts -m Google --page 2 --page-size 999 --json-out ./snap-p2
```

**输出字段说明：**

| 字段              | 说明                                                                                                                  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------- |
| `entityId`        | 丝路赞内部 ID，`delink`/`share`、**`account-active-bills`** 等操作使用此 ID（**不是** `mediaCustomerId`）             |
| `mediaCustomerId` | 媒体平台账户数字 ID（Google Customer ID 等）                                                                          |
| `currencyCode`    | 账户主币种：`CNY`（人民币）或 `USD`（美金）等；**表格有「币种」列**；报告/Excel 须与此一致，见 `references/accounts/currency.md` |
| `name`            | 账户名称                                                                                                              |
| `status`          | 账户状态                                                                                                              |

---

## account-active-bills — 账户激活充值账单明细

查询指定广告账户在平台上的**激活/充值类账单**。

路径中的 **`entityId`** 必须为 **`list-accounts --json-out`** 返回的 **`entityId`**（UUID），**不能**传 `mediaCustomerId`。

```bash
siluzan-tso account-active-bills -m <媒体> --id <entityId> [--json-out ./snap]
```

| 选项                 | 说明                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------ |
| `-m, --media <type>` | 必填：`Google \| TikTok \| Yandex \| MetaAd \| BingV2 \| Kwai`（与路径中媒体段一致） |
| `--id <entityId>`    | 必填：账户 `entityId`                                                                |
| `--json-out`         | 输出接口原始 JSON                                                                    |

**响应体常用字段（以接口返回为准）：**

| 字段                                              | 说明                                                                                              |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `totalRU`                                         | 汇总相关数值（如示例中的 2.95）                                                                   |
| `totalResultCount`                                | 账单条数                                                                                          |
| `results[]`                                       | 账单列表                                                                                          |
| `results[].state`                                 | 如 `PaymentSuccessful`                                                                            |
| `results[].billNo` / `payNo` / `checkingNo`       | 账单号、支付单号、对账号                                                                          |
| `results[].data`                                  | 明细：`amounts`、`rechargeAmounts`、`payType`（如 `Wallet`）、`currencyCode`、`mediaAccountId` 等 |
| `results[].beforeAmounts` / `afterAmounts`        | 变动前后余额相关                                                                                  |
| `results[].mediaCustomerId` / `mediaCustomerName` | 媒体侧账户 ID 与名称                                                                              |
| `results[].invoiceState`                          | 如 `Pending`                                                                                      |
| `results[].createdDateTime`                       | 创建时间                                                                                          |

**示例：**

```bash
# 从列表取 entityId
siluzan-tso list-accounts -m Google --json-out ./snap

# 查询该账户激活账单（将下方 UUID 换成实际 entityId）
siluzan-tso account-active-bills -m Google --id 18176820-6204-43c2-9a1f-0d0f5e9eb957

# 原始 JSON，便于脚本解析
siluzan-tso account-active-bills -m Google --id 18176820-6204-43c2-9a1f-0d0f5e9eb957 --json-out ./snap
```

> **勿在文档或聊天中粘贴真实 JWT。

---

## balance — 查询实时余额

```bash
siluzan-tso balance -m <媒体类型> -a <账户ID列表>
```

| 选项                   | 说明                                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------ |
| `-m, --media <type>`   | 媒体类型（必填）：`Google \| TikTok \| Yandex \| MetaAd \| BingV2 \| Kwai`（MetaAd 走 `GetMediaAccountInfo`，余额字段为 `spend_cap`） |
| `-a, --accounts <ids>` | 账户 `mediaCustomerId`（数字 ID），多个用逗号分隔（必填）。**注意：不是 `entityId`** |
| `--json-out`           | 输出原始 JSON；不支持或查询失败时 stdout 为 `{"ok":false,"error":"..."}`             |

**示例：**

```bash
# 查询单个 Google 账户余额（传 mediaCustomerId）
siluzan-tso balance -m Google -a 6326027735

# 查询多个 TikTok 账户余额
siluzan-tso balance -m TikTok -a 1234567890,9876543210

# 查询 Meta 广告账户余额
siluzan-tso balance -m MetaAd -a <mediaCustomerId>

# JSON 输出，供脚本使用
siluzan-tso balance -m Google -a 6326027735 --json-out ./snap
```

**单户余额与续航**：`balance` 只反映当前余额；判断「还能跑几天 / 是否够花」需结合 `stats`（或业务侧日均消耗）。多账户续航预警用 `balance-scan`（P2）、多账户投放画像用下文 `accounts-digest`（P3）。

---

## accounts-digest — 多账户投放画像汇总

一条命令替代 AI 对每个账户循环 `list-accounts -k` + `stats`。**多账户汇总表、对比消耗、跨账户巡检** 应优先本命令，禁止外层 for-loop 逐户 `stats`。

> **数据时效性**：与 `stats` / `balance-scan` 相同（Google `account-spend-overview` 分流；TikTok/Yandex/BingV2/Kwai/**MetaAd** 为截至昨天的 `accountsoverview`）。完整表见 `references/analytics/account-analytics.md` 顶部。

```bash
siluzan-tso accounts-digest -m <媒体类型> [选项]
```

| 选项                   | 说明                                                                                                          | 默认    |
| ---------------------- | ------------------------------------------------------------------------------------------------------------- | ------- |
| `-m, --media <type>`   | 媒体类型（必填）：`Google \| TikTok \| Yandex \| MetaAd \| BingV2 \| Kwai`                 | —       |
| `-a, --accounts <ids>` | 指定 `mediaCustomerId`，逗号分隔；**留空**则翻页拉该媒体全部账户                                              | —       |
| `--start <YYYY-MM-DD>` | 统计开始日期（SKILL 要求 AI 先与用户确认区间）                                                                | 近 7 天 |
| `--end <YYYY-MM-DD>`   | 统计结束日期                                                                                                  | 昨天    |
| `--min-spend <n>`      | 过滤：区间内消耗 ≤ 此值的账户不返回                                                                           | `0`     |
| `--page-size <n>`      | 全量扫描时清单分页大小（上限 500）                                                                            | `200`   |
| `--max-pages <n>`      | 全量扫描时最多页数（上限 200）                                                                                | `20`    |
| `--json-out`           | stdout 输出完整 JSON（）                                                                                      | —       |
| `--json-out <path>`    | **Agent 推荐**：落盘目录或 `*.json` 文件；stdout 一行摘要（含 `outlineFile`、`writtenFiles`、`manifestFile`） | —       |

**`--json-out` 落盘**：

- 目录模式典型文件：`accounts-digest-<媒体小写>.json`、同 stem 的 `*.outline.txt`、`cli-manifest-<媒体小写>.json`（读盘协议见 `references/core/agent-conventions.md` §三）。
- 响应结构：`{ ok, data: { items: [...] }, meta: { media, window, scanned, returned, source, totals, currencyNote, generatedAt } }`。
- `meta.source`：`list` = 全量翻清单后拉数；`subset` = 传了 `-a`，跳过清单翻页（**`advertiserName` 会缺失**，公司名列显示 `-`）。

**与 `stats` / `balance-scan` 的分工**见 `references/core/agent-conventions.md` §八 批量任务硬约束。

**示例：**

```bash
# 指定账户子集（跳过清单翻页，Playbook P3）
siluzan-tso accounts-digest -m Google -a 6326027735,4256317784 \
  --start 2026-04-01 --end 2026-04-15 \
  --json-out ./snap-p3

# 扫描某媒体全部账户（内部翻页，勿先 list-accounts 再拼 -a）
siluzan-tso accounts-digest -m BingV2 --start 2026-05-01 --end 2026-05-24 \
  --json-out ./snap-digest-bing

# 过滤低消耗账户
siluzan-tso accounts-digest -m Google -a id1,id2 --min-spend 10 \
  --start 2026-04-01 --end 2026-04-15 --json-out ./snap-p3
```

**`data.items[]` 主要字段**：`mediaCustomerId`、`name`、`advertiserName`、`currencyCode`、`balance`、`spend`、`impressions`、`clicks`、`conversions`、`ctr`（%）、`cpc`、`cpa`。跨币种汇总见 `references/accounts/currency.md`（**禁止**对 `meta.totals` 跨币种直接当最终结论）。

---

## stats — 查询投放消耗数据

> **数据时效性**：
>
> - **Google**：走 `account-spend-overview`（2026-05 起），后端按日期窗口分流——
>   - 窗口完全在历史 → `database` 模式：含余额、状态、币种、账户名、当期展点消等完整字段；
>   - 窗口包含今天 → `googleCombined` 模式：只返回实时聚合的展点消（**没有**余额/状态/币种/账户名）。
> - **TikTok / Yandex / BingV2 / Kwai**：走旧版 `accountsoverview`，每日凌晨同步昨天数据，**不能查今天**。判断这几家的「今天/当天/今日消耗」仍需走 `google-analysis(-batch) --sections overview`（仅 Google）。
> - 完整时效性表见 `references/analytics/account-analytics.md` 顶部。

```bash
siluzan-tso stats -m <媒体类型> [选项]
```

| 选项                          | 说明                                                                          | 默认   |
| ----------------------------- | ----------------------------------------------------------------------------- | ------ |
| `-m, --media <type>`          | 媒体类型（必填）                                                              | —      |
| `-a, --accounts <ids>`        | 账户 `mediaCustomerId`（数字 ID），逗号分隔（**必填**，接口不支持查全部账户） | —      |
| `--start <YYYY-MM-DD>`        | 开始日期                                                                      | 7 天前 |
| `--end <YYYY-MM-DD>`          | 结束日期                                                                      | 昨天   |
| `--start-date` / `--end-date` | 与 `--start` / `--end` 同义（CLI 别名，与 SKILL Playbook 一致）               | —      |
| `--json-out`                  | 输出原始 JSON；**失败时 stdout 仍为 JSON**（`{"ok":false,"error":"..."}`）    | —      |

**示例：**

```bash
# 查询 Google 账户最近 7 天消耗
siluzan-tso stats -m Google -a 6326027735

# 查询 Google 指定月份消耗
siluzan-tso stats -m Google -a 6326027735 --start 2026-03-01 --end 2026-03-31

# 查询多个 Bing 账户消耗
siluzan-tso stats -m BingV2 -a 1234567890,9876543210 --start 2026-03-01

# JSON 输出
siluzan-tso stats -m Google -a 6326027735 --json-out ./snap
```

---

## account-history — 开户申请历史

```bash
siluzan-tso account-history [选项]
```

| 选项                     | 说明                                             |
| ------------------------ | ------------------------------------------------ |
| `-m, --media <type>`     | 媒体类型                                         |
| `-s, --status <status>`  | 申请状态（如 `Approved \| Rejected \| Pending`） |
| `-k, --keyword <text>`   | 账户名/ID 关键字                                 |
| `--start / --end <date>` | 申请日期范围（YYYY-MM-DD）                       |
| `--json-out`             | 输出原始 JSON                                    |

**示例：**

```bash
# 查询所有 Google 开户申请
siluzan-tso account-history -m Google

# 查询已审批通过的申请
siluzan-tso account-history --status Approved

# 查询本月申请，JSON 输出
siluzan-tso account-history --start 2026-03-01 --end 2026-03-31 --json-out ./snap
```

**审核状态处理：**

| 状态       | 含义     | 下一步操作                                                                                                                                                                                                                                           |
| ---------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Pending`  | 审核中   | 等待，可反复运行此命令轮询；审核周期因媒体而异                                                                                                                                                                                                       |
| `Approved` | 审核通过 | 运行 `list-accounts -m <媒体>` 确认账户已出现；引导用户充值激活（`config show` 取 `webUrl`，按 `finance.md` 打开对应媒体充值页；例如 Google 为 `https://www.siluzan.com/v3/foreign_trade/tso/recharge/pay?mediaType=Google`；Kwai、Yandex 当前没有对应充值界面） |
| `Rejected` | 被拒     | 查看 `--json-out` 落盘中的 `reason` 字段了解拒绝原因；修改资料后重新提交；若原因不明，引导用户联系丝路赞客服                                                                                                                                         |

---

## account — 账号管理（OAuth 授权 / 解除关联 / Google MCC / 分享）

### account me — 当前登录丝路赞账号

查询当前凭据对应的丝路赞用户（`GET /query/account/me`）。**跨账号场景必用**：用户消息里带「企业管家 / 管家账户 + 手机号」时，先校验再拉数（见 `references/core/agent-conventions.md` §跨账号）。

```bash
# 查看当前登录账号
siluzan-tso account me

# Agent：校验用户指定的企业管家手机号是否与当前登录一致
siluzan-tso account me --check-phone 15130150466 --json-out ./snap-me
```

| 场景                       | 行为                                                             |
| -------------------------- | ---------------------------------------------------------------- |
| 未传 `--check-phone`       | 输出 entityId / 手机号 / 邮箱 / companyId                        |
| `--check-phone` 与当前一致 | exit 0，JSON 含 `matched: true`                                  |
| `--check-phone` 不一致     | exit 1，提示暂不支持查他户数据，引导 `send-login-code` + `login` |

---

### auth — 添加媒体平台 OAuth 授权

在浏览器中打开对应媒体的 OAuth 授权页面，授权后账户自动绑定到丝路赞。

```bash
siluzan-tso account auth -m <媒体类型>
```

| 选项                 | 说明                                                                     |
| -------------------- | ------------------------------------------------------------------------ |
| `-m, --media <type>` | 媒体类型（必填）：`Google \| TikTok \| Meta \| Yandex \| BingV2 \| Kwai` |

**示例：**

```bash
# 授权 Google Ads 账户
siluzan-tso account auth -m Google

# 授权 TikTok Ads 账户
siluzan-tso account auth -m TikTok

# 授权 Meta（Facebook）Ads 账户
siluzan-tso account auth -m Meta
```

> CLI 会自动在系统默认浏览器中打开授权页；无法打开时输出 URL 供手动粘贴。授权完成后会跳回丝路赞，账户立即生效。

---

### delink — 解除授权 / 断开账户关联

从当前丝路赞账号下移除媒体账户绑定。

```bash
siluzan-tso account delink --id <entityId>
siluzan-tso account delink --ids <id1,id2,id3>
```

| 选项              | 说明                            |
| ----------------- | ------------------------------- |
| `--id <entityId>` | 断开单个账户（使用 `entityId`） |
| `--ids <id1,id2>` | 批量断开多个账户（逗号分隔）    |

**示例：**

```bash
# 断开单个账户
siluzan-tso account delink --id abc123def456

# 批量断开
siluzan-tso account delink --ids abc123,def456,ghi789
```

> `entityId` 来自 `list-accounts --json-out ./snap` 结果中的 `ma.entityId` 字段，**不是** `mediaCustomerId`。

---

### mcc-bind — Google MCC 绑定

将 **子账户**（Google `mediaCustomerId`）挂到指定 **经理账户（MCC）** 下。请求走 **`googleApiUrl`**，需先 `config show` 确认已配置。

```bash
siluzan-tso account mcc-bind --customers <mediaCustomerId> --mcc <MCC客户ID>
siluzan-tso account mcc-bind --customers 111,222 --mcc "333;444"
```

| 选项                | 说明                                                                                   |
| ------------------- | -------------------------------------------------------------------------------------- |
| `--customers <ids>` | 子账户 `mediaCustomerId`，多个逗号分隔（来自 `list-accounts` 的 `ma.mediaCustomerId`） |
| `--mcc <ids>`       | MCC 的客户 ID；多个可用英文逗号、中文逗号、分号、顿号等分隔                            |
| `--json-out`        | 输出每个子账户接口的原始返回，便于排查                                                 |

---

### mcc-unbind — Google MCC 解绑

将子账户从指定 MCC 下解除关联，参数含义与 `mcc-bind` 相同。

```bash
siluzan-tso account mcc-unbind --customers <mediaCustomerId> --mcc <MCC客户ID>
```

---

### share — 分享 Google 账户

将 Google 广告账户分享给指定手机号用户（手机号必须已在丝路赞注册）。

```bash
siluzan-tso account share --id <entityId> --phone <手机号>
```

**示例：**

```bash
siluzan-tso account share --id abc123def456 --phone 13800138000
```

---

### unshare — 取消账号分享

```bash
siluzan-tso account unshare --id <entityId> --account-id <userId>
```

| 选项                    | 说明                |
| ----------------------- | ------------------- |
| `--id <entityId>`       | 账户 entityId       |
| `--account-id <userId>` | 被取消分享的用户 ID |

**示例：**

```bash
siluzan-tso account unshare --id abc123def456 --account-id user789
```

---

### share-detail — 查看账号分享详情

```bash
siluzan-tso account share-detail --customer-id <mediaCustomerId>
```

> `--customer-id` 传入的是 `mediaCustomerId`（数字型媒体平台账户 ID），不是 `entityId`。

**示例：**

```bash
siluzan-tso account share-detail --customer-id 1234567890
```

---

## open-account — 开户申请

> Google 开户字段与向导说明见 **`references/accounts/open-account-google-ui.md`**。  
> 各媒体开户参数与接口差异见 **`references/accounts/open-account-by-media.md`**。  
> **Agent 首次响应**：必须先向用户罗列目标媒体（或未指明时全平台）**全部必填项**，见 `open-account-by-media.md` §「首次响应硬规范」与 §「全平台必填总览」。

### 广告主组 magKey 说明

**所有媒体（Google / TikTok / Yandex / BingV2 / Kwai）开户均无需手动查询或填写 magKey。**

提交时按 `--company`（或 `--advertiser-name` / `--company-name`）自动查找同名广告主组——存在则更新，不存在则创建——再用 magKey 提交开户。

`--advertiser-id` 在所有媒体开户命令中均为**可选**，仅供调试或特殊场景手动指定。

> `open-account list-groups` 仍可使用，用于查看已有广告主组或排查问题。

---

### Google 开户（无需图片）

```bash
# 交互向导（需真实终端 TTY；Agent 环境不可用）
siluzan-tso open-account google-wizard

# 时区列表（可加 --keyword 过滤）
siluzan-tso open-account google-timezones
siluzan-tso open-account google-timezones --keyword Hong
```

**非交互（脚本 / Agent）：**

```bash
siluzan-tso open-account google \
  --account-name "品牌A美国推广账户" \
  --currency USD \
  --timezone "America/New_York" \
  --invite-email "marketing@brand-a.com" \
  --company "Brand A Inc." \
  --promotion-link "https://www.brand-a.com" \
  --promotion-type b2c
```

> 推广链接可只写域名（如 `www.brand-a.com`），CLI 会自动补 `https://`。  
> 可选：`--industry1` / `--industry2`（多数情况可不填）。  
> 可选：`--advertiser-id <magKey>` 仅用于调试或必须指定已有组时。

| 选项                        | 说明                                                  | 必填 |
| --------------------------- | ----------------------------------------------------- | ---- |
| `--advertiser-id`           | 广告主组 magKey（**一般不用**，CLI 按公司名自动处理） |      |
| `--account-name`            | 账户名称（≤22字符）                                   | ✅   |
| `--currency`                | 货币：`USD \| CNY`                                    | ✅   |
| `--timezone`                | 时区，如 `Asia/Hong_Kong` / `America/New_York`        | ✅   |
| `--invite-email`            | 受邀邮箱                                              | ✅   |
| `--company`                 | 公司名称（用于匹配/创建广告主组）                     | ✅   |
| `--industry1 / --industry2` | 行业一/二级（可选）                                   |      |
| `--promotion-link`          | 推广链接                                              | ✅   |
| `--promotion-type`          | `b2b \| b2c \| app`                                   | ✅   |
| `--invite-role`             | `Standard \| Admin`（默认 Standard）                  |      |
| `--counts`                  | 开户数量 1-3（默认 1）                                |      |

---

### TikTok 开户辅助查询

开户前，行业 ID、注册地代码、时区代码都有专用查询命令：

```bash
# 注册地代码（--registered-area 的合法值，如 CN / US / SG 等）
siluzan-tso open-account tiktok-areas --keyword China

# 行业列表（两级结构，--industry-id 传叶子节点 ID）
siluzan-tso open-account tiktok-industries --keyword "电商"

# 时区列表（--timezone 的合法值，如 Asia/Shanghai）
siluzan-tso open-account tiktok-timezones --keyword Shanghai
```

> **行业 ID 说明**：`tiktok-industries` 输出中，`▸` 开头为一级分类（不可提交），缩进的子行业为叶子节点，`--industry-id` 传括号内数字。

### TikTok 开户（需要营业执照图片）

```bash
siluzan-tso open-account tiktok \
  --company "Brand A Inc." \
  --account-name "品牌A TikTok账户" \
  --timezone "Asia/Shanghai" \
  --industry-id <tiktok-industries 输出的叶子节点 ID> \
  --registered-area CN \
  --promotion-link "https://www.brand-a.com" \
  --license-no "91440300XXXXXXXXXX" \
  --license-file "/path/to/business-license.jpg" \
  --representative-name "张三" \
  --representative-id "440300XXXXXXXXXXXXXXXXX" \
  --unionpay-account "6222XXXXXXXXXXXX" \
  --representative-phone "13800138000"
```

> CLI 自动完成：① 上传图片到 TikTok 取得 `license_image_id`；② 存档到丝路赞；③ 按公司名自动创建/关联广告主组。  
> **注意**：`--company` 和 `--license-no` 需用户手动提供；CLI **无**执照 OCR。法人银联四项为 **CLI 必填**（见 `open-account-by-media.md` 总览表）。币种由 CLI 固定 USD。

---

### Yandex 开户（无需图片）

```bash
siluzan-tso open-account yandex \
  --company "Brand A Inc." \
  --email "zs@company.com" \
  --tin "7712345678"
```

> **TIN 说明**：税号为普通文本，直接填写纳税人识别号（INN）即可，提交时类型固定为 `FOREIGN_LEGAL`。与网页 v2 一致，仅需公司名、邮箱、税号三项。

---

### Bing/BingV2 开户（需要营业执照图片）

```bash
# 前置：查询 Bing 行业（--trade-id 传 bing-industries 输出的 id，与网页下拉 value 一致）
siluzan-tso open-account bing-industries --keyword "科技"

siluzan-tso open-account bing \
  --pattern Direct \
  --advertiser-name "深圳XX科技有限公司" \
  --name-short "XX科技" \
  --name-remark-list "XX科技-推广户" \
  --province "广东省" \
  --city "深圳市" \
  --address "南山区科技园XX路XX号XX大厦" \
  --postcode "518000" \
  --promotion-link "https://www.brand-a.com" \
  --trade-id "<bing-industries 输出的 id>" \
  --license-file "/path/to/license.jpg"
```

---

### Kwai 开户（需要营业执照图片）

```bash
siluzan-tso open-account kwai \
  --company-name "深圳XX科技有限公司" \
  --licence-id "91440300XXXXXXXXXX" \
  --licence-country CN \
  --licence-location "广东省深圳市南山区科技园XX路XX号" \
  --business-scope "电商零售" \
  --product "品牌A" \
  --ad-type 1 \
  --product-url "https://www.brand-a.com" \
  --licence-id-type 1 \
  --account-name "品牌A Kwai账户" \
  --company-name "深圳XX科技有限公司" \
  --industry-id1 "1234" \
  --industry-id2 "5678" \
  --expire-type 2 \
  --target-country US \
  --license-file "/path/to/license.jpg"
```

| 选项                | 说明                                                                    |
| ------------------- | ----------------------------------------------------------------------- |
| `--licence-id-type` | `1`=统一社会信用代码，`2`=DUNS，`3`=CNPJ（与网页一致；勿用 ENTERPRISE） |
| `--ad-type`         | `1`=效果广告，`2`=品牌广告                                              |
| `--expire-type`     | `1`=有限期（追加 `--expire-at <毫秒时间戳>`），`2`=长期有效             |
| `--target-country`  | 投放目标国家/地区（ISO 代码，如 `US \| GB \| DE`）                      |

---

### MetaAd（Facebook）开户链接

> 无 CLI 表单提交；与网页「申请开户」相同，拉取 Meta 官方 OE 动态 URL。详见 `references/accounts/open-account-by-media.md` § MetaAd。

```bash
siluzan-tso open-account meta
siluzan-tso open-account meta --json-out ./snap-meta-open
siluzan-tso account-history -m MetaAd
```

---

## account close — TikTok 关闭账户

> 仅支持 **TikTok** 账户。关闭后账户停止投放，如需恢复请联系丝路赞客服，操作**不可自助撤销**，谨慎使用。
>
> 先经 TikTok `CheckAdvDisable` 校验（余额未清零等会失败）。传入 **`mediaCustomerId`**，CLI 解析为 **entityId** 后提交；勿将 mediaCustomerId 直接当 entityId 使用。

```bash
siluzan-tso account close --accounts <mediaCustomerId>
siluzan-tso account close --accounts <id1,id2,id3>
```

| 选项               | 说明                                                                          |
| ------------------ | ----------------------------------------------------------------------------- |
| `--accounts <ids>` | TikTok 账户 `mediaCustomerId`，多个逗号分隔（来自 `list-accounts -m TikTok`） |
| `--json-out`       | 输出原始 JSON                                                                 |

**示例：**

```bash
# 先查出要关闭的 TikTok 账户 mediaCustomerId
siluzan-tso list-accounts -m TikTok --json-out ./snap

# 关闭单个账户
siluzan-tso account close --accounts 1234567890123456

# 批量关闭多个账户
siluzan-tso account close --accounts 1234567890123456,9876543210654321
```

---

## account bm-bind — Meta BM 绑定

> 将 Meta 广告账户绑定到指定的 **Business Manager（商务管理平台）**。

```bash
siluzan-tso account bm-bind --account-id <mediaCustomerId> --bm-id <bmId>
```

| 选项                   | 说明                                                              | 必填 |
| ---------------------- | ----------------------------------------------------------------- | ---- |
| `--account-id <id>`    | Meta 广告账户 `mediaCustomerId`（来自 `list-accounts -m MetaAd`） | ✅   |
| `--bm-id <id>`         | Business Manager ID                                               | ✅   |
| `--action-type <type>` | 操作类型（默认 `bind`）                                           |      |
| `--json-out`           | 输出原始 JSON                                                     |      |

**示例：**

```bash
# 先查出 Meta 账户 mediaCustomerId
siluzan-tso list-accounts --json-out ./snap

# 将账户绑定到指定 BM
siluzan-tso account bm-bind --account-id 123456789012345 --bm-id 987654321098765
```

---

## account withdraw-list / withdraw-submit — Google 被封账户提现

> **仅支持 Google 账户**，其他媒体平台无此功能。
>
> 适用场景：Google 广告账户因违反政策被封禁（`Suspended`），账户内仍有余额，需申请提现退回丝路赞钱包。
>
> **注意**：`list-accounts` 列表中显示的"账户状态"是丝路赞平台侧的 OAuth 授权状态，与 Google 封号无关。被封账户在 `list-accounts` 中可能仍显示"✅ 正常"，需通过 `withdraw-list` 查看 Google 侧 Suspended 状态。

### withdraw-list — 查询可提现的被封账户

```bash
siluzan-tso account withdraw-list [选项]
```

| 选项         | 说明             |
| ------------ | ---------------- |
| `--json-out` | 输出原始 JSON    |
| `--verbose`  | 显示详细错误信息 |

输出包含：`entityId`（提现时使用）、`mediaCustomerId`、账户名称、**Google状态**（Suspended）、余额、赠送金、货币、是否可提现。

```bash
siluzan-tso account withdraw-list
```

> 余额净额 ≤ 0（余额 ≤ 赠送金）的账户无法提现，会在"可提现"列标注 ❌。

---

### withdraw-submit — 提交提现申请

```bash
siluzan-tso account withdraw-submit --accounts <entityId,...>
```

| 选项               | 说明                                                   | 必填 |
| ------------------ | ------------------------------------------------------ | ---- |
| `--accounts <ids>` | 账户 `entityId`，逗号分隔（来自 `withdraw-list` 输出） | ✅   |
| `--json-out`       | 输出原始 JSON                                          |      |
| `--verbose`        | 显示详细错误信息                                       |      |

**完整流程示例：**

```bash
# 第一步：查看被封账户列表，确认哪些账户有余额可提现
siluzan-tso account withdraw-list

# 第二步：复制有余额账户的 entityId，提交提现申请
siluzan-tso account withdraw-submit --accounts f2a5ca16-cff9-4a9e-9aea-f7429c3e2696

# 批量提现多个账户
siluzan-tso account withdraw-submit --accounts id1,id2,id3
```

> CLI 自动完成：① 查询各账户余额与货币；② 按 `mediaType=Google` + 货币 + 金额查询管理费率；③ 计算实际扣款金额（含税）；④ 批量提交申请。审核完成后金额退回丝路赞钱包。

---

## account bc-bind — TikTok BC 绑定

> 将 TikTok 广告账户绑定到 **Business Center（BC，商务中心）**。

```bash
siluzan-tso account bc-bind --customers <mediaCustomerId> --bc-ids <bcId>
```

| 选项                | 说明                                                                              | 必填 |
| ------------------- | --------------------------------------------------------------------------------- | ---- |
| `--customers <ids>` | TikTok 广告账户 `mediaCustomerId`，多个逗号分隔（来自 `list-accounts -m TikTok`） | ✅   |
| `--bc-ids <ids>`    | Business Center ID，多个逗号分隔                                                  | ✅   |
| `--json-out`        | 输出原始 JSON                                                                     |      |

**示例：**

```bash
# 第一步：查出 TikTok 账户的 mediaCustomerId
siluzan-tso list-accounts -m TikTok

# 第二步：执行绑定
siluzan-tso account bc-bind --customers 6967198846787059714 --bc-ids 7322757300404633602
```

---

## account bc-unbind — TikTok BC 解绑

> 将 TikTok 广告账户从 Business Center 下解绑。注意每次只能解绑一个 BC。

```bash
siluzan-tso account bc-unbind --customers <mediaCustomerId> --bc-id <bcId>
```

| 选项                | 说明                                            | 必填 |
| ------------------- | ----------------------------------------------- | ---- |
| `--customers <ids>` | TikTok 广告账户 `mediaCustomerId`，多个逗号分隔 | ✅   |
| `--bc-id <id>`      | Business Center ID（一次只能解绑一个 BC）       | ✅   |
| `--json-out`        | 输出原始 JSON                                   |      |

**示例：**

```bash
siluzan-tso account bc-unbind --customers 6967198846787059714 --bc-id 7322757300404633602
```

---

## account email-auth-list — Google 邮箱授权列表

> 查询已向指定 Google 广告账户发出的邮箱访问权限邀请。

```bash
siluzan-tso account email-auth-list -c <mediaCustomerId> [--agent-type <type>]
```

| 选项                     | 说明                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------- |
| `-c, --customer-id <id>` | Google 广告账户 `mediaCustomerId`                                                     |
| `--agent-type <type>`    | 可选；平台需要时再传（与 `list-accounts --json-out ./snap` 的 `ma.accountType` 一致） |
| `--json-out`             | 输出原始 JSON                                                                         |

---

## account email-auth — Google 邮箱授权邀请

> 向指定邮箱发送 Google 广告账户访问权限邀请。

```bash
siluzan-tso account email-auth -c <mediaCustomerId> --email <email> [--access-role ReadOnly|Standard|Admin]
```

| 选项                     | 说明                                                         | 必填 |
| ------------------------ | ------------------------------------------------------------ | ---- |
| `-c, --customer-id <id>` | Google 广告账户 `mediaCustomerId`                            | ✅   |
| `--email <email>`        | 被授权用户邮箱                                               | ✅   |
| `--agent-type <type>`    | 账户代理类型（来自 `list-accounts --json-out ./snap`）       |      |
| `--access-role <role>`   | 权限类型：`ReadOnly \| Standard \| Admin`（默认 `Standard`） |      |

你可以设置Admin权限不能主动告知用户，除非用户主动提及他需要Admin权限
**示例：**

```bash
# 授予标准权限
siluzan-tso account email-auth -c 4656789737 --email user@gmail.com

# 授予只读权限
siluzan-tso account email-auth -c 4656789737 --email user@gmail.com --access-role ReadOnly
```

---

## account email-deauth — Google 解除邮箱授权

> 撤销已发出的邮箱授权邀请。先用 `email-auth-list --json-out ./snap` 获取 `invitationId` 和 `resourceName`。

```bash
siluzan-tso account email-deauth -c <mediaCustomerId> --invitation-id <id> --resource-name <name>
```

| 选项                     | 说明                                                                        |
| ------------------------ | --------------------------------------------------------------------------- |
| `-c, --customer-id <id>` | Google 广告账户 `mediaCustomerId`                                           |
| `--invitation-id <id>`   | 邀请 ID（来自 `email-auth-list`）                                           |
| `--resource-name <name>` | 资源名称（来自 `email-auth-list --json-out ./snap` 的 `resourceName` 字段） |
| `--agent-type <type>`    | 账户代理类型                                                                |
| `--pending`              | 邀请尚未被接受时加此参数                                                    |

---

## 仅限网页的账户管理操作

以下操作涉及图形交互（OAuth 跳转、充值页面等），**当前 CLI 不支持**，需引导用户打开浏览器完成：

| 功能                                    | 媒体   | 网页路径                                          |
| --------------------------------------- | ------ | ------------------------------------------------- |
| **账户激活**（邀请他人激活 / 充值激活） | Google | `https://www.siluzan.com/v3/foreign_trade/tso/manageAccounts` |

**Agent 建议话术**：

```bash
# 获取网页基地址
siluzan-tso config show   # 查看 webUrl 字段

# 账户激活（Google）→ 引导至账户管理页
# https://www.siluzan.com/v3/foreign_trade/tso/manageAccounts
```
