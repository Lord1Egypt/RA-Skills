# 余额、消耗与多账户汇总

> 流程见 `playbooks.md` **P2** / **P3**；单户读数见 `workflows.md` **W1**。币种口径见 `currency.md`。

## Contents

- balance
- balance-scan（P2）
- accounts-digest（P3）
- stats

## balance-scan — 多账户余额续航扫描

一键扫描某媒体下**全部有效账户**的余额与日均消耗。`data.items` 返回**所有已检查账户**（不只预警行）；用 `hitReason` 标记续航/余额不足。**P2 必用**；**禁止**外层循环逐户 `balance`。

> **数据异常（exit 2）**：无账户 / 全部 OAuth 失效 / **余额全为 null** 时 CLI 退出码 **2**，`--json-out` 的 `ok=false` 且 `meta.dataIssue` 为 `no_accounts` | `all_oauth_invalid` | `all_balances_null`。须向用户说明原因，**禁止**当成「无预警命中」。可试 `--refresh-dp` / `login` / `--verbose`。

```bash
siluzan-tso balance-scan -m <媒体类型> [选项]
```

| 选项                                  | 说明                                                                           | 默认         |
| ------------------------------------- | ------------------------------------------------------------------------------ | ------------ |
| `-m, --media <type>`                  | 必填：`Google \| TikTok \| Yandex \| MetaAd \| BingV2`                 | —            |
| `-a, --accounts <ids>`                | 指定 `mediaCustomerId`（逗号分隔）；**跳过清单翻页**，对这些 ID 拉数后全部输出 | —            |
| `--threshold-days <n>`                | 剩余续航天数阈值                                                               | `7`          |
| `--spend-days <n>`                    | 日均消耗回看自然日数（截至昨天不含今天，**北京时间**；日均 = 窗口合计 / N）    | `7`          |
| `--min-balance <n>`                   | 绝对余额阈值（与 threshold 取并集）                                            | —            |
| `--min-daily-spend <n>`               | 日均消耗低于此值视为僵尸账户，不做续航估算                                     | `0.01`       |
| `--target-days <n>`                   | 建议充值目标续航天数                                                           | `30`         |
| `--page-size <n>` / `--max-pages <n>` | 全量扫描分页（上限 500 / 200）                                                 | `200` / `20` |
| `--json-out`                          | Agent 推荐落盘；**全量扫描必带**，否则超时暂停后无法续跑                       | —            |
| `--time-budget <时长>`                | 单次执行的时间预算（`25m` / `90s`；`off` 不限）。默认按宿主工具超时推断，一般不用传 | 自动         |
| `--fresh`                             | 丢弃 `--json-out` 里的旧断点从头扫。仅用户明确要求重扫时用                     | off          |

> **超时暂停（exit 75）**：账户多时一次执行扫不完，CLI 会在工具超时前停下，stdout 一行 `kind=siluzan-tso-scan-paused`、`state=paused`，含 `progress` 与 `resumeCommand`。原样执行 `resumeCommand`（同一 `--json-out`），重复到不再 paused 才读盘交付。规则见 `references/core/agent-conventions.md` §八。

**示例：**

```bash
# 全量巡检（Playbook P2）
siluzan-tso balance-scan -m Google --threshold-days 7 --json-out ./snap-p2

# 近 3 日日均 + 续航阈值 7 天
siluzan-tso balance-scan -m Google --threshold-days 7 --spend-days 3 --json-out ./snap-p2

# 已知子集
siluzan-tso balance-scan -m BingV2 -a id1,id2,id3 --json-out ./snap-p2-subset

# Meta 余额续航
siluzan-tso balance-scan -m MetaAd --json-out ./snap-p2-meta
```

**读盘要点**：先看 `meta.dataIssue`（非空则失败）。`data.items` = **全部已检查账户**（OAuth 失效户不在 items，见 `meta.skippedInvalidOAuth`）；`meta.hitCount` = 触阈值条数。预警筛 `hitReason !== "none"`；`hitReason="none"` 表示已检查但未触阈值。按 `remainingDays` 升序交付。用 **`dailySpend`** 做日均（口径见 `meta.spendDays` / `meta.spendWindow`），勿把 `stats` 区间合计 `spend` 当「每天消耗」。Google 消耗走 `account-spend-overview`，`startDate`/`endDate` 带东八区墙钟（`…T00:00:00+08:00` / `…T23:59:59+08:00`），与 `stats` 同口径。与 `balance` / `accounts-digest` 分工见 `references/core/agent-conventions.md` §八。向用户写 Markdown 表时 `advertiserName` / `name` 必须把 `|` 换成 `｜`（见 conventions §三）。

