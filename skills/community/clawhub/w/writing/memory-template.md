# Working File Templates — Writing

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/writing/config.yaml` | Key by key, read-modify-write |
| Voice traits, format habits, the never-list, corrections, pieces in flight, audiences, box index, due dates | `~/Clawic/data/writing/memory.md` | Rewritten in place; stays small |
| Their own writing kept as the reference for a voice | `~/Clawic/data/writing/samples/<kebab-name>.md` | One file per sample, from the first |
| House style for a publication, client, employer or project | `~/Clawic/data/writing/style-sheets/<context>.md` | One file per context, from the first |
| Things you produced that get re-read — reusable templates, standing bios and sign-offs, editorial letters, briefs, outlines that survived the piece | `~/Clawic/data/writing/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Finished and published pieces | `~/Clawic/data/writing/pieces/<year>.md` | Append-only, cut by year |
| People they write to or for — editors, clients, managers, recurring recipients | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill's contacts in one file |
| Writing projects with a life beyond one piece — a newsletter, a client's blog, a report series | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project; the style sheet stays in `style-sheets/` and is named from it |
| **Anything durable this table does not name** | `~/Clawic/data/writing/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A voice trait was confirmed, corrected, or contradicted twice | `## Voice` |
| The user rejected a word, phrase, construction or move ("never say that") | `## Never` |
| They shared writing of their own that is representative | `samples/<kebab-name>.md` |
| They stated how they handle a format or channel | `## Formats` |
| They edited your draft | `## Corrections` — what you wrote, what they changed it to |
| A style decision was made for a publication, client or project | `style-sheets/<context>.md` |
| A piece was finished, sent or published | `pieces/<year>.md`, and its row leaves `## Pieces` |
| A piece was commissioned or started, with a deadline | `## Pieces` |
| A template, bio, sign-off, outline or editorial letter will be reused | `artifacts/<kebab-name>.md` |
| A named person's register or channel preference was learned | Their row in `contacts.md` |
| A recurring deadline or review cycle was agreed | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except samples, style sheets, artifacts, the pieces log and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/writing/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Samples, style sheets and artifacts are the exception: each is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:GHOST_ADMIN_KEY` · `keychain:substack` · `1password:Work/Newsletter/api` · `bitwarden:Personal/Medium` · `file:~/.config/newsletter/token`

When the user pastes something to save, replace each secret value before writing and leave the pointer visible: `api_key: <env:GHOST_ADMIN_KEY>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: publication and outlet names, editor and client names, bylines, public URLs of published work, word counts and deadlines, subscriber counts, style rules, document titles, and the user's own prose. **Secrets, strip them**: publishing-platform API keys and admin tokens (Ghost, Substack, WordPress, Medium, Mailchimp), SMTP and app passwords, share or preview links carrying an access token (`?token=`, `?key=`), CMS logins, and anything inside a pasted `.env` or credentials block.

