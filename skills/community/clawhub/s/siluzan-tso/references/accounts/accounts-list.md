# 账户列表与账单

> 流程见 `workflows.md` **W1**；开户见 **W2** + `open-account-by-media.md`。

## Contents

- list-accounts
- account-active-bills
- account-history

## list-accounts — 查询广告账户列表

```bash
siluzan-tso list-accounts [选项]
```

| 选项                    | 说明                                                                               |
| ----------------------- | ---------------------------------------------------------------------------------- | ---------------------- |
| `-m, --media <type>`    | 媒体类型（留空查全部）：`Google \| TikTok \| Yandex \| MetaAd \| BingV2`   |
| `-k, --keyword <text>`  | 统一模糊搜索：账户名称 **或** ID。数字型 ID（含 Google `928-780-1878`）CLI 先去连字符再搜；**查单户必须带 `-k`** |
| `-s, --status <status>` | 账户状态：`normal \| invalid \| all`（默认 all）                                   |
| `-p, --page <n>`        | 页码（默认 1）                                                                     |
| `--page-size <n>`       | 每页数量（交互默认 20；`--json-out` 未指定时 999）                                 |
| `--json-out`            | 输出原始 JSON                                                                      |
| `--unicode`             | 表格使用 Unicode 线框；**默认**为 ASCII `+-                                        | ` 线框（兼容各类终端） |
| `--plain`               | 已默认 ASCII，无需再传；保留兼容旧脚本                                             |
| `--refresh-dp`          | 强制重拉 Datapermission（排查「本页全部 OAuth 失效」类会话异常）                   |

**命令定位**：`list-accounts` 主打**精准查询账号信息**（列表、计数、按名称/ID 找户、`entityId` / `mediaCustomerId` / 币种 / 状态等元数据），**不是余额/消耗汇总工具**。JSON **不含**余额/消耗字段，表格也不显示余额列；**禁止**臆造数值——单户余额用 `balance`、全量余额预警用 `balance-scan`（P2）、多户消耗画像用 `accounts-digest`（P3）、单户消耗用 `stats`（均见 `accounts-balance-stats.md`）。

`--login-customer-id <id>` 只保留 `ma.loginCustomerId` 匹配的账户（Google MCC，`397-889-3117` 与 `3978893117` 相同）。D 组日巡检用 `--login-customer-id 3978893117`。没有这个参数名的写法会失败。同一参数也用于 `balance-scan`、`accounts-digest`、`guard`：先拉全量清单，再按该字段过滤，然后才拉消耗。不传时结果与原来一致。`--json-out` 下列全部时带 `--page-size 999`，否则只过滤本页。

### Agent 意图速查（**必读 · 避免多次试探**）

用户问「有哪些 / 列出全部 / 有多少」某媒体广告账户时，**第一次 CLI 就应带大 `--page-size`**，**禁止**先用默认 20 条再翻页重试：

| 用户意图                      | 推荐命令（一步）                                                        | 脚本读落盘 JSON                                                                                         |
| ----------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| 列出全部某媒体账户            | `list-accounts -m <媒体> --page-size 999 --json-out <dir>`              | `items[]`（`ma.mediaCustomerId`、`ma.mediaCustomerName`、`ma.currencyCode`、`ma.invalidOAuthToken` 等） |
| 哪些账户 OAuth / 授权失效     | 同上（或 `-s invalid`）；表格看「授权状态」列                           | **`ma.invalidOAuthToken === true`**（勿用审核状态 / `mediaAccountState`）                               |
| 有多少个账户                  | 同上                                                                    | **`total`**（无需翻页；`itemCount < total` 时说明 page-size 不够大）                                    |
| 只查某一个户                  | `list-accounts -m <媒体> -k <用户原样ID或名称> --json-out <dir>`         | Google CID 带横杠可原样；**禁止**无 `-k` 拉首页再判定未绑定                                             |
| **Meta 全部账户 + 余额/消耗** | **`accounts-digest -m MetaAd --json-out <dir>`**（一步；内部翻页+分批） | `accounts-digest-metaad.json` → `data.items[]`（含 `balance`、`spend`）                                 |
| Meta 余额续航预警             | `balance-scan -m MetaAd --json-out <dir>`                               | `balance-scan-metaad.json`                                                                              |

> **MetaAd ID 格式**：OAuth 授权户（`list-accounts` 里 `mediaAccountType=FacebookAds`）官方 `mediaCustomerId` 带 `act_`。`balance` / `stats` / `balance-scan` / `accounts-digest` 的 `-a` 传裸数字或 `act_` 均可（CLI 会补前缀）。**禁止**把 70+ 个 ID 拼成一条 `balance -a …`；全量用 `accounts-digest`。

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

