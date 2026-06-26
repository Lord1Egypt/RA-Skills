---
name: wyckoff
description: Wyckoff A-share analysis agent with full CLI + MCP integration. Detects local CLI installation, guides users through setup (install → register → configure data sources → configure model → optional MCP server), then executes Wyckoff-style volume-price analysis with auditable portfolio decisions. Supports first-time onboarding, daily operational workflows (portfolio management, signal queries, recommendations) via the wyckoff CLI, and 14-tool MCP server for Claude Code / Cursor integration.
---

# Wyckoff Trading Agent

This skill operates in two modes: **Setup** (Step 0) and **Analysis** (Steps 1–9). Step 0 runs only when prerequisites are missing; once everything is configured, jump directly to analysis.

## Step 0: Environment Detection & Guided Setup

Run these checks in order. Stop at the first failure and guide the user to fix it before continuing.

### 0.1 CLI Installation Check

Run `wyckoff --version`.

- **Success** → proceed to 0.2.
- **Failure** → guide installation:
  ```
  pip install youngcan-wyckoff-analysis
  ```
  Or one-line install:
  ```
  curl -fsSL https://raw.githubusercontent.com/YoungCan-Wang/Wyckoff-Analysis/main/install.sh | bash
  ```
  After install, verify with `wyckoff --version` again.

### 0.2 Auth Check

Run `wyckoff auth status`.

- **Logged in** → proceed to 0.3. (Credentials are auto-saved; token expiry triggers automatic re-login.)
- **Not logged in** → guide registration and login:
  1. Tell user to open https://wyckoff-analysis.pages.dev/ to register an account.
  2. After registration, run: `wyckoff auth login <email> <password>` (credentials will be persisted, no need to login again).
  3. Verify with `wyckoff auth status`.

### 0.3 Data Source Check

Run `wyckoff config show`.

- **tushare_token** present → OK.
- **tushare_token** missing → guide:
  - Tushare token is free, get it from https://tushare.pro/ after registration.
  - Then run: `wyckoff config tushare <token>`
- **tickflow_api_key** present → OK.
- **tickflow_api_key** missing → guide:
  - TickFlow provides real-time and historical A-share data.
  - Purchase at: https://tickflow.org/auth/register?ref=5N4NKTCPL4
  - Then run: `wyckoff config tickflow <api_key>`

Note: At least one data source (tushare or tickflow) must be configured. Both are recommended for better coverage.

### 0.4 Model Check

Run `wyckoff model list`.

- **Has models** → proceed to Step 1.
- **No models** → guide: `wyckoff model add` (interactive) or `wyckoff model set <name> <provider> <api_key> --model <model_name>`.

### 0.5 MCP Server Setup (Optional — Ask User)

After all checks pass, **ask the user** whether they want to register the Wyckoff MCP Server with their AI tools (Claude Code / Cursor / etc.).

- **User says yes** → guide:
  ```
  pip install "youngcan-wyckoff-analysis[mcp]"
  claude mcp add wyckoff -- wyckoff-mcp
  ```
  Once registered, the MCP client can directly call 14 Wyckoff tools (diagnose_stock, screen_stocks, get_signal_pending, etc.) without going through the CLI TUI.

  If the user uses a non-Claude MCP client, guide them to add this to their MCP config:
  ```json
  {
    "mcpServers": {
      "wyckoff": {
        "command": "wyckoff-mcp",
        "env": {
          "TUSHARE_TOKEN": "<token_from_wyckoff.json>",
          "TICKFLOW_API_KEY": "<key_from_wyckoff.json>"
        }
      }
    }
  }
  ```
  Credentials already saved in `wyckoff.json` are also auto-read by the MCP server, so env vars are optional if `wyckoff login` + `wyckoff config` have been run.

- **User says no / skip** → proceed directly to analysis.

When all checks pass, print a brief summary and proceed to analysis.

## CLI Operational Commands

When the user's intent is operational (not analysis), route directly to the appropriate CLI command instead of running the analysis pipeline:

| Intent | Command |
|---|---|
| View portfolio | `wyckoff portfolio list` |
| Add position | `wyckoff portfolio add <code> <shares> <cost>` |
| Remove position | `wyckoff portfolio rm <code>` |
| Set cash | `wyckoff portfolio cash <amount>` |
| View signals | `wyckoff signal` |
| View recommendations | `wyckoff recommend` |
| Screen market | `wyckoff screen` |
| Run backtest | `wyckoff backtest <code>` |
| Generate report | `wyckoff report <codes>` |
| Launch dashboard | `wyckoff dashboard` |
| View chat logs | `wyckoff log` |
| Manage memory | `wyckoff memory` |
| Sync cloud data | `wyckoff sync` |
| Cleanup local data | `wyckoff cleanup` |
| Update CLI | `wyckoff update` |
| Register MCP Server | `pip install "youngcan-wyckoff-analysis[mcp]" && claude mcp add wyckoff -- wyckoff-mcp` |

