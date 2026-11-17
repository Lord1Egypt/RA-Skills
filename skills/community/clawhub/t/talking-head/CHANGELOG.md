# Changelog

All notable changes to the **talking-head** skill. Versioning follows SemVer.

## 2.0.0 — every real-run command carries `--approved`, and the core refuses without it

**Breaking, and the break is upstream.** `ofox-video-core` 2.0.0 makes its
four billable subcommands — `generate`, `create`, `batch`, `chain` — refuse to
run unless `--approved` is on the command line. This skill's one real-run
`generate` command now passes it. The `--dry-run` commands are untouched: a
quote is how the number being approved gets produced, so gating it would close
the only route through itself.

**What a caller has to do differently**

- **Install `ofox-video-core` 2.0.0 or newer.** This version of this skill
  needs it. On an older core the updated commands stop with `unknown option
  '--approved'` before any request — nothing is submitted and nothing is
  billed, so the failure is safe, but every real run fails.
- **A command copied from an older version of this file is now refused.**
  Anything pasted from an earlier revision, a transcript or a wrapper script
  hits the guard, prints the quote-first steps and exits non-zero. Nothing is
  submitted and nothing is billed. Re-run it with `--dry-run` to get the
  quote, or with `--approved` once the cost table has gone in front of the
  user.
- **The `batch` route needs it too.** This file shows only `batch --dry-run`;
  its real run takes `--approved` in the same place.

**What `--approved` is not.** It does not prove that an approval happened — an
agent can type it without showing anyone a price, exactly as it could
previously just run the command. What changed is that spending without quoting
is no longer the default: it now has to be written into the command, where a
transcript shows it and a reviewer can object. The gate in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md)
is still the rule, and this skill still states it in full.

**Documentation only otherwise. No price, default, prompt template, flag
meaning or generation behaviour changed.**

## 1.1.1 — the recovery command asked for the whole repo, and asked the agent to run it

**Documentation only. No flag, price, prompt template or generation behaviour
changed.**

"If the script isn't found" ended in a skills.sh command that installed *every*
skill in this repo, into *every* agent, user-level, with confirmation
suppressed — four widenings past the one skill that was actually missing.
ClawHub's scanner flags exactly that (rule T08, "unpinned and overbroad
third-party installation via npx"), and the flag is accurate rather than noise:
an agent that read the line and ran it would have rewritten the user's whole
skills setup to recover one relative path.

The line now asks for the missing skill and nothing else —
`npx skills add ofoxai/skills --skill ofox-video-core`, which asks for that one
skill and answers none of the agent, scope or confirmation questions on the
user's behalf. The repo's own `npx ofox-skills ofox-video-core` still answers
all three (every agent, user-level, no prompts), which is why the line handed
to the user is the skills.sh one.

**What a caller has to do**: nothing changes for any command this skill
already prints, and nothing changes while `ofox-video-core` is installed. What
changes is conduct on the one path where it genuinely is absent — **relay the
command and let the user run it**; do not run an installer yourself. An
install writes outside the working directory, and that is not a decision to
take silently for someone.

All three distribution routes are still named (this repo's own
`npx ofox-skills`, skills.sh, and LobeHub or ClawHub), because recovery advice
that names one installer is wrong advice on every other channel this skill
ships through.

## 1.1.0 — the three unmeasured claims are measured; ten hedges become one paragraph

1.0.0 shipped with an unusual amount of hedging, because it had to: this was
the only skill here whose default model had never generated a spoken word in
this repo, and every number it planned against came from
`bytedance/seedance-2.5` — the one model its own route could not use. That
caveat was repeated in about ten places.

**It now has a paid run of its own.** Job
`855833b4-0819-4bd5-bc8c-397db009069a`, 2026-09-16,
`alibaba/wan-3.0-prime`, 10 seconds at 480p, seed `368003184`, 64 cents, 29
words of scripted dialogue built from this file's own template — and read
afterwards rather than declared done at `STATUS completed`.

| Question | Result |
|---|---|
| **Speech rate** | **3.16 words a second** — 29 words across a 9.17s speech span (`silencedetect` -30dB/0.35s: speech 0.46s→9.63s, two internal pauses totalling 0.76s, voiced-only rate 3.45 w/s) |
| **Truncation** | none — a `whisper tiny.en` transcription returns all 29 words in order with nothing added; only punctuation differs |
| **Lip-sync, gross** | confirmed — mouth open mid-word at 2.5s with the audio voiced; lips closed at 9.8s in the trailing silence, which is the closing beat the template asks for |
| **Lip-sync, per phoneme** | **still unmeasured**, and frames cannot measure it. Left open |
| **Face lock** | held for the full 10s — face structure, eyes, earring, hair parting, black top, gold necklace, grey background all match the input portrait |

