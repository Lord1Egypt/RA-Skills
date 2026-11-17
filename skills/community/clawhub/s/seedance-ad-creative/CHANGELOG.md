# Changelog

All notable changes to the **seedance-ad-creative** skill. Versioning follows SemVer.

## 2.0.0 — every real-run command carries `--approved`, and the core refuses without it

**Breaking, and the break is upstream.** `ofox-video-core` 2.0.0 makes its
four billable subcommands — `generate`, `create`, `batch`, `chain` — refuse to
run unless `--approved` is on the command line. Both of this skill's real-run
`generate` commands — the first-frame example under "Two ways to attach a
reference image" and the one under "Generating" — now pass it. The `--dry-run`
commands are untouched: a quote is how the number being approved gets
produced, so gating it would close the only route through itself.

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

This file starts at 1.0.4; earlier versions predate it.

## 1.13.7 — the recovery command asked for the whole repo, and asked the agent to run it

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

## 1.13.6 — the "no hosting needed" note needed its other half

**Documentation only. No flag, default, price or prompt template changed.**
One cell of the identity-reference row.

1.13.5 added that an image reference accepts a `data:` URI so a local file
needs no hosting. True, and dangerous on its own: a `data:` URI built into
`--extra-json` is bounded by `ARG_MAX`, and over the limit **the reference is
dropped silently and the job is submitted and billed as plain text-to-video**
(measured 2026-09-17, exit `0`, no `input_references` in the payload). The row
now carries that caveat and points at the reproduction and the guard in
`ofox-video-core`'s `references/api-params.md`.

## 1.13.5 — the identity-reference row said it had never been run; it has

**Documentation only. No flag, default, price or prompt template changed.**
One cell of the "two ways an image can enter a shot" table.

It read *"no image-reference job has been run end to end in this repo, and
whether `@image1` tokens resolve by position is unverified"*. Both halves were
closed by `ofox-video-core`'s measurement of 2026-09-16 (job `0f5c8b4e`, two
`image_url` references, 44 cents): the references' named features came
through, and **the `image1` / `image2` tokens resolve by position, in array
order**.

**What a caller can now do differently:** the route bills at the **plain t2v
rate** (not the dearer video-to-video rate a `video_url` moves a job to), and
an image reference accepts a **`data:` URI**, so a local file needs no
hosting. ⚠️ Pass `--aspect-ratio` explicitly on this route — the measured job
passed none and came back portrait from two landscape references. Two images
is the most that has been sent; nine, and mixing an image with audio or video
elements, are untested.

## 1.13.4 — found by a grep this file should have been in from the start

**Documentation only. No default, price, prompt template or behaviour
changed.**

The reference-image paragraph said `--real-person true` was untested on
`bytedance/seedance-2.5`. It was measured on 2026-09-16 and it **lifts** the
submission refusal. The paragraph now says that, with the framing that
matters: the flag is Ofox's privacy-preserving preprocessing path for
**authorised** real-person references — an authorisation claim, never a way
past the check, never a retry after a refusal, never set on a user's behalf.
Evidence and limits are linked to `ofox-video-core`'s
`references/api-params.md` rather than copied in.

This skill was **not** on the list of files to fix. The list was assembled
from memory of which files had said it; this one turned up only when the
search was run across the repo with a pattern that could cross a line break.
That is the lesson worth keeping: the scope of a writeback is decided by a
search, not by recall.

**The route this skill recommends is untouched**, and it is still the better
one: attach a frame of the product alone and write the model into the
timeline as text. The `chain` constraint gains a clarification instead of a
loophole — the flag is an assertion about a **real** person the user may use,
which a face the model invented in the previous segment is not, and no chain
has been run with it set.

## 1.13.3 — the UGC-variant table told you to say where the phone is

**Documentation only. No flag, default, price or behaviour changed.**

The UGC-variant slot table's `Device line (new)` row said to write *where the
phone is*, quoting cases 25 and 27 (`propped on a gym bench, slightly low
angle`). Measured 2026-09-15 on job `2ecbedec` — `ugc-ads`' first paid run,
88 cents — that construction puts **a phone in the shot**, visible in every
frame, with a lit screen. The model has no concept of an off-screen camera: a
noun given a position in the room is set dressing, and set dressing is
rendered.

