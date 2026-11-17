# Changelog

All notable changes to the **shorts-reels** skill. Versioning follows SemVer.

## 2.0.0 — every real-run command carries `--approved`, and the core refuses without it

**Breaking, and the break is upstream.** `ofox-video-core` 2.0.0 makes its
four billable subcommands — `generate`, `create`, `batch`, `chain` — refuse to
run unless `--approved` is on the command line. Both of this skill's real-run
commands — the `create` in the five-different-clips route and the `generate`
that promotes a winning take — now pass it, and so does the real run of the
`batch` shown here as a dry run. The `--dry-run` commands are untouched: a
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
- **`poll` is not gated, deliberately.** It only ever issues GETs against jobs
  that already exist, and it is how a set you have already paid for gets
  collected — so the five-`create`-then-one-`poll` route needs the flag on the
  creates and never on the poll. `contact-sheet` is local ffmpeg and is not
  gated either. **A promotion is a second purchase**: its own dry run, its own
  table, its own `--approved`.

**What `--approved` is not.** It does not prove that an approval happened — an
agent can type it without showing anyone a price, exactly as it could
previously just run the command. What changed is that spending without quoting
is no longer the default: it now has to be written into the command, where a
transcript shows it and a reviewer can object. The gate in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md)
is still the rule, and this skill still states it in full.

**Documentation only otherwise. No price, default, prompt template, flag
meaning or generation behaviour changed.**

## 1.0.1 — the recovery command asked for the whole repo, and asked the agent to run it

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

## 1.0.0 — first release

The live-fire findings of 2026-09-15 — this scenario's own paid batch —
landed before this version went out, so they are part of the first release
rather than a version of their own.

A scenario skill for short-form social raw material: several cheap vertical
9:16 drafts in one priced batch, a contact sheet to pick from, then a single
re-render of whichever take earned it. A thin layer over `ofox-video-core`'s
existing `batch --takes N` rather than new machinery.

**It owns format and economics, not prompt craft**, and says so in its second
section. A vertical draft is still a clip of something, and the prompt for it
belongs to whichever scenario fits — `ugc-ads`, `seedance-ad-creative`,
`seedance-short-drama`, `seedance-product-video`, `seedance-anime-drama`. The
skill routes there explicitly rather than growing a fifth template.

**Ambient / mood b-roll has a row of its own, because no scenario skill owns
it.** A clip with no product, no people and no beat — rain on a window, steam
off a cup, a city at dusk — is high-frequency in short-form and falls through
every scenario skill's description. Left unrouted it gets improvised from the
ad template, which arrives with a hook, a showcase and a hero freeze bolted
onto something that has nothing to show. The row sends it straight to the
shared `prompt-structure.md` — the vendor's four-sentence formula, the style
anchor, the camera language — which is scenario-neutral by construction.

**"Five clips" is ambiguous, and settling it is the first must-ask.** Five
takes of one idea is `batch --takes 5` — one estimate, one contact sheet, five
seeds. Five *different* clips is five `create` calls and one multi-id `poll`,
which is a different command, a different cost shape and a different output.
Picking wrong spends money on the wrong shape of deliverable and no amount of
prompt quality recovers it, so the skill asks before drafting and documents
both routes.

**No price table, on purpose, with three reasons.** Prices are catalog facts
that move; which model is cheapest depends on the resolution tier; and at
least one video model in this catalog is priced differently on its two
upstream providers, so even "model X costs Y" is underspecified without naming
the provider. What the skill ships instead is a **reproducible comparison
ritual**: two dry runs — the draft set on the cheap model and one flagship
clip — shown side by side as they print. That argument stays true when the
catalog changes.

**Both measured anchors are quoted with their parameters**, and there are now
two. `ofox-video-core`'s batch path was verified at 3 takes of
`bytedance/seedance-2.0-mini`, 480p, 4 seconds, 24 cents total, exactly
matching its estimate, contact sheet rendered — a measurement of the mechanism,
estimate matches bill. This scenario then got a paid run of its own
(2026-09-15), driven by an agent working from this file, so what it exercised
was the skill rather than the API: **5 takes at the same model, tier and
duration, `BATCH_COST_TOTAL 0.40` — 40 cents, 8 cents a take, reconciling
exactly with the estimate**, contact sheet produced, each take carrying its
own distinct seed (`432922460`, `264334079`, `809870386`, `465992541`,
`213135543`), and the five takes visibly different variations of one idea
rather than five near-identical clips — which is the property that makes a
batch a selection artifact and the only one worth paying five times for. The
skill still states that neither anchor is a quote for any other combination
and that 8 cents a take is a per-second rate times 4, not a fixed price.

