# rendering — 统一输出渲染指南

> 本文件是 LLM 把引擎 JSON 润色成用户可见文本的**唯一权威指南（格式唯一权威源）**。
> 模板（templates/）**仅作字段映射速查**（字段名 → JSON 路径），输出格式一律以本文件为准；本文件管「什么场景用什么模板 + 通用规则 + 骨架」。
> 全局参数（--data-dir / --today / JSON 输出）见 SKILL.md。

---

## 0. 通用规则（所有命令适用）

### 0.1 数字格式

| 场景 | 格式 | 示例 |
|---|---|---|
| 金额 | `¥` + 千分位逗号 + 2 位小数 | `¥200,000.00` |
| 月数 | 保留 1 位小数 + 「个月」 | `1.5 个月` |
| 百分比 | 保留 1 位小数 + `%` | `66.7%` |
| 比率 | 保留 2 位小数 | `0.50` |

> **禁止**向用户展示引擎输出的浮点原始值（如 `200000.0` / `1.663201663201663`）。
> 月数 < 0.1 时四舍五入到 `0.1`（不展示 0，避免「延后 0 个月」的噪声）。

### 0.2 误差披露（见 §1.4 长模板与 §2.1 撤回）

简化口径数字（`impact.delay_months_simple` / `feedback.ahead_months_simple`）**必须**用「约/大约/估算」措辞，并附误差说明：
- 首次出现：`延后约 {n} 个月（简化口径，误差 ±20%~50%）`
- 后续提及：`约 {n} 个月` 即可
- 真实口径（`delay_months_real` / `ahead_months_real`）：`真实口径约 {n} 个月（含通胀/回撤）`

### 0.3 性质声明

涉及「信托/资产保护/法律」话题时，明确声明：**本工具为个人自律记账工具，无法律效力**（§0）。
日常审批/报表不需要每次重复声明。

### 0.4 多币种渲染

**符号来源**：取 `inputs.base_currency`（或 contract.currency）→ 查 CURRENCY_SYMBOLS 映射。
CNY→¥ / USD→$ / EUR→€ / GBP→£ / HKD→HK$ / JPY→¥ / SGD→S$ / AUD→A$ / CAD→C$。未知币种用 code 本身。

**外币消费（original_currency ≠ null）**：金额行双显——原始 + 换算后：

```text
· 消费金额：$200.00 USD（汇率 7.25 → ¥1,450.00 CNY）
```

- `inputs.original_amount` / `inputs.original_currency` / `inputs.exchange_rate` 有值时才双显
- CNY 原生消费（`original_amount=null`）：单显基准币种金额，不画蛇添足
- 审计日志/冷静期提醒中外币条目同样双显：`$200.00 USD (→¥1,450.00)`
- 汇率保留 2 位小数 + `→` 箭头表示换算方向

### 0.6 引擎错误渲染

| 退出码 | error 值 | 用户提示 | 处理建议 |
|---|---|---|---|
| 2 | `not_found` | 「未找到契约数据，请先初始化（记账初始化）」 | 引导 init |
| 3 | `guard` | 「操作被安全护栏拦截：{message}」 | 转述 message，引导合规路径 |
| 4 | `invalid` | 「参数有误：{message}」 | 转述 message，引导修正 |
| 1 | `import_pending` | 「资产待核对，禁止审批；请先完成人工核对确认」 | 引导 import-asset --confirm |
| 1 | `exists` | 「契约已存在，不可重复初始化；如需重建请走『记账重置』」 | 引导 reset |
| 1 | `invalid_transition` | 「{message}」 | 转述 message，引导正确操作 |
| 1 | `request_not_found` | 「未找到该申请，可能已终裁或撤回」 | 引导查 reminders 或 log |
| 1 | `not_due` | 「该申请尚未到期，请到期后再终裁」 | 展示 expire_at |
| 1 | `already_expired` | 「该申请已过期，请走到期终裁」 | 引导 expire |
| 1 | `missing_rate` | 「{message}」 | 引导提供 `--rate`（如 USD→CNY 7.25） |
| 1 | `override_not_open` | 「尚未达到人工覆写条件（须连续 3 次申诉被驳）」 | 引导继续申诉或接受判定 |
| 1 | `cushion_violation` | 「奖励支取击穿安全垫，规则引擎拒付」 | 引导缩减金额或等里程碑 |

