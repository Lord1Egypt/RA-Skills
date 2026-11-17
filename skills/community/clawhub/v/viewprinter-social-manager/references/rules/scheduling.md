# scheduling: Get approval, state the absolute time, and do not post twice

## Priority: CRITICAL

## What goes wrong

- A relative time is passed through unresolved and the post goes out a day
  early. **That is not recoverable.**
- A retry after a lost response sends the post twice.
- Success is reported before the tool returned, so the user believes something
  is queued that is not.

## Before scheduling

Make sure the content, destinations and time are covered by the user's approval.
Use approval already given in the conversation; ask only for missing or changed
details. **State the resolved time and destinations before the action.**

Publishing cannot be recalled by these tools.

## Promotional-content and AI labels require an explicit choice

**Always ask whether the user wants promotional-content and AI labels before
publishing or scheduling, unless their explicit answer already covers this
post or batch.** These are separate choices. Approval to post, an account's
business status, a brand mention, generated media, or an old agent's payload
is not consent to enable them.

This applies to TikTok `brandOrganicToggle` (own-brand promotion),
`brandContentToggle` (paid partnership), and `isAigc` (AI-generated content),
and Instagram `isAiGenerated`, plus equivalent options exposed by
`platforms_list` on other platforms. Explain the applicable choices in plain
language; do not bundle paid partnership with own-brand promotion.

Ask, for example: "For this batch, do you want the own-brand promotional label
on TikTok? Separately, do you want AI-generated labels on TikTok and Instagram?"
Ask about paid partnership when applicable. Wait for the answer; silence or a
preselected UI option is not consent. One explicit answer can cover the named
batch and platforms; do not ask again within that approved scope.

Only enable a flag after an explicit opt-in. If the user declines an optional
label, omit its parameter rather than inheriting `true` from an example,
template, prior post, or draft. Check saved options before releasing a draft;
if the tools cannot inspect or change them, resolve that before sending it.
Do not add disclosure wording to captions or overlays without approval either.

If current platform rules require a disclosure, explain the requirement and
ask how the user wants to proceed. Keep that destination held until resolved;
do not silently enable the flag or promise that omission prevents labels the
platform applies itself. Record the user's choices with the publishing request.

## Calling it

`posts_save` without a `post_id` records the intent and queues it (unless
`draft: true`). A queued post can begin publishing immediately.

- Omit `scheduled_at` to send as soon as possible; otherwise pass ISO 8601.
  Resolve relative times ("tomorrow at 9") against the user's timezone and state
  the absolute time back to them.
- **Pass `idempotency_key` and reuse it on retry.** A retry without one is how a
  post goes out twice.
- `media_ids` order **is** the slideshow order.
- `platform_options` is keyed by platform. An unknown key is refused, not
  ignored — check `platforms_list` for what each option does and where it
  applies.

## Instagram trial reels

When the live capabilities and connected schema expose `trialReel`, preserve
the user's chosen audience and promotion mode:

- `platform_options.instagram.trialReel: MANUAL` keeps a trial until the creator
  chooses to share it with everyone.
- `SS_PERFORMANCE` permits Instagram to share the trial with followers if it
  performs well. This is organic distribution, not a paid boost, and requires
  approval for that broader sharing.

Confirm current applicability with `platforms_list`; do not assume every media
type can be a trial. Omitting `trialReel` creates an ordinary Reel, and
`shareToFeed: false` is not a substitute. Never publish an ordinary Reel merely
to test whether the trial option works. For schema mismatches, follow
`platforms-first.md` and validate a held draft before releasing it.

Keep disclosure-label choices separate from trial promotion. Record the exact
options submitted. A published response alone does not prove trial mode or
later sharing to followers; use the accepted request for the former, and report
the latter as unknown unless the current tools explicitly expose that state.

## Afterwards

**Report success only after the tool returns**, and distinguish queue acceptance
from delivery. A post that is queued has not yet gone out.

## Context

- Applies to releasing a held draft as well as to a fresh post: `posts_save`
  with its `post_id` and `draft: false` sends it, and that needs the same
  approval.
