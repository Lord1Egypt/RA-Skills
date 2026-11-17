# 使用用例

以下示例均为研究、模拟或本地记录用途；不连接券商，也不会发送真实订单。飞书中可直接使用自然语言；若 Agent 需要工具参数，按每个示例的调用填写。

## 1. 每日盘前/盘后市场检查

飞书可直接说：

```text
查看今天 A 股大盘、成交额、涨跌家数和市场情绪。
```

对应工具：

```text
get_market_review()
```

适合用于快速了解市场环境。行情默认来自腾讯公开数据；配置同花顺凭据后，`STOCK_DATA_PROVIDER=auto` 会优先使用 iFinD。

## 2. 诊断一只股票的技术面

飞书可直接说：

```text
分析 600519 的最新行情、均线、RSI、支撑位和压力位，只做研究，不给买卖指令。
```

对应工具：

```text
ask_stock(stock_code_or_name="600519")
```

股票代码可使用 `600519`、`600519.SH`、`000001.SZ` 等形式。输出是指标快照，需要结合基本面、公告和个人风险承受能力判断。

## 3. 用策略筛选候选股

飞书可直接说：

```text
用放量突破策略，从 A 股中筛出 10 只候选股，市值不低于 100 亿；给出筛选条件和结果，不要声称收益保证。
```

对应工具：

```text
screen_stocks(
  strategy="volume_breakout",
  market_cap_min_yi=100,
  top_n=10
)
```

可用策略：`bull_momentum`、`low_valuation_value`、`volume_breakout`、`growth_tech`、`oversold_rebound`、`book_volume_turnover`、`volume_ratio_watch`。筛选结果只是候选清单，不能直接等同于交易建议。

## 4. 对单只股票做轻量回测

飞书可直接说：

```text
对 600519 做 180 根日线的均线交叉策略回测，初始资金 10 万，解释收益、回撤和交易次数的局限。
```

对应工具：

```text
backtest_strategy(
  stock_code="600519",
  strategy="sma_cross",
  lookback_bars=180,
  initial_cash=100000
)
```

策略可选 `sma_cross`、`momentum_breakout`、`rsi_mean_reversion`、`ma_5_10_60_trend`、`macd_cross_trend`。回测不包含滑点、全部税费和未来数据不可得等现实因素，历史结果不代表未来表现。

## 4.0 用 Alpha Zoo 横评预置因子（不使用对话或 LLM）

首次使用前，在 Skill 根目录运行：

```bash
python3.11 scripts/bootstrap_vibe_trading.py
```

随后可直接调用：

```text
run_factor_research(
  action="benchmark",
  zoo="gtja191",
  universe="csi300",
  period="2018-2025",
  top_n=20
)
```

可用因子库为 `academic`、`alpha101`、`fundamental`、`gtja191`、`qlib158`；市场为 `csi300`、`sp500`、`btc-usdt`。这会调用私有 Vibe-Trading 环境中的固定 Alpha Zoo 命令，不需要模型 Key 或 `confirm_external_ai=true`，也不会进入聊天或下单路径。数据下载与回测可能耗时，结果必须结合样本外、交易成本和因子相关性复核。

查询已有因子而不跑回测：

```text
run_factor_research(action="list", zoo="academic", universe="csi300", theme="momentum", limit=10)
run_factor_research(action="show", factor_id="academic_carhart_mom")
```

## 4.0.1 用腾讯公开日线做价量因子横评（无需 Tushare）

当 Tushare 没有历史日线权限时，可传入一份自己归档的股票池，以腾讯复权日线评估基础价量因子。股票池至少 20 只，且必须符合研究期的实际可投资范围；不要把今天的 CSI300 成分股拿去回测早年数据。

```text
run_tencent_factor_research(
  stock_codes=["600000", "600009", "600015", "600016", "600018", "600019", "600028", "600030", "600031", "600036", "600050", "600104", "600196", "600276", "600309", "600438", "600519", "601012", "601138", "601991"],
  start_date="2024-01-01",
  end_date="2025-12-31",
  factor_ids=["momentum_20", "reversal_5", "low_volatility_20", "volume_ratio_20", "ma_gap_20"],
  forward_days=20,
  rebalance_days=20,
  oos_split="2025-01-01",
  random_seeds=20
)
```

