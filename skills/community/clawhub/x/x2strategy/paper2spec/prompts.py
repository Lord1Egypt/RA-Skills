"""Prompt templates for structured extraction.

Each prompt takes a ``{context}`` variable (retrieved paper chunks)
and returns a natural-language description of the target section.

The multi-layer extraction prompts (LAYER_*) are used by the extractor
to produce a full StrategySpec through 4 focused LLM calls.
"""

SYSTEM_PROMPT = (
    "You are an expert quantitative researcher and algorithmic trader. "
    "Extract precise, structured information from academic finance papers. "
    "Be rigorous — prefer exact values from the paper over guessed defaults."
)

METHODOLOGY_PROMPT = """Synthesize the trading strategy methodology from the provided text.

Context from paper:
{context}

Instructions:
1. Describe the core trading idea (e.g., Momentum, Mean Reversion, Factor-based, Pairs Trading).
2. Explain the step-by-step process of the strategy — how signals are generated, how portfolios are formed.
3. Detail how the portfolio is constructed (weighting scheme, rebalancing frequency, long/short structure).
4. Identify whether this is a time-series strategy (per-asset over time) or cross-sectional strategy (across assets).
5. Note any formulas, equations, or mathematical definitions used.
6. Focus on the core strategy; ignore literature review unless it defines the strategy.

Output a clear, structured description of the methodology (3-5 paragraphs).
Include specific parameter values, thresholds, and calculation details when mentioned."""

SIGNAL_LOGIC_PROMPT = """Extract precise trading rules and signal logic from the text.

Context from paper:
{context}

Extract the following with maximum specificity:
1. **Entry conditions**: When to buy/go long — exact indicator thresholds, crossover conditions, ranking criteria
2. **Exit conditions**: When to sell/close — time-based, signal-reversal, stop-loss, take-profit
3. **Technical indicators**: Name, calculation period, parameters (e.g., RSI(14), SMA(200), MACD(12,26,9))
4. **Fundamental factors**: Accounting ratios (P/E, B/M, ROE), factor definitions, data transformations
5. **Sorting/ranking procedures**: Quantile sorts, double sorts, conditional sorts — number of groups, breakpoint methodology
6. **Threshold values**: Exact numeric thresholds, percentile cutoffs, z-score boundaries
7. **Holding period and rebalancing**: How long positions are held, when portfolios are reformed
8. **Data requirements**: Price fields (Close, Open, High, Low, Volume), fundamental fields, frequency

Be precise — extract exact formulas, parameter values, and conditional logic.
If the paper uses multiple strategy variants, describe each one."""

DATA_DESCRIPTION_PROMPT = """Extract data requirements and sample description from the text.

Context:
{context}

Identify with specificity:
1. **Data sources**: CRSP, Compustat, Yahoo Finance, FRED, Bloomberg, Datastream, etc.
2. **Asset universe**: S&P 500, NYSE/AMEX/NASDAQ, all US stocks, international markets, specific sectors
3. **Time period**: Exact start and end dates (e.g., January 1963 to December 2019)
4. **Data frequency**: Daily, Weekly, Monthly — and whether returns or prices are used
5. **Selection/filter criteria**: Price filters (>$5), market cap filters (>$100M), exchange filters, industry exclusions
6. **Fundamental data fields**: All accounting variables used (Book-to-Market, Operating Profitability, Investment, etc.)
7. **Alternative data**: Macro indicators, sentiment scores, analyst forecasts, options data
8. **Benchmark**: Market index used for comparison (S&P 500, CRSP value-weighted, Russell 2000)

Be comprehensive — list ALL data sources and filters mentioned in the paper."""

# ═══════════════════════════════════════════════════════════════
# Layer 0: Strategy Detection (multi-strategy pre-scan)
# ═══════════════════════════════════════════════════════════════

