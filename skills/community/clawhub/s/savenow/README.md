# savenow

[![CI](https://github.com/Chelebii/savenow/actions/workflows/test.yml/badge.svg)](https://github.com/Chelebii/savenow/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Node.js Version](https://img.shields.io/badge/node-%E2%89%A518-brightgreen.svg)](https://nodejs.org)

> Save durable conversation notes from an OpenClaw + Telegram session into a daily memory file, with a semantic-dedupe preview and one-tap Apply / Cancel.

`/savenow` reads the current Telegram-topic conversation, picks out the few things worth keeping (resolved fixes, conventions, decisions, system mappings), and appends them to `memory/YYYY-MM-DD.md`. Before writing, it shows you a markdown diff of exactly what would change and lets you confirm with an inline button.

## Why

Chat is cheap, memory is expensive. Most of what you say in a session is conversational glue — but every now and then a useful fix or rule gets buried in the scrollback. `savenow` is a one-command escape hatch: tap `/savenow`, glance at the diff, tap **Apply**.

## Status

- **0.1.1** — ClawHub publish bundles now exclude the test harness; runtime behavior is unchanged. See [CHANGELOG.md](./CHANGELOG.md).
- **0.1.0** — first public release: semantic dedupe, preview/apply flow, inline Telegram buttons. See [CHANGELOG.md](./CHANGELOG.md).
- **Scope:** OpenClaw + Telegram **only**. The skill depends on `sessions_list` / `sessions_history`, the `MessageThreadId` runtime context, and Telegram inline keyboards. Vanilla Claude Code, CLI, and web surfaces are not supported by design.

## Demo

```text
/savenow
```

```markdown
### /savenow preview — memory/2026-05-15.md

**3 candidates** → 2 add, 0 merge, 1 skip. No write performed.

---

**1. ADD — Gateway token mismatch fix**
- Resolved `unauthorized: gateway token mismatch` by updating `gateway.cmd` and the related env variables.
- Next time a similar error appears, check token and env alignment first.
_compared against:_ (no close match above 0.4)

**2. MERGE — Telegram inline button rules → existing "Telegram UI conventions" (14:02)**
_reason: Two new rules belong to the same existing topic._
new bullets:
- Inline keyboards use a single-row, 3-button layout.

**3. SKIP — Sprint planning notes**
_reason: Temporary plan, no lasting value._
_(closest existing: "Sprint cadence rules" — title sim 0.62)_

---

Buttons expire in 30 min. Or `/savenow auto` next time to skip preview.
```

Telegram below this message:

```
[ ✅ Apply ]  [ ❌ Cancel ]
```

Tap **Apply** → bullets land in `memory/2026-05-15.md`. Tap **Cancel** → nothing happens.

## Requirements

- **OpenClaw** agent runtime (provides `sessions_list`, `sessions_history`, `CommandTargetSessionKey`, `MessageThreadId`)
- **Telegram bot** as the chat surface (for inline button rendering)
- **Node.js ≥ 18**

## Install

### 1. Check prerequisites

- An OpenClaw agent runtime up and running. If you don't have it yet, follow the OpenClaw setup at <https://docs.openclaw.ai>.
- A Telegram bot connected to that agent. `/savenow` is a Telegram-surface command and won't render its Apply / Cancel buttons elsewhere.
- Node.js 18 or newer. Verify with `node --version`.
- `git` on the machine that hosts the OpenClaw runtime.

### 2. Clone the repo into your OpenClaw skills folder

OpenClaw discovers skills inside `<workspace>/skills/<skill-name>/`. For the default user workspace this is:

| OS              | Skills folder                                |
|-----------------|----------------------------------------------|
| Linux / macOS   | `~/.openclaw/skills/`                        |
| Windows         | `%USERPROFILE%\.openclaw\skills\`            |

Clone savenow into that folder:

```bash
# Linux / macOS
git clone https://github.com/Chelebii/savenow ~/.openclaw/skills/savenow

# Windows (PowerShell)
git clone https://github.com/Chelebii/savenow $env:USERPROFILE\.openclaw\skills\savenow
```

If you keep multiple OpenClaw workspaces, drop it under the one you actually use (`~/.openclaw/workspaces/<name>/skills/savenow/` in OpenClaw's per-workspace layout).

You can also download a release tarball from the [Releases page](https://github.com/Chelebii/savenow/releases) and extract it to the same path — both layouts work.

No dependencies to install. The scripts use only Node's standard library.

### 3. Verify the install

Run the test suite from the skill folder:

```bash
cd ~/.openclaw/skills/savenow
node tests/run.mjs
```

You should see `12 passed, 0 failed, 12 total`. Then do a one-off dry run of the merge script:

```bash
node scripts/merge-daily-memory.mjs \
  --entries-file examples/sample-entries.json \
  --memory-path /tmp/savenow-demo.md
```

Open `/tmp/savenow-demo.md` — you'll see a memory file with the sample entries already merged. Delete it when you're done; it's just a smoke test.

### 4. Register the skill with OpenClaw

OpenClaw auto-discovers any folder under `skills/` that has a `SKILL.md` with a `name:` field, so cloning is usually enough. To force a rescan:

- Restart your OpenClaw agent process, **or**
- Run `openclaw skills reload` (if your CLI exposes it), **or**
- Send `/help` in Telegram — `/savenow` should show up in the list once the agent has picked it up.

The skill announces itself via the frontmatter at the top of `SKILL.md`:

```yaml
---
name: savenow
description: ...
user-invocable: true
version: 0.1.0
metadata: { "openclaw": { "requires": { "bins": ["node"], "surface": "telegram" } } }
---
```

`user-invocable: true` is what makes `/savenow` callable from Telegram. The `requires.bins: ["node"]` line tells the runtime to refuse to load the skill if Node isn't on the PATH; `requires.surface: "telegram"` documents the supported chat surface.

### 5. Try it on a real conversation

1. Open a Telegram topic with your OpenClaw bot.
2. Have a real conversation — fix a bug, decide a rule, agree on a convention.
3. Type `/savenow`. The bot should reply with a markdown preview and two inline buttons:

   ```
   [ ✅ Apply ]  [ ❌ Cancel ]
   ```

4. Tap **Apply**. The bot replies with a one-line confirmation; the entries are now in `memory/YYYY-MM-DD.md` inside the active workspace.
5. If you don't want to apply, tap **Cancel** (or just ignore — the preview expires in 30 minutes).

If `/savenow` doesn't appear or the buttons don't render, see [Troubleshooting](#troubleshooting) below.

### Troubleshooting

| Symptom                                                                  | Likely cause                                                                                 | Fix                                                                                                              |
|--------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| `/savenow` isn't recognized                                              | Skill folder is in the wrong place, or `SKILL.md` is missing / has invalid frontmatter.       | Confirm the path matches the table above. `cat SKILL.md` should start with `---\nname: savenow`.                 |
| Bot says `node: command not found` or similar                            | Node isn't on the PATH for the OpenClaw process.                                              | Install Node 18+ and restart the agent so it sees the new PATH.                                                  |
| Preview shows up but no inline buttons                                   | You're on a non-Telegram surface (Claude Code, CLI, web).                                     | This skill is Telegram-only by design. Use `/savenow auto` to write without buttons, or switch to Telegram.      |
| `/savenow apply` says "Pending preview is from a different topic"        | You ran the preview in one Telegram topic and tried to apply in another.                      | Rerun `/savenow` in the topic where you want the entries to land, then `apply`.                                  |
| `/savenow apply` says "Preview expired"                                  | More than 30 minutes passed between preview and apply.                                        | Rerun `/savenow` to generate a fresh preview.                                                                    |
| Memory file lands on the wrong date                                      | The OpenClaw process timezone differs from yours, or the session spanned midnight.            | Force a date with `--date YYYY-MM-DD` on the merge script if you're running it manually.                         |
| Tests fail in CI but pass locally                                        | Line-ending or encoding skew.                                                                 | `git config core.autocrlf input` (Linux/macOS) or check your `.gitattributes` settings.                          |

If something else breaks, open an issue with the script output, your OS, and your Node version — see [CONTRIBUTING.md](./CONTRIBUTING.md).

## Usage

| Command                       | What it does                                                                  |
|-------------------------------|-------------------------------------------------------------------------------|
| `/savenow`                    | Preview only. Shows markdown diff + Apply / Cancel buttons. Writes nothing.   |
| `/savenow apply`              | Write the most recent pending preview (TTL 30 min, same topic).               |
| `/savenow cancel`             | Discard the pending preview without writing.                                  |
| `/savenow auto`               | Extract + write directly. Skips preview and buttons.                          |
| `/savenow auto <sessionKey>`  | Auto on an explicit session.                                                  |
| `/savenow list`               | List same-topic candidate sessions without writing.                           |
| `/savenow <sessionKey>`       | Preview against an explicit session.                                          |

## Memory file format

```text
# YYYY-MM-DD

## HH:MM - Short title
- bullet
- bullet
```

When new bullets merge into an existing section, the script appends them in-place and adds a single trailing marker:

```text
## 14:02 - Telegram UI conventions
- Inline keyboards use a single-row, 3-button layout.
- Cancel button always sits on the rightmost slot.
- (merged 16:48)
```

A subsequent merge into the same section replaces the marker (no stacking).

## How dedupe works

1. **Agent-level semantic comparison.** Before writing the entries JSON, the agent reads today's memory and tags each candidate with `action: "add" | "skip" | "merge"`. Merges name an existing section via `merge_target_title`.
2. **Merge script applies the actions.** For `merge`, bullets are appended in-place to the matched section, deduping exact bullet matches. For `skip`, nothing is written.
3. **Lexical Jaccard safety net.** For `add` entries, the script still runs the original Jaccard check (0.88 title similarity + bullet overlap). If it fires, the entry is demoted to `skip` and recorded as `fallbackSkipped` in the result JSON.

This keeps the smart, paraphrase-aware decisions in the agent and the deterministic, testable writing in the script.

## Configuration

CLI flags on the scripts:

| Script                    | Flag                       | Default                       | Notes                                          |
|---------------------------|----------------------------|-------------------------------|------------------------------------------------|
| `merge-daily-memory.mjs`  | `--entries-file`           | (required)                    | Path to entries JSON                           |
|                           | `--memory-path`            | `memory/YYYY-MM-DD.md`        | Override the target file                       |
|                           | `--date`                   | local today                   | Override the date stamp for the default path   |
|                           | `--allow-merge`            | `true`                        | Set to `false` to force merges → adds          |
| `preview-diff.mjs`        | `--entries-file`           | (required)                    | Same as above                                  |
|                           | `--memory-path`            | `memory/YYYY-MM-DD.md`        | File to compare against                        |
|                           | `--pending-file`           | (none)                        | If set, writes the pending-state JSON          |
|                           | `--session-key`            | `""`                          | Recorded into pending state                    |
|                           | `--message-thread-id`      | `""`                          | Recorded into pending state                    |
|                           | `--ttl-minutes`            | `30`                          | Preview validity                               |

## Pending state

`/savenow` writes `temp/savenow-pending.json` containing the entries snapshot, expiry, and session/topic identity. `/savenow apply` reads it, validates TTL and session match, runs the merge, and deletes the pending file. A second preview in a different topic clobbers the pending — apply in the original topic will then fail closed and ask the user to rerun preview.

## Limitations

- **OpenClaw + Telegram only.** Other surfaces (vanilla Claude Code, CLI, web) are not supported.
- **Local-time date stamps.** Memory files are named after the local date — sessions that span midnight may write to "yesterday".
- **Pending state is workspace-singleton.** Only one pending preview at a time. A new preview in another topic clobbers the old one.

## Repository layout

```text
savenow/
├── SKILL.md                    skill spec, workflow, command forms
├── README.md                   this file
├── LICENSE                     MIT
├── CHANGELOG.md
├── package.json
├── scripts/
│   ├── merge-daily-memory.mjs  apply-side: writes to memory file
│   ├── preview-diff.mjs        preview-side: renders diff + pending state
│   └── lib/memory.mjs          shared helpers
├── examples/                   sample inputs and outputs
└── tests/run.mjs               zero-dep test runner
```

## Tests

```bash
node tests/run.mjs
```

No test framework. Each test sets up a temporary working directory with inline input data, spawns one of the scripts as a subprocess, and asserts on the JSON it writes to stdout and the memory file on disk. You should see `12 passed, 0 failed, 12 total`.

## Contributing

Issues and PRs welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide. In short:

- Keep scripts dependency-free.
- Preserve backward compatibility for the `{ title, bullets }` entries shape.
- Add a test in `tests/run.mjs` for any new behavior.
- Be kind — see [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

Found a security issue? Please don't open a public issue — see [SECURITY.md](./SECURITY.md).

## License

MIT — see [LICENSE](./LICENSE).
