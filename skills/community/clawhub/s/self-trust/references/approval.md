# approval — 审批热路径（§4.4 / §5.1）

> 适用：审批有分歧、触发冷静期、白名单场景。日常小额直批不需要读本文件。
> 全局参数（--data-dir / --today / JSON 输出）见 SKILL.md，不再重复。

## 1. judge 提交（--action submit，默认）

```bash
python scripts/cli.py judge --amount <元> --category <类目> [--planned]
```

输出 JSON 关键字段：
- `decision.scene`：A（批准）/ B（附条件）/ C（驳回）——§4.4 三场景，全局唯一标准；
- `decision.result` / `decision.summary`：结论与一句话依据；
- `cooldown.triggered` / `cooldown.threshold` / `cooldown.days`：是否入冷静期（F2 阈值）；
- `request_id` / `expire_at`：**仅冷静期触发时存在**——申请已入 pending_requests 队列（跨会话持久不丢单），后续撤回/确认/申诉都用这个 `request_id`；
- `whitelist`：白名单双上限判定（`listed` / `fast_track` / `per_tx_ok` / `annual_ok` / `remaining_annual`，§5.1.2）；
- `impacted_objectives[]`：lag 恶化校验命中的目标（name/weight/amount_share/delay_months_real/delay_months_simple/lag/material_lag）；
- `optimization_applied`：optimization_goal 三档阈值乘数与实际判定垫（goal/cushion_multiplier/judge_cushion）；
- `inputs.*`：全部中间变量（F0/F1/F3/F3.5 + remaining_after 等）——渲染意见书时原样引用；
- `impact.delay_months_simple`：简化口径延后月数（F5，须标「约」+误差披露）。

每笔提交自动落 approval_log F8 快照（含全部中间变量，§10.1 可复盘验算）。

## 2. 意见书渲染

驳回/附条件强制三段式（**格式见 `references/rendering.md` §1.4**）：契约对照 → 目标影响 → 替代方案。
措辞基调：「不是不让你花，是帮你算清代价后选更好的花法」（§5.3）。

## 3. 冷静期生命周期（§5.1）——已实装

`cooldown.triggered=true` 且非白名单极速 → 告知：
「申请已入冷静期 N 天（expire_at 见输出），第 1 天与到期前 1 天会提醒，期间可『记账撤回』或『记账确认执行』或『记账申诉』」。

| 动作 | 命令 | 状态迁移 |
|---|---|---|
| 撤回 | `python scripts/cli.py judge --action withdraw --request-id <id>` | cooling → withdrawn |
| 确认执行 | `python scripts/cli.py judge --action finalize --request-id <id>` | cooling → decided（按入队时原判定终裁） |
| 到期终裁 | `python scripts/cli.py judge --action expire [--request-id <id>]` | 原判定 A/B → decided；C → expired；省略 id 处理全部到期项 |
| 提醒数据 | `python scripts/cli.py judge --action reminders` | 只读，输出 `reminders[]`（days_left；kind=expiring 到期≤1天 / cooling 冷静中） |

撤回正向激励（§5.1.1）：withdraw 输出 `feedback`（withdrawn_amount / objective / ahead_months_simple / ahead_months_real / estimation_note）——「撤回 = 多攒 X 元 ≈ 目标提前约 Y 个月」，Y **原样引用引擎输出，禁止心算**；并转述 estimation_note（估算非承诺）。

## 4. 白名单告知（§5.1.2）

- `whitelist.fast_track=true`：免冷静等待，**不豁免 §4.4 判定与安全垫校验**；告知剩余年度额度 `whitelist.remaining_annual`（放行后引擎自动记账 used_annual，跨自然年归零）。
- 超单笔/年度上限 → 降级常规审批（走冷静期），明确告知原因（`per_tx_ok` / `annual_ok`）。
