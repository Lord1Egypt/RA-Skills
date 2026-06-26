---
name: baseball-trend
description: >
  Viral fake "ESPN behind-home-plate broadcast cutaway" of a user — broadcast-style still
  + 15s Kling-omni clip with native two-announcer commentary that names the user. Fixed
  trend: Yankees vs Red Sox ALCS Game 3 at Fenway Park, premium seats, scorebug + chyron
  with the user's name. Triggers: "make me a behind-home-plate cutaway", "fake MLB
  broadcast of me", "AI ESPN baseball crowd shot", "viral MLB broadcast trend",
  "Yankees Red Sox cutaway with me". Needs the user's name + one reference photo.
argument-hint: <username> <photo-url-or-path>
---

# baseball-trend

15-second ESPN-style broadcast cutaway of a user, sitting behind home plate at a fake Yankees vs Red Sox ALCS Game 3 game at Fenway Park, with two announcers naming them on air.

Fixed-recipe skill — the prompts below are calibrated. Substitute the username and keep the marked anchors intact.

## Stage 0 — Intake

If invoked with empty args and no usable prior context, print this menu and stop:

> **Who should appear in the fake MLB broadcast cutaway?** Required:
>
> - **Name** — exactly as it should appear in the chyron and announcer dialogue
> - **Reference photo** — one front-facing or 3/4 portrait, local path or HTTPS URL

If only one field is missing, ask only for that field. Otherwise ask the two questions below one at a time.

**1. Username** *(required)* — used both in the broadcast chyron and in the announcers' commentary, e.g. `"Jane Doe"`. Save as `state.username`. This replaces every literal `${username}` in the prompts below.

**2. Reference image** *(required)* — one front-facing 3/4 portrait, good lighting, one face. Resolve to a CDN URL and save as `state.reference_image_url`:

- **`https://…` URL** → use as-is.
- **Local path** → upload the file with `upload_asset`, then use the returned public URL.
- **Claude Desktop, photo pasted inline** → inline pastes don't reach MCP tools yet (Anthropic limitation). Reply with:

  > Heads up — pasted images don't reach MCP tools on Claude Desktop yet. Two options:
  > - **Paste a URL** if it's already hosted somewhere — fastest.
  > - **Attach the image file** so I can upload it before generation.

  When a local file arrives: convert it to a public URL with `upload_asset` and use `public_url`.

After both answers are in, echo one short confirmation ("Generating behind-home-plate cutaway for **{username}**…") and start the pipeline. **No further yes/no gates after this point** — the pipeline runs end-to-end.

## Pipeline

Two Pika MCP calls, sequential. Engines are locked: `gpt-image-2` for the still, `kling-v3-omni` for the video.

### Step 1 — Broadcast still (`generate_image`)

The chyron + scorebug get baked into the still at frame 0 (load-bearing — when Kling is asked to "pop in" the chyron mid-clip it appears at second 4–5 with a visible flash and breaks the trend; baking it into the first frame makes Kling treat it as pixel-locked burned-in UI).

Call `mcp__pika__generate_image` with:

- `provider`: `gpt-image-2`
- `reference_images`: `[state.reference_image_url]`
- `aspect_ratio`: `16:9`
- `quality`: `medium` (default for speed; `high` is now exposed but ~2 min/call — use only when fidelity matters)
- `output_format`: `png`
- `prompt` (verbatim, `${username}` substituted):

```
A screenshot from a live MLB game TV broadcast on ESPN. The camera cuts to the audience — our reference image person, sitting smiling in premium field-level seats behind home plate at Fenway Park, smiling naturally and unaware they're on camera. Hardlock: Do not alter their facial structure and maintain their likeness. The subject must match the reference person.

The image looks exactly like a real TV screenshot — broadcast color grading, slight compression artifacts, interlacing grain, telephoto broadcast camera feel. It's the New York Yankees vs Boston Red Sox, MLB American League Championship Series (ALCS), Game 3, Boston home stadium (Fenway Park). Yankees lead 2-0 in the ALCS so far.

CRITICAL — broadcast graphics that MUST be visible in this image:
1. A real ESPN-style bottom scorebug for MLB, showing Yankees vs Red Sox with team logos, inning, outs, balls/strikes count, and score (with a small runners-on-base diamond), looking like a real live broadcast scorebug.
2. Directly above the scorebug, a clean broadcast-style lower-third name graphic / chyron that reads exactly: "${username}" — set in a classic ESPN sans-serif, in the network's color treatment. The chyron sits in the lower-left area, above the scorebug, like a real broadcast identifier for the on-camera guest.
3. The ESPN network logo watermark in a corner.

All three graphics must look like real burned-in broadcast UI — not Photoshop overlays. 16:9 aspect ratio.
```

