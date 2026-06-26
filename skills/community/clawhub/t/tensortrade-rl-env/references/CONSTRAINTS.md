# Constraints

## preservation_manifest

```yaml
required_objects:
  business_decisions_count: 139
  fatal_constraints_count: 44
  non_fatal_constraints_count: 174
  use_cases_count: 19
  semantic_locks_count: 12
  preconditions_count: 4
  evidence_quality_rules_count: 2
  traceback_scenarios_count: 5

```

## Domain Constraints Injected (39)

- **`SHARED-BT-LAB-001`** <sub>(fatal)</sub>: 未来函数（Lookahead Bias）：在模拟历史时间点 t 的交易决策时， 不得使用 t 时刻之后才能知道的信息。最常见形式： (1) 使用收盘价计算信号并同日以收盘价成交； (2) 将 T 日收盘后计算的指标标记在同一根 K 线； (3) 使用当日最高/最低价作为成交假设。 信号计算与成交时间必须对齐：T 日收盘后计算信号，T+1 日开盘成交。
- **`SHARED-BT-LAB-002`** <sub>(high)</sub>: 指标预热期（Warmup Period）处理：滚动窗口指标在前 N 个 bar 时 NaN， 这些 bar 不应参与信号计算和持仓决策。强制要求指标的 warmup_period 与最长 lookback 期等长，且 warmup 期间持仓应置零。
- **`SHARED-BT-LAB-003`** <sub>(fatal)</sub>: ML/DL 模型时序数据划分必须按时间顺序：TRAIN < VALID < TEST， 不可使用随机 k-fold 分折（会将未来数据混入训练集）。 应使用 TimeSeriesSplit 或 Walk-Forward 验证。
- **`SHARED-BT-LAB-004`** <sub>(fatal)</sub>: 开盘价/最高价/最低价成交假设：日线回测中假设每日可以最高价卖出或 最低价买入（如动量策略"最高价止盈"），这是明显的 lookahead， 因为日内最高/最低价只有收盘后才能确认。成交价只能用开盘价或 前一日收盘价（带滑点）。
- **`SHARED-BT-LAB-005`** <sub>(high)</sub>: 数据对齐偏移（Off-by-one）：pandas rolling/shift 等操作容易引入细微的 1 期偏移错误。应在代码中明确记录每个序列的"观测时间点"， 并通过 assert 验证关键时间对齐关系。
- **`SHARED-BT-LAB-006`** <sub>(high)</sub>: 过度优化（Overfitting）：回测数量越多，过拟合概率越高。 Bailey et al.（2014）证明 Optimal Sharpe Ratio 期望值随回测次数单调递减。 应使用 Walk-Forward 验证代替 in-sample 参数穷举，并报告 Deflated Sharpe Ratio（DSR）而非峰值 Sharpe。
- **`SHARED-BT-SURV-001`** <sub>(fatal)</sub>: 幸存者偏差（Survivorship Bias）：使用当前市场成分股作为历史回测股票池， 会遗漏曾经存在但后来退市、摘牌或被合并的股票，系统性高估策略历史收益率。 回测股票池必须使用历史时点快照（point-in-time universe）。
- **`SHARED-BT-SURV-002`** <sub>(high)</sub>: In-Sample / Out-of-Sample 划分：策略开发、参数选择必须在样本内完成， 样本外数据仅用于最终验证，不可多次"看"样本外数据后继续调优 （会将样本外变为新的样本内，重蹈过拟合）。
- **`SHARED-BT-SURV-003`** <sub>(high)</sub>: 停牌/缺失数据的填充策略：停牌日价格不可简单用前一日收盘价 forward-fill， 因为这会在复盘时造成"零成交量"日参与了因子计算和信号生成。 应在因子计算层显式过滤缺失交易日，不填充。
- **`SHARED-BT-SURV-004`** <sub>(high)</sub>: 异常值（Extreme Value）污染：原始市场数据可能含有数据源错误（如除权未 及时调整、手工录入错误导致的极端价格），不清洗直接进入因子计算会产生 极端信号，污染整个横截面。应在 pipeline 入口处过滤 3-sigma 异常值。
- **`SHARED-BT-COST-001`** <sub>(fatal)</sub>: 交易成本（佣金 + 印花税/转让税 + 过户费）必须在回测初始化时强制配置， 不可使用零成本默认值。忽略成本的回测策略绩效指标具有欺骗性， 高换手率策略尤其严重（单边往返成本往往吞噬 50%+ 的毛收益）。
- **`SHARED-BT-COST-002`** <sub>(high)</sub>: 滑点（Slippage）建模：回测若无滑点，假设每笔订单以理想价格成交， 高频策略在实盘中会因成交价劣化而产生严重亏损。至少应配置固定点差 或比例滑点；大单应使用成交量比例模型（如不超过日成交量 5%）。
- **`SHARED-BT-COST-003`** <sub>(high)</sub>: 换手率（Turnover）必须在回测绩效报告中展示并与成本关联分析。 月换手率超过 50%（年化 600%+）时，策略净收益对成本假设极度敏感， 每 10bps 成本变化可能改变策略盈亏结论，必须做成本敏感性分析。
- **`SHARED-BT-COST-004`** <sub>(medium)</sub>: 仓位规模化（Position Sizing）必须纳入资金量约束：回测应模拟固定资金量 下的实际持仓股数（取整），而非假设可以持有小数股。 对小盘股，最小交易单位（A股：100股/手）会导致实际可持仓量与目标权重 产生偏差，应在回测中模拟取整效应。
- **`SHARED-BT-TIME-001`** <sub>(high)</sub>: 时间戳时区统一：多数据源合并时，UTC vs 本地时间混用是常见数据腐败源。 所有时间戳必须在 pipeline 入口处统一转换为同一时区（推荐 UTC 存储， 市场本地时区展示），不可在 pipeline 中途混用不同时区。
- **`SHARED-BT-TIME-002`** <sub>(high)</sub>: 交易日历对齐：合并不同市场或不同频率数据时（如日线价格 + 周频因子）， 必须使用明确的交易日历进行 reindex/merge，不可使用 outer join 后 fillna， 否则会在非交易日（节假日）创建虚假数据行。
- **`SHARED-BT-TIME-003`** <sub>(high)</sub>: 增量更新边界校验：历史数据增量更新时，必须从数据库查询已存最新日期， 仅下载该日期之后的数据。若重新下载已有数据并追加，会产生时间戳重复行， 导致回测时序错误。更新前后必须校验无重复 (index.duplicated().any() == False)。
- **`SHARED-BT-TIME-004`** <sub>(medium)</sub>: 回测绩效归因失真：基准（Benchmark）选择不当会使 Alpha/Beta 计算失真。 应选用策略实际可投资的被动基准（如 HS300 ETF），而非不可直接投资的 价格指数（如 HS300 指数）。价格指数不含股息再投资，会低估持仓基准收益。
- **`SHARED-BT-PERF-001`** <sub>(medium)</sub>: 最大回撤（Max Drawdown）计算必须使用净值序列（portfolio value）， 不可用累计收益率序列代替。若使用对数收益率累加，会低估回撤深度 （因对数收益率在下跌时会比简单收益率偏小）。
- **`SHARED-BT-PERF-002`** <sub>(medium)</sub>: Sharpe Ratio 年化化约定：年化 Sharpe = 日 Sharpe × sqrt(252)（股票，252 交易日） 或 × sqrt(365)（加密货币，365日）。不同系统默认不同，跨系统对比前必须 确认年化因子，否则 Sharpe 不可比。
- **`SHARED-BT-PERF-003`** <sub>(medium)</sub>: Calmar Ratio / Sortino Ratio 优于 Sharpe Ratio 作为风险调整收益指标： Sharpe 假设收益正态分布，A 股/加密市场的收益分布显著左偏（肥尾）， 会低估下行风险。量化评估应同时报告 Sortino（仅下行波动）和 Calmar（年化收益/最大回撤），不应单一依赖 Sharpe。
- **`SHARED-BT-PERF-004`** <sub>(medium)</sub>: 回测绩效归因应拆解为：alpha（主动收益）、beta（市场收益）、 因子暴露收益（style/sector）和特异性收益（stock selection）。 不做归因的回测无法区分"策略优秀"与"顺风行情恰好 beta 对了"。
- **`SHARED-FR-IC-001`** <sub>(high)</sub>: IC（信息系数）是衡量因子预测能力的核心指标，定义为因子值与 下期收益率的 Spearman 秩相关系数（ICIR = IC / std(IC)）。 IC 绝对值 > 0.05 视为有预测能力的初步证据，ICIR > 0.5 视为稳定。 不计算 IC 直接报告回测绩效是因子有效性证明缺失的典型问题。
- **`SHARED-FR-IC-002`** <sub>(high)</sub>: IC 衰减（IC Decay）分析：因子预测能力通常随持仓期增长而衰减。 应计算 1/5/10/20 日 IC 序列，识别因子的最优持仓期。 IC 在1日高但20日迅速衰减的因子是短期因子，不适合月度换仓策略； 反之亦然。使用错误的持仓期会严重损害因子实盘表现。
- **`SHARED-FR-IC-003`** <sub>(high)</sub>: Harvey, Liu & Zhu (2016) 警告：学术界已发现 300+ 个"显著"因子， 其中大量是多重检验下的误发现（False Discovery）。因子有效性要求： t-stat > 3.0（而非传统的 1.96）；或在不同时段/市场独立复现； 或有清晰的经济学逻辑。不满足上述条件的因子极可能是数据挖掘产物。
- **`SHARED-FR-IC-004`** <sub>(high)</sub>: 因子换手率（Factor Turnover）控制：高 IC 但高换手率的因子，在扣除 交易成本后净 IC 可能为负。应计算换手率调整后的有效 IC： net_IC = IC - turnover × cost_per_turn。目标换手率 ≤ 50%（月频）。
- **`SHARED-FR-IC-005`** <sub>(medium)</sub>: 因子衰减期（Half-life）是因子信号强度的核心参数，直接决定最优再平衡频率。 半衰期 < 5 日：日频或周频换仓；5-20 日：周频或双周；> 20 日：月频换仓。 错误地对短期因子使用月频换仓，会导致大量 alpha 在持仓期内消散。
- **`SHARED-FR-NEUT-001`** <sub>(high)</sub>: 行业中性化（Industry Neutralization）：因子值若不对行业均值中性化， 因子收益中会混入行业轮动收益，难以判断是因子本身还是行业暴露驱动了收益。 行业中性化操作：factor_neutral = factor - industry_mean(factor)。
- **`SHARED-FR-NEUT-002`** <sub>(high)</sub>: 市值中性化（Market Cap Neutralization）：小盘股效应（小盘跑赢大盘） 是金融史上最持久的 anomaly 之一，会污染几乎所有未中性化的因子。 若因子与市值高度相关，选股会系统性偏向小盘，收益来自市值暴露而非因子本身。 需同时进行行业和市值中性化（Fama-MacBeth 回归或残差法）。
- **`SHARED-FR-NEUT-003`** <sub>(high)</sub>: 异常值处理（Winsorize/MAD）：因子原始值通常含有极端值，极端值会扭曲 分组分析（如 Q1/Q10 十分位）。应对原始因子值做 Winsorize（截尾至 [1%, 99%] 或 3-sigma）或 MAD（中位数绝对偏差）缩尾，然后再排名/中性化。
- **`SHARED-FR-NEUT-004`** <sub>(medium)</sub>: 因子正交化（Factor Orthogonalization）：当多个因子共同用于合成打分时， 高相关因子的合成等效于对单一因子过度权重，稀释信号多样性。 应在合成前对因子做施密特正交化或 PCA，消除因子间的多重共线性。
- **`SHARED-FR-NEUT-005`** <sub>(medium)</sub>: 缺失数据填充策略：因子计算中的 NaN（停牌/新股/数据缺口）若用截面均值填充 会引入 lookahead bias（均值本身含未来信息）；若完全删除会产生幸存者偏差； 正确做法是用截面中位数（当日所有股票的中位数，不依赖未来）或将该股当日排除。
- **`SHARED-FR-PORT-001`** <sub>(high)</sub>: 分层分析（Quantile Analysis）：因子评估应使用 Q1/Q5（五分位）或 Q1/Q10（十分位）分组的多空收益差（top minus bottom spread）作为 主要评估指标，而非简单的多头收益。Q1 多 Q5 空的"单调性"检验是 因子有效性的核心证据：单调递增/递减 > 非单调 >> 仅多头有效。
- **`SHARED-FR-PORT-002`** <sub>(medium)</sub>: Alpha 衰减测试（Alpha Decay Test）：因子的月度 IC 在不同时段（牛市/熊市/ 震荡市）的稳定性是因子鲁棒性的重要证据。IC 仅在某个特定市场状态下有效 的因子不适合全天候部署；应分段（rolling 12M）展示 IC 时序， 识别因子失效期。
- **`SHARED-FR-PORT-003`** <sub>(medium)</sub>: 换仓成本感知（Turnover-Aware Selection）：因子排名靠近中间地带（49-51 分位） 的股票，排名小幅波动就会触发换仓，产生大量无效交易成本。 应在选股时设置换仓缓冲区（buffer zone）：只在排名变化超过阈值时才换仓。
- **`SHARED-FR-PORT-004`** <sub>(medium)</sub>: 分组收益的统计显著性（Bootstrap 检验）：因子分层收益差（Q1-Q5 spread） 即使在历史数据上很大，也可能是偶然，需要 bootstrap 或 t-test 检验 显著性（p-value < 0.05）。小样本回测期（< 3年）的分层收益尤其不可靠。
- **`SHARED-FR-XFER-001`** <sub>(high)</sub>: 因子跨市场可移植性验证：在一个市场有效的因子，不必然在另一个市场有效。 将美股因子直接套用 A 股、或将股票因子套用期货/加密货币，需要独立 IC 验证， 不可假设跨市场通用性。A 股特有异象（如反转效应、ST 价格异常）不存在于美股。
- **`SHARED-FR-XFER-002`** <sub>(medium)</sub>: 因子有效性时间稳定性：曾经有效的因子会因市场学习和套利行为逐渐失效 （McLean & Pontiff 2016 证明因子发表后平均衰减 58%）。 应定期（每季度/年）重新评估因子 IC，失效因子应及时替换或降权。
- **`SHARED-FR-XFER-003`** <sub>(medium)</sub>: 因子与宏观经济环境的交互：利率周期/经济周期/市场情绪对因子有效性影响显著。 价值因子（低 P/B）在利率上升期更有效；动量因子在趋势市更有效，震荡市失效。 部署因子前应评估当前宏观环境与因子最优生存环境的匹配度。
