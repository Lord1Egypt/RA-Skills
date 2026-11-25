# trading-idea-analyst

Macro-first research for trading ideas. Instead of starting from the loudest
headline, the agent walks a fixed macro checklist, forms 2–4 theses with
counter-evidence, researches each (in parallel sub-agents where available) and
returns idea cards with a thesis, stop, targets, time stop, exit triggers and
event risk. Every idea gets an id and a machine-readable line, so you can
later see how the ideas actually did.

Part of [Agent Trading Journal](https://github.com/MaximSinyaev/agent-trading-journal): source code, issues and releases are there.

## Works on its own

- Needs only what your agent already has: web search or any market data tool.
  No CLI, no install, no API keys.
- Ideas are shown in chat. If you agree, they are also appended to a local
  markdown log (`trading-ideas.md` by default) so they can be scored later.
- Optional: with the **Trading Journal** skill installed (`trade` CLI), ideas
  and the trades you take from them go into its local SQLite journal instead,
  and the scorecard compares paper idea quality with your real P&L.

## What this skill does and does not do

- Reads the web through your agent's own search tools; nothing else is
  downloaded. No telemetry.
- Writes only the idea log file you agree to (or, if present, the Trading
  Journal through its `trade` CLI).
- Whatever your agent reads (news, your positions if you share them) goes to
  your agent's model provider, as with any tool output.

## Disclaimer

Research aid, not financial, investment or tax advice. Provided as is, without
warranty; use at your own risk.

License: MIT in the source repository; copies published on ClawHub are distributed under MIT-0, as ClawHub requires.
