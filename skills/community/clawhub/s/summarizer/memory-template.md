# Working File Templates — Summarizer

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

`store_summaries` gates the content of every box below: `full` writes summary text, `index-only` writes the source row and the index but no summary body, `none` writes nothing outside `config.yaml`. When it is `none`, say so once and do not ask again.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/summarizer/config.yaml` | Key by key, read-modify-write |
| Status, box index, due dates, audiences, sources, corrections, queue | `~/Clawic/data/summarizer/memory.md` | Rewritten in place; stays small |
| A delivered summary, chunk map, or synthesis | `~/Clawic/data/summarizer/summaries/<source-kebab>.md` | Born as its own file, from the first one |
| Editions of a recurring stream | `~/Clawic/data/summarizer/editions/<stream>-<year>.md` | Append-only, cut by year |
| Terms, acronyms, entity names, and metric definitions that must survive every compression | `~/Clawic/data/summarizer/glossary.md` | One row per term, from the first |
| Output shapes the user approved or reuses | `~/Clawic/data/summarizer/templates/<name>.md` | One file per shape |
| A house style guide, banned-word list, or voice document the user supplies | `~/Clawic/data/summarizer/style-<name>.md`, pointed to by `style_file` | Replaced, not appended |
| Coverage matrices, reusable extract passes, anything long that is read whole | `~/Clawic/data/summarizer/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Sources processed, with their coverage and cut-off | `## Sources` in `memory.md`, then `sources.md` at the split threshold | One row per source |
| Corrections and the rule each one produced | `## Corrections` in `memory.md`, then `corrections.md` at the split threshold | One row per correction |
| Who a summary is written for, and their reading preferences | `## Audiences` in `memory.md`, referencing a contact key | One row per audience |
| People — recipients, counterparties, recurring participants | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill in one inventory |
| Work this summarizing belongs to — a review, an evaluation, an engagement | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project |
| **Anything durable this table does not name** | `~/Clawic/data/summarizer/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A summary was delivered that the user will look for again | `summaries/<source-kebab>.md` (`store_summaries: full`) |
| Any source was processed | Its row in `## Sources` — title, type, date, coverage, cut-off, where the summary lives |
| A long source was chunked | The level-1 chunk map inside its `summaries/` file, under `## Chunk Map` |
| A recurring edition shipped | `editions/<stream>-<year>.md`, plus the run date in `## Due` |
| A term, acronym, entity, or metric definition had to be pinned | `glossary.md` |
| An output shape was approved, or asked for a second time | `templates/<name>.md` |
| The user supplied a style guide, banned-word list, or voice document | `style-<name>.md`, and `style_file` in `config.yaml` |
| A matrix, extract pass, or other long text was produced | `artifacts/<kebab-name>.md` |
| The user corrected a summary | `## Corrections`, with the error class from `verification.md` |
| A summary was written for a named person | `## Audiences` here, and the person in the shared `contacts.md` |
| A source contained a deadline, or a cadence was agreed | `## Due` |
| A source is queued to be summarized later | `## Queue` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except summaries, editions, templates, artifacts, the glossary and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/summarizer/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Summaries, editions, templates, artifacts and the glossary are the exception: each is born as its own file whatever its size, because each is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, and above all not the source the user pastes in. Transcripts, tickets, logs, `.env` snippets and pasted config are the densest carriers of live credentials in this catalog. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:STRIPE_API_KEY` · `keychain:vpn-prod` · `1password:Work/DB/prod` · `bitwarden:Personal/Router` · `vault:kv/app/db` · `ssm:/prod/db/password` · `profile:prod` · `file:~/.ssh/id_ed25519`

When the user pastes something to save, replace each secret value before writing and leave the pointer visible: `password: <ssm:/prod/db/password>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: document and meeting titles, author and speaker names, publication and event dates, DOIs, public URLs, outlet names, issue and PR numbers, repo and branch names, version numbers, company and product names, contract party names, figures already stated in the source, ticket ids, last four digits.