- The row is now `Capture line (new)` and asks for the **viewpoint** as a
  property of the shot (`selfie viewpoint`, `handheld`, `a fixed viewpoint at
  bench height, slightly low`), keeping the flaws the row exists for —
  autofocus hunting, exposure shifts, compression artifacts.
- A ⚠️ under the table names **both** affected cells: that row, and the CLOSE
  row's case-25 quote `the camera continues recording for a moment`, which
  has the same shape. It gives the replacement wording, the AVOID item to add
  as an object (`a phone, a camera, a tripod or a lit screen visible anywhere
  in the shot`), and links the full note in `ofox-video-core` 1.24.0's
  `prompt-structure.md`.
- It records that nothing caught this before delivery: the prompt passed
  `--dry-run` and `--print-payload`, and only the extracted frames showed it.

The gallery quotes stay in the table — they are accurate records of what those
authors wrote, and this skill's UGC table is explicitly a description of
gallery practice. What changed is that a reader is now told which parts of
them are safe to copy.

## 1.13.2 — a seed does not reproduce a take, and this skill said it did

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

## 1.13.1 — UGC and vertical drafts now have their own skills

Two sibling scenario skills shipped, and both take work this file used to
absorb by default. No behaviour in this skill changes; the routing does.

- **`ugc-ads`** owns handheld, phone-shot creator clips. The "UGC variant"
  section here stays as a slot diff against the cinematic template, with a
  pointer at the top saying that skill is the better route — it inverts the
  polish default outright, which this file cannot do while its own archetypes
  are Luxury, Playful and Minimalist-tech.
- **`shorts-reels`** owns several cheap vertical drafts and the
  draft-then-promote ladder. The ad prompt is still written here; the set runs
  there.

Both are added to "When NOT to use". **What a caller has to do**: nothing, if
the routing was already right. If you have been using this skill's UGC variant
table for genuinely creator-style clips, move to `ugc-ads` —
`npx ofox-skills` installs it.

## 1.13.0 — two defaults did not survive naming another model

1.12.0 let a user say "use wan" / "use hailuo". Two entries in the defaults
table were written when `seedance-2.5` was the only option:

- **`--resolution 720p` does not exist on `minimax/hailuo-3`**, which offers
  `768p` and `2k` only — so the draft row of the cost table is `768p` there and
  the deliverable row is `2k`, not `1080p`. The script rejects `720p` on that
  model locally, before submitting, at no cost, but a cost table quoting a tier
  the model doesn't have is wrong before that point. The defaults row and a new
  "What changes when the model changes" section carry the right tiers.
- **The attached product photo's shape.** "`--aspect-ratio` does not apply once
  an image is attached" held because `seedance-2.5` overrides it. On another
  model nothing overrode it and no `aspect_ratio` was sent at all, so the clip
  could come out in a shape the photo never had — after it was paid for.
  `ofox-video-core` 1.22.0 fixes that in the tool: `adaptive` is forced on
  `seedance-2.5` and applied as the default on a model that offers it when no
  `--aspect-ratio` was passed. The `--aspect-ratio` row now says which
  mechanism applies where. Cropping or padding the photo to the brief's ratio
  before generating is unchanged and still decides the output's shape.

**What a caller has to do**: use `ofox-video-core` 1.22.0 or newer if a user
names a model other than `seedance-2.5`. On an older core, pass
`--aspect-ratio adaptive` explicitly with a photo attached, or stay on the
default model.

Docs only in this skill; the behaviour change is in `ofox-video-core`.

Also corrected: this skill said `wan-3.0-prime` runs on a **single** `aliyun`
upstream. The catalog now reports two (`alicloud`, `aliyun`) — every
`alibaba/*` model gained a second upstream between 2026-09-02 and 2026-09-14.
Since `ofox-video-core` pins only the Seedance family, a `wan-3.0-prime` or
`hailuo-3` job routes by weight, so a moderation result on one run is not
guaranteed to repeat. The moderation table's own dated-evidence caveat already
said not to read it as policy; this says why that matters mechanically.

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
were the only option. An explicit user request ("generate this with wan")
had no documented vocabulary in this file to map that word onto a real
model id, so an agent could read the old copy as licence to render on 2.5
regardless of what was asked for.

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
  clearance for either model. Flagged as directly relevant to this skill's
  own "A model *and* a locked product" section, since a person on screen is
  exactly the kind of shot that hits moderation.
