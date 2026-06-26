---
name: kiss-cam
description: >-
  Generate a viral fake "in-arena Kiss Cam moment" of any two subjects — a
  fan-filmed phone shot of the MSG Jumbotron with retro Kiss Cam graphic +
  scoreboard, plus a 15s Kling v3-omni clip with PA-announcer commentary and
  crowd reaction. Any subject styles (human, 3D toy, illustrated avatar). No
  names. Triggers: "make me a kiss cam moment", "kiss cam version of these
  two", "Jumbotron kiss cam trend", "fake NBA kiss cam". Requires the pika MCP.
argument-hint: <subject-a-photo-path-or-url> <subject-b-photo-path-or-url>
---

# kiss-cam

A two-call pika pipeline: spectator-POV Jumbotron still (`gpt-image-2`) → 15-second in-arena kiss cam clip with PA-announcer commentary and crowd reaction (`kling-v3-omni`, first-frame-locked to the still). The trend look is calibrated — pass both reference images straight through. There is no textual substitution into the prompts; the subjects are anchored only through `reference_images`. Don't reach for `${subject_a}` / `${subject_b}` placeholders. Step 1 and Step 2 prompts are verbatim, not scaffolds.

## Prerequisites

pika MCP available in the host. Tool name prefix varies by mount point — use whatever the host exposes. Tools needed: asset upload, image generation, reference-video generation, and async status follow-up when a generation does not complete inline.

## Stage 0 — Intake

If invoked with empty args and no usable prior context, print this menu and stop:

> **Which two subjects should be on the Kiss Cam?** Required:
>
> - **Subject A reference photo** — local path or HTTPS URL
> - **Subject B reference photo** — local path or HTTPS URL

If one photo is already present, ask only for the missing photo. Running before both have arrived leaves Step 1 with a missing `reference_images` entry and produces an inconsistent still.

- **Subject A reference photo** *(required)* — local path or https URL. Save as `state.subject_a_url`.
- **Subject B reference photo** *(required)* — local path or https URL. Save as `state.subject_b_url`.

For each: if already an `https://…` URL, use it as-is. If local path → `mcp__pika__upload_asset` → PUT bytes to `presigned_url` → use `public_url`. On Claude Desktop, pasted inline images don't reach MCP — ask once for a URL or a `.zip` attachment instead (this is the one allowed clarifier; once both URLs are in, the "no further yes/no gates" rule below applies).

Either subject can be in any visual style — photoreal human, 3D rendered character, designer toy, illustrated avatar, sculpted figurine, etc. The recipe preserves whatever style the reference uses; do not redraw in a different style. **No names are used anywhere** — the Kiss Cam graphic does not have a chyron with names. Just two subjects caught on the Jumbotron.

Confirm back in one line ("Generating a Madison Square Garden Kiss Cam moment for these two…") and start. **No further yes/no gates after this point** — the pipeline runs end-to-end.

## Step 1 — Spectator-POV Jumbotron still (`generate_image`, gpt-image-2)

The kiss cam graphic + scoreboard + retro frame get baked into the still at frame 0 — load-bearing, so Kling treats the entire decorative UI as pixel-locked burned-in UI in Step 2 instead of animating it mid-clip.

**Why gpt-image-2 (and no fallback):** sharper LED panel detail (scoreboard numerals, kiss cam typography, retro decorative edges) and stronger reference-likeness lock than alternative providers; the LED-sharpness + likeness combo is what sells the trend. On a `moderation_blocked` response, re-roll the same call instead of swapping providers — alternatives produced softer likeness and softer LED detail in earlier trials. We call gpt-image-2 at 1K 16:9 (1792×1024); the 2K/4K variants (AGNT-336) don't help here since Kling pro outputs 1080p downstream.

