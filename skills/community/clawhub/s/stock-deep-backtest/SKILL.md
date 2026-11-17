---
name: stock-deep-backtest
description: >
  股票深度回测（Stock Deep Backtest）技能 —— 基于 QuantAll（全A解析）MCP，
  对"已回测的策略"做深度诊断：策略为什么有效/失效、最终在哪儿赚钱、能否用入场因子筛选改善。
  三层能力：① 四个回测视角（summary 成绩单 / detail 横截面 / segments 持仓片段 / timeline 时序净值）；
  ② 原生分组（行业/市值/交易所/时间 + 热力图）；③ 因子筛选改善（单/双/多因子 → 片段收益对比）。
  固定调用指令已固化为 tasks/*.json，run_task_file 可直接执行；深度分析由 scripts/ 脚本完成；
  一键完整链路 run_full_attribution.py → make_report_html.py 出 HTML 报告（免责声明 + A/B 结构）。
  触发：策略归因/回测诊断/策略为什么有效或失效/分组回测/首尾分析/入场因子筛选/稳健性检验/参数敏感性
  /alpha 归因/因子暴露/回测复盘等深度评估关键词。
  不主动在"跑个回测看收益"需求中触发——那是 strategy_backtest 的事；本技能做"之后的深度诊断"。
agent_created: true
license: MIT
version: 0.0.0
status: 正式出版（由 backtest-attribution 草案 v0.5 整理出版：更名 stock-deep-backtest、
  固定调用固化为 tasks/*.json、脚本精选 8 个入 scripts/、旧文档与 POC 脚本归档 archive/）
---

# 股票深度回测（Stock Deep Backtest）· v0.0.0

> 回测之后的事：量化定位策略**为什么有效/失效、最终在哪儿赚钱、能否用入场因子筛选改善**。
> 依赖 QuantAll（全A解析）MCP；与 `strategy_backtest` 的分工：**它跑回测，本技能做诊断**。

---

## 1. 核心认知（先读）

1. **`strategy_backtest` 自带图层，评估回测时不要新建图层**（制作人确认）：
   - `view=summary` 图层 = 回测持仓（每只股票一个散点）、**权重自动 = 个股总收益** → 直接 `group_by_*` 分组即得"策略最终在哪类股票赚钱"。
   - `group_by_time` 在此图层**不适用**（回测曲线全部从同一时间起点绘制、无真实逐日坐标）；时间维度用 segments 图层或 `timeline_analysis.py`。
2. **两种图层口径**：回测图层（股票级，权重=个股总收益）回答"**在哪儿赚钱**"；买点图层（`new_layer_from_code(buy)` 重建，散点=买点）回答"**每个信号质量如何**"（此时三分组工具全可用）。
3. **segments 图层**（`view=segments`）：每个持仓片段一条曲线，**权重=片段收益**（引擎称"卖价除买价"）、**X 轴按时间平移**（等价 `get_time_id()`）、`group_by_time` 可用。核心用途：**入场因子归因**（move_by_code 设 X/Y=入场点因子值 → 看片段收益分位差异 → select 筛选改善）。
4. **排名口径铁律**：因子值筛选必须用**每日截面排名**（`sub.groupby("entry")["fv"].rank(pct=True)`），**禁用全局排名**（牛市时段全体同涨会虚增改善量、甚至反转方向，实测约 40% 虚增）。报告须双口径对照 + 附时间分布（筛选占比季度均值≈0.3 为均匀）。
5. **口径对照铁律**：summary（逐笔截面均值）与本地连续复利组合净值对事件驱动策略可能**符号相反**（D7）——报告结论前务必两口径对照，反转策略是"假有效"典型。
6. **矩阵方向**：`run_codes` 返回 time×stock（index=时间，columns=股票）；聚合跨股票用 `axis=1`，跨时间用 `axis=0`。

## 2. 触发边界

| 用户意图 | 用哪个 |
|------|------|
| 跑个策略看收益/夏普 | `strategy_backtest`（QuantAll 技能） |
| **诊断为什么有效/失效、归因、分组、测稳健性、首尾、入场因子筛选** | **本技能** |
| 批量评估因子 IC | `factor-catalog` / `batch_factor_analysis` |
| 多因子筛选去冗余 | `factor-prune` |

---

## 3. 固定调用指令（`tasks/*.json`，`run_task_file` 直接执行）

> 依赖图层状态：**回测类 JSON 自带建图层**；分组/平移类 JSON **依赖已存在的图层**（先跑对应回测 JSON）。

| JSON | 工具/用途 | 依赖 |
|------|----------|------|
| `backtest_summary.json` | 回测 summary（金叉范本）→ 建回测图层 | — |
| `backtest_detail.json` | 回测 detail（个股 7 标量 → 横截面归因） | — |
| `backtest_segments.json` | 回测 segments（持仓片段 → 入场因子归因） | — |
| `backtest_timeline.json` | 回测 timeline（每日时序 → 净值/择时） | — |
| `group_industry.json` | 行业分组（k=1.0） | 回测图层 |
| `group_mcap.json` | 起始市值十分档（代码已含 row_rank） | 回测图层 |
| `group_exchange.json` | 交易所分组 | 回测图层 |
| `group_time.json` | 时间分组（逐交易日） | **segments/买点图层**（回测图层不适用）；⚠️ 须**直接 MCP 调用**（run_task_file 白名单缺 `group_by_time`，见下） |
| `move_factor_y.json` | 单因子 Y 轴排序平移（ANOM_SKEW 范本，排序开启） | segments 图层 |
| `move_combo_score.json` | 5 因子组合连续排序值 Y 轴（高分位=优质买点） | segments 图层 |
| `move_combo_boolean.json` | 5 因子各自前 30% 交集布尔 Y 轴（1=被筛出） | segments 图层 |

**用法**：`run_task_file(task_file="<绝对路径>/tasks/backtest_summary.json")`。换策略/因子只需改 JSON 里的 `code` 字段。JSON 表达 None 用 `null`；`group_by_attrs` 必须传 `k=1.0`（`k=null` 会塌缩成单桶，引擎 bug，见 §7）。

**⚠️ run_task_file 白名单限制**：经实测，`run_task_file` 仅支持 tool_name ∈ {strategy_backtest, move_by_code, weight_by_code, select_by_code, new_layer_from_code, factor_analysis, heat_map, group_by_attrs, group_by_code, batch_weight, batch_select, batch_factor_analysis, batch_factor_corr, available_data, get_user_selection, execute_python_script}——**不含 `group_by_time`**。凡 group_time 的调用请直接 MCP 调用（已向制作人提 P2 补白名单）。已实测可用：summary/segments 回测、行业/市值/交易所分组、单因子与组合排序平移，全部经 run_task_file 验证通过（2026-08-30）。

---

## 4. 四个回测视角（能干嘛）

### 4.1 summary → 成绩单 + 回测图层直接分组（评估回测首选）
```
strategy_backtest(view="summary") → 图层=股票级散点、权重=个股总收益
→ group_industry.json / group_mcap.json / group_exchange.json（tasks）
```
- **已验证（金叉 MA5/20，5590 只）**：盈利比率 53.27%、年化均值 +9.99%、夏普 0.231；行业最好 玻璃 +209%/半导体 +87%，最差 白酒 −34%；市值档 1→10 收益倍数 1.43→1.20 **单调递减（强小盘暴露）**。
- **判读**：某组显著优 → 该风格是收益来源；小盘≫大盘 → 规模暴露；行业差异大 → 行业集中风险。

### 4.2 detail → 个股横截面归因（D8，`detail_ic_analysis.py`）
返回每只股票 7 个标量（总收益/年化/回撤/夏普/胜率/盈亏比/基准），**不是曲线**——当横截面标签向量做归因：收益分布画像 / 因子 IC（Pearson+Spearman）/ 行业分组 / 市值档 / 极端股 Top1%。
- **已验证（金叉）**：波动率 vol60 相关最强（spearman **+0.383**）= 高波动股赚更多；市值 −0.104（弱小盘）。
- **用法**：`python scripts/detail_ic_analysis.py [detail结果txt路径]`。

### 4.3 segments → 持仓片段 + 入场因子归因（D3 核心）
绘制每个持仓片段（权重=卖价除买价，X=时间）。分析路线（制作人早期构想，逐步实现）：
1. **单因子**：`move_factor_y.json`（或 x）排序开启（与 IC 同口径）；不考虑时间→x 方向，考虑时间→y 方向（X 保持时间）。
2. **双因子**：X=因子A、Y=因子B → 热力图交互矩阵。
3. **三因子**：X/Y 两因子 + `select_by_code(code="row_rank(<因子C>)>0.7")`。
4. **多因子**：`batch_select(code_dict={...}, mode="independent_summary"/"intersect"/"union")`。
- **批量精确归因**：`segment_screen_eval.py`（矩阵级，制作人指定算法：`cum.where(buy/sell)` + `bfill` 算买点片段收益；70s/50 因子）与 `segment_combo_eval.py`（双因子 intersect / rank 融合 / 多因子贪心叠加）。
- **已验证（金叉，全局片段收益 1.38%，截面排名口径）**：单因子改善最好 GTJA_Alpha70 +0.64pp；双因子 intersect 最优 +1.25pp；贪心 5 因子 +1.53pp（片段收益→2.91%）；**时间分布均匀（无聚集）**。

### 4.4 timeline → 时序净值 / 择时 / 选股能力（D4，`timeline_analysis.py`）
返回每日表（收益%/收益排序/持仓/买卖点数），引擎只绘制不支持分析——脚本本地重建：净值（连续复利年化/夏普/回撤）、收益排序分位（选股 alpha 代理）、择时检验（持仓比 vs 未来收益）、交易活跃度、时段分解、极端日画像。
- **已验证（金叉，450 日）**：连续复利年化 **+51.7%**（vs summary 逐笔 +9.99%，两口径差异巨大但方向一致）；排序分位 0.499≈0.5（**无选股 alpha**）；择时 r≈0（**不择时**）；2025Q3 贡献全期 78%（局部有效）。
- **用法**：`python scripts/timeline_analysis.py [MCP timeline 落盘txt]`。

---

## 5. 深度分析脚本（`scripts/`）

| 脚本 | 用途 |
|------|------|
| `run_full_attribution.py` | **一键完整链路**（矩阵片段收益→单因子双口径→双因子→贪心→JSON，~72s；`python run_full_attribution.py golden_cross|reversal|macd`） |
| `make_report_html.py` | HTML 报告渲染（**免责声明 + A/B 结构**：A=基础分析 summary/detail/timeline，B=因子筛选改善；`python make_report_html.py <策略名>`） |
| `timeline_analysis.py` | timeline 深度：净值重建/排序分位/择时检验/时段分解/极端日（§4.4） |
| `heatmap_eval.py` | 热力图统计评估（**分布感知**：均值/中位/胜率/截尾敏感性/时间分布/bootstrap 显著性——收益偏态长尾，不能只看均值） |
| `segment_screen_eval.py` | 矩阵级入场因子筛选改善评估（每日截面排名 + 时间分布，§4.3） |
| `segment_combo_eval.py` | 双因子/多因子组合筛选（intersect / rank 融合 / 贪心叠加，§4.3） |
| `detail_ic_analysis.py` | detail 横截面归因：分布画像/因子IC/行业/市值/极端股（§4.2） |
| `mcap_industry_cross.py` | 市值×行业二维交叉 pivot（最强/最弱组合 Top10） |

- 通用：`run_codes` 一次拉多矩阵（hold/ret/因子…）+ duckdb 读 `stock_basic`；日收益先 1%/99% 截尾防停牌缺口极端值；`scripts/factor-screen-final-50.xlsx` 为 50 个清洗因子参考库（name/code/IR）。
- **停牌限制**：矩阵算法（bfill）在片段中途停牌处会断裂拆段——全市场停牌率<2% 结果仍有借鉴；**严谨验证走全A解析 MCP**（引擎自动处理停牌）。

---

## 6. 诊断维度（D1~D8，每次诊断过一遍）

| 维度 | 内容 | 入口 |
|------|------|------|
| D1 分组 | 行业/市值/交易所 → 风格暴露 | 回测图层 + tasks 分组 JSON / mcap_industry_cross.py |
| D2 妖股 | 极端股对收益的贡献 | detail 极端股画像 / 截尾对比 |
| D3 入场因子 | 买点前因子能否筛选改善片段收益 | segments + move_factor_y.json / screen_eval / combo_eval |
| D4 时间 | 时段分解/局部有效 | timeline_analysis.py / group_time |
| D5 首尾 | 最好/最差 10% 段特征对照 | segments 排序 / poc2（archive） |
| D6 归因 | beta/alpha/因子暴露 | attribution_poc.py（archive） |
| D7 口径 | summary 逐笔 vs 连续复利是否一致 | timeline_analysis.py / strategy_compare.py（archive） |
| D8 横截面 IC | 个股收益 vs 因子 | detail_ic_analysis.py |

---

## 7. 关键坑（AI 必读）

1. **group_by_attrs 必须传 `k=1.0`**：`k=null` 会把分组轴塌缩成单桶（引擎 bug）；直接 MCP 与 run_task_file 行为一致。
2. **group_by_code 需代码末尾自行 `row_rank()`**（无参数控制）；`move_by_code` 用 `to_percentile=true` + `optimized_display=true`（绘图优化）。
3. **热力图细分上限 1 万**（X 细分数 × Y 细分数 ≤ 10000）；`group_by_time`(449 桶) 后叠多属性层级易超限，须在干净图层上跑。
4. **分组调用同轴互斥**：每次调用替换当前轴设置（不叠加）；X/Y 两轴独立可同时保留。
5. **大结果自动落盘**：group_by_time(449桶)/detail(5590×7) 超 15 万字符时 MCP 报 token 超限并落盘到 `tool-results/*.txt`——**不是失败**，用 `json.load` 解析即可。
6. **数值字段不能进 group_by_attrs**（报"不是分组属性"）；数值维度走 group_by_code。
7. **停牌 → 复牌 `pct_change` 出 ±100%+ 假收益**：归因前按 1%/99% 截尾；**绝不把 NaN 当 0**。
8. **未来函数**：标签收益必须 `shift(-1)`，因子只用过去窗口。
9. **scipy 不可用**（quantall venv）：Spearman 用 `rank()` 后 Pearson 代替。
10. **起始市值冻结写法**：`mcap=d['总市值'].ffill().bfill(); mcap0=mcap.iloc[[0]].reindex(index=mcap.index).ffill()`；**不要** `d['总市值'].iloc[0]` 直接当面板。

---

## 8. 已验证样例结论（金叉 MA5/20 全市场，5590 只，2024-08-28→2026-08-07）

> 注：数值随数据库更新会小幅变动（2026-08-30 重测 summary：盈利比率 50.16%、年化均值 +7.72%、夏普 0.187、持仓比 47.1%，方向与历史一致）。

> 「均线金叉 = 半仓市场 beta + 小盘/波动暴露的趋势策略：制造科技（玻璃/半导体/机械基件）有效、金融消费（白酒/证券/保险）失效；收益集中于 924 行情（**局部有效**、参数敏感）；无选股 alpha（排序分位 0.5）、不择时（r≈0）；剔除极端股仍稳——属'顺风有效、逆风脆弱、不靠妖股'类。入场因子筛选改善真实但温和（单因子 <1pp，贪心 5 因子 +1.5pp，时间分布均匀），多因子交集展示（Y=1 片段 +5.7% vs 全局 +1.7%）可直观看到优质买点。」

**对照（反转策略：20日跌15%买、回0卖）**：summary 逐笔 +7.08%（"看似有效"）但连续复利年化 **−9.2%**——**两口径方向相反 = D7 假有效典型**；流程可泛化且能区分策略机制。

---

## 9. 给全A解析制作人的工具建议

- **P0 · 策略收益序列结构化输出**：`strategy_backtest` 返回组合每日收益 Series / 持仓权重矩阵（结构化），使归因直接用引擎精确执行。
- **P1 · `segments` 结构化**：返回每片段记录表（stock/entry/exit/return/days），免本地拆段（当前脚本须 run_codes 重算）。
- **P1 · `timeline` 结构化输出**：直接返回每日指标 DataFrame，免脚本本地重建。
- **P1 · `group_by` 原生分组**：`strategy_backtest` 加 `group_by` 参数一次返回分组 summary。
- **P2 · `detail` 增加 IC/IR 时间序列**：支撑 IC/IR 时序分析。
- **P2 · `run_task_file` 白名单补 `group_by_time`**：实测白名单缺 `group_by_time`（分组三工具独缺它），导致时间分组无法经任务文件执行，只能直接 MCP 调用。
- **P2 · 确认 `use_price` 语义**：实测 close 与 next_open 的 summary 逐位相同，疑似未流入统计。
- **P3 · 解耦预热与基准窗口**：区分 `warmup_days` 与 `eval_start`。

---

## 10. 目录结构

```
stock-deep-backtest/
├── SKILL.md                  # 本文档（v0.0.0）
├── tasks/                    # 固定调用指令 JSON（11 个，run_task_file 执行）
├── scripts/                  # 深度分析脚本（8 个）+ 因子库 xlsx + 输出
│   ├── data/db_translate.json
│   └── factor-screen-final-50.xlsx   # 50 个清洗因子参考（name/code/IR）
└── archive/                  # 历史归档：SKILL_v0.4 存档、POC 脚本、旧 task JSON
```
