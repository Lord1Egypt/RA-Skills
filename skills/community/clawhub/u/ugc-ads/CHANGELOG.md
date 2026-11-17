# Changelog

All notable changes to the **ugc-ads** skill. Versioning follows SemVer.

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

## 1.1.0 — the CAPTURE fix was run and held; the photo path brought two problems

**Documentation only. No default, price, prompt template or flag changed** —
but three things a caller says or does before spending are new, and one of
them is a free local step that was missing.

A second paid run (`ede33e6d`, 2026-09-17, 8s / 480p / 9:16, 88 cents) tested
the two things this file most needed: the **corrected CAPTURE wording**, which
had been shipped without ever being generated, and the **attached-photo
route**, which the brief recommends and nothing had ever run.

**✅ The correction held.** Six sampled frames contain no phone, no camera, no
tripod and no lit screen. The failing construction (`DEVICE:`, "where the
phone is") and its replacement (`CAPTURE:`, the device as a viewpoint) have
now each been measured once, which makes this the best-evidenced line in the
template rather than the one with a known defect and a hopeful fix.

**What a caller has to do differently:**

- ⚠️ **Crop a landscape product photo to 9:16 before attaching it.** The
  traceability table carried an unflagged contradiction: `Photo: yes` → attach
  the frame and pass **no** `--aspect-ratio`, while this file treats 9:16 as
  the default nobody is asked about. With a frame attached the model forces
  `adaptive` and the clip takes the **photo's** shape, so an ordinary
  landscape product shot silently cancels the vertical premise — no error, no
  warning, and it is discovered on delivery. The crop is free and local, it is
  what the measured run did (529x941 in, 480x854 out), and it now appears in
  the table, in a note under it, and as a line in the recap. Found by reading
  two rows of this file against each other; it cost nothing.
- ⚠️ **Expect a flash frame and a hard cut when the photo's background is not
  the scene.** Measured here: background brightness 250 through 0.08s (the
  white studio photo), 33 from 0.12s (the night desk the prompt described).
  About a tenth of a second of the photo, then a cut. **This scenario is the
  worst place in the repo for it**, because an unbroken un-staged take is the
  whole product and the cut lands on frame one. Write the SCENE as the place
  the photo was actually taken, or supply a photo from the target setting, or
  trim the first 0.15s. The mechanism is general and is written up once in
  `ofox-video-core` 1.28.0 (`prompt-structure.md`).
- ⚠️ **With a photo attached, look specifically for polish creeping back in.**
  Run 2 leans toward the look this skill exists to avoid — bottle near centre,
  shallow-focus background, warm key with falloff, flattering steam. **But it
  changed two variables at once** (the photo and the CAPTURE wording), so
  nothing here attributes the drift to the photo. That reading is a
  **hypothesis, not a finding**, and it is labelled as one in the file; the
  single-variable run that would settle it is the same prompt with and without
  the photo. Until then: check for polish, and treat a text-only re-roll as a
  live option.

"What has been tested, and what has not" is rewritten around two runs instead
of one, and the anti-polish pass is now claimed for the **text-only** path
specifically rather than for the skill as a whole.

## 1.0.2 — the real-person flag is measured, and two places here said it was not

**Documentation only. No default, price, prompt template or behaviour
changed.**

"People, products and what the API refuses" and the defaults table's
`--real-person` row both treated the flag as untested on
`bytedance/seedance-2.5`. It was measured on 2026-09-16 and it **lifts** the
submission refusal of a real-person reference image. Both now say that, and
both say what it is: Ofox's privacy-preserving preprocessing path for
**authorised** real-person references — a question for the user about rights
to a likeness, never a flag an agent adds to make a job go through, and never
a retry after a refusal. `ofox-video-core`'s `references/api-params.md` holds
the evidence and its limits; they are linked, not copied.

The split this skill is built on is unchanged and still the recommended
route: the product goes in the attached frame with no person in it, and the
creator is written in the prompt text.

## 1.0.1 — the frontmatter did not parse, and the installer said nothing

The `description` carried a `: ` (colon then space) inside an unquoted YAML
value. YAML reads that as a nested mapping and rejects the whole block, so
`skills add` **skipped this file entirely** — and reported the count of skills
it found, never the ones it dropped. This skill was uninstallable from
skills.sh while appearing published everywhere else.

Replaced with an em dash, matching the rest of these descriptions. Nothing
else changed. A parse check over every SKILL.md is now a publish gate in
CONTRIBUTING.md, because nothing in this repo had ever parsed its own
frontmatter — which is why this survived.

## 1.0.0 — first release

The live-fire findings of 2026-09-15 — the paid run, and the template change
it forced — landed before this version went out, so they are part of the first
release rather than a version of their own. What ships here is the corrected
skill, not the one that was tested.

A scenario skill for handheld, phone-shot creator clips — an unboxing, a first
impression, a use-it-once review — where amateur texture is the deliverable
rather than a compromise. Text-to-video through `ofox-video-core`, with an
image-to-video route for locking a real product's label.

**The load-bearing content is an inversion, and it is stated first.** Every
other video scenario in this repo pushes toward polish, and so does most of
the shared prompt guidance: cinematic anchors, studio keys, a slow-motion
climax and a hero freeze. All of that is a defect here. The skill opens with a
default-versus-here table, names the three habits that leak in from the other
scenarios (style words carried across, the ad beat structure, a camera that
behaves), and ends that section with the check worth running every time —
re-read your own prompt for `cinematic`, `studio`, `professional`,
`film grain`, `rim light`, `shallow depth of field`, `slow motion`. The
failure mode is silent: a polished clip has not errored, it has rendered
exactly what it was asked for and stopped being UGC.

**The anti-polish vocabulary is linked, not copied.** It already exists in
`ofox-video-core/references/prompt-structure.md`, derived from real gallery
cases 25 and 40, and duplicating it would mean one copy getting corrected
while the other kept the old wording. The skill carries a table of *which*
section to load for each need — the UGC anti-polish row for the AVOID list,
`Consumer capture` for phone-capture anchors, the handheld and autofocus rows
for camera behaviour, `Pacing` for the flat action chain, and
`The plastic look is designed out, not forbidden` for why a prohibition alone
is never enough. The prompt template's AVOID slot is an instruction to quote
that row, and the worked example shows the quoted result.

**The one edit that quoted row routinely needs is called out.** It ends
`…fisheye, vignette, or legible text`, which was written for a text-only clip
where every letter would be invented — and in an unboxing of a *real* product
it points at the label the user is advertising. The skill says to lock a real
label in an attached first frame instead, drop that clause, and replace it
with the specific lettered carriers to exclude; the worked example sidesteps
the question by giving its product a plain unprinted box.

**One paid run backs this scenario, and the skill says exactly what it does
and does not establish.** Job `2ecbedec`, `bytedance/seedance-2.5`, 8 seconds,
480p, 9:16, text-to-video, hands only — **billed 88 cents**, and generated
from this skill's own template by an agent working from this file and nothing
else, so the chain under test was skill → agent → command → artifact rather
than the API. Judged on frames extracted from the delivered clip against
criteria written before it ran:

- **The inversion holds, which was the claim most at risk.** The
  pre-registered failure condition was a clip that looks like the ad
  `seedance-ad-creative` would produce — centred hero framing, dramatic
  lighting, a shallow-focus beauty shot. It is none of those: off-centre loose
  framing, one practical window light with real falloff, no grade. Hands only,
  no invented face, product as described. That is a **pass** on the thing this
  skill exists to do.
- **The capture line failed, and it was corrected rather than explained
  away** — see the entry below.

The run is recorded as one clip, not a guarantee: one model, one duration, one
tier, one product, one room, hands only, no dialogue, no attached photo, and
everything outside that is still an experiment. It is also now the skill's
single cost anchor, carried with the parameters it was measured at, in the
approval-gate section. The rest of what the skill rests on is stated as
plainly as before: gallery practice for what a good UGC prompt looks like, and
mechanism facts measured in this repo — the attached-photoreal-person refusal,
the music/moderation failure, prohibitions on object classes holding better
than on tempo, and a camera move written only as a verb tending not to happen.

**The `DEVICE:` line became `CAPTURE:`, because naming the phone put a phone
in the shot.** The template's device slot said to write *where the phone is*,
and the tested prompt did — *"the phone is propped against a biscuit tin at
the back of the desk, slightly too low and a little off-square"*. The
delivered clip has a phone sitting in the box, visible in every frame, with a
small glowing screen that also broke the same prompt's own `no legible text`
clause. The model has no concept of an off-screen camera: a noun with a
position in the room is set dressing.

The slot was **not** deleted — it is how this skill conveys imperfect framing,
autofocus hunting and exposure shifts, which are most of what makes a clip
read as phone-shot. It now asks for those as properties of the shot (`a fixed
viewpoint from the back of the table, at mug height and a little too low, so
the near table edge cuts across the bottom of the frame`) and never for a
device's location. Around that:

- a ⚠️ naming the failure, the job, the exact phrasing that caused it, and why
  the phrasing reads as natural — the gallery's own UGC cases are written that
  way (`static phone propped on bathroom sink`), so a reader will
  reintroduce it otherwise;
- the split that makes it decidable: a phone named as *how the image was made*
  is a format anchor and stays; a phone named as *a thing at a place* is scene
  content and goes;
- `a phone, a camera, a tripod or a lit screen visible anywhere in the shot`
  in the template's and the worked example's AVOID lists, phrased as objects,
  the form this repo has measured holding;
- the timeline slots reworded so a re-frame is something **the frame** does
  (`the view tilts up a few degrees to catch it`) rather than a hand adjusting
  a phone, and the close is `the shot keeps running for a moment` rather than
  case 25's own `the camera continues recording for a moment`;
- a failure-mode row, and the note that **nothing catches this before
  delivery** — that prompt passed `--dry-run`, passed `--print-payload` and
  passed this skill's own re-read-for-polish-words check. Only the extracted
  frames could see it.

The corrected wording has not itself been generated, and the worked example
says so.

Also in this release:

- **Four positive levers**, because the negative list cannot carry the clip on
  its own: the capture is part of the fiction (a CAPTURE line no other skill
  here has), one practical light that behaves badly, framing that is a little
  wrong, and a real room rather than a set.
- **The clutter-versus-invented-text tension is named and resolved.** A UGC
  set is supposed to be cluttered; this repo's one measured rule about
  invented signage says a set full of lettered surfaces produces it however
  strongly the AVOID list forbids it. The skill keeps the clutter and moves
  the lettered carriers out of frame or out of focus, forbids them **as
  objects** rather than as "text", and locks the product's own packaging with
  a photo instead of describing it.
- **The person route, split correctly.** A photoreal person in an attached
  frame is refused at submission; a photoreal person generated from text is
  not. So a product photo carries the product **alone** — no hand, no foot —
  and the person is written into the timeline. Hands-only is recommended as
  both the most common real unboxing shape and the lowest-anatomy-risk one,
  with the measured note that a written size limit on a limb is not a defence:
  one job stated `only the fingertips and the first knuckle ever visible`
  twice, in the shot and in AVOID, and rendered most of the hand anyway.
- **No music, with the reason attached** — a prompt asking this model for
  music came back `output_moderation_failed` on audio copyright in this repo,
  unbilled. Ambient and action sounds only.
- **No hardcoded model, price, resolution, duration or aspect-ratio table.**
  Those are catalog facts and the skill points at `ofox-video.sh models` /
  `providers MODEL` / `generate --dry-run` instead — with the note that
  `providers` without an argument prints the flagship's matrix rather than the
  catalog, and that the rate `models` shows is each model's own *default*
  resolution, so it ranks rather than quotes.
- **The core-directory probe ships from day one**, so the skill works on
  LobeHub's `ofoxai-skills-<name>` layout as well as skills.sh / ClawHub /
  `npx ofox-skills`.
- **It says what degrades without the core installed**, which for this skill
  is more than usual: everything is written out locally except the
  anti-polish AVOID list, deliberately. The fallback is named.
- **It says when not to buy.** A real unboxing filmed on a real phone costs
  nothing and cannot fail an authenticity check.

**What a caller has to do**: install `ofox-video-core` beside this skill.
`npx ofox-skills` installs every skill in this repo, which is what keeps the
sibling path resolvable.