> **统一原则**：错误时只转述 `message` 字段 + 给出下一步建议，**不暴露** JSON 原文、不暴露退出码数字。

---

### 0.7 引擎消息串语言约定（杜绝复发）

> 引擎模块（`scripts/modules/*.py`）在构建 `message`/`note`/`warning`/`summary` 等面向用户的字符串时，必须遵守：

1. **全中文**：所有用户可见串为中文，不混用英文。
2. **禁露字段名/枚举值**：不得将 `corpus_status` / `imported_pending` / `imported_confirmed` / `monthly_history` / `invest_ratio` / `override_log` / `safety_cushion` 等字段名或枚举常量直接暴露给用户；如需引用内部状态，翻译为中文等价描述（如 `imported_pending`→「待核对」、`manual`→「手动录入」）。
3. **键值映射**：若 message/note 需要引用合约字段的当前值（如 `corpus_status` 还原值），代码内应对枚举值做中文映射后再拼接，不得把原始英文字符串直吐给渲染层。
4. **渲染层统一映射**：`render/renderer.py` 与任何拼接状态值的模块，一律走 `core.i18n.zh_status(value)`——它是覆盖全部状态族（RequestStatus / ObjectiveStatus / corpus_status / **SpendStatus** / **ConfigChangeStatus** / **RewardStatus**）的 union 映射，映射不到回退原值。新增状态族须在 `i18n.py` 并入 `STATUS_ZH`，并补 `test_i18n.py::test_status_zh_covers_all_families` 覆盖断言，确保渲染层不漏接。奖励状态经 `RewardStatus`（locked/unlockable/unlocked/exhausted）由 `modules/reward.py` 产出 `reward_status` 字段；资产导入状态复用 `corpus_status`（imported_pending/imported_confirmed/manual）由 `modules/import_asset.py` 产出 `import_status` 字段——两者渲染层一律 `zh_status()` 中文化。

> rendering.md 是输出格式**唯一权威源**，本约定与 §0.6 同级——引擎产出的 message/note 是用户最终看到的文本，必须全量中文化，无豁免。

---

### 0.5 全局输出骨架（所有命令统一，无一例外）

所有用户可见回执（含审批/撤回/终裁/提醒/初始化/报表/校准/奖励/申诉/覆写/自定义/对账/重置/导入/demo/错误提示/目标归档）**统一套用**以下骨架：

```text
============================================
{prefix}{命令标签}·{结果词} 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
{命令专属正文，逐行}
--------------------------------------------
{上下文行：按需}
```

- `{prefix}`：命令语义前缀 emoji，**保留不删**，授权集（超纲即违规）：✅ 成功 / 📊 数据 / ⏰ 时效 / 📋 流程 / ⚠️ 警示 / 🏆 奖励。驳回结论词用 `❌`（`❌审批·驳回`），不计入命令前缀集，但允许出现在标题行。
- 时间戳置于行尾：` 🕐[YYYY-MM-DD HH:MM GMT+8]`。
- 代码块统一用 ` ```text` 包裹全文输出。
- **分隔线规则（唯一，无歧义，严禁偏离）**：
  - 顶部、标题下：纯 ASCII `=` × 44（不用 `─`/框侧线 ┌│└，规避编码风险）；
  - 正文 ↔ 上下文行之间：纯 ASCII `---` × 44（是 `-` 不是 `=`，用来区分「正文块」与「上下文行」）；
  - **卡片最末行之后严禁任何分隔线**（尾部无 `=`、无 `---`；`=` 只在顶部与标题下各一次）。
- 上下文行（如「〔今日〕已批 N 笔 …」）仅消费类命令附，置于 `---`×44 分隔线之后（即正文块与上下文行之间）。
- 金额遵循 §0.1（¥ + 千分位 + 2 位小数）。
- 命令专属正文内容由各节（§1~§11）定义，本骨架只定外层结构；各节示例均已按此套写。
- **字段缺失降级（引擎未产出时，严禁把 `null`/字段名/内部注记暴露给用户）**：
  - `expire_at` / `request_id` 通常非 null（judge 真实产出 request_id 与 expire_at），仅异常为 null 时冷却期行降级为「冷静期 {days} 天，到期终裁（§2.3）」，**不显编号**（编号属内部队列标识，用户无需见）；
  - `alt_plan` 为 null → 替代方案行降级为「（暂无自动替代方案，可自行分期：单笔不超冷静期阈值、不击穿安全垫）」；
  - demo 命令的 `alt_plan_scenario3` 非空时，替代方案填其 `months` / `per_month`（演示三场景场景 C 即 18 期 / ¥2,333.33），不适用上述 null 降级；
  - 任一字段缺失均不得写成「引擎未生成 xxx」「返回 null」等调试语。

---

## 1. 审批提交（judge --action submit）

### 1.1 模板选择（决定结果词与正文）

```text
decision.scene
├─ "A" + cooldown.triggered=false + whitelist.fast_track=false → 紧凑卡片 A-1（§11）
├─ "A" + cooldown.triggered=false + whitelist.fast_track=true  → 紧凑卡片 A-3（§11）
├─ "A" + cooldown.triggered=true                               → 长模板 A-2（§1.4）
├─ "B"                                                         → 长模板 B（§1.4）
└─ "C" + inputs.financed=true                                  → 长模板 C-融资购房（§1.4）
   "C" + inputs.financed=false                                 → 长模板 C（§1.4）
