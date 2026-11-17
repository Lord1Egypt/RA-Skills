# report — 报表/校准/奖励/目标生命周期/日志（§6.1~§6.4 / §10.1）

> 全局参数（--data-dir / --today / JSON 输出）见 SKILL.md。数字一律原样引用引擎 JSON，禁止心算。

## 1. 记账报表（§6.1）——已实装

```bash
python scripts/cli.py report
```

输出关键字段（双段呈现）：
- **文字统计**：`corpus` / `net_assets` / `monthly_net` / `living_baseline` / `effective_cushion` / `cushion_margin`（垫上余量）/ `cushion_alert`（余量 <1 个月生活费 → 红色预警，§10.2）；
- `objectives[]`：每目标 achieved_ratio / lag / time_progress / color（green=超前 / yellow=落后 / red=lag≥10% 严重落后）/ 单目标 ascii 进度条；无 deadline 目标只展示攒钱占比；
- `ascii`：拼好的双轨进度条 + 近 6 月资金流向 ASCII 趋势图（攒钱/生活/冲动 + 安全垫红线，monthly_history 快照数据源）——直接引用展示，勿自绘；
- `pending_cooling[]`：冷静期挂起申请（顺带提醒用户）；
- `notes[]`：conversational「估算数据，精度有限」/ 安全垫预警 / 临时校准生效提示——**必须转述**；
- `snapshot_appended`：当月首报自动落一条 monthly_history 快照（income 等实绩为 null 不虚构，由对账补录）。

## 2. 月度校准（§6.2 / §6.4）——已实装

```bash
python scripts/cli.py calibrate [--force]   # 同月幂等（skipped=true），--force 强制重跑
```

确定性规则（引擎执行，LLM 只转述 `changes[]`）：
- **缓冲**：目标连续 2 月 `lag > 0`（F4）才触发（lag_streak≥2），单月突发不收紧；
- **柔性优先**：真实净月增（F3.5/F7）>0 → target_amount 下调 / deadline 顺延建议，写 `rebalance_override` 临时层，**不改原始 objectives**；
- **刚性兜底**：柔性不可行 → boost 上限 +15pct + 非计划审批通过率收紧；
- **收入放松**：monthly_history 实绩连续 2 月 ≤ 基线×0.8 → 宽松态（invest_ratio 临时 −10pct，保 living_baseline），优先于收紧；恢复自动回滚；
- **次月自动回滚**：跨月清空上月 rebalance_override；报表强制提示「仅本月有效/原始权重不变」；
- §6.4：active→overdue 由引擎确定性翻转（超期客观事实）；completed 仅建议不代决。

## 3. 里程碑奖励（§6.3）——已实装

```bash
python scripts/cli.py reward                       # 默认 --action status：各目标达成率/可解锁/剩余额度
python scripts/cli.py reward --action unlock       # 扫描解锁：达成率≥120% → reward_quota = 超额×20%（F6）
python scripts/cli.py reward --action claim --objective <名> --amount <元> --purpose "<用途>"
```

- claim：免冷静期但**仍走 §4.4 统一判定与安全垫校验**（场景 C → `error=cushion_violation` 拒付）；
- reward_quota 分次递减到 0 即用尽；单目标仅解锁一次基础奖励（150%/200% 梯度留参数不实现，§8.2）；
- 全程落 reward_log。

## 4. 目标生命周期（§6.4）——已实装

```bash
python scripts/cli.py objective --name <名> --to completed|archived [--confirm]
```

- 无 `--confirm` → 返回 need_confirm + released_weight 提示（回显闸门）；
- completed 须达成 100%（否则 `error=not_achieved`）；archived 归档后 current_amount 回归资金池自由层；
- weight 释放后提示用户重分配（引擎不自动改其它目标权重，§10.3）；落 approval_log 归档记录；
- overdue 由 calibrate 引擎自动翻转，不走本命令；延期/降额走护栏修改（§5.4 闸门）。

## 5. 审计日志查询（§10.1）——已实装

```bash
python scripts/cli.py log --name approval_log|appeal_log|override_log|reward_log|monthly_history
```

只读（默认 approval_log）；审计仅追加不可删，每笔审批含 F8 完整中间变量，可逐式复盘验算。
