---
name: Writing
slug: writing
version: 1.1.2
description: Drafts, edits, and rewrites prose in the user's own voice — emails, posts, essays, memos, proposals, social copy. Use when asked to write, draft, edit, tighten, shorten, rewrite, or proofread something; when a draft reads flat, wordy, robotic, or "not like me"; when a piece will not start, a sentence will not come out right, or the ending trails off; when an email has to deliver bad news, say no, chase a reply, or make an ask that lands; when a post needs a hook, a headline, or a cut to fit a limit; when order, transitions, or paragraph structure are the real problem; when writing in a second language, or matching a house style, spelling variant, or word count. Learns and reuses their voice across sessions. Not for grammar-only fixes (`grammar`), sales copy (`copywriting`), book manuscripts (`book-writing`), journal papers (`academic-writing`), narrative craft (`storytelling`), versioned draft-and-audit workflows (`write`), or inbox triage and follow-ups (`email-management`).
homepage: https://clawic.com/skills/writing
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: ✍️
    os:
    - linux
    - darwin
    - win32
    displayName: Writing
    configPaths:
    - ~/Clawic/data/writing/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/writing/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/writing/config.yaml` (what the user declared) and `~/Clawic/data/writing/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/contacts/contacts.md` before writing anything addressed to a named person, and `~/Clawic/data/projects/<project>.md` before writing into an ongoing project. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a voice trait confirmed or corrected; a sample of their own writing worth keeping; a rejection ("never say that"); a format or channel convention they hold; a style sheet for a publication, client, or project; a piece finished or published; a template that worked and will be reused — a cold email, a bio, a sign-off, an editorial letter, an outline. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People they write to and for go to the shared box `~/Clawic/data/contacts/contacts.md`**, not here: one file holds the editor, the client and the manager whoever added them, so the register for "an email to Marta" survives whichever skill wrote it. One row per person, identified by `Key` (lowercase email → handle → kebab name). Update your own row in place; never add a second row for the same key.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `env:GHOST_ADMIN_KEY`, `keychain:substack`, `1password:Work/Newsletter/api`, `file:~/.config/newsletter/token`.

Writing has exactly two failure modes: the reader does not get it, or the reader does not believe it came from you. Diagnose which one before touching a sentence — the fix for the first is structure and cuts, the fix for the second is voice, and applying either to the other wastes the pass. Deliver the text, not advice about the text. Work from defaults immediately: never open with questions about their style, their audience, or how proactive to be. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: locale, language) → the Configuration table default.

## When To Use

- Drafting from scratch: emails, messages, posts, essays, memos, proposals, updates, bios, cover letters, speeches
- Editing existing prose: tightening, restructuring, cutting to a limit, fixing a flat or generic draft, proofing before send
- Voice work: learning how a person writes, reproducing it, checking a draft against it, writing under a brand or another person's byline
- Diagnosing a draft that is "wrong" without the user being able to say why — order, rhythm, register, or a buried ask
- Standing consistency: house style sheets, spelling variants, terminology, recurring formats and their conventions
- Writing in a second language, where the errors are register and idiom rather than grammar
- Not for grammar and spelling correction alone (`grammar`), conversion-driven sales copy (`copywriting`), narrative craft and story arcs (`storytelling`), or book-length projects (`book-writing`) — this is the general prose craft under all four
- Not for the workflow around the text either: a versioned draft-and-audit pipeline with numbered revisions and sign-off gates is `write`, and deciding which mail to answer, routing it, and chasing the follow-ups is `email-management` — this skill writes the words once that pipeline hands it a piece to write

## Quick Reference

| Situation | Play | Depth |
|-----------|------|-------|
| "Make this better", no other instruction | Structure pass, then the cut to `cut_target_pct`, then voice — in that order (Rule 2) | `revision.md` |
| "That doesn't sound like me" | Re-derive the fingerprint from stored samples, then offer two variants and let the pick be the signal | `voice.md` |
| Draft reads flat, generic, or machine-written | Structural tells first: uniform sentence length, abstractions in the subject slot, stacked hedges, tricolons | `clarity.md` |
| Blank page, or the draft will not start | Three-move outline, then a timeboxed zero draft written from the middle | `drafting.md` |
| All the parts are there and it still reads wrong | Order and transitions, not sentences — pick the shape the purpose demands | `structure.md` |
| Clear in your head, mush on the page | Character in the subject slot, action in the verb, nominalization deleted | `clarity.md` |
| Too long for the slot | Cut arithmetic: whole sections, then clauses, then adjectives last (Rule 3) | `revision.md` |
| Email that has to land: bad news, a no, a chase, a cold ask, an apology | One ask, in the first screen, with a deadline and an owner | `emails.md` |
| Blog post, essay, op-ed — hook, headline, or a pitch to an editor | Lead types, headline patterns, scannability, the outlet's own word limit | `posts.md` |
| X, LinkedIn, a thread, a bio, a comment | Payload in line 1, hard character limits, thread spine | `social.md` |
| Memo, proposal, status update, exec summary, announcement, performance review | Decision-first shape; what each document owes its reader | `workplace.md` |
| Editing someone else's draft, or answering an editor's notes | Severity tiers, editorial letter vs inline, what you may not touch | `feedback.md` |
| Same voice across many pieces, a publication's house style, a spelling variant | A style sheet as a written artifact, with the decisions that keep getting re-litigated | `style-guide.md` |
| Writing in a language that is not their first | Register and L1 interference, hedging calibration, idiom risk | `second-language.md` |
| Anything else writing | Name the format, the one reader, and the single thing that must happen after reading; draft to that, then run the Output Gates | — |

Coverage map: `voice.md` fingerprint and personas · `drafting.md` blank page to zero draft · `structure.md` shapes, order, openings, endings, titles · `clarity.md` sentence surgery and readability math · `revision.md` the pass system and the cut · `emails.md` email and chat · `posts.md` posts, essays, articles, pitching · `social.md` short-form channels · `workplace.md` business documents · `feedback.md` editing others and being edited · `style-guide.md` house style and consistency at scale · `second-language.md` writing in an L2.

## Core Rules

1. **Read the voice before writing a word.** `## Voice`, `## Never` and `## Formats` in `memory.md`, plus any sample or style sheet `## Boxes` points at for this format. Writing first and adjusting after produces a draft the user has to reject once before getting what they already told you — the single most expensive mistake in this domain, because it costs their trust and not just a turn.
2. **Structure before sentences.** Before polishing anything, state the piece's claim in one sentence and its moves in order. If you cannot, the problem is not the prose and no line edit will fix it (`structure.md`). Line-editing a piece whose order is wrong is work that gets deleted.
3. **The cut is arithmetic, not taste.** Target reduction = draft words × `cut_target_pct` (default 20%); target length = draft words × (1 − `cut_target_pct`). A 1,200-word draft loses 240 words and comes back at ≤960 — the target is what leaves, never what stays. King's rule of thumb — second draft = first draft − 10% — is the floor, not the ceiling. Order of cutting: whole sections, then sentences that restate, then subordinate clauses, then adjectives. Adjective-hunting alone recovers a marginal fraction and leaves every structural repetition in place.
4. **Match the fingerprint, not the tics.** A voice is four measurable things: sentence-length distribution, who or what occupies the subject slot, concreteness ratio, and the never-list. Copying catchphrases without those four produces parody, and users read parody as mockery (`voice.md`).
5. **One ask, once, in the first screen.** Any piece that wants something states it before the context that justifies it: what, by when, by whom. Context after the ask is read; context before the ask is skipped and then blamed for the confusion (`emails.md`, `workplace.md`).
6. **Deliver the text, not the advice.** Default output is the finished passage in `markup`, ready to paste. Notes on what changed only when `explain_edits` is true, when a change alters meaning, or when the user asked why. A list of suggestions is what an editor gives a writer; the user asked for the writing.
7. **Never rewrite inside a quotation, a name, a number, a citation, or code.** Quoted speech, legal language, brand names, figures and identifiers are the writer's evidence. Flag a suspected error next to them; do not correct it on your own authority. This survives every other rule, including voice matching.
8. **Readability scores are triage, not targets.** Flesch Reading Ease = 206.835 − 1.015 × (words ÷ sentences) − 84.6 × (syllables ÷ words). Use it to find the one paragraph scoring far below the piece's own average, never to hit a number: the formula counts syllables, so accurate technical terms score as "hard" while vague, empty prose scores well.
9. **Rhythm is variance, not length.** Flag three or more consecutive sentences within ±3 words of each other — that flatness is what readers call "robotic". A single long sentence is only a problem when it carries more than one main clause plus two subordinate ones; `sentence_flag_words` (default 30) is the trigger to check, not the verdict.

