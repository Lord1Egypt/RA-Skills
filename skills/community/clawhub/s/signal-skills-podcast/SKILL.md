---
name: podcast
description: Pull podcast transcripts on demand and mine them for ideas, trends, and mechanics — without dumping raw transcript into context. Use when the user shares a podcast/episode URL, names a show, or asks what's worth taking from an episode/series. Handles Apple Podcasts, YouTube, RSS feeds, and show names; a Spotify link needs the show's name.
metadata:
  openclaw:
    homepage: https://github.com/OrenSegal/signal-skills
    requires:
      bins: [python3]
---

**Paths.** `SKILL_DIR` in the commands below is the folder that holds this file and its scripts. On Claude Code it is `${CLAUDE_SKILL_DIR}`. If that still reads as a variable name, your host does not fill it in: use the folder this file was loaded from (for Codex, `~/.agents/skills/podcast`). Put the real path in place of `SKILL_DIR` when you run a command.

Turn podcasts into extracted findings. The whole point is that raw
transcript NEVER enters main context — subagents eat the noise, you keep
the signal.

## Why this exists

A 60-minute episode is ~10k words and roughly 70% filler: banter, sponsor
reads, audience-hyping, restating the last point. Reading it directly
burns context and buries the 3 specifics that mattered. Summarizing it
flattens exactly the weird concrete detail that WAS the idea.

Extract, don't summarize.

## What are you mining for?

This skill isn't hardwired to one lens (e.g. customer/monetization
validation) — that's one possible focus among several (technical patterns,
design/craft inspiration, a specific research question, general "what's
worth knowing here").

**Priority order for picking the lens:**
1. **The user stated one this run** ("mine this for X") — use it, exactly.
2. **Not stated** → don't default to a blank, filter-free summary either.
   Default to relevance to the current project you're running in (its
   CLAUDE.md, its current roadmap/open questions, whatever you already know
   about what the user is building) crossed with the podcast's own actual
   subject matter. A dev-workflow episode mined from inside a codebase repo
   defaults to "what does this change about how we build here," not to
   generic self-help takeaways.
3. **Genuinely no project context available** (a bare Claude Code session
   with no repo) → then ask, or fall back to general signal (mechanics,
   claims, predictions, no relevance filter) and say that's what you did.

Whichever lens applies, it changes what counts as fluff vs. payload in
Step 3 and how Step 4 frames relevance — decide it before fanning out
extractors, not after.

## Your source list