| 字段 / JSON 路径                       | 说明                                                                                                                                                                                                                                                  |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ma.entityId`                          | 丝路赞内部 ID，`delink`/`share`/`reauth`、**`account-active-bills`** 等操作使用此 ID（**不是** `mediaCustomerId`）                                                                                                                                    |
| `ma.mediaCustomerId`                   | 媒体侧账户 ID（`stats`/`balance`/`accounts-digest` 的 `-a` 只用此字段）：Google/TikTok/Bing 多为数字；**Yandex 形如 `porg-…`**；Meta 常带 `act_`。**不是** `entityId`                                                                                 |
| `ma.currencyCode`                      | 账户主币种：`CNY` / `USD` 等；**表格有「币种」列**；报告/Excel 须与此一致，见 `references/accounts/currency.md`                                                                                                                                       |
| `ma.mediaCustomerName`                 | 账户名称（表格「账户名称」）                                                                                                                                                                                                                          |
| `ma.mediaAccountState` 等              | 平台开户/审核态（如 Approved / Linked）；**不是** OAuth 是否可用                                                                                                                                                                                      |
| **`ma.invalidOAuthToken`**             | **OAuth 是否失效**：`true`=失效，`false`=正常。**表格必有「授权状态」列**（✅ 正常 / ⚠️ 失效），与此字段一一对应；判失效、筛 `-s invalid`、走 `reauth` 均看它                                                                                         |
| `scopeActivationBypassed`（可选，JSON 顶层，不在 `items` 里） | 只在命中时出现，值为 true：当前企业已跳过按户开通。继续取数或报表，不要调用 `present_activate`，也不要按户判断套餐。表格不加列、不加行。没有这个字段不等于未开通 |
| **`ma.scopeActivatedSources`**（可选） | **仅当本次 `list-accounts` 输出中出现该字段时才可读**：非空且存在未过期条目（看 `expireAt`）= 已激活；空数组或全部过期 = 未激活。出现时 Google 表格才有「套餐激活」列。**若 JSON/表格中无此字段/列：禁止向用户谈套餐是否激活，禁止臆造未激活/已激活** |
| `ma.TTADInfo.status` 等                | 媒体侧投放/审核细态（TikTok 表格「审核状态」等）；**勿**当成 OAuth 授权状态                                                                                                                                                                           |

> **Agent**：用户问「哪些授权失效 / OAuth 状态」时，读盘看 `items[].ma.invalidOAuthToken`，表格看「授权状态」列；**不要**用 `mediaAccountState` 或审核状态列代替。
> 用户问「哪些买了套餐 / 是否激活套餐」，或准备出激活卡时：先看 JSON 顶层 `scopeActivationBypassed`。值为 true 则该公司不用按户开通，继续原来的取数或报表，不要调用 `present_activate`。否则**仅当**输出含 `ma.scopeActivatedSources`（或 Google 表格有「套餐激活」列）才可据此回答；没有有效 CTAIAD 条目才是未开通。字段缺失时不要猜，直接取数；只有接口正文出现「未开通套餐」才出激活卡。单独一个「开通」是开户，不是激活卡。
> **Google 单户**：若输出中能确认套餐**已激活**，可用 `account check-access -a <mediaCustomerId>` 再确认网关侧授权是否可用；若输出无激活字段，仍可直接跑 `check-access`（以返回 `status` 为准），**不要**先编造「未激活」。见 `accounts-permissions.md` § check-access。

---

## account-active-bills — 账户激活充值账单明细

查询指定广告账户在平台上的**激活/充值类账单**。

路径中的 **`entityId`** 必须为 **`list-accounts --json-out`** 返回的 **`entityId`**（UUID），**不能**传 `mediaCustomerId`。

```bash
siluzan-tso account-active-bills -m <媒体> --id <entityId> [--json-out ./snap]
```

| 选项                 | 说明                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------ |
| `-m, --media <type>` | 必填：`Google \| TikTok \| Yandex \| MetaAd \| BingV2`（与路径中媒体段一致） |
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

siluzan-tso account-active-bills -m Google --id <entityId>
siluzan-tso account-active-bills -m Google --id <entityId> --json-out ./snap
```

> \*\*勿在文档或聊天中粘贴真实 JWT。

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
| `Approved` | 审核通过 | 运行 `list-accounts -m <媒体>` 确认账户已出现；引导用户充值激活（`config show` 取 `webUrl`，按 `finance.md` 打开对应媒体充值页；例如 Google 为 `https://www.siluzan.com/v3/foreign_trade/tso/recharge/pay?mediaType=Google`；Yandex 当前没有对应充值界面） |
| `Rejected` | 被拒     | 查看 `--json-out` 落盘中的 `reason` 字段了解拒绝原因；修改资料后重新提交；若原因不明，引导用户联系丝路赞客服                                                                                                                                         |

---