## Format Specs

Conventional budgets and shapes. Where an outlet, employer, or platform publishes its own limit, that number wins — check it and record it in `~/Clawic/data/writing/style-sheets/<context>.md` (`style-guide.md`). Reading time = words ÷ 240 (silent prose reading runs roughly 200-300 wpm, Rayner); spoken delivery = words ÷ 140.

| Format | Budget | Shape | Opening | Done when |
|---|---|---|---|---|
| Email, internal | 50-150 words | Ask → context → next step | The ask, in the first two lines | One decision is requested and the deadline is a date |
| Email, cold | 75-125 words | Relevance → specific ask → easy out | Why this person, not why you | It can be answered with one word |
| Chat message | 1-3 sentences | Whole ask in one message | The ask | No "hi" as a standalone message |
| Blog post | 800-1,500 words | Hook → promise → 3-5 sections → payoff | A concrete scene, number, or claim | Every subhead states something, not a topic |
| Essay | 1,500-4,000 words | Question → attempts → turn → resolution | The tension, not the thesis | The turn is earned, not announced |
| Op-ed | 600-800 words | Claim in ¶1 → 3 arguments → call | The claim | The outlet's stated limit is met exactly |
| Newsletter issue | 400-1,200 words | One idea per issue + a standing furniture block | The idea, above the fold | It survives being read on a phone in 90 seconds |
| Memo | 1 page (~500 words) | BLUF: decision → why → what happens next | The decision or recommendation | A reader who stops after ¶1 acts correctly |
| Proposal | 2-10 pages | Problem → approach → scope → price → risk | The problem in their words | Scope names what is excluded |
| Exec summary | 150-300 words | Situation → complication → question → answer | The answer | It stands alone with the deck deleted |
| Status update | 100-200 words | Shipped → blocked → next → ask | The one thing that changed | A blocked item names who unblocks it |
| X post / thread | 280 chars per post | Hook post → one idea per post → close | The claim, no throat-clearing | Post 1 works alone |
| LinkedIn post | 100-250 words | Line 1 payload → short paragraphs → one ask | The payload before the "see more" fold | It reads with all formatting stripped |
| Bio | 25 / 50 / 100 words | Role → proof → hook | Role and current work | All three lengths exist and agree |
| Cover letter | 250-400 words | Why them → evidence → what you would do first | A specific fact about them | Nothing restates the résumé |
| Speech / script | words ÷ 140 = minutes | One idea per minute, signposted | A concrete image | Read aloud without stumbling twice |