`sources.md` (next to this file) is the user's own hand-maintained list of shows
worth mining. It ships empty and is not an exhaustive directory: it holds
shows that either scored well on a past mining run or fill a specific
gap (a different angle on a claim already in the ledger, so cross-show dedup
has something to check against). When the user asks "what else should I
mine" or "find me more sources like X," read `sources.md` first instead of
guessing from scratch — it already has each show's angle and why it's there.
Update it (don't just answer in chat) whenever a mining run or a
conversation surfaces a new worthwhile show, so the list compounds instead
of resetting every session.

## Step 0 — Check the ledger before doing anything

`ledger.py` (next to this file) tracks state across runs so re-mining a show
doesn't repeat work: which episodes are already extracted, what predictions
are still open, and cross-show overlap.

```bash
python3 SKILL_DIR/ledger.py mined --show "<show name>"
```

Cross-reference this against the episode list `resolve.py` returns (Step 1)
and only fan out extractors (Step 3) on episodes NOT already in this list.
If every candidate episode is already mined, say so and skip straight to
Step 3.5 (prediction check) and Step 5 (report) — don't re-extract.

### Corpus questions skip extraction entirely

If the user is asking what the corpus already knows ("what have my mined
shows said about pricing", "who's actually been right about agent tooling")
rather than asking you to mine a URL, answer straight from the ledger and
stop — no `resolve.py`, no transcripts, no extractor fan-out:

```bash
python3 SKILL_DIR/ledger.py query --topic "<topic>" [--show "<show>"] [--since 2026-01-01] [--tag measured]
python3 SKILL_DIR/ledger.py scoreboard [--by-guest]
```

`query` searches every finding ever recorded (Step 3 stores them, not just
predictions). `scoreboard` gives confirmed/(confirmed+failed) hit rate per
show, or per speaker with `--by-guest` once findings carry a `speaker` field.
This path costs a few hundred tokens instead of the full mining pipeline —
always check whether the question is answerable this way before doing
anything else.

### Watched shows ("check subscriptions")

```bash
python3 SKILL_DIR/ledger.py subscribe --show "<url-or-show-name>"
python3 SKILL_DIR/ledger.py subscriptions
python3 SKILL_DIR/ledger.py unsubscribe --show "<url-or-show-name>"
```

When the user says "watch this show" or "check my subscriptions": for each
subscribed source, run `resolve.py` (Step 1), diff against `mined` (this
step) to find only-new episodes, mine those (Steps 2-4), and end with one
combined report (Step 5) across all subscriptions plus a prediction-check
pass (Step 3.5) against every show's open predictions, not just the newly
mined one — a new episode on show A can resolve a prediction made on show
B. This is also what a scheduled run should invoke (see Hygiene) so digests
show up on a cadence instead of only on request.

## Step 1 — Resolve source → feed → transcripts

`resolve.py` (next to this file) does the whole first mile for ANY show.
Don't hand-roll curl pipelines; don't hardcode a feed.

```bash
python3 SKILL_DIR/resolve.py "<url-or-show-name>" --limit 12 --download tx/
```

If it prints that a proxy is set but not used and fetches fail to resolve
hosts, the machine has no direct route out: add `--use-proxy`.

Accepts an Apple URL, a direct RSS URL, a bare show name, a YouTube URL,
or a Spotify URL together with `--name "<show name>"`. Prints the feed, marks the `?i=` target episode, lists
which episodes have transcripts, and with `--download` writes flattened
`.txt` plus a `manifest.json` (title, date, path, words, target).

What it encodes, so you don't rediscover it:
- **Apple pages 500 on fetch. Never fetch them.** Only the `id<N>` in the
  URL matters → `itunes.apple.com/lookup?id=<N>&entity=podcast` → feedUrl.
- **The `?i=<EPISODE_ID>` DOES resolve** — but only via the *show* lookup
  with `entity=podcastEpisode&limit=200`, matching on `trackId`. Looking
  up the episode id directly returns `resultCount:0`. This is the trap.
- Spotify has no open API, so a Spotify link alone exits with a message.
  Ask the user for the show's name and pass `--name`; the name is searched
  on iTunes and the first hit is used, so check the `show:` line it prints.
- Some shows (Apple-exclusive) expose no `feedUrl`. Say so, don't guess.

**YouTube gets its own path in `resolve.py`** — it isn't RSS, so it
doesn't share the feed machinery above:
- `youtube.com/watch?v=...` or `youtu.be/...` → single video, treated as
  one episode.
- `youtube.com/@handle`, `/channel/UC...`, `/playlist?list=...` → resolved
  via `yt-dlp --flat-playlist`, capped at `--limit` videos, newest first.
- Requires `yt-dlp` on PATH (`brew install yt-dlp`). No API key needed.
- Transcript source is auto-captions (`--write-auto-sub`, falls back to
  `--write-sub` if manual captions exist), pulled per-video directly by
  `resolve.py` — there is no separate Step 2 fallback needed for YouTube,
  it's already the primary path. A video with captions disabled or too
  fresh for auto-captions to have generated yet downloads nothing for
  that entry and is reported as a failure, not silently skipped.
- No published date beyond `upload_date` (YYYYMMDD from yt-dlp) — good
  enough for staleness checks, not a real RSS pubDate.

## Step 2 — Transcription fallback (only if the feed has no transcript tags)

Fallback order when `resolve.py` prints no `podcast:transcript` tags:
1. Show's own site — google `"<episode title>" transcript`
2. `yt-dlp --write-auto-sub --skip-download --sub-lang en --sub-format vtt "<yt-url>"`
3. Actual transcription (Whisper local, or a cloud ASR API) — only once 1-2
   are exhausted. Hosts like Flightcast and Transistor embed official
   machine transcripts; 12 episodes can be free and instant instead of an
   hour of local compute.

Before step 3, check the remembered preference:

```bash
python3 SKILL_DIR/ledger.py config-get transcription_method
```

- If it returns `local` or `cloud`, use that method silently — don't re-ask.
- If empty, ask the user with `AskUserQuestion`: local Whisper (free, slower,
  private, `uv run --with openai-whisper whisper ep.mp3 --model small
  --output_format txt`) vs. a cloud ASR API (paid, fast, needs an API key in
  env — gate on the key actually being present, borrowed from OpenClaw's
  `requires.env` dependency-gating idea: don't offer cloud as a real option
  if no ASR key is set). Offer a "remember this choice" option on each; if
  chosen, persist it with `ledger.py config-set transcription_method
  local|cloud` so future runs skip the question.

## Step 3 — Fan out extractors

Batch by word count, not by a fixed episode count: read `words` per episode
from Step 1's `manifest.json` and group episodes into subagents so each
agent's combined transcript stays around ~25k words. A handful of short
episodes can share one agent; a 3-hour outlier gets its own. This is cheaper
and more even than a flat "1-2 episodes per agent" rule when show lengths
vary widely.

Extraction is mechanical (reading a transcript and shaping findings, no
judgment calls that need the main session's model) — run extractor
subagents on a cheaper/faster model (e.g. Haiku) at low reasoning effort.
Reserve the session's actual model for Step 4 synthesis, Step 3.5's
contradiction-spotting, and any web cross-check verdicts (Step 3.7), where
judgment actually matters. This is the single biggest cost lever in the
whole pipeline — don't skip it because "it's just Python subagents," it's
model selection on the `agent()`/Task call itself.

Each extractor reads its transcript IN FULL and returns structured findings
only. Never read the transcript yourself.

The extraction prompt must demand SHAPES, not a summary:

1. **What it actually is** — vs. what the clickbait title promised. The
   gap between these two is itself a signal about the show.
2. **Concrete mechanics** — named workflows, prompt patterns, configs,
   step order, exact numbers. Anything reproducible. Be greedy here; this
   is the payload.
3. **Claims with numbers** — each tagged `[measured]` / `[anecdotal]` /
   `[speculative]` based on how the speaker sourced it. This tag does
   most of the fluff-cutting work.
4. **Tools named** — and crucially: actually used, or just name-dropped?
5. **Pain points / "I wish X existed"** — the idea seeds.
6. **Falsifiable predictions** — checkable later, which makes the show
   scoreable over time.
7. **Fluff ratio** — % substance, and what the filler was.

Rules for every extractor:
- Quote at most one short sentence where phrasing is load-bearing.
  Paraphrase otherwise. Never reproduce long passages — it's someone
  else's copyrighted work.
- Empty section → say "none". Never manufacture content.
- Unsourced hype goes in FLUFF, not CLAIMS.

**Also require a structured block**, so the corpus stays machine-queryable
across shows and runs (this is what feeds Step 3.5's dedup and the
ledger). Ask each extractor to close its response with a fenced JSON block:

```json
{
  "episode": "<title>",
  "show": "<show name>",
  "date": "<published date>",
  "findings": [
    {"claim": "...", "tag": "measured|anecdotal|speculative", "topic": "...", "speaker": "<optional>"}
  ],
  "predictions": [
    {"text": "<falsifiable prediction text>", "speaker": "<optional>"},
    "<or a plain string when unattributed>"
  ]
}
```

`topic` is a short free-text tag (e.g. "onboarding", "pricing", "agent
loops") — it's what makes cross-show topic overlap in Step 3.5 findable
instead of requiring manual eyeballing.

After each extractor returns, record it — pass the findings themselves
(`--findings-json`), not just the file path, so `query`/`scoreboard` (Step 0)
can search the corpus without re-reading anything off disk. When a finding
or prediction can be attributed to a specific guest/host, pass `speaker` on
the prediction object (plain strings still work when it can't be):

```bash
python3 SKILL_DIR/ledger.py record --show "<show name>" \
  --episode "<title>" --date "<date>" --findings-path "<path to saved findings>" \
  --findings-json '[{"claim": "...", "tag": "measured", "topic": "..."}]' \
  --predictions-json '[{"text": "<prediction 1>", "speaker": "<guest name>"}, "<prediction 2, unattributed>"]'
```

## Step 3.5 — Check old predictions, surface cross-show overlap

Before synthesizing, pull what earlier mining runs (on this show or others)
already put on record:

```bash
python3 SKILL_DIR/ledger.py predictions --show "<show name>"
python3 SKILL_DIR/ledger.py dedup --threshold 0.5
```

- **Predictions**: for each open prediction, check whether anything in the
  freshly-mined episodes confirms, refutes, or is now stale (a
  tool/model/pricing prediction older than ~8 weeks is presumptively stale —
  say so rather than silently carrying it forward). Resolve it:
  `ledger.py check-prediction --show "<show>" --episode "<title>" --text "<substring>" --status confirmed|failed|stale`.
  Before doing this by hand across every show, run
  `ledger.py stale-sweep --weeks 8` to batch-flag the obvious rot in one
  pass (`--dry-run` first to see the candidate list; without it, it writes).
- **Dedup**: `ledger.py dedup` does token-overlap matching across every
  show's recorded predictions/claims — it's a candidate list to check by
  hand, not a verdict (no embeddings, deliberately dependency-free). High
  scores between two different shows are exactly the "repetition across
  independent sources = signal" and "contradiction = most valuable finding"
  moments Step 4 cares about — go find them explicitly instead of relying on
  memory of past mining sessions.

## Trust mechanics, distrust ratings

Measured 2026-07-16 by running two independent extractions over the same
12 transcripts with the same prompt:

- **Mechanics matched almost perfectly** across runs — step orders, tool
  names, numbers, prompt structures. Extraction of concrete detail is
  reliable.
- **Judgments diverged wildly.** One episode scored 35% substance in one
  pass and 70% in the other. Fluff ratio is a vibe, not a measurement.

So: report mechanics as findings. Report fluff ratios as rough
orientation only, never as data, and never build a "signal quality"
ranking that the user might mistake for measurement. If a rating actually
matters to a decision, extract twice and compare.

Corollary: extractors reliably catch what a *single* pass misses about
evidence quality. The highest-value thing a second pass found was that an
impressive-looking dashboard predated the system being credited for it.
Ask explicitly: *does the evidence shown actually postdate the thing it's
offered as proof of?*

## Step 3.7 — Cross-check the load-bearing claims against the open web

Optional, and deliberately narrow so it can't balloon cost. Claude Code has
`WebSearch` natively; harnesses without an equivalent skip this step (say so
rather than failing — see `AGENTS.md`).

Eligible claims, ranked, top ~5 only:
1. Open predictions old enough to plausibly have resolved —
   `ledger.py grade-candidates --min-weeks 2 --limit 10` returns exactly
   this worklist (oldest first, already excluding anything too fresh to
   check), so don't hand-scan every open prediction; work off this list.
2. `[measured]`-tagged findings that are actually load-bearing to the
   user's lens (Step 4 filters against the same lens — decide this here,
   not after).

Never spend a web check on `[anecdotal]`/`[speculative]` findings or fluff.
Skip anything that already has a `source_url` recorded from a prior check.

For each eligible claim, one subagent, one WebSearch pass: "find independent
evidence confirming or refuting: `<claim, dated, source show/episode>`."
Subagent returns a verdict (confirmed / refuted / no independent evidence
found) plus the URL it used. Feed that straight back into the ledger so the
scoreboard carries real evidence, not vibes:

```bash
python3 SKILL_DIR/ledger.py check-prediction --show "<show>" \
  --episode "<title>" --text "<substring>" --status confirmed|failed \
  --source-url "<url the web check used>"
```

Findings (not predictions) that get web-corroborated or web-contradicted
don't have a ledger slot for the verdict yet — carry the tag inline into
Step 5's confidence tags as `web-corroborated` / `web-contradicted` instead.
A `web-contradicted` finding is the single highest-value thing this skill
can surface — it belongs at the top of Step 4's contradictions, not buried.

## Step 4 — Synthesize across episodes

One episode is one opinion. The trend only exists across episodes.

- **Repetition across independent episodes** = signal. Same claim from
  different guests, different weeks → real.
- **Contradictions** = the most valuable output. Where does ep 3 refute
  ep 9? Where did a prediction already fail? (Step 3.5's dedup pass and
  prediction ledger are what make this mechanical instead of eyeballed.)
- **Decay check** — model/tool episodes rot in weeks. Date-stamp
  everything and mark what's already stale.
- **Filter against whatever lens the user gave you** (see "What are you
  mining for?" above). "What's trending" is generic slop regardless of
  lens. "What does this confirm, contradict, or add to the specific thing
  the user is actually working on" is the useful question, whatever that
  thing is this run — it isn't always one product, and it isn't always
  customer/monetization relevance.

## Step 4.5 — Cross-check against your own analytics (optional)

If any synthesized finding is the kind of claim your own product data
could confirm or refute (a funnel rate, an event frequency, a retention
number), see `analytics-check.md` (next to this file) before writing the
report. It's backend-agnostic by design (PostHog, Amplitude, Mixpanel,
GA4, detected at runtime, gated on credentials actually being present) and
upgrades a claim from anecdotal to verified/contradicted-against-your-data
— the single highest-value thing this skill can do that a generic
research summary can't: tell you a guest's advice is wrong for *your*
users specifically, not just unmeasured in general. Skip it entirely if
no backend is configured; don't fabricate a comparison.

## Step 5 — Report (in-house, no external skill dependency)

Chat text or a raw markdown dump doesn't hold up as something to reopen or
share later. This skill owns its report rendering: `template.html` and
`render_report.py` (both next to this file, symlinked from the
`signal-report` skill so the two never drift, but invoked directly here —
no skill-to-skill call at runtime).

**Don't hand-write the report HTML.** Build a JSON payload (see
`render_report.py`'s docstring for the exact schema: title, eyebrow,
headline, query, tiers[].items[]) and run:

```bash
python3 SKILL_DIR/render_report.py payload.json out.html
```

then publish `out.html` with the `Artifact` tool on Claude Code. On any
other harness (no `Artifact` tool available), run the same script with
`--open` instead to preview it in the local default browser, or just
report the output path — see `AGENTS.md` next to this file for the full
non-Claude fallback path.

If the user wants something they can paste into a prompt, ticket, or chat
message instead of (or alongside) the Artifact, add a `.md` output target
in the same invocation — same payload, same validation, picked by file
extension:

```bash
python3 SKILL_DIR/render_report.py payload.json out.html out.md
```

The script owns all the
boilerplate and the hard style rules mechanically, so you only decide
content:

- every finding in scope for the user's query goes in the payload (not a
  curated top-N — rank by priority, don't cut). A genuine volume problem
  (50+ findings) gets called out explicitly with a link to the full data,
  never a silent truncation.
- findings grouped into priority tiers, each with a short label explaining
  what the tier means (e.g. "Ship before the deadline", "Already
  validated", "Open decision", "Worth a test", "Skip this source"). Every
  tier with at least one item belongs in the payload; the script refuses
  to render a tier with zero items rather than silently rendering it
  empty, so don't include one you're not populating.
- within a tier: order items by confidence (confirmed-twice above measured
  above anecdotal above unresolved), not by source or chronology.
  `web-corroborated`/`web-contradicted` (Step 3.7, if it ran) rank above
  plain `measured` — independent external confirmation beats a single
  transcript's say-so.
- reasoning inline with each finding via the `reasoning` field, never a
  separate section: what it claims, why it matters here, and the evidence
  (source, episode/date, confidence tag) together.
- fold in the ledger's open predictions (Step 3.5) and dedup output as
  their own items/tier, so contradictions/overlaps land in the ranking
  instead of a separate ignored section.
- episode + date per finding, always, in each item's `source` field.

What the script enforces for you:
- **No em dashes anywhere in the copy** — `render_report.py` scans every
  text field and refuses to render (with the exact field named) if it
  finds one. You'll get a hard error, not a missed review pass.
- **Confidence is visible, not just implied** — `tag`/`tag_class` are
  required per item, so there's no path to omitting the tag.
- **Theme tokens can't be corrupted** — the script only ever substitutes
  the title into the CSS head; it never touches the `:root` /
  `:root[data-theme]` / media-query blocks. A dark/light token inversion
  cannot happen through this path.

What still needs a real decision (the script can't do this for you):
- **Palette grounding.** `template.html`'s default (dark panel, sans
  display, monospace data, signal-strength bars) is one worked example,
  not a mandatory look. If the show/episode's subject calls for something
  else, edit the CSS variables directly before running the script for that
  mining run, rather than defaulting to warm-cream+serif+terracotta (the
  AI-cliché default).
- Load `artifact-design` before publishing — still required by the
  `Artifact` tool itself.

## Step 6 — Publish the scoreboard (optional, zero extra tokens)

The per-episode report above is the private, working-session output. The
scoreboard is a different, public-facing report: every show (or guest, with
`--by-guest`) ranked by confirmed prediction hit rate, built entirely from
data Step 3/3.5/3.7 already recorded — no new mining, no new LLM calls, just
reformatting the ledger:

```bash
python3 SKILL_DIR/scoreboard_report.py out.html out.md
python3 SKILL_DIR/scoreboard_report.py --by-guest --min-tested 2 out.html
```

Reuses `render_report.py`/`template.html` (hit-rate bands as tiers instead
of topic tiers), so it inherits the same filter toolbar, theme rules, and
em-dash guard for free. It errors out plainly if nothing has been graded
yet (`ledger.py check-prediction` never ran) rather than publishing an
empty "too early to grade" wall — run Step 3.7 against
`grade-candidates` first if that happens.

This is the one report in this skill worth publishing even when no one
asked for it: "who's actually been right" is inherently shareable in a way
a private findings digest isn't, and it costs nothing incremental to
produce since the grading work already happened as a side effect of normal
mining. Treat it as a standing, low-effort distribution loop — refresh and
republish it after every `check-prediction`/`grade-candidates` pass, not
as a one-off.

## What runs on-device vs. what needs Claude

Don't spend tokens on anything a script can already do deterministically.
The dividing line, mapped onto the steps above:

**On-device, zero tokens (scripts, CLI tools, local compute):**
- Step 0 — ledger lookups (`ledger.py mined/predictions/dedup`), all local
  JSON reads/token-overlap matching, no LLM involved.
- Step 1 — `resolve.py` (feed resolution, RSS parsing, `yt-dlp` metadata),
  and transcript **download** wherever the feed/host already publishes one.
- Step 2 — actual **transcription** when it's needed: local Whisper
  (`whisper ep.mp3 --model small`) runs entirely on-device, no API call, no
  token cost. Prefer it over cloud ASR by default; cloud ASR is the one
  paid fallback in this whole pipeline and only kicks in if the user opted
  into it (Step 2's remembered `transcription_method` preference).
- Recording ledger state after each extractor (`ledger.py record`,
  `check-prediction`) — plain file writes.

**Requires Claude (this is where tokens actually go):**
- Step 3 — the extraction itself. Turning a full transcript into shaped
  findings (mechanics, tagged claims, predictions, fluff ratio) is
  language understanding, not pattern matching — this is the one
  irreducible token cost in the whole pipeline, and it's also the entire
  point of the skill (distillation, not just fetching).
- Step 3.5 — judging whether fresh findings confirm/refute/stale-out an
  open prediction; dedup's token-overlap output is a mechanical candidate
  list, but deciding whether two candidates are actually the same claim
  needs judgment.
- Step 4 — cross-episode synthesis (repetition-as-signal, contradictions,
  decay, lens filtering).
- Step 5 — the report copy itself (headline, tier labels, reasoning
  prose). The HTML shell is static and reusable; the words in it aren't.

Rule of thumb: if a step is "fetch, parse, store, or pattern-match", push
it into `resolve.py` / `ledger.py` rather than doing it inline as a
subagent turn. If a step requires reading prose and deciding what it means,
that's the token spend this skill exists to justify.

## Hygiene

- Transcripts go to the scratchpad, NEVER the repo. Someone else's words,
  and they bloat git.
- Keep a manifest (`title`, `date`, `path`, `words`) so the synthesis
  stage can cite which episode a finding came from.
- 12 episodes ≈ 80k words ≈ free via RSS. Whisper on 12 episodes is ~1hr
  of compute. Always check step 2's fallback ladder before reaching for
  Whisper/cloud ASR.
- State lives in `~/.signal-skills/podcast/config.json` (preferences +
  `subscriptions`) and `~/.signal-skills/podcast/state/<show-slug>.json`
  (per-show ledger: mined episodes, findings, predictions). Both are plain
  JSON, inspectable/editable by hand if the ledger ever needs correcting.
- To run "check subscriptions" on a cadence instead of only on request, use
  the `schedule` skill to create a weekly cron-scheduled agent that invokes
  this skill with that instruction. The manual path keeps working either
  way — scheduling is opt-in setup, not a requirement.

## What's deliberately NOT borrowed from prior art

Researched 2026-07-16 against OpenClaw's AgentSkills spec and several
existing Claude Code podcast skills before building the above:

- **OpenClaw's skill format has no memory/state, hooks, or structured
  output of its own** — it's YAML frontmatter + a markdown body, full stop.
  The ledger/predictions/dedup/structured-output machinery above has
  nothing to inherit from that spec; it's bespoke to this skill. The one
  idea worth taking was `requires.env`-style dependency gating, folded into
  Step 2's cloud-ASR check.
- Consumer summarizers (BibiGPT, Podwise) lean on mind-maps/flashcards —
  skipped deliberately: that's re-summarizing, which is the exact failure
  mode this skill exists to avoid.
- VERIDIVE's "DeepWatch" continuous topic-monitoring is the closest
  existing analogue to Step 3.5's dedup/prediction-tracking. This skill's
  version stayed a manual-trigger, dependency-free, token-overlap pass
  through 2026-07-16 — right-sized for a skill invoked on demand, not a
  running service. Subscriptions + scheduled "check subscriptions" runs
  (added since, see Step 0 and Hygiene) close some of that gap, but the
  underlying dedup/prediction logic is still the same token-overlap pass,
  just invoked on a cadence instead of only on request — not a rebuild into
  a standing watcher service.
