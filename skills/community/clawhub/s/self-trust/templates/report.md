# 记账报表 — 字段速查（templates/report.md）

> ⚠️ **本文件仅作字段映射速查 + 渲染决策逻辑。**
> 输出**格式一律以 `references/rendering.md` §5 为准**（套 §0.5 骨架，数字 §0.1）。
> 旧格式示例（§0.5 标准化前，含被禁 `─` 字符）已全部移除，禁止照抄。

---

## 渲染决策树（决定展示哪些段，格式套 rendering.md §5）

- `cushion_alert=true` → 头部追加红色预警：`⚠️ 安全垫余量不足 1 个月生活费，请控制支出`
- `objectives[]` → 逐行引用 `objectives[].ascii`（引擎已拼好进度条+达成率+时间轴+颜色，不自绘）；颜色：绿=超前 / 黄=落后 / 红=lag≥10% 严重落后；无 deadline 目标只展示攒钱占比
- `ascii` 含趋势图 → 展示；含「暂无月度快照」→ 如实转述，不虚构；`snapshot_appended` 非空追加「本月首报已自动落一条月度快照」
- `pending_cooling` 非空 → 逐笔列出（融资购房申请追加首付/月供信息）；**空数组整段省略**
- `notes` 非空 → **逐条转述**，不可省略；空数组整段省略
- `mode_transition_hint` 非空 → 追加为最后一条提示
- `rebalance_override` 非空 → 追加「⚠️ 本月校准临时调整已生效（仅本月有效，原始权重不变）」
- `monthly_basis=gross_estimate` → 月度净流入行附 `〔毛口径·待校准〕` 标记；`notes[]` 已含毛口径提示，逐条转述即可
- `monthly_basis=net` → 追加净口径分解行（net = entered − debt_monthly − rigid_monthly），**仅展示不进判定**

## 省略清单（以下字段不向用户展示）

| 字段 | 原因 |
|---|---|
| `formulas_used` | 内部公式编号，用户无需 |
| `ref` | 文档章节引用，内部用 |
| `stub` | 引擎标记，内部用 |
| `snapshot_appended` 内部字段 | 仅告知「已落快照」即可，income/invest 等为 null 不虚构 |
| `objectives[]` 内部字段（weight/lag_streak 等） | 已在 ascii 中呈现，不重复 |

## JSON 字段速查表

| 占位符 | JSON 路径 | 说明 |
|---|---|---|
| `{date}` | `date` | 报表日期 |
| `{mode}` | `mode` | 数据模式 |
| `{corpus}` | `corpus` | 资金池余额 |
| `{net_assets}` | `net_assets` | 净资产 |
| `{monthly_net}` | `monthly_net` | 月度净流入 |
| `{living_baseline}` | `living_baseline` | 生活费基线 |
| `{effective_cushion}` | `effective_cushion` | 安全垫 |
| `{cushion_margin}` | `cushion_margin` | 垫上余量 |
| `{cushion_alert}` | `cushion_alert` | 余量<1月生活费→true |
| `{objectives[].ascii}` | `objectives[].ascii` | 逐目标进度条（已拼好） |
| `{ascii}` | `ascii` | 完整 ASCII（进度条+趋势图） |
| `{pending_cooling[]}` | `pending_cooling[]` | 冷静期挂起列表 |
| `{notes[]}` | `notes[]` | 备注数组（必须逐条转述） |
| `{rebalance_override}` | `rebalance_override` | 校准临时层（非null时提示） |
| `{mode_transition_hint}` | `mode_transition_hint` | 模式切换建议（非null时提示） |
| `{snapshot_appended}` | `snapshot_appended` | 当月首报快照（非null时提示） |
| `{monthly_basis}` | `monthly_basis` | 毛口径/净口径标记：`gross_estimate` / `net` |
| `{monthly_net_effective.net}` | `monthly_net_effective.net` | 净口径分解-净（**展示用，不进判定**） |
| `{monthly_net_effective.entered}` | `monthly_net_effective.entered` | 净口径分解-录入值 |
| `{monthly_net_effective.debt_monthly}` | `monthly_net_effective.debt_monthly` | 净口径分解-负债月供 |
| `{monthly_net_effective.rigid_monthly}` | `monthly_net_effective.rigid_monthly` | 净口径分解-刚性月摊 |