结果中的 `direction_selected_in_train` 只允许由训练期决定；`eligible_for_further_validation=true` 仅表示样本外最高分组与分组价差为正、Rank IC 同向且优于本次随机对照，仍需纳入成本、容量和更多独立时间段复核。腾讯数据会缓存在 `~/.local/share/stock-screener-pro/tencent-factor-cache`；传 `refresh_cache=true` 可强制刷新。

## 4.1 使用均线、MACD、KDJ 与量价研究快照

飞书可直接说：

```text
分析 600519 的 MACD、KDJ、MA5/10/60 和量价状态；只给出可复核指标与数据限制，不要给买卖指令。
```

对应工具：

```text
ask_stock(stock_code_or_name="600519")
```

读取 `technical_diagnosis.book_technique_research`。其中的“底背离观察”“顶背离观察”是基于最近日线局部高低点的程序化标记，必须结合收盘确认与更长周期核验，不是买卖指令。宝塔线、盘口深度、封板质量、板块出现频率、振幅、流通股本和20日涨停历史在当前数据源中不可统一验证，结果会如实说明。

## 4.2 用书中量比/换手条件建立观察池

```text
screen_stocks(
  strategy="book_volume_turnover",
  turnover_min=3,
  top_n=10
)
```

或使用较严格的强量比观察：

```text
screen_stocks(strategy="volume_ratio_watch", top_n=10)
```

前者覆盖“换手≥3%、量比≥1.5”的可得条件；后者覆盖“量比>2、换手<5%”的可得部分。两者都不声称已验证振幅、流通股本、涨停历史或个股题材热度。

## 4.3 检验三均线和 MACD 交叉规则

```text
backtest_strategy(
  stock_code="600519",
  strategy="ma_5_10_60_trend",
  lookback_bars=180,
  initial_cash=100000
)

backtest_strategy(
  stock_code="600519",
  strategy="macd_cross_trend",
  lookback_bars=180,
  initial_cash=100000
)
```

这两项只用历史日线进行简化模拟，不支持自动打板、排板、回封、龙回头或实盘超短执行。请把它们视为规则检验工具，并比较基准收益、最大回撤、交易次数及样本外期间，而非依据单一回测结果行动。

## 4.4 判断“明天是否值得继续观察”的完整示例

这个流程用于把“明天该不该买”拆成可核验的问题；Skill 不会输出自动买入指令，也不会连接券商。建议在收盘后运行，因为盘中日K、成交量和指标都可能变化。

### 第一步：确认市场环境

```text
get_market_review()
```

查看 `market_sentiment`、指数涨跌与 `market_breadth_sample`。市场整体明显偏弱时，即使个股技术指标转强，也应把结论降为“等待确认”或“暂缓观察”，而不是孤立地解读个股。

### 第二步：取得个股的收盘后技术快照

飞书可直接说：

```text
分析某只股票的收盘后 MA5/10/60、MACD、KDJ 与量价状态；只输出研究判断、风险和数据限制，不给交易指令。
```

对应工具：

```text
ask_stock(stock_code_or_name="股票代码或名称")
```

重点读取 `technical_diagnosis.book_technique_research`：

| 核验项 | 相对积极的研究观察 | 需要等待或暂缓的观察 |
| --- | --- | --- |
| `ma_5_10_60.alignment` | `多头排列`，且价格未明显偏离均线 | `空头排列` 或均线顺序混乱 |
| `macd_12_26_9` | 收盘后 `gold_cross=true`；底背离仅作为附加观察 | `dead_cross=true`，或信号尚在盘中变化 |
| `kdj_9_3_3` | 没有顶背离观察 | `top_divergence_watch=true`，需要复核上涨衰竭风险 |
| `volume_price.state` | 量增价涨，且成交没有异常失真 | 放量走弱、缩量上涨或量价中性 |
| `breakout_observation` | 收盘后再复核突破是否成立 | `current_bar_complete=false` 时不能据此下结论 |

