---
name: zettelclaw
description: "Work inside a Zettelclaw vault using the current typed frontmatter schema, inbox + Base workflows, and human-write/agent-read guardrails. Use when creating, updating, organizing, or searching notes in a Zettelclaw vault, including inbox processing, /ask callouts, and journal scaffolding."
---

# Zettelclaw

Follow the canonical Zettelclaw vault model: capture externally, write durable notes manually, and use the agent for navigation/synthesis.

This is an instruction-only skill. It does not install software by itself. `qmd` is optional when it is already available in the environment, and `rg` is the supported fallback for search.

## Vault structure

```
<vault>/
├── 00 Inbox/
├── 01 Notes/
├── 02 Journal/
├── 03 Templates/
├── 04 Attachments/
└── README.md
```

## Note types

Use YAML frontmatter on every note:

- Required on all notes:
  - `type`
  - `tags`
  - `created`
- Required on `doc` and content notes:
  - `status` (`queued | in-progress | done | archived`)
- Optional content metadata:
  - `author`
  - `source`

Use these primary types:

- `note`: durable atomic thinking note; no `status`
- `doc`: non-atomic working/reference note; uses `status`
- `journal`: daily log note; no `status`
- content types: `article`, `book`, `movie`, `tv`, `youtube`, `tweet`, `podcast`, `paper` (and extensible additional content types); uses `status`

## Templates

Always read the matching template in `03 Templates/` before creating a note:

- `note.md`
- `journal.md`
- `clipper-capture.json`

Use core templates/date syntax. Do not require Templater.

## Inbox workflow

- Web captures land in `00 Inbox/` via `clipper-capture.json`.
- Clipper sets `type` by URL (`tweet`, `youtube`, else `article`) and `status: queued`.
- Process inbox captures by keeping/moving, converting into a `type: note`, or deleting.
- Do not auto-write durable thinking notes from captured content unless explicitly asked.

## Bases workflow

- `00 Inbox/inbox.base` is the canonical queue view.
- Grouping is by `note.type` for scan-by-content-type triage.
- Prefer creating/editing `.base` files over Dataview.

## Titles as APIs

A note's title is its interface. Use complete, declarative phrases: "Spaced Repetition Works Because of Retrieval," not "Spaced Repetition." A well-titled note can be linked and understood without opening it. When creating or renaming notes, always prefer a full declarative statement.

## Tag conventions

Tags live in the frontmatter `tags` array, not inline in the body.

- Lowercase, hyphenated: `spaced-repetition`, not `Spaced Repetition` or `spacedRepetition`.
- Topic-oriented, not structural: `learning` (what it's about), not `important` (how you feel about it).
- Nest only when a hierarchy is genuinely useful: `ai/transformers` is fine, deep nesting is not.
- Suggest tags based on the vault's existing taxonomy rather than inventing new ones.

## Editing rules

- Preserve existing prose unless user asks to rewrite.
- Do not add or maintain an `updated` frontmatter field.
- Use dense wikilinking (`[[Note Title]]`) and allow unresolved links as stubs.
- Do not create top-level folders unless explicitly requested.
- Do not assign/change `status`, move notes, or delete notes without explicit instruction.
- Agent write surface is limited to:
  - `/ask` response callouts
  - optional daily briefing callout in journals

## Search patterns

Default QMD collections:

- `zettelclaw-inbox`
- `zettelclaw-notes`
- `zettelclaw-journal`
- `zettelclaw-attachments`

```bash
# qmd (preferred when installed)
qmd query "spaced repetition and retrieval" -c zettelclaw-notes
qmd search "status: queued" -c zettelclaw-inbox
qmd vsearch "what have I been learning about memory" -c zettelclaw-notes

# ripgrep fallback
rg -l 'type: note' "01 Notes/"
rg -l 'type: article' "00 Inbox/" "01 Notes/"
rg -l 'status: queued' "00 Inbox/" "01 Notes/"
```

## OpenClaw integration

If configuring OpenClaw memory paths, use:

- `agents.defaults.memorySearch.extraPaths`

Do not write legacy top-level `memorySearch`.
Only change OpenClaw config when the operator explicitly wants this vault wired into an OpenClaw installation.