---

## balance — 查询实时余额

```bash
siluzan-tso balance -m <媒体类型> -a <账户ID列表>
```

| 选项                   | 说明                                                                                                                                                        |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-m, --media <type>`   | 媒体类型（必填）：`Google \| TikTok \| Yandex \| MetaAd \| BingV2`（MetaAd 走 `GetMediaAccountInfo`，余额字段为 `spend_cap`）                       |
| `-a, --accounts <ids>` | 账户 `mediaCustomerId`（来自 `list-accounts` 的 `ma.mediaCustomerId`），逗号分隔（必填）。**禁止**传 `entityId` / tokenId / 其它 UUID；Yandex 须传 `porg-…` |
| `--json-out`           | 输出原始 JSON；不支持或查询失败时 stdout 为 `{"ok":false,"error":"..."}`                                                                                    |

**示例：**

```bash
# 查询单个 Google 账户余额（传 mediaCustomerId）
siluzan-tso balance -m Google -a 6326027735

# Yandex：传 porg-…（mediaCustomerId），禁止 entityId/UUID
siluzan-tso balance -m Yandex -a porg-kqquuxx6

# 查询多个 TikTok 账户余额
siluzan-tso balance -m TikTok -a 1234567890,9876543210

# 查询 Meta 广告账户余额（OAuth 户传裸数字或 act_ 均可）
siluzan-tso balance -m MetaAd -a <mediaCustomerId>

