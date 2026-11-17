---
name: recallit
description: Build and drill spaced-repetition packs with recallit — turn a PDF, URL, repo, or plain concept into honest, source-grounded flashcards, then run the daily review loop. Use when the user wants to "make a deck/pack", "turn this into flashcards", "study X with recallit", or wants to drill/review a pack they already have. Fully keyless (no API keys needed); works entirely through the CLI.
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["recallit", "bun"] },
        "install":
          [
            {
              "id": "node-global",
              "kind": "node",
              "package": "@waits/recallit",
              "bins": ["recallit"],
              "label": "Install recallit (global node package @waits/recallit)",
            },
          ],
      },
  }
---

# recallit

recallit is a local, code-graded spaced-repetition engine. Everything below runs through the
`recallit` CLI — no browser required. That matters here: inside a container/remote OpenClaw
install the browser SPA (`recallit start`'s web UI) is usually **not reachable**, so this skill
is written entirely for the CLI/agent-loop path. It works with zero API keys — `ANTHROPIC_API_KEY`
is optional and only used by recallit's own *built-in* pack-authoring agent (`recallit pack
<source>`), which this skill does not depend on.

You do two things with this skill:
1. **Author a pack** — read a source, draft honest cards yourself, gate + install them.
2. **Drill a pack** — pull due cards, ask the user, let the *engine* grade the answer.

**If `openclaw skills info recallit` (or `skills check`) still shows this skill as "needs
setup," don't wait on OpenClaw to fix it — the install spec above is not auto-run for workspace
skills.** Verified directly: `openclaw onboard --non-interactive ...` completes its "skills
setup" step (`skipSkills: false`) without touching this skill's missing `bun`/`recallit`
binaries — that auto-install path is reserved for trusted bundled skills, not this one. You (the
agent) should just run the installers yourself via your shell tool:

```bash
brew install bun               # only needed if `bun` itself is missing
bun add -g @waits/recallit     # recallit is bun-only (imports bun:sqlite) — install with bun, not npm
```

On the Umbrel OpenClaw container specifically: verified its image (`node:22-trixie-slim`) ships
neither `bun` nor `recallit` by default, only node + brew + chromium, and `apt`/`apt-get` are
shimmed to fail and point at brew — so `brew install bun` is the right first command there, not
apt. Confirmed `~/.recallit` resolves to `/data/.recallit` in that container (`HOME=/data`),
which *is* the volume the image already persists across app updates — no extra data-dir
configuration needed.

## The grading contract (non-negotiable)

**You never grade the user's answer.** You ask the question, take the user's typed reply, and
hand it to the CLI:

```bash
recallit answer <cardId> "<user's exact answer>" --topic <id>
```

This calls the engine's `gradeResponse` function and prints the verdict, e.g.:

```
answer="Scale a new habit down so it takes less than two minutes to do" -> Good (matches after normalization)
next due 2026-07-09T00:00:00.000Z
```

Report exactly that rating and reason back to the user. Do not soften it, override it, or decide
yourself whether the answer was "close enough" — the CLI already decided.

`recallit answer` grades differently depending on how the card was authored (see "draft cards"
below) — the same command works for both, dispatch is automatic:

- **Flashcards** (no `meta.grader`) use lexical similarity against `back` verbatim — verified
  directly: a correct paraphrase ("make the new habit take under two minutes to start" for a card
  whose back was "Scale a new habit down so it takes less than two minutes to do") scored 0.48
  similarity and came back `Again`, below the pass threshold. Nudge the user toward the card's key
  wording for these — don't imply any correct-in-spirit answer will pass.
- **Checkable items** (`meta.grader: "coverage"` + `meta.rubric`) grade for *meaning*: an LLM
  examiner judges whether the answer demonstrates each required checkpoint, but code re-verifies
  the cited evidence is a literal substring of the *user's own answer* before it counts — the
  rating is still 100% code-decided, only the "did they get the idea" read is semantic. This path
  needs a model: `ANTHROPIC_API_KEY` (default), or any OpenAI-compatible endpoint via
  `RECALLIT_EXAMINER_URL` + `RECALLIT_EXAMINER_MODEL` (+ optional `RECALLIT_EXAMINER_KEY`) —
  e.g. a local Ollama: `RECALLIT_EXAMINER_URL=http://localhost:11434/v1
  RECALLIT_EXAMINER_MODEL=qwen2.5:1.5b`. With neither configured it gracefully degrades to a
  stricter keyword-ish floor over the same checkpoints (verified: no provider → no crash, just a
  stricter grade — never a thrown error either way). Honest caveat, verified against a real 1.5B
  local model: small models grade noticeably harsher than Claude on the same answer — the
  anti-fabrication check drops their sloppier evidence citations, which fails safe (under-credits,
  never over-credits).

## Why not `recallit daily` / `agent` / `talk` / `quickstart`

These commands exist and are documented in `recallit --help`, but they're built for a live
terminal: they block on a synchronous `prompt()` read and drive recallit's own internal
Claude-Agent-SDK session (spends `ANTHROPIC_API_KEY`). Run one from a non-interactive agent
tool-call (no real stdin) and it ends immediately with 0 turns reviewed — verified by running
`daily --help` and `agent --help` against the published CLI: both ignored `--help` entirely,
launched a real session, and terminated only because stdin read as empty. **Don't use them as
the drill loop in this skill.** Use `due` + `answer` instead (below) — no key required, and the
agent turn is *you*, in the chat you're already having with the user.

(Aside: none of the `--help` flags are actually implemented anywhere in the CLI — every
subcommand just treats `--help` as an ignored flag and runs for real. Don't run any recallit
command "just to see the help text"; read this skill or `recallit` with no arguments instead,
which does print real usage.)

## Mental model

A pack is plain files under `packs/<id>/`:

```
packs/<id>/
  manifest.json        # { schemaVersion:1, engine:">=0.1.0", id, name, modality, meta }
  cards.json            # all cards; the gate stamps meta.status:"needs-review" on flagged ones
  .author/source.txt    # the grounding corpus of record (raw extracted source text)
```

`cards.json` is the single source of truth. `recallit pack write` (no LLM — deterministic) stamps
`meta.status:"needs-review"` on any card whose quote isn't a literal substring of the source, and
`recallit topic add` installs only the ready cards, skipping needs-review automatically.

## Authoring a pack

### Step 0 — resolve the mode

- **Conversational (default).** Scope briefly, preview ~3 sample cards, let the user steer, confirm, install.
- **Ambient.** The user described intent in prose ("turn this into a deck of just the actionable stuff"). Parse source + filter from their words, echo back what you understood, then proceed as conversational.
- **One-shot.** The user said "just do it" / "no preview". Skip the preview; generate, gate, install ready cards, report. Still never auto-install needs-review or web-grounded cards without asking.

### Step 1 — ingest the source into `.author/source.txt`

Extract the source's text using whatever file-read / web-fetch tools you have available, and save
it verbatim into `packs/<id>/.author/source.txt` — the corpus every card must quote from. Pick
`<id>` as a kebab-case slug of the title.

| Source | How |
|---|---|
| PDF / local file | Read it directly; for a long document, read in page/section ranges. |
| URL / article | Fetch it for clean text. If a JS app / paywall returns nothing usable, say so. |
| Concept (no doc) | Search the concept + subtopics, fetch a few reputable results, write the evidence (quote + url per line) into `source.txt`. Set `meta.grounding: "web"` on the manifest. The concept name seeds queries — it is never card content. |
| Code repo | Clone (shallow) to a temp dir; use README / package manifest / exported types as the surface. |

**Precondition — do not skip:** if the corpus is empty or near-empty (image-only PDF, paywalled
page with nothing extracted), abort with a clear message. Never emit cards from an empty corpus.

### Step 2 — scaffold `manifest.json`

```json
{
  "schemaVersion": 1,
  "engine": ">=0.1.0",
  "id": "<slug>",
  "name": "<Human Title>",
  "modality": "text",
  "meta": { "source": { "kind": "pdf|url|repo|concept", "ref": "<path-or-url>" }, "grounding": "source" }
}
```

Use `"grounding": "web"` for concept packs.

### Step 3 — draft cards, grounded in the corpus

Walk the corpus front to back. For each fact/point worth remembering, decide which of two kinds
it is — this decision is what determines how it gets graded later, so make it deliberately, not
by default:

**(a) Flashcard — exactness is the point** (a term, a date, a definition, a quote, a formula,
vocabulary). Emit:

```json
{
  "type": "qa",
  "front": "What is the two-minute rule?",
  "back": "Scale a new habit down so it takes under two minutes to start.",
  "context": "optional surrounding sentence",
  "tags": ["habits"],
  "meta": { "sourceQuote": "<VERBATIM span copied from source.txt>", "locator": "p.162" }
}
```

This grades via lexical match against `back` (see "The grading contract" above) — the learner
needs to reproduce close to this wording. Right for anything where the wording *is* the answer;
wrong for "explain this in your own words" material, which the strict match will mark wrong even
when correct.

**(b) Checkable item — comprehension is the point** (explain why X, the argument's key points, a
mechanism, "what does this mean") — a single quote can't capture the whole answer. Emit:

```json
{
  "type": "explain",
  "front": "Why does the two-minute rule work?",
  "back": "It removes the activation-energy barrier to starting, so the habit forms before willpower is needed.",
  "meta": {
    "grader": "coverage",
    "rubric": [
      { "id": "barrier", "claim": "lowers the barrier to starting", "required": true, "sourceQuote": "<VERBATIM substring>" },
      { "id": "forms-first", "claim": "the habit forms before it requires willpower", "required": false, "sourceQuote": "<VERBATIM substring>" }
    ]
  }
}
```

This grades via `recallit answer`'s coverage/examiner path (a key present): the learner passes by
covering the *required* checkpoints in their own words — a correct paraphrase is Good, not Again.
Without a key, it degrades to a deterministic keyword-ish floor over the same checkpoints (still
never crashes, just stricter). `back` here is a concise exemplar for human review, not the
grading contract.

Honesty rules, strictly, for both kinds:
- Every `sourceQuote` (the flashcard's one, or each rubric checkpoint's) must be copied verbatim
  from `source.txt` — a literal substring. No quote, no card/checkpoint — the gate holds whatever
  isn't grounded (`quote-not-in-corpus` for (a), `rubric-point-not-in-corpus:<id>` for (b)).
- `back` (and each rubric `claim`) must be entailed by its quote, not outside knowledge.
- Don't introduce numbers or proper nouns in a flashcard's `back` that aren't in the quote/context
  (checkable items skip this check — `back` there is an exemplar, not the grounding contract).
- 2–5 checkpoints per checkable item is plenty; mark only the core points `required: true`.

Bias toward fewer, sharper items overall: an article → ~15–30; a chapter → ~10–20; mix both kinds
as the material actually warrants rather than defaulting to all-flashcard.

### Step 4 — preview & steer (conversational/ambient modes)

Draft ~3 sample cards from the first chunk, confirm each `sourceQuote` is a literal substring of
the source, show them, and offer to steer before spending effort on the whole source. Skip in
one-shot mode.

### Step 5 — write & gate (deterministic — don't hand-grade this either)

Write all drafted cards to `packs/<id>/cards.json` (a plain JSON array, no `status` field yet):

```bash
recallit pack write packs/<id>
# → "23/25 ready, 2 need review (grounding: source)" + each flagged front + reason
```

Reason codes: `quote-not-in-corpus`, `missing-source-quote`, `rubric-empty`,
`rubric-point-not-in-corpus:<id>`, `unverified-number`, `unverified-proper-noun`,
`duplicate-front`, `quality:*`. `recallit pack review packs/<id>` lists the flagged cards any
time, no LLM involved in either command.

### Step 6 — report

Tell the user honestly: `N ready, M need review`, the pack path, and the flagged fronts + reasons.

### Step 7 — install

Confirm first in conversational/ambient modes ("Install these N cards as topic '<id>'?"). For
`grounding:"web"` packs, always show the unverified note and require an explicit yes, even in
one-shot mode.

```bash
recallit topic add packs/<id>     # installs READY cards only — skips needs-review automatically
recallit stats --topic <id>       # totalCards, dueNow
```

## Drilling a pack (the daily loop)

This is the part that's different from the Claude Code version of this skill: instead of an
interactive terminal session, you run the loop yourself, one exchange at a time, in the chat.

1. List what's due:
   ```bash
   recallit due --topic <id> [--limit n]
   ```
2. For each due card, present the `front` to the user in chat and wait for their reply.
3. Grade it via the engine — never yourself:
   ```bash
   recallit answer <cardId> "<user's exact reply>" --topic <id>
   ```
   Report the rating (`Again|Hard|Good|Easy`) and reasons exactly as printed.
4. Repeat until the due list is empty or the user wants to stop.

If the user wants to self-rate instead of typing a free-text answer (Anki-style), use
`recallit review <cardId> <Again|Hard|Good|Easy> --topic <id>` — still just recording their own
call, not a judgment you make.

Useful alongside the loop:
```bash
recallit context --topic <id>     # the engine's weak-spot notes for this topic, if any
recallit preview <cardId>         # see a card's current schedule
recallit stats --topic <id>       # totalCards, dueNow
```

## Editing an existing pack

```bash
recallit pack edit <id> "<instruction>"     # e.g. "add 10 cards on chapter 5", "fix card 7"
```

Re-reads `cards.json` + `.author/source.txt`, applies the instruction, re-gates. Additive edits
(only new cards) merge and preserve FSRS review history; changed/removed cards force a rebuild
that resets the schedule and asks to confirm first (`--dry-run` to preview without installing).

Manual fallback: hand-edit `cards.json`, then `recallit pack write packs/<id>` to re-gate, then
`recallit topic add packs/<id> --force` (note: `--force` resets FSRS).

## Installing / sharing a pack someone else made

`recallit topic add <source>` also accepts a GitHub ref, a git URL, an npm spec, or a `.tgz` —
not just a local dir:

```bash
recallit topic add github:owner/repo[#ref]
recallit topic add git+<url>
recallit topic add npm:<spec>
recallit pack share <id>     # print the install string + browse URL for a repo-local pack
```

## Honest about the guarantee

The substring gate verifies the quote is **present** in the source, not that `back` faithfully
**interprets** it. Flag cards whose answer adds numbers/proper-nouns not in the quote. Say "every
card cites a verbatim line from the source you can check" — not "every card is verified true."