```

### 1.2 字段选择（show vs omit）

**展示**：`decision` / `cooldown` / `inputs.amount` / `inputs.category` / `inputs.planned` / `inputs.corpus` / `inputs.remaining_after` / `inputs.effective_cushion` / `impact.delay_months_simple` / `impacted_objectives[0].name`（有冷静期时 `request_id` / `expire_at`）

**省略**（内部变量，不向用户展示）：
- `inputs.liabilities_sum` / `inputs.monthly_payment_sum` / `inputs.rigid_monthly`（已在 corpus 中体现）
- `inputs.monthly_invest_real` / `inputs.inflation`（内部测算参数）
- `inputs.invest_ratio`（配置参数，非审批结果）
- `optimization_applied.*`（调度内部变量，除非用户问「为什么判定收紧了」）
- `formulas_used`（公式编号）
- `stub` / `mode_transition_hint`（后者非 null 时追加为提示行）

### 1.3 特殊场景

- **融资购房**（`inputs.financed=true`）：展示首付/贷款/月供三件套，判定看首付是否击穿垫 + 月供是否可覆盖
- **impacted_objectives 为空数组**：省略目标影响行（小额支出不拖累目标时常见）
- **rebalance_override 非 null**：在正文末追加「⚠️ 本月校准临时调整已生效，审批门槛/投资比例有临时偏移」

### 1.4 长模板（A-2 / B / C）套骨架示例

```text
============================================
📋审批·附条件 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
契约对照：{decision.summary 中的契约条款}
目标影响：{impacted_objectives[0].name} 延后约 {impact.delay_months_simple} 个月（简化口径，误差 ±20%~50%）
替代方案：{decision.summary 中的替代方案}
冷静期 {days} 天，到期 {expire_at}（编号 {request_id}）（若 `expire_at` / `request_id` 异常为 null，按 §0.5 字段缺失降级规则降级为「冷静期 {days} 天，到期终裁（§2.3）」且不显编号）
```

> C（驳回）强制三段式：契约对照 → 目标影响 → 替代方案；附冷静期与 request_id。

### 1.5 毛口径提示行（inputs.monthly_basis）

`inputs.monthly_basis` 由引擎产出：`gross_estimate`（毛口径待校准，未录负债/刚性）或 `net`（净口径）。

- 当 `monthly_basis == "gross_estimate"` 且本笔判定为 **B（附条件）/ C（驳回）** 或触发冷静期时，在卡片正文追加一行：
  `⚠️ 月净流入为毛口径估算，安全垫/基线偏高（说『记账自定义·补负债』或『补刚性』即净口径化）`
- 小额直批（场景 A 且无冷静期）**不**附此行，避免刷屏（分叉 1：仅大额场景/首笔提示）。
- 该提示只说明口径风险，**不改变任何判定结论**（decision 仍原样引用）。
- `inputs.monthly_net_effective` 为展示用净口径分解（仅展示，不进判定），一般不在 judge 卡片单列；如需说明净口径可引用其 `net` 值。

---

## 2. 冷静期生命周期（judge --action withdraw/finalize/expire/reminders）

### 2.1 撤回（withdraw）

字段来源：返回的 `feedback.*` 对象（**不是** submit 的 `inputs.*`）。

```text
============================================
✅撤回·已撤回 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
申请 {request_id}（{category} {amount}）已撤回
即时回馈：相当于 {feedback.objective} 目标提前约 {feedback.ahead_months_simple} 个月
· 估算非承诺：基于简化口径，误差 ±20%~50%
· 钱留在账上，冷静期自动解除
```

- `feedback.objective` 为 null 时改为「你的长期目标」。
- `feedback.ahead_months_real` 非 null 时追加真实口径行。
- 必须转述 `feedback.estimation_note`（估算非承诺）。

### 2.2 确认执行（finalize）

```text
============================================
✅终裁确认·已执行 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
申请 {request_id} 按「{decision.result}」终裁执行
{decision.summary}
```

> 简短即可——用户主动确认，不需要重复全部数字。

### 2.3 到期终裁（expire）

```text
============================================
⏰到期终裁·已处理 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· {processed[0].category} ¥{processed[0].amount} → {processed[0].final_status}（{processed[0].decision.result}）
· ...
```

> `processed` 为空数组时：`⏰ 🕐[YYYY-MM-DD HH:MM GMT+8] 到期终裁·已处理` + 正文「✅ 无到期申请待终裁」。

### 2.4 提醒（reminders）

```text
============================================
⏰冷静期提醒·查询 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· {reminders[0].kind=expiring?⚠️ 即将到期:⏳ 冷静中}：{reminders[0].category} ¥{reminders[0].amount}
  剩余 {reminders[0].days_left} 天（到期 {reminders[0].expire_at}）编号 {reminders[0].request_id}
