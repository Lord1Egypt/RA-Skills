# Meta Instant Form 线索广告（导航）

> 流程见 `workflows.md` **W13**。命令参数见 [meta-ads-write.md](meta-ads-write.md) / [meta-ads-read.md](meta-ads-read.md)。

## 支持范围（硬边界）

| 能力 | CLI | 说明 |
| --- | --- | --- |
| Instant Form 线索广告 | ✅ | `OUTCOME_LEADS`；组优化目标仅 `LEAD_GENERATION` / `QUALITY_LEAD` |
| 视频 / Advantage+ / 其它目标 | ❌ | 本批不做 |
| 系列/组/广告列表 | 走巡检 | `facebook-analysis campaign-entities` / `adset-entities` / `ad-entities`（只读） |
| 拉已有线索 | 走 W11 | `clue -m Meta`，不是 `meta-ad` |
| 周期/诊断报告 | 走 P4-FB | `facebook-analysis run` |
| 当天/小时巡检 | 走自动化 SOP | `references/operations/hosted-automation-facebook.md` |

## 何时 Read

| 任务 | Read |
| --- | --- |
| 创建 / 编辑 / 启停 | [meta-ads-write.md](meta-ads-write.md) |
| 读账户 / 主页 / 表单 / 按 ID 读对象 | [meta-ads-read.md](meta-ads-read.md) |
| JSON 字段 | `assets/meta-lead-create-template.json`（先）+ `assets/meta-lead-create-template.md` |
| 出方案 / 审查稿 / 要表格 | [meta-lead-launch-plan-template.md](meta-lead-launch-plan-template.md) |

## Gotchas

- **命令族**是 `meta-ad`，**禁止**塞进 Google `ad`，**禁止** `--media MetaAd` 调 `ad campaigns`。TikTok / Bing / Yandex **没有**对等搭建命令。
- `-a` / JSON `account` = `list-accounts -m MetaAd` 的 `mediaCustomerId`（数字或 `act_`）。**禁止**传 `entityId`（UUID）。
- **金额**：CLI / JSON 填**主币种元**。读出口 `*Display` 已是元；原始 `daily_budget="1000"` 在 USD 是 $10，**禁止**当 $1000。
- **CBO / ABO**：预算只放一边；本批不能切换。
- **默认 PAUSED**。投放须系列 / 组 / 广告三个都 `ACTIVE`。
- **表单 / 图 / 创意无就地改口**。换图或换表单：新建创意，再 `ad-edit --creative-id`。
- **主页 `--json-out`**：数组在 `items[]`（`id` / `name` / `tasks`），**不是** `pages[]`。`tasks` 须含 `ADVERTISE`。空列表或 `PAGE_LIST_EMPTY` / `PAGE_NOT_LINKED` → 补主页广告投放权限并重新授权，不要硬填历史 `pageId`。
- **HTTP 403**（账户/主页）：当前 Token 没有该户 Facebook Ads 权限，停；换有权限的登录或重新授权，不要硬跑 `create`。
- **`LEAD_TOS_REQUIRED`**：主页须在 Ads Manager 勾选潜在客户开发广告服务条款；**禁止**让接口代勾。
- **`BID_AMOUNT_REQUIRED`**：停下并看 `needs_decision`。不要把日/总预算当成 bid cap，也不要改成别的出价策略。只有事先写了 `adset.bidAmountOnRequired`（或 `adset-create --bid-amount-on-required`）才会按**该金额**用 `LOWEST_COST_WITH_BID_CAP` 再试一次。
- **组定向**：创建时国家/年龄/性别 + 可选 `flexible_spec`，并提交 `targeting_automation.advantage_audience`（默认 `1`；有非空 `flexibleSpec` 时默认 `0`）。`adset-edit` 不套这个默认值：不传则保留当前的 `0` 或 `1`；读不到当前值时停下，须显式 `--advantage-audience`。`--countries` 默认整表替换，追加用 `--countries-mode append`。组失败用已有 `campaignId` 续跑，不要新建空系列。
- **支付方式**：建到广告对象时 Graph 可能报「请更新支付方式」。已建成的系列/组/创意会留着，**不要**重头 `create`；停下来让用户在账单与支付中心加有效付款方式，再用 `ad-create` 续跑。
- 花费上限顶满（`spend_capDisplay` ≈ `amount_spentDisplay`）时对象仍能建成，**ACTIVE 也投不出去**。