So the **3 words a second budget holds on the model this skill actually
uses**, and is slightly conservative. The ten disclaimers that said the figure
came from seedance are gone; in their place is one paragraph in "A
thirty-second clip holds about ninety words" stating the measured rate, and
one bounded list in "What is measured, and what is not". A measurement does
not get argued with ten times.

**The bounds are stated once and properly, because one run is one run:** one
prompt, English only, 480p, 10 seconds — and ⚠️ **the upstream is unknown.**
`alibaba/wan-3.0-prime` is not upstream-pinned, Ofox routes by weight across
`alicloud` and `aliyun`, and the sidecar does not record a provider (checked:
its top-level keys are `created_at`, `job_id`, `model`, `name`, `prompt`,
`request`, `status`, `updated_at`, `video_cost`, `video_file`,
`video_seconds`). This is one observation on wan-3.0-prime, not a statement
about both upstreams, and the gap in what the script records is named rather
than glossed — a job's upstream cannot be recovered after the fact.

Bounded rather than deleted, too: identity held **within** one clip, so
whether two jobs from the same portrait match **each other** is still untested
and "Splitting a long script" still says so.

**`--real-person true` is no longer described as untested — and it is
deliberately not described as a workaround.** It lifts seedance-2.5's
real-person refusal (measured 2026-09-16; the shared write-up lives in
`ofox-video-core`'s `api-params.md` and is linked rather than restated here).
Ofox's own words are "privacy-preserving preprocessing for **authorized**
real-person references", so every mention in this file frames it as **an
assertion that the user holds the rights to the likeness** — offered only
after consent is settled, never as a retry after `input_moderation_failed`,
never set on a user's behalf, never for a public figure. The failure-mode row
that used to read "do not reach for it, it is untested" now reads "do not
reach for it as the fix", which is the durable version of that instruction.

**The default model stays `alibaba/wan-3.0-prime`, and the question is
recorded as open.** seedance-2.5 plus the flag is now a genuine alternative
route where before it was closed — but the A/B behind it was 4 seconds at
480p with no dialogue, and it says nothing about which model speaks a script
better, holds a face better, or costs less per usable clip. A new section, "An
open question this file does not settle: the default model", names what would
close it: the same portrait and the same script as job `855833b4`, run on
seedance-2.5 with the flag, read the same way. Switching a shipped default on
one blink test would have been the easy call and the wrong one.

**The approval-gate line changed shape rather than disappearing.** The
message used to require one line saying the scenario had no paid run behind
it. It now requires one line saying what the evidence actually is — one 10s
English run at 480p — because "thin evidence, described accurately" is what a
user needs to hear, and the draft is still there to be watched. The skill has
one billed job behind it, 64 cents, quoted as a sense of scale; the `--dry-run`
figure remains the only number put in front of anyone.

## 1.0.0 — first release

A scenario skill for one person, framed chest-up, speaking a short script to
camera: a portrait as the opening frame, the words as text in the prompt, the
voice generated. Execution is delegated to `ofox-video-core`.

**The scenario was redefined before it was built, by a measurement.** The
original framing was "use this portrait to read this audio". That is not
available: the API accepts an `audio_url` reference, validates it, fetches it
and bills the job, and the delivered audio is **not** the audio that was sent
— measured 2026-09-15 on job `d8561509-dcc6-4f2c-8864-a193cd239b14`,
`bytedance/seedance-2.5`, 55 cents, input near-continuous speech against a
sparse output, envelope correlation 0.41. So this skill takes **text** and
lets the model produce a voice for it, and says outright that a supplied
recording cannot be made to play.

**This is the first scenario skill in this repo whose default model is not
`bytedance/seedance-2.5`, and the reason is evidence rather than taste.**
Seedance 2.5 refuses a real person's photograph as an image-to-video input at
submission (`HTTP 400 input_moderation_failed`, "may contain real person",
nothing billed) — and a portrait is this scenario's defining input. In the
2026-09-15 three-model comparison, `alibaba/wan-3.0-prime` accepted the same
portrait and completed at 12.8 cents (2s, 480p) and `minimax/hailuo-3`
accepted it at 32 cents (4s, 768p). Wan is the default because it also reaches
further in duration; hailuo is named as the fallback.

**What that comparison does not establish is stated as prominently as what it
does**, because this repo has shipped claims before whose supporting
measurement answered a different question:

- nobody read the frames of the two accepting jobs — "completed" is a job
  status, not a verdict on whether the clip looks like the person or whether
  the mouth matches the words;
- the portrait was synthetic, generated for the test, so it is one content
  class;
- **wan's speech is unmeasured.** Every word-rate number this skill plans
  against comes from a gallery corpus, and every Ofox run in this repo that
  produced spoken dialogue was on `bytedance/seedance-2.5` — the one model
  this route cannot use. The skill says so in three places and never presents
  seedance's figures as if they applied to wan;
- **wan's frame lock is unmeasured** — "what a frame lock actually holds" in
  the shared reference is three seedance-2.5 jobs, so "the clip opens on your
  portrait and stays that person" is the hypothesis this route is built on,
  not a finding;
- **wan is not upstream-pinned.** The script pins `byteplus` for Seedance
  only; wan routes by weight across two upstreams that moderate differently,
  so one accepting run is one upstream's verdict at best.

**The word capacity is stated before anything is priced, and it is budgeted
against the right tier.** The shared word-rate section carries two tiers, and
the one that applies here is the one named after this skill: monologue /
talking head, 3.5 words a second in English and 5 characters a second in
Chinese. The dialogue-drama band (0.4–1.7 words/s) measures two people with
silence between their lines, so it is a floor here rather than a budget. The
skill plans a little under its own tier — **3 words a second, 4 characters a
second** — because the template spends clip time on an opening beat and a
written silent ending while asking for an unhurried delivery, and because the
asymmetry is one-sided: under-filling costs a pause, overrunning costs the
whole clip. That puts a 30-second clip at about **ninety spoken words** and 15
seconds at about 45. The clip-length-to-word-count table is the scenario's
consequence only; the rates and their gallery cases stay in
`ofox-video-core`'s `prompt-structure.md`, linked rather than restated, along
with the fact that both tiers are counts of gallery prompt text rather than
measurements of what this API delivers. When a script overruns, the brief's
`Overrun` question offers cutting it, lengthening the clip, or splitting
across jobs, and the splitting section says what splitting really costs: a
bill per part, a visible join, and continuity that is only as good as
re-attaching the same portrait, which on this model is untested.

**A likeness section sits above the mechanics.** Confirm the user may use the
face, refuse identifiable public figures, and do not offer `--real-person
true` as a workaround — it is documented for `bytedance/seedance-2.0` and
untested on 2.5 in this repo.

Also in this release:

- **Two routes, and the model follows the route.** With a portrait it is
  `alibaba/wan-3.0-prime`; with no portrait it is ordinary text-to-video on
  the script's default, which is the shape this repo has actually run (five
  completed 20–30s jobs built around photoreal people). The default exists
  because of the photograph, and the skill says so rather than treating wan as
  a house preference.