## Sentence Diagnostics

The observable symptom names the repair. Depth, worked examples and the passive/nominalization rules: `clarity.md`.

| Symptom | Cause | Repair |
|---|---|---|
| Reader asks "so who does what?" | The subject slot holds an abstraction, not an actor | Put the character in the subject and the action in the verb |
| Sentence is 40 words and still vague | Nominalizations: the verbs became nouns (`make a decision`, `provide support`) | Turn each noun back into its verb; the sentence usually halves |
| Every sentence the same length | Flat rhythm, the loudest machine-written tell (Rule 9) | Break one long sentence in two, fuse two short ones; aim for a spread, not a mean |
| Paragraph read twice to follow it | New information in the topic position, old information in the stress position | Open with what the reader already knows, end on what is new (Gopen & Swan) |
| Feels hedged and weightless | Stacked qualifiers: `may potentially`, `it seems that`, `somewhat` | One hedge per claim, maximum; delete the rest or state the actual uncertainty |
| Same referent renamed three times | Elegant variation — the reader thinks a new thing was introduced | One thing, one name, every time |
| Transitions feel bolted on | The paragraphs are in the wrong order; `however` is patching a jump | Reorder, then delete the connective that is no longer needed (`structure.md`) |
| Strong draft, weak ending | It stops at the last argument instead of landing the consequence | End on the change in the reader, not on a summary |
| Anything else | Read it aloud; the place you stumble is the place to cut | — |

