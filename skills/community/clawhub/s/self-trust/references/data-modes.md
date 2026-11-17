# data-modes — 三数据模式/对账/切换（§3 / §3.1 / §3.2）

> 全局参数（--data-dir / --today / JSON 输出）见 SKILL.md。

## 1. 三模式对比（§3）

| 模式 | 资产台账 | 日常消费 | 负担 | 适用 |
|---|---|---|---|---|
| `ledger` | 完整持久 | 逐笔强制 | 高 | 精细化记账用户 |
| `conversational` | 不留存（会话即弃） | 单次临时 | 极低 | 试用/不愿记账 |
| `hybrid`（默认） | 资金池/目标/注入持久 | 口头临时审 | 中 | 绝大多数用户 |

边界护栏：
- ledger 缺流水 → 报表标「数据不全，测算存在偏差」；
- conversational 每次审批**必须用户手动确认当前总资产**，未确认审批中止；审批结论仍落 approval_log（审计不豁免）；报表 notes 自动标「估算数据，精度有限」；
- hybrid：临时消费数据**绝不修改底层 corpus**，只有正式收入/注入/经审批支取才更新。

## 2. 平滑过渡提示（§3.1）——已实装

仅 hybrid 触发、仅提示不自动改（用户终裁，`记账切模式` 命令本身待实施）：
- 连续 7 天上报（report_streak ≥ 7）→ 建议升 ledger；
- 连续 14 天缺报（gap_streak ≥ 14）→ 建议降 conversational。

实装口径（modules/streaks.py，运行态字段 last_report_date / report_streak / gap_streak）：
- 「上报事件」= `report` 报表生成 / `reconcile` 对账补录 → report_streak 按连续自然日 +1
  （同日幂等、断档重计 1），gap_streak 归零；
- `judge` 审批不算上报，仅惰性刷新 gap_streak（距最近上报日自然日数）；
- 达阈 → report / judge / reconcile 输出附 `mode_transition_hint`（suggest_mode + 真实计数文案），
  report 另将文案追加进 notes；report 场景先观察后记录（`gap_streak_observed` 回显），
  缺报 14 天后首次报表仍能看到降级建议；
- ledger / conversational 已定态不弹；引擎绝不自动改 mode（§10.3）。

## 3. hybrid 定期对账（§3.2）——已实装

```bash
python scripts/cli.py reconcile [--corpus <元>] [--income <元>] \
    [--invest <元>] [--living <元>] [--impulse <元>]
```

- 用户拍板修正：`--corpus` 写入修正后的资金池余额（configurator 动作，引擎不自动改写，§10.3 最小权限）；输出 `changes.corpus.from/to` 回显差异；
- 当月实绩补录：`--income/--invest/--living/--impulse` 追加一条 monthly_history 快照（`source=reconcile`；同月多条按最后一条为准，§6.2 收入监测口径）；
- 每次对账更新 `reconcile.last_reconcile` = 当日、`reminder_streak` 归零；
- 对账差额不进入审批判定历史，仅同步真实基数（F0 回到真实现金流）；
- 提醒调度[待实施]：距 last_reconcile 满 period_days（默认 30）推送核对提醒；reminder_streak 超阈值（默认 2）建议降级 conversational（复用 §3.1，不强制）。ledger / conversational 不触发本机制。

## 4. 切换命令

`记账切模式 ledger|conversational|hybrid`[待实施] —— mode 为非核心配置字段，普通确认即可（不过 §5.4 闸门），但仍属配置区（仅配置者可改）。
