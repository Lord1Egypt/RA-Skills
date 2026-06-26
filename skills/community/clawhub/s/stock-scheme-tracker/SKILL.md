---
name: stock-scheme-tracker
description: Save and track per-stock investment strategies with entry/exit conditions. Triggers on "保存策略", "跟踪策略", "检查股票策略", "核对建仓条件", "scheme", "stock strategy". Two modes: save (extract strategy from analysis → append to tracking file) and check (evaluate all conditions against user-provided market data, output actionable recommendations).
version: 1.1.0
requires:
  anyBins:
    - python3
    - python
  env:
    - STOCK_SCHEME_PATH
primaryEnv: STOCK_SCHEME_PATH
emoji: 📈
---

# Stock Strategy Tracker 📈

Save per-stock investment strategies extracted from analysis reports into a persistent tracking file, then periodically check if market conditions have triggered any entry, stop-loss, or take-profit conditions. Provide actionable next-step recommendations.

---

## Quick Start

### Install

Copy the skill directory to your agent's skills folder:

```bash
# OpenClaw
cp -r stock-scheme-tracker ~/.openclaw/skills/

# WorkBuddy
cp -r stock-scheme-tracker ~/.workbuddy/skills/

# Claude Code (project-level)
cp -r stock-scheme-tracker .claude/skills/
```

### Configure

Set the environment variable to point to your tracking file:

```bash
# Add to your shell profile (~/.zshrc, ~/.bashrc, etc.)
export STOCK_SCHEME_PATH="$HOME/Documents/stock/scheme.md"
```

Or configure via your agent's config:

```json
// OpenClaw: ~/.openclaw/openclaw.json
{
  "skills": {
    "entries": {
      "stock-scheme-tracker": {
        "env": {
          "STOCK_SCHEME_PATH": "~/Documents/stock/scheme.md"
        }
      }
    }
  }
}
```

If `STOCK_SCHEME_PATH` is not set, the skill defaults to `~/Documents/stock/scheme.md`.

### Verify

```bash
echo $STOCK_SCHEME_PATH
# Should output your configured path
```

---

## Workflow Decision Tree

1. **Determine mode**: Did the user just complete an analysis (→ save mode), or do they want to review existing strategies (→ check mode)?
2. **Save mode**: Extract strategy elements from the analysis, format them, and append to the scheme file.
3. **Check mode**: Read all strategies from the scheme file, fetch latest market data for each stock, evaluate every condition, and output a summary with next-step recommendations.

## Save Mode

### When to Use
- Immediately after completing any stock investment analysis (e.g., DCF valuation, Buffett framework, technical analysis, or any investment report).
- The user says "保存策略", "把策略记下来", "跟踪这个票", "save strategy", "track this stock", or any variant.

### Extraction Rules
From the analysis text, extract these fields. If a field is not mentioned, mark it as "未明确" rather than fabricating.

| Field | Description | Example |
|-------|-------------|---------|
| `stock_code` | Stock code | 688111 |
| `stock_name` | Stock name | 金山办公 |
| `analysis_date` | Analysis date | 2026-04-22 |
| `recommendation` | Core recommendation | 建议观察，等待更好入场时机 |
| `entry_conditions` | Entry conditions (price/valuation/events) | PE≤45-50；股价180-200元 |
| `stop_loss` | Stop-loss condition | 跌破前期低点或技术位 |
| `target_price` | Target price / take-profit range | 机构目标价400元 |
| `exit_signals` | Exit signals (assumption invalidation) | 月活环比下滑；市场份额跌破80% |
| `position_size` | Suggested position size | 轻仓试探 |
| `time_horizon` | Holding period | 3年 |
| `key_assumptions` | Key assumptions | AI商业化持续推进 |
| `open_questions` | Open questions | WPS AI付费转化率是多少 |
| `current_price` | Price at analysis | ~250元 |
| `current_pe` | PE at analysis | 62.46 |
| `market_cap` | Market cap at analysis | 1147亿 |

### Output Format
Append a new section to the scheme file (path from `STOCK_SCHEME_PATH` env var) using the exact format defined in `references/scheme_format.md`. Use Markdown table for entry conditions so they can be machine-parsed later.

