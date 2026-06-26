# Xerg

Find wasted AI spend in OpenClaw, Hermes, and Cursor.

Xerg is a local-first CLI for auditing AI spend in dollars, not raw token counts. It reads OpenClaw and Hermes logs plus Cursor usage exports, separates confirmed waste from savings opportunities, and lets you measure fixes with `--compare`.

Everything runs locally by default. The CLI is open source (MIT), published on npm as `@xerg/cli`, and the full source is at [github.com/xergai/xerg](https://github.com/xergai/xerg). No account is required for local audits. Hosted sync and hosted MCP are optional paid workspace features.

The `npx @xerg/cli` path fetches and executes the published npm package before running Xerg. If you want to review the code first and avoid that fetch on each use, install the CLI globally with `npm install -g @xerg/cli` or run a local build.

## Install

```bash
npm install -g @xerg/cli
```

Or run without installing:

```bash
npx @xerg/cli init
```

## What It Finds

- **Retry waste** - failed calls that burned spend before a later success
- **Loop waste** - runs that exceeded efficient iteration bounds
- **Context bloat** - input token volume far above the workflow baseline
- **Downgrade candidates** - expensive models on operationally simple tasks
- **Idle waste** - recurring heartbeat or monitoring loops worth reviewing

Local JSON findings can include `signalSource`, `ruleId`, and evidence references so agents can distinguish observed signals from inferred or legacy unknown provenance. Compare output leads with normalized waste rate and per-unit rows before workload-dependent spend deltas.

## Quick Start

```bash
xerg init
xerg audit --compare
```

Use direct commands when you want explicit control:

```bash
xerg doctor --runtime openclaw
xerg audit --runtime hermes
xerg audit --json
```

## Sources

- Local machine: OpenClaw and Hermes
- Local Cursor usage export: `xerg audit --cursor-usage-csv ./cursor-usage.csv`
- Remote OpenClaw sources via SSH or configured remote transports

If local defaults are empty, inspect the target directly first with `xerg doctor --remote user@host`.

## Optional Hosted Follow-Up

```bash
xerg connect
xerg mcp-setup
```

- `connect` offers browser auth and pushing the latest audit
- `mcp-setup` prints or writes hosted MCP config for supported clients
- local audits and compare remain available if you skip hosted setup

## Security And Data Flow

- Local audits read OpenClaw, Hermes, or Cursor usage files and may write local JSON snapshots for `--compare`.
- Remote OpenClaw audits pull selected files to local temporary storage before analysis.
- Xerg Cloud sync only happens when you run `connect`, `audit --push`, `push`, or `mcp-setup`.
- Push payloads include audit totals, rollups, findings, recommendations, comparison deltas, and source metadata. They exclude raw prompt and response content, local source file paths, local snapshot store paths, and internal finding details.
- Local provenance fields are intentionally not part of the pushed v2 wire payload yet.

## CI And Automation

```bash
xerg audit --push --fail-above-waste-rate 0.25
xerg audit --fail-above-waste-usd 100
xerg audit --json
```

## Links

- Docs: [xerg.ai/docs](https://xerg.ai/docs)
- GitHub: [xergai/xerg](https://github.com/xergai/xerg)
- npm: [@xerg/cli](https://www.npmjs.com/package/@xerg/cli)
- Pilot: [xerg.ai/pilot](https://xerg.ai/pilot)
- Support: `query@xerg.ai`