Save the returned URL as `state.broadcast_still_url`.

**Agent-side self-check before Step 2**: the chyron must spell the username correctly and the scorebug must look like real broadcast UI. If either looks wrong, re-roll Step 1 (everything downstream pixel-locks to this frame). This is the agent's own check — do not ask the user.

### Step 2 — 15s broadcast video (`generate_reference_video`)

`image_types: ["first_frame"]` locks `state.broadcast_still_url` as Kling's literal frame 0, keeping the chyron + scorebug pixel-static for the full 15s.

Call `mcp__pika__generate_reference_video` with:

- `provider`: `kling`
- `kling_model`: `kling-v3-omni`
- `duration`: `15`
- `aspect_ratio`: `16:9`
- `quality_mode`: `pro`
- `reference_images`: `[state.broadcast_still_url]`
- `image_types`: `["first_frame"]`
- `sound`: `true`
- `prompt_adherence`: `strict` *(load-bearing — without it the scorebug animates and identity drifts late in the clip)*
- `negative_prompt` *(verbatim, load-bearing — without these entries Kling occasionally morphs the scorebug or fades the chyron)*:

```
scene cuts, camera angle changes, scorebug animation, chyron pop-in, chyron fade-in, chyron text changes, graphics animating, exaggerated acting, direct address to camera, blurry face, identity drift, distorted anatomy
```