### Important
- If the stock already exists in the scheme file, update the existing section rather than duplicating it. Preserve historical entries by appending a date-stamped update note.
- After saving, briefly confirm to the user what was saved.

## Check Mode

### When to Use
- User says "检查策略", "核对建仓条件", "看看哪些票可以买", "策略跟踪", "check strategy", or any variant.
- Can be invoked standalone without any prior analysis.

### Steps
1. Read the scheme file (path from `STOCK_SCHEME_PATH` env var).
2. For each tracked stock, fetch the latest market data (price, PE, key metrics). Use available financial data tools or web search.
3. Evaluate each `entry_conditions` row: compare current value vs target value.
4. Mark each condition as `✅ 已触发`, `❌ 未触发`, or `⚠️ 接近触发`.
5. Check if any `exit_signals` have occurred.
6. Output a clean summary table and specific next-step recommendations per stock.

### Output Format

```markdown
## 策略核对报告 — 2026-04-23

### 金山办公 (688111)
| 条件类型 | 目标 | 当前 | 状态 |
|----------|------|------|------|
| PE建仓 | ≤45-50 | 62.46 | ❌ 未触发 |
| 股价建仓 | 180-200 | 250 | ❌ 未触发 |

**建议**: 继续观察，等待PE回落至50以下或股价跌破200再考虑建仓。
```

## Core Tasks

Here are natural-language prompts that trigger this skill:

- "我刚分析完金山办公，帮我保存策略"
- "检查一下我跟踪的股票，哪些条件触发了"
- "核对建仓条件"
- "跟踪策略"
- "把刚才的分析结论记录到策略跟踪文件"
- "I just finished analyzing Apple, save the strategy"
- "Check all my stock strategies"

## Environment Variable Contract

| Variable | Purpose | Required | Set Via |
|----------|---------|----------|---------|
| `STOCK_SCHEME_PATH` | Path to the strategy tracking Markdown file | No (defaults to `~/Documents/stock/scheme.md`) | Shell profile or agent config |

## Security & Guardrails

1. **Local file only**: Both scripts only read/write a local Markdown file specified by `STOCK_SCHEME_PATH`. No network calls are made by `save_scheme.py` or `check_scheme.py`.
2. **Market data source**: During check mode, market data is fetched via the agent's available financial data tools or web search. This involves querying public market quotes (stock codes and metric names only) — no private strategy content or position details are transmitted.
3. **No trading execution**: This skill provides analysis and recommendations only. It does NOT execute any trades or connect to brokerage accounts.
4. **No credential collection**: This skill only requires `STOCK_SCHEME_PATH` (a file path). It never asks for API keys, tokens, passwords, or any other credentials.
5. **Data integrity**: The save script uses atomic write patterns and preserves historical entries. Existing stock sections are updated in-place rather than overwritten.
6. **Path validation**: The scripts validate that `STOCK_SCHEME_PATH` points to a `.md` file and will create parent directories if needed.

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "No such file or directory" | `STOCK_SCHEME_PATH` not set or points to invalid path | Set env var or rely on default `~/Documents/stock/scheme.md` |
| Strategy not found during check | Scheme file is empty or format is corrupted | Verify the file uses the format in `references/scheme_format.md` |
| Duplicate entries for same stock | Save mode ran twice without updating | The script auto-detects duplicates; if using manual edit, follow the update convention |
| Chinese characters garbled in output | Terminal encoding mismatch | Ensure your terminal uses UTF-8 (`export LANG=en_US.UTF-8` or `zh_CN.UTF-8`) |

## Release Notes

- **1.1.0** — Fixed metadata consistency (top-level requires/env), added credential collection disclaimer, clarified market data query scope in security section.
- **1.0.0** — Initial release. Save and check modes with Markdown-based tracking file.

## Links

- [Scheme Format Reference](references/scheme_format.md)
- [Save Script](scripts/save_scheme.py)
- [Check Script](scripts/check_scheme.py)

## Publisher

* **Publisher:** @dc
* **License:** MIT-0
* **Source:** https://github.com/dc-stock/stock-scheme-tracker