表内任一项都不是单独的买卖条件；尤其是背离标记只比较最近局部高低点，必须结合更长周期、公告和市场环境复核。

### 第三步：把量比和换手条件变成候选池

```text
screen_stocks(
  strategy="book_volume_turnover",
  turnover_min=3,
  top_n=10
)
```

这会执行换手率≥3%、量比≥1.5 的可得部分。若要观察量比更高、换手不过热的对象：

```text
screen_stocks(strategy="volume_ratio_watch", top_n=10)
```

请注意：振幅≤5%、流通股本≤20亿、20日涨停历史与题材热度不在这个公共数据筛选内；结果中的 `data_limit_note` 会明确说明这一点。

### 第四步：检验规则在该股票历史上的风险特征

```text
backtest_strategy(
  stock_code="股票代码",
  strategy="ma_5_10_60_trend",
  lookback_bars=180,
  initial_cash=100000
)
```

再用 MACD 规则交叉验证：

```text
backtest_strategy(
  stock_code="股票代码",
  strategy="macd_cross_trend",
  lookback_bars=180,
  initial_cash=100000
)
```

不要只看 `total_return`。至少同时比较 `max_drawdown`、`total_trades`、`benchmark_buy_and_hold_return` 与 `alpha`；交易次数很少或回撤超出自身承受范围时，应视为证据不足。回测未包含涨跌停成交限制、完整税费、滑点、停牌与幸存者偏差。

### 第五步：需要基本面和事件复核时

在你明确同意本次模型/行情调用后：

```text
run_agent_research(
  engine="tradingagents",
  stock_code="股票代码",
  analysis_date="YYYY-MM-DD",
  max_debate_rounds=1,
  confirm_external_ai=true
)
```

让多角色研究重点检查近期公告、业绩预期、行业景气、估值假设和反方风险。`confirm_external_ai=true` 只确认这一轮外部 AI 研究调用，不是券商交易授权。

### 如何汇总结论

将结论限制为三种研究状态，避免把技术指标说成确定预测：

- **继续观察**：市场环境没有明显拖累，收盘后均线/量价/趋势指标大体一致，且历史回测风险可接受。
- **等待确认**：信号仍在盘中、量能不足、指标分歧，或需要等待公告/行业信息复核。
- **暂缓观察**：市场明显偏弱、均线走弱、MACD 死叉、KDJ 顶背离观察或出现放量走弱。

这不是对下一交易日涨跌的预测，更不是收益承诺。实际决策还应考虑仓位、流动性、个人风险承受能力以及独立的基本面核验。

## 5. 建立本地自选与价格提醒

添加自选：

```text
manage_portfolio(
  action="add_watchlist",
  target_type="watchlist",
  stock_code="600519",
  group_name="消费观察"
)
```

创建价格上穿提醒：

```text
manage_alerts(
  action="create",
  stock_code="600519",
  rule_type="price_above",
  threshold=1600
)
```

查看和删除：

```text
manage_portfolio(action="list_all")
manage_alerts(action="list")
manage_alerts(action="delete", rule_id=1)
```

这些操作只写入本机 SQLite 记录和本地提醒规则，不会向券商发单。

## 6. 运行五日方向预测

飞书可直接说：

```text
对 600519 和 000001 做五日方向预测，说明这是 walk-forward 模型输出，并列出不确定性。
```

对应工具：

```text
predict_stock(codes=["600519", "000001"], force=false)
```

`force=true` 会忽略可用缓存重新计算。预测是模型信号，不是价格目标或收益承诺。

## 7. 检查同花顺、DSA 与 AI4Trade 状态

```text
get_skill_status(
  verify_tonghuashun=true,
  include_details=true
)
```

该调用会验证同花顺授权状态，并返回行情源、DSA、AI4Trade、OpenClaw 模型桥接和 TradingAgents 后端状态。不会返回任何 Token、密码或密钥。

## 8. 获取 AI4Trade 信息，或进行受确认操作

查看公开信号：

```text
get_ai4trade(resource="signals", symbol="BTC", limit=10)
```

查看账户和模拟持仓：