# JSON 输出，供脚本使用
siluzan-tso balance -m Google -a 6326027735 --json-out ./snap
```

**单户余额与续航**：`balance` 只反映当前余额；判断「还能跑几天 / 是否够花」需结合 `stats`（或业务侧日均消耗）。多账户续航预警用 `balance-scan`（P2）、多账户投放画像用下文 `accounts-digest`（P3）。

---

## accounts-digest — 多账户投放画像汇总

一条命令替代 AI 对每个账户循环 `list-accounts -k` + `stats`。**多账户汇总表、对比消耗、跨账户巡检、账户级 CPA / 零转化巡检** 应优先本命令，禁止外层 for-loop 逐户 `stats`。

> **数据时效性**：与 `stats` / `balance-scan` 相同（Google `account-spend-overview` 分流；TikTok/Yandex/BingV2/**MetaAd** 为截至昨天的 `accountsoverview`）。完整表见 `references/analytics/account-analytics.md` 顶部。

> **反模式**：
>
> - **无** `--period` / `--date-start`；区间只用 `--start`/`--end`（别名 `--start-date`/`--end-date`）。
> - 口语「零询盘 / 转化成本」且**无 CRM 询盘附件** → 本命令（P3），**不是** P7。
> - `conversions` / `cpa` 可能为 **null**（overview 未返回转化）→ 交付写「转化未返回」；脚本勿对 null 做数值比较。过滤用 `--max-cpa` / `--zero-conversions`，巡检交付用 `agentBrief.userDelivery`，勿手写脆弱 Python 重算 CTR/合计。
> - **没有** `cpa-risk-scan`。`--max-cpa` 的零转化仅当消耗已超过阈值才命中。`meta.totals` **只合计 returned**，禁止写成全部账户。`ctr` 已是百分数。
> - **没有**按户循环 `ad campaigns` 来判断 Display / PMax 的做法。要系列类型（含暂停）就加 `--with-campaign-types`。要「启用系列里有没有 PMax」或「启用但区间展示为 0」就加 `--with-enabled-campaigns`。两个开关不要一起开。只查消耗 > 0 的户。
> - 行上已有 `dailySpend`（区间消耗 / 天数）和 `remainingDays`（余额 / 日均，未拉余额时为 null）。要续航就不要 `--skip-balance`，也不要再对同一批账户跑 `balance-scan`。

```bash
siluzan-tso accounts-digest -m <媒体类型> [选项]
```

| 选项                          | 说明                                                                                                          | 默认    |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------- | ------- |
| `-m, --media <type>`          | 媒体类型（必填）：`Google \| TikTok \| Yandex \| MetaAd \| BingV2`                                    | —       |
| `-a, --accounts <ids>`        | 指定 `mediaCustomerId`，逗号分隔；**留空**则翻页拉该媒体全部账户                                              | —       |
| `--start <YYYY-MM-DD>`        | 统计开始日期（SKILL 要求 AI 先与用户确认区间）                                                                | 近 7 天 |
| `--end <YYYY-MM-DD>`          | 统计结束日期                                                                                                  | 昨天    |
| `--start-date` / `--end-date` | 同 `--start` / `--end`（兼容别名）                                                                            | —       |
| `--min-spend <n>`             | 过滤：区间内消耗 ≤ 此值的账户不返回                                                                           | `0`     |
| `--max-cpa <n>`               | 过滤：保留 CPA > n 的账户；零转化仅当消耗已 > n 才命中                                                        | —       |
| `--zero-conversions`          | 过滤：保留区间消耗 > 0 且转化 = 0 或转化未返回的账户                                                          | off     |
| `--skip-balance`              | 只拉消耗、不拉余额（转化成本巡检推荐）                                                                        | off     |
| `--page-size <n>`             | 全量扫描时清单分页大小（上限 500）                                                                            | `200`   |
| `--max-pages <n>`             | 全量扫描时最多页数（上限 200）                                                                                | `20`    |
| `--login-customer-id <id>`    | 只保留该 MCC（`ma.loginCustomerId`）下的账户。可带横杠。先拉清单再过滤，**不要**先 `list-accounts` 把 ID 拼进 `-a` | —       |
| `--with-campaign-types`       | **仅 Google**。对区间消耗 > 0 的账户并发请求 `campaigns/types-summary`，每行写入系列类型（含暂停）。判断「有没有 Display/PMax」用这个 | off     |
| `--campaign-type-concurrency <n>` | 上面这个请求的并发（1–16）                                                                              | `8`     |
| `--with-enabled-campaigns`    | **仅 Google**。对区间消耗 > 0 的账户并发拉系列列表。`hasEnabledPmax` 只看启用中的系列；`zeroImpressionEnabled` 是启用、展示为 0、且不是 PMax/Display 的系列。D 组巡检用这个，禁止逐户 `ad campaigns`。不要和上一行一起开 | off     |
| `--enabled-campaign-concurrency <n>` | 启用系列列表的并发（1–16）                                                                         | `8`     |
| `--json-out <path>`           | **Agent 推荐**：落盘目录或 `*.json` 文件；stdout 一行摘要（含 `outlineFile`、`writtenFiles`、`manifestFile`）。全量扫描必带，否则超时暂停后无法续跑 | —       |
| `--time-budget <时长>`        | 单次执行的时间预算（`25m` / `90s`；`off` 不限）。默认按宿主工具超时推断，一般不用传                           | 自动    |
| `--fresh`                     | 丢弃 `--json-out` 里的旧断点从头扫。仅用户明确要求重扫时用                                                    | off     |

> **超时暂停（exit 75）**：同 `balance-scan`。stdout 为 `state=paused` 时原样执行 `resumeCommand`，直到输出正常摘要；`--with-campaign-types` / `--with-enabled-campaigns` 的按户结果也会续用。续跑沿用首次执行的区间与账户清单。

**`--json-out` 落盘**：

- 目录模式典型文件：`accounts-digest-<媒体小写>.json`、同 stem 的 `*.outline.txt`、`cli-manifest-<媒体小写>.json`（读盘协议见 `references/core/agent-conventions.md` §三）。
- 响应结构：`{ ok, data: { items: [...] }, meta, agentBrief }`。`meta.totalsScope` 恒为 `returned`（只合计命中行）。`agentBrief.userDelivery` 是可粘贴表或「全部正常」句；巡检任务**只发这一段**。
- `meta.source`：`list` = 全量翻清单后拉数；`subset` = 传了 `-a`，跳过清单翻页（**`advertiserName` 会缺失**，公司名列显示 `-`）。
- `meta.nullConversionCount`：`conversions == null` 的行数；交付时勿把 null 当 0 硬比。
- `items[].ctr` 已是百分数（`11.01` = 11.01%）。`--json-out` 后 stderr 有一行防误读摘要。

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

# 转化成本巡检：CPA > 500（零转化仅消耗已超 500 才命中）；不拉余额
siluzan-tso accounts-digest -m Google --start 2026-07-14 --end 2026-07-20 \
  --max-cpa 500 --skip-balance --json-out ./snap-cpa
# 读盘后 print(data.agentBrief.userDelivery) 原样发给用户

# 零转化 / 口语「零询盘」巡检（无 CRM 附件时用本命令，不是 P7）
siluzan-tso accounts-digest -m Google --start 2026-07-20 --end 2026-07-20 \
  --zero-conversions --json-out ./snap-zero-conv

# Google 四项巡检：CPA、余额、零转化、有没有 Display/PMax。一条命令，不要再逐户拉系列
siluzan-tso accounts-digest -m Google --login-customer-id 397-889-3117 \
  --with-campaign-types --start 2026-10-16 --end 2026-10-22 \
  --json-out ./snap-inspect
```

