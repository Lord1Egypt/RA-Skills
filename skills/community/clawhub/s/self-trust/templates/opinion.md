# 审批意见书 — 字段速查（templates/opinion.md）

> ⚠️ **本文件仅作字段映射速查（字段名→JSON 路径）+ 场景语义要点。**
> 输出**格式一律以 `references/rendering.md` 为准**（审批紧凑卡片见 §11、长模板 B/C 见 §1.4）。
> 下方「场景语义要点」只讲该展示哪些信息、**不**提供可照抄的格式；旧格式示例（§0.5 标准化前，与 rendering.md 冲突）已全部移除，禁止照抄。

---

## 场景语义要点（决定展示哪些字段/信息，格式套 rendering.md）

- **A-1 无冷静期**（金额 ≤ 阈值，直接放行）：套 §11 紧凑卡片；impacted_objectives 为空时省略目标影响行。
- **A-2 触发冷静期**（金额 > 阈值未破垫）：套 §1.4 长模板；须同时传达「可以花」+「先等 N 天」+「等不住可撤」三层；附冷静期天数/到期/request_id。
- **A-3 白名单极速放行**（免冷静期）：套 §11 A-3；告知剩余年度额度。
- **B 附条件**：套 §1.4；给具体数字选项（分期/延迟里程碑/缩减金额），不空泛建议；有冷静期附 request_id/到期。
- **C 驳回**：套 §1.4 三段式（契约对照→目标影响→替代方案）；基调「不是不让你花，是帮你算清代价后选更好的花法」。
- **C-融资购房**（financed=true）：展示首付/贷款/月供三件套，判定看首付是否击穿垫 + 月供是否可覆盖。
- **撤回激励**（withdraw）：全部来自 `feedback.*`（非 submit 的 `inputs.*`）；`feedback.objective` 为 null 时省略目标名；必须转述 `feedback.estimation_note`。

> 分期方案（`alt_months` / `alt_per_month`）为**唯一允许 LLM 推算的值**（不改变判定结论，仅呈现建议）：`alt_months = ceil(inputs.amount / cooldown.threshold)`，`alt_per_month = cooldown.threshold`；金额本身仍引用引擎输出。

---

## JSON 字段 → 占位符速查表

| 占位符 | JSON 路径（judge submit 返回） | 说明 |
|---|---|---|
| `{decision.result}` | `decision.result` | 批准/附条件/驳回 |
| `{decision.summary}` | `decision.summary` | 一句话依据 |
| `{inputs.amount}` | `inputs.amount` | 申请金额 |
| `{inputs.category}` | `inputs.category` | 支出类目 |
| `{inputs.planned}` | `inputs.planned` | 是否计划内（布尔） |
| `{inputs.corpus}` | `inputs.corpus` | 资金池余额 |
| `{inputs.remaining_after}` | `inputs.remaining_after` | 扣除后余额 |
| `{inputs.effective_cushion}` | `inputs.effective_cushion` | 安全垫阈值 |
| `{inputs.monthly_net}` | `inputs.monthly_net` | 月度净流入 |
| `{inputs.monthly_basis}` | `inputs.monthly_basis` | 毛口径/净口径标记（`gross_estimate`/`net`）；`gross_estimate` 且 B/C/冷静期时在卡片正文追加 §1.5 毛口径提示行 |
| `{inputs.monthly_invest_nominal}` | `inputs.monthly_invest_nominal` | 月度可投增量（名义） |
| `{inputs.financed}` | `inputs.financed` | 是否融资购房 |
| `{inputs.down_payment}` | `inputs.down_payment` | 首付金额 |
| `{inputs.financed_amount}` | `inputs.financed_amount` | 贷款金额 |
| `{inputs.mortgage_monthly}` | `inputs.mortgage_monthly` | 月供 |
| `{inputs.debt_service_ok}` | `inputs.debt_service_ok` | 月供是否可覆盖 |
| `{cooldown.triggered}` | `cooldown.triggered` | 是否触发冷静期 |
| `{cooldown.threshold}` | `cooldown.threshold` | 冷静期阈值 |
| `{cooldown.days}` | `cooldown.days` | 冷静期天数 |
| `{impact.delay_months_simple}` | `impact.delay_months_simple` | 简化口径延后月数 |
| `{impact.note}` | `impact.note` | 误差披露语 |
| `{impacted_objectives[0].name}` | `impacted_objectives[0].name` | 最相关目标名（数组空时省略整行） |
| `{impacted_objectives[0].delay_months_real}` | `impacted_objectives[0].delay_months_real` | 真实口径延后月数 |
| `{request_id}` | `request_id` | 申请编号（仅冷静期触发时存在） |
| `{expire_at}` | `expire_at` | 到期时间（仅冷静期触发时存在） |
| `{whitelist.fast_track}` | `whitelist.fast_track` | 是否白名单极速 |
| `{whitelist.remaining_annual}` | `whitelist.remaining_annual` | 白名单剩余年度额度 |
| `{alt_months}` | 推导：`ceil(inputs.amount / cooldown.threshold)` | 分期月数（唯一允许推算） |
| `{alt_per_month}` | `cooldown.threshold`（每笔不超阈值） | 分期月额（引用阈值） |

### withdraw 返回字段（撤回激励文案专用）

| 占位符 | JSON 路径（judge withdraw 返回） |
|---|---|
| `{feedback.withdrawn_amount}` | `feedback.withdrawn_amount` |
| `{feedback.monthly_invest_nominal}` | `feedback.monthly_invest_nominal` |
| `{feedback.objective}` | `feedback.objective`（可能为 null） |
| `{feedback.ahead_months_simple}` | `feedback.ahead_months_simple` |
| `{feedback.ahead_months_real}` | `feedback.ahead_months_real` |
| `{feedback.estimation_note}` | `feedback.estimation_note` |
