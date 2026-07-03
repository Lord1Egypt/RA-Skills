---
name: totalreclaw
description: "End-to-end encrypted, decentralized memory for OpenClaw. A native kind:memory provider — recall is automatic via memory_search/memory_get, and facts are captured in the background. Trigger on 'install TotalReclaw', 'set up TotalReclaw', 'restore my recovery phrase', any recall request ('what do you remember about me', 'what's my X'), AND any explicit remember request ('remember X', 'save X')."
version: 3.3.12-rc.19
author: TotalReclaw Team
license: MIT
homepage: https://totalreclaw.xyz
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    emoji: "🧠"
    os: ["macos", "linux", "windows"]
    keywords:
      - memory
      - e2ee
      - e2e-encryption
      - encryption
      - privacy
      - agent-memory
      - persistent-context
---

# TotalReclaw — OpenClaw native memory provider

End-to-end encrypted memory stored across a decentralized network (not on a single company server). TotalReclaw is OpenClaw's **native `kind:"memory"` provider**: recall runs through the conventional `memory_search` / `memory_get` tools (the same surface `active-memory` uses), and **facts are captured automatically in the background** — you do not call a tool to remember each fact. This skill tells you the install + account-setup flow and when to drive recall explicitly.

## How memory works here (read first)

- **Recall is native.** `memory_search` and `memory_get` are the memory tools. OpenClaw's `active-memory` sub-agent routes recall through them and the plugin injects guidance telling you when to search. When the user asks about themselves ("what's my X?", "do I X?", "what do you remember?"), call `memory_search`. If 0 results, say so plainly — don't guess from session history.
- **Capture is automatic.** The plugin extracts facts from the conversation in the background (trajectory poller). You do **not** call a tool on every preference/fact the user states — that happens for you. Never write user facts to `MEMORY.md`, `USER.md`, or any local file; those are agent-persona config, user memories live encrypted on-chain.
- **Explicit remember only on request.** If the user explicitly says "remember X" / "save X" / "note X" / "don't forget X", use the CLI: `tr remember --json "X"`. One call per distinct fact.

Do not describe storage as `"local"`, `"local-only"`, `"stored locally"`, `"on disk"`, or `"without an account"` — memories are decentralized on-chain (not on any single company server) and an account is required to derive the encryption key.

## Phrase safety (HARD)

The 12-word recovery phrase MUST NEVER enter chat or the agent's LLM context. The plugin's browser-based pair flow handles phrase generation and import. Never echo it, never ask the user to paste it, never pass it to any tool. If the user pastes one anyway, tell them it's compromised and re-pair for a fresh wallet.

## Install

```
openclaw plugins install @totalreclaw/totalreclaw
openclaw skills install totalreclaw
```

Published on npm + ClawHub (`p-diogo`, GitHub-verified). For a release candidate, pin with `@rc`; stable resolves from `latest`. The plugin self-applies any gateway config it needs on load and auto-reloads (see Restart below) — no manual gateway restart.

## Setup (pair — user-initiated QR)

Pairing is a deliberate, user-initiated QR flow (the plugin does **not** auto-pair on load). When credentials don't exist:

1. Run `tr pair --json` → returns `{"url":"https://…/pair/p/<id>#pk=…","pin":"123456","expires_at_ms":…}`.
2. Surface the **url** and **pin** to the user verbatim (read from the JSON; never invent values): "Open `<url>` in your browser, enter PIN `<pin>`, and generate or paste your 12-word recovery phrase. Reply done once it's sealed."
3. The user completes in the browser (phrase is generated/imported browser-side, encrypted, posted to the relay — never touches this chat). On completion `~/.totalreclaw/credentials.json` is written.
4. Confirm: `✓ TotalReclaw set up.` (If credentials already exist when first asked: `✓ TotalReclaw is already set up.`)

Pair is UNCONDITIONAL when no credentials — the user installing/requesting setup IS the consent; do not add a second consent gate. `tr --help` lists every subcommand.

```bash
TR_CLI="$(ls -d ~/.openclaw/npm/node_modules/@totalreclaw/totalreclaw/dist/tr-cli.js ~/.openclaw/extensions/totalreclaw/dist/tr-cli.js 2>/dev/null | head -1)"
node "$TR_CLI" pair --json        # start/re-pair
node "$TR_CLI" status --json      # {"version":"…","paired":true,…}
```

## Restart (agent-driven, never user-manual)

The plugin self-reloads: after install it writes the gateway config it needs and signals `SIGUSR1` to its own PID so the gateway picks it up without a manual restart. **If `memory_search`/`memory_get` are not bound** (tools didn't take effect on first load), issue the literal slash command `/totalreclaw-restart` **autonomously** — announce it in one line, never ask the user to authorize it, never stall, never `kill` / `docker restart` / prompt the user to restart. This mirrors the autonomous-restart pattern other runtimes use; the user should never perform a manual restart.

## Tools + CLI surface

**Recall (native memory contract — agent-facing):** `memory_search`, `memory_get`.

**Explicit capture + curation (CLI — `tr`, i.e. `node "$TR_CLI" …`):**
`tr remember` (explicit write) · `tr pin` / `tr unpin` · `tr retype` · `tr set_scope` · `tr status` · `tr export` · `tr pair`. Import + plan upgrade run via the gateway subcommand: `openclaw totalreclaw import from <source> --file <path> [--json]`, `openclaw totalreclaw upgrade [--json]`, `openclaw totalreclaw import status|abort`.

The legacy `totalreclaw_*` agent tools and the `tr recall` CLI are retired — recall is `memory_search`, explicit capture is `tr remember`. If a stale guide references them, follow this SKILL instead.

Full guide: <https://github.com/p-diogo/totalreclaw/blob/main/docs/guides/openclaw-setup.md>
