# Changelog

All notable changes to the **video-extend-edit** skill. Versioning follows SemVer.

## 2.0.0 — every real-run command carries `--approved`, and the core refuses without it

**Breaking, and the break is upstream.** `ofox-video-core` 2.0.0 makes its
four billable subcommands — `generate`, `create`, `batch`, `chain` — refuse to
run unless `--approved` is on the command line. This skill's one real-run
`chain` command now passes it. The `--dry-run` commands are untouched: a quote
is how the number being approved gets produced, so gating it would close the
only route through itself.

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
- **The local ffmpeg steps are not gated** — extracting the last frame,
  trimming a head, joining two files and building a contact sheet all spend
  nothing and are untouched. A `chain` commits every segment at once, which is
  why its dry run is the only place the sequence can still be stopped.

**What `--approved` is not.** It does not prove that an approval happened — an
agent can type it without showing anyone a price, exactly as it could
previously just run the command. What changed is that spending without quoting
is no longer the default: it now has to be written into the command, where a
transcript shows it and a reviewer can object. The gate in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md)
is still the rule, and this skill still states it in full.

**Documentation only otherwise. No price, default, prompt template, flag
meaning or generation behaviour changed.**

## 1.3.1 — the recovery command asked for the whole repo, and asked the agent to run it

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

## 1.3.0 — an ACTION clause with no starting state fails silently

**Documentation only. No default, price, prompt template slot, command or
route changed.**

Carrying a published 12-second product clip 12 seconds further (job
`565e3193-68d7-4223-bb15-337723e89836`, $2.88, i2v + a local ffmpeg join)
produced two findings about writing the prompt, and both are now in the file.

- **An ACTION verb that has no starting state in the attached frame does
  nothing, and says nothing.** The clause asked a hard case lid to close onto
  its base; in the anchor frame that case was already closed. No error, no
  warning, nothing in the returned metadata. The other half of the same ACTION
  line — a cloth drawn out of frame — landed in the same job, verified as a
  real translation rather than the push-in cropping it out. "Read the PNG
  before you write the ACTION line" is now a measured step in **Pull the
  frame**, not a line of craft advice, and the template's `ACTION` slot says
  it too.