- **A question set of five in four slots**, with `Portrait` and `Script` as
  must-ask rows carrying no "Let the AI decide" — inventing someone's words is
  the one thing this skill must never do — plus skip rows that route
  "and then he replies…" to `seedance-short-drama` and "summarise this
  article" to `explainer`.
- **A single-shot prompt template with no manifest and no cut list**, a
  verbatim-quote rule for the script, one gesture per beat, an explicit
  ending beat, `no music` in both the sound block and `AVOID` (a scored cue
  failed output moderation on copyright in this repo, unbilled), and no
  on-screen text — the frame slot that could carry a title card is already
  spent on the portrait.
- **Portrait handling**: look at it, crop it to the delivery ratio (crop,
  never pad — an attached frame makes the output follow the image), and
  measure the real pixels rather than trusting a reported size.
- **No hardcoded model, price, resolution, duration or aspect-ratio table.**
  Those are catalog facts and the skill points at `ofox-video.sh models` /
  `providers MODEL` / `generate --dry-run`.
- **No cost anchor, because there has never been a bill.** The approval-gate
  section says the dry-run figure is the only number to show, and that the
  message must carry the script in full plus one line saying the scenario is
  unproven.
- **An after-it-lands checklist** — is it the right person, do the mouth and
  words agree, were all the words said — because `STATUS completed` answers
  none of them, and the identity check is the one carrying the most new
  information on this route.
- **The core-directory probe ships from day one**, so the skill works on
  LobeHub's `ofoxai-skills-<name>` layout as well as skills.sh / ClawHub /
  `npx ofox-skills`.

**What a caller has to do**: install `ofox-video-core` beside this skill.
`npx ofox-skills` installs every skill in this repo, which is what keeps the
sibling path resolvable.
