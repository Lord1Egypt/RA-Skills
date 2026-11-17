# tasks/ 固定调用指令模板（run_task_file 执行）

> 每个 JSON 含 `tool_name` + 参数，用 `run_task_file(task_file="<绝对路径>")` 执行。
> 依赖图层状态：**回测类自带建图层**；分组/平移类依赖已存在的图层。

## 回测类（strategy_backtest，自带建图层）

| 文件 | 说明 |
|------|------|
| `backtest_summary.json` | summary 成绩单 → 回测图层（股票级，权重=个股总收益） |
| `backtest_detail.json` | detail 个股 7 标量 → `scripts/detail_ic_analysis.py` 横截面归因 |
| `backtest_segments.json` | segments 持仓片段（权重=卖价除买价、X=时间）→ 入场因子归因 |
| `backtest_timeline.json` | timeline 每日时序 → `scripts/timeline_analysis.py` 深度分析 |

## 分组类（依赖回测图层或 segments 图层）

| 文件 | 说明 |
|------|------|
| `group_industry.json` | 行业分组（group_by_attrs, k=1.0） |
| `group_mcap.json` | 起始市值十分档（group_by_code, 代码已含 row_rank） |
| `group_exchange.json` | 交易所分组（group_by_attrs, k=1.0） |
| `group_time.json` | ⚠️ 时间分组——**run_task_file 白名单缺 group_by_time，须直接 MCP 调用**；仅 segments/买点图层可用 |

## 平移类（依赖 segments 图层）

| 文件 | 说明 |
|------|------|
| `move_factor_y.json` | 单因子 Y 轴排序平移（ANOM_SKEW 范本；to_percentile=true + optimized_display=true） |
| `move_combo_score.json` | 5 因子组合连续排序值 Y 轴（高分位=优质买点） |
| `move_combo_boolean.json` | 5 因子各自前 30% 交集布尔 Y 轴（1=被筛出） |

## 换策略/换因子

只改 JSON 里的 `code` 字段即可（金叉为默认范本）。`group_by_attrs` 必须 `k=1.0`（`k=null` 会塌缩成单桶，引擎 bug）。