**Why a Jumbotron-POV phone shot (and not a TV broadcast overlay):** the first iteration produced a TV broadcast cutaway with a pink-heart kiss cam graphic on the feed — user feedback was "the kiss cam graphics is ugly, look how real kiss cam moments look in real videos." Real viral kiss-cam clips online are virtually all spectator phone shots OF the Jumbotron (Obama-era USA Basketball kiss cam, Sarah Hyland / Wells Adams kiss cam, etc.). The Jumbotron-shot framing hits the aesthetic users actually associate with "real kiss cam" — retro red border + sparkly hearts + cursive Kiss Cam script + adjacent LED scoreboard panels + arena darkness + fans filming with phones.

**`prompt`** (verbatim, sent as-is — no template substitutions):

```
A high-resolution spectator-POV phone screenshot from inside packed Madison Square Garden during a Knicks vs Bulls NBA game, filmed by a fan in the lower bowl looking up at the giant suspended Jumbotron displaying the in-arena "Kiss Cam" segment. Real fan-filmed phone footage aesthetic — TikTok / Instagram online kiss-cam clip style.

Foreground (bottom 20% of frame): silhouettes of the backs/heads of a few fans in the row in front, slightly out-of-focus, dark; a couple of phones held up filming the Jumbotron, bright phone screens visible.

Mid-ground / upper 80%: the Jumbotron dominates the upper-center, bright LED panels against the dark arena ceiling and cabling above. Slight phone-camera tilt, slightly off-center natural handheld framing. Dim arena around, hint of upper-deck silhouettes.

The Jumbotron's central LED panel displays the kiss cam segment in iconic retro arena kiss cam style:
- Thick deep crimson red glowing decorative border frame.
- Bright red sparkly cartoon heart icons glowing in the corners and along edges.
- Subtle white star pattern texture in the red border.
- At the bottom center, large flowing white cursive script "Kiss Cam" with red glow and drop shadow.

Inside the kiss cam frame on the Jumbotron, two subjects framed two-shot chest-up:
- LEFT (Subject A) is the character from the FIRST reference image — preserve their exact likeness AND exact visual style (medium, level of stylization, color palette, rendering attributes). Do not redraw in a different style. Subject A is smiling shyly with one hand near the face, looking caught-off-guard and giggling.
- RIGHT (Subject B) is the character from the SECOND reference image — preserve their exact likeness AND exact visual style. Do not redraw in a different style. Subject B is seated upright at human scale next to Subject A, head tilted slightly toward Subject A.
- Around them inside the frame: packed Knicks fans in blue-and-orange jerseys, laughing, pointing, smiling at the kiss cam.

Adjacent LED panels on the Jumbotron show: "KNICKS 57 — BULLS 61", Q4, clock "4:32", with team logos. Small "MADISON SQUARE GARDEN" / "MSG" / AT&T branding.

Phone-camera aesthetic: slight motion blur, mild handheld imperfection, slightly noisy in dark areas, bright LED slightly blown out, 16:9 aspect ratio, real spectator POV. Looks like a still pulled from a fan-filmed Instagram / TikTok kiss cam clip.
```

**Call params:**

