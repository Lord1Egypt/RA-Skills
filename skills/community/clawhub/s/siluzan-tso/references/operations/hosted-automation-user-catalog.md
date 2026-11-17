# 宿主编排能力目录

> **何时 Read**：用户明确问自动化 / 巡检 / 熔断 / 自控 / 异常监控 / 自动优化时。其他任务**跳过**本文件。
> **怎么读**：下表每行只 Read **一个**「SOP」列路径。Google 金额口径见 `references/google-ads/google-ads.md` § Gotchas + `references/accounts/currency.md`。
> 宿主侧告警优先级写作 **告警P1**（勿与 Playbook **P1** 账户诊断混淆）。

`guard` 与自动暂停/改价**只支持 Google**。Bing / Yandex / TikTok / Facebook 只能拉数告警，步骤见各自 SOP。

---

## Google：预算与 ROI 自控

| 场景             | 自动动作（摘要）                                                                                         | 首选 CLI / SOP（只读一份）                                                                                               |
| ---------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 单日预算熔断     | 当日花费相对日预算达阈值 → **列出命中**；暂停须逐账户 `ad campaign-status`                               | **首选** `references/operations/guard.md`（`guard budget-circuit`）；细节/单户排障见 `hosted-automation-self-control.md` |
| CPA 飙升自动降价 | 窗内 CPA 超目标 → 下调出价上限                                                                           | `references/operations/hosted-automation-optimize-weak-downbid.md`                                                       |
| 连续空耗自动暂停 | 当日花费达阈值且 0 转化 → **列出命中**；暂停须逐账户 `adgroup-status`/`ad-status`；宿主发 **告警P1**「空耗熔断」 | **首选** `references/operations/guard.md`（`guard zero-conv`）；细节见 `hosted-automation-self-control.md`               |

> **消耗 ≠ 日消耗**：`spend` 为 `--start`～`--end` 合计。`guard` 命令已强制 `--date` 单日；手写 `ad campaigns` 时须 `start=end=当日`。续航日均用 `balance-scan.dailySpend`。

## Google：异常监控

字段键名以当次 `--json-out` 为准，细则只读：`references/operations/hosted-automation-monitoring-json.md`。

| 场景       | CLI 入口（摘要）                                                         |
| ---------- | ------------------------------------------------------------------------ |
| 账户封禁   | `list-accounts` / `balance`（见 `references/accounts/accounts.md` 索引） |
| 落地页死链 | `google-analysis --sections final-urls` 或 `ad list`                     |
| 素材拒审   | `ad list` / `google-analysis --sections ads`                             |
| 花费异动   | `google-analysis --sections campaign-hour`                               |
| 余额枯竭   | `balance-scan`（P2）                                                     |

## Google：自动优化

索引（可选）：`references/operations/hosted-automation-optimize-index.md`。执行时直接读 SOP：

| 场景            | SOP                                                                        |
| --------------- | -------------------------------------------------------------------------- |
| 差广告降价/关停 | `references/operations/hosted-automation-optimize-weak-downbid.md`         |
| 高转化提价扩量  | `references/operations/hosted-automation-optimize-scale.md`                |
| A/B 决出胜者    | `references/operations/hosted-automation-optimize-ab-winner.md`            |
| 异动根因排查    | `references/analytics/account-analytics.md` + 对应 `report-templates/*.md` |

---

## Bing（BingV2）：只读巡检

全部步骤只读一份：`references/operations/hosted-automation-bing.md`。**不能**自动暂停/改价/改预算。

| 场景           | 做什么                                                                 | SOP                                              |
| -------------- | ---------------------------------------------------------------------- | ------------------------------------------------ |
| 余额 / IO 续航 | `balance-scan -m BingV2`；有 IO 再 `insertion-orders` + `monthly-spend` | `references/operations/hosted-automation-bing.md` |
| 账户封禁       | `bing-analysis account-status`；非 Active 告警                         | 同上                                             |
| 素材拒审       | `bing-analysis bulk-ads --editorial-status Disapproved`                | 同上                                             |
| 落地页死链     | `bulk-ads` 拉 URL，宿主 HTTP 探活                                      | 同上                                             |
| 当日超预算     | `campaign-entities` 日预算 + `run --aggregation Daily` 当日花费；只告警 | 同上                                             |
| CPA / 空耗     | `run --aggregation Daily\|Hourly`；只告警，不降价、不暂停              | 同上                                             |

## TikTok：只读巡检

全部步骤只读一份：`references/operations/hosted-automation-tiktok.md`。**不能**自动暂停/改价/改预算。

| 场景         | 做什么                                                                                          | SOP                                                 |
| ------------ | ----------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| 余额 / 封禁  | `tiktok-analysis account-status`；非 `STATUS_ENABLE` 告警                                       | `references/operations/hosted-automation-tiktok.md` |
| 素材拒审     | `ad-entities --secondary-status AD_STATUS_AUDIT_DENY`                                           | 同上                                                |
| 落地页死链   | `ad-entities` 拉 URL，宿主 HTTP 探活                                                            | 同上                                                |
| 当日超预算   | `campaign-entities` + `official-report` 系列当日 `spend`；只告警                                | 同上                                                |
| CPA / 空耗   | `official-report` 组小时/日报 + `adgroup-entities`；只告警，不降价、不暂停                      | 同上                                                |

## Yandex：只读巡检

全部步骤只读一份：`references/operations/hosted-automation-yandex.md`。**不能**自动暂停/改价/改预算。无小时维度。

| 场景         | 做什么                                                                 | SOP                                                |
| ------------ | ---------------------------------------------------------------------- | -------------------------------------------------- |
| 余额 / 归档  | `yandex-analysis account-status`；`archived=true` 告警                 | `references/operations/hosted-automation-yandex.md` |
| 素材拒审     | `ad-entities --status REJECTED`                                        | 同上                                               |
| 落地页死链   | `ad-entities` 拉 `landingUrls`，宿主 HTTP 探活                         | 同上                                               |
| 当日超预算   | `campaign-entities --time-increment 1 --network ALL`；只告警           | 同上                                               |
| CPA / 空耗   | `adgroup-entities` 近 3 日 + 当日 `--time-increment 1`；只告警         | 同上                                               |

## Facebook / MetaAd：只读巡检

全部步骤只读一份：`references/operations/hosted-automation-facebook.md`。**不能**自动暂停/改价/改预算。

| 场景         | 做什么                                                                                          | SOP                                                    |
| ------------ | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| 余额 / 封禁  | `facebook-analysis account-status`；`account_status != 1` 告警                                  | `references/operations/hosted-automation-facebook.md` |
| 素材拒审     | `ad-entities --effective-status DISAPPROVED`                                                    | 同上                                                   |
| 落地页死链   | `ad-entities` 拉 `landing_urls`，宿主 HTTP 探活                                                 | 同上                                                   |
| 当日超预算   | `campaign-entities` + `insights --level campaigns --time-increment 1`；只告警                   | 同上                                                   |
| CPA / 空耗   | `insights --level adsets` hourly/日报 + `adset-entities`；只告警，不降价、不暂停                | 同上                                                   |