**Secrets, strip them**: API keys, tokens and session cookies pasted inside a transcript or log; passwords and connection strings; private keys and passphrases; `.env` file bodies; meeting join links carrying a passcode; share links with a token in the query string; signing, webhook and pager secrets; one-time codes; and personal identifiers the summary does not need — full card or account numbers, national ID numbers, home addresses, and third-party medical detail.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [summaries/](#summaries) · [editions/](#editions) · [glossary.md](#glossarymd) · [templates/](#templates) · [artifacts/](#artifacts) · [style files](#style-files) · [shared contacts inventory](#shared-contacts-inventory) · [shared projects box](#shared-projects-box) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/summarizer/` if it does not exist.

```yaml
default_length: brief
default_audience: executive
default_mode: hybrid
output_language: same-as-source
delivery_channel: slack
markers: plain
omission_note: always
verify_pass: always
store_summaries: full
style_file: style-house.md

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  bullet_terminator: none        # no full stops on bullets
  heading_depth: 2
restrictions:
  banned_words: [leverage, utilize, synergy]
  never_paraphrase: [clause numbers, dosages]
source_handling:
  keep_chunk_maps: true
  never_store: [board minutes]
cadence:
  project_digest: weekly-friday
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Summarizer Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Sources processed (23) → `sources.md`; read before summarizing anything, to check it is not already done
- Terms that must survive compression (41) → `glossary.md`; read before any transcript, paper, or metrics source
- Q2 board pack summary → `summaries/board-pack-2026-q2.md`; read when the Q3 pack arrives
- Vector-DB evaluation matrix (7 sources) → `artifacts/vector-db-matrix.md`; read when the vendor question returns
- Weekly project digest → `editions/project-digest-2026.md`; read before writing this week's edition
- Exec brief shape → `templates/exec-brief.md`; read before writing for Dana
- House style guide → `style-house.md`; read before any externally published summary

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Project digest | week, Friday | 2026-07-24 | 2026-07-31 |
| Acme MSA — notice deadline | once | — | 2026-09-01 |

## Audiences
| Audience | Contact key | Length ceiling | Jargon | Always wants | Always cuts |
|---|---|---|---|---|---|
| Dana (CFO) | dana@example.com | 80 words | none | the number vs plan, the ask | method, tooling |
| Platform team | platform-team | standard | full | versions, failure modes | business framing |

## Sources
| Source | Type | Date | Coverage | Summary | Notes |
|---|---|---|---|---|---|
| Q2 board pack | report, 44 pp | 2026-07-14 | full | `summaries/board-pack-2026-q2.md` | figures restated vs Q1 |
| #platform channel | slack | 2026-07-25 | to 2026-07-25 17:40 | — | next edition starts here |

## Corrections
| Date | Source type | Error class | Rule it produced |
|---|---|---|---|
| 2026-06-11 | paper | hedge removal | keep the modal on every effect claim |
| 2026-07-02 | earnings | number drift | never derive a growth rate the report did not print |

## Queue
- Vendor SOC 2 report — waiting on the file
- Q3 planning doc — after the 4 Aug revision

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Cadences use `week`/`month`/`quarter`; a one-off deadline lifted out of a document uses `once` and is deleted after it passes.
- **`## Sources`**: `Coverage` is `full`, a page or timestamp range, or a cut-off — it is what makes the next edition start in the right place (`recurring.md`). One row per source; re-processing a source **updates** its row, never adds a second.
- **`## Audiences`**: the person lives in the shared contacts box; this table holds only the contact key plus what is summarizer-specific. Never write an email address, phone number, or biography here.
- **`## Corrections`**: the error class comes from the taxonomy in `verification.md`. A rule appearing twice is promoted to `config.yaml` under the restrictions area, and the correction rows stay as the evidence.
- These headings are exactly the ones `sources.md` and `corrections.md` get when their sections outgrow this file, so each split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their sources, audiences, and taste |
| `complete` | Know what they read, who they write for, and what they always cut |

## summaries/

One file per source, at `~/Clawic/data/summarizer/summaries/<source-kebab>.md`, created the first time that source is summarized. Written only when `store_summaries: full`. Every file opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Q2 board pack — summary
*Read when the Q3 pack arrives, or when a Q2 figure is questioned. Source published 2026-07-14, summarized 2026-07-26.*

Coverage: full document, 44 pp. Level: standard (240 words). Written for: Dana (CFO).

...the summary...

Omitted: segment detail for APAC, the appendix methodology.
```

For a long source, the same file carries the reusable asset below the summary:

```markdown
## Chunk Map
| # | Section | Claims | Numbers | Open threads |
|---|---------|--------|---------|--------------|
| 1 | Introduction | thesis: ... | — | defines "active account" |
| 2 | Market | 3 claims | 4.2M EUR FY25 | conflicts with ch. 7 |
```

The chunk map is why this file exists after the summary has been read: the next question about the same source is answered from the map instead of a re-read (`long-sources.md`). Never delete a chunk map to save space.

Naming: after the source, never after the date it was made — `board-pack-2026-q2.md`, not `summary-july.md`. A period in the name is part of the source's identity, not a timestamp.

## editions/

Append-only log of a recurring stream, cut by year.

```markdown
# Project digest — 2026

## 2026-07-24 — covers 2026-07-18 to 2026-07-24
New: staging cluster migrated — rollback window closes 31 Jul
Changed: launch 14 May → 4 Jun
Still open: legal review — 19 days, awaiting Priya
Resolved: upload failures on Safari — fixed in 4.2.1
Next: rollback window 31 Jul

## 2026-07-17 — covers 2026-07-11 to 2026-07-17
Nothing changed. Three items open, oldest 12 days.
```

- Newest edition at the top, so the previous one is the first thing read next week.
- The `covers` range on every edition, with no gaps and no overlaps between consecutive editions.
- A quiet period is recorded as a quiet period — never skipped silently, or the gap looks like a missing file.

## glossary.md

The box that keeps a term meaning the same thing across months of summaries. One row per term, from the first.

```markdown
# Glossary

| Term | Expansion / definition | Rule | First seen |
|------|------------------------|------|------------|
| ARR | Annual recurring revenue | Expand on first use for non-finance readers | 2026-05-02 |
| active account | Logged in within 30 days (their definition, not the industry one) | Never substitute "user" | 2026-06-14 |
| Kubernetes | — | ASR renders it "Cooper Nettie's"; repair on sight | 2026-07-03 |
| Cure Period | Defined term in the Acme MSA, 30 days from written notice | Never paraphrase; quote the clause | 2026-07-19 |
```

- `Rule` is the operative column: what to do with the term, not what it means.
- A metric whose definition is local to this user goes here the first time it appears (`data.md`), because two different definitions in two months is a defect nobody attributes to the summary.
- ASR repairs go here too (`media.md`, `meetings.md`) — the same name will be mangled the same way next episode.

## templates/

One file per approved output shape, at `~/Clawic/data/summarizer/templates/<name>.md`.

```markdown
# Exec brief — Dana
*Use for anything going to Dana. Approved 2026-06-20.*

Slots, in order:
1. The number and its comparator
2. Three supports, one line each
3. The ask, with a date — or "No decision needed"
4. Caveats, one line
Length: ≤80 words. Markers: plain. No tables.
```

Slots and constraints only — never sample content that could be mistaken for real data.

## artifacts/

One file per thing, at `~/Clawic/data/summarizer/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **coverage matrix** for a multi-source synthesis, **reusable extract pass** for a fan-out, and any long text the user asks to keep that is read whole. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Vector DB evaluation — coverage matrix
*Read when the vector-database question returns, or before adding a source to the evaluation. 7 sources, 2026-07-22.*

| Claim / dimension | A (2026, benchmark) | B (2025, vendor) | C (2026, cohort) |
|---|---|---|---|
| p95 latency at 1M vectors | 42 ms | "sub-10 ms" | not measured |
```

## style files

A style guide, banned-word list, or voice document the user supplies is a long text: it goes to its own file at `~/Clawic/data/summarizer/style-<name>.md`, and `config.yaml` holds only the path in `style_file`. Never inline it into `config.yaml`, and never paraphrase it into `memory.md` — it is the user's declaration and it is stored verbatim.

## Shared contacts inventory

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that deals with people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Dana Ruiz | dana@example.com | CFO | email | receives the weekly brief | 2026-07-24 | — |
```

- **Identity is `Key`**, and it is a column of the row, never implicit: lowercase email if there is one, otherwise the handle, otherwise `<kebab-name>` plus a stable disambiguator. `Preferred channel` is the *type* of channel, not the address, and never serves as the key.
- **Read the file before adding.** If the key is already there, update that row in place — never append a second row for the same person. Rows written by other skills are theirs: add a missing field, never rewrite their content.
- **Retirement is part of the inventory.** When a person stops being a recipient, delete the row and note the date in `memory.md`. An inventory that only grows stops being an inventory.
- **Scale cut**: one row per person while there are ≤15, or until one person no longer fits their row. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` with the same fields, and `contacts.md` becomes the index with the `File` pointer filled in. If you arrive and the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Nothing that authenticates goes in this file — no passwords, no tokens, no calendar links carrying a passcode.
- Summarizer-specific preferences stay in `## Audiences` in `memory.md`, referencing the key. Duplicating the person is how two skills end up disagreeing about who they are.

## Shared projects box

Lives at `~/Clawic/data/projects/<project>.md`, one file per project from the first, and is shared with every skill that tracks work.

```markdown
# Vector DB selection

status: active
objective: pick a vector store for the search rewrite by 2026-08-15

## Decisions
- 2026-07-22 — shortlist cut to A and C; B excluded, vendor benchmark unreproducible. Matrix: `summarizer/artifacts/vector-db-matrix.md`
```

- **Identity is the file name** (the project slug). Read the file before writing; append to the existing sections rather than creating a second file with a near-identical name.
- **Write only what this skill produced**: a decision the summarizing established, a synthesis conclusion with its date, and a pointer to the artifact. Never restate the project's own plan or status — those belong to whichever skill owns the work.
- **Closing a project is `status: done | cancelled — <date>` inside the file**, never a deletion: it is the record of what was delivered. Past ~20 closed projects, move them to `projects/archive/<project>.md` without renaming.
- **Foreign structure wins.** If the file already exists with different headings, add under the closest match rather than imposing this shape.
- People named in a project are referenced by their contacts key, never copied in.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`sources.md` — the `## Sources` table, same columns. It is the box that stops the same document being summarized twice with different conclusions, and it is the first read of any recurring job.

`corrections.md` — the `## Corrections` table, same columns. The reason this file exists is that a correction is only worth recording if it is read before the next summary of the same source type; a correction log nobody opens is a diary.
