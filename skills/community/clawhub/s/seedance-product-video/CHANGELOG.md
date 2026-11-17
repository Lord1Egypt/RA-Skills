# Changelog

All notable changes to the **seedance-product-video** skill. Versioning follows SemVer.

## 2.0.0 — every real-run command carries `--approved`, and the core refuses without it

**Breaking, and the break is upstream.** `ofox-video-core` 2.0.0 makes its
four billable subcommands — `generate`, `create`, `batch`, `chain` — refuse to
run unless `--approved` is on the command line. All four of this skill's
real-run commands — three `generate` and one `chain` — now pass it. The
`--dry-run` commands are untouched: a quote is how the number being approved
gets produced, so gating it would close the only route through itself.

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
  its real run takes `--approved` in the same place. A `chain` commits every
  shot at once, so quoting it first matters more there than anywhere else.

**What `--approved` is not.** It does not prove that an approval happened — an
agent can type it without showing anyone a price, exactly as it could
previously just run the command. What changed is that spending without quoting
is no longer the default: it now has to be written into the command, where a
transcript shows it and a reviewer can object. The gate in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md)
is still the rule, and this skill still states it in full.

**Documentation only otherwise. No price, default, prompt template, flag
meaning or generation behaviour changed.**

This file starts at 1.0.2; earlier versions predate it.

## 1.17.2 — the recovery command asked for the whole repo, and asked the agent to run it

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

## 1.17.1 — the "no hosting needed" note needed its other half

**Documentation only. No flag, default, price or prompt template changed.**
One cell of the identity-reference row.

1.17.0 added that an image reference accepts a `data:` URI so a local file
needs no hosting. True, and dangerous on its own: a `data:` URI built into
`--extra-json` is bounded by `ARG_MAX`, and over the limit **the reference is
dropped silently and the job is submitted and billed as plain text-to-video**
(measured 2026-09-17, exit `0`, no `input_references` in the payload). The row
now carries that caveat and points at the reproduction and the guard in
`ofox-video-core`'s `references/api-params.md`.

## 1.17.0 — the headline route was finally run, and the 5-second template failed it

**Documentation only. No flag, default, price or command changed** — but one
piece of **planning guidance is new and it forbids something the template used
to permit**, so read the first bullet before writing another short clip.

Until 2026-09-17 every clip this file was built on was **pure text-to-video
with a fictional product**, while the skill's own description leads with
turning a **real product photo** into listing footage. Job
`54a721ce-61a1-46cf-b5bf-6973f31b8258` (5s, 480p, 16:9, a real photograph as
`--frame-first-image`, 55 cents) closed that gap, and the result is split.

**What a caller has to do differently:**

- 🚨 **At 5 seconds, never put DETAIL in the same clip as TURNTABLE or ORBIT.**
  "Scale the segments, don't copy the stamps" told you to scale the
  timestamps. Measured: **scaling a timestamp does not scale the camera
  move.** A one-second DETAIL pushed all the way to a cap macro anyway, and
  the three turntable seconds after it happened inside that macro — the clip
  never returned to the whole product and is not deliverable as a listing
  showcase. A short clip is **one** move. If the user wants a detail and a
  rotation, that is a longer clip or two clips, and both go in the cost table
  as rows. Where the boundary sits between 5s (one move) and 12s (four
  segments, three clips) is **not measured** — quote 8 or 10 as an experiment.
- **Do not describe the turntable as measured on the photo path.** It is not.
  `54a721ce` never framed its rotation wide enough to read, so the only
  turntable evidence is still the text-to-video run `dc02f604`. The clip that
  would settle it has **no DETAIL segment in it**.

**Separately, the identity-reference row is no longer "never run".** It said
*"no image-reference job has been run end to end in this repo"* and that
whether the `image1` tokens resolve by position was unverified. Both were
closed on 2026-09-16 (`ofox-video-core`, job `0f5c8b4e`, two `image_url`
references, 44 cents): the features came through and **the tokens resolve in
array order**. It bills at the plain t2v rate and accepts a `data:` URI, so a
local file needs no hosting — but ⚠️ pass `--aspect-ratio` explicitly, because
the measured job passed none and came back portrait from landscape
references.

**What it confirmed, and it is worth as much as the failure:**

- **The photo anchor works.** Frame 0 is the attached photograph — whole
  product, white background, wordmark legible. Everything this file says about
  attaching a photo for a real SKU held on its first real outing.
- **The white-surface SCENE convention is doing more work than anyone knew.**
  There is no cut at the top of that clip, and that is causal: measured
  elsewhere the same day, a supplied first frame whose background **disagrees**
  with the written SCENE yields about 0.1s of the photo and then a hard cut
  (`ofox-video-core` 1.28.0). Writing the SCENE as the surface the photo was
  actually shot on is what keeps this skill out of that trap. Keep doing it.

## 1.16.1 — the real-person flag is measured; two rows and a paragraph said otherwise

**Documentation only. No default, price, prompt template or behaviour
changed.**

The "Two ways to attach the photo" paragraph, the defaults table's
`--real-person` row and the `input_moderation_failed` troubleshooting row all
said it was untested whether `--real-person true` lifts Seedance 2.5's
refusal. It was measured lifting it on 2026-09-16, and all three now say so —
while saying what the flag actually is: Ofox's privacy-preserving
preprocessing path for **authorised** real-person references, an
authorisation route rather than a way past the check, offered only when the
user holds the right to that likeness and never set on their behalf. The
evidence and every limit on it are linked to `ofox-video-core`'s
`references/api-params.md` rather than restated here.

**The recommendation is unchanged, and that is the point.** For a product
video the thing that has to be exactly right is the object: attach a photo of
the product alone and write any person into the prompt text. The
troubleshooting row in particular now warns *against* reaching for the flag as
a retry — a refusal is a question about rights, not an error to route around.

## 1.16.0 — the turntable has been run: it works, and its speed does not listen

1.15.2 added a warning to the one skip row that pointed at an option nobody
had ever run. That option has now been run, so the warning changes shape: it
is no longer "this is untested", it is "this works and here is the one thing
it will not do".

**Job `dc02f604-6c83-4837-b7fb-88e8df1876fb`**, 2026-09-16, seed `88995356`,
`bytedance/seedance-2.5` on `byteplus`, **5 seconds at 480p, 1:1**,
`--generate-audio false`, **text-to-video with no product photo**, billed
**55 cents**. Subject: a matte black travel mug with a brushed steel band and
a small logo plate — the plate chosen deliberately as the asymmetric feature
that makes a rotation readable at all.

