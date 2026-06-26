# System Capability Playbook

Use this file to force stable use of the full system capability set.

## Capability Routing Matrix

1. Time capability
- Trigger: Any request requiring "today/now/盘中/收盘后/明天" interpretation.
- Action: Read system/tool current time, convert to `Asia/Shanghai`, then decide session state.
- Fallback: If calendar ambiguity exists, query authoritative trading calendar before giving trade-time verdict.

2. Online retrieval capability
- Trigger: Symbol analysis, near-current context, or trading-day validation.
- Action: Fetch OHLCV with source fallback from `rules/source-fallbacks.md`, then run completeness checks.
- Fallback: Continue with remaining symbols and mark failed symbols as `data_unavailable`.

3. Structured parsing capability
- Trigger: User provides holdings/cash/candidate in free text.
- Action: Parse into typed fields `{symbol, cost, qty, cash, candidate}` and infer scenario automatically.
- Fallback: If one field is missing, continue with available fields and state missing assumptions explicitly.

4. CSV processing capability
- Trigger: CSV file exists.
- Action: Parse dates/numeric columns, map into canonical OHLCV schema, reconcile with online window.
- Fallback: If malformed CSV, explain parse issue and continue online path.

5. Image understanding capability
- Trigger: K-line, intraday, or chart screenshot exists.
- Action: Perform independent micro-structure interpretation and merge with structural conclusion.
- Fallback: If unreadable image, state reason and continue with text/CSV/online inputs.

6. Local compute + Python capability
- Trigger: Need indicator computation, consistency checks, or chart rendering.
- Action: Compute MA50/MA200 and structural diagnostics; render chart only when session rule allows.
- Fallback: If environment blocks plotting, still provide full textual decision with explicit omission reason.

7. Web/news validation capability
- Trigger: Need explanation of abnormal event-date volume/price behavior.
- Action: Search targeted event windows only for validation annotations.
- Fallback: If unavailable, keep structural decision unchanged and note validation gap.

## Multi-Input Priority

Apply this precedence when evidence conflicts:
1. Cleaned OHLCV structure (online + validated CSV)
2. Session and calendar constraints (time rules)
3. Image micro-structure clues
4. Event-date news annotations

Never allow layer 4 to override layers 1-3.

8. CLI orchestration capability
- Trigger: User wants to install, configure, manage portfolio, or query signals/recommendations.
- Action: Run `wyckoff` CLI subcommands, parse output, present results to user.
- Fallback: If CLI not installed, trigger full setup guide from `rules/cli-setup-guide.md`.
- Routing: For operational intents (portfolio, signal, recommend, config), execute CLI directly without entering the analysis pipeline.

## Degrade Policy

- Never invent OHLCV rows, dates, events, or session status.
- Never output immediate intraday execution if current time is not tradable session.
- Keep output auditable even under partial failures: always include source/fallback table and missing-data notes.
- Prefer "safe downgrade + explicit uncertainty" over confident speculation.
