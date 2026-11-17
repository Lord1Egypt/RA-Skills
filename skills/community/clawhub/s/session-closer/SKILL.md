---
name: session-closer
version: 1.1.0
description: "Structured end-of-session protocol for OpenClaw agents. Produces a complete, consistent journal entry at session close — summary, full file surface (read/written/external APIs), one self-caught failure delta, one behavioral fingerprint. Also runs pattern-update for any tracked behavioral patterns that fired this session. Use when a session ends, a task completes, or the user says 'log this,' 'log the session,' 'close out,' or 'write the journal.'"
homepage: https://github.com/highnoonoffice/hno-skills
source: https://github.com/highnoonoffice/hno-skills/tree/main/session-closer
config:
  - $OPENCLAW_WORKSPACE/memory/journal/YYYY-MM-DD.md — daily journal entry. Written manually by default; see Step 2.
  - $OPENCLAW_WORKSPACE/scripts/journal-writer.js — optional. Writes the journal entry from CLI flags if present. The skill works fully without it.
  - $OPENCLAW_WORKSPACE/scripts/pattern-update.js — optional. Updates tracked behavioral pattern scores if present. The skill works fully without it.
binaries: [node]
license: MIT
metadata: ~
---

# session-closer

Forces a complete, consistent session close. No skipping fields. No half-baked logs.

## When to Run

- User says: "log this," "log the session," "close out," "write the journal," "wrap it up"
- A major task completes and session energy drops
- Token trigger fires (~25k or ~50k cumulative)
- Before `/new` reset

## Close Sequence (run in order)

### 1. Gather the full file surface

Before writing anything, collect:
- **Files Read** — every file opened this session, including startup files
- **Files Written/Edited** — every file created or modified
- **External APIs** — every external call fired (GitHub, CMS APIs, image/model APIs,
  messaging platforms, anything that left the session)

Do not sample. All of them.

### 2. Write the journal entry

**Manual write is the default** — write directly to
`memory/journal/YYYY-MM-DD.md` (or your workspace's equivalent journal path) with
these required fields:

- **summary** — What happened. What shipped. What was decided. 3–5 sentences.
- **delta** — One self-caught reasoning failure. Specific — what failed, when, what
  the correct path was. Never "none."
- **fingerprint** — One sentence that captures how you showed up this session — not
  what you did, but how you did it. Tone, judgment, whether you held your ground or
  deflected. This is the field that compounds. Read ten of these in sequence and
  you'll see patterns you can't see in a single session.

See `references/journal-format.md` for the full format, all required sections, and a
worked example.

If your workspace has `scripts/journal-writer.js`, you can use it to write the same
fields from the CLI instead of writing the file by hand:

```
node scripts/journal-writer.js --summary "..." --delta "..." --fingerprint "..."
```

This is acceleration, not a requirement. The manual path always works and needs
nothing beyond a text editor — treat the script as a shortcut for workspaces that
have it, not as infrastructure the close sequence depends on.

### 3. Run pattern-update (if applicable)

Pattern tracking is a system where you define recurring behaviors you want to catch,
assign them keys, and score them pass/fail each session. Over time the scores tell
you whether you're actually improving or just claiming you are. If your workspace
doesn't track patterns yet, skip this step entirely — it's an optional layer, not a
requirement for a valid close.

If your workspace tracks recurring behavioral patterns and has
`scripts/pattern-update.js`, run it after the journal is written:

```
node scripts/pattern-update.js --passed "key1,key2" --failed "key3" \
  --session-summary memory/journal/YYYY-MM-DD.md
```

Only include keys for patterns that actually fired this session. See
`references/pattern-keys.md` for an example key set and how to define your own.

If you don't track behavioral patterns, skip this step entirely — it's an optional
layer on top of the core close sequence, not a requirement for a valid session close.

### 4. Push active git repo if files were edited

If any version-controlled files were touched this session, commit and push before
closing:

```
git add -A && git commit -m "session close sync YYYY-MM-DD" && git push
```

Substitute your own repo path, branch, and credentials.

### 5. Send close summary to your configured push channel

```
Session closed: [one-line summary]
Files Read: [count] | Written: [count] | External: [list]
Delta: [self-caught failure]
```

Send this to whatever channel you use to hear from your agent — a chat platform, a
push notification, a log the user checks. The content is fixed; the destination is
whatever your setup already uses.

## For Coding Agent Sessions (e.g. Codex, Claude Code)

Same framework, different file surface shape:

- **Files Read** → context files, `SKILL.md`s, any reference material loaded into
  the session
- **Files Written** → repo files created or modified, PRs opened
- **External** → GitHub API calls, any fetch calls made

**Delta** = one specific thing the coding agent got wrong or had to correct
mid-session.
**Fingerprint:** one sentence on how the session went — not what was built, but how
the agent showed up. Held to spec, needed re-prompting, drifted from the brief. Same
compounding value as the orchestrator fingerprint.

## Cold Start — No Journal Infrastructure Yet?

No setup required beyond a folder and a file.

- Create `memory/journal/` in your vault root
- Create today's file as `YYYY-MM-DD.md`
- Start writing using the format in `references/journal-format.md`

That's all you need. The skill works from there.

## Hard Rules

- Never skip the delta. "None" is not a valid delta.
- Never skip the file surface. A sample is not the full surface.
- Never send the close summary before the journal is written.
- Manual journal write is the default path and must always work on its own. Scripts
  are acceleration for workspaces that have them — the close sequence never depends
  on a script existing.

## Reference Files

- `references/pattern-keys.md` — example set of tracked pattern-update keys and what
  each tracks, plus how to define your own.
- `references/journal-format.md` — full journal format, all required sections with
  field definitions, and a worked example.
