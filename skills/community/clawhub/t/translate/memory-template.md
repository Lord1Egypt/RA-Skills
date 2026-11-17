# Working File Templates — Translate

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/translate/config.yaml` | Key by key, read-modify-write |
| Language pairs in use, register per locale, environment facts, pain points, box index, due dates | `~/Clawic/data/translate/memory.md` | Rewritten in place; stays small |
| Term decisions, do-not-translate items, forbidden renderings | `## Glossary` in `memory.md` while there is one pair and few terms; `~/Clawic/data/translate/glossaries/<src>-<tgt>.md` from the second pair or past the threshold | One row per term, per pair |
| A locale's long-form style guide — register, punctuation, voice, worked examples | `~/Clawic/data/translate/styles/<locale>.md` | Born as its own file the first time a locale has more than a one-line rule |
| Jobs delivered: date, pair, content type, word count, tool, reviewer, issues | `~/Clawic/data/translate/deliveries/<year>.md` | Append-only, cut by year |
| Things you produced that get re-read — translation briefs, LQA reports, back-translation reports, pseudolocalization findings, subtitle or character-limit specs, pronunciation guides, naming decisions, job query logs, scope-change logs, approved reference texts | `~/Clawic/data/translate/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| A translator, reviewer, agency, or in-market checker | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill's contacts in one file |
| A localization effort tracked as work in progress | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project |
| What a CAT tool, MT API plan, or agency retainer costs per month | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row per subscription |
| **Anything durable this table does not name** | `~/Clawic/data/translate/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A term was decided, or a candidate rejected | Its row in `## Glossary` (or the pair's glossary file) |
| A brand, product, or code-like item must stay untranslated | `### Do Not Translate` |
| A reviewer or the user corrected a rendering | `### Forbidden Renderings`, with the accepted form |
| Register, variant, or script was settled for a locale | `## Locale Register`; anything longer than a line goes to `styles/<locale>.md` |
| A new language pair was worked in | `## Language Pairs` |
| A job was delivered | A row in `deliveries/<year>.md` |
| Something about the setup cost effort to find — where the strings live, which plural categories the framework exposes, a font missing a script, a CMS that mangles entities, an MT engine's behavior on this content | `## Environment` |
| A defect reached the reader, or a session went wrong | `## Pain Points`, with the cause |
| A brief, LQA report, back-translation, pseudoloc pass, subtitle spec, pronunciation guide, or reference text was produced | `artifacts/` |
| A query was answered, or the source changed mid-project | `artifacts/queries-<job>.md` or `artifacts/scope-changes-<job>.md` — the one for that job, created on the first entry |
| A translator, reviewer or agency was named | The shared contacts box |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except style guides, delivery logs, artifacts and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, promoted one level (`### Terms` inside `memory.md` becomes `## Terms` in the extracted file), so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

The glossary has one extra trigger: **a second language pair splits it immediately**, whatever the entry count, because a term table mixing pairs cannot be read while translating into either one. Destination `glossaries/<src>-<tgt>.md`, with the source and target as BCP 47 codes (`en-es`, `en-pt-BR`).

Artifacts and style guides are the exception to counting: a brief, an LQA report or a locale style guide is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:DEEPL_AUTH_KEY` · `env:OPENAI_API_KEY` · `keychain:phrase-token` · `1password:Work/Lokalise/api` · `bitwarden:Clients/Acme/tms` · `file:~/.config/trados/credentials`

When the user pastes something to save — a TMS config, a CI snippet that pushes translations, a `.env` from the localization pipeline — replace each secret value before writing and leave the pointer visible: `auth_key: <env:DEEPL_AUTH_KEY>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: locale and script codes, glossary terms and their renderings, repository paths and catalog filenames, TMS project ids and TM names, engine and platform names, word counts, rates and prices with their currency, invoice numbers, translator names and roles. **Secrets, strip them**: MT and CAT API keys and auth tokens, TMS and webhook secrets, CI tokens that push locale files, client portal passwords, anything inside a pasted `.env` or credentials file.

One more rule that is not about credentials: **source documents are usually confidential, and often full of personal data** (medical records, contracts, HR letters). Keep the terminology and the decisions, never the document. If a reference text must be kept, save the excerpt the decision rests on, strip the names, and say so.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [glossaries/](#glossaries) · [styles/](#styles) · [deliveries/](#deliveries) · [artifacts/](#artifacts) · [shared contacts](#shared-contacts) · [shared projects](#shared-projects) · [shared subscriptions](#shared-subscriptions)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/translate/` if it does not exist.

```yaml
source_lang: en
target_locales: [es-419, pt-BR, de-DE, ja-JP]
formality: per-locale
variant_policy: regional
mt_policy: mtpe
review_stage: second-person
placeholder_style: icu
catalog_format: json
subtitle_cps: 17
deliverable_shape: bilingual-table
cat_tool: phrase

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  key_naming: screen.section.element
  translator_notes: "developer comment above the key"
voice:
  inclusive_language: brand-approved-list-only
  humor: "keep it, never invent it"
risk_posture:
  mt_banned_for: [legal, medical, safety]
  certification_authority: "receiving institution decides"
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Translate Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Glossary en→es-419 (46 terms) → `glossaries/en-es-419.md`; read before translating into es-419
- Glossary en→ja (31 terms) → `glossaries/en-ja.md`; read before translating into ja
- ja-JP style guide → `styles/ja-JP.md`; read before any Japanese copy, UI or marketing
- Deliveries 2026 (22 jobs) → `deliveries/2026.md`; read when quoting, or when asked what was done for a client
- Onboarding LQA, June → `artifacts/lqa-onboarding-es-419.md`; read before touching onboarding strings again
- Mobile character limits → `artifacts/char-limits-mobile.md`; read before translating any mobile UI string

## Due
| What | Every | Last run | Next due |
|---|---|---|---|
| Glossary consolidation across pairs | quarter | 2026-04-12 | 2026-07-12 |
| TM cleanup: duplicates and outdated segments | 6 months | 2026-02-03 | 2026-08-03 |
| In-market review of the top 10 pages | quarter | 2026-05-20 | 2026-08-20 |
| Re-check MT output after an engine or model change | on change | 2026-06-01 | on change |

## Language Pairs
| Source | Target | Content types | Volume | Who reviews |
|---|---|---|---|---|
| en | es-419 | app UI, help center | ~4k words/month | Ana (see contacts) |
| en | ja | app UI, store listing | bursts at release | agency (see contacts) |

## Locale Register
| Locale | Address form | Variant / script | Notes |
|---|---|---|---|
| es-419 | tú | neutral Latin American, no voseo | "computadora", never "ordenador" |
| de-DE | Sie in product, du in marketing emails | — | decision made 2026-03-04 by the user |
| ja | desu/masu, no keigo escalation in UI | — | full guide in `styles/ja-JP.md` |

## Glossary
### Terms
| Source | Target | Pair | Part of speech | Context / why | Set on |
|---|---|---|---|---|---|
| workspace | espacio de trabajo | en→es-419 | noun | never "área"; matches the UI label; approved by Ana, in-market | 2026-03-11 |

### Do Not Translate
Acme · Acme Cloud · SmartSync (registered) · `webhook` (kept in English by the dev team) · error codes `ACM-###`

### Forbidden Renderings
| Wrong | Right | Pair | Why |
|---|---|---|---|
| "ordenador" | "computadora" | en→es-419 | Peninsular; the market is Mexico and Colombia |
| "アカウントを削除しますか" | "アカウントを削除してもよろしいですか" | en→ja | the short form reads abrupt in a destructive dialog |

## Environment
Strings live in `apps/web/locales/<locale>.json`, i18next v23 (`_one`/`_other` suffixes, no CLDR `few`). Mobile uses `.xcstrings` and `strings.xml` — plurals only exist on mobile. Help center is Zendesk; its editor strips `<xliff:g>`. Devanagari has no font in the PDF template.

## Pain Points
2026-05: a `%1$s`/`%2$s` swap in German shipped and crashed the invoice screen. Placeholder parity is now checked per file, not per segment.

## How They Work
Ships weekly; wants the file back, not a discussion. Cares about register more than speed.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here. `on change` is a valid cadence: it fires on the named event, not on a date.
- **`## Glossary`**: the three sub-headings are exactly the ones a pair's glossary file gets when it splits (`## Terms`, `## Do Not Translate`, `## Forbidden Renderings`), so the split stays a copy-paste. `Set on` is the decision date, which is what settles an argument two releases later, and `Context / why` also carries who approved a contested term (`approved by Ana, in-market`) and `pending` when the decision was taken under time pressure — the pair `who + when` is what makes the row re-usable instead of re-arguable.
- **`## Locale Register`**: one row per locale, not per job. A row that needs a paragraph is a `styles/<locale>.md` waiting to be created; leave the one-line summary here and the pointer in `## Boxes`.
- **`## Environment`** holds facts that change future decisions, in prose, not incident notes — those go in `## Pain Points`.

| Status | Meaning |
|---|---|
| `ongoing` | Still learning their content, terminology and register |
| `complete` | Glossary, style and register settled for every active pair |

## glossaries/

One file per language pair, at `~/Clawic/data/translate/glossaries/<src>-<tgt>.md`, created by the split procedure above or immediately when a second pair appears.

```markdown
# Glossary — en → es-419

## Terms
| Source | Target | Part of speech | Context / why | Set on |
|---|---|---|---|---|
| workspace | espacio de trabajo | noun | UI label; never "área"; approved by Ana, in-market | 2026-03-11 |
| to sync | sincronizar | verb | never "sincronizar con" unless an object follows | 2026-03-11 |

## Do Not Translate
Acme · SmartSync · `webhook` · error codes `ACM-###`

## Forbidden Renderings
| Wrong | Right | Why |
|---|---|---|
| ordenador | computadora | Peninsular; market is Mexico and Colombia |
```

- **Identity is the source term plus its part of speech.** The same word in two parts of speech is two rows, because `sync` the noun and `sync` the verb are different words in most targets.
- Read the file before adding: if the term is there, do not add a second row — either the new context justifies a part-of-speech row, or the existing row is wrong and gets corrected in place with a new `Set on`.
- Past ~200 terms the file stops being readable in one pass; split by domain (`glossaries/en-es-419-ui.md`, `-legal.md`) and leave the pair file as the index. Keep the same three headings.
- Terms are never deleted silently: a rendering that changes moves to `## Forbidden Renderings` with the new one, so old text can be found and fixed.

## styles/

One file per locale, at `~/Clawic/data/translate/styles/<locale>.md`, created the first time a locale's rules outgrow a single line in `## Locale Register`. Read whole, before any writing into that locale.

```markdown
# Style — ja-JP
*Read before writing any Japanese: UI, marketing, or support. Updated 2026-06-02.*

Register: desu/masu throughout; no sonkeigo or kenjōgo in product UI, even in error messages.
Punctuation: full-width 。、 ; no space before or after parentheses; ASCII digits.
Line breaking: never start a line with 。、」or ) — kinsoku applies in the app's own renderer.
Voice: shorter than the English; drop "please" rather than translate it.
Worked example: "Are you sure you want to delete this?" → 「削除してもよろしいですか？」 (not 削除しますか)
```

If the user supplies their own style guide as a document, save it here under the same name and record the source and date at the top rather than rewriting it in your words.

## deliveries/

```markdown
# Deliveries — 2026

| Date | Pair | Content type | Words | Tool | Reviewer | Issues found | Project |
|---|---|---|---|---|---|---|---|
| 2026-07-14 | en→es-419 | app UI, release 4.2 | 1,840 | phrase | Ana | 2 minor, 0 major | acme-localization |
| 2026-07-21 | en→ja | store listing | 620 | none | agency | 1 major (register) | acme-localization |
```

- `Words` is the source word count, so two rows are comparable; note the count method if it was not a word count (subtitle minutes, page count) in the same cell (`620 words`, `18 min`).
- `Project` is the name of the shared project file, when one exists — a pointer, never a copy.
- Cut by year. A year with more than ~150 rows splits by quarter (`deliveries/2026-q3.md`), leaving `2026.md` as an index table (`Date | Pair | Words | → file`).

## artifacts/

One file per thing, at `~/Clawic/data/translate/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **translation brief**, **LQA report**, **back-translation report**, **pseudolocalization findings**, **subtitle or character-limit spec**, **pronunciation guide**, **naming or transcreation decision**, **job query log** (`queries-<job>.md`: segment reference, question, answer, date, who answered), **scope-change log** (`scope-changes-<job>.md`: date, what changed, word delta), **conversion table**, **approved reference text**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# LQA — onboarding, en→es-419
*Read before touching onboarding strings again. 2026-06-18.*

Sample: 1,100 of 4,200 words. Weights: minor 1, major 5, critical 10.
Score: 100 − (14 × 100 / 1100) = 98.7 — pass at ≥98.
Errors: 6 terminology (all "área" for workspace, now a forbidden rendering), 1 major mistranslation of a
negation in the trial-expiry notice, 2 punctuation.
Action taken: glossary row added, negation segment retranslated, reviewer asked to re-check trial strings only.
```

```markdown
# Naming decision — product name in zh-Hans
*Read before any Chinese marketing or store copy. 2026-05-30.*

Decision: keep the Latin brand, add a descriptive Chinese subtitle; no phonetic transliteration.
Rejected: 艾克米 — reads as a generic transliteration and one native reader heard "aching".
Cleared by: trademark check pending (see the project file).
```

If the user tracks the effort as a project, the decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the reasoning staying here and referenced by name.

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that knows people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|---|---|---|---|---|---|---|
| Ana Rivera | ana@example.com | reviewer, es-419 | email | in-market review, invoices monthly | 2026-07-14 | — |
```

- **Identity is `Key`**: the email in lowercase; if there is none, the handle; if neither, `<kebab-name>` plus a stable disambiguator. The key is a column of the row, never implicit.
- Read the file before adding. If the key is already there, update that row in place — never a second row for the same person. Only rows you created are yours to change; leave other skills' rows alone.
- `Preferred channel` is the type of channel (email, WhatsApp, Slack), not the address.
- **Scale cut**: one row per person while there are ≤15, or until one no longer fits its row. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` and `contacts.md` becomes the index with the `File` pointer. If you arrive and the folder already looks like that, follow it.
- **Foreign columns win.** If `contacts.md` exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Rates belong here only as a note with the currency (`0.11 EUR/word`), never a bank detail, portal password, or contract file.
- Removing someone: delete the row and note the date in `## Pain Points` or `## Language Pairs` in `memory.md`, whichever explains why. A contact list that only grows stops being one.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per project, from the first one. Used when the localization effort is work in progress the user tracks — a launch into three locales, a full site translation, a game release.

```markdown
# acme-localization
status: active
goal: ship es-419, pt-BR and ja for release 5.0
milestones: strings frozen 2026-08-01 · translation 08-08 · in-market review 08-15 · release 08-22
decisions: regional variants, not neutral Spanish (2026-05-30) · brand name stays Latin in zh (see translate artifacts)
```

- Identity is the project slug, which is the filename. Read before writing; update the existing file in place.
- Closing it is `status: done | cancelled — <date>` inside the file, never deleting it: it is the record of what was delivered. Past ~20 closed projects, move them to `projects/archive/<project>.md` without renaming.
- Keep the localization detail in this skill's boxes and leave only the decision line here. Duplicating a decision in two places is how two skills start contradicting each other.

## Shared subscriptions

Lives at `~/Clawic/data/finances/subscriptions.md`. Write here only when the user names what a tool or retainer costs.

```markdown
# Subscriptions

| Name | What it is | Monthly | Renews | Owner | Reference |
|---|---|---|---|---|---|
| DeepL Pro | MT API for draft translation | 25 EUR | monthly | user | env:DEEPL_AUTH_KEY |
| Phrase | TMS and translation memory | 145 EUR | annual, 2027-02-14 | user | 1password:Work/Phrase |
```

- Identity is `Name`. Read before adding; if it is there, update the row in place.
- **Amounts carry their currency inside the value** (`25 EUR`), because rows from other skills are in other currencies and someone will add the column up. An annual price stays annual with its renewal date rather than being divided into a fake monthly figure.
- Cancelling is deleting the row and noting the date in `memory.md` — a subscription list that only grows is a budget that never falls.
- `Reference` is a pointer, never a key or a card number.
- **Foreign columns win**: match the file's existing header, add what is missing as a trailing note.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`, promoted one level.

`glossaries/<src>-<tgt>.md` — `## Terms`, `## Do Not Translate`, `## Forbidden Renderings`. The forbidden renderings are the reason this file earns its keep: without them the same wrong word is re-proposed every release and re-rejected by the same reviewer.

`pairs.md` — `## Language Pairs` and `## Locale Register`, once the user works in more than a handful of locales. Same two headings, same columns.
