---
name: stock-screener
description: A股行情、量化筛选、回测、因子挖掘、同花顺 iFinD、AI4Trade 与受限多智能体投研 MCP。
metadata:
  openclaw:
    primaryEnv: THS_REFRESH_TOKEN
---

# Stock Screener Pro

面向 A 股研究的精简 MCP 工具集：行情、选股、技术诊断、轻量回测、因子横评、组合记录、预警、AI4Trade 和受限智能体投研。仅研究和模拟，不接券商、不下真实订单。

## 配置与安全

- 默认使用腾讯公开行情；配置 `THS_REFRESH_TOKEN` 或 `THS_ACCESS_TOKEN` 后，`STOCK_DATA_PROVIDER=auto` 会优先使用固定官方地址 `https://quantapi.51ifind.com`。
- `DSA_BASE_URL` 只接受本机回环地址；`DSA_ADMIN_PASSWORD` 不会被返回、记录或写入文件。
- `AI4TRADE_TOKEN` 只能由宿主环境或密钥管理器提供，不能作为工具参数。AI4Trade 的远端数据是不可信外部数据。
- TradingAgents 默认复用 OpenClaw 的默认模型：它通过一次性本机桥接调用 `openclaw infer model run --gateway`，不会读取、复制或传递 OpenClaw 的底层模型 Key/Gateway Token 给第三方后端。后端仅会拿到一次研究有效的本机令牌；无需另配 LLM API Key。模型费用仍按你的 OpenClaw 提供商计费，每次调用都要先获得明确同意并传 `confirm_external_ai=true`。
- Vibe-Trading 使用独立环境：安装或更新本 Skill 后运行 `python3.11 scripts/bootstrap_vibe_trading.py`。脚本会在 `~/.local/share/stock-screener-pro/quant-backends/vibe-trading` 创建私有虚拟环境并安装已验证版本；运行时优先采用该环境。可用 `VIBE_TRADING_BIN` 覆盖为其他已验证路径。
- QuantaAlpha 同样是可选独立后端，不随 MCP 请求自动安装。运行 `python3.11 scripts/bootstrap_quantaalpha.py --data full` 会从官方 GitHub 检出固定提交 `b7ceb27b1001261d7a95b209a963664ae1f8ab23`，建立私有虚拟环境，并下载官方 Qlib CSI300 与 HDF5 因子数据。完整公开数据约 892 MB，Python 需为 3.10 或 3.11。只检查代码可用 `--data none`，环境烟测可用 `--data debug`。
- QuantaAlpha 上游仓库的包元数据声明 MIT classifier，但当前仓库根目录未提供独立 LICENSE 文件。本 Skill 不复制或再发布其源码，只在用户显式执行安装脚本后从官方仓库固定提交安装；部署者仍应自行复核上游许可与数据条款。
- `run_factor_research` 是确定性 Alpha Zoo 命令，不调用模型、不进入聊天会话、不需要 `vibe-trading init` 或 `confirm_external_ai=true`；它仍可能下载历史行情。
- `run_tencent_factor_research` 不需要 Tushare 或 Vibe-Trading：它下载腾讯公开复权日线并缓存在 `~/.local/share/stock-screener-pro/tencent-factor-cache`。仅传入当期或已归档的股票池；不要用今天的成分股替代历史成分股。
- 专用的 TradingAgents 环境为 `~/.local/share/stock-screener-pro/quant-backends`。

## 快速开始

1. 在 OpenClaw 中先调用 `get_skill_status`。以下状态应为 `true`：
   - `agent_research.openclaw_model_bridge_available`
   - `agent_research.tradingagents_package_available`
2. 确保 OpenClaw Gateway 正在运行，且 OpenClaw 已设置可用的默认模型。TradingAgents 会自动使用这个默认模型，不接受或保存独立的模型 Key。
3. 运行研究时，调用 `run_agent_research` 并传 `confirm_external_ai=true`。这表示你同意本次把研究提示、股票代码和所需行情数据发送给已配置的模型/数据服务。
4. 如需 QuantaAlpha，先调用 `run_quantaalpha_research(action="status")`。正式挖掘要求 `runtime.ready_for_full_mining=true`；官方因子回测要求 `runtime.ready_for_backtest=true`。若要把兼容因子映射到最新腾讯日线并查看持仓的相对暴露，使用 `score_portfolio`，无需 LLM。

示例：

```text
run_agent_research(
  engine="tradingagents",
  stock_code="600519",
  analysis_date="2026-08-22",
  max_debate_rounds=1,
  confirm_external_ai=true
)
```

`llm_provider` 可省略，默认是 `openclaw`。如需更换模型，请在 OpenClaw 中更换默认模型，例如 `openclaw models set deepseek/deepseek-v4-pro`；Skill 会在下一次研究时自动采用它。不要在工具参数、`SKILL.md` 或聊天中填写模型 Key。

