# v2 输入口径、来源与估值字段

先运行 `python scripts/score_engine.py --template --output metrics.json`，得到null空模板；不要用示例数值替代真实数据。
`scripts/test_value_model.py`提供完整的**合成测试输入**，仅用于理解结构，禁止用于实际持仓结论。

## 数据来源与日期

顶层`date`为分析日YYYY-MM-DD。每只股票包含`indicators`和同名键的`indicator_meta`：

```json
{
  "roe_ttm": {
    "source": "原始财报URL或可复核数据记录标识",
    "as_of": "2026-09-04",
    "published_at": "2026-08-25",
    "period_end": "2026-06-30",
    "unit": "percent",
    "kind": "actual"
  }
}
```

上例只是字段格式。`as_of`是原始观测/信息可得日期，不得拿今天的抓取日为旧数据续期；可另存`fetched_at`。
源缺失、日期晚于分析日、过期等会剔除该指标并留下原因。财务字段必须同时提供报告期与公告日，且报告期≤公告日≤数据日≤分析日。
财务数据及报告期上限550个自然日（只是技术兜底，不代表旧财报充分有效）；若已有新财报必须用最新已披露期。
预期、行业景气、周期恢复、机构持股、股东户数、调研热度允许90日；其他指标默认7日；交易状态1日。超龄自动停用，无法获得就null，不刷新日期伪装有效。
现价使用独立`price_meta`，与上述来源/日期同结构。风险使用独立`risk`，见下文。

## 财务与增长

百分比一律用百分数：20%写20；金额单位统一元，股份统一股，每股数据元/股；比率如现金转化与CV用小数。
- TTM=`本年累计+上年全年-上年同期累计`；单季=`本期累计-上期累计`。
- `roe_ttm`：归母净利TTM/平均归母净资产×100；净资产非正时不适用，不能机械计算。
- `gross_margin`、`net_margin`、`debt_ratio`：同期间毛利/收入、净利/收入、总负债/总资产×100。
- `net_profit_ttm`与`operating_cashflow_ttm`：同期实际金额，元；引擎只在同报告期且净利为正时重算现金转化，不接收外部`ocf_to_np`替代。
- `np_cv_3y`：不少于3个年度净利的标准差/正均值；meta增加`annual_samples`与`positive_mean=true`。亏损/非正均值不套CV。
- `rev_yoy`、`np_yoy`：同期同比百分数。`prior_net_profit`为对应去年同期利润；≤0时不使用同比增长评分。扣非和归母口径明确标注，不能混用。**v2.4.0 起 `np_yoy` 可自算**：缺该字段时，若有正 `net_profit_ttm` 与正 `prior_net_profit` 且两者 `period_end` 相差约一年（350–380 天），引擎按 `(net_profit_ttm/prior_net_profit-1)×100` 派生；已有值优先不覆盖。
- `qoq_trend`：improving/flat/deteriorating，至少3个单季观测判断连续变化，注意季节性。
- `forecast`：beat/inline/flat/miss，必须有可比预期与实际口径；无预期不得用猜测补充。
- `cycle_recovery` / `loss_recovery`：improving/flat/deteriorating，分别用于周期和亏损企业；记录量价、利润率、产能和恢复路径的证据。
- `normalized_profit_growth_pct`：券商/保险正常化盈利增长，不能用牛市利润直接外推。
- `sector_np_yoy_pct` / `sector_rev_yoy_pct`：**申万行业财报TTM净利/营收同比**，百分数，取行业聚合口径（用 `westockdata sector finance`）。引擎据此派生 `industry_boom`（净利70%+营收30%，只有净利时单口径），净利曲线`-20→0/0→35/10→60/25→85/50→100`、营收曲线`-10→0/0→40/10→70/25→100`。
- `industry_boom`：**不再手填**。有行业数据时由上面两项派生并覆盖手填值；行业数据缺失或过不了证据门槛时才退回手填，仍没有则按期望分50插补。行业口径必须与个股所属行业一致，跨行业拼接无效。
- `dividend_yield_pct`：股息率百分数（每股现金分红TTM/现价×100），0–100，慢变量（90日）。
- `cash_dividend_ttm`：最近12个月**现金分红总额**，元，与净利同口径，非负；财报级（550日）字段。
- `dividend_spread_pct`：**派生项，不接受输入**。= `dividend_yield_pct − market.risk_free_rate_pct`；曲线`-1→0/0→50/1→80/2.5→100`个百分点，进 V（权重20）。
- `dividend_coverage`：**派生项，不接受输入**。= `net_profit_ttm / cash_dividend_ttm`；曲线`0.8→0/1.2→45/1.7→75/2.5→100`倍，进 Q（权重10）。
  上述两项必须**同时**可算才启用股息子项，缺一即整块不进分母。缺有效无风险利率时同样不启用。

