# 账户管理（导航）

> `SKILL.md` 已指向子文件时，**直接 Read 子文件**，不必先读本文件。

## 何时 Read

| 任务                                                                                                    | Read                                                                                                                          |
| ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 列表 / 有哪些 / 有多少 / OAuth 失效筛查 / 激活账单 / 开户申请历史                                       | [`accounts-list.md`](accounts-list.md)                                                                                        |
| 单户余额、多户余额续航（**P2 `balance-scan`**）、单户消耗 `stats`、多户画像（**P3 `accounts-digest`**） | [`accounts-balance-stats.md`](accounts-balance-stats.md)                                                                      |
| 分享 / 解绑 / 重授权 / MCC / BC / BM / 关闭 / 提现 / 邮箱授权                                           | [`accounts-permissions.md`](accounts-permissions.md)                                                                          |
| 五大媒体开户参数与首次必填                                                                              | [`open-account-by-media.md`](open-account-by-media.md)（Google UI：[`open-account-google-ui.md`](open-account-google-ui.md)） |
| 充值 / 转账 / 发票                                                                                      | [`finance.md`](finance.md)                                                                                                    |
| 币种与跨币种禁止求和                                                                                    | [`currency.md`](currency.md)                                                                                                  |
| 写审计 / `--commit` / restore                                                                           | [`write-audit-restore.md`](write-audit-restore.md)                                                                            |

## Gotchas（账户域）

- `list-accounts` **不含**余额/消耗；列全部账户用 `--page-size 999`，禁止默认 20 再翻页。
- `entityId`（UUID，分享/delink/账单/`reauth`）≠ `mediaCustomerId`（`balance`/`stats`/`accounts-digest`/`ad` 的 `-a`）。**Yandex 的 mediaCustomerId 形如 `porg-…`，不是 UUID。**
- MetaAd OAuth 户官方 `mediaCustomerId` 带 `act_`。`balance` / `stats` / `balance-scan` / `accounts-digest` 的 `-a` 传裸数字或 `act_` 均可，CLI 会规范成清单官方 ID 再打 TSO。
- **Google CID**：广告后台展示常为 `XXX-XXX-XXXX`（连字符），平台 `mediaCustomerId` 是**纯数字**。查单户必须 `list-accounts -m Google -k <用户原样>`（CLI 去横杠）；**禁止**无 `-k` 拉首页 20 条再判定未绑定。`stats`/`balance`/`ad *`/`google-analysis` 的 `-a` 可带连字符（CLI 会去掉）；若仍见 `HTTP 403：123-456-7890` 这类**回显带横杠 ID**，优先改成纯数字重试，**不要**直接当 OAuth 失效去 `reauth`。
- **禁止臆测授权过期**：403 / 拉数失败时**禁止**口头说「可能授权过期」。须 ID 核验后，**仅 Google** 执行 `account check-access -a <mediaCustomerId>`（无 `-m`，其他媒体禁止调用），以返回 `status` 为准（见 [`accounts-permissions.md`](accounts-permissions.md)）；仅当 `list-accounts` 输出含激活字段且可判定未激活时，勿用其判断授权过期；非 Google 看 `invalidOAuthToken`。
- `stats`/`balance` 空结果 + verbose `HTTP 403`：先确认 `-a` 是否为 `ma.mediaCustomerId`（且 Google 已去连字符）；**禁止**把 `entityId` / tokenId 当 `-a`；未跑 `account check-access`（或未见 `invalidOAuthToken=true`）**禁止** `reauth`。
- 多账户余额预警用 `balance-scan`（P2），多账户消耗汇总用 `accounts-digest`（P3）；**禁止**外层 for-loop 逐户 `balance`/`stats`。
- `stats` 默认 `spend` = **区间合计**，不是日消耗；日均看 `balance-scan.dailySpend` 或合计÷天数。