For the full CLI reference, see `rules/cli-setup-guide.md`.

## Input Protocol

Accept any combination of:
- Stock symbol(s), single or multiple.
- `holdings`: `[symbol+cost+qty, ...]`.
- `cash`: available cash amount.
- `candidate`: optional non-holding symbol.
- CSV file(s), image(s), text constraints/goals.

Infer scenario automatically:
- `holdings` non-empty + `candidate`: rotation comparison + per-holding actions.
- `holdings` non-empty + no `candidate`: per-holding add/reduce/hold/exit.
- `holdings` empty + `cash`: empty-position cash deployment.
- No portfolio fields: symbol analysis flow.

Do not require users to explicitly say "switch/add/reduce/empty-position."

## Full Capability Orchestration (Steps 1–9, Required Order)

1. **Parse and normalize inputs.**
   - Normalize symbols to exchange-qualified format when possible.
   - Parse holdings into `{symbol, cost, qty}`.
   - Preserve raw user inputs for output audit.

2. **Acquire current time via system/tool first.**
   - Fetch current timestamp from tool/system.
   - Convert to `Asia/Shanghai`.
   - Print `当前北京时间：YYYY-MM-DD HH:MM（UTC+8）`.

3. **Decide trading availability with authoritative calendar checks.**
   - Judge weekday and continuous-auction windows: `09:30-11:30`, `13:00-15:00` (Beijing time).
   - Query authoritative trading calendar when holiday/adjusted-workday uncertainty exists.
   - If not tradable, downgrade to post-market review + next-session plan + T+1-safe order strategy.

4. **Fetch online data with source fallback.**
   - Follow `rules/source-fallbacks.md` strictly for each symbol.
   - Perform schema and row-count validation before accepting a source.
   - Log fallback attempts and final source per symbol.

5. **Integrate CSV/image modalities when provided.**
   - Use CSV as supplemental historical structure input and reconcile with fetched data.
   - Treat chart images as micro-structure evidence; explicitly acknowledge image reception.
   - Continue analysis if one modality fails and state exact failure cause.

6. **Run Wyckoff structural analysis first.**
   - Analyze latest available window (target 500 trading days) with `MA50`/`MA200`.
   - Identify only evidenced phases/events (SC/ST/Spring/LPS/SOS/UTAD).
   - Use event-date news search only for validation context, never as primary trade logic.

7. **Produce portfolio decisions after structure analysis.**
   - For each holding, output one explicit action: `add / reduce / hold / exit`.
   - If candidate exists, compare against structurally weakest current holding and decide `switch / partial switch / hold`.
   - If holdings are empty and cash exists, output staged cash deployment suggestion.

8. **Render plots only when session rules allow.**
   - Skip plotting during tradable intraday windows.
   - When plotting is allowed, enforce all constraints in `rules/alpha-system-prompt.md`.

9. **Apply capability degrade policy.**
   - Never fabricate OHLCV rows, event timestamps, or trading status.
   - If all sources fail for a symbol, mark `data_unavailable` and continue others.
   - If valid rows < 30, report `insufficient structure depth` and avoid hard phase labels.
   - If image parsing fails, explain reason and continue CSV/text/online path.

For detailed capability-routing policy, read `rules/system-capability-playbook.md`.

## Fixed Output Contract

Always output in this order:
1. `当前北京时间：YYYY-MM-DD HH:MM（UTC+8）`
2. Trading verdict: `当前是否可盘中交易：是/否` (with reason if no).
3. Data audit table per symbol: `symbol`, `source_used`, `rows_kept`, `window_end_date`, `fallback_count`.
4. Wyckoff analysis: current cycle background and phase (only evidenced), key events with rationale, action boundaries respecting T+1.
5. Portfolio action section (portfolio flow only): holdings snapshot, per-holding actions, candidate comparison, cash suggestion, final summary in Wyckoff tone.
6. Plotting section (only when allowed by session rules).

## Hard Constraints

- Do not change the fixed prompt wording unless explicitly requested.
- Do not fabricate missing OHLCV rows.
- Do not ignore image input if image is parseable.
- Do not use opaque white text boxes in chart annotations.
- If fetching data requires running Python scripts, run them only in a sandboxed environment.
- Prefer direct web/API fetch first; use Python scripts only when needed for fallback, parsing, or normalization.

## Resources

- `rules/alpha-system-prompt.md`: fixed role and hard rules.
- `rules/source-fallbacks.md`: online source switching policy.
- `rules/system-capability-playbook.md`: full system capability routing and degrade policy.
- `rules/cli-setup-guide.md`: CLI installation, registration, MCP setup, and command reference.
- GitHub: https://github.com/YoungCan-Wang/Wyckoff-Analysis