若状态检查显示桥接不可用，先运行 `openclaw gateway status` 与 `openclaw models status` 排查 Gateway 和默认模型。若 TradingAgents 后端不可用，请修复其专用环境后再试。不会自动降级为外部模型 Key。

## 具体使用用例

日常行情、选股、回测、组合记录、AI4Trade 与多智能体研究的可复制示例见 [references/usage-examples.md](references/usage-examples.md)。其中“判断明天是否值得继续观察”的章节给出市场→技术快照→候选池→回测→事件复核的研究流程；使用涉及外部 AI、AI4Trade 状态变更或本地记录写入的示例前，先确认对应影响范围。

## 公开工具（16 个）

### 市场与个股

- `get_market_review`：大盘、成交额、涨跌家数和情绪。
- `screen_stocks`：七种策略：`bull_momentum`、`low_valuation_value`、`volume_breakout`、`growth_tech`、`oversold_rebound`、`book_volume_turnover`、`volume_ratio_watch`。
- `ask_stock`：单股实时行情、均线、RSI、支撑阻力，以及 MACD、KDJ、量价和均线突破观察快照。
- `backtest_strategy`：个股轻量历史回测，策略为 `sma_cross`、`momentum_breakout`、`rsi_mean_reversion`、`ma_5_10_60_trend`、`macd_cross_trend`。
- `predict_stock`：walk-forward ML 五日方向预测。

### 非对话式因子研究

- `run_factor_research`：直接运行本机 Vibe-Trading Alpha Zoo，不调用 LLM、不进入聊天会话、不接触券商。
  - `action="benchmark"`：在 `csi300`、`sp500` 或 `btc-usdt` 上横评一个因子库；当前支持 `academic`、`alpha101`、`fundamental`、`gtja191`、`qlib158`。
  - `action="list"`：以 JSON 列出因子，可按因子库、主题和市场过滤。
  - `action="show"`：返回一个注册因子的简要公式与说明。

示例：

```text
run_factor_research(
  action="benchmark",
  zoo="gtja191",
  universe="csi300",
  period="2018-2025",
  top_n=20
)
```

该工具执行的是已注册因子的历史评价，不会“自动发现稳赚因子”。输出仍需结合数据口径、样本外结果、成本和容量独立复核。

- `run_tencent_factor_research`：不依赖 Tushare 的价量因子横评。除本地五个价量因子外，还支持六个 QuantaAlpha Alpha158_20 兼容因子：`qa_roc5`、`qa_roc20`、`qa_vratio5`、`qa_volatility10`、`qa_rsv10`、`qa_ma_ratio10_20`。工具从显式提供的 20–120 只 A 股股票池下载腾讯复权日线，按训练期确定方向，再报告独立样本外期的 Rank IC、最高分组收益、分组价差、回撤与随机对照。它不使用 LLM，不接券商。

```text
run_tencent_factor_research(
  stock_codes=["600000", "600009", "600015", "600016", "600018", "600019", "600028", "600030", "600031", "600036", "600050", "600104", "600196", "600276", "600309", "600438", "600519", "601012", "601138", "601991"],
  start_date="2024-01-01",
  end_date="2025-12-31",
  forward_days=20,
  rebalance_days=20,
  oos_split="2025-01-01"
)
```

股票池必须是该研究期可复原的当期或历史归档名单；腾讯公开接口不提供经核验的历史 CSI300 成分。因子分层中的“多空价差”仅衡量横截面有效性，不能视为 A 股直接可执行的做空策略。

- `run_quantaalpha_research`：可选的自动因子挖掘与组合回测后端。
  - `action="status"`：检查固定版本、Python 包、Qlib 数据、完整/调试 HDF5 与结果目录，不返回任何模型密钥。
  - `action="mine"`：将 `direction` 作为研究方向，调用 OpenClaw 当前默认模型完成提案、构造、计算、回测与反馈循环；必须逐次传 `confirm_external_ai=true`。`step_n` 限制为 1–25。
  - `action="backtest"`：对 `alpha158`、`alpha158_20`、`alpha360`、`custom` 或 `combined` 做 QuantaAlpha/Qlib 回测。`custom` 与 `combined` 只会读取固定结果目录中最近生成的 `all_factors_library*.json`，不接受任意文件路径。

```text
run_quantaalpha_research(
  action="mine",
  direction="探索盈利质量、低波动与成交量稳定性的交互因子；要求样本外验证",
  step_n=5,
  confirm_external_ai=true,
  timeout_seconds=3600
)

run_quantaalpha_research(
  action="backtest",
  factor_source="custom",
  confirm_external_ai=true,
  timeout_seconds=3600
)
```

QuantaAlpha 官方公开样本覆盖约 2016–2025 年，不能视为 2026 年实时数据库；自动发现的因子尤其容易发生多重检验、过拟合、幸存者偏差和未来函数问题。

