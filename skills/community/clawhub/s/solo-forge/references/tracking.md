# 项目管理模块

管理项目数据时加载此模块。所有数据直接读写 JSON 文件。

## 数据位置

- `data/deals.json` — 项目数据
- `data/clients.json` — 客户档案（管理见 [clients.md](clients.md)）
- `data/config.json` — 用户偏好

文件不存在时创建空结构。完整 schema 示例见 `data/example/`。⚠️ example/ 仅作结构参考，不得作为业务数据使用。

## 计费类型支持

`billing_type` 字段决定付款结构：

| billing_type | 付款结构 | milestones 用法 |
|:---|:---|:---|
| fixed | 固定总价，按里程碑分期 | [{label, pct, amount}] |
| hourly | 按工时计费，月度结算 | 不用 milestones，用 hours(工时数)×rate(时薪) |
| daily | 按天计费 | 不用 milestones，用 days(天数)×daily_rate(日薪) |
| retainer | 月度/季度服务费 | [{label, period("月"/"季"), amount}] |
| commission | 按成果提成 | [{label, condition, pct(提成百分比), cap(金额上限，单位：元)}] |

用户未指定时默认 `fixed`。生成报价/合同时按 billing_type 自动调整付款条款。

### 非 fixed 类型的字段取值

| 字段 | hourly | daily | retainer | commission |
|:---|:---|:---|:---|:---|
| total_amount | 0（完工后按实结算） | 0（完工后按实结算） | 单期服务费（如月费） | 0（按结果结算） |
| due_date | 下次结算日 | 下次结算日 | 合同到期日 | 首次结算日 |
| milestones | `[]` | `[]` | [{label, period, amount}] | [{label, condition, pct, cap}] |

## 操作映射

| 用户说 | 执行 |
|:---|:---|
| "添加项目/新建项目" | 追加 deal，按 billing_type 计算付款节点 |
| "项目列表/查看项目" | 列出所有，显示总额/已收/待收/状态 |
| "更新项目/已收款X元" | 找到 deal 更新 paid 字段 |
| "逾期检查/催款提醒" | 遍历进行中的 deal，对比 due_date |
| "经营概览" | 汇总总金额/已收/待收/回款率/客户集中度 |

## deal 关键字段

`id`, `client`, `project`, `total_amount`, `paid`, `status`(进行中/已交付/已完成/已取消), `due_date`, `billing_type`(fixed/hourly/daily/retainer/commission), `milestones`[{label, pct, amount}], `notes`, `created_at`(YYYY-MM-DD), `updated_at`(YYYY-MM-DD)

hourly 额外字段：`hours`(工时数), `rate`(时薪，单位：元)
daily 额外字段：`days`(天数), `daily_rate`(日薪，单位：元)

每次更新 deal 时自动更新 `updated_at`。

## 逾期检查逻辑

对比 due_date 与当前日期：1-3天🟡友好 / 4-7天🟠正式 / 8-14天🔴严肃(提及违约金：每日0.5%累计不超30%) / 15天+🚨法律预警

## 用户配置 (config.json)

首次使用时询问确认默认值并保存：
`default_deposit_pct`(40), `default_milestone_pct`(30), `default_final_pct`(30), `default_acceptance_days`(5), `default_penalty_daily_pct`(0.5), `default_revision_rounds`(3), `default_quote_validity_days`(15), `currency`("人民币")

## 项目状态转换

| 当前状态 | 触发词/条件 | 新状态 | 说明 |
|:---|:---|:---|:---|
| 进行中 | "交付了""做完了" | 已交付 | 标记后触发：建议发验收报告 |
| 已交付 | "验收通过了""客户确认了" | 已完成 | 标记后触发：建议发满意度调查 + 确认尾款 |
| 进行中/已交付 | "取消了""不做了" | 已取消 | 需确认已收款金额，提醒结算已完成部分 |
| 已完成 | — | — | 终态，不再变更 |

用户说"做完了""验收通过了""项目取消了"时自动更新 status 和 `updated_at`。用户也可手动指定状态。

## 客户集中度

计算方式：从 deals.json 按 client 分组求和 total_amount → 最大客户金额 / 全部总额 × 100%

最大客户占总营收 >40% → 主动提醒"客户集中度较高，建议拓展更多客户"