**It works.** The logo plate tracks from a sliver at the left edge (0.1s), to
fully face-on in the centre (3.2s, the small lettering on the steel band
coming round with it), to heading off toward the right edge (4.8s). The mug's
position, scale, contact shadow, background and framing are unchanged from the
first frame to the last. So the camera really was fixed and the product really
did turn on its own vertical axis, without tipping, sliding or floating —
which is the whole of what this option promises.

**And the rate does not listen.** The prompt asked for "most of one turn";
five seconds delivered roughly **a quarter to a third**. That is not a new
surprise, and the file is careful to say so: it is the same grammar as `a full
360 degrees` producing about half a turn on both measured camera orbits, and
of the hinge whose material and geometry landed while its knuckle count did
not. The description renders; the quantity attached to it does not.

**The practical calibration, which is what a user needs: a full 360 does not
fit in 5 seconds.** Somebody asking for "a 360-degree showcase" is asking for
the thing this run did not deliver, so the brief now says to correct that
before the cost table and offer the choice — more seconds, or accepting that
the clip shows part of the surface. **No seconds-per-turn figure is quoted**,
deliberately: one run at one duration cannot support one, and inventing a
helpful-sounding number would repeat the prompt's own mistake.

Changed, five places: the `Motion` question's turntable option, the skip row
for spin / turntable / rotate / 360-on-its-axis, the full template's TURNTABLE
slot, the compact template's turntable swap, and the defaults table's Motion
row. The template sentences now carry the phrasing that ran — axis, constant
speed, fixed camera, stays in place, never tips — and **no degree count**,
because the one that was written did not arrive and only set an expectation.
Two rows were added to the failure table: the short turn, and how to tell a
turntable from an orbit by reading three frames.

**The bound that matters most here is the route.** One run, 5 seconds, and
**text-to-video with no product photo** — which is not this skill's main path.
A real SKU goes image-to-video, where an attached first frame fixes the
product's appearance and the clip's shape, and whether a turntable behaves the
same way with a frame attached is **untested**. So is any longer duration.
Both are stated where the option is chosen, not only where it is documented.

No prompt craft for the orbit, no default, no price and no routing moved.

## 1.15.2 — routing: stills now have skills of their own, and one skip row admits it is untested

No prompt change, no defaults change, no new measurement, no mapping changed.
One bullet added to "When NOT to use", because two image scenario skills
shipped on 2026-09-15 and this file's routing pre-dates them.

`product-image` owns a set of product stills to choose between — each one an
edit of the same product photo, priced as a set total — and `image-edit` owns
a single change to a single picture. Both are cents where this skill is
dollars, so an agent that reaches for a video generation because a request
merely mentioned a product photo has made an expensive misread, and nothing in
this file previously said so.

The bullet is deliberately two-sided. The two kinds of job are complementary:
stills first and a clip afterwards is a normal sequence, just two jobs with two
cost tables. And a still generated as **this skill's own first frame** stays
here, because an attached image forces the clip's ratio to follow it and that
decision belongs where the video is priced.

**Also: one skip row now carries a caveat it always should have.** Surfaced
while checking the routing above, and pre-dating it. The row mapping "spin",
"turntable", "rotate", "360 on its axis" to **product turntable, camera
fixed** is the only skip row that lands on the *untested* motion option — this
file has said since 1.6.0 that the fixed-camera phrasing has no gallery source
and has never been run here, and that the measured default is the camera
orbit. The caveat lived 200 lines away from the mapping, so an agent following
the skip table picked the untested route without ever being told.

**The mapping is unchanged** — a user who says "turntable" gets a turntable,
because they named it. What changed is that the row now says to tell them, in
the same breath, that the orbit is the option with evidence behind it. No
prompt, default or price moved.

## 1.15.1 — a seed does not reproduce a take, and this skill said it did

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

Also corrected here: the section stating "the seed reproduces a take only
while the prompt is byte-identical", which made the same inverted claim in
this skill's own words, against this scenario's own grinder pair. The pair's
finding stands — one edited paragraph moved the product's appearance — it just
establishes necessity, not sufficiency. A product clip is where a client
notices a promotion that came back different, so the section now says to price
and describe it as another roll.

## 1.15.0 — two defaults did not survive naming another model

1.14.0 let a user say "use wan" / "use hailuo". Two entries in the defaults
table were written when `seedance-2.5` was the only option:

- **`--resolution 720p` does not exist on `minimax/hailuo-3`**, which offers
  `768p` and `2k` only — so *both* rows of this skill's cost table move there
  (`768p` for the listing clip, `2k` for the higher tier; it has no `1080p`
  either). The script rejects `720p` on that model locally, before submitting,
  at no cost, but a cost table quoting a tier the model doesn't have is wrong
  before that point. The defaults row and a new "What changes when the model
  changes" section carry the right tiers.
- **The attached photo's shape.** "With a photo attached the flag is not sent"
  held because `seedance-2.5` overrides it. On another model nothing overrode
  it and no `aspect_ratio` was sent at all, so the clip could come out in a
  shape the photo never had — after it was paid for. `ofox-video-core` 1.22.0
  fixes that in the tool: `adaptive` is forced on `seedance-2.5` and applied as
  the default on a model that offers it when no `--aspect-ratio` was passed.
  The `--aspect-ratio` row now says which mechanism applies where; the advice
  is unchanged — don't pass the flag on the photo route — and cropping or
  padding the photo to the brief's ratio first is still what decides the
  output's shape.

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

## 1.14.1 — find the core skill instead of assuming its directory name

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

## 1.14.0 — a real choice of video model, not just a locked-in default