四项都要时不要加 `--max-cpa` / `--zero-conversions`（会丢掉其它行）。外层命令必须直接是 `siluzan-tso`，不要写进 Python 再调用。

**`data.items[]` 主要字段**：`mediaCustomerId`、`name`、`advertiserName`、`currencyCode`、`balance`、`spend`（**区间合计**，同 `stats`）、`dailySpend`（`spend / meta.window.dayCount`）、`remainingDays`（`balance / dailySpend`；没拉余额或日均低于 0.01 时为 null）、`impressions`、`clicks`、`conversions`（可为 null）、`ctr`（%）、`cpc`、`cpa`（可为 null）。跨币种汇总见 `references/accounts/currency.md`（**禁止**对 `meta.totals` 跨币种直接当最终结论）。

**`--with-campaign-types` 额外字段**（只在打开开关时出现）：

| 字段 | 含义 |
| --- | --- |
| `campaignTypesStatus` | `ok` 查到了；`skipped-no-spend` 区间消耗为 0，没请求；`error` 这一户失败 |
| `campaignTypes` | `ok` 时是计数 > 0 的类型名（如 `Search`、`Display`、`PerformanceMax`）；否则 `null` |
| `channelTypeV2` | 仅 `ok` 时出现，与 `campaignTypes` 是同一数组。用户要的 `channelTypeV2` 就是这个字段，不要再逐户 `ad campaigns` |
| `hasDisplay` | `ok` 时才是布尔。`Display` 计数 > 0 为 true |
| `hasPmax` | `ok` 时才是布尔。`PerformanceMax` / `PERFORMANCE_MAX` 计数 > 0 为 true |
| `campaignTypesError` | `error` 时的短原因 |

脚本规则：`campaignTypesStatus === "ok" && hasDisplay === false && hasPmax === false` 才算「无展示且无 PMax」。`error` 和 `skipped-no-spend` 单独列出，**禁止**当成「无」。`meta.campaignTypes` 有 `requested` / `ok` / `failed` / `skippedNoSpend`。digest 成功后用本地脚本读 JSON、写 Excel。不要再 `balance-scan`，不要再逐户 `ad campaigns`。工作目录里已有这份 digest 时，`ad campaigns` 会直接读这里的系列类型；巡检不要加 `--live`。提示词若把这两步写成编号流程，仍以 digest 这一条为准。

**`--with-enabled-campaigns` 额外字段**（只在打开开关时出现）：

| 字段 | 含义 |
| --- | --- |
| `enabledCampaignStatus` | `ok` 查到了；`skipped-no-spend` 区间消耗为 0，没请求；`error` 这一户失败 |
| `hasEnabledPmax` | `ok` 时才是布尔。只看 `statusV2=Enabled` 的系列里有没有 PMax。暂停的 PMax 不算 |
| `enabledCampaignCount` | `ok` 时是启用系列条数 |
| `zeroImpressionEnabled` | `ok` 时是数组。启用、区间展示为 0、且类型不是 PMax / Display。元素为 `{ id, name, channelType }` |
| `enabledCampaignError` | `error` 时的短原因 |

`enabledCampaignStatus === "ok" && hasEnabledPmax === false` 才算「启用系列里没有 PMax」。`error` 和 `skipped-no-spend` **禁止**当成「无」。`meta.enabledCampaigns` 有 `requested` / `ok` / `failed` / `skippedNoSpend`。

```bash
# D 组：CPA、零转化、余额续航、启用 PMax、启用但 0 展示。一条命令
# 不要 --skip-balance，不要再 balance-scan，不要先 list-accounts 拼 -a，不要逐户 ad campaigns
siluzan-tso accounts-digest -m Google --login-customer-id 397-889-3117 \
  --with-enabled-campaigns --start 2026-10-19 --end 2026-10-25 \
  --json-out ./snap-dgroup
```

---

## stats — 查询投放消耗数据