金融Q额外字段：银行`provision_coverage`、`npl_ratio`、`cet1_buffer_pct`；券商`roe_normalized`、`risk_coverage_ratio`、`net_capital_to_netasset`；保险`roe_normalized`、`core_solvency_ratio`、`comprehensive_solvency_ratio`。均为百分数，其中cet1_buffer_pct为实际核心一级资本率减该银行适用监管要求的**百分点差**。不能把通用阈值当成当前法规。

## 相对估值与交易环境

PE/PB/PS历史分位需逐时点当时已披露利润/净资产/收入与匹配股本，或来源明确的同口径历史估值序列。**不能用当前EPS除历史股价，不能用行业分位替代个股分位**。
`pe_pct`/`pb_pct`/`ps_pct`的meta必须标`basis=point_in_time`和`history_months>=36`；尽量使用60个月。无法满足则null。
`rel_industry_discount`=`(个股倍数/可比公司中位数-1)×100`；meta提供`multiple=PE/PB/PS`，需与行业档位选用的分位类型匹配；负倍数、分母非正或业务不可比时不算。
PEG辅助计算：PE20、未来增长20（20%），PEG=20/20=1；禁止再次×100。无未来增长或增长≤0时null，不用历史增速静默替代。PEG不再参与V评分。

F字段：`main_inflow_20d_pct`=20日净流入/流通市值×100；`inflow_5d`=in/flat/out；`institution_change_pct`=已验证机构持股比例的百分点变化；`volume_signal`=rising_expansion/normal/weak；`holders_change`=down/flat/up。
机构持股字段必须说明机构范围和起止时间，不把旧北向20日数据直接改名。先核实供应商披露频率与覆盖，取不到就是null。
volume_signal：成交额/60日均额>1.5且上涨为rising_expansion，1–1.5为normal，其余weak。
T字段：`ma_alignment`=bull/tangle/bear；`rs_60d`为60日相对基准超额百分点；`macd`=golden_expand/golden/death/death_expand；`drawdown_from_250d_high`为正回撤百分数；`annual_vol`为年化波动百分数。
N字段：`rating_buy_ratio`0–100；`news_sentiment`与`major_announcement`=positive/neutral/negative；`research_visits_3m`非负调研次数。定性字段必须附原文来源与日期。
`ma60`、`low_3m`、`tech_resistance`均为价格。只给低于现价的有效支撑参考，不再用成本×0.92或固定波动公式生成止损。

## 估值结构

`valuation`需要`method`、`source`、`sources`（来源列表）、`as_of`、`horizon=current_fair_value`、`assumptions`（非空对象）、`scenarios.bear/base/bull`。
每个情景必须提供完整字段。当前不支持外部直接填写“目标价”绕过公式，也不自动平均不同方法。保守≤基准≤乐观由经营假设产生，不机械±20%。