## Output Gates

Before delivering any draft or edit:

- Can I state this piece's one claim and its 3-5 moves in order — and does the draft follow that order (Rule 2)?
- Is the ask, decision, or payload inside the first screen, stated once (Rule 5)?
- Did I check the draft against `## Voice` and `## Never`, and is every word on the never-list absent?
- Does the sentence-length spread vary, with no three consecutive sentences within ±3 words (Rule 9)?
- Is it inside the format's budget after the cut, and inside the platform's hard limit where one exists?
- Is every quotation, name, number, citation and code block byte-identical to the source (Rule 7)?
- Am I returning the finished text in `markup`, not a list of suggestions (Rule 6)?
- Did anything durable come out of this — a confirmed voice trait, a rejection, a sample, a style decision, a reusable template, a finished piece? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/writing/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| voice_file | path | none | Long-form voice guide at `~/Clawic/data/writing/<file>`; read with `memory.md` and outranks observed traits when they conflict (`voice.md`) |
| spelling | us \| uk \| ca \| au \| in | us | Spelling, quotation-mark and date conventions in every draft and edit (`style-guide.md`) |
| edit_depth | light \| standard \| heavy | standard | How far an edit may go: `light` = mechanics and cuts only; `standard` = sentence rewrites within the existing structure; `heavy` = reordering and rewriting whole sections (`revision.md`) |
| cut_target_pct | number (0-40, %) | 20 | The reduction the cut pass aims for (Rule 3) and the figure quoted when reporting a trim |
| feedback_mode | rewrite \| inline \| letter | rewrite | Whether edits come back as the corrected text, as margin notes on their text, or as an editorial letter (`feedback.md`) |
| explain_edits | bool | false | Whether each non-trivial change ships with a one-line reason (Rule 6) |
| sentence_flag_words | number (words, 15-60) | 30 | Length at which `clarity.md` inspects a sentence for splitting (Rule 9) |
| markup | markdown \| plain \| html \| rich-notes | markdown | Format every delivered draft is written in, including whether headings and bold are used at all |
| default_register | text | none | Baseline formality when the format does not dictate one; unset means the format's convention in Format Specs decides |
| ai_tell_sweep | bool | true | Whether every generated draft is checked against the machine-written tells in `clarity.md` before delivery |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Conventions** — Oxford comma, em-dash vs parentheses, heading case, numerals vs words, contractions, emoji, ellipsis and exclamation tolerance — affects every draft and the style sheet for each context
- **Output register** — first vs second person, "we" vs "I", jargon tolerance per audience, humour, profanity — affects tone selection when `default_register` is unset
- **Work order** — outline approved before drafting or draft first and restructure after, how many variants to offer, whether to show the diff or the whole text — affects `drafting.md` and delivery shape
- **Channels** — where they actually publish (newsletter platform, blog, LinkedIn, X, internal wiki) and each one's real limits — affects Format Specs and `social.md`
- **Restrictions** — banned words and phrases, claims they may not make, compliance or legal review requirements, embargoes, topics off-limits under a byline — affects `## Never` and the Output Gates
- **Cadence** — publishing rhythm, recurring deadlines, review or approval cycles, voice re-check frequency — every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Languages** — which languages they write in and the register they use in each; dialect within a language (`spelling`) — affects `second-language.md`

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Editing while drafting | The critic and the generator compete for the same attention; the draft never reaches its end and the opening gets polished twenty times | Zero draft to the last line first, timeboxed, then edit (`drafting.md`) |
| Line-editing a piece whose order is wrong | Every polished sentence gets deleted in the restructure | Structure pass first, always (Rule 2) |
| Cutting adjectives to hit a word target | Recovers a marginal fraction and leaves the repeated sections that caused the bloat | Cut in the Rule 3 order: sections, restatements, clauses, adjectives |
| Copying catchphrases to imitate a voice | Reproduces the tics without the structure — the result reads as parody | Match the four fingerprint dimensions first (Rule 4, `voice.md`) |
| Asking "does this sound like you?" | Yes/no gives you no information to store and puts the work on them | Offer two variants that differ on one dimension; the pick is a data point worth writing down |
| Front-loading context before the ask | The reader skims to find what is wanted and misses the context they skipped | Ask first, context second (Rule 5) |
| Hunting passive voice everywhere | Passive is correct whenever the receiver of the action is the topic of the paragraph | Fix passives that hide the actor; keep the ones that hold the topic position |
| Adding a summary because the piece is unclear | Doubles the length and confirms the body failed | Fix the body; a summary is for length, not for confusion |
| Treating house style as grammar | "Oxford comma", "US vs UK", "sentence case" are preferences; calling them errors burns credibility on the real errors | Style sheet decides; flag as style, not as a mistake (`style-guide.md`) |
| Applying the user's stored voice to a ghostwritten piece | The byline belongs to someone else; their voice, not the user's | Voice is selected by byline and context, never by default (`voice.md`) |
| Proofing on screen, in the same view it was written | The eye completes what it expects; typos survive three passes | Change the medium: read aloud, or read the last paragraph first (`revision.md`) |
| Rewriting a quote to make it flow | Fabricates a source's words — unrecoverable if published | Cut inside a quote with an ellipsis, add with brackets, or paraphrase outside the marks (Rule 7) |
| A style decision that only lives in the chat | Re-litigated on every piece; consistency across a body of work is impossible | Style sheet artifact with the date and the reasoning (`style-guide.md`) |
| Sending it the moment it reads well | It reads well to the person who just wrote it | Gate the send on the Output Gates, not on the feeling |