```text
get_ai4trade(resource="account")
get_ai4trade(resource="positions")
```

例如关注一位 AI4Trade 交易员时，必须先获得用户对该次操作的明确同意，再调用：

```text
manage_ai4trade(action="follow", leader_id=123, confirm=true)
```

`confirm=true` 仅确认 AI4Trade 平台内的对应状态变更；它不构成券商交易授权。

## 9. 用 OpenClaw 默认模型进行多角色投研

飞书可直接说：

```text
用多角色投研框架研究 600519，截至 2026-08-22，做一轮牛熊讨论和风险复核；我同意本次调用 OpenClaw 模型和行情服务。
```

对应工具：

```text
run_agent_research(
  engine="tradingagents",
  stock_code="600519",
  analysis_date="2026-08-22",
  max_debate_rounds=1,
  confirm_external_ai=true
)
```

默认 `llm_provider=openclaw`，使用 OpenClaw 当前默认模型，不需要单独填写 LLM API Key。该调用可能产生模型费用，也可能将股票代码、研究提示和行情请求发送到已配置服务；每次都要单独传 `confirm_external_ai=true`。

## 10. 使用 Vibe 的研究团队预设

```text
run_agent_research(
  engine="vibe_swarm",
  preset="investment_committee",
  prompt="研究贵州茅台的估值、核心风险与需要继续核验的事实；仅研究和模拟。",
  confirm_external_ai=true,
  timeout_seconds=900
)
```

Vibe 需要先完成自己的 `vibe-trading init` 提供商配置。含有实盘买卖、下单、委托等意图的 Vibe 提示会被拒绝。

## 11. 用 QuantaAlpha 自动挖掘并回测因子

首次使用时在 Skill 目录显式安装独立后端与完整公开数据：

```bash
python3.11 scripts/bootstrap_quantaalpha.py --data full
```

先检查状态：

```text
run_quantaalpha_research(action="status")
```

再运行一次受限研究任务：

```text
run_quantaalpha_research(
  action="mine",
  direction="探索盈利质量、低波动和成交量稳定性的交互因子；报告泄漏检查与样本外验证要求",
  step_n=5,
  confirm_external_ai=true,
  timeout_seconds=3600
)
```

对最近生成的因子库回测：

```text
run_quantaalpha_research(
  action="backtest",
  factor_source="custom",
  confirm_external_ai=true,
  timeout_seconds=3600
)
```

也可用 `factor_source="alpha158_20"` 做无需自定义因子库的官方因子回测。QuantaAlpha 的公开样本止于 2025 年附近，适合研究流程验证，不等于实时预测；结果仍须检查多重检验、幸存者偏差、交易成本、滑点和样本外稳定性。

## 12. 用 QuantaAlpha 兼容因子评估当前持仓

这个入口不调用模型，而是把 Alpha158_20 中六个可由 OHLCV 重算的因子映射到腾讯复权日线。先提供持仓，再补充一个可复原、逻辑一致的对照池，使合并后的股票数达到 20–120 只：

```text
score_portfolio(
  portfolio_codes=["600186", "600276", "600522", "601138", "601991", "603920", "000725", "002747"],
  peer_codes=["600000", "600009", "600016", "600019", "600028", "600030", "600031", "600036", "600050", "600104", "600309", "600519", "601012", "601088", "601318", "601668", "601857", "600900"],
  start_date="2024-01-01",
  as_of_date="2026-09-03",
  oos_split="2025-07-01",
  position_weights=[0.0075, 0.0463, 0.0728, 0.5590, 0.0405, 0.0904, 0.0046, 0.0310]
)
```

权重会自动归一化，因此既可以传市值，也可以传比例；省略时按等权处理。输出中的 `peer_percentile` 和 `relative_exposure_score` 只描述相对于这组股票的因子暴露。组合准入门槛会在 `portfolio_composite_gate` 中原样返回；若 `composite_uses_oos_eligible_factors=false`，分数只能作为探索性对照。它们不是明日上涨概率、未来收益率或买卖信号。若对照池混合多个行业，尤其要关注未做行业和市值中性化这一限制。