LAYER0_STRATEGY_DETECTION_PROMPT = """Analyze this research paper and determine how many INDEPENDENT trading strategies it proposes.

PAPER TITLE: {title}

ABSTRACT:
{abstract}

METHODOLOGY:
{methodology}

SIGNAL LOGIC:
{signal_logic}

INSTRUCTIONS:
A paper may contain multiple independent strategies. Count them carefully:

**Multiple strategies** exist when the paper:
- Proposes distinct strategy approaches that use different indicators or logic (e.g., "Value" vs "Momentum")
- Tests multiple selection methods that are independently implementable (e.g., distance method, cointegration method, stationarity-based method)
- Covers multiple asset classes with fundamentally different signal generation logic

**Single strategy** when:
- The paper has one core idea, even if it tests parameter robustness (different lookback windows)
- Multiple tables just show sub-period or regional breakdown of the SAME strategy
- The paper mixes long-only and long-short versions of the same signal — that's one strategy with two execution plans, not two strategies

Return JSON:
{{
    "num_strategies": <integer>,
    "strategies": [
        {{
            "name": "Short descriptive name",
            "strategy_type": "technical|fundamental|hybrid|multi_asset",
            "brief_description": "1-3 sentences describing the core idea",
            "differentiation": "How this strategy differs from others in the paper (empty if only 1)",
            "key_section_hints": ["Section names, table refs, or formulas relevant to this strategy"]
        }}
    ]
}}

CRITICAL RULES:
1. Be conservative — when in doubt, treat it as ONE strategy. False splits are worse than missing a split.
2. Parameter variations (e.g., 3-month vs 12-month momentum) are NOT separate strategies.
3. Each strategy must be independently implementable with different signal logic.
4. Order strategies by importance/prominence in the paper (main strategy first).

Output ONLY valid JSON."""

# ═══════════════════════════════════════════════════════════════
# Stage 2: Multi-layer specification extraction prompts
# (4 focused LLM calls instead of 1 monolithic call)
# ═══════════════════════════════════════════════════════════════

LAYER1_METADATA_AND_DATA_PROMPT = """Extract strategy metadata and data requirements from this research paper.

PAPER TITLE: {title}
{strategy_focus}
ABSTRACT:
{abstract}

METHODOLOGY:
{methodology}

DATA DESCRIPTION:
{data_description}

Extract as JSON:
{{
    "strategy_name": "Concise descriptive name based on paper content",
    "strategy_type": "technical|fundamental|hybrid|multi_asset",
    "asset_class": ["equity", "bonds", "commodities", "crypto", "forex"],
    "description": "2-4 sentence summary of the core trading idea",
    "price_data": true,
    "volume_data": false,
    "fundamental_data": ["P/E", "ROE", "Book-to-Market"],
    "alternative_data": ["FRED-MD macro factors", "sentiment"],
    "lookback_period": 252,
    "data_frequency": "daily|weekly|monthly",
    "data_source": "e.g., CRSP, Yahoo Finance",
    "time_period": "e.g., 1963-2019",
    "universe_assets": ["US equities"],
    "universe_selection_criteria": "e.g., NYSE/AMEX common stocks, price > $5",
    "expected_sharpe": null,
    "expected_return": null,
    "max_drawdown": null,
    "expected_performance": {{}}
}}

INSTRUCTIONS:
1. strategy_type: "technical" (price/volume only), "fundamental" (accounting data), "hybrid" (both), "multi_asset" (multiple asset classes)
2. fundamental_data: List ALL accounting/financial metrics explicitly used (not just mentioned)
3. alternative_data: External/non-traditional data (macro, sentiment, analyst forecasts)
4. lookback_period: In trading days (252 ≈ 1 year, 126 ≈ 6 months, 21 ≈ 1 month)
5. universe_selection_criteria: Be comprehensive — include ALL filters (price, market cap, exchange, industry exclusions)
6. expected_*: Extract from MAIN results table only; use null if not reported; annual_return as decimal (0.12 = 12%)
7. If a field is not mentioned in the paper, use null or empty — do NOT guess

Output ONLY valid JSON."""

LAYER2_INDICATORS_PROMPT = """Extract all indicators, factors, and computed signals used in this trading strategy.

STRATEGY CONTEXT:
Name: {strategy_name}
Type: {strategy_type}
Description: {description}
{strategy_focus}
SIGNAL LOGIC FROM PAPER:
{signal_logic}

METHODOLOGY FROM PAPER:
{methodology}

Extract as JSON:
{{
    "indicators": [
        {{
            "indicator_id": "lowercase_underscore_id",
            "name": "Human-readable name",
            "category": "technical|fundamental|derived",
            "formula": "Clear natural language description of the calculation",
            "latex": "LaTeX formula if applicable, e.g., r_{{i,t-12:t-1}}",
            "inputs": ["close", "volume", "book_value", "market_cap"],
            "parameters": {{"window": 252, "threshold": 0.5}},
            "scope": "time_series|cross_sectional",
            "output_type": "scalar|boolean|ranking"
        }}
    ]
}}

INDICATOR CATEGORIES:
- **technical**: Computed from price/volume data (SMA, RSI, MACD, momentum returns, volatility)
- **fundamental**: Computed from accounting/financial data (P/E, Book-to-Market, ROE, Operating Profitability)
- **derived**: Combination of multiple indicators or transformations (composite scores, z-scores, residuals)

SCOPE:
- **time_series**: Computed per asset over time (e.g., 12-month return for stock X)
- **cross_sectional**: Computed across assets at a point in time (e.g., rank all stocks by P/E)

OUTPUT TYPE:
- **scalar**: Numeric value (returns, ratios, z-scores)
- **boolean**: True/False signal (RSI < 30)
- **ranking**: Ordinal ranking across assets (1st, 2nd, ...)

INSTRUCTIONS:
1. Extract ALL indicators explicitly used in the strategy — not just mentioned in passing
2. indicator_id: Use descriptive lowercase format (e.g., "momentum_12m", "book_to_market", "rsi_14")
3. formula: Describe precisely HOW the indicator is calculated step-by-step
4. inputs: List exact data fields needed (close, open, high, low, volume, book_value, earnings, etc.)
5. parameters: Include all tunable values with defaults from the paper
6. If a formula involves intermediate steps, describe the full calculation chain

Output ONLY valid JSON."""