- `prompt` (verbatim, `${username}` substituted everywhere; pre-trimmed to fit Kling's 2500-char cap; chyron-on-frame-0 lock at top):

```
First frame is the provided reference image. The ESPN scorebug AND the "${username}" lower-third chyron are ALREADY on screen at frame 0 — keep them visible, unchanged, pixel-locked across all 15 seconds. Do NOT animate them, do NOT change their text.

Realistic live MLB broadcast shot of the subject sitting in premium field-level seats behind home plate at Yankees vs Red Sox ALCS Game 3 in Boston, Fenway Park. The shot feels like a real TV cutaway when the broadcast camera finds a notable guest in the crowd between innings.

The subject is seated in his field-level seat, smiling naturally and not over-performing. Not locked into eye contact with the lens. Occasionally glances toward the field, then toward camera, then back to the field — like a real in-game crowd reaction. One continuous take. No cuts. No angle changes.

Action timeline:
0-4s: smiling casually in his seat as the camera lands on him; looks around naturally, not paying attention to camera.
4-7s: relaxed natural wave toward the camera (crowd cheers when he waves the first time); glances up at the Jumbotron above him then back to camera.
7-11s: cheers briefly with visible excitement, reacting to the playoff atmosphere; turns to his friend on the left, exchanges words, laughs (we don't hear him speak).
11-15s: claps naturally while smiling.

Keep all movement subtle, believable, human. No exaggerated acting. No direct talking to camera.

Broadcast styling: real live sports broadcast look, telephoto broadcast camera feel, natural ballpark lighting, slight broadcast compression, slight interlacing / TV grain, authentic crowd movement in the background, realistic field-level framing. Subject remains seated behind home plate the full shot.

Audio: Natural live sports-broadcast commentary from two male announcers talking about him being at the game tonight. Casual, warm, authentic — like real MLB commentators noticing a known guest. Sample lines:
"${username} is here tonight at Fenway, taking in this massive playoff matchup."
"You can see he's enjoying himself here behind home plate for Game 3."
"Great atmosphere in the building, and ${username} getting a lot of love from the crowd."

Constraints: Preserve identity strongly. Keep him seated behind home plate throughout. No constant eye contact with camera. No talking to camera. No exaggerated gestures. No scene cuts. Scorebug + chyron do not change at any point. Genuine MLB TV broadcast crowd cutaway feel.
```

Save the returned video URL as `state.broadcast_video_url`. If generation completes asynchronously, follow the MCP tool's returned status handle until the video reaches a terminal state.

### Step 3 — Deliver

Return both Pika CDN URLs: the still image URL and the final video URL. If the host client requires local media markers, create the local preview outside this skill after confirming both CDN URLs are reachable.

One-line summary: *"Behind-home-plate cutaway for {username} — 15s, 16:9, 1080p, Kling v3-omni, native two-announcer commentary."*

## Load-bearing phrases (don't strip these)

These are empirical behavior dependencies, not writing style — removing them breaks the recipe:

- In the **still prompt**: `Hardlock: Do not alter their facial structure and maintain their likeness` + `The subject must match the reference person` (without these, identity drifts on the first frame, and everything downstream inherits the drift).
- In the **video prompt**: `Preserve identity strongly` + `The ESPN scorebug AND the "${username}" lower-third chyron are ALREADY on screen at frame 0 — keep them visible, unchanged, pixel-locked` (without these, Kling re-animates the chyron mid-clip).
- The full **negative_prompt** list — every entry there came from a specific failure mode in prior runs.
- `prompt_adherence: "strict"` and `image_types: ["first_frame"]` — see inline notes above.

## Engine choice: Kling-only (with one caveat)

Seedance has a two-stage `partner_validation_failed` 422 gate (validated 2026-05-12 across 4 runs on the NBA sibling skill):

- **Input-side** (`body.image_urls`): rejects if the reference contains a recognizable real person.
- **Output-side** (`body.generated_video`): rejects AFTER generation if the produced clip contains recognizable-looking faces — and every broadcast cutaway has a crowd full of faces.

The output-side gate is unavoidable for this trend regardless of subject, so Seedance is functionally unusable here. Kling is the engine that works **for ordinary user photos**.

**Kling caveat — recognizable celebrities are blocked too.** Kling has its own content-moderation gate that fires on celebrity references (validated 2026-05-13: a Michael Jordan reference + "Ke Wang" chyron returned `task_status: failed, task_status_msg: "Failure to pass the risk control system"` at submit-time). This is correct behavior — the trend illusion only works with a non-public-figure reference where the chyron name + face are coherent. If a user supplies a celebrity photo, surface the gate to them and ask for a non-celebrity reference instead.

**Kling trade-offs**: 2500-char `prompt` cap (recipe above is pre-trimmed), no `seed` param (re-rolls are non-reproducible — to re-roll just call again).

## Runtime expectations

Typical run time is 4-7 minutes:

| Step | Wall clock | Notes |
|---|---:|---|
| Reference upload | 5-30s | Skip when the user supplies HTTPS |
| Broadcast still | 60-120s | Re-roll before video if the chyron or scorebug is wrong |
| Kling video | 3-5 min | One 15s pro render with native commentary |
| Delivery check | <30s | Verify final URL and obvious identity/chyron continuity |

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Chyron pops in mid-clip (~4–5s flash) | Chyron not baked into the still | Re-run Step 1; verify chyron is visible in `state.broadcast_still_url` before Step 2 |
| Scorebug animates / morphs mid-clip | `prompt_adherence` not `strict`, or `negative_prompt` was trimmed | Restore strict adherence and the full negative_prompt |
| Identity drift late in the clip (face changes after ~10s) | Reference image too small / Kling losing the face | Re-run Step 2; if drift persists, re-run Step 1 with a tighter face crop on the still (more facial pixels = stronger lock) |
| Username mispronounced by announcers | Native audio is one take | Re-run Step 2 |
| Seedance `partner_validation_failed` 422 | Tried Seedance instead of Kling | Use Kling only — see engine-choice section above |
| Kling `task_status: failed` with `task_status_msg: "Failure to pass the risk control system"` | Reference photo is a recognizable celebrity / public figure | Ask the user for a non-celebrity reference. Kling correctly blocks impersonation patterns (celebrity face + fake-event chyron) |
| `generate_image` 400 `invalid_image_file` from `openai v1/images/edits` | Reference is an iPhone HEIC-derived JPEG with heavy EXIF and/or extreme aspect ratio (e.g. 2316×3088) | Re-encode the reference before upload: `convert in.jpg -strip -auto-orient -resize 1536x1536\> out.png`, then upload the cleaned PNG |
| `quality: "high"` runs feel slow (~2 min/call) | gpt-image-2 high is a deliberately slower fidelity tier, not a bug — upstream typical is around two minutes per the manifest | Wait it out — most runs return cleanly. If a specific run does fail, retry once; fall back to `quality: "medium"` only if it persists |

## What NOT to do

- Don't sport-swap. NBA / NFL / soccer variants → fork this skill; don't parameterize this one.
- Don't add suffixes to the chyron (e.g. " - AI Creator"). Chyron is the username alone — the trend illusion depends on it reading like a real broadcast identifier.
- Don't add post-edits — no `add_captions`, `generate_music`, `edit_*`. Kling burns the scorebug + chyron + native commentary directly; anything added afterward breaks the broadcast illusion.