> **数据时效性**：
>
> - **Google**：走 `account-spend-overview`；`--start` / `--end` 日历日按 **UTC+8** 转为 `YYYY-MM-DDTHH:mm:ss+08:00` 再请求（起 00:00:00、止 23:59:59，含今天时 end 截到当前时刻）。与 `google-analysis`（只传年月日）口径不同。
>   - 窗口完全在历史 → `database` 模式；窗口含今天 → `googleCombined` 模式（仅实时消耗，无余额/状态/币种/账户名）。
> - **TikTok / Yandex / BingV2**：走旧版 `accountsoverview`，每日凌晨同步昨天数据，**不能查今天**。Bing 看昨天/今天消耗用 `bing-analysis`（数据可能不完整）；TikTok 用 `tiktok-analysis official-report`。Google「今天」仍走 `google-analysis(-batch) --sections overview`。
> - 完整时效性表见 `references/analytics/account-analytics.md` 顶部。

```bash
siluzan-tso stats -m <媒体类型> [选项]
```

| 选项                          | 说明                                                                                                                           | 默认   |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------ |
| `-m, --media <type>`          | 媒体类型（必填）                                                                                                               | —      |
| `-a, --accounts <ids>`        | 账户 `mediaCustomerId`（**必填**；与 `list-accounts` 的 `ma.mediaCustomerId` 一致；Yandex=`porg-…`；**禁止** UUID/`entityId`） | —      |
| `--start <YYYY-MM-DD>`        | 开始日期                                                                                                                       | 7 天前 |
| `--end <YYYY-MM-DD>`          | 结束日期                                                                                                                       | 昨天   |
| `--start-date` / `--end-date` | 与 `--start` / `--end` 同义（CLI 别名，与 SKILL Playbook 一致）                                                                | —      |
| `--by-day`                    | 按日明细（`items[]` 带 `date`）；按日 Excel 见 `stats-daily-excel.md`                                                          | 关     |
| `--json-out`                  | 输出原始 JSON；**失败时 stdout 仍为 JSON**（`{"ok":false,"error":"..."}`）                                                     | —      |

**口径（易错）**：默认 **`spend` = 区间合计**（非日消耗）。按日加 `--by-day`；单日可用 `start=end`；日均用 `spend/天数` 或 `balance-scan` 的 `dailySpend`。

**空结果 / verbose `HTTP 403` 排查（必做，再谈 OAuth）**：

1. 用户若已给出账户号（如 Yandex `porg-kqquuxx6`），`-a` **必须原样用该 mediaCustomerId**；先 `list-accounts -m <媒体> -k <mediaCustomerId>` 核验存在即可。
2. **禁止**把 `ma.entityId`、`externalMediaAccountTokenId` 或会话里其它 UUID 传给 `-a`（会空结果，verbose 常打出被吞的 `HTTP 403`，**不等于** OAuth 过期）。
3. Google：仅当 `list-accounts` **输出中出现** `scopeActivatedSources` 且可判定未激活时，才可向用户说明需先激活套餐；**若无该字段，禁止谈套餐激活**。空结果时按 CLI 报错/字段说明，**禁止**用非 CLI / 自拼请求等方式绕过。
4. 仅当 `list-accounts` 显示 `invalidOAuthToken=true`（或授权状态列为失效），且用户确认后，才走 `account reauth --id <entityId> --i-confirm --commit "…"`（见 `accounts-permissions.md`）。
5. `list-accounts` 显示 `Linked` + `hasToken:1` + `invalidOAuthToken=false`（若有激活字段则须已激活）时，**禁止**因 stats/balance 空结果自行 `reauth`/解绑。

**示例：**

```bash
siluzan-tso stats -m Google -a <mediaCustomerId>
siluzan-tso stats -m Google -a <mediaCustomerId> --start 2026-03-01 --end 2026-03-31
# Yandex：-a 必须是 porg-…（mediaCustomerId），不是 entityId
siluzan-tso list-accounts -m Yandex -k porg-kqquuxx6 --json-out ./snap
siluzan-tso stats -m Yandex -a porg-kqquuxx6 --start 2026-07-21 --end 2026-07-21 --json-out ./snap
siluzan-tso stats -m Yandex -a porg-xxx --start <S> --end <E> --by-day --json-out ./snap/daily.json
siluzan-tso stats -m BingV2 -a <id1>,<id2> --start 2026-03-01
siluzan-tso stats -m Google -a <mediaCustomerId> --json-out ./snap
```

---