LAYER3_LOGIC_PIPELINE_PROMPT = """Extract the logic pipeline that transforms indicators into final trade signals.

STRATEGY: {strategy_name}
TYPE: {strategy_type}
{strategy_focus}
AVAILABLE INDICATORS:
{indicators_summary}

SIGNAL LOGIC FROM PAPER:
{signal_logic}

METHODOLOGY FROM PAPER:
{methodology}

Extract as JSON:
{{
    "logic_pipeline": [
        {{
            "step_id": "step1",
            "description": "What this step does",
            "function": "filter|rank|quantile_sort|group_quantile_sort|condition|threshold|crossover|arithmetic|z_score|custom",
            "scope": "time_series|cross_sectional|within_group",
            "group_by": "",
            "inputs": ["indicator_id_or_prior_step_output"],
            "parameters": {{"n_quantiles": 5, "threshold": 0.5}},
            "expression": "Natural language or pseudo-code expression",
            "output": "output_variable_name",
            "output_type": "label|boolean|scalar|ranking"
        }}
    ]
}}

FUNCTION TAXONOMY:

## Cross-sectional Operations (across all assets at one point in time):
- **filter**: Remove assets based on condition (e.g., "keep if price > $5, market cap > $100M")
- **rank**: Rank all assets by indicator value (output: 1, 2, 3...)
- **quantile_sort**: Sort assets into N quantiles/groups (output: "Q1", "Q2", ..., "Qn")
- **group_quantile_sort**: Sort WITHIN groups from a prior step (scope: within_group, group_by: prior_output)
- **z_score**: Standardize indicator values across assets at each time point

## Time-series Operations (per asset over time):
- **condition**: Boolean or categorical check (e.g., "if close > SMA_200") → output_type: boolean or label
- **threshold**: Classify into categories based on numeric thresholds → output_type: label
- **crossover**: Detect signal crossovers (e.g., "SMA_50 crosses above SMA_200") → output_type: boolean

## General Operations:
- **arithmetic**: Mathematical combination of indicators (e.g., "indicator_A - indicator_B")
- **custom**: Any other logic — describe clearly in expression

OUTPUT TYPES:
- **label**: Categorical ("Q1", "long_target", "oversold", "value_stock")
- **boolean**: True/False
- **scalar**: Numeric value
- **ranking**: Integer rank (1, 2, 3...)

MULTI-DIMENSIONAL STRATEGIES (Double/Triple Sort):
For strategies with multiple sorting dimensions:
1. Step N-2: First sort (quantile_sort → factor_a_quintile)
2. Step N-1: Second sort WITHIN groups (group_quantile_sort, group_by: factor_a_quintile)
3. Step N (FINAL): Combine into trade signal using condition function

Example double-sort:
  step1: quantile_sort by book_to_market → value_quintile (Q1..Q5)
  step2: group_quantile_sort by momentum WITHIN value_quintile → momentum_decile (D1..D10)
  step3: condition → IF value_quintile='Q1' AND momentum_decile='D10' THEN 'long_target'

CRITICAL RULES:
1. The FINAL step must produce an actionable trade signal (long/short/hold), not an intermediate classification
2. step_id must be sequential (step1, step2, ...)
3. Each step's inputs must reference either indicator_ids or prior step outputs
4. Include ALL intermediate steps — don't skip from raw indicators to final signal
5. For sorting strategies: specify n_quantiles, breakpoint methodology
6. expression field: Write clear pseudo-code showing the exact logic

Output ONLY valid JSON."""

