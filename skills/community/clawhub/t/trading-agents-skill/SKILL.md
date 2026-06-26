---
name: trading-agents
description: >
  Orchestrate a swarm of specialized Claude subagents that simulate a professional trading firm
  to analyze stocks and produce trading decisions. Based on the TradingAgents framework (arXiv 2412.20138),
  this skill deploys analyst agents (fundamental, technical, sentiment, news), bull/bear research debaters,
  a trader, a risk manager, and a portfolio manager — all collaborating to produce a comprehensive
  trading recommendation. Use this skill whenever the user asks about stock analysis, trading decisions,
  market research for specific tickers, investment recommendations, portfolio decisions, or wants
  a multi-perspective analysis of any publicly traded security. Also trigger when the user mentions
  "trading agents", "multi-agent trading", "stock swarm", or wants an AI-driven trading desk analysis.
metadata:
  openclaw:
    requires:
      bins: ["python3", "pip", "uv"]
---

# TradingAgents: Multi-Agent Trading Analysis Skill

This skill orchestrates a swarm of Claude subagents that mirror the structure of a real trading firm.
Each agent has a distinct role, specific tools, and a clear mandate. The agents collaborate through
structured reports, adversarial debate, and sequential review — producing a final trading recommendation
that reflects diverse analytical perspectives.

## Prerequisites

This skill requires **Python**, **pip**, and **uv** to be installed on the system. Before running
any analysis, set up the Python environment:

1. Install uv (if not already installed):

   ```bash
   pip install -U uv
   ```

2. Sync the project dependencies from the skill directory:
   ```bash
   cd {SKILL_PATH} && uv sync
   ```
   This installs all required packages (yfinance, akshare, etc.) into a managed virtual environment
   based on `pyproject.toml`. You only need to do this once, or when dependencies change.

All Python scripts in this skill must be executed with `uv run` to ensure they use the correct
environment. For example: `uv run scripts/fetch_market_data.py NVDA`

## Architecture Overview

The system follows a five-stage pipeline inspired by the TradingAgents paper:

```
Stage 1: Analysis (parallel)     → 4 analyst agents gather data simultaneously
Stage 2: Research (debate)       → Bull and bear researchers debate the findings
Stage 3: Trading decision        → Trader synthesizes everything into a signal
Stage 4: Risk review             → Risk manager evaluates the proposed trade
Stage 5: Final approval          → Portfolio manager makes the go/no-go call
```

## How to Use This Skill

When the user asks for a stock analysis or trading decision, follow these steps:

### Step 0: Parse the Request

Extract from the user's message:

- **Ticker(s)**: The stock symbol(s) to analyze (e.g., NVDA, AAPL)
- **Date context**: Whether they want current analysis or historical (default: today)
- **Debate rounds**: If specified, how many bull/bear rounds (default: 1)
- **Focus areas**: Any specific concerns (e.g., "worried about earnings", "considering for long-term hold")

If the ticker is ambiguous or missing, ask the user to clarify.

### Step 1: Launch Analyst Agents (Parallel)

Spawn **four analyst subagents simultaneously** using the Agent tool. Each agent gets its own
prompt from the `agents/` directory. Pass each agent the ticker, date, and any user context.

Read the agent prompts before spawning:

- `agents/fundamental_analyst.md` — Analyzes financial health, valuation, earnings
- `agents/technical_analyst.md` — Analyzes price patterns, indicators, chart signals
- `agents/sentiment_analyst.md` — Gauges market mood from social media and forums
- `agents/news_analyst.md` — Evaluates recent news and macro events

Each analyst should save their report to a working directory. The prompts instruct them on
format and what tools to use (web search, yfinance via the `scripts/fetch_market_data.py` script, etc.).

**Important**: Launch all four in a single message to maximize parallelism. Don't wait for one
to finish before starting the next.

### Step 2: Collect Analyst Reports

Once all four analysts complete, read their reports. Compile them into a single briefing document
that will feed into the research phase.

### Step 3: Bull/Bear Research Debate

Spawn the debate in rounds. For each round:

1. Spawn **bull researcher** and **bear researcher** simultaneously (read `agents/bull_researcher.md`
   and `agents/bear_researcher.md`). Give them all four analyst reports plus any previous debate history.
2. The bull researcher argues for the investment opportunity; the bear researcher argues against.
3. After each round, both researchers can read each other's previous arguments and respond.

Default is 1 round. For deeper analysis, the user can request 2-3 rounds. More rounds means
more thorough analysis but also more time and tokens.

After the debate, spawn the **research manager** (read `agents/research_manager.md`) to synthesize
the debate into a balanced research summary.

### Step 3.5: Compile Debate Record

After the research manager produces the summary, compile a standalone **debate record document**
(`debate_record.md`) that presents the full bull/bear debate process in a clear, readable format.
This document should include:

1. **辩论背景**: The ticker, date, and number of debate rounds
2. **第 N 轮辩论**: For each round, show the bull case followed by the bear case, clearly labeled
3. **研究经理总结**: The research manager's balanced synthesis at the end