- **"Negative clauses are honoured more reliably" is about the AVOID list, and
  one `CAMERA` sentence warns against carrying it there.** The same sentence
  produced three outcomes, now tabulated in **The prompt**: three qualitative
  framing clauses landed; the one *quantified* clause came up short ("about two
  thirds of the frame width" measured 52%, at most ~58% counting the part
  cropped off-frame); and the one *negative* framing-state clause ("from 8s the
  case is no longer in frame") did nothing at all. The quantified miss lines up
  with this repo's existing count-versus-quality finding rather than being new.
  Both readings are marked n=1 and as shapes to watch, not rules, and the
  positive rewrite to reach for meanwhile is given.

**What a caller has to do differently:** before writing `ACTION`, open the
extracted PNG and walk it object by object, checking that each verb can start
from what is actually in the picture. An agent that fills the slot from the
scene described by the user — rather than from the frame — can write a clause
that is silently discarded, and the job still completes and still bills.

## 1.2.0 — this skill's reason for existing was an inference; it is now a measurement

**Documentation only. No default, price, prompt template, command or route
changed.** The frame-out / generate / join route is unchanged and remains the
only way to lengthen a clip here.

What changed is the evidence under it. This file argued, from inference, that
Ofox exposes no native `extend` or `edit` mode. That was tested on 2026-09-16
and the real behaviour is more specific than "unsupported":

- **The `mode` field is accepted and discarded.** Job
  `4686f434-16b0-451f-8941-970e5b3d4a15` sent an invented mode value inside an
  ordinary text-to-video request and got `200`, a completed plain 4-second
  t2v clip, and a $0.44 t2v bill. A value nothing could implement cannot have
  been honoured, so the field is dropped somewhere in the chain.
- **`duration: -1`** — the form the gallery's official edit case uses to lock
  the output to the input's length — returns `502 route_error`, raised before
  any reference URL is fetched.

**What a caller has to do differently:** stop describing extend/edit as
something the API *refuses*. Nothing refuses it. An agent that tells a user
"the request will be rejected", or that watches for an error code before
falling back to this skill's route, is waiting for something that never
arrives — and a `200` on a request carrying `mode` is not evidence the mode
ran. The description, "Read this before planning anything", "Unmeasured
edges" and the "When NOT to use" table all now say *accepted and has no
effect*, with the job id.

Also noted, and it changes nothing here: `input_references` **images** were
measured working the same day (job `0f5c8b4e`). That is subject/style
guidance with an unchanged duration ceiling, not a clip to continue, so it is
listed under "Unmeasured edges" as ruled out rather than as a new route.

## 1.1.0 — the chain command was run, and the real-person wall is now half a wall

Two of this file's own "not measured here" statements were closed on
2026-09-16. Both were load-bearing: one was the largest stated gap in the
skill, the other was the only composed command it recommended without having
run.

### `chain --frame-first-image` has been run end to end

1.0.0 and 1.0.1 said the routing was readable in the script but that "the
composed command has not been run end to end here", and listed it under
**Unmeasured edges** as the thing most wanted. It ran: `STATUS
chain_completed`, two shots of 4 seconds at 480p seeded from a frame pulled out
of an existing clip, **88 cents across the two**, matching the sequence
estimate.

- Shot 1 opened on the supplied frame (job `69bc799d`) — the bottle's position
  and scale, the gold cap, the water and the background all match the PNG fed
  in. That is the runtime confirmation of what reading `cmd_chain`'s argument
  handling had only predicted.
- Shot 2 opened on shot 1's closing frame (job `2a3ebe06`) — ripples, slab
  edge, position and light direction carried across, with the slight seam
  brightness shift `ofox-video-core` already records.

The caveat is gone from the "Several segments" section and the Unmeasured edges
entry is narrowed rather than deleted: a chain of more than two shots from a
user's frame, and any chain on a non-default model, are still unrun.

**One thing that run does not do is finish the join**, and the file now says so
where it could otherwise be misread: the two shots came back the same size *as
each other*, which is exactly why `chain`'s own concat succeeded without
rescaling. The user's source clip is not in that set, so the rescale recipe in
finding 3 is unchanged and still mandatory — it is the case where the sizes
genuinely differ.

**Two new data points for finding 2, and a distinction worth protecting.** The
size table is now five rows. The same 720x480 3:2 frame produced 794x530 in two
independent jobs on two different days — so **the size mapping is reproducible
even though the picture is not.** This repo's "a fixed seed does not reproduce
a clip" finding is about *content* and stays exactly as true; the file states
both and says outright that neither weakens the other. The refusal to write a
formula for a non-catalog ratio stands: two observations of one ratio establish
that the mapping is stable for that ratio, not that it is derivable for
another.

### The real-person gap is half-answered — and only half

`--real-person true` was measured lifting the `input_moderation_failed` refusal
on `bytedance/seedance-2.5`. The measurement belongs to `ofox-video-core` and
this file links to
[`api-params.md`](../ofox-video-core/references/api-params.md) → the
real-person section for it rather than restating it.

**The wording is a hard constraint and is the risk in this release.** The flag
is Ofox's privacy-preserving preprocessing path for real-person references the
user is **authorised** to use: an authorisation route, **never** a way past the
check. It appears nowhere in this skill as a workaround for a rejection.

**And the half that is still open is this skill's own case**, which is why
"Before you spend: look at the frame" now splits the two explicitly instead of
rounding up. The measured input was a **synthetic portrait posed for the
test**. A frame lifted out of live-action footage of a real person has never
been sent, with or without the flag; neither has anything been measured about
whether the preprocessing leaves that person recognisable enough for the
segment to match the footage it joins. The file says in as many words: **do not
tell a user they can now extend footage of people.** What can honestly be
offered is a route to price as an experiment when the footage is theirs to use.

Same treatment in the `input_moderation_failed` failure row, the Unmeasured
edges entry for real-person footage, and the short-drama row of "When NOT to
use".

## 1.0.1 — two holes found by blind routing testers, both on the money path

Routing itself was correct in every blind test. These are defects in the file,
found by testers who followed it literally.

- **The audio hand-off was a hole, and the default it shipped was broken.**
  The join recipe strips audio from both parts with `-an` and then said to
  "lay the final track on afterwards with `mux-audio joined.mp4 track.m4a`" —
  without ever saying where `track.m4a` comes from. In this skill's own
  scenario that recipe, followed literally, hands the user a fifteen-second
  video whose generated nine seconds are silent, and nothing flagged that as
  the default outcome. A new section, **"The audio hand-off"**, names the
  three honest endings — the source clip's own track padded out, keeping the
  model's generated track and accepting a hard cut between two unrelated
  soundtracks, or deliberate silence — with the commands for each and an
  explicit note that **which one sounds best is craft, not a measurement.**
- **And it contained a worse trap than silence.** `mux-audio` runs to the
  **shorter** of its two inputs, so muxing the source clip's own unpadded
  track onto the joined file **destroys the segment that was just paid for**.
  Reproduced locally at zero cost: a 14-second joined picture and a 5-second
  track produced a **5.0-second** file. The padding step is therefore written
  as mandatory, the script's own `NOTE:` is quoted as the thing to act on, and
  the case has its own row in the failure-mode table. Every command in the new
  section was run end to end on real files before being written down.
- **"The source clip's own tier" was a default nobody could execute.** The
  recommended-defaults table said to match the source's resolution tier but
  never said how to map an arbitrary `WIDTHxHEIGHT` onto a tier — a tester
  with a 1080x1920 phone clip had to guess and said so. A new subsection gives
  a decidable rule (**short side → the highest offered tier at or below it**,
  with the tier list read live rather than hardcoded) and states plainly that
  **nothing measures which tier "matches" a source best**: what is measured is
  that the delivered size comes from the tier and the frame's ratio, and the
  join rescales everything anyway, so this choice decides how much detail
  exists to be scaled and what the segment costs — not the finished file's
  size. Tiers not written as a pixel height are called out as outside the
  rule, and dropping a tier to save money is named as a legitimate row in the
  cost table rather than a mistake.
- `--generate-audio`'s default row now says what it really is: the audio
  decision, made **before** the paid job, because only the keep-the-model's-
  track ending needs `true`.
- The hand-over section now says the deliverable is the `-with-audio.mp4` file
  when a track was muxed on, and that the chosen ending has to be stated —
  a user cannot hear an ending from a path.

## 1.0.0 — first release

A scenario skill for the case where the user already has footage and wants
more of it: a frame is pulled out of their clip locally for nothing, handed to
a new video job as its first frame, and the result is joined onto the
original. Three routes over one mechanism — `last-frame` to extend, `frame-at`
to replace the ending from a chosen second, and `chain` for several segments.

**The route this skill does not take is the one its planning document named.**
Video-to-video via `input_references` was the obvious candidate and is
measured not to reach what it promises: a video reference leaves a single
job's duration ceiling unchanged, so there is no mechanism there for extending
a clip past one job's length; it requires a publicly reachable URL with no
local-file form; it bills at the dearer video-to-video tier; and the one real
run on it could not distinguish continuing a scene from a style reference
redrawing a near-static picture. The frame route is cheaper, takes a local
file, and anchors on an actual frame. Video-to-video is recorded under
"Unmeasured edges" as *no evidence yet*, phrased so that a later measurement
adds a second route rather than overturning this file.

**Built on one paid run, two zero-cost readings and one local reproduction,
and the skill says which is which throughout.** Job `35b6aed1` (2026-09-15),
`bytedance/seedance-2.5`, 4 seconds, 480p, one frame attached, **44 cents
billed against a 44-cent estimate**. The input was built to be hostile in
exactly one way: a frame taken out of an existing 854x480 clip with
`frame-at --at 6.5`, then resized to 720x480 — a 3:2 shape that is not in the
model's aspect-ratio list at all. Four findings came out of it:

- **A frame whose shape is not in the catalog is accepted.** No rejection of
  any kind. The skill therefore does not tell anyone their clip has to be
  16:9, because that would be false.
- **The delivered segment's pixel dimensions never come from the source
  clip.** Three observations — 1792x1008 in at 720p gave 1280x720 twice, and
  720x480 in at 480p gave 794x530 — all keeping the ratio and none keeping the
  size. The rule is written as "dimensions come from the tier you paid for and
  the frame's ratio"; **no formula for a non-catalog ratio is published**,
  because one data point cannot support one.
- **Which is why the join needs a rescale, and why skipping it is silent.**
  A plain `concat -c copy` across the two sizes does *not* error: it produces
  a variable-resolution mp4 whose container header advertises only the first
  part's size. Reproduced locally at zero cost — header 854x480, frame at 4
  seconds really 794x530. Not erroring is worse than erroring, so this is the
  most prominent thing in the file, with a normalise-then-join recipe that was
  run end to end across a size change, a frame-rate change and mixed audio
  presence, plus a verification loop that is the only thing which catches the
  silent case.
- **The result continues the scene rather than reproducing the fed frame.**
  The camera measurably pulled back and the prompted ripples appear where the
  source clip has none. The promise is therefore worded as **continuity of the
  same set and subject** — never "keeps the style", which nothing measured
  here supports.

Also in this release:

- **A pre-flight look at the extracted frame, before any money moves.** A
  photoreal person in an attached frame is refused at submission on
  `bytedance/seedance-2.5` (`input_moderation_failed`, unbilled), so the route
  stops there for live-action footage of people. The fallbacks are stated
  precisely rather than hopefully: `alibaba/wan-3.0-prime` and
  `minimax/hailuo-3` were measured accepting a real person's **portrait
  image**, which is not a frame lifted out of footage, and **neither model's
  image-to-video behaviour has been measured in this repo at all**. The
  measured run here deliberately used a clip with no people, so it says
  nothing about real-person footage in either direction.
- **"Re-shooting from second N regenerates everything after N" is stated
  before the routes**, where a reader hits it while planning rather than
  afterwards. There is no mechanism for changing the middle of a clip and
  keeping its ending.
- **`chain --frame-first-image` is documented with its evidence split out.**
  The flag reaching shot 1 was confirmed locally at zero cost by observing
  that shot 1 raises `references_conflict` only when a frame is present; both
  halves of the composition are measured separately; **the composed command
  has not been run end to end**, and the file says so and offers the
  one-`generate`-per-segment alternative for anyone who wants only measured
  ground.
- **No hardcoded model, price, resolution or duration table.** Those are
  catalog facts that move, and the skill points at `ofox-video.sh models` /
  `providers` / `generate --dry-run`. The single cost figure it prints carries
  the exact parameters it was measured at.
- **An ffmpeg check of its own.** `ofox-video.sh check` covers `curl`, `jq`
  and the key but not ffmpeg, and this skill cannot run one step without it.
- **The core-directory probe ships from day one**, above the first example
  containing a hardcoded path, so the skill works on LobeHub's
  `ofoxai-skills-<name>` layout as well as skills.sh / ClawHub /
  `npx ofox-skills`.
- **A routing table with eight rows**, including the two that are easiest to
  get wrong: "change what is in the picture" has no path in this repo at all
  (`image-edit` is a single still, not footage), and a multi-shot sequence
  with no existing footage is core's `chain` directly rather than this skill.
- Shared prose is linked, not restated: the approval gate, the prompt formula
  and the pre-prompt question rules all live in `ofox-video-core/references/`.

**What a caller has to do**: install `ofox-video-core` beside this skill, at a
version that has `frame-at` — `last-frame` is older, so on a core without
`frame-at` the extend route still works and only the replace-the-ending route
is unavailable. `npx ofox-skills` installs every skill in this repo, which is
what keeps the sibling path resolvable. `ffmpeg` is required for every route.