## Where Experts Disagree

- **Outline first vs discovery draft.** Argument-driven pieces (memos, proposals, op-eds) fail without a fixed outline — the reader must be able to stop early. Exploratory pieces (essays, personal writing) are often thought that only happens on the page, and an outline pre-decides the conclusion. Frontier: does the piece exist to transmit a conclusion, or to reach one (`drafting.md`)?
- **Readability formulas.** Plain-language practice treats an average sentence around 20 words as a target; technical editors point out that syllable-counting formulas penalise the precise term and reward vagueness. Both are right about different corpora: use the score to find outliers within one document, never to compare two documents on different subjects (Rule 8).
- **Adverbs and qualifiers.** King's "the road to hell is paved with adverbs" is right about `-ly` intensifiers propping up weak verbs, and wrong about adverbs that carry the actual claim (`rarely`, `only`, `almost`). Delete the ones that could be replaced by a stronger verb; keep the ones that change the truth conditions.
- **Voice imitation limits.** One school says a good ghostwriter is undetectable; another says any voice reproduced without the person's judgement is a forgery that will eventually publish something they would not have said. Practical frontier: reproduce voice freely, but never generate a *claim, opinion or commitment* the person has not made (`voice.md`).
- **How much to cut.** Prose written to be read rewards maximum compression; prose written to be heard or skimmed needs redundancy, because the listener cannot re-read. Cut a memo to the bone; leave a speech its repetitions (`Format Specs`).

## Security & Privacy

**Local storage:** voice traits, style sheets, samples, templates and the log of finished pieces stay in `~/Clawic/data/writing/` on this machine, plus person rows in the shared `~/Clawic/data/contacts/` and project files in `~/Clawic/data/projects/`.

**This skill does NOT:** make network requests, publish anything anywhere, or store credentials for any publishing platform. Drafts and pasted text are stored only when the user asks for them to be kept, and secrets inside them are replaced by pointers before writing (`memory-template.md`).

**Guardrails:** clearing or overwriting stored voice, samples or style sheets requires explicit confirmation, and a stored preference is never deleted because a single draft contradicted it.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/writing (install if the user confirms):
- `grammar` — mechanical correction of spelling, agreement and punctuation without touching style
- `copywriting` — persuasion built to convert: offers, benefits, calls to action
- `storytelling` — narrative arc, scene and tension when the piece is a story
- `documentation` — technical docs, READMEs and API reference, where structure is dictated by the doc type
- `book-writing` — chapter architecture and voice consistency across a manuscript

## Feedback

- If useful, star it: https://clawic.com/skills/writing
- Latest version: https://clawic.com/skills/writing

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/writing.