- `provider`: `gpt-image-2` (load-bearing — sharpest LED detail and strongest reference-likeness lock; no fallback provider, re-roll the same call on moderation hits)
- `reference_images`: `[state.subject_a_url, state.subject_b_url]` *(order matters — Subject A must be index 0, Subject B index 1; the prompt's "FIRST / SECOND reference image" refers to array index)*
- `aspect_ratio`: `16:9`
- `quality`: `medium` *(default for speed; `high` is now exposed but ~2 min/call — use only when fidelity matters)*
- `output_format`: `png`

**Do not pass textual feature descriptions for either subject.** The prompt above already refers to each subject only as "the character from the FIRST/SECOND reference image" — that's intentional. Describing hair / face / clothing / accessories in text fights the reference image and causes drift: verbal features override the visual reference, and the model homogenizes the subjects toward the description.

The reference images carry all identity + style information; the prompt only adds the style-preservation lock. This works for any reference style — photoreal, 3D rendered, sculpted, illustrated, etc. — without naming the style.

Save the returned URL as `state.kisscam_still_url`.

**Agent-side self-check before Step 2**: visually inspect — if the "Kiss Cam" text is misspelled, the scoreboard looks wrong, or either subject's likeness drifted, re-roll Step 1. Everything downstream pixel-locks to this image. This is the agent's own check — do not ask the user.

**On failure** (`moderation_blocked` from gpt-image-2 — often female/female subject pairings + "kiss cam" wording): re-roll the same call. Do NOT swap providers — alternatives produce softer likeness and softer LED detail.

## Step 2 — In-arena kiss cam clip (`generate_reference_video`, kling-v3-omni)

Kling-omni `image_types: ["first_frame"]` locks the still as literal frame 0, so the Jumbotron, scoreboard, kiss cam frame, hearts, cursive "Kiss Cam" text, and foreground fan silhouettes all stay pixel-locked across all 15s. Only the content inside the kiss cam panel animates.

**Call params:**

- `provider`: `kling`
- `kling_model`: `kling-v3-omni`
- `duration`: `15`
- `aspect_ratio`: `16:9`
- `quality_mode`: `pro` (1080p)
- `reference_images`: `[state.kisscam_still_url]` *(use the latest value — Step 1 re-rolls overwrite it)*
- `image_types`: `["first_frame"]`
- `sound`: `true`
- `prompt_adherence`: `strict`
- `negative_prompt` (verbatim):

```
scene cuts, scoreboard changing, Kiss Cam text changing, graphics morphing, character turning real, character becoming 2D, identity drift, gimbal stabilized, exaggerated acting, theatrical expressions, over-acting, mugging at camera, cartoon reactions, subjects lip-syncing PA announcer dialogue, characters mouthing the announcer lines, subjects' mouths moving with off-screen voice, subjects talking to camera, on-screen lip-sync
```

`prompt_adherence: strict` paired with the full `negative_prompt` anchor list are load-bearing — without both, Kling animates the scoreboard or "Kiss Cam" text mid-clip and subjects regress toward over-acting / lip-syncing the off-screen PA announcer.

**`prompt`** (verbatim, ~2400 chars — keep it pre-trimmed because Kling caps prompts at 2500 chars):

```
First frame: spectator-POV phone shot at MSG of the Jumbotron Kiss Cam segment. Fan-filmed TikTok / Instagram kiss-cam clip style. Handheld phone, NOT pro broadcast.

Camera: continuous handheld shot. Subtle micro-wobble. Slow smooth push-in zoom across 15s toward the kiss cam panel.

Locked: Jumbotron, scoreboard (KNICKS 57 / Q4 4:32 / BULLS 61), red kiss cam border, sparkly hearts, cursive "Kiss Cam" script, AT&T branding, dark arena, foreground fan silhouettes — all consistent.

Inside the kiss cam frame:
Both subjects are the two characters already shown on the kiss cam panel of the first-frame reference still — preserve their exact likeness AND exact visual style across all 15 seconds. Do not redraw either subject in a different style. They animate with subtle, restrained, true-to-life motion within their original style — small natural blinks, gentle breathing, slight head turns, brief micro-smiles. Neither stiff and frozen, nor over-acting. The level of expression is what a real person shows when caught unexpectedly on a stadium camera. Keep all movement subtle, believable, human.
Surrounding Knicks fans react naturally in the background.

Timeline (all reactions stay subtle and human-scale):
0-3s: Subject A notices the camera, small embarrassed half-smile, glances at Subject B. Subject B notices a beat later, soft natural realization, slight smile beginning. Fans behind react gently.
3-7s: A and B exchange a brief warm look, share a quiet small laugh. Faces relax into natural smiles.
7-11s: A and B lean in and share a gentle kiss on the lips — brief, sweet, natural, not staged. Crowd cheers softly.
11-15s: They pull apart with light natural smiles. B leans head gently on A's shoulder. Both share a small quiet laugh.

Audio (non-diegetic / OFF-SCREEN only — Subject A and Subject B stay SILENT throughout, mouths closed, do not lip-sync the dialogue below):
- Packed-arena ambient throughout.
- OFF-SCREEN gender-neutral PA announcer (NOT from either visible subject — an unseen arena voice), amplified, slightly echoey, playful.
  0-3s: "Oh, kiss cam at the Garden — look at this!"
  3-7s: "Hahaha — let's see if they go for it!"
  7-11s: crowd erupts with "AWWWWS," cheers, claps swelling.
  11-15s: PA laughing: "There it is! Big love at the Garden tonight!"
- Phone mic picks up nearby fans louder than PA echo.

Aesthetic: real spectator phone-shot, noisy darks, slightly blown LED, subtle motion blur. 16:9, 1080p.
```

**Why "subtle, restrained, true-to-life motion within the reference style"** (and not "subtle motion only", a specific style label, or an expressive micro-expression list):

- *First iteration* constrained stylized subjects with "subtle head/eye shifts only — remains a vinyl toy throughout" — looked frozen and pasted-in.
- *Second iteration* named a specific style ("Pixar-quality 3D character"), which forced subjects toward that look even when the reference was a different style.
- *Third iteration* said "animate naturally and expressively" with a loaded list of micro-expressions ("eyes widening, mouths opening for shock, cheeks lifting when laughing, hands coming up to the face") — subjects then over-acted, mugged at the camera, became theatrical.

The working framing keeps the style-preservation lock but specifies subtle, restrained, true-to-life motion at the level of someone actually caught on a stadium camera — paired with `exaggerated acting / theatrical expressions / over-acting / mugging at camera / cartoon reactions` in the `negative_prompt` to suppress regression toward the third-iteration failure mode.

Save the returned video URL as `state.kisscam_video_url`. If generation completes asynchronously, follow the MCP tool's returned status handle. Client-layer timeouts can orphan the upstream task with no recovery handle, so re-run from scratch on timeout.

**On failure**: re-run kling — don't switch video engines. Seedance's two-stage likeness gate (same as the `baseball-trend` sibling) makes it unusable here. If the still itself is the issue (use the Step 1 self-check criteria — text spelling, scoreboard, likeness — to decide), re-run Step 1.

## Step 3 — Deliver

Return both Pika CDN URLs: the still image URL and the final video URL. If the host client requires local media markers, create the local preview outside this skill after confirming both CDN URLs are reachable.

One-line summary: *"Kiss Cam moment at MSG — 15s, 16:9, 1080p, Kling v3-omni, native PA-announcer commentary and crowd reaction."*

## Runtime expectations

- **Step 1 — gpt-image-2 medium, 16:9, 2 reference images:** ~40–90s
- **Step 2 — kling v3-omni, pro 1080p, 15s, sound on:** ~3–5 min
- **Step 3 — download + emit markers:** ~5–10s
- **Total wall-clock per take:** ~4–6 minutes

If a re-roll is needed at Step 1 the budget restarts there; at Step 2 only the video stage repeats.

## Load-bearing phrases (keep verbatim)

Don't edit these without a re-validation pass — they're empirical behavior dependencies, not stylistic choices.

**Image prompt (Step 1):**

- `spectator-POV phone screenshot ... lower bowl looking up at the giant suspended Jumbotron` — without this, the model defaults to a broadcast-feed aesthetic
- `iconic retro arena kiss cam style` + the four decorative bullets (crimson border, sparkly hearts, star pattern, cursive Kiss Cam) — together produce the recognizable retro look
- `the character from the FIRST / SECOND reference image` — image-grounding lock; never replace with verbal feature descriptions
- `preserve their exact likeness AND exact visual style` + `Do not redraw in a different style` — the style-preservation lock; both halves are load-bearing

**Kling prompt (Step 2):**

- `First frame: spectator-POV phone shot at MSG of the Jumbotron Kiss Cam segment` — anchor that matches the still
- `preserve their exact likeness AND exact visual style across all 15 seconds` — identity + style continuity across the clip
- `subtle, restrained, true-to-life motion within their original style` + `Neither stiff and frozen, nor over-acting` + `The level of expression is what a real person shows when caught unexpectedly on a stadium camera` — calibrates the motion level (avoids both the "vinyl-toy frozen" and "theatrical over-acting" failure modes)
- `gentle kiss on the lips — brief, sweet, natural, not staged` — the kiss beat anchor (do not soften to "head" / "cheek" — the trend is a lip kiss)
- `Audio (non-diegetic / OFF-SCREEN only — Subject A and Subject B stay SILENT throughout, mouths closed, do not lip-sync the dialogue below)` + `OFF-SCREEN gender-neutral PA announcer (NOT from either visible subject — an unseen arena voice)` — without these, Kling defaults to attributing the quoted dialogue to a visible face and lip-syncs the announcer lines onto Subject A or B
- `Phone mic picks up nearby fans louder than PA echo` — sells the spectator-phone audio aesthetic

**Kling negative_prompt (Step 2):**

- `exaggerated acting, theatrical expressions, over-acting, mugging at camera, cartoon reactions` — without these Kling regresses toward the "expressive" failure mode where subjects mug at the lens
- `subjects lip-syncing PA announcer dialogue, characters mouthing the announcer lines, subjects' mouths moving with off-screen voice, subjects talking to camera, on-screen lip-sync` — paired with the off-screen audio anchor; suppresses Kling's default behavior of animating a visible mouth to match any speech on the audio track

**Params:**

- `provider: gpt-image-2` (Step 1) — see Step 1 rationale
- `prompt_adherence: strict` (Step 2) — without it, scoreboard and "Kiss Cam" text drift mid-clip
- `image_types: ["first_frame"]` (Step 2) — pins the still as literal frame 0
- `quality_mode: pro` (Step 2) — 1080p output
- `duration: 15` (Step 2) — the timeline beats (0-3s / 3-7s / 7-11s / 11-15s) are written for 15s; changing duration breaks the kiss-beat timing

## Engine choice: gpt-image-2 + Kling-only

**Step 1 — gpt-image-2, no fallback.** Empirically sharpest LED panel detail (scoreboard numerals, kiss cam typography, retro decorative edges) and strongest reference-likeness lock — the combo is what sells the trend. On a `moderation_blocked` response, re-roll the same call rather than swapping providers; alternatives produced softer likeness and softer LED detail in earlier trials.

**Step 2 — Kling, no Seedance.** Seedance has a two-stage `partner_validation_failed` 422 gate (same as the `baseball-trend` sibling skill): an input-side gate that rejects references with recognizable real people, and an output-side gate that rejects AFTER generation if the produced clip contains recognizable-looking faces. Every Kiss Cam shot has a packed-arena crowd full of faces, so the output-side gate is unavoidable here. Kling is the only engine that lands this recipe.

**Kling trade-offs**: 2500-char `prompt` cap (recipe above is pre-trimmed to ~2400 chars; re-inflating it can trigger prompt-length errors), no `seed` param (re-rolls are non-reproducible — to re-roll just call again).

## Failure cheat sheet

| Symptom | Fix |
|---|---|
| `moderation_blocked` on Step 1 | gpt-image-2 safety gate (often female/female subject pairings + "kiss cam" wording). Re-roll the same call; do NOT swap providers — alternatives produce softer likeness and softer LED detail |
| Kling prompt error: prompt > 2500 chars | Re-inflated audio or aesthetic section in the Kling prompt. Cut from the audio or aesthetic block; never from the animation timeline |
| Scoreboard, "Kiss Cam" text, or graphics animate mid-clip | `prompt_adherence` not set to `strict`, or `negative_prompt` missing entries like "scoreboard changing" / "Kiss Cam text changing". Verify both params; re-run Step 2 |
| Subject identity drifts after ~8s | Reference still face crop too small — not enough facial pixels for Kling to lock. Re-roll Step 1 with a tighter face crop on the subjects |
| Subject gets redrawn in a different style (photoreal → illustrated, or vice versa) | Style-preservation lock weakened, or a specific style label (Pixar / anime / etc.) crept into either prompt. Restore the "preserve exact likeness AND visual style" anchor; remove any style label |
| PA announcer mispronounces a word or misses the kiss beat | Native audio is one take per Kling generation. Re-run Step 2 — no prompt-level fix |
| One of the on-screen subjects lip-syncs / mouths the PA announcer's dialogue | Kling defaults to attributing any quoted dialogue on the audio track to a visible face in frame — without an explicit off-screen anchor, it picks a subject and animates their mouth to the words. Verify the audio block is framed as `Audio (non-diegetic / OFF-SCREEN only — Subject A and Subject B stay SILENT throughout, mouths closed...)` and the `negative_prompt` contains `subjects lip-syncing PA announcer dialogue, characters mouthing the announcer lines, on-screen lip-sync`; re-run Step 2 |
| Subjects mug at camera / over-act / theatrical expressions / cartoon reactions | Animation block prescribes a loaded list of simultaneous micro-expressions, or timeline beats use exaggerated descriptors ("huge smile", "shy excited wiggle", "eyes widen"). Restore the `subtle, restrained, true-to-life motion` framing in the animation block; strip emotion adjectives from the timeline; verify `exaggerated acting / theatrical expressions / over-acting / mugging at camera / cartoon reactions` are in the `negative_prompt` |
| Kiss lands on cheek / forehead / head instead of lips | Timeline beat softened away from `gentle kiss on the lips`. Restore the verbatim lip-kiss line in the 7-11s beat; the trend is a lip kiss, not a peck on the head |
| Seedance attempted instead of Kling | Wrong engine chosen. Switch to `kling` — Seedance's two-stage likeness gate makes it unusable here (see "Engine choice") |
| Step 2 times out with no `task_id` returned | Client-layer timeout orphaned the upstream task — no recovery handle. Re-run Step 2 from scratch |

## What not to do

- **Don't add name chyrons.** This trend has NO names — it's two anonymous subjects caught on cam.
- **Don't render this as a TV broadcast cutaway with a heart overlay.** It's a Jumbotron-shot.
- **Don't bare-phrase "subtle motion only"** (subjects freeze into vinyl-toy stiffness) **OR load the animation block with simultaneous micro-expressions** like "eyes widening, mouths opening, cheeks lifting" (subjects over-act and mug at the camera). The working framing is `subtle, restrained, true-to-life motion at the level of someone caught unexpectedly on a stadium camera` — both failure modes hide in the word "subtle"; the qualifier "true-to-life" is what calibrates it.
- **Don't write timeline beats with exaggerated emotion adjectives** like "huge smile", "shy excited wiggle", "eyes widen", "giggles back". Use restrained verbs: "notices", "small smile", "exchange a look", "share a quiet laugh".
- **Don't name a specific target style** (Pixar, anime, Disney, photoreal, etc.) in either prompt. The reference image defines the style; the prompt only says "preserve the reference style."
- **Don't soften the kiss to forehead / cheek / "kiss on top of the head".** The trend is a lip kiss — keep the verbatim `gentle kiss on the lips — brief, sweet, natural, not staged` beat.
- **Don't write the audio block as bare quoted dialogue without an OFF-SCREEN anchor.** Kling defaults to attributing any quoted speech to a visible face and will lip-sync the announcer lines onto Subject A or B. Always frame the audio block with `Audio (non-diegetic / OFF-SCREEN only — Subject A and Subject B stay SILENT throughout, mouths closed, never lip-sync any dialogue below)` and add the anti-lip-sync terms to `negative_prompt`.
- **Don't gender either subject** in the narrative or PA dialogue. Use "Subject A / Subject B", "they/them", or descriptions without pronouns.
- **Don't swap providers on moderation hits** — re-roll the same `gpt-image-2` call.
- **Don't try Seedance.**
- **Don't generate music.** Native PA announcer + crowd ambient IS the soundtrack.
- **Don't run a post-processing layer** (`add_captions`, `generate_music`, `edit_concat`, `edit_text_overlay`, `edit_pip`, any `edit_*`). Kling burns the scorebug + chyron + native commentary directly; anything added afterward breaks the kiss-cam illusion.
