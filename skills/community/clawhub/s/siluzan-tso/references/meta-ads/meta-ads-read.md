# Meta 线索广告 · 只读

> 流程见 `workflows.md` **W13**。金额/ID 口径见 [meta-ads.md](meta-ads.md)。
> **何时 Read**：选主页、复用表单、按 ID 复核刚创建的对象。

## 命令

```bash
siluzan-tso list-accounts -m MetaAd --page-size 999 --json-out ./snap
siluzan-tso meta-ad account -a <accountId> --json-out ./snap
siluzan-tso meta-ad pages -a <accountId> --json-out ./snap
siluzan-tso meta-ad forms -a <accountId> --page-id <pageId> --json-out ./snap
siluzan-tso meta-ad campaign -a <accountId> --id <campaignId> --json-out ./snap
siluzan-tso meta-ad adset -a <accountId> --id <adSetId> --json-out ./snap
siluzan-tso meta-ad ad -a <accountId> --id <adId> --json-out ./snap
```

`meta-ad campaign/adset/ad` 仍是**按 ID 读单条**（W13 复核刚创建的对象）。账户级列表、拒审、落地页走 `facebook-analysis campaign-entities` / `adset-entities` / `ad-entities`（见 `hosted-automation-facebook.md`）。

## 字段口径

| 字段 | 含义 |
| --- | --- |
| `account_status=1` | 账户活跃 |
| `amount_spent` / `balance` / `spend_cap` / `daily_budget` | 网关最小货币单位字符串 |
| `*Display` | 主币种元（展示用这个） |
| `currency` | ISO 币种；换算按此币种小数位（JPY 等零小数不 ×100） |
| `items[].id`（`meta-ad pages`） | 投放主页；**不含** Page Token。`tasks` 含 `ADVERTISE` 才可投 |
| `data[].id`（`meta-ad forms`） | Instant Form ID，可写入 JSON `form.reuseId` |

`spend_cap` 与 `amount_spent` 持平 → 花费上限已顶满，ACTIVE 也投不出去。

拉表单留资线索：`clue -m Meta -a <pageId> --start --end`（W11）。