Docs only; no script changes — `--model` already accepted all three models
named below. Until now `model` sat in the never-ask row with the copy
"script default, no flag needed", which reads as if `bytedance/seedance-2.5`
were the only option. An explicit user request ("turn this into a listing
video with wan") had no documented vocabulary in this file to map that word
onto a real model id.

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
  clearance for either model. Noted as least relevant to this scenario's own
  usual clips (inanimate products, no person in frame) and most relevant to
  the out-of-scope presenter case.
- **`hailuo-3`'s 15s duration cap flagged against this skill's own
  durations**: it lands exactly at the segmented template's ceiling and
  below the out-of-scope presenter clip's 30s.
- **The never-ask row and the `--model` row now say the same thing**:
  never-ask means the agent doesn't raise the question itself, not that an
  explicit user choice gets overridden. A model named by id or by a
  recognizable shorthand ("wan", "hailuo") is used instead of the
  `seedance-2.5` default — never silently substituted back.

What a caller can do now that they could not before: say "use wan for this
listing video" or "try hailuo" and have the agent actually pass that model,
instead of it defaulting back to Seedance 2.5 with no vocabulary to do
otherwise.

## 1.13.0 — the per-waypoint shot size, downgraded from verified to once-held-once-failed

**Docs only, and the run that forced it is not this skill's.** 1.11.0 wrote
up `a shot size on every waypoint` as a verified repair for a segment
inheriting the previous one's framing, on the strength of clip C
(`8efeb556`, the eyeglasses) holding the whole product in frame through an
orbit that deliberately kept the risky DETAIL-macro-then-ORBIT order. A
`seedance-ad-creative` clip has since done the same thing and failed, so
every place this file asserted the repair now says what it actually is.

- ⚠️ **Job `cb6b7870-22f7-4a15-9168-8a013805775f`** (2026-09-07, 15s, 720p,
  **i2v** with a generated first frame, rejected) has the identical shape: a
  macro beat immediately before a waypoint orbit, a shot size on all three
  waypoints (`a medium shot ... the whole bottle from cap to base inside the
  frame with margin above and below`), and a closing `the bottle stays fully
  in frame at every moment of the move`. Six frames across that move are all
  a close shot of the bottle's upper body, base never in frame. So: **once
  held, once failed**, with the differences unexamined — i2v with a paid
  macro first frame against t2v, a tall cylinder against a folded pair of
  glasses.
- **What changed in this file.** §3's `That fix has now been run, and it
  works` becomes `run twice: it worked once and failed once`; the ORBIT slot
  note in the full template, the Motion row in `Recommended defaults`, and
  the `orbit travels but the base is out of frame` row in the failure table
  all carry the same correction. **Keep writing the shot size** — omitting it
  is measured to be worse and it voided a whole waypoint on clip B — and then
  read a draft's frames rather than trusting the prompt.
- ✅ **One thing gained, and it is directly usable here: put a widening view
  after a cut.** The failing clip's two post-cut shot sizes were both
  delivered, the last holding the whole product cap to base with margin.
  Together with clip D's existing hedge — where three framings landed but
  their boundaries had rendered as cuts — that makes three clips agreeing
  that a shot size stated across a cut is far more reliable than one stated
  inside a continuous move. Clip D's bullet now says to read it as evidence
  for the post-cut case only.
- **The failure half of the finding is unaffected and is now measured
  twice.** An unstated shot size inherits the previous segment's framing, and
  it can silently delete a waypoint's content — clip B, plus the new clip's
  SHOWCASE. It is the *repair* half that is one-for-two.

No change to templates, flags, defaults or the scenario boundary. The
repo-wide record lives in `ofox-video-core` 1.20.0's `A camera move needs its
waypoint frames, not just a verb`, not here.

## 1.12.2 — the key requirement, moved to the front of a description that gets truncated

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

## 1.12.1 — two Chinese fragments in a shipped file, rendered in English

Docs only; no script changes, no advice changed. Clip D's write-up (added in
1.12.0) quoted two clauses from that clip's Chinese prompt verbatim, in a file
that ships: a boundary marker and one `AVOID` item. `CONTRIBUTING.md` is
English-only for anything shipped, and every other Chinese-language quotation
in this repo is given in translation. Both now read as English — `hard cut`
and `no ... hang tag` — with a line above them saying the prompt was Chinese
and that clauses from it are translated. Nothing a caller does changes.

## 1.12.0 — one clip run outside this skill's own boundary: a presenter on camera, and what it moved

Docs only; no script changes. Clip D —
`e378f058-f224-4450-94b4-798840ad139b`, 2026-09-06, seed `561877558`,
`bytedance/seedance-2.5` on `byteplus`, **image-to-video** with a generated
product-only first frame, 30s, 720p, `aspect_ratio: adaptive` (forced by the
attached image), **audio left on**, billed **7.20 USD**, plus **0.154615 USD**
for the first frame on `openai/gpt-image-2` — **7.354615 USD** total. Accepted
by the repo owner. `n: 1012` in the gallery.

**Read this first.** The clip breaks this skill's own `description`, which
ends `Do not use for ... anything involving people/dialogue`, and it breaks a
second rule too — a fictional product is supposed to go text-only rather than
generate-a-reference-then-animate. Both exclusions are **unchanged**, no new
skill was created, and whether presenter-led commerce video deserves a
scenario of its own is undecided. It is recorded because its findings bear on
the templates here.

### Added — a new section, "One clip outside this skill's own boundary: a presenter on camera"

- **The first-frame lock survives the product being worn.** Every earlier
  frame-lock result in this repo had the product sitting still; the sneaker
  clip had a model beside the product, never wearing it. Clothing is the most
  deformable category there is, so this was the predicted risk of the whole
  run. Six discrete features enumerated in advance — the two-tone colour
  split, the centre zip and its orange pull, the pocket set, the hood and its
  drawcords, the cuff tabs, the blank sleeve patch — **all six held** across
  hanger, body, outdoor and studio. Stated as **one clip**, with the hedges:
  no control, cuff tabs unreadable in the backlit outdoor segment, and the
  garment's **loft** drifted (it reads thicker than the attached shell), which
  is a continuous property the six discrete features do not cover.
- **"Product-only first frame, person written in text" has a second data
  point**, and this one has the generated person **pick the product up and
  wear it** rather than merely share a frame with it. No
  `input_moderation_failed`; `--real-person` not passed and not needed.
- **A shot size on every waypoint, a third time** — with the hedge that clip
  D's boundaries rendered as cuts, so the framings are partly delivered by
  cutting rather than by resisting inheritance inside one move.
- **Nine hard cuts and ten shots in one job**, all confirmed by reading frames
  — a new maximum for this repo, previously 6 hard cuts, and done with an
  image attached, dialogue on the track and two locations.
- **All nine timestamped boundaries became hard cuts, including the six that
  never said so** — a 6-for-6 confirmation of the shared file's rule. One of
  those six was written as a camera verb and delivered a cut, so a bare camera
  verb neither produces a move nor prevents one.
- Timestamps: eight of nine within 0.5s, the outlier 1.29s early. **Eight land
  early, one (the 2s cut, delivered at exactly 2.000) lands on its stamp, none
  lands late** — noted as a shape, not a rule.

### Added — the failures, recorded as failures

- **The zero-fake-text construction has a boundary.** Its per-part list named
  only **outer** surfaces, and when the lining came on camera it carried a
  neck brand label, a small tab and a care/spec panel. At 12x none resolves
  into readable letters, so there is **no readable fake text** — but three
  carriers `AVOID` had named outright. **Zero fake text is half-held, not
  held.** The repair (extend the declaration to lining, inner collar and
  pocket interiors; name interior carriers in AVOID) is **inferred from the
  defect and has not been run**.
- **A prohibition pinned to a second is only as reliable as the cut.** `No
  person before 8s` was broken at 6.708s because that cut landed 1.29s early.
  Move the thing to a later segment rather than writing the prohibition
  harder.
- **"Completely still" delivered a settle**: 23 of 54 final frames cross
  0.0005, **zero** cross 0.005, framing identical at 28.0s and 29.9s. The
  camera did not move; a living subject breathes.
- **A style clause could not be separated from its own scene** — `no cinematic
  colour grading` against a dawn-ridge-under-low-cloud location that supplies
  that light by itself. Recorded as a deviation, not a violation.
- **Detector blind spot, eighth time in this repo and fourth in a row in this
  scenario — and the first one outdoors.** The 20.958s boundary needs 0.15.
  Four clips have now needed 0.05 / 0.10 / 0.10 / 0.15. Lowering the default
  is still not the fix, and the blind spot is not a studio artefact.

### Changed — existing sections that this clip refines

- "Measured on this scenario's own clips": the zero-fake-text bullet, the
  `--generate-audio false` bullet and the detector bullet each gained a
  pointer to where clip D moved them.
- The full template's "Printed text goes in quotes" slot note now carries the
  interior-surface rule.
- The defaults table: `--duration` notes the 30s exception; `--generate-audio`
  notes that a spoken clip drops the flag rather than setting it to `true`.
- "Several shots": the hard-cut ceiling moves from 6 to 9, and the
  timestamp-is-a-cut rule gains its 6-for-6 confirmation.
- "A product photo": a note on what generating a reference for a *fictional*
  product bought and cost. **The rule for a real SKU is untouched.**
- "When NOT to use": the people/dialogue exclusion is restated as standing,
  with a pointer to the one clip run against it and why that is not permission.
- Failure-modes table: two new rows — interior labels despite an AVOID list,
  and a second-pinned prohibition broken by a cut landing early.

### Not verified — stated as such

**The audio content was not checked by this skill.** Only the track's
existence was measured (aac 32000 Hz stereo, 130074 bps, 940 frames). Whether
the four Chinese lines are accurate, whether lip sync lands, and whether the
ambience is layered per segment were all judged by the repo owner on playback
— that is his judgement, not a measurement here. Frame checking was a 1fps
overview plus both sides of all nine boundaries plus six full frames plus
three high-magnification crops; **not an exhaustive scan**.

## 1.11.0 — a third clip made to test two fixes: one works, one half works, and the orbit stops half way round

Docs only; no script changes. Clip C —
`8efeb556-bf38-45ec-940b-a792ef74bfcf`, 2026-09-06, seed `616202922`,
`bytedance/seedance-2.5` on `byteplus`, pure text-to-video with no image,
12s, 720p, `--aspect-ratio 16:9`, `--generate-audio false`, billed 2.88 USD,
gallery case `n: 1011`, accepted — is not a third look at the same thing. It
is an **independent** run on a different product (a fictional pair of folded
eyeglasses) at a different seed, written for one purpose: to test the two
fixes 1.10.1 recorded as *aimed at an observed cause and not yet re-run*. One
is verified, one is half verified, and a finding that was unmeasurable is now
measured.

- **The per-waypoint shot size is verified.** 1.10.1 proposed it; the failure
  table and §3 now say it has been run. Clip C states a shot size on all
  three waypoints, closes the paragraph with `at every one of those views the
  entire pair of glasses is inside the frame, nothing cropped`, and
  **deliberately keeps the DETAIL-macro-immediately-before-ORBIT ordering**
  that caused clip B's inheritance in the first place — so the defect had
  every chance to recur. Every frame of the move holds the whole product with
  margin, where the grinder's base was outside the frame for its entire
  orbit. **One confirming run, with the causal ordering preserved**, which is
  what makes it a verification rather than a second observation. The
  corollary — a segment inherits the previous segment's framing unless told
  otherwise — now has both halves, the failure and the repair.
- **The accessory wording is half repaired.** `beside` had been recorded as a
  stable reading meaning "on either side of", deliberately not fixed. Clip C
  wrote `to the right of the glasses and only to the right ... Nothing lies to
  the left of the glasses and nothing lies above or below that line`. The
  **left/right constraint held** — nothing on the left, which neither grinder
  clip managed — and the **single-line constraint did not**: the cloth sits
  forward of and below the case. So the rule is now: **the left/right axis is
  controllable by explicit wording, placement in depth is not.** One run each
  way, and on **two** accessories rather than the template's three. The
  ACCESSORIES slot, its note, the worked example and a new failure row all
  carry the wording that worked with the depth limitation beside it.
- **⚠️ The written return to the opening view is withdrawn — it does not
  bring the camera home, and 1.10.x read one clip as saying it did.** Clip C's
  orbit is one continuous shot and its subject carries an unambiguous
  asymmetric feature (two folded temples), so azimuth is readable at every
  frame: front at 6.0s → side at 7.5s → rear at about 9.6s. The move stopped
  at the rear, and the named front view came back only after the cut into
  ACCESSORIES. Clip B's landing on that frame is therefore a coincidence of
  its move having begun, unasked, at the rear — **one coincidence and one
  plain failure, which is no evidence at all.** The closing return line is
  gone from the template's ORBIT slot, from the copyable waypoint block and
  from the worked example; if the clip has to end on the opening view, that
  view is the next segment, after the cut.
- **About half a turn is measured, not inferred.** Two clips, different
  products, different seeds, different prompts, agree on roughly 180 degrees,
  and clip C reads it frame by frame inside one continuous shot rather than
  from two endpoints. Write an orbit expecting half a turn and pick the two
  interior views accordingly. Clip B's own total **stays unmeasurable** — that
  was a fact about that clip and no later run changes it, which is also why
  `ofox-video-core`'s `Measuring a camera's travel: only inside one continuous
  shot` is *validated* by clip C rather than replaced: it predicted exactly
  which conditions would make a rotation readable.
- **Interior timing, first attributable run.** Clip C's waypoints are distinct
  pictures that do not contradict themselves, so §4 can finally say which was
  late: the side on time, the rear about 0.6s late, the return never. Two
  interior pictures written, two rendered — the first run to hit §4's own
  budget exactly, losing only the ending, which is why §4 now also says not to
  put the view that matters most at the end of a move.
- **A description is honoured; a number attached to it is not** — a new
  finding, and the one that constrains the shot-size result above. Clip C's
  hinge landed qualitatively and completely (a barrel hinge, interleaved,
  acetate edge one side and the flat brushed temple bar the other, unchanged
  through the macro push-in and the whole orbit) and **missed the count**:
  three interleaved knuckles were written, and 5x magnification shows four
  knuckle blocks plus a screw head top and bottom. It pairs with
  `seedance-ad-creative`'s `60fbea52`, where a limb limit written twice was
  ignored, and with two findings already in this skill — three interior
  waypoints written and two rendered, and `a full 360 degrees` producing no
  measurable total. **What it does not undercut**: the instruction that fixed
  the framing is a *spatial description*, not a count, which is why it landed
  where the knuckle count did not — so "write it down and you get it" holds
  for looks and framing and stops at countable parts. The general form went
  to the shared file as `A description is honoured; a number attached to it is
  not`; this skill carries a PRODUCT-slot note and a failure row.
- **Three confirmations added, not new claims**: zero invented text on a
  harder set than the pair's (acetate, titanium, clear lenses, a **hard case
  lid** — the classic wordmark carrier — where a 5x zoom shows a specular
  highlight and no lettering), with the PRODUCT-block no-text clause plus a
  per-carrier AVOID and **no first frame** to anchor anything; thin protruding
  parts holding for the third time (two slim temples, no third temple, after
  the crank arm twice); and the duration budget holding again at
  2.67/3.04/**4.00**/2.33 against a written 3/3/4/2. The lenses also stayed
  clear and never mirrored, and the temples never unfolded.
- **The final frame holds completely on clip C, and the earlier stillness
  figures were an artefact.** Measured without an `-ss` pre-seek — which gives
  the first post-seek frame no predecessor to diff against, so it scores as a
  change — clip C has **zero** frames above a 0.0005 scene score after
  11.541667s, with the last change anywhere in the clip at 11.375s, so the
  hold runs about 0.67s. Clip B measured the same way is **seven** frames, not
  the six recorded in 1.10.1. The conclusion is unchanged and firmer: two of
  three held, and the two that differ are the same-seed pair.
- **The orbit is not described as even or constant-speed anywhere.** What the
  frames support is that the azimuth advances monotonically with no dead
  stretch; a per-half-second scene-delta reading is not a clean
  angular-velocity proxy on this subject, since near the front view the same
  rotation moves the picture much less. Whether the prompt's `constant speed`
  landed is left unstated in both directions.
- **The same-lighting detector blind spot, third consecutive clip.** At
  threshold 0.25 only 2.67s and 5.71s appear; the third cut at **9.71s**
  needs **0.10**, where clip A needed 0.05 and clip B 0.10. Three
  after-the-fact discoveries against a default wrong for all three, so
  **lowering the default is not the fix** — how far to lower it is only
  knowable once the frames have been read.
- **`--aspect-ratio 16:9` → exactly 1280x720, `--generate-audio false` → no
  audio stream at all**, third time each. And the poll survived the same
  `SSL_ERROR_SYSCALL` transport fault the pair did, retrying the **poll, not
  the create** — third consecutive clip, recorded in `ofox-video-core`.

Nothing here widens an untested edge: the turntable phrasing is still a
*product* verb rather than a camera one and remains unmeasured, and no run in
this repo has shown a written 360 performed.

## 1.10.1 — the orbit arrived; it did not demonstrably go round, and 1.10.0 said it did

Docs only; no script changes. **This entry corrects 1.10.0, which is
unreleased alongside it — read the two together rather than as an addition,
because the wrong reading here is the intuitive one and a future reader is
likely to re-derive it.** What 1.10.0 got right is the finding this skill's
`Motion` default now rests on: `the camera orbits the grinder a full 360
degrees` produced no movement at all, and the same prompt at the same seed
with the angles written out as pictures produced a camera that moved and
ended on the front view it named. What it got wrong is how far that camera
travelled — recorded as a clean monotonic full circuit, when the clip cannot
support any total at all.

- **The corrected reading, and the reason two earlier ones failed.** ⚠️
  **Superseded in part by 1.11.0: the orbit did not "arrive" either.** An
  independent clip covers the same half turn and stops at the rear, so this
  clip's ending on the named front view is a coincidence of where its move
  began — and the ~180 degrees is now a measurement rather than an
  observation, taken on that other clip. The front
  view is fixed by the frame at 2.8s (knob at the left, crank arm extending
  cleanly sideways). Inside the continuous ORBIT segment — the hard cut at
  6.291667s to about 10s — the frames read the rear through 6.40–8.40s, a
  side at about 8.80–9.00s, and the front again from 9.60s. So: **the segment
  ends on the opening orientation**, the **observable travel is about 180
  degrees**, and the **total is unmeasurable**, because the written path's
  other half could only have happened across that hard cut and the shot
  before it is DETAIL's macro of the knurled ring — rotationally
  near-symmetric, carrying no orientation cue. An earlier draft read the
  segment's own first frame as the front and reported 180 degrees with no
  return; 1.10.0 read across the cut and reported the full circuit. Neither
  pair of endpoints was connected by continuous motion. §3 now states the two
  claims and the limitation, and says plainly that this skill claimed the
  circuit once.
- **The general rule went to the shared file, not here**, as
  `Measuring a camera's travel: only inside one continuous shot` in
  `ofox-video-core/references/prompt-structure.md` — it is about checking any
  clip, not about catalog footage, and it sits next to the existing
  read-the-frames-not-the-detector guidance because it is the same class of
  mistake.
- **The near-stationary stretch is six sampled frames, not five** — 6.40,
  6.80, 7.20, 7.60, 8.00 and 8.40, with 8.80 the transition, so roughly 2
  seconds held and the rest of the move in about 1.2. §4 and the failure table
  are corrected.
- **The framing defect voided half a waypoint, which §3 now says.** *(The
  fix proposed for it — a shot size on every waypoint — was verified in
  1.11.0 on a clip that kept the same ordering on purpose.)* The 7s
  waypoint asked for the knurled ring seen edge-on, and that ring was outside
  the inherited macro framing for the entire orbit — so an unspecified shot
  size did not merely crop the picture, it deleted part of what a waypoint
  asked for, and the missing beat looks like the model ignoring a waypoint
  when the prompt had already made it impossible.
- **The scene detector missed a real cut in *both* clips, not just the
  rejected one** — clip A at **9.750s** (visible only at threshold 0.05) and
  clip B at **10.041667s** (needs 0.10), neither at the 0.25 both were checked
  at. These are the fifth and sixth confirmations of the same-lighting blind
  spot in this repo and its strongest form, since a controlled pair needed two
  *different* lower thresholds and no single number would have caught both. It
  also weakens one of 1.10.0's own claims, now hedged: `no cut anywhere inside
  this segment` was **not contradicted** rather than verified, because the
  pass that reported nothing inside the orbit is the same pass that missed
  that segment's closing boundary.
- **Two instruction readings recorded, both stable across the pair.**
  `hold the final frame` held in clip A (every frame of its last half second
  under a 0.0005 scene score) and drifted in clip B (six frames above 0.0005,
  one above 0.002 — ⚠️ **re-measured in 1.11.0 as seven above 0.0005**; the
  earlier count came from an `-ss` pre-seek that scores its first frame as a
  change) — so ask for it and expect a settle. And `in a row on the
  grey surface beside the standing grinder` put the accessories on **both
  sides** of the grinder in both clips: identical in the pair, so a stable
  reading of `beside` rather than a roll, which makes it plannable — name the
  side and say the product is not between any two items if the row has to
  stay together. *(1.11.0 ran that: naming the side works, `both on the same
  line` does not.)* 1.10.0's ACCESSORIES row read as if the slot rendered exactly
  as written; the items did, the placement did not.
- **The gallery case number is `n: 1009`, not `n: 1008`.** Another session
  committed 1008 to a different clip while this work was in progress, and `n`
  is append-only, so the uncommitted case moved rather than the committed one.
  Corrected in `SKILL.md` and in 1.10.0's own entry above.

Every hedge 1.10.0 carried survives — it is still two runs, the turntable
phrasing is still unmeasured, and nothing here widens a claim.

## 1.10.0 — an orbit that never happened, and the one paragraph that fixed it

Docs only; no script changes. Until now this skill had generated nothing of
its own — every figure in it came from the gallery, from
`seedance-ad-creative`'s product jobs, or from `ofox-video-core`'s two
three-shot test runs. It now has two 12-second 720p clips of a fictional hand
coffee grinder, `bytedance/seedance-2.5` on `byteplus`, **pure text-to-video
with no image attached**, `--aspect-ratio 16:9`, `--generate-audio false`,
2.88 USD each. They are a controlled pair: **the same seed (`642303335`), the
same model, the same flags, and the same prompt text except the ORBIT
paragraph.** The first was rejected, the second accepted on 2026-09-05 and is
the gallery's first `ofox`-sourced case in the `product-video` category
(`n: 1009` — this entry originally said 1008; see 1.10.1). Versions in force
when they ran: this skill 1.8.0, `ofox-video-core` 1.15.0.

- **`the camera orbits the grinder a full 360 degrees at constant height and
  constant speed` produced no orbit at all.** Job
  `1cf5ac46-058f-4615-a47b-067743f76f8c`: from 6.0s to about 9.7s a
  near-static front view with a slight push-in, the crank arm pointing right
  in every frame — 3.7 of 12 seconds, the core segment of a catalog clip,
  delivering no new angle. Note which half of that sentence was obeyed: the
  product genuinely did not rotate, and the camera genuinely did not travel.
- **The same prompt at the same seed, with that one paragraph rewritten as
  timestamped waypoint pictures, travelled the whole circuit.** *(The extent
  claimed in this bullet — the circuit, and the degree readings below it — is
  corrected in 1.10.1: the move arrives, and its total travel is
  unmeasurable. ⚠️ **And 1.11.0 withdraws the arrival too**: an independent
  clip covers the same half turn and stops at the rear, so this clip's ending
  on the named frame is a coincidence of where its move began. What still
  stands from this bullet is the waypoint form producing movement where a
  camera verb produced none.)* Job
  `50f623b2-c54a-4d9d-9646-31dd06e2a926`, read against the clip's own opening
  frame rather than the start of the segment, using the crank arm as a
  protractor — it extends horizontally in one direction, so it runs cleanly
  sideways from the front or the rear and hides behind the collar from either
  side: front at 2.8s, rear at 7.0s, a side at 9.0s, front again at 10.0s, and
  the same orientation still holding at 11.5s. A clean monotonic circuit.
  **So: describe each angle as a still picture with a timestamp on it. A
  camera verb is not honoured.** A negative control and a positive one, one
  variable apart — which is what makes the prompt the attributable cause
  rather than the roll, and it is still two runs.
- **What that pair cannot attribute, now stated as a limitation in the skill
  rather than left to read as more than it is.** Each waypoint carried two
  kinds of description at once — a camera-position label ("directly behind the
  grinder") and an appearance description ("only the smooth back of the collar
  and the walnut knob beyond it are visible") — and on the 8s waypoint the two
  contradict each other, since from directly behind that arm extends sideways
  rather than pointing away from the lens. The rendered arm-hidden frame
  matches the appearance clause and contradicts the position clause, so the
  run cannot say which half the model followed. Section 3 now says so
  explicitly, and every "the waypoint appeared" line is written to mean the
  picture appeared, not that a position label was obeyed. The forward-looking
  line that follows — **write a waypoint as an appearance description, not a
  camera-position label** — is marked as reasoning from that confound, not as
  something measured, and the template, the §3 slot and the worked example are
  rewritten to carry appearance clauses only.
- **Which motion this skill recommends has not changed; how to write it has.**
  The gallery evidence for "camera orbits, product still" is untouched — every
  rotation there is written as camera movement, and the fixed-camera turntable
  still has no gallery source and, now stated plainly, has never been run here.
  What moved is that the recommended option no longer stands on the words "the
  camera orbits": the `Motion` question, the `Recommended defaults` row, the
  full template's ORBIT slot and a new "3. Camera motion: waypoint pictures,
  not a camera verb" all carry the waypoint construction, and the section is
  the single place the measurement lives.
- **A caller copying the old wording got the rejected clip, so the two
  copyable orbit sentences were replaced.** The worked example's ORBIT line
  was the failing phrasing verbatim; it is now the waypoint form, flagged as
  the one line in that example that is neither case 17's nor a translation of
  it. The compact 5s template's one-sentence orbit is the same phrasing at a
  shorter duration — nothing in this repo has run it, so it is now marked
  untested rather than safe, with a pointer to the waypoint form for any clip
  that has to show more than one side.
- **The pictures are honoured; the spacing between them is not — now its own
  subsection, "4. A timestamp orders the pictures; it does not schedule
  them".** It is a different failure mode from "a camera verb is not
  honoured", and someone will need it without reading the whole A/B, so it has
  its own heading and points back to §3 for the pair. Four evenly spaced
  moments were written into a four-second segment — three interior views at
  7s, 8s and 9s, then the opening front view by 10s. Two of the three interior
  views rendered, and sampled every 0.4s from 6.4s to 10.0s, five of ten
  frames still show the crank pointing right: one view is held for roughly
  half the segment and the rest of the circuit is covered in the last second
  and a half. *(1.10.1: **six** of ten, not five — 6.40 through 8.40 all read
  crank-right, with 8.80 the transition. And "the rest of the circuit" is the
  superseded extent: what the last 1.2 seconds covers is the observable
  rear-to-front travel, not a circuit anyone can measure.)* Stated as counts
  and durations rather than as a per-waypoint schedule, because the confound
  above means "this waypoint was a second late" is not attributable. So:
  **two interior pictures plus the return** for a
  four-second orbit, and no angle planned to land on a given second — if a
  picture has to exist at a given time, make it a segment boundary, where
  stamps have held to about a second across every run here. The return is the
  one wording with evidence behind it: `by 10s the camera has returned to the
  exact front view of the opening shot` names a frame the clip already
  contains rather than a quantity of rotation, and the 10.0s frame is that
  frame.
- **What the accepted clip still gets wrong beyond that pacing, cause
  identified and fix not yet run**: no shot size was written on any waypoint,
  so the orbit inherited the macro closeness of the DETAIL segment
  immediately before it — the base and
  the knurled ring are out of frame for the whole orbit, several angles of the
  collar and the crank and never the whole product from the side or the back.
  The template's slot notes now say a segment inherits the previous segment's
  framing unless told otherwise, and every waypoint carries its own shot size.
- **The rest of the template rendered as written, and two AVOID items earned
  their place.** REVEAL (a plain grey box lid lifting straight up out of
  frame) and DETAIL (macro on the knurled ring and the metal/wood seam, slow
  straight push-in) came back exactly as described. ACCESSORIES produced the
  three correct items, evenly spaced, not touching, **only** in the final
  segment and with no duplication — the two failure modes that slot risks, and
  the AVOID list named both (`no accessory appearing before the final segment`,
  `no duplicated accessory`).
- **Three things the text-only route confirmed that this skill previously only
  argued for.** Zero invented text across an all-bare set of metal, glass and
  wood, including the glass jar's steel screw lid, with **no first frame to
  anchor anything** — the PRODUCT block's explicit "there is no printed text,
  no logo, no engraving and no marking anywhere" plus a carrier-by-carrier
  AVOID list. Zero deformation of the crank arm, a thin protruding
  right-angle part, through both clips. And the consistency lock holding on
  text alone: every earlier accepted clip here that needed a product's
  identity held had an attached image doing that work, so "write the
  consistency lock every time" now rests on a measurement rather than only a
  rationale.
- **`--aspect-ratio 16:9` took effect and the output is exactly 1280x720** —
  the first clean confirmation of ratio control in this repo, since every
  earlier product-adjacent clip attached a frame and was forced to `adaptive`.
  It worked *because* the route was text-only, which "A product photo" now
  states as a benefit of this skill's rule against generating a reference
  image: on that route the platform ratio is a flag, not a crop made
  beforehand. `--generate-audio false` was confirmed the same way — the
  delivered files carry no audio stream at all, not a silent one. Four
  segments at 3/3/4/2 also held: the rejected clip measured 3.12/2.88/3.7/2.3,
  every segment within 0.3s of plan.
- **Two boundaries added where the claims they qualify already live.** The
  seed reproduces a take only while the prompt is byte-identical — both clips
  ran seed `642303335` and the grinder is visibly a different design in each,
  so "give me that take at 1080p" is still the seed's job and "let me tweak
  one line and keep the look" is not. And the scene detector missed the
  rejected clip's 9.7s boundary at threshold 0.25 while finding 3.12s and
  6.00s, a fifth confirmation of the same-lighting blind spot; the record
  stays in `ofox-video-core`'s shared `Checking the cuts`, with a failure-table
  row here pointing at it rather than a competing list.

## 1.9.0 — the four-segment template is inside the measured envelope

Docs only; no script changes. This skill's caution about its own full
template — "the full template's four segments sit one beyond that", meaning
beyond three shots in an 8-second 480p clip with no image attached — was
accurate when written and is now stale.

- **"Several shots: timestamps inside one job" is updated with the route this
  skill actually uses.** Two accepted `seedance-ad-creative` jobs at 720p
  attached a generated product image as `--frame-first-image` and cut inside
  the same job: `7ae7d49e-7eb9-4165-9d95-09cd525d53ed` (15s, 5 shots, 4 hard
  cuts) and `ac927785-92ef-4e28-97b9-ff8172ec5554` (20s, 7 shots, 6 hard
  cuts). Every written cut happened, and the attached frame held the product's
  shape and colours across all of them — on the second, verified as far as
  t=19.6s, which is the property a catalog clip depends on. So four segments
  need no fallback and no hedge in the recap. What is still unmeasured (past
  10 shots or 6 hard cuts, 1080p, the `volcengine` upstream) is named.
- **The failure-table row for missing cuts now points at the transition mix
  rather than the shot count**, and at reading frames instead of trusting a
  scene detector's count — detection at threshold 0.3 under-reports cuts
  between shots of the same subject under the same light, which is every cut
  in a studio product clip.

## 1.8.0 — the segmented template's timestamps didn't scale, and ACCESSORIES could go negative

Docs only; no script changes. Prompted by an audit of every scenario
skill's template after a real short-drama clip was accepted but flagged for
spending too much of its runtime on setup and the ending instead of the
part the clip was actually for (`seedance-short-drama`'s 1.9.0). This
skill's own "Full template — 10–15s, three or four segments" was checked
for the same failure shape and found a related but different defect: its
absolute stamps (`0–3s / 3–7s / 7–12s / 12–<N>s`) do not scale with
`--duration`. REVEAL, DETAIL and ORBIT alone already run to 12s at those
literal numbers, so the template only fits a 15s clip as written — at 10s
or 12s, the recommended low end of this skill's own duration default,
ACCESSORIES is left with zero or negative seconds, and the abstract
template's stamps didn't even match its own worked example (which uses
3/6/10/12, not 3/7/12/N).

- **The four stamps are now `<a>`/`<b>`/`<c>` placeholders**, scaled to the
  chosen `--duration` rather than copied literally, with a new note
  directly under the template ("Scale the segments, don't copy the
  stamps") spelling out why and pointing at the worked example's actual
  proportions.
- **ACCESSORIES' proportion was checked, not just its arithmetic**: it
  stays the smallest segment by design — 2–3s, never the majority — while
  ORBIT keeps the single largest share, because showing the product from
  every angle is the point of a catalog clip. This skill's plain,
  restrained positioning is unchanged; this release fixes a template that
  couldn't produce a valid prompt at its own recommended durations, not the
  skill's stance on how showy a listing clip should be.

Ad-creative and anime-drama were audited in the same pass and needed no
change — see `seedance-short-drama`'s 1.9.0 changelog entry for why, and
`ofox-video-core`'s 1.13.0 entry for the shared two-30-second-job finding
that motivated the audit.

## 1.7.0 — creative brief, segmented catalog template, camera-orbit default

New:

- **"Before writing the prompt: the creative brief."** Before any prompt is
  written the skill fills a four-axis brief — product photo and target
  platform / aspect ratio (both must-ask, neither has a delegation option),
  background, motion — and asks only the open axes. The rules that govern
  that — the three tiers, **one** `AskUserQuestion` call of at most four
  questions with one dependency follow-up, "Let the AI decide" always last
  and never pre-selected, a delegated pick resolved to a concrete value
  marked `(AI's pick)`, the recap in the same message as the prompt and the
  cost table, the generic skip rows, the fixed flow (read → brief → ask →
  prompt → `--dry-run` → recap + prompt + table → yes → generate), and the
  anti-patterns — live once in
  `ofox-video-core/references/creative-brief.md` and are linked, not
  restated. This skill keeps its own question set and its own inference rows
  ("Etsy" → 1:1, "4:3 legacy catalog" → 4:3, "white background" → pure
  white, "spin" → turntable, "orbit" → camera orbit, an attached photo →
  image-to-video) so that **zero questions is a normal outcome**.
  Resolution, duration and audio are never asked — they are rows in the cost
  table.
- **"Prompt template."** A full template (10–15s, three or four segments:
  optional plain reveal → detail push-in → orbit or turntable → accessory
  pan, one action per 3–5s segment, consistency lock, negative list,
  technical tail marked "gallery habit, effect unverified"), a compact 5s
  orbit template, and a worked example adapted from the community
  hair-dryer reveal (case 17). Vocabulary is not restated: the template
  points at `ofox-video-core/references/prompt-structure.md` by section
  heading.

Behaviour changes a caller may notice:

- **Default motion is now "the camera orbits, the product stays still".**
  Every rotation in the gallery's product-adjacent prompts is written as
  camera movement (official case 42's `360-degree orbit`, case 39) or a hand
  turning the product (case 24); none writes a turntable with a fixed
  camera. The turntable sentence is kept as the alternative and is what the
  brief picks when the user says "spin" or "turntable".
- **The pure white background is now labelled a marketplace convention, not
  gallery evidence.** The gallery's cleanest product prompt (case 17) uses a
  reflective studio surface; case 41 pins its background rather than
  removing it. The brief offers pure white (recommended), light grey studio,
  or the photo's own background.
- **"Prefer a real product photo — practically require it" is replaced by a
  two-row rule**: a real SKU (logo, printed label, distinctive geometry,
  brand packaging) requires the photo; a category prototype or fictional
  brand may go text-only, with expectations set — the gallery's four
  product-video prompts (cases 16–19) are all text-only and all fictional.
  The section also states that **an AI-generated product image is not a
  substitute for a photo of the real item**: no gallery product case takes
  that route, and a generated image can be wrong in the same ways the video
  can, then lock the error in as the first frame.
- **Aspect ratio moved from "ask the user" in the defaults table to a
  must-ask brief item** with four platform options (1:1 marketplace
  recommended, 9:16 TikTok Shop, 16:9 detail page, 4:3 legacy catalog). The
  reason is unchanged: with a photo attached the output follows the photo's
  shape, so the photo has to be cropped or padded to the ratio before
  generating.
- **Several shots inside one job are now the documented route for cuts.**
  Verified on Ofox 2026-09-03 (two three-shot prompts, `seedance-2.5`,
  `byteplus`, 8s, 480p, 16:9, no audio, pure text-to-video with no image
  attached — both cut within about one second of the written timestamps).
  Not covered by those runs: more than three shots, clips longer than 8s,
  an attached reference image (this skill's usual route), cuts with
  dialogue, other resolutions, `volcengine`. The full template's four
  segments are one beyond the tested count and the file says so.
  "Multi-shot product sequences" is replaced by "Several shots: timestamps
  inside one job, `chain` across jobs" — `chain` is for sequences past the
  30s ceiling or shots that need their own approval, seed or resolution.
- **Both image semantics are named**: `--frame-first-image` (first frame,
  verified, the default here) and identity references via
  `--extra-json '{"input_references":[…]}'` for several angles of one
  product (up to 9 images; element shape from `api-params.md`; not run end
  to end in this repo). The two are mutually exclusive
  (`references_conflict`). New failure-table rows for `references_conflict`,
  `input_moderation_failed`, "the output is the photo's shape" and "the clip
  did not cut where written".
- **Real-person reference photos** (a hand modelling a ring): the file now
  says Seedance 2.5 image-to-video refuses them at submission and that
  `--real-person true` is untested on 2.5; the reliable route is a photo of
  the product alone.
- Duration default is `5` for the compact orbit and `10`–`15` for the
  segmented template, instead of a single `5`.
- `description` now mentions the brief and "a simple camera orbit or
  turntable motion"; scope (catalog footage, no people, no brand mood) and
  triggers are unchanged. When NOT to use adds the border case with
  `seedance-ad-creative` (a clean showcase with a lid reveal, case 17): the
  test is whether there is a brand narrative or emotional tone to carry.

What to do: nothing breaks. Agents that previously jumped from request to
`--dry-run` should now fill the brief first and expect to ask 0–3 questions
before quoting — and must settle the platform ratio before any photo is
attached. Callers who copied the old turntable example still get a valid
prompt; it is now the alternative rather than the default.

## 1.6.0 — link the shared approval gate instead of restating it

- "Cost: quote it, get a yes, then spend it" and "Before you spend: show the
  prompt, not just the price" are replaced by one section that links
  [`ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md),
  the spec now shared by every Ofox skill in this repo. Both sections were
  right; keeping four private copies of them was the problem.
- What stays here is scenario-specific: one table row per shot for a
  multi-shot sequence, since each shot is a separately billed job.
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

## 1.2.0 — multi-shot product sequences

Documents `ofox-video-core` 1.6.0's `chain`: each shot opens on the previous
shot's closing frame, so the product keeps its position and lighting across
cuts, and the shots are joined into one file. Applies here because the
real-person restriction that blocks chaining live-action sequences does not
apply to objects.

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

## 1.0.2 — ClawHub frontmatter

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