- **The never-ask row and the `--model` row now say the same thing**:
  never-ask means the agent doesn't raise the question itself, not that an
  explicit user choice gets overridden. A model named by id or by a
  recognizable shorthand ("wan", "hailuo") is used instead of the
  `seedance-2.5` default — never silently substituted back.

What a caller can do now that they could not before: say "use wan" or "try
hailuo" for an ad and have the agent actually pass that model, instead of it
defaulting back to Seedance 2.5 with no vocabulary to do otherwise.

## 1.11.0 — a rejected ad: "slow" got executed as "still", and every beat needs an event

**The first rejected clip in this scenario, and it was rejected for something
this file did not have a rule about.** Job
`cb6b7870-22f7-4a15-9168-8a013805775f` (2026-09-07, 15s, 720p, 5 shots, 4
hard cuts, generated first frame attached, Luxury tone) was built to Template
A and passed every check this file knew how to make: all four cuts landed
within half a second of their stamps, the shot budget held, the etched brand
word survived unaltered, a near-black studio produced zero invented text, and
the payoff beat worked. The verdict on it was that the product rotates once
and then nothing much happens — too simple, too monotonous. Billed 3.60 USD
for the clip plus 0.153995 USD for the frame, 3.753995 USD in total, and it
is kept as a rejected case rather than a gallery entry.

- **New section, `7. Every beat needs a physical event — and "slow" is not
  "still"`.** Read off sampled frames: **two of the five segments contain no
  physical event at all** (the orbit, which never moved, and the held hero
  frame) and a third contains only moving light (the macro HOOK). Only the
  cap unscrewing and the steam rising are events, so roughly **5.5 of the 15
  seconds** have anything happening in them. The cause is three sentences
  written on purpose — `the camera holds
  still`, `the bottle itself never moves or rotates`, `the camera is
  completely still and the bottle does not move`. The middle one is the
  instructive failure: it was written to stop the product self-rotating,
  which worked, but the camera was given nothing to do in exchange, so the
  segment came out static on both counts. Three repairs: no pure-display
  beat, `slow` is a speed rather than a quantity, and a product that cannot
  move on its own needs motion brought in from outside (pour, ice, steam, a
  hand, moving air) or the shot count raised from 5 to 7.
- **The two accepted 15s/5-shot ads are the control, and the difference is
  not pacing.** `7ae7d49e` and `60fbea52` share the exact envelope — 15s, 5
  shots, 4 hard cuts, first frame attached. Neither cuts faster. What they
  have is a physical event in *every* segment: bubbles rising continuously in
  one, a hand entering and a droplet falling in the other.
- **The warning that was already here, and why it did not bind.** `The beats
  below are a floor, not a ceiling` and `Split a beat into two shots rather
  than holding one for six seconds` were both in this file when that prompt
  was written, and the prompt sat exactly on the floor at 15s/5 shots. Those
  sentences are about the shot **count**; neither says anything about what
  must happen inside a beat. A beat can be at the floor and still be dead.
  The paragraph now says so and points at 7, `SHOWCASE` carries a required
  physical-event slot, and the Luxury archetype line in 3 marks `slow
  movement` as a speed and not a quantity.
- **`PAYOFF` moves from a proposed counter-measure to a verified one, first
  try.** It was written from `60fbea52`'s failure — a drop that hung from a
  pipette for a five-second climax and never landed — and carried here
  unverified for two versions. This clip gave the payoff its own stamp
  (`11-13s`, a separate boundary from the climax) plus a required-event
  sentence whose negative clause names the earlier failure exactly: `the
  steam has to leave the neck and travel up through the light within these
  two seconds, not merely hang above it`. The steam rises, glows and drifts,
  confirmed at t=12.5s, and that segment scores 0.0049 — the
  second-liveliest in a clip rejected for stillness.