LAYER4_EXECUTION_PROMPT = """Extract the execution plan and risk management rules.

STRATEGY: {strategy_name}
TYPE: {strategy_type}
{strategy_focus}
LOGIC PIPELINE (available signals):
{logic_summary}

DATA DESCRIPTION:
{data_description}

METHODOLOGY:
{methodology}

Extract as JSON:
{{
    "execution_plan": [
        {{
            "plan_id": "exec_1",
            "description": "Description of this execution plan",
            "trigger": {{
                "trigger_type": "time_driven|signal_driven",
                "frequency": "daily|weekly|monthly|end_of_month|quarterly",
                "signal_lookup": "signal_name_if_signal_driven",
                "delay_bars": 1,
                "price_type": "open|close|vwap"
            }},
            "action": {{
                "signal_source": "final_signal_from_pipeline",
                "logic": "WHEN 'long_target': LONG; WHEN 'short_target': SHORT",
                "default_action": "hold"
            }},
            "position_sizing": {{
                "method": "equal_weight|quantile_based|signal_based|volatility_scaled",
                "max_position_pct": 0.1,
                "total_exposure": 1.0,
                "long_short": "long_only|short_only|long_short"
            }}
        }}
    ],
    "risk_management": [
        "Rule description (e.g., Stop loss at -10%)",
        "Position limit per asset",
        "Maximum sector exposure 25%"
    ]
}}

ACTION LOGIC FORMAT (pseudo-code):
  WHEN 'signal_value': ACTION [on TARGET]
  Examples:
    "WHEN 'Q1': LONG; WHEN 'Q5': SHORT"
    "WHEN long_signal=True: LONG; WHEN long_signal=False: EXIT"
    "WHEN spread_zscore < -2: LONG stock_A, SHORT stock_B; WHEN |zscore| < 0.5: CLOSE ALL"

INSTRUCTIONS:
1. trigger_type: "time_driven" for calendar-based rebalancing, "signal_driven" for indicator-triggered
2. frequency: Match the paper's rebalancing frequency (most academic papers use monthly or quarterly)
3. delay_bars: Set to 1 for lookahead bias prevention (execute next bar after signal)
4. signal_source: Reference the FINAL output from the logic pipeline
5. logic: Use pseudo-code describing which signal values trigger which actions
6. method: "equal_weight" is default for academic strategies; use paper's method if specified
7. long_short: "long_only" if paper only tests long positions, "long_short" if both
8. risk_management: Extract any stop-loss, position limits, drawdown constraints mentioned
9. If the paper doesn't specify a rule, use null or omit — don't fabricate constraints

Output ONLY valid JSON."""

# ═══════════════════════════════════════════════════════════════
# Legacy: single-call specification prompt (kept for backward compat)
# ═══════════════════════════════════════════════════════════════

SPECIFICATION_PROMPT = """Convert the extracted paper content into a precise, executable strategy specification.

Title: {title}
Methodology: {methodology}
Signal Logic: {signal_logic}
Data Description: {data_description}

Map the information into a JSON object with the following structure:

{{
  "strategy_name": "<concise name>",
  "strategy_type": "technical | fundamental | hybrid",
  "asset_class": ["equity"],
  "description": "<one-paragraph summary>",
  "price_data": true,
  "volume_data": false,
  "fundamental_data": [],
  "alternative_data": [],
  "lookback_period": 200,
  "data_frequency": "daily",
  "data_source": "",
  "time_period": "",
  "universe_assets": [],
  "universe_selection_criteria": "",
  "expected_sharpe": null,
  "expected_return": null,
  "max_drawdown": null,
  "indicators": [
    {{
      "indicator_id": "ind_1",
      "name": "SMA",
      "category": "technical",
      "formula": "Simple moving average of close prices",
      "inputs": ["close"],
      "parameters": {{"window": 20}},
      "scope": "time_series",
      "output_type": "scalar"
    }}
  ],
  "logic_pipeline": [
    {{
      "step_id": "step_1",
      "description": "...",
      "function": "condition",
      "scope": "time_series",
      "inputs": ["ind_1"],
      "parameters": {{}},
      "expression": "close > SMA_20",
      "output": "long_signal",
      "output_type": "boolean"
    }}
  ],
  "execution_plan": [
    {{
      "plan_id": "exec_1",
      "description": "...",
      "trigger": {{
        "trigger_type": "time_driven",
        "frequency": "daily",
        "delay_bars": 1,
        "price_type": "open"
      }},
      "action": {{
        "signal_source": "long_signal",
        "logic": "if long_signal: buy; else: sell",
        "default_action": "hold"
      }},
      "position_sizing": {{
        "method": "equal_weight",
        "total_exposure": 1.0,
        "long_short": "long_only"
      }}
    }}
  ],
  "risk_management": []
}}

Return ONLY the JSON object, no additional text."""
