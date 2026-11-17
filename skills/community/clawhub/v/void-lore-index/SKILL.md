---
name: void-lore-index
description: >
  Lore & universe wiki keeper for world-building / roleplay servers.
  Indexes a local markdown lore vault (characters, places, factions,
  rules, artifacts) and answers canon questions with sourced excerpts —
  "What are the rules of travel in Sector 4?" returns the actual canon
  text, never a guess. Entries can carry WITH expiry rules (retire at
  arc N, or N days/weeks after their stamp) so superseded canon stops
  influencing answers; retcon marks keep deliberate exceptions alive.
user-invocable: true
metadata:
  {"openclaw": {"emoji": "⛏️", "requires": {"bins": ["python3"], "files": [], "config": []}}}
---

# Void Lore Index — canon wiki keeper

Answers continuity questions from a local markdown **lore vault**.
Every answer is an excerpt from a real vault file plus its id — the
skill never invents canon. "Sector 4 travel rules" returns the section
that actually says so, with the file it came from.

Vault: any directory of `.md` files (subdirs OK). Point the skill at it:

```bash
L=~/.openclaw/plugin-skills/void-lore-index/lore_index.py
python3 $L config --vault ~/lore/my-universe
python3 $L index
```

## Entry anatomy (what the indexer reads)

```markdown
---
title: Sector 4 Travel
tags: travel, sector-4, FTL
with: arc-4            # retires from canon when the arc passes 4
stamp: 2026-03-01      # anchor date for duration-based WITH rules
influence: retained    # optional: stays influential even past expiry
---

# Sector 4 Travel

Travel through Sector 4 requires a Class-3 hull ...
```

WITH rules (`with:` frontmatter, or inline `[[WITH: arc-4]]`):

| Rule | Meaning |
|---|---|
| `arc-4` | expires when the vault arc (config `--arc` or `_arc.md`) exceeds 4 |
| `90d` / `2w` / `36h` | expires that long after the entry's `stamp:` (or file mtime) |
| `on 2027-01-01` | fixed calendar expiry |
| `~90d` | **soft** variant — weak memory, excluded from answers unless `influence: retained` |

Unparsable rules are flagged `unknown` (never silently dropped).

## Command reference

Run via bash; add `--json` for structured output (preferred for parsing).

| Command | Purpose |
|---|---|
| `config --vault DIR` | set the vault (also `--arc N`, `--excerpt-chars`, `--top-k`, `--with-limbo-days`, `--token-budget`) |
| `index` | (re)build the index from the vault |
| `vacuum` | re-scan the vault, diff WITH state changes (new/removed/changed) |
| `ask <question>` | canon answer: top matches with heading-scoped excerpts under a char budget |
| `search <terms> [--expired]` | scored list of matching entries |
| `get <id>` | full text of one entry + its WITH state |
| `retcon <id>` [--clear] | keep an entry influential past its WITH expiry |
| `add --title T --body "..."` | write a new entry into the vault (only vault-writing command) |
| `status` | WITH rules expiring/expired — the attention list |
| `stats` | vault summary: counts, WITH states, retained, parse errors |

## Behaviour rules the agent must follow

1. **Never invent canon.** Answer only with excerpts `ask` returned and
   name the entry id they came from. Zero matches → say so and offer to
   add the entry; do not guess, even if the question sounds trivial.
2. **Check freshness before answering a continuity question.** Run
   `vacuum` first if the vault may have changed; `status` shows any WITH
   rules expiring/expired. An answer sourced to an expired entry is a
   continuity bug — prefer active entries, and say when the only source
   is expired/retained.
3. **Tokens are chars**: `token_budget` (default 4000 chars) caps how
   much `ask` returns; the meta line reports `used/budget`.
4. **Expiring canon**: `⚠ expiring` means the WITH rule lapses in the
   current arc or within `with_limbo_days` (default 7). Surface this to
   the user — it usually means someone needs to write the replacement.
5. **`add` is the only writer**, and only into the configured vault.
   `retcon` touches the index, never the user's files.

## Example session

```bash
python3 $L ask "what are the rules of travel in Sector 4"
python3 $L search "warp lane tolls" --limit 8
python3 $L status          # ⚠ which canon is expiring/expired
python3 $L add --title "Keth Relay Fauna" --tags "fauna,sector-2" \
  --body "Bioluminescent drifter swarms nest in the relay ring..." \
  --with-rule "~90d"
python3 $L retcon sector-2/relay-fauna.md   # it's still canon, keep it
```

## State & files

- Index: `~/.openclaw/void-lore-index/index.json` (atomic writes)
- Config: `~/.openclaw/void-lore-index/config.json`
- Vault files are read-only to the skill — re-index any time, edits stay yours.

## Limitations

- Matching is lexical (title/tag/body term overlap, weighted): great for
  "which entry talks about X", not paraphrase search. Name things the way
  the vault names them, or use `search` first to find ids.
- `ask` excerpts are per-section under the char budget; for a full
  entry use `get <id>`.
- Arc numbers are integers (1, 2, 3 …); arc-based WITH needs the vault
  arc kept current (`config --arc N` or `_arc.md` with `arc: N`).