- ⚠️ **A conclusion this repo marked verified is downgraded to "once held,
  once failed", and it is not this skill's own.** `A shot size on every
  waypoint` was recorded as a verified cure for a segment inheriting the
  previous one's framing. This clip wrote it on all three SHOWCASE waypoints,
  closed with `the bottle stays fully in frame at every moment of the move`,
  and still rendered six frames of upper-body close shot with the base never
  in view and the brand word clipped at the right edge. Same structure as the
  clip that held (macro beat, then waypoint orbit); different result. The
  record and the unexamined differences (i2v with a paid macro first frame
  against t2v, most of all) are in `ofox-video-core` 1.20.0.
- **One usable rule out of that failure, from the same clip.** Its `11-13s`
  and `13-15s` shot sizes were both written across hard cuts and both
  delivered — the last one holding the whole bottle cap to base with margin,
  which is what the waypoints asked for and never got. So when a beat needs
  the framing to open up, put the wider shot after a cut rather than inside a
  camera move. Cheap here, because Template A's boundaries are hard cuts
  anyway.
- **`--target-aspect` confirmed end to end on a real ad frame, and it removes
  both manual steps.** One flag produced the API's own `1792x1024` bytes at
  the `-uncropped` path and an exactly-16:9 `1792x1008` at the plain path.
  **No downscale to 1280x720 was needed** — `adaptive` takes the ratio, not
  the pixel count, so a 1792x1008 frame yielded a 1280x720 clip.
  `60fbea52`'s third hand-crop step was never necessary.
- **A sound written as `faint` was honoured as inaudible, while the two
  timed cues landed exactly.** New paragraph in 4. The clip's AUDIO line
  named three cues; the cap thread and `the short pneumatic tick of the seal
  parting at 9s` rise off a -43 to -46 dB floor to -30.9 dB at 7.7s and a
  -21.7 dB peak across 8.8-9.2s, the loudest passage in the clip and exactly
  where written. `a faint hiss of steam at 11s` produced no measurable event
  at all — the level *drops* to -41.6 dB at 11.5s — although the steam is
  plainly visible. **Timing a sound to a visible action works; an intensity
  adjective is not a volume control.** Also a new row in 6's AVOID record.
- **A second image-cost measurement at the same pair.** 0.153995 USD against
  `60fbea52`'s 0.154035 USD, both `openai/gpt-image-2` at `--quality high`,
  agreeing to within four hundredths of a cent. 15.4 cents is the figure to
  plan with at that pair — still quoted from the script's own line, label
  included.
- **A fourth row in the multi-shot record, and a warning attached to it.**
  Four 720p first-frame jobs now, three accepted and one rejected; all four
  wrote every boundary as a hard cut and all four kept every cut. The
  rejected one hit its stamps more precisely than any of the three accepted
  ones. `Do not read "every cut landed" as "the clip worked"` is now written
  next to the table, because that table is exactly the sort of evidence that
  invites it.
- ⚠️ **A per-segment scene score was tried as the evidence for all this and
  it does not support it — the numbers are out and a warning is in.** An
  earlier draft of this section carried a per-segment score table. It does
  not reproduce, and worse, the metric ranks this clip almost backwards:
  measured at native 24fps with the cut frames excluded, the beat where steam
  visibly rises scores 0.0008 — second from the bottom — while the orbit that
  never moved scores 0.0039 and a static macro whose only change is a
  highlight sweeping brushed metal tops the clip at 0.0078. `scene` counts
  whole-frame pixel churn, so a large low-contrast light sweep beats a small
  high-contrast physical event, and a near-black set maximises both errors.
  The conclusion is unchanged because it never rested on those numbers — it
  rests on the frames and on the verdict — but the table is gone and section
  7 now says to sample frames instead. The general form is a new section in
  `ofox-video-core` 1.20.0, `A scene score is pixel churn, not motion`.
- ⚠️ **The 0.25 scene-detection default finds only two of its four cuts.**
  The scores descend monotonically through the clip — 0.395, 0.311, 0.216,
  0.132 — because the shots get more alike as it goes, so 0.15 finds three
  and 0.10 is the first threshold that finds all four. Scanned once at the
  default, the clip reads as "half the written cuts were dropped"; in fact
  all four landed, at 3.000 / 7.542 / 11.042 / 13.250s against stamps of 3 /
  8 / 11 / 13. The repo-wide record is in `ofox-video-core`'s `Checking the
  cuts`.
- **Regression check on the 1.10.1 description change: no change in
  behaviour.** This run doubled as the first real end-to-end use of the skill
  after the `description` was rewritten to lead with the key requirement. The
  creative brief ran normally — three questions in one round, the must-ask
  photo question first and with no AI option, `Camera` and `Aspect` carrying
  `Let the AI decide` last, `"premium"` inferred to the Luxury archetype via
  the skip table without spending a question, and duration, resolution,
  model, provider and audio all correctly not asked. Template A's skeleton
  came out intact and the recap, the full prompt and the cost table arrived
  in one message. Nothing in this section changes because of that; it is
  recorded so the question does not have to be reopened.

Docs only; no script changes. The prompt templates, flags and defaults are
unchanged apart from the `SHOWCASE` slot gaining a required physical-event
element.

## 1.10.1 — the key requirement, moved to the front of a description that gets truncated

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

## 1.10.0 — a third accepted ad: the cuts and the duration split held, the climax's payoff did not

Docs only; no script changes. One accepted 720p job
(`60fbea52-b14b-4796-80bf-03afe0aa4fa0`, seed `799906248`, 2026-09-05, in the
gallery as `aura-serum-ad`) — 15s, 5 shots, 4 hard cuts, image-to-video from a
generated first frame, billed 3.60 USD for the video at the t2v rate plus
0.154035 USD for the frame on `openai/gpt-image-2` at `--quality high --size
1792x1024`. Versions in force when it ran: this skill 1.9.0,
`ofox-video-core` 1.14.0, `ofox-image-core` 1.4.0. It confirms four things
this skill already claimed, refines one, and breaks two.

Confirmed:

- **All four hard cuts survived**, at 2.62 / 4.75 / 6.62 / 12.25s, on a
  timeline that wrote every boundary as a hard cut. That is this scenario's
  third all-hard-cut job at 4 of 4, 6 of 6 and 4 of 4, and the sixth run
  repo-wide whose written hard cuts all rendered — against the one that lost
  all three of its at a share of 3 of 9. The row goes into "Several shots"'s
  existing evidence table; the single repo-wide list stays in the shared
  file.
- **The written duration split was honoured within 0.4s per shot** — planned
  3 / 2 / 2 / 5 / 3, rendered 2.62 / 2.13 / 1.87 / 5.63 / 2.79, including a
  deliberately lopsided split. Spending the seconds by function is now a
  measured instrument on this path, so the stale Template A bullet warning
  that four or five beats was beyond what had been verified — retired in
  1.9.0 and never rewritten — is replaced by this measurement.
- **The frame lock held from 0.3s to 14.9s**: bottle, frosted finish, black
  collar and bulb, label, glass of water, eucalyptus sprig, desk grain and
  bare wall all unchanged. So did the label word `AURA`, in every shot it
  appeared in, plus the same word rendered correctly as an end card — with
  the reference frame declared the sole authority on the label and an
  explicit ban on redrawing, restyling or re-lettering it.
- **A hand written in text over an object-only first frame** came back
  anatomically clean again.

New, and refined:

- **New: a continuous state change can be one of a consistency lock's listed
  changes, if its direction is pinned.** The light bars from the blinds were
  allowed to `only ever creep lower and warmer, never brighter, never
  higher, and never change direction`, and they did exactly that. One
  observation — but a dimming afternoon no longer has to be written as
  discrete steps.
- **"5. Text on screen" gains a clause.** The two studio ads got zero
  invented text on sets where nothing could carry lettering, so they never
  really tested the rule. This one is a **desk** — book spines and paper are
  the classic failure — and it still came back with zero invented text,
  because the wall was specified `entirely bare … no printed surface of any
  kind` and AVOID named every carrier of printed matter as an object rather
  than forbidding text. So: design it out of the set where the set allows it,
  and **where it does not, exclude each carrier by object** — a bare "no
  text" has already failed once, on a neon street.
- **New "6. What the AVOID list has held, and what it has lost."** An honest
  per-item record for this scenario's runs, including the two items this job
  lost.

Broken, and corrected:

- **The written climax did not render, and it is the one defect that reached
  the picture.** `10.5-12s the drop lands on the surface of the oil … one
  clean ring spreads out and dies` never happened: at 11.8s the drop is still
  hanging from the pipette, at 12.25s the clip cuts to the hero frame. Five
  and a half seconds of climax bought a suspended drop and no payoff — the
  build-up is the kind of picture this model is good at, so it made that and
  skipped the fast physical beat. Template A now carries an optional `PAYOFF`
  line under `CLIMAX`, with a slot note and a failure-table row: write the
  payoff as its own timed shot, compress the build-up, and name the result as
  a required visible event.
- **A quantified limit on how much of a body part appears is not a control.**
  `only the fingertips and the first knuckle ever visible` was stated twice,
  in the shot and in AVOID, and the render shows the hand to the knuckles.
  The shot was fine, and what made it fine was the macro framing plus one
  simple action. The framing-order note in Template A now says so, so the
  limit stops reading as a second line of defence.
- **A loudness written per shot is not honoured.** Shot 2 read `room tone,
  nothing else, very quiet` and came back as the loudest sustained passage
  in the clip (about -27 to -24 dB mean against roughly -44 dB in the shot
  before it). The sound *effects* did land where written — the loudest
  transients are the pipette lift at 7-8s and the drop at 10-11s — and the
  close did thin to near silence. So name what each shot contains and leave
  the relative levels to an editor, the way the music already goes on
  afterwards.
- **`no lens flare stars, no sparkle particles` lost**: a small starburst
  glint sits on the drop at about 9.6s. Minor, and now on the record in
  section 6.
- **The weakest shot was the abstract macro**: 2.1 seconds inside amber oil
  came back a near-flat colour field with two refracted bands. The same shot
  into a carbonated drink had rising bubbles to carry it (`7ae7d49e`). A
  liquid macro needs something inside the liquid that moves.

Two corrections to this skill's guidance about its `ofox-image-core`
dependency, which shipped 1.5.0 through 1.7.0 the same day this entry was
written:

- **The generated first frame is no longer cropped by hand.** `60fbea52`'s
  was, in two manual steps (`1792x1024` → `1792x1008` → `1280x720`), because
  no flag existed for it then. `--target-aspect` / `--target-size` now
  measure the written file and crop it exactly, and the image-to-video
  section says to use them — `adaptive` means a wrong-ratio image is charged
  at the price of the clip it opened. "Crop or pad" is now "cropping only,
  never padding", matching the shared reference.
- **The image cost row is quoted from the printed line, not corrected by
  hand.** The paragraph used to say to read `ofox-image-core`'s warning about
  which pair its estimate was anchored at; 1.7.0 made the lookup pair-aware,
  so the line prices the pair being sent or labels itself `ROUGH UPPER
  BOUND`. It also now says to dry-run with the *same* `--target-aspect` the
  real call uses, since that flag decides the `--size` the estimate is priced
  at.

What to do: nothing breaks. A caller writing a CLIMAX whose payoff is a
small, fast event should split it, and should stop relying on a written limb
limit or a written per-shot level. When generating the first frame, pass
`--target-aspect` and relay the estimate line as printed.

## 1.9.0 — a model *and* a locked product, no generated music, and the envelope this scenario measured itself

Docs only; no script changes. Two accepted 720p ad clips (2026-09-04, jobs
`7ae7d49e-7eb9-4165-9d95-09cd525d53ed` and
`ac927785-92ef-4e28-97b9-ff8172ec5554`) plus one unbilled refusal
(`1ff72400-0f30-4be1-a417-f52d43955d09`) between them fix a landmine in
Template A, open a route the skill had documented only as a restriction, and
retire a stale envelope warning.

- **Template A's AUDIO slot was the shape that gets refused.** It read
  `<upbeat | cinematic | minimal> instrumental; percussion hits synced to <the
  climax event>`, copied from gallery cases 12 and 14. Asking this model for
  music failed `output_moderation_failed` with `the output audio may be
  related to copyright restrictions` — not billed — and the same ad with
  recorded sound only passed. The slot is now room tone plus two or three
  diegetic sounds, AVOID names the music words, and "4. No dialogue, no music
  — but a sound block" replaces the old advice to write the music's character.
- **The AUDIO-slot fix above did not originally reach every other place the
  same shape appeared, and this release now closes those too**: the worked
  example (adapted from case 12) still had `AUDIO: upbeat instrumental; the
  downbeat lands on the cut-in and on the snap`, plus a `HOOK` line and a
  `CLOSE` line both keyed to a music beat — exactly the pattern that failed
  on `1ff72400`. It now uses recorded sound only, with a note explaining that
  its audio direction is a deliberate departure from case 12's own scored
  cue, not a translation of it. Template A's `HOOK`/`TRANSITION`/`CLOSE`
  option lists, Template B's compact skeleton, the brief's traceability
  table and the UGC-variant comparison table are updated the same way, so no
  live template in this skill still offers a music-beat option as a thing to
  write into a prompt.
- **New "A model *and* a locked product: the route that works."** "The
  reference frame cannot contain a real person" is not "the video cannot
  contain a real person": the refusal is a check on the attached picture at
  submission, and photoreal people generated from prompt text pass routinely
  (five 20–30s jobs). So attach a frame of the **product alone** and write the
  person into the timeline — measured end to end on `ac927785`, where a
  runner was in frame for seven or eight seconds and the product's colours
  were still identical at t=19.6s. The route locks the product, not the
  person; that limit is stated too. `--real-person true` remains untested on
  2.5.
- **New slot note: order the framing so the risky anatomy stays small.** The
  same job came back with no deformation, and what it did differently was the
  escalation — foot, then hand and lower leg, then knee, then the full figure
  exactly once and that once distant, from behind, head turned away — with
  focus on the product in all seven shots and never on the person.
- **New "5. Text on screen: lock it, or design it out."** Text you want is
  reliable when it exists on the attached frame and the clip only preserves it
  (`7ae7d49e` closed on a legible wordmark in the frame's own typeface). Text
  you don't want is removed by the set: both ads returned zero invented
  signage because neither studio contained a surface lettering could sit on.
- **The four-or-five-beat warning is retired.** The Ofox-measured envelope
  now reaches 20 seconds, 7 shots and 6 hard cuts **with a first frame
  attached** — this scenario's own two jobs did it — so Template A's beats are
  inside what has been run. "Several shots" carries the two-row evidence table
  and names what is still unmeasured.
- Three new failure-table rows (audio-copyright refusal, a refused frame when
  a person is needed, invented signage) and a rewritten cut-count row that
  points at the transition mix rather than the shot count.

## 1.8.0 — a travelling camera option, a transition menu, and the beat count as a floor

Docs only; no script changes. Same review as `seedance-short-drama` 1.8.0,
where a real clip rendered exactly as written and was rejected for being
visually plain. Template A came out of that review in better shape than the
drama template — it already carries slow motion, speed ramps, `low-angle
dolly-in` and an orbit inside its beats — but three gaps were real:

- **The `Camera` question had no travelling option.** Orbit, push-in and
  rack-focus reveal are three ways to move a little around a product that
  stays on a table. A fourth is now offered and the option count is
  unchanged, because the rack-focus reveal folds into the push-in as its
  variant (same picture family: one detail fills the frame): **travelling
  move — the camera goes somewhere and the move *is* the transition**, taken
  from case 13, which plunges down through the gears, passes into a spinning
  brass box and spirals out to a wide inside one 30-second piece that never
  cuts. Pick it when the product sits in a world worth crossing.
- **Template A named no transition kinds.** Its `FORMAT` line said "hard cuts
  on the timestamps" and that was the whole vocabulary. A `TRANSITION` slot
  now sits in the timeline with a hard cut on the downbeat, case 13's
  pass-through, an occlusion (phrasing from cases 2, 8, 41 — none of them
  ads, and labelled as such), case 15's white flash and case 15's extreme
  speed ramp, plus the note that an unnamed boundary becomes a hard cut by
  default.
- **The five beats read as a target instead of a floor.** Counted per case,
  the gallery's ads run 5 shots in 20s (case 15) up to 9 `CUT`s in one
  generation (case 14), with case 26 at seven segments in 30s — so a 30s spot
  written as five 6-second beats is the slowest ad in the set. The template
  now says to split a beat rather than hold one for six seconds, points at
  "Shot density, measured per case" in the shared file for the counts, and
  restates the Ofox-verified envelope (three shots in eight seconds) so a
  denser attempt is priced as an experiment.

## 1.7.0 — creative brief, timestamped ad template, multi-shot inside one job

New:

- **"Before writing the prompt: the creative brief."** Before any prompt is
  written the skill fills a four-axis brief — product photo (must-ask, no
  delegation option), brand tone, hero camera move, aspect ratio — and asks
  only the open axes. The rules that govern that — the three tiers, **one**
  `AskUserQuestion` call of at most four questions with one dependency
  follow-up, "Let the AI decide" always last and never pre-selected, a
  delegated pick resolved to a concrete value marked `(AI's pick)`, the recap
  in the same message as the prompt and the cost table, the generic skip
  rows, the fixed flow (read → brief → ask → prompt → `--dry-run` → recap +
  prompt + table → yes → generate), and the anti-patterns — live once in
  `ofox-video-core/references/creative-brief.md` and are linked, not
  restated. This skill keeps its own question set and its own inference rows
  ("premium" → Luxury, "young" → Playful, "orbit" → slow orbit, "spin" or
  "white background" → out of scope, that is `seedance-product-video`), so
  that **zero questions is a normal outcome**. Resolution is never asked —
  720p and 1080p are two rows in the cost table.
- **"Prompt template."** Template A (15–30s: header manifest, then hook →
  showcase → slow-motion climax → hero close with slogan or logo, 3–5s per
  segment, AUDIO / CONSISTENCY / AVOID blocks), Template B (10s or less,
  three beats, marked as inferred — the gallery has no ad under 20s), a UGC
  variant slot table (cases 24–27), and a worked example adapted from the
  official fruit-biscuit ad (case 12, translated, timestamps added).
  Vocabulary is not restated: the template points at
  `ofox-video-core/references/prompt-structure.md` by section heading.

Behaviour changes a caller may notice:

- **Prompt order is no longer product-first.** All nine gallery ad prompts
  open with a style/format line (or the reference-image anchor) and place
  the product second or third; none leads with the product. Prompts of 15s
  and longer now use a header manifest (FORMAT → STYLE → CHARACTER → PRODUCT
  → SCENE → timeline → CAMERA → AUDIO → CONSISTENCY / AVOID); 10s and
  shorter follow the vendor's subject-first formula. The file says plainly
  that there is no A/B evidence for either order, only no case for the old
  one.
- **Several shots inside one job are now the documented route for cuts.**
  Verified on Ofox 2026-09-03 (two three-shot prompts, `seedance-2.5`,
  `byteplus`, 8s, 480p, 16:9, no audio, pure text-to-video with no image
  attached — both cut within about one second of the written timestamps).
  Not covered by those runs: more than three shots, clips longer than 8s,
  an attached reference image, cuts with dialogue, other resolutions,
  `volcengine`. Template A's own four or five beats are therefore flagged
  as beyond the tested count. "Multi-shot ad sequences" is replaced by
  "Several shots: timestamps inside one job, `chain` across jobs" — `chain`
  is for sequences past the 30s ceiling or shots that need their own
  approval, seed or resolution, not for every cut.
- **Duration default stays at 10s but is now flagged as a draft length**:
  every gallery ad with a stated length runs 20–30s. When the user gives no
  duration the recap says so and offers 15–20s as a row.
- **The product-photo section names both image semantics.**
  `--frame-first-image` (first frame, verified) and identity references via
  `--extra-json '{"input_references":[…]}'` (up to 9 images, element shape
  from `api-params.md`, not run end to end here), and states that the two
  are mutually exclusive (`references_conflict`). New failure-table rows for
  `references_conflict`, `input_moderation_failed` and "the clip did not cut
  where written".
- **Real-person reference frames**: the section now says Seedance 2.5
  image-to-video refuses them at submission and that `--real-person true`
  is untested on 2.5; the recommended route is a text-described person with
  the product locked to the image. The UGC variant table repeats this for
  creator-style clips.
- `description` now mentions the brief and the timestamped shape; triggers
  are unchanged.

What to do: nothing breaks. Agents that previously jumped from request to
`--dry-run` should now fill the brief first and expect to ask 0–3 questions
before quoting. Callers who copied the old product-first example still get a
valid prompt; the new order is what the collected ads look like.

## 1.6.0 — link the shared approval gate instead of restating it

- "Cost: quote it, get a yes, then spend it" and "Before you spend: show the
  prompt, not just the price" are replaced by one section that links
  [`ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md),
  the spec now shared by every Ofox skill in this repo. Both sections were
  right; keeping four private copies of them was the problem.
- What stays here is scenario-specific: dry-run both a 720p draft and a 1080p
  deliverable when that choice is still open, so the difference is a row in
  the table rather than a sentence.
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

## 1.2.0 — multi-shot ad sequences

Documents `ofox-video-core` 1.6.0's `chain` for beat sequences (establishing →
push-in → hero) that would otherwise cut between unrelated renders. Works for
product and environment shots; a sequence built around a photoreal human model
cannot be chained, since Seedance 2.5 refuses real-person reference frames.

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

## 1.0.4 — ClawHub frontmatter

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
