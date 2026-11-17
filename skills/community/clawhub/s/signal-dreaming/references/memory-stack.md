# Where signal-dreaming sits in OpenClaw's memory stack

Orientation material, moved out of `SKILL.md` in 5.0.3 so the always-loaded file
stays within its character budget. Nothing here is a step: the operational
consequence — never read or write `memory/dreaming/**` or `memory/.dreams/**` —
is stated in `SKILL.md` and enforced in Phase 1 of `dream-protocol.md`.

Verified against OpenClaw **2026.9.2**. This skill operates entirely on the documented Markdown layer — `MEMORY.md` plus `memory/*.md` — which remains the durable memory model.

**Built-in memory-core Dreaming** is a separate system, **enabled by default**; set `plugins.entries.memory-core.config.dreaming.enabled: false` to turn it off. Earlier releases of this skill called it opt-in, which was true when they were written and is not true now:

| | memory-core built-in Dreaming | signal-dreaming (this skill) |
|---|---|---|
| Trigger | Managed cron when enabled | Cron agentTurn |
| Source | Short-term recall store under `memory/.dreams/` | Daily logs on disk |
| Output | `DREAMS.md` / `memory/dreaming/{phase}/` | `memory/dream-log.md` + L2 files |

The two are independent; run this skill with built-in Dreaming on or off. This protocol never reads or writes `memory/dreaming/**` or `memory/.dreams/**`, and skips `## Light Sleep` / `## REM Sleep` blocks if it finds them inside a daily log (older `inline` mode).

Adjacent components this protocol deliberately does not touch:

- **`memory-wiki`** — per the OpenClaw docs it "does not replace the active memory plugin"; its vault is its own layer, neither read nor written here.
- **Alternate backends** (QMD, Honcho, LanceDB) — they change how `memory_search` retrieves, not where durable notes live. This protocol reads and writes files, so it is backend-agnostic.
- **Database-first state** — the SQLite migration covers runtime state (sessions, transcripts, task ledgers). Workspace Markdown memory is out of scope.
- **Automatic memory flush** — the pre-compaction pass writes daily notes; this protocol consumes them. No conflict.

**A version number in this file dates.** It records what was true of OpenClaw when
someone last checked, not a compatibility guarantee. Re-read the current docs
before relying on any line here; the protocol itself derives its limits from the
runtime rather than from this page, so a stale note here changes orientation, not
behaviour.
