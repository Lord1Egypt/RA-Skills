---
name: resend-cli
description: "Use this skill when the task is specifically about operating Resend from an AI agent, terminal session, or CI job via the official resend CLI: installing/authenticating the CLI, sending/listing/updating/cancelling emails, batch sends, domains and DNS, webhooks and local listeners, inbound receiving, contacts, topics, segments, broadcasts, templates, API keys, profiles, or debugging Resend CLI/API failures. Trigger on mentions of Resend CLI, `resend`, `resend doctor`, `resend emails send`, `resend domains`, `resend webhooks listen`, `resend emails receiving`, or agent-friendly terminal automation."
compatibility: "Designed for skills-compatible coding agents. Live operations require the official `resend` CLI plus a `RESEND_API_KEY` or stored profile. The bundled helper uses Python 3.10+ standard library only."
metadata:
  author: OpenAI
  version: "3.0.0"
  cli-version: "1.4.1"
  source: "https://github.com/resend/resend-cli"
  last-reviewed: "2026-03-14"
---

# Resend CLI

This skill is for agents that should operate **Resend through the official CLI first**, not by
dropping straight to raw REST.

The goal is not just “know the commands”. The goal is to make an agent:

1. choose the right Resend primitive,
2. choose the right CLI command,
3. run it in a deterministic non-interactive way,
4. detect the important CLI coverage gaps before it gets stuck, and
5. fall back to MCP/API only when the CLI genuinely does not cover the job.

## Start here

Load only the files that match the task:

- `references/agent-operating-model.md` — the default decision process for live Resend work
- `references/install-auth-and-profiles.md` — install methods, auth priority, profiles, config paths
- `references/subprocess-contract.md` — how agents should invoke `resend` safely and parse output
- `references/command-selection.md` — fast routing from user intent to the right command(s)
- `references/sending-scheduling-and-batch.md` — transactional sends, schedules, tags, attachments, batch limits
- `references/domains-dns-and-deliverability.md` — domain creation, verification, receiving, TLS, tracking, 403/domain mismatch
- `references/webhooks-and-listeners.md` — webhook creation, update, signature handling, temporary local listeners
- `references/inbound-receiving-and-threading.md` — inbound list/get/attachments/forward/listen flows
- `references/contacts-topics-segments-and-broadcasts.md` — subscription modelling, targeting, campaigns
- `references/templates-and-coverage-gaps.md` — template lifecycle and the important current CLI gaps
- `references/diagnostics-and-fallbacks.md` — debug order, CLI quirks, when to fall back to MCP/API
- `references/recipes.md` — short end-to-end playbooks
- `references/sources.md` — first-party source manifest and refresh notes

Machine-readable assets:

- `assets/command-catalog.json` — command index with detail levels (`source_inspected`, `readme_confirmed`, `tree_confirmed`)
- `assets/task-router.json` — route common tasks to command sequences
- `assets/error-map.json` — fast-fail diagnosis hints
- `assets/coverage-gaps.json` — current CLI limitations and ambiguities that matter to agents
- `assets/subprocess-contract.json` — deterministic invocation defaults
- `assets/scaffold-index.json` — reusable command/file scaffolds
- `assets/source-manifest.json` — authoritative URLs used to build this skill

Bundled helper:

- `scripts/resend_cli.py` — agent wrapper for probing, routing, scaffolding, batch linting, diagnosis, and safe subprocess execution

## Core operating rules

### 1) Prefer the official CLI for live Resend work

Default order of preference:

1. **Official Resend CLI** for live terminal/CI/agent operations
2. **Official Resend MCP server** if the environment already exposes it and the CLI is unavailable
3. **Official SDK** when editing app code inside an existing integration
4. **Raw REST** only for stack-neutral examples, protocol debugging, or feature gaps

Do not choose raw REST just because it is familiar.

### 2) For agents, stay non-interactive by default

For bounded commands:

- pass all required flags explicitly
- use global `--json -q`
- prefer `RESEND_API_KEY` or a stored profile over typing secrets interactively
- set `RESEND_NO_UPDATE_NOTIFIER=1` for deterministic output
- capture **both stdout and stderr** defensively

