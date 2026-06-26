---
name: windy-access
description: "Wire any agent into the Windy ecosystem in one command. Use when the user wants their agent to have an email address (Windy Mail), a chat identity (Windy Chat), an Eternitas passport (verifiable identity), and free LLM access (Windy Mind, OpenAI-compatible). Auto-detects OpenClaw, Hermes Agent, Claude Code, and falls back to a generic ~/.windy/bundle.json for any other runtime. Triggers on phrases like 'connect my agent to Windy', 'give my agent an email', 'set up windy-connect', 'agent credentials bundle'. Pairing happens in a browser via Sign-in-with-Google."
user-invocable: true
version: "0.2.0"
author: sneakyfree
license: MIT
platforms: [macos, linux]
compatibility: Auto-detects the host agent runtime — OpenClaw (XDG config), Hermes Agent (~/.hermes), Claude Code (~/.claude). Falls back to ~/.windy/bundle.json for any other framework (LangChain, AutoGen, in-house). Requires Python 3.11+ on macOS or Linux.
metadata:
  author: sneakyfree
  version: "0.2.0"
  openclaw:
    emoji: "🌪️"
    homepage: https://github.com/sneakyfree/windy-connect
    requires:
      bins:
        - python3
    install: []
  hermes:
    tags: [Identity, Mail, Chat, LLM, Onboarding]
    related_skills: []
    requires_tools: []
allowed-tools: Read Bash(windy:*) Bash(pipx:*) Bash(curl:*) Bash(python3:*) AskUserQuestion
---

**Persona:** You are an agent-onboarding assistant who completes a one-shot pairing between the host agent and the Windy ecosystem. You preserve idempotency and reversibility above all else — every write goes into the runtime's conventional location, with marker-bounded blocks where the file is shared, so every change is undoable via `windy disconnect`.

# What this skill does

`windy connect` mints an **Eternitas Agent Credentials Bundle (v1)** for the current agent, **auto-detects which runtime is installed**, and writes the right credentials in the right place:

## Per-runtime write map

### OpenClaw (`$XDG_CONFIG_HOME/openclaw/`)

| Credential | File / location | Notes |
|---|---|---|
| Windy Chat (Matrix) | `secrets/windy-chat.env` (owned) | `MATRIX_HOMESERVER`, `MATRIX_USER_ID`, `MATRIX_ACCESS_TOKEN`, `MATRIX_DEVICE_ID` |
| Windy Mind (OpenAI-compat) | `secrets/windy-mind.env` (owned) + `extensions/windy-mind/openclaw.plugin.json` (owned) | Wired as an OpenClaw provider |
| Windy Mail (Himalaya) | `~/.config/himalaya/config.toml` (marker block `[accounts.windy]`) | Shared config — other Himalaya accounts preserved |

### Hermes Agent (`~/.hermes/` or `$HERMES_HOME`)

| Credential | File / location | Notes |
|---|---|---|
| Windy Mind | marker block in `~/.hermes/.env` | `WINDY_MIND_BASE_URL`, `WINDY_MIND_API_KEY`, `WINDY_MIND_DEFAULT_MODEL`. Coexists with the user's own `OPENROUTER_API_KEY`/etc. |
| Windy Mail | marker block in `~/.hermes/.env` | Native Hermes vars: `EMAIL_ADDRESS`, `EMAIL_PASSWORD`, `IMAP_HOST`, `IMAP_PORT`, `IMAP_USERNAME`, `SMTP_*`. Hermes's built-in email tool works immediately. |
| Windy Chat (Matrix) | marker block in `~/.hermes/.env` as `WINDY_CHAT_*` | **Hermes has no native Matrix tool.** Credentials are exposed for skills / MCP servers; the CLI reports this in `windy status`. |
| Eternitas passport | marker block in `~/.hermes/.env` as `WINDY_ETERNITAS_EPT` + `WINDY_ETERNITAS_PASSPORT` | Available for any skill that wants to assert verifiable identity. |

### Claude Code (`~/.claude/`)

| Credential | File | Notes |
|---|---|---|
| Windy Mind | `~/.claude/windy.env` (owned, source from shell rc) | `OPENAI_BASE_URL` + `OPENAI_API_KEY` — routes Claude Code through Windy Mind |
| Mail, Chat | — | Skipped: Claude Code has no native mail or chat surface today |

### Generic fallback (`~/.windy/`)

| Credential | File | Notes |
|---|---|---|
| Everything | `~/.windy/bundle.json` (owned) + `~/.windy/windy.env` (owned) | Canonical bundle. Any custom framework (LangChain, AutoGen, in-house code) can read from this location without a dedicated writer. |

When MULTIPLE runtimes are detected on the same machine, the CLI prompts which to wire — default is all of them. Disconnect reverses every write transactionally.

