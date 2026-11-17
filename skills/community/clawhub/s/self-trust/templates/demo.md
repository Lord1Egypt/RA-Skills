# 三场景模拟演示 — 字段速查（templates/demo.md）

> 用初始化生成的**真实契约参数**测算（引擎输出，禁止心算），但**不落地真实账目**。
> 输出**格式一律以 `references/rendering.md` §4 为准**（套 §0.5 骨架）。
> 旧格式示例（§0.5 标准化前）已全部移除，禁止照抄。

## §4.1 双模式警告字段

| 条件 | 警告行模板 | 数据来源 |
|---|---|---|
| `demo_defaults_used=true` | `⚠️ 演示数据（场景为合成，基于默认参数），非真实审批` | 固定文案 |
| `demo_defaults_used=false` | `⚠️ 演示数据（场景为合成，基于你真实契约：资金池 ¥{corpus} / 月净流入 ¥{monthly}），非真实审批` | `engine_params.corpus` / `engine_params.monthly_contribution`（原样引用） |
| `engine_params.monthly_basis` 非空 | 真实契约含毛/净口径标记（`gross_estimate`/`net`），仅作上下文说明，不影响演示测算 | `engine_params.monthly_basis` |

## §4.2 场景列表字段

| 字段 | JSON 路径 | 格式 |
|---|---|---|
| 场景标签 | `scenarios[i].name` | 原样引用 |
| 金额 | `scenarios[i].amount` | §0.1（¥ + 千分位 + 2 位小数） |
| 判定 | `scenarios[i].scene` | A→批准 / B→附条件 / C→驳回 |
| 冷静期天数 | `scenarios[i].cooling_days` | 整数；A 时省略 |
| 目标延后 | `scenarios[i].delay_months_simple` | >0 时附注「· 目标延后约 {n:.1f} 个月（简化口径）」；≤0 或 null 省略 |
| 替代方案期数 | `alt_plan_scenario3.months` | 仅 C 场景输出；null 时整行省略 |
| 替代方案每期 | `alt_plan_scenario3.per_month` | §0.1 格式 |

## 上下文行（固定文案，套 §0.5 骨架 `---`×44 分隔线后）

```
这是演示，不影响真实账户（干跑不落账目、不入冷静期队列、不写审计）；
现在可以说「审查：买X花Y」开始真实审批。
```

> ⚠️ 字段路径说明：demo 与 judge 为**不同命令、输出 schema 不同**，路径自然不同——demo 在输出中包了一层 `engine_params` + `scenarios[]`，故用 `engine_params.cooldown_threshold` / `scenarios[i].cooldown_days`；judge 直接用 `cooldown.threshold` / `cooldown.days`。**此差异是设计使然，非 bug；渲染时以当次命令实际输出的 JSON 键为准，勿跨命令套用。**