· ...
```

> `reminders` 为空数组时：正文「✅ 无冷静期挂起申请」。
> `kind=expiring`（≤1天）用 ⚠️ 并建议「确认执行或撤回」；`kind=cooling` 用 ⏳ 常规提醒。

---

## 3. 初始化（init）

```text
============================================
✅记账初始化·已生成 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
资金池 {symbol}{corpus} {currency}·月度净流入（{monthly_basis}）{symbol}{monthly_contribution} {currency}
目标：{objectives[0].name}（{symbol}{target_amount}，{deadline}）...
⚠️ {warnings 逐条}
· 已生成默认契约，可随时说『自定义』逐项调
```

- `currency` 非 CNY：金额用对应符号（USD→$ / EUR→€ / HKD→HK$ 等）；CNY 默认用 ¥ 不标币种名。
- `monthly_basis`：`gross_estimate`（毛口径待校准）/ `net`（净口径）。为 `gross_estimate` 时月度净流入后附 `〔毛口径·待校准〕` 标记。
- `warnings` 非空逐条转述（⚠️ 前缀）；`rejected_objectives` 非空转述被拒原因；`demo` 非空按 demo 渲染。

---

## 4. 演示（demo）

### 4.1 双模式警告（`demo_defaults_used` 决定）

| 条件 | 警告行 | 含义 |
|---|---|---|
| `demo_defaults_used=true` | `⚠️ 演示数据（场景为合成，基于默认参数），非真实审批` | 纯合成数据，无真实契约 |
| `demo_defaults_used=false` | `⚠️ 演示数据（场景为合成，基于你真实契约：资金池 ¥{corpus} / 月净流入 ¥{monthly}），非真实审批` | 场景仍合成，但用真实契约参数测算 |

> **关键区分**：`demo_defaults_used=false` 时必须从 `engine_params.corpus` / `engine_params.monthly_contribution` 原样引用资金池与月净流入（禁止心算），让用户明确知道演示基于自己的真实参数。

### 4.2 场景列表格式

```text
============================================
✅演示·已生成 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
{4.1 警告行}
· 场景A {name} ¥{amount} → 批准（无冷静期）[· 目标延后约 {n} 个月（简化口径）]
· 场景B {name} ¥{amount} → 批准（触发 {days} 天冷静期）[· 目标延后约 {n} 个月]
· 场景C {name} ¥{amount} → 驳回（冷却）[· 目标延后约 {n} 个月]
  · 替代方案：{months} 期 / 每期 ¥{per_month}（单笔不超冷静期阈值、不击穿安全垫）