This gives the reader a single document to see the entire adversarial debate process,
rather than having to read multiple separate files. The individual bull_case.md, bear_case.md,
and research_summary.md files should still be saved separately as well.

### Step 4: Trading Decision

Spawn the **trader agent** (read `agents/trader.md`). Give it:

- All four analyst reports
- The research debate summary
- The user's original context/constraints

The trader produces a concrete recommendation: BUY, SELL, or HOLD, with position sizing guidance,
entry/exit points, and confidence level.

### Step 5: Risk Management Review

Spawn the **risk manager** (read `agents/risk_manager.md`). Give it:

- The trader's recommendation
- All analyst reports
- Current portfolio context if available

The risk manager evaluates: position size appropriateness, portfolio concentration risk,
volatility assessment, downside scenarios, and liquidity concerns.

### Step 6: Portfolio Manager Approval

Spawn the **portfolio manager** (read `agents/portfolio_manager.md`). Give it everything:

- Analyst reports, debate summary, trader recommendation, risk assessment

The portfolio manager makes the final call: APPROVE, REJECT, or MODIFY the recommendation,
with reasoning.

### Step 7: Compile Final Output

Produce **two outputs**:

1. **A comprehensive report file** (Markdown) saved to the workspace, containing:
   - Executive summary with the final decision
   - Each analyst's key findings (condensed)
   - Bull/bear debate highlights
   - Trader's recommendation details
   - Risk assessment summary
   - Portfolio manager's final decision and reasoning
   - Disclaimer that this is AI-generated analysis, not financial advice

   Additionally, a **debate_record.md** file that compiles the entire bull/bear debate
   process into a single readable document (see Step 3.5).

2. **A conversational summary** in the chat, covering:
   - The final recommendation (BUY/SELL/HOLD)
   - Top 3 reasons for the decision
   - Key risk factors
   - Confidence level
   - Link to the full report

## Configuration Defaults

- **Debate rounds**: 1 (configurable by user, max 5)
- **Data sources**: Web search + yfinance (scripts/fetch_market_data.py) + optional APIs
- **Output**: Both report file + conversational summary

## Helper Scripts

- `scripts/fetch_market_data.py` — Fetches price history, financial statements, and key metrics via yfinance
- `scripts/technical_indicators.py` — Computes common technical indicators (RSI, MACD, Bollinger Bands, moving averages)

These scripts are used by the analyst agents. Run them from the skill directory using `uv run`:

```bash
uv run scripts/fetch_market_data.py <TICKER> [-o OUTPUT_DIR]
uv run scripts/technical_indicators.py <TICKER> [-o OUTPUT_DIR]
```

## Source Citation & Data Quality Standards

All analyst reports must meet these standards:

- **Primary sources first**: Financial data should come from first-hand, authoritative sources:
  company investor relations pages, stock exchange filings (SEC EDGAR, HKEX, SSE/SZSE),
  official earnings releases, and annual/quarterly reports. Third-party aggregators (Yahoo Finance,
  Bloomberg, etc.) are acceptable as supplementary sources but should be labeled as such.

- **Every key data point must cite its source** with a clickable URL, the reporting period
  (e.g., "FY2025", "Q1 2026"), and the currency/unit (e.g., "人民币/百万元", "USD millions").

- **News must come from authoritative media**, prioritized in this order: official company
  announcements > tier-1 financial media (Reuters, Bloomberg, FT, WSJ, 财新, 第一财经) >
  regional authoritative media > industry publications. Each news item must include the
  publication date and a clickable link.

- **Sentiment claims must be attributed** to specific sources with links, not vague statements
  like "market sentiment is bullish." For Chinese/HK stocks, 雪球 (xueqiu.com) should be
  the primary sentiment data source.

- **Technical indicators must include plain-language explanations** so non-expert readers
  can understand what each indicator means and why it matters.

- **Industry-specific analysis is required**: Analysts and risk managers must go beyond
  generic metrics and cover sector-specific KPIs. For example:
  - Banking: capital adequacy ratio, NPL ratio, provision coverage ratio, NIM
  - E-commerce: GMV, take rate, MAU/DAU, customer acquisition cost
  - Consumer electronics: supply chain, market share trends, component cost analysis
  - Automotive/EV: monthly delivery/sales data (12–36 months), competitive comparison
  - Insurance: NBV, embedded value, combined ratio, solvency ratio
  - Multi-segment companies: break down by segment with relevant industry metrics for each

## Important Notes

- **Not financial advice**: Always include a disclaimer in both the report and the summary. This is an AI research tool for educational purposes.
- **Data freshness**: yfinance data may have delays. Web search helps get the latest news.
- **Cost awareness**: Each analysis spawns 8-12+ subagents. For users analyzing multiple tickers, suggest doing them one at a time or warn about the computational cost.
- **Error handling**: If an analyst agent fails (e.g., can't find data), note the gap in the final report rather than blocking the entire pipeline. The system should be resilient to partial failures.
- **No internal paths in reports**: Never include internal file system paths (e.g., `/sessions/...`, `/tmp/...`, working directory paths) in any report that the reader will see. These are implementation details. Reports should reference other reports by filename only (e.g., "详见 fundamental_analysis.md"), not by absolute path.