| method | 每个情景输入与公式 |
| --- | --- |
| normalized_pe | `eps_normalized`×`fair_pe`；二者正数。合理倍数需依据可比增长/质量与风险，不机械采用历史PE中位数 |
| justified_pb | `bps`×(`sustainable_roe_pct`-`terminal_growth_pct`)/(`cost_of_equity_pct`-`terminal_growth_pct`)；bps>0，Ke>g≥0且ROE>g；增长、留存与资本约束一致 |
| embedded_value | `embedded_value_per_share`×`fair_ev_multiple`；仅保险，正值。内含价值假设和新业务/存量业务含义需解释 |
| ev_ebitda | 企业价值=`ebitda_normalized`×`fair_multiple`，再做股权桥接；仅周期企业 |
| ev_sales | 企业价值=`revenue_forward`×`fair_multiple`，再做股权桥接；仅成长企业，说明未来利润率和融资风险；倍数须与前瞻收入一致且代表估值日企业价值 |
| fcfe / ddm | 年末每股自由现金流/股利`cashflows`（3–10项）；`discount_rate_pct`为股权成本；`terminal_cashflow`为明确的下一年可持续每股现金流；`terminal_growth_pct`为长期增长 |
| fcff | `cashflows`为公司整体年末自由现金流金额，折现率为WACC；终值现金流为下一年整体金额；折现后再做股权桥接 |

DCF公式：`ΣCF_t/(1+r)^t + terminal_cashflow/(r-g)/(1+r)^N`。要求r>0、-100%<g<r、终值现金流>0；股利不得为负。
终值现金流必须包含维持长期增长所需的再投资，不自动拿最后一年异常利润外推。
股权桥接：`(企业价值-net_debt-minority_interest+non_operating_assets)/diluted_shares`。四个字段均必填，即使为0；净债务允许负值，稀释股数必须正；不要对同一现金重复加回。
金额、现金流、股数须使用相同货币与规模单位；外币估值先统一币种。每股fcfe/ddm必须反映未来融资稀释，不能把总额当每股值。
周期企业必须在`assumptions.cycle_normalization`说明完整周期利润与恢复路径；DCF假设说明收入、利润率、再投资、资本约束、折现及终值；没有可信预测时暂不估值。
预测不是已披露事实，标明假设和预测期，来源与假设不得伪造。引擎检查结构和数学条件，不验证外部源真伪，也不能证明假设经济合理。

`consensus`独立对象：`target`、`institutions`（至少3个去重机构名）、`source`、`as_of`（90日内）、`horizon`。单一机构重复研报不得凑数量；保留机构预测年度与分歧记录。

## 风险、配置与版本

`market`块除四个温度标量外，可放下列**原始序列**让引擎自算（显式给值优先，序列需自带`indicator_meta.<序列名>`）：
`hs300_close_series`（沪深300收盘，≥250）、`turnover_series`（全市场成交额，≥250，近似量能）、`advance_ratio_series`（逐日上涨家数占比%，≥20）。
另需`risk_free_rate_pct`（10年期国债收益率%，0–20，90日内有效）供股息利差使用。`broken_net_ratio`无法派生，仍需外部提供。
自算结果记在`market.derived`，`notes`同步写明。
**出分口径（v2.4.0）**：四项里拿到 ≥3 项（`MIN_MARKET_ITEMS`）即输出温度分，分母改用**可用项权重和**归一；不足 3 项才为"数据不足"。输出附 `coverage`（可用权重占比）、`used`/`missing`（用上/缺失的项）、`min_items`（门槛=3），`notes` 写明"由 N/4 项归一得出"。

`risk={status:checked, events:[], source:..., as_of:...}`表示7日内已核查无风险。未查或失败：status=not_checked/failed，events=null。风险标签ST、*ST、退市预警、立案调查使用标准名称。
财务降级字段`major_shareholder_reduce_pct`（近30日占总股本比例）、`goodwill_to_netasset`均百分数并附meta。

`portfolio_policy`：risk_tolerance=conservative/balanced/aggressive；horizon_years、max_drawdown_pct、total_assets为正；cash_need_pct、equity_budget_pct、other_assets_pct为0–100；holdings_complete=true；weight_basis=total_assets。
`current_weight`必须是股票市值/全部资产×100，不能用股票市值合计做分母。总资产包括股票、现金及其他资产；融资或负债账户需单独建模，当前不自动配置。
每只持仓需`industry`、`exposure_group`和`tradability=normal`及`tradability_meta`（1日内）。分组缺失、NR、风险未查、停牌/涨跌停等均暂停整个配置。

旧JSON可以生成“缺失信息/暂不评级”报告，但不会沿用旧中性分与三法目标价。补足新schema后再评级。历史v1快照不与v2直接比较分差。