--------------------------------------------
这是演示，不影响真实账户（干跑不落账目、不入冷静期队列、不写审计）；
现在可以说「审查：买X花Y」开始真实审批。
```

- 金额 `{amount}` 取自 `scenarios[].amount`（原样引用 §0.1 格式）。
- 目标延后 `{n}` 取自 `scenarios[].delay_months_simple`（有值且 >0 时附注；=0 或 null 时省略）。
- 替代方案仅场景 C 输出，取自顶层 `alt_plan_scenario3.months` / `.per_month`（null 时整行省略，不降级为文字）。
- **上下文行**置于 `---`×44 分隔线之后（套 §0.5 骨架）。

---

## 5. 报表（report）

```text
============================================
📊报表·已生成 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· 资金池 ¥{corpus}·净资产 ¥{net_assets}
· 安全垫余量 ¥{cushion_margin}
· {objectives[].name} 达成 {achieved_ratio}%·{color}（时间轴应达 {time_progress}%）
· 本月净流入 ¥{monthly_net}{monthly_basis?〔毛口径·待校准〕}（进度平稳）
· 安全垫预警：{cushion_alert?⚠️ 告警:余量充足，无预警}
（monthly_basis=net 时追加净口径分解行：
· 月净流入（净）¥{monthly_net_effective.net}（录入 ¥{monthly_net_effective.entered} − 负债月供 ¥{monthly_net_effective.debt_monthly} − 刚性月摊 ¥{monthly_net_effective.rigid_monthly}））
{pending_cooling 为空?（本段整段省略）:
· 冷静期挂起（{pending_cooling.length} 笔）：
  · {pending_cooling[0].category} ¥{pending_cooling[0].amount} 待决
    到期 {pending_cooling[0].expire_at}（编号 {pending_cooling[0].request_id}）}
（notes[] 逐条转述）
```

- `notes[]` 必须**逐条转述**，不可省略。
- `cushion_alert=true` 时红色预警。
- `pending_cooling` 为空时整段省略。
- `monthly_basis`：`gross_estimate`（毛口径待校准）/ `net`（净口径）。为 `gross_estimate` 时月度净流入行附 `〔毛口径·待校准〕` 标记，且 `notes[]` 中会含毛口径提示（引擎产出，逐条转述即可，不另起独立行）。
- `monthly_basis=net` 时追加净口径分解行：`net = entered − debt_monthly − rigid_monthly`，**仅作展示，不进判定**（F0/F1/F2/judge 仍用原始 `monthly_contribution`）；`debt_monthly` / `rigid_monthly` 为 0 时该行数值平凡但仍输出。

---

## 6. 校准（calibrate）

```text
============================================
📊月度校准·已生效 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· {changes.length>0?以下调整已生效:✅ 无需调整，目标进度正常}
· {changes[0].description}
· ...
（rebalance_override 非空：· 仅本月有效，原始权重不变）
```

- `skipped=true`：结果词改「已跳过」，正文「✅ 本月已校准过（同月幂等），--force 可强制重跑」。
- changes 中具体数字**原样引用**，禁止心算。

---

## 7. 奖励（reward）

### status

```text
============================================
🏆奖励状态·查询 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· {objectives[0].name}：达成率 {achieved_ratio}% {reward_unlocked?已解锁:未解锁}
  {reward_quota>0?可支取 ¥{reward_quota}:暂无可支取额度}
· ...
```

### unlock

```text
============================================
🏆奖励解锁·已解锁 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· {objectives[0].name} 达成 {achieved_ratio}%（≥120%）→ 解锁奖励额度 ¥{reward_quota}
```

- 无新解锁：正文「✅ 暂无新解锁的奖励（达成率 ≥120% 时自动解锁）」。

### claim

```text
============================================
✅奖励支取·已执行 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
{objective} ¥{amount}（{purpose}）
· 剩余额度 ¥{remaining_quota}
```

- `error=cushion_violation` 时按 §0.6 错误提示渲染。

---

## 8. 审计日志（log）

```text
============================================
📋审计日志·{log} 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
共 {count} 条，展示最近 {min(10,count)} 条：
· [{records[0].time}] {records[0].event??:records[0].scene} ¥{records[0].amount} {records[0].category}
· ...
```

> 默认只展示最近 10 条，告知总数；用户要求看全部时再全量展示。

---

## 9. 申诉/覆写（appeal）

### 申诉

```text
============================================
📋申诉·{upheld?维持:改判} 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
{decision.summary}
· 申诉计数 {appeal_count}/3 {override_open?→ 已开放人工覆写入口:}
```

- `override_open=true` 追加：「你已连续 3 次申诉被驳，可走人工覆写（须确知目标延后影响）」。

### 覆写（第一步无 --confirm）

```text
============================================
⚠️人工覆写·预览 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· 目标影响：延后约 {target_impact.delay_months_simple} 个月（简化口径，误差 ±20%~50%）
· 真实口径约 {target_impact.delay_months_real} 个月
· 确认知悉后回复「确认覆写」执行
```

### 覆写（第二步 --confirm）

```text
============================================
✅人工覆写·已执行 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
申请 {request_id} 放行
· 目标延后影响已记录（约 {target_impact.delay_months_simple} 个月）
· 已落 override_log
```

---

## 10. 自定义/对账/重置/导入

### 自定义预览（无 --confirm）

```text
============================================
📋修改预览·待确认 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· {changes[0].field}: {changes[0].from} → {changes[0].to}
  后果：{changes[0].consequence}