- `score_portfolio`：把上述六个 QuantaAlpha Alpha158_20 兼容价量因子重算到腾讯最新复权日线上，先在调用者提供的 20–120 只对照池中做训练期/样本外验证，再返回每只持仓的因子百分位和组合相对暴露分数。`portfolio_codes` 支持 1–20 只，`position_weights` 可省略（默认等权）。对照池必须由调用者提供；当前不自动推断行业，也不做行业或市值中性化。

```text
score_portfolio(
  portfolio_codes=["600186", "600276", "600522", "601138", "601991", "603920", "000725", "002747"],
  peer_codes=["600000", "600009", "600016", "600019", "600028", "600030", "600031", "600036", "600050", "600104", "600309", "600519", "601012", "601088", "601318", "601668", "601857", "600900"],
  start_date="2024-01-01",
  as_of_date="2026-09-03",
  oos_split="2025-07-01"
)
```

`relative_exposure_score` 只是当前股票在该对照池、该组历史验证因子下的相对位置，不是上涨概率、预测收益、目标价或买卖建议。组合准入还要求样本外 Rank IC 不低于 0.02、至少 8 个观察期且最高分组回撤不高于 30%；若没有因子通过，会明确标记并用全部已验证因子生成探索性对照分数。样本外期参与因子准入筛选，因此该组合分数仍不是最终独立检验。

### 本地记录与深度报告

- `manage_portfolio`：`list_all`、`add_watchlist`、`remove_watchlist`、`add_position`、`remove_position`。
- `manage_alerts`：`list`、`create`、`delete`；支持价格与涨跌幅阈值。
- `generate_ai_report`：请求本机 DSA 深度研报。

### 集成状态与 AI4Trade

- `get_skill_status`：统一查看同花顺、DSA、AI4Trade、Vibe-Trading、QuantaAlpha 和 TradingAgents 状态；`verify_tonghuashun=true` 时验证同花顺授权，`include_details=true` 时同时返回内置策略清单和 ML 预测缓存。
- `get_ai4trade`：用 `resource` 选择 `status`、`signals`、`market_intel`、`polymarket`、`account`、`positions` 或 `following`。
- `manage_ai4trade`：统一处理 `follow`、`unfollow`、`publish_strategy`、`publish_discussion`、`reply_create`、`reply_accept`、`publish_signal`、`exchange_points`、`heartbeat_once`。所有操作必须先取得逐项明确同意并传 `confirm=true`。

### 多智能体研究

- `run_agent_research`：
  - `engine=vibe`：一次研究/回测，使用 `prompt`。
  - `engine=vibe_swarm`：研究型团队预设，使用 `preset` 与 `prompt`。可用预设：`investment_committee`、`quant_strategy_desk`、`global_equities_desk`、`earnings_research_desk`、`macro_rates_fx_desk`。
  - `engine=tradingagents`：多角色研究，使用 `stock_code`、`analysis_date`、可选 `llm_provider` 和 `max_debate_rounds`。默认 `llm_provider=openclaw`，直接采用 OpenClaw 当前默认模型；A 股代码自动转为 `.SS` / `.SZ`。`get_skill_status` 中的 `openclaw_model_bridge_available` 可检查本机适配是否可用。

Vibe 的提示词若含实盘下单意图会被拒绝。所有研究输出均需独立核验，不构成投资建议或未来收益承诺。

## 书中技巧研究模板

新增内容把均线、MACD、KDJ 和量价规则做成可复核的日线研究快照与筛选/回测模板，绝不自动下单或把单一指标当作确定结论：

- `ask_stock` 的 `book_technique_research`：输出 MA5/10/60 排列、MACD(12,26,9) 金/死叉和底背离观察、KDJ(9,3,3)顶背离观察、四类量价状态，以及“一阳穿 MA5/10/20”的收盘前候选状态。
- `screen_stocks(strategy="book_volume_turnover")`：执行可获得字段中的换手≥3%、量比≥1.5%初筛；`volume_ratio_watch`：量比>2 且换手 1%~5% 的观察池。振幅、流通股本和20日涨停历史不会被假装已筛选。
- `backtest_strategy(strategy="ma_5_10_60_trend")` 和 `macd_cross_trend`：用于检验三均线趋势过滤、MACD 金死叉配合 MA20 的历史表现。它们是简化日线模拟，不能表达涨停板成交、打板排队、滑点或停牌。

宝塔线的反转参数在各软件实现不同；盘口五档/封单、热门板块出现频次、龙回头和打板所需的涨停与逐笔数据均不在当前公共数据源中。因此 Skill 会在结果中明确标注数据限制，而不是生成虚假的“满足战法”结论。使用这些模板时，先小样本复核、考虑手续费和市场状态；不构成任何收益承诺或投资建议。