One more thing that is not a credential but still does not belong here: third-party personal data that arrives inside a pasted draft — identity numbers, card numbers, medical details, home addresses. Leave them in the draft you hand back; keep them out of every file under `~/Clawic/data/`.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [samples/](#samples) · [style-sheets/](#style-sheets) · [artifacts/](#artifacts) · [pieces/](#pieces) · [shared contacts box](#shared-contacts-box) · [shared projects box](#shared-projects-box) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/writing/` if it does not exist.

```yaml
spelling: uk
edit_depth: heavy
cut_target_pct: 25
feedback_mode: rewrite
explain_edits: true
markup: markdown
voice_file: voice-guide.md

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  oxford_comma: false
  headings: sentence-case
  numerals: "spell out under 10"
channels:
  newsletter: buttondown
  social: [linkedin]
restrictions:
  no_claims: ["guaranteed", "fastest in the market"]
languages:
  primary: en-GB
  also_writes: [es]
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Writing Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Voice samples (4) → `samples/`; read before any first draft in a new format, and whenever voice is disputed
- Newsletter house style → `style-sheets/newsletter.md`; read before every issue
- Acme client style → `style-sheets/acme.md`; read before anything under the Acme byline
- Cold outreach template → `artifacts/cold-intro-email.md`; read before writing a cold email
- Standing bios (25/50/100 words) → `artifacts/bios.md`; read whenever a bio, byline or speaker blurb is requested
- Published pieces (31) → `pieces/2026.md`; read before pitching, to avoid re-proposing a covered angle

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Newsletter issue | week, Thursday | 2026-07-23 | 2026-07-30 |
| Voice re-check against latest samples | quarter | 2026-04-10 | 2026-07-10 |

## Voice
Sentence length 8-22 words, wide spread, one very short sentence per paragraph.
Concrete subjects: people and products in the subject slot, almost never "this" or "it".
Contractions always. Second person for the reader, first person singular for themselves — never "we".
Opens on a scene or a number; closes on a consequence, never a summary.
Dry, understated humour; no exclamation marks.

## Formats
- Email: 4 lines maximum, ask in line 1, no greeting beyond the name
- Newsletter: one idea, 700-900 words, a standing "what I'm reading" block at the end
- LinkedIn: 150 words, line-1 payload, no hashtags

## Never
- "utilize", "leverage" as a verb, "delve", "in today's fast-paced world"
- Rhetorical questions as an opening
- Em-dash pairs in client work (fine in personal writing)
- Claims about competitors by name

## Corrections
| Date | You wrote | They changed it to | Trait |
|------|-----------|--------------------|-------|
| 2026-06-14 | "This enables teams to..." | "Your team can..." | Second person, actor as subject |
| 2026-07-02 | Three-item list with a summary line | The three items, no summary | No summaries |

## Pieces
| Piece | Format | For | Words | Due | Status |
|-------|--------|-----|-------|-----|--------|
| Pricing teardown | blog post | own site | 1,200 | 2026-08-05 | outline agreed |

## Audiences
Newsletter: ~2,100 subscribers, mostly technical founders. Acme blog: their marketing team edits before publishing.

## How They Work
Wants the rewritten text, not notes. Reads everything on a phone. Sends the draft, then asks for the cut separately.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring deadline and review cycle this skill agrees to belongs here.
- **`## Voice`**: observed traits only, phrased as behaviour that can be checked against a draft ("one very short sentence per paragraph"), never as an adjective ("punchy"). An adjective cannot be verified by the Output Gates. If `voice_file` is set, that document outranks this section wherever they conflict.
- **`## Never`**: absolute, and checked by an Output Gate. Anything conditional belongs in `## Formats` or a style sheet with its condition attached, because a never-list with exceptions stops being checkable.
- **`## Corrections`**: the `Trait` column is what makes this worth keeping — a correction with no extracted trait is an anecdote. When the same trait appears three times, promote it to `## Voice` and leave the rows where they are.
- **`## Pieces`** holds what is in flight only. When a piece ships, its row moves to `pieces/<year>.md` with the outcome, and leaves this table. A piece nobody is writing any more is not in flight; delete the row and note why.
- These headings are exactly the ones the split-out files get, so a split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their voice; check the draft against samples |
| `complete` | Voice is established; drafts can go straight to the Output Gates |
| `paused` | User asked to stop recording preferences — read what exists, write nothing new |

## samples/

One file per sample of the user's own writing, at `~/Clawic/data/writing/samples/<kebab-name>.md`, created the first time they share something representative. A sample is the evidence behind `## Voice`; without it, a disputed trait cannot be settled and gets re-argued.

```markdown
# Sample — launch announcement, own newsletter
*Read when: writing a newsletter issue, or when a voice trait is disputed. Captured 2026-07-26. Their words, unedited.*

Context: they wrote this alone, no editor, and called it "exactly right".
Metrics: 412 words · sentences 6-24 words · 3 paragraphs of 2 sentences

...the text, verbatim...
```

- Keep it verbatim. A sample you tidied is no longer evidence of anything.
- Three to five samples across their real formats beat twenty of the same kind. Once a format has two samples that agree, stop collecting for that format.
- If the user shares something written *by someone else* as a target voice, say so in the file's first line and never merge it into `## Voice` — it is an aspiration, not their fingerprint.

## style-sheets/

One file per context at `~/Clawic/data/writing/style-sheets/<context>.md` — a publication, a client, an employer, a project, a byline. Read before writing anything in that context; this is the file that stops the same decision being re-made every piece.

```markdown
# Style sheet — Acme blog
*Read before anything published under the Acme byline. Started 2026-05-02, last decision 2026-07-19.*

Spelling: US · Oxford comma: yes · Headings: title case · Numerals: spell out under 10
Length: 900-1,300 words. Hard cap 1,400, enforced by their CMS.
Voice: second person, no first person singular. Product name never abbreviated.
Terminology: "customer" not "user"; "platform" not "tool"; "sign in" not "log in"
Banned: "revolutionary", "seamless", any competitor by name
Structure: H2 every 200-300 words, a takeaway box after the third section
Review: their marketing team edits before publishing; expect the intro to be rewritten
Open questions: whether case-study numbers need legal sign-off — asked 2026-07-19
```

- One line per decision, with the answer, not the debate. The debate goes in the same line only when it will otherwise be reopened.
- A rule contradicted by the user's own `## Never` list: the style sheet wins inside its context, and the conflict gets a line here saying so.
- If the context is also a project, this file holds the style and `~/Clawic/data/projects/<project>.md` holds the work; each names the other, and neither copies the other's content.

## artifacts/

One file per thing, at `~/Clawic/data/writing/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **reusable template** (a cold email, an intro, a decline, a follow-up sequence), **standing text** (bios at each length, sign-offs, boilerplate, disclaimers), **editorial letter**, **brief**, and **an outline that outlived its piece**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Cold intro email — the version that gets replies
*Read when: writing a cold email or a first approach. Written 2026-06-11, 4 sends, 3 replies.*

Structure: specific fact about them → the one line of relevance → a yes/no ask → an easy out.
...the template, with [brackets] for the parts that change...
Do not reuse: the postscript — it read as a gimmick the second time.
```

```markdown
# Bios — 25 / 50 / 100 words
*Read whenever a bio, byline, speaker blurb or profile is requested. Updated 2026-07-04.*

25: ...
50: ...
100: ...
Rule: the three must agree on role and current work; update all three or none.
```

## pieces/

The log of finished work, cut by year. This is what makes "have I already written about this?" answerable, and what a pitch is checked against.

```markdown
# Pieces — 2026

| Date | Title | Format | Where | Words | Outcome |
|------|-------|--------|-------|-------|---------|
| 2026-07-11 | Pricing without a sales team | blog post | own site | 1,140 | best-read post of the quarter |
| 2026-07-23 | Issue 44 — the boring migration | newsletter | own list | 810 | 3 replies, 1 unsubscribe |
```

- `Outcome` is one clause of what actually happened, recorded only if it is known. An empty outcome column is honest; an invented one poisons every future decision made from this table.
- A piece that was killed stays in the table with `Outcome: killed — <reason>`. The reason is the reusable part.

## Shared contacts box

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that deals with people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Marta Ruiz | marta@acme.com | Editor, Acme blog | email | Cuts intros hard; wants the ask in line 1 | 2026-07-19 | — |
```

- **Identity is `Key`**: lowercase email if there is one, otherwise a handle, otherwise `<kebab-name>` plus a stable disambiguator. The key is a column of the row, never implied by the file name. `Preferred channel` is the *type* of channel, not an address, so it can never serve as the key.
- **Read the file before adding.** If the key is already there, update the row in place — never append a second row for the same person. Rows written by another skill are not yours to rewrite; add what is missing to the `Context` cell and leave the rest.
- What this skill contributes to `Context` is register and channel: how they want to be written to, what they cut, what they never reply to. Not their life story.
- **Retirement**: when a relationship ends, delete the row and note the date in `memory.md`. A contact list that only grows stops being a contact list.
- **Scale cut**: one row per person while there are ≤15, or until one person no longer fits on a row. Past that, a file per person at `~/Clawic/data/contacts/<name>.md` with the same fields, and `contacts.md` becomes the index with the `File` pointer filled in. If you arrive and the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Never a password, a private phone number the user did not ask you to keep, or an access token. A credential reference, if one is unavoidable, is a pointer only.

## Shared projects box

Lives at `~/Clawic/data/projects/<project>.md`, one file per project, shared with every skill that tracks work. Used here when a writing job has a life beyond one piece: a newsletter, a client's blog, a report series, a book proposal in progress.

```markdown
# Acme blog — ghostwritten series
status: active
owner: Marta Ruiz (see contacts)
goal: 2 posts a month under the Acme byline, through 2026-12
style: ~/Clawic/data/writing/style-sheets/acme.md
milestones:
- 2026-06-30 — first three posts published
decisions:
- 2026-05-02 — second person throughout, no first-person singular
```

- **Identity is the project name**, which is the file name in kebab case. Read the folder before creating a file: if the project is already there under another skill's hand, add to it rather than starting a second file.
- **The style stays in `style-sheets/`, the work stays here**, and each names the other by path. Duplicating the style rules into the project file guarantees two versions that disagree within a month.
- **The client or editor goes in `contacts.md`** and is referenced here by name only. Never duplicate the person record inside the project file.
- **Retirement**: a finished project keeps its file with `status: done — <date>` — it is the record of what was delivered. Never delete it. Past ~20 closed projects, move them to `~/Clawic/data/projects/archive/<project>.md` without renaming.
- **Foreign structure wins.** If the file already exists with different fields, add yours as new lines and leave theirs alone.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`voice-profile.md` — `## Voice`, `## Formats`. These travel together: a format habit is a voice trait with a condition on it, and separating them means checking two files before every draft.

`corrections.md` — `## Corrections`, `## Never`. The reason this file earns its existence is the `Trait` column: without it, the same correction is made every quarter and no trait is ever promoted to `## Voice`.

`pieces-in-flight.md` — `## Pieces`. Only reached by someone running many commissions at once; the finished-work log is `pieces/<year>.md` and is a different file for a different question.