### 3) Run `doctor` early when the environment is unknown

When you do not know whether the CLI is installed, authenticated, or pointed at the right account:

```bash
resend --json -q doctor
```

This is usually the fastest first read on:

- CLI availability/version
- whether an API key is being resolved
- whether verified domains exist
- whether the machine looks like an AI-agent environment

### 4) Choose the primitive before the command

- One logical transactional email → `emails send`
- Up to 100 distinct transactional emails in one request → `emails batch`
- Scheduled transactional email mutation → `emails update` / `emails cancel`
- Campaign to a segment → `broadcasts create` / `broadcasts send`
- Reusable hosted content → `templates *`
- Sender or receiving setup → `domains *`
- Inbound processing → `emails receiving *` + `webhooks *`
- Scoped credentials → `api-keys *`
- Recipient data and preferences → `contacts`, `contact-properties`, `topics`, `segments`
- Local dev event loop → `webhooks listen` or `emails receiving listen`

### 5) Know the current CLI gaps

This version of the skill treats these as especially important:

- **Template send gap:** the CLI manages templates, but the current `emails send` command surface does not expose a direct `--template-id`/template-vars flow.
- **Domain capability update gap:** `domains update` exposes TLS/open/click tracking, but not an explicit sending/receiving capability toggle, while inbound help text references such a toggle.
- **Stream commands are special:** `webhooks listen` and `emails receiving listen` are long-running and should be treated as NDJSON/event streams in agent mode.
- **JSON error channel discrepancy:** the README promises machine JSON on stdout only, but the current source writes JSON errors with `console.error`, so wrappers must parse stderr too.

### 6) Keep IDs and file paths

Most multi-step flows become much easier if the agent persists:

- domain IDs
- email IDs
- webhook IDs
- topic IDs
- segment IDs
- template IDs/aliases
- API key IDs
- the file paths it generated for HTML or batch JSON

## The mutation ladder

For state-changing live operations:

1. classify the task
2. confirm the command sequence
3. make any needed file assets (`.html`, batch JSON)
4. run with `--json -q`
5. verify with `get`, `list`, or a follow-up check
6. persist returned IDs and next-step context
7. only then continue to the next mutation

## Bundled helper script

`scripts/resend_cli.py` is intentionally agent-oriented.

Commands:

- `probe` — find the CLI, report install hints, and show environment basics
- `catalog` — list known commands from the bundled catalogue
- `info` — inspect one command and its notes/gaps
- `recommend` — route a free-text task to the best CLI sequence
- `scaffold` — print or materialise sample commands/files
- `lint-batch` — statically validate an `emails batch` JSON file
- `doctor` — explain likely causes of common CLI/API failures
- `run` — execute the official CLI with deterministic defaults and tolerant JSON parsing

Examples:

```bash
python3 scripts/resend_cli.py probe
python3 scripts/resend_cli.py catalog --resource emails
python3 scripts/resend_cli.py info "emails send"
python3 scripts/resend_cli.py recommend "send 70 different shipment notifications"
python3 scripts/resend_cli.py scaffold batch-send --write-dir ./tmp
python3 scripts/resend_cli.py lint-batch ./tmp/batch-emails.json
python3 scripts/resend_cli.py doctor --command "emails send" --status 403 --message "1010 forbidden"
python3 scripts/resend_cli.py run -- emails list --limit 5
```

## Response shape this skill should produce

A strong answer usually includes:

1. the exact Resend primitive,
2. the exact CLI command or command sequence,
3. any file scaffolding the user needs,
4. the operational caveats that matter here,
5. the verification step,
6. the fallback path if the CLI does not currently cover the flow.

## Example prompts this skill should handle

- “Use the Resend CLI to send a scheduled password reset email”
- “Should I use `emails send`, `emails batch`, or `broadcasts create`?”
- “Create a sending + receiving domain in `eu-west-1`”
- “Set up local webhook listening with ngrok”
- “Why is my batch file failing?”
- “How do I manage multiple Resend accounts from one agent?”
- “Can the CLI send a hosted template directly?”
- “How should my agent parse `resend` output safely?”
