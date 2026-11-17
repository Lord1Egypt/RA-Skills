# Changelog

All notable changes to the **seedance-short-drama** skill. Versioning follows SemVer.

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

This file starts at 1.0.3; earlier versions predate it.

## 1.13.5 — the recovery command asked for the whole repo, and asked the agent to run it

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

## 1.13.4 — 1.13.3 moved the default it said it had not moved

**Documentation only. No price, prompt template or behaviour changed — and
this time the defaults table is back where 1.13.3 claimed to have left it.**

1.13.3 rewrote the `--real-person` row's *Default* column from `leave unset
(false)` to `leave unset (false) — unless the user holds the right to the
likeness in an attached photo and has said so`. That is a different
instruction, not a corrected piece of evidence: it invites the photo route in
the one skill whose own body says the opposite two sections earlier ("the
default stands") and whose "When NOT to use" hands a supplied portrait to
`talking-head`. The carve-out belongs in `keyframe-animation`, where a
user-supplied pair of frames *is* the input; here the input is a script. The
default is unconditional again, and the *Why* column keeps every word of the
corrected evidence.

**A fourth stale absolute, in the worked example.** Case 1's walkthrough still
read "on Ofox a photoreal person cannot be attached, so both are carried in
text" — the same claim 1.13.3 softened in two other places and missed here
because the sentence wraps and carries no hedging word to grep for. It now
says the attached frame is refused *unless the caller asserts the rights to
that likeness*. The example's own choice — both characters in text — is
unchanged.

## 1.13.3 — this file was still calling a measured flag untested

**Documentation only. No default, price, prompt template or behaviour
changed.**

Four places in this file said `--real-person true` was untested on
`bytedance/seedance-2.5`. It was measured on 2026-09-16 — a single-variable
A/B — and it **lifts** the submission refusal. Those four are corrected: the
"Reference images and real people" bullet, the defaults table row, the
`input_moderation_failed` troubleshooting row, and the "When NOT to use"
entry about animating a real person's photo.

The correction is deliberately not a green light. Every one of them now says
the same two things: the flag is Ofox's privacy-preserving preprocessing path
for **authorised** real-person references — an authorisation route, never a
way past the check, never a retry after a refusal, never set on a user's
behalf — and what was measured is one short single-frame clip at one tier on a
synthetic portrait, which is nothing like a drama carrying one face across a
shot list. The evidence and its limits live in `ofox-video-core`'s
`references/api-params.md` and are linked rather than copied, so there is one
place to correct next time.

**What did not change, and why it is worth naming.** The identity-reference
bullet (`input_references` with a real person, untested either way) is about a
different route and is still true. The text route stays this skill's answer
for character consistency — the measurement moved a wall, not this skill's
default.

## 1.13.2 — routing against two new neighbours

**Documentation only. No flag, default, price, prompt template or behaviour
changed.**

`talking-head` and `explainer` ship alongside this skill, and both produce
spoken video with a realistic human in frame — which is close enough to this
skill's territory that an agent choosing between them needs the boundary
written down. The boundary is **who is being spoken to**: characters talking
to each other is short drama; a single speaker facing the audience is not.

Two edits carry it. The frontmatter `description`'s "do not use for" clause
now names both — a script read from a portrait the user supplies is
`talking-head`, an idea that still has to be chosen out of an article is
`explainer` — which is the line an agent actually reads when deciding whether
to load this skill at all. "When NOT to use" gains the same boundary with the
reasoning, including the fact that `talking-head` runs a different model
because `bytedance/seedance-2.5` refuses a real person's photograph at
submission.

Nothing about this skill's own scope moved: a monologue *inside* a scene is
still short drama, and the dialogue budget, shot density and camera-register
guidance are untouched.

## 1.13.1 — a seed does not reproduce a take, and this skill said it did

**Documentation only. No flag, default, price or behaviour changed.**

This skill's batch/promotion section told the agent that re-running a take's
seed with the same prompt at a higher resolution "reproduce[s] that take
rather than rolling a new one". That was inherited from `ofox-video-core`,
where it had been written from a 2026-09-05 measurement that only tested the
*other* direction: one seed, two prompts a paragraph apart, visibly different
subjects. The converse was never run.

It has been now. Three submissions of one byte-identical request —
`bytedance/seedance-2.0-mini`, 4s / 480p / 16:9, seed `424242` — returned:

| Job | Outcome |
|---|---|
| `2e45464c-9ea7-4836-96dd-93dffb5ef58d` | completed, 8 cents |
| `cf877512-3faf-42b5-92ad-2e83fa55dabf` | **failed** `output_moderation_failed`, not billed |
| `ef83ccb8-7147-416f-a4af-e2fb04a618d1` | completed, 8 cents |

The two completed clips are different generations — the single red balloon
sits in a different place and at 13x the pixel area at t=1s, and again at
t=3s. One identical request in three did not come back at all.

**What this changes for a caller**: a promotion is another roll aimed at the
same shot, not that shot enlarged, and the agent has to say so *before* the
user pays for it. A byte-identical prompt is still necessary — read it out of
the sidecar rather than retyping it — it is just not sufficient. The full
record, including the 2026-09-05 pair it replaces, is in `ofox-video-core`
1.23.0.

## 1.13.0 — the 720p default does not survive naming another model

1.12.0 let a user say "use wan" / "use hailuo". The defaults table was written
when `seedance-2.5` was the only option, and **`--resolution 720p` does not
exist on `minimax/hailuo-3`**, which offers `768p` and `2k` only. The script
rejects `720p` there locally, before submitting, at no cost — a wasted turn
rather than a wasted dollar, but avoidable. The defaults row and a new "What
changes when the model changes" section name the right tier, and flag
`hailuo-3`'s 15s duration ceiling against this skill's 4–30s room.

Aspect ratio needs no change here: this skill is text-to-video, where
`--aspect-ratio` is validated per model and decides the frame directly. If a
frame image is ever attached, `ofox-video-core` 1.22.0 now applies the frame's
shape per model (forced on `seedance-2.5`, the default elsewhere when no ratio
is passed) and prints a `NOTE:` saying which — on an older core a non-seedance
model sent no `aspect_ratio` at all.

Also corrected: this skill said `wan-3.0-prime` runs on a **single** `aliyun`
upstream. The catalog now reports two (`alicloud`, `aliyun`) — every
`alibaba/*` model gained a second upstream between 2026-09-02 and 2026-09-14.
Since `ofox-video-core` pins only the Seedance family, a `wan-3.0-prime` or
`hailuo-3` job routes by weight, so a moderation result on one run is not
guaranteed to repeat. The moderation table's own dated-evidence caveat already
said not to read it as policy; this says why that matters mechanically.

Docs only.

## 1.12.1 — find the core skill instead of assuming its directory name

Docs only; no script changes. Every example in this file calls the execution
layer as `../ofox-video-core/references/ofox-video.sh`, which resolves only
when the core skill's directory is named after the skill — true for skills.sh,
ClawHub and `npx ofox-skills`, and **false for LobeHub**, which unpacks each
skill to `~/.agents/skills/ofoxai-skills-<name>`. There the sibling is
`ofoxai-skills-ofox-video-core`, so this skill died on

```
bash: ../ofox-video-core/references/ofox-video.sh: No such file or directory
```

with the core skill installed and sitting right next to it. Reproduced in a
faked LobeHub layout on 2026-09-14.

New **"Where the core skill lives"** section, placed above the availability
check so it is read before the first call rather than after the first failure.
It carries a probe over the five known locations — the two sibling names, the
two under `~/.agents/skills/`, and `~/.claude/skills/` — and says to substitute
what it printed for `../ofox-video-core`, in the script commands and the
`references/*.md` links alike. The ~100 example commands stay written the
readable way; only the resolution rule is new.

**"If the script isn't found" is no longer a single command.** It used to name
`npx skills add ofoxai/skills` as the only fix, which tells a LobeHub user to
abandon their installer for a core they have already installed. It now splits
on the probe's result: a directory printed means the name was wrong and
nothing needs installing; nothing printed means the core really is absent, and
the fix is whichever installer the user already has. The shared reference
files (`prompt-structure.md`, `creative-brief.md`, `approval-gate.md`,
`api-params.md`) get the same two-branch reading, since they ship with
`ofox-video-core` and go out of reach for the same reason.

"Running the script" now points at the probe rather than restating the
relative path as if it were fixed.

Verified, not just written: in a faked LobeHub layout the probe returned
`../ofoxai-skills-ofox-video-core` and a `--dry-run` generate through it
exited 0 with nothing submitted; in the skills.sh layout it returned
`../ofox-video-core`, identical to the hardcoded path, so the working case
does not regress.

## 1.12.0 — a real choice of video model, not just a locked-in default

Docs only; no script changes — `--model` already accepted all three models
named below. Until now `model` sat in the never-ask row with the copy
"script default, no flag needed", which reads as if `bytedance/seedance-2.5`
were the only option. It was not the whole story: an explicit user request
("generate this with wan", "try hailuo") had no documented vocabulary in this
file to map that word onto a real model id, so an agent could read the old
copy as licence to render on 2.5 regardless of what the user asked for.

- **New "Choosing a video model"**, right after `Recommended defaults`: a
  table covering `bytedance/seedance-2.5` (default), `alibaba/wan-3.0-prime`
  and `minimax/hailuo-3` — price and duration cap from the public catalog
  (`GET /v1/models/catalog`, re-checkable, no key needed), and a real
  moderation data point for each. The moderation column is the one part
  that came from an actual paid call, not the catalog: a photoreal-portrait
  i2v reference and a Re:Zero/Rem-styled anime t2v prompt were both rejected
  on `seedance-2.5` (`input_moderation_failed`, and `output_moderation_failed`
  for copyright after generating) and both accepted on `wan-3.0-prime` and
  `hailuo-3`. Cited from `.trellis/spec/skills/external-api-integration.md`,
  "Gotcha: moderation policy is per-model, not a platform-wide constant" —
  stated as evidence about exactly those two content classes, not a general
  clearance for either model.
- **The never-ask row and the `--model` row now say the same thing**:
  never-ask means the agent doesn't raise the question itself, not that an
  explicit user choice gets overridden. A model named by id or by a
  recognizable shorthand ("wan", "hailuo") is used instead of the
  `seedance-2.5` default — never silently substituted back.

What a caller can do now that they could not before: say "use wan" or "try
hailuo" and have the agent actually pass that model, instead of it defaulting
back to Seedance 2.5 with no vocabulary to do otherwise.

## 1.11.1 — the key requirement, moved to the front of a description that gets truncated

Docs only; no script changes, no advice changed. `description` now **opens**
with one sentence: `Requires OFOX_API_KEY — create one at
https://app.ofox.ai.` The dependency itself is unchanged and was already
declared in `metadata.openclaw.requires.env`, which stays exactly as it
was — that is the route ClawHub and openclaw read. Nothing a caller does
changes.

**Two separate blind spots, measured 2026-09-06 against Codex CLI 0.149.1 with
a project-level install of this repo.** It listed all nine skills, but asked
which environment variables `seedance-product-video` needs before use it
answered that it could not tell from the visible skill metadata. The first
cause is the obvious one: some agents read only the frontmatter's `name` and
`description`, never `metadata`. The second only surfaced on a controlled
retry — same agent, same question, the requirement added to the **end** of the
description and nothing else changed — where the answer did not budge. Pressed
for a verbatim quote, the agent said the description in its context was
truncated and did not include the final sentence; it put its own visible tail
at about 257 characters, and the fragment it could still quote ends at
character 320 of the real text. So the window is roughly 300 characters, and
these descriptions run 828 to 1200. "Reads the description" is not the same as
"reads all of it".

**What that costs, beyond the key.** Inside a ~300-character window the
`Use when ...` trigger examples of all four scenario skills fall outside: they
begin at character 431 (`seedance-ad-creative`), 594
(`seedance-product-video`), 641 (`seedance-anime-drama`) and 690
(`seedance-short-drama`). A truncating agent has never matched any of them
on an example — it matches on the opening summary alone. Anything that has to
reach such a reader belongs in the first ~300 characters, which is why this
sentence leads instead of trailing, and why it is 58 characters rather than the
106 first drafted: that position is the scarcest space in the skill, and every
character spent there displaces a character of trigger material.

**Why character 0 and not the end of the opening sentence.** The first
sentence-ending period sits at character 268 in `ofox-image-core`, 430 in
`seedance-ad-creative` and 593 in `seedance-product-video`. Placed there the
sentence would straddle or clear the window in exactly those three, and
reaching a boundary at all in two of them would mean repunctuating shipped
prose. Character 0 is the only position that is inside the window under both
the 257- and the 320-character reading, for all six skills, without altering a
word of the existing text.

Two readers were never affected and are unchanged by this: Claude Code reads
the description in full, and OpenCode read at least the first 1075 characters
of `seedance-product-video` — it answered `OFOX_API_KEY` correctly even from
the trailing version.

## 1.11.0 — the only continuity route open to this scenario, now measured

Docs only; no script changes. This skill has always been the one that cannot
attach a frame: `bytedance/seedance-2.5` refuses a photoreal person at
submission, so the frame route every other scenario uses to continue a clip is
closed here. What was left — re-describing the previous clip's last frame in
words — was documented nowhere and measured never.

`c2eb32e1-3b54-4a56-8d78-86e63bc355c7` (2026-09-06, 8s, 480p, seed `18854260`,
0.88 USD) is a continuation written from a paragraph describing another clip's
final frame, with no image attached. It reproduced the over-the-shoulder
staging, both characters' positions near and far, the distinguishing prop in
the right number and place, wardrobe basics and palette. It did not reproduce
the exact pose, the camera's distance, or the light level — the same split
this repo already records under "A description is honoured; a number attached
to it is not".

The new section, "Continuing a scene across jobs, when no frame can be
attached", carries the block to copy and the two consequences: write the
continuation to pick up on a prop, a line or a position rather than on a
matched pose, and give the first beat its own timestamp as an action already
underway, because the block's `no re-staging` half is a prohibition on a tempo
and those are soft — the measured run still opened with about two seconds of
near-static preparation.

One limit is stated in the section rather than buried: that run was an **anime**
continuation. The mechanism is the prompt rather than the art style, but no
live-action continuation has been measured here, so a first one is an
experiment and should be priced as one.

## 1.10.0 — the transition-mix rule confirmed, the envelope opened up, and a movement floor for the one-take

Docs only; no script changes. Four accepted short-drama clips and one
rejected anime clip, generated 2026-09-03/04, settle three things this skill
was previously hedging about and add one it had no warning for. Cross-scenario
detail lives in `ofox-video-core`'s shared references (1.14.0); this file
carries the scenario's own half.

- **"Choosing a transition, not defaulting to a cut" now shows six jobs, not
  two.** Ordered by hard-cut share of the boundaries: 3-of-9 rendered **none**
  of its three hard cuts, while 3-of-8, 3-of-6 and 5-of-7 rendered all of
  theirs, as did two commerce jobs at 4-of-4 and 6-of-6. The direction is
  settled — **write hard cuts as at least half the boundaries when the beat
  needs a cutting rhythm** — and the threshold is still unknown, since the
  failing and passing cases are one boundary apart.
- **A verification rule to go with it**: check a draft by reading frames, not
  by counting a scene detector's hits. At threshold 0.3 the detector cannot
  see a cut between two shots in the same place under the same light, and it
  missed the single most important cut in each of two accepted clips —
  `41f87ac7-d7a6-4c8c-8efd-feb7bdc4818d` at 9.5s and
  `036ac3a8-6f68-47ad-a553-86a29aa3e5b8` at 9s.
- **"Shots, cuts and jobs" is rewritten around the measured envelope**: up to
  10 shots in 30 seconds with up to 6 hard cuts, at 480p and 720p. The caveat
  this section used to carry — that the two verified runs were silent while
  every real short-drama job has lines in it — is closed: four of the six
  jobs are short drama with audio on, and `036ac3a8` carried five lines across
  seven shots with all seven rendering in order. What remains unmeasured is
  named, including a single line split across a cut.
- **New: the one-take registers have a movement floor.** Job
  `16023efe-48d6-45fe-8fd8-f5c6fbfe6519` (20s, one continuous shot, zero cuts,
  characters stable) was rejected as too static, because its whole movement
  plan was one very slow push while the actors held a standing position. The
  `Camera` question's `Travelling one take` option, the shot-density table row
  and a new block under "Shot density" now say what the register requires:
  each phase must arrive somewhere the previous one could not see, movement is
  written as travel rather than as distance-closing, and a beat that genuinely
  happens on one face wants the **held take** instead.
- **The `AVOID` slot's text items are labelled a backstop, not a defence.**
  A period or festival setting needs the lettered surfaces composed out of the
  shots — the strongest possible `no legible text` still returned sign-like
  shapes on a neon street (`41f87ac7`), while a New Year courtyard with
  couplets in five of seven shots stayed clean by composition (`036ac3a8`).
- **The `SOUND` slot defaults music to none**, since asking this model for a
  scored cue has failed output moderation on audio copyright (unbilled).
- Five new rows in the failure table: hard cuts that did not happen, a
  detector reporting fewer cuts than were written, an inert one-take, invented
  lettering, and the ±1.5s cut-placement expectation with the measured fact
  that the deviation does not accumulate along the timeline.

## 1.9.0 — a duration budget, so the exciting part stops paying for the ending

Docs only; no script changes. Another correction from a real clip: the
first 720p short-drama job made with 1.8.0 (2026-09-03, job
`4e5c9581-d462-443b-9663-b1aa6d72f527`, 30s, ten shots, $7.20) was accepted
but flagged with four specific complaints — the fight in the middle was
good, the last third was plain; don't compress the best part to make room
for the ending; transitions were wasting seconds on slow motion; give the
repository owner more say in the brief. 1.8.0's `Shot density` table fixed
*how many* shots and *how long each one runs*; it had nothing to say about
*which* shots get the seconds, so a clip could pass every row of that table
and still spend a third of its runtime on a stand-off and a mirrored
stand-down. Fixed:

- **New "Duration budget — spend the seconds where the beat is."** A
  function-based split (setup / core / close) in concrete seconds at 20s,
  24s and 30s, in two rows: action/spectacle (payoff is the middle, close
  stays small) and dialogue/slice-of-life (payoff can legitimately be the
  last line, close gets real weight). Slow motion, speed ramps and freeze
  frames now have an explicit cap — about 2–3s total in a 30s clip, once by
  default — because the flagged clip's one decisive strike alone ran 4.5s
  once a speed ramp, a freeze and a resume were stacked on it. A symmetrical
  bookend (last shot mirrors the first) is documented as optional and priced
  out of the close budget, not added on top. The uniform ten-shots-at-3.0s
  pattern that produced the flagged clip is named as the counter-example the
  section exists to prevent.
- **"Choosing a transition, not defaulting to a cut" gained a finding that
  cuts against the direction 1.7.0's research pointed:** a `HARD CUT` label
  is not a guarantee, because a timeline weighted toward continuous
  transitions can soften an explicitly named hard cut along with the rest.
  Two 30-second jobs, read side by side (job `844c9145-9b10-4335-9fdc-ec4937793a2f`,
  8 boundaries, 3 hard cuts landed as written; job
  `4e5c9581-d462-443b-9663-b1aa6d72f527`, 9 boundaries, 3 hard cuts, **zero**
  detected). Two samples, not a threshold — the full comparison is in
  `ofox-video-core/references/prompt-structure.md`.
- **Two new brief questions, `Pacing` and `Effects`, in round two of a
  published deliverable** (`creative-brief.md`'s new second round) — where
  the runtime goes, and whether a slow-motion or freeze-frame beat belongs
  in the clip at all. Previously both were left entirely to the agent's own
  judgement, which is exactly what produced the flagged clip's imbalance
  without anyone approving it as a choice.

What a caller can do now that they could not before: ask "should the fight
or the ending get the runtime" as an actual question with concrete second
counts behind each answer, instead of discovering the answer only after
paying for a 720p clip; and check a draft's cut points against a documented
finding that a hard-cut-heavy timeline needs a hard-cut-heavy *mix*, not
just hard-cut labels.

## 1.8.0 — the template stopped defaulting to restraint: camera register, a transition menu, shot density

Docs only; no script changes. This release is a correction, not a feature:
the first real short-drama clip produced with 1.7.0 (2026-09-03, job
`38ca8311-5b2d-47d5-a45d-e8ebea0e6312`, 20s at 480p, four static shots, cuts
landing on 5/10/15s exactly as written, characters consistent across all four,
Mandarin delivery clean) was **rejected as too plain to publish**. Nothing in
it broke. It was written by filling this skill's own template with this
skill's own defaults, and the template's defaults were restraint on every
axis at once. Four things were wrong and are fixed:

- **The `Camera` question could not express a moving camera.** Its options
  were `Handheld documentary`, `Steady cinematic` and `Static
  over-the-shoulder` — three labels for the camera staying roughly where it
  is, which is the synonym-options anti-pattern `creative-brief.md`'s "The
  shape of a question" already forbids. The question is now about the
  **register**, and one answer settles both what the camera does and how many
  shots there are: `Travelling one take` (no cuts, the camera moves through
  the space, an occlusion or pass-through carries each new view, 3–5 phases of
  5–8s — cases 2, 6, 8) / `Multi-shot cut list` (a new size and position at
  every stamp, 2–5s a shot, 4–10 shots in 20–30s — cases 1, 11, 14) / `Held
  take` (locked or breathing handheld on one or two faces — cases 3, 22) /
  `Let the AI decide`. Handheld versus locked is now documented as a texture
  inside the register rather than a fourth option. New skip rows map traversal
  words ("walks with her", "one take", "out onto the street") and cutting
  words ("intercut", "shot list") straight onto a register.
- **The transition slot offered two of the nine kinds.** The template line was
  `HARD CUT.` or `Without cutting, <what changes the framing>`; the other
  seven kinds in the shared "Transitions" table were reachable only by an
  author who already knew to go looking. The line is now a `TRANSITION` slot
  that names the choice as a choice, with occlusion and pass-through spelled
  out inline, and a new "Choosing a transition, not defaulting to a cut"
  subsection lists all nine kinds and which four have short-drama instances
  (hard cut 1/4/5/7, cuts forbidden 2/3/6/8, occlusion 2/3/8, pass-through 8)
  — plus the fact that an unnamed boundary renders as a hard cut, so silence
  there is a decision.
- **The `CAMERA:` block had no movement field.** It held lens, depth of
  field, focus and the axis rule, so camera movement had nowhere to go — and
  the rejected run duly came back with "locked off, never a whip, never a
  zoom, never a push-in" in the `CAMERA` line and "camera still" in all four
  shots. The field now leads the block, with `static` as one of its values
  rather than the absence of one, and the slot table explains why it is not
  optional.
- **Shot density was unstated, so the template's floor became the target.**
  New "Shot density — pick a register, then count": four registers with per-
  case anchors (held take, case 3's eight beats in one 15s frame; travelling
  one take at 5–8s a phase, cases 2/6/8; cut list at 3–5s, cases 1/18/22;
  spectacle at 2–3s, cases 11/34), the target count for 20s and 30s in each,
  and the finding that four 5-second static shots is the slowest point on the
  whole table and a shape the gallery does not contain. The Ofox-verified
  envelope (three shots in eight seconds) is restated as the limit it is, so
  a dense register is priced as an experiment.

Also: a **second worked example**, adapted from case 1 — 24 seconds, nine
shots at about 2.7s, four kinds of transition, a stairwell and a roof the
camera travels through, eleven spoken words. The case-3 example is kept
unchanged, and a new "Two worked examples, two registers" heading says both
are legitimate short drama and the brief's `Camera` answer picks between them.
A new failure-mode row covers the clip that renders exactly as written and
still looks like nothing, with the fix (re-ask the register, rewrite, new cost
table) rather than a shrug.

## 1.7.0 — creative brief, structured prompt template, several shots per job

Docs only; no script changes. What moves:

- **Behaviour change: several hard-cut shots in one job.** This skill said
  "one job = one continuous shot" and "Seedance may not honor a hard cut
  mid-clip". Two real runs on Ofox (2026-09-03, `bytedance/seedance-2.5` via
  `byteplus`, 8s, 480p, three shots each) cut where the timestamps said, to
  about ±1s — recorded in `ofox-video-core/references/prompt-structure.md`
  under "Several shots in one job". That section here is now "Shots, cuts and
  jobs": timestamps are cut boundaries, 2–5s per shot, `HARD CUT.` between
  them. What was **not** verified — 30s or 8+ shots, dialogue across a cut,
  resolutions other than 480p, `volcengine` — is listed as unverified rather
  than assumed. `chain` still does not apply here (real person); separate
  jobs remain the route when each shot needs its own approval, seed or
  resolution, or the sequence exceeds 30s.
- **New "Before writing the prompt: the creative brief".** The rules for it —
  three tiers (must-ask / ask-if-open / never-ask), one AskUserQuestion round
  of at most four questions with at most one branch follow-up, zero questions
  as the normal case when the input settles everything, the recommendation
  first and "Let the AI decide" always last and never preselected, a
  delegated choice resolved to a concrete value marked `(AI's pick)`, the
  recap riding in the same message as the cost table, the generic skip rows,
  the no-`AskUserQuestion` fallback and the anti-patterns — live once in
  `ofox-video-core/references/creative-brief.md`, which this section links
  rather than restating. What this skill carries is its own: six questions
  (beat, aspect, arc, camera, lines over budget, drafts), the short-drama
  inference rows (the language of quoted lines maps to the spoken language
  and is never asked; stage directions and tone words build the emotional
  arc), the answer-to-prompt map, and a worked recap. The `Beat` question is
  must-ask and therefore carries **no** "Let the AI decide" option, per the
  shared rule — if the user says "you pick", name the beat you chose in the
  recap and let the cost table be the check.
- **New "Prompt template"**, replacing "Writing a good short-drama prompt": a
  15–30s manifest + timestamped-shots template and a 10s-or-less single-shot
  one, each with a worked example adapted from the gallery (cases 3 and 20,
  translated). Vocabulary is linked from `prompt-structure.md`, not copied.
  Scenario slots: the emotional-arc arrow chain, 1–3 visible signals per shot,
  delivery notes on lines, off-screen partners, wardrobe colour blocks, ending
  state, a sound block, the negative list.
- **Dialogue budget is two tiers.** Dialogue drama averages 0.4–1.7 words/s
  (2–3 words/s is a ceiling, not a target; most seconds carry no line);
  talking head runs 3.5 words/s English or 5 characters/s Chinese/Japanese.
  The old single figure over-wrote drama and under-wrote monologue.
- **Defaults.** `--aspect-ratio 9:16` is now the brief's Aspect question,
  falling back to 9:16 when skipped or delegated; the gallery's short-drama
  sample is mostly 16:9 (5 of the 6 that state a ratio), which the table now
  says. Character description: clothing with colour and material is the one
  field every gallery prompt writes; the other fields are as needed.
- **Reference images.** Both meanings of an attached image are named — frame
  lock (`--frame-first-image`) and identity reference (`input_references`) —
  with what is actually verified: the frame path refuses real people; the
  identity path is untested with real people; `--real-person true` on 2.5 is
  untested. Cross-job consistency here stays text-based.
- `description` now says a clip may be one shot or a few hard-cut shots, that
  the skill runs a brief when the input leaves things open, and that
  anime/manga scenes belong to `seedance-anime-drama`.
- Sentences that restated `approval-gate.md` — where an estimate comes from,
  how a batch is itemised, how the real bill is reported — are pointers now.
  The gate itself has not changed.

**What callers do**: nothing mechanical — same script, same flags. An agent
that had learned to split every cut into its own job can put two or three
shots in one 8–15s job. Expect one question round before the cost table when
a request leaves beat, aspect, arc or camera open; "just do it" delegates the
taste questions, not the must-ask ones.

## 1.6.0 — link the shared approval gate instead of restating it

- "Cost: quote it, get a yes, then spend it" and "Before you spend: show the
  prompt, not just the price" are replaced by one section that links
  [`ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md),
  the spec now shared by every Ofox skill in this repo. Both sections were
  right; keeping four private copies of them was the problem.
- What stays here is scenario-specific: the quoted dialogue goes in front of
  the user in full, because a line silently rewritten or translated is the
  most expensive thing that can go wrong in this scenario.
- Batches get an itemised table, not just `BATCH_COST_TOTAL`.

## 1.5.0 — tell people they can get a price without signing up

- New section: `models`, `providers` and `--dry-run` all work with no API key,
  so quote the job first and point at signup second. Opening with "go get an
  API key" asks someone to register before they know what it costs.
- New troubleshooting entry for
  `bash: ../ofox-video-core/…: No such file or directory` — it means the core
  skill isn't installed alongside this one, not that anything is broken. That
  raw error names neither the missing skill nor the fix, and a non-programmer
  reads it as "this is broken".

## 1.4.0 — exit codes, timeouts, contact sheets, and showing the prompt

Follow-up to `ofox-video-core` 1.8.0, closing gaps a second role-play review
found in this skill specifically:

- **Exit codes are listed here now.** This skill pointed at
  `references/api-params.md` for them; that file only has the `error.code`
  table, so an agent looking up exit 6 found nothing where it was sent.
- **Timeout guidance.** `generate` can block nine minutes, longer than a
  default agent tool call allows. Names `create` + `poll` as the way out, and
  the `takes x max-wait` arithmetic for `batch`.
- **Duration expectations**, so the wait isn't silent for the user.
- **Hand over the `CONTACT_SHEET` path.** In a batch flow it is the artifact
  the user looks at first, and this skill never said to give it to them.
- **Per-take seeds** are now reported by `batch`, which makes "take 3 was the
  good one, render it properly" a real command instead of a reroll.
- **Show the prompt, not just the price.** The user is paying for the prompt;
  a clip that costs exactly what was quoted and shows a character they never
  pictured is still a wasted job.

## 1.3.0 — quote before spending, and stop littering the user's repo

Rewrites the cost and delivery guidance around `ofox-video-core` 1.7.0's new
`--dry-run`. Previously this skill told the agent to relay an estimate that
the script only prints once the job is already billable — following it
literally billed the user with no warning.

- Cost flow is now: `--dry-run` to quote, wait for a yes, re-run without it.
- **`--out-dir` in every example.** This skill never mentioned it, and the
  script defaults to the current directory — so an agent copying an example
  dropped a bare-UUID mp4 into the user's project root.
- **`batch` is documented here now.** "Give me a few to choose from" is a
  normal request, and this skill previously offered no path to it but running
  `generate` repeatedly: no batch total, no contact sheet, no stop-on-failure.
  Includes the draft-cheap-then-render-expensive ladder.
- Quote `BATCH_COST_TOTAL`, not `BATCH_COST_PER_TAKE`.
- Report costs as money, not as the raw ten-decimal string.
- States how the relative script path resolves, instead of leaving it to the
  core skill's documentation.
- **Prompt language now documented.** Audio follows the language the prompt is
  written in, and every example here is English — so an agent handed Chinese
  dialogue could reasonably translate it and ship an English-dubbed clip the
  user has already paid for. Quoted dialogue stays in the user's language; the
  word-per-second budget is noted as English-calibrated, with a character
  count for Chinese and Japanese.

## 1.2.0 — chaining does not apply here, and now says so

`ofox-video-core` 1.6.0 added `chain`, which carries one shot's closing frame
into the next for visual continuity. **It cannot be used for this skill**:
Seedance 2.5 image-to-video refuses reference frames containing a real person
(`input_moderation_failed`, nothing billed), and this skill is
realistic-human by definition. Documented up front so a user doesn't discover
it mid-sequence — consecutive short-drama shots are generated independently,
with continuity coming from repeating the character description verbatim.

## 1.1.1 — cost guidance uses the script's own estimate

`ofox-video.sh` now prints a cost estimate before submitting, read from live
rates. This skill's guidance no longer tells the agent to compute one by hand
from a table that can go stale — relay the printed figure, and if it says the
estimate is unavailable, say that rather than substituting a number.

## 1.1.0 — jobs are pinned to the byteplus upstream

**Behavior change, inherited from ofox-video-core 1.4.0.** Jobs now go to the
`byteplus` upstream (ByteDance's platform for markets outside mainland China)
instead of wherever Ofox's weighted routing sent them. The two upstreams
moderate differently and routing was explicitly unpredictable, so the same
prompt could pass one run and be rejected the next. Pass `--provider
volcengine` for the mainland platform or `--provider auto` for the old
behavior. Pricing is identical either way.

No change to prompts or defaults otherwise.

## 1.0.3 — ClawHub frontmatter

- Frontmatter now carries a top-level `version` and
  `metadata.openclaw.homepage`/`envVars`/`primaryEnv`. ClawHub's publish
  scanner reads those, not `metadata.version` or the top-level `homepage`
  this skill already had.
- No change to prompts, defaults, or behavior.

### Inherited from ofox-video-core 1.2.0

This skill delegates execution, so it picks up per-model parameter validation
for free: a bad `--duration`/`--resolution`/`--aspect-ratio` for the chosen
model is now caught locally, with that model's own legal values named, instead
of costing a round trip to come back as a generic `invalid_request`.