· 确认令牌 {token}（回复「确认修改」+ 令牌生效）
{cooldown_window?· ⚠️ 削弱型修改，确认后进入 {cooldown_days} 天冷静窗，窗内可无理由撤回:}
```

### 自定义确认（--confirm + --token）

```text
============================================
✅修改生效·已生效 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
{changes_summary}
{cooldown_window?· 进入 {cooldown_days} 天冷静窗（编号 {request_id}），窗内可「记账自定义·撤回」:}
```

### 对账（reconcile）

```text
============================================
📊对账·已完成 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
{changes.corpus?· 资金池 ¥{changes.corpus.from} → ¥{changes.corpus.to}（差额 ¥{changes.corpus.diff}）:}
{pending_spends_cleared?· 清销已批支出 {pending_spends_cleared.count} 笔（合计 ¥{pending_spends_cleared.total}）:}
· 下次对账提醒：{next_reconcile_date}
```

### 重置预览（无 --confirm）

```text
============================================
⚠️重置警告·待确认 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· 将重建整个契约（审计日志保留）
· 旧契约 sha256: {old_contract_sha256}
· 确认后须提供新契约参数（资金池/月度流入/目标）
```

### 重置确认（--confirm）

```text
============================================
✅重置·已生效 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· 旧契约 sha256: {old_contract_sha256}（已归档）
· 新契约回执：（按 §3 init 渲染）
```

### 导入暂存

```text
============================================
📋资产导入·待核对 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· 总资产 ¥{summary.total_assets}
· 负债 {summary.liabilities_count} 项 / 刚性支出 {summary.rigid_count} 项
{suspicious.length>0?· ⚠️ 可疑流水 {suspicious.length} 条，请核对:· 无可疑流水}
· 确认令牌 {token}
· 核对后回复「确认导入」+ 令牌生效；或「取消导入」放弃
· ⚠️ 导入待核对状态将锁定全部审批
```

### 导入确认

```text
============================================
✅资产导入·已生效 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· {applied.summary}
· 审批已解锁
```

### 导入取消

```text
============================================
✅资产导入·已取消 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
资产状态已还原
```

### 目标完结/归档（objective --to completed/archived）

```text
============================================
✅目标·已归档 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
· {name} 已达成 {achieved_ratio}%，归档至历史目标
· 后续资金可重新分配
```
---

## 11. 审批紧凑卡片（judge submit A-1/A-3 轻量回执）

> 适用：场景 A-1 / A-3 小额直批、计划内/外均适用；连续高频审批时优先用此卡片，替代 §1.4 长模板。
> B（附条件）/ C（驳回）**不**走此卡片，仍用 §1.4 三段式长模板（同样套 §0.5 骨架）。

### 11.1 格式（套 §0.5 骨架）

```text
============================================
✅审批·批准 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
¥{amount} {category}
安全垫 ¥{effective_cushion} 之上 · FIRE 不受损
账本 ¥{corpus} → ¥{remaining_after}
--------------------------------------------
〔今日〕已批 {n} 笔 / ¥{today_total} / 安全垫余量 ¥{margin}
```

非空示例（场景2 手机 ¥6,000，FIRE 延后；A-2 附条件 + 冷却期行同卡）：
```text
============================================
📋审批·附条件 🕐[YYYY-MM-DD HH:MM GMT+8]
============================================
¥6,000.00 合理享受
安全垫 ¥24,000.00 之上 · FIRE 约 1.5 个月（简化口径，误差 ±20%~50%）
账本 ¥50,000.00 → ¥44,000.00
冷静期 3 天，到期 2026-08-01T00:00:00（编号 6f3bdd97b623）
--------------------------------------------
〔今日〕已批 1 笔 / ¥6,000.00 / 安全垫余量 ¥18,000.00
```

### 11.2 字段规则

| 行 | 来源 |
|---|---|
| 头 | `✅审批·批准 🕐[YYYY-MM-DD HH:MM GMT+8]`（结论词=批准/附条件/驳回；**不**重复场景字母 A/B/C） |
| 消费行 | `¥{amount} {category}`（金额格式遵循 §0.1：¥ + 千分位 + 2 位小数） |
| 判定行 | impacted_objectives 为空：`安全垫 ¥{effective_cushion} 之上 · FIRE 不受损`；非空：`安全垫 ¥{effective_cushion} 之上 · {name}约{delay_months_simple}个月（简化口径，误差 ±20%~50%）`（多目标用 `、` 连 `{name}约{n}月`；任一 material_lag=true 前缀 ⚠️） |
| 账本行 | `账本 ¥{corpus} → ¥{remaining_after}` |
| 框外累计 | `〔今日〕已批 {n} 笔 / ¥{today_total} / 安全垫余量 ¥{margin}`（margin = remaining_after − (corpus − effective_cushion)） |

### 11.3 约束

- 时间戳 ` 🕐[YYYY-MM-DD HH:MM GMT+8]`
- 金额**合规** ¥ 格式（§0.1），不豁免千分位/小数。
- 分隔线：顶部/标题下 `=` × 44、正文↔上下文行 `---` × 44（套 §0.5，不用 `─`/侧框，尾部严禁 `=`）。
- 无冷静期（A-1/A-3）不输出冷静期行；A-2（有冷却）在判定行后追加「冷静期 {days} 天，到期 {expire_at}（编号 {request_id}）」即可。**若 `expire_at` / `request_id` 为 null，按 §0.5 字段缺失降级规则处理**——降级为「冷静期 {days} 天，到期终裁（§2.3）」且**不显编号**（编号属内部队列标识，用户无需见），严禁把 `null`/字段名/调试语暴露给用户。
- 多币种（§0.4）：消费行改双显 `$45.00 USD（汇率 7.10 → ¥319.50 CNY）`，其余行仍用基准币种 ¥。
- 此卡片与 §1.4 opinion 长模板并存：用户未指定时，**小额直批默认用本卡片**；涉及冷静期/白名单/融资购房等需展开说明时回退长模板。

---

## 附：全命令输出渲染速查

| 命令 | 模板 | 核心展示字段 | 省略字段 |
|---|---|---|---|
| judge submit A-1 / A-3 | §11 紧凑卡片 | amount/effective_cushion/remaining_after | formulas/optimization/内部变量 |
| judge submit A-2 | §1.4 长模板 | +cooldown/request_id/impact | 同上 |
| judge submit B | §1.4 长模板 | +alt_months/alt_per_month | 同上 |
| judge submit C | §1.4 长模板 | +替代方案/差额 | 同上 |
| judge withdraw | §2.1 | feedback.* | — |
| judge finalize | §2.2 | request_id/decision | — |
| judge expire | §2.3 | processed[] | — |
| judge reminders | §2.4 | reminders[] | — |
| report | §5 | 全五段 | formulas/ref/stub/snapshot内部 |
| init | §3 | corpus/monthly/objectives | — |
| demo | §4 | 三场景 | — |
| calibrate | §6 | changes[] | formulas |
| reward status | §7 | achieved_ratio/reward_quota | — |
| reward unlock | §7 | reward_quota | — |
| reward claim | §7 | amount/remaining | — |
| log | §8 | records[]（最近10条） | — |
| appeal | §9 | upheld/decision/appeal_count | — |
| customize 预览 | §10 | changes[]/token | — |
| customize 确认 | §10 | changes_summary | — |
| reconcile | §10 | changes/pending_spends_cleared | — |
| reset 预览 | §10 | old_contract_sha256 | — |
| reset 确认 | §10 | +init回执 | — |
| import-asset 暂存 | §10 | summary/suspicious/token | — |
| import-asset 确认 | §10 | applied | — |
| import-asset 取消 | §10 | — | — |
| objective 归档 | §10 | achieved_ratio | — |
| 错误提示（12类） | §0.6 表 + §0.5 骨架 | message + 引导 | JSON/退出码 |

> 所有条目均套 §0.5 全局骨架：`{prefix}[时间戳] {命令}·{结果词}` + `=`×44 + 正文 + 上下文行。