# When to use this skill

Trigger when the user asks for any of:

- "Give my agent an email address."
- "Connect my OpenClaw / Hermes / Claude Code to Windy."
- "Wire in a free LLM provider."
- "Pair my agent with an Eternitas passport."

Skip this skill if `windy status` already reports a live, non-expired bundle — pairing is idempotent but the user usually doesn't need a second one.

# How to use this skill

## 1. Verify the CLI is installed

```bash
windy version
```

If `windy` is not on PATH:

```bash
curl -fsSL https://get.windyconnect.com | sh
# or, manually:
pipx install windy-connect
```

Idempotent; chooses pipx > pip --user based on what's available. Python 3.11+ required.

## 2. Run the pair flow

```bash
windy connect
```

This:

1. Opens `https://api.windyconnect.com/pair` in the user's default browser with a one-time user code.
2. Polls `POST /v1/device/poll` (RFC 8628 device-code flow) until the user finishes Sign-in-with-Google in the browser.
3. Receives the bundle and writes credentials into the locations in the per-runtime table above. **Auto-detects the host runtime.**

The CLI prints a clear summary of every file it wrote and every config block it touched (marker-bounded, so reversal is exact).

## 3. Verify

```bash
windy status
```

Reports what's wired, per detected runtime, and when each credential expires. Bundles refresh automatically when within 7 days of expiry (or when `windy refresh` is invoked).

## 4. Unwind, if needed

```bash
windy disconnect --yes
```

Removes every file the CLI wrote and strips every marker-bounded block from every runtime. **Does not touch the user's other Himalaya accounts, Hermes env vars, OpenClaw extensions, or anything else outside our markers.**

# Tier choice (per ADR-052)

The pair page asks the user to pick one of two tiers:

- **Anonymous tier** — no Eternitas passport. Email + chat + Mind all work; identity is a per-install opaque token.
- **Credentialed tier** — Eternitas passport minted; agent can authenticate to other agents in the ecosystem (and, eventually, to humans who require verifiable identity).

When you (the assistant) run this skill on behalf of the user, ask which tier they want unless they've already specified. Default to anonymous if uncertain — they can `windy upgrade` later.

# Hermes-specific guidance

Hermes Agent stores everything under `~/.hermes/`. After `windy connect`:

- `~/.hermes/.env` now contains a marker-bounded windy-connect block with all Windy credentials. The block includes `EMAIL_*` / `IMAP_*` / `SMTP_*` vars, which Hermes's native email tool consumes immediately — try `send an email to <addr>` and it routes through Windy Mail's Stalwart server.
- **Windy Mind is exposed via `WINDY_MIND_BASE_URL` / `WINDY_MIND_API_KEY`** rather than clobbering `OPENAI_API_KEY`. To use Windy Mind as Hermes's default LLM, the user can `hermes config set model.default openai-compatible` and point the provider at `$WINDY_MIND_BASE_URL`. The reason we don't auto-override `OPENAI_*` is that Hermes users often have a real OpenAI key for non-Windy work — clobbering would surprise them.
- **Matrix is exposed but not native.** Hermes's built-in messaging is Slack/Telegram/WhatsApp/Email/Teams/Discord. Matrix support comes via a skill or MCP server that reads `WINDY_CHAT_*`. If the user asks for Matrix, point them at `windy-chat-mcp` (TBD) or the underlying `matrix-nio` Python library.

# OpenClaw-specific guidance

After `windy connect` on OpenClaw, Windy Mind appears as a provider in the OpenClaw extension catalog; agents can route to it via the standard provider-selection UX. Mail works through Himalaya (which OpenClaw ships); Chat works through the Matrix client OpenClaw bundles. Nothing else for the user to do.

# When things go wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `windy: command not found` after install | `~/.local/bin` not on PATH | Add `export PATH="$HOME/.local/bin:$PATH"` to shell rc; reopen shell |
| Pair page returns "device-code expired" | User took >15 min in the browser | Re-run `windy connect` to start a new session |
| `windy status` shows everything except Mail | Stalwart admin endpoint unreachable | Network issue — retry; if persistent, file a windy-connect issue |
| `windy status` reports "windy_chat skipped: Hermes has no native Matrix" | Expected on Hermes | Not a bug — the credentials are still written as `WINDY_CHAT_*` for skills/MCP to consume |
| Mind requests get 401 from `api.windymind.ai` | Mind admin-key endpoint not yet wired (pre-launch) | Tracked in `docs/upstream-gaps.md`; the sandbox key works for local testing |

# Files this skill touches

This skill ONLY runs `windy` CLI commands. It does NOT write files directly — every write goes through `windy connect`, which uses marker-bounded blocks and isolated env files so that reversal is precise. Do not bypass `windy connect` to install credentials manually.