⚠️ **There is no "Seedance 2.5 Fast".** Planning notes that name it are wrong;
no such id exists in the catalog. The skill says so where a model gets chosen
and points at `models` as the authoritative list.

⚠️ **`providers` takes a model argument, and without one it prints the
flagship's matrix rather than the catalog** — the most expensive model's rates,
read while believing you are shopping for the cheapest. This skill is the one
where that mistake costs the most, so it spells out the two-step: `models` to
shortlist, `providers MODEL` to quote. The `models` column is also the rate at
each model's *own* default resolution, so a model can rank worse there and
still be the cheapest at the tier you are actually drafting on.

Also in this release:

- **When to step up to a dearer model, split by *why* the draft was
  rejected** — fidelity, detail that has to survive, publication, or a
  duration/resolution ceiling the budget model can't reach are reasons to
  promote; a beat that didn't happen, a camera that didn't move, or every take
  failing the same way are prompt problems that a dearer model renders more
  expensively. Plus the non-reason: moderation policy is per-model, so a model
  change can be a route rather than a downgrade.
- **The seed's boundaries, stated four ways — a promotion is another roll
  aimed at a take, never that take returned.** Measured 2026-09-15: three
  submissions of one byte-identical request on a fixed seed came back as two
  visibly different clips and one `output_moderation_failed`, so this API is
  not reproducible even with nothing changed. A byte-identical prompt is still
  necessary (measured separately: same seed, one paragraph reworded, visibly
  different subjects), which is why the promotion reads its prompt out of the
  sidecar; the seed is not a handle for "that one, but fix the third beat";
  and across two different models it is further still — nothing in this repo
  has measured a seed carrying a take across models. The skill's instruction
  is to say all of this *before* the promotion is paid for.
- **`--seed` still doesn't belong on a batch, for a corrected reason.** Not
  "you would pay N times for N identical clips" — that rests on a
  reproducibility this API doesn't have. It removes the only axis a batch
  varies deliberately: every take asks for the same generation, each is
  billed, and whatever variation comes back is the server's rather than one
  you chose.
- **Batch mechanics relayed rather than reinvented**: stop on first rejected
  create, a post-submission failure not stopping the others, `batch_partial`
  and the `TAKES_*` counters, concurrent waiting at the default 4, the
  `--takes` cap of 10, and the resume command `batch` prints instead of a
  second `batch`.
- **Contact-sheet honesty.** Three thumbnails per take answer composition,
  look and whether the beat happened; they do not answer fine detail or
  legibility. Open the take, or re-tile one clip with `contact-sheet` for
  free.
- **Two approvals, not one.** The draft round gets an itemised table quoting
  `BATCH_COST_TOTAL` (never `BATCH_COST_PER_TAKE`); the promotion gets its own
  table later, because which take wins — or whether any does — isn't known at
  the first gate.
- **Vertical is checked, not assumed.** Aspect-ratio lists differ per model
  and the budget models' are shorter, so the skill reads `models` before
  picking; and with a frame attached the ratio follows the image, so crop to
  9:16 first — crop, never pad.
- **Duration is named as the multiplier that hurts most**, since it applies to
  every take in the set.
- **The core-directory probe ships from day one**, so the skill works on
  LobeHub's `ofoxai-skills-<name>` layout as well as skills.sh / ClawHub /
  `npx ofox-skills`.

**What a caller has to do**: install `ofox-video-core` beside this skill, and
at least one scenario skill to write the prompt with. `npx ofox-skills`
installs every skill in this repo, which is what keeps the sibling paths
resolvable. `ffmpeg` is optional — without it the contact sheet is skipped
with a reason and the videos are untouched.
