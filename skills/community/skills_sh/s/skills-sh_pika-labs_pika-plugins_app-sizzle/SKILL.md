---
name: app-sizzle
description: >
  Generate cinematic 1080p iOS app teaser videos from real App Store screenshots,
  with a GPT-image-2 enhancement pass on each selected screen before generation.
  Output is a beat-driven cinematic teaser built from GPT-enhanced screenshots,
  ending with the brand logo/icon plus a deterministic `COMING SOON` overlay.
  Screens sourced from Pika MCP App Store fetch, a live website (auto-captured), user-supplied files, or URLs.
  Starts by sourcing real screens and brand assets before any generation.
  Triggers on: app sizzle, app teaser, app promo, iOS app promo video, app video,
  app product video, coming soon, seedance, motion graphics, make a promo for my
  app, make a video for [app], gpt enhance promo.
  NOT for: short-form consumer content like GRWM, vlogs, UGC, or non-app product
  ads (use content-video); app-sizzle is specifically for iOS app teaser videos
  sourced from App Store screens or real app UI.
argument-hint: <app-name-or-url> [screens=<app-store-url|website-url|paths>] [logo=<path-or-url>] [aspect=16:9|9:16|1:1]
required-capabilities:
  - mcp__pika__capture_website
  - mcp__pika__fetch_appstore_screens
  - mcp__pika__generate_image
  - mcp__pika__generate_reference_video
  - mcp__pika__edit_text_overlay
  - mcp__pika__task_status
  - mcp__pika__upload_asset
---

# App Sizzle — GPT-Image-2 Enhanced iOS App Teaser

Generate a polished 15-second app teaser from real app screens. Each selected screen is passed through GPT-image-2 before Seedance so compressed captures become cleaner references without inventing UI.

**Generation contract:** use `resolution="1080p"`, `duration=15`, and `sound=True`. Skip `fast=true` because it caps Seedance at 720p. The skill owns duration and sound so the user only has to supply app identity, screens, logo, and aspect ratio.

The visual aesthetic is **derived from the app's personality** — not defaulted to liquid glass. The agent reads the app's soul from its icon, screenshots, and category, then chooses a treatment. The user provides the app identity and assets; the agent decides everything else (mode, prompt, camera, style).

---

## Mode: Reference-to-Video

Primary: `mcp__pika__generate_reference_video(provider="seedance", resolution="1080p")` with 3–5 screenshots + the app icon/logo as the final reference.

Fallback to `provider="kling", quality_mode="pro"` (= 1080p) when:
- Seedance returns non-audio `partner_validation_failed` (celebrity faces, screen-recording UI)
- Seedance returns `insufficient_balance`
- Seedance stays queued/running until it returns a timeout such as `seedance timed out after ...`

Do not treat generated-audio moderation as an immediate Kling fallback. See the Seedance generated-audio moderation recovery runbook in Generate Video first.

Kling prompt uses `<<<image_1>>>` … `<<<image_5>>>` tokens instead of `@Image1` … `@Image5`. Drop the `resolution` param (Kling uses `quality_mode` instead). See Gotchas.

---

## Stage 0 — Asset Sourcing

If invoked with empty args and no relevant prior context, print this menu verbatim and stop. Do not call tools until the user supplies the app identity and screen source.

```
To make your app promo, I need:

1. App name + one-line description of what it does
   (e.g. "Nova — an AI journaling app for iOS")

2. Where should I pull the app screens from?
   — iOS App Store: give me the App Store URL or app name → I'll use
     `mcp__pika__fetch_appstore_screens` to fetch screenshots, metadata, and icon
   — Web app / website: give me the URL → I'll capture it with Pika MCP
   — Local files / URLs: drop the paths and I'll upload them

3. Brand logo — path or URL (preferred) or skip to use the App Store icon
   The logo anchors the end card and prevents Seedance from hallucinating brand text.
   If you don't have a logo file, use the fetched App Store icon as the fallback.

4. Aspect ratio: 16:9 (landscape/YouTube) / 9:16 (Reels/TikTok) / 1:1
```

If the trigger message or prior context already supplies part of this, ask only for the missing required fields before touching any tool. These are the only questions the user needs to answer; the agent decides mode, prompt, camera, and style.

Once answered, the agent:
1. Sources the screens (MCP App Store fetch / website capture / upload local files)
2. **Analyzes each screen** (Stage 1) — reads every screenshot, maps UI → feature
3. **Designs the narrative arc** (Stage 2) — builds a 15s story structure before touching the prompt
4. Selects the 3–5 best screens for the promo (ordered by narrative role)
5. Uploads logo + screens to get public URLs
6. Writes the screen-specific prompt (Template A or B)
7. Generates at 1080p

---

## Stage 0.5 — Asset Gate

Before calling any generation tool, verify both assets are in hand:

| Asset | Required | If missing |
|-------|----------|------------|
| Real app screenshots (≥1 actual sourced image) | Yes | Stop and ask for screenshots |
| Brand logo OR app icon | Yes | Use the `mcp__pika__fetch_appstore_screens` icon when App Store sourcing is used; otherwise stop and ask for a logo/icon |

If either is missing, tell the user exactly what's needed and wait. Real assets are what keep the teaser grounded; text-to-video placeholders make Seedance invent UI.

Avoid:
- Generate using text-to-video as a substitute when screens were expected
- Describe imaginary UI in the prompt ("a dark dashboard with…") without a real reference image
- Proceed with "I'll use a placeholder for now"
- Make up what the app looks like from its name or description

The only acceptable path forward is real assets from the user. If MCP fetching or
capturing failed (App Store returned nothing, website screenshot errored), report
what happened and ask the user to provide the screens manually. Never invent them.

---

## Screen Sourcing

### iOS App Store

Use Pika MCP `mcp__pika__fetch_appstore_screens`; do not use a local scraper. It accepts a full App Store URL, numeric app ID, or app-name search term:

```
fetch_appstore_screens(
  query: <app_store_url | numeric_app_id | search_term>,
  country: "us",
  max_screens: 10,
  include_icon: true
)
```

Expected result shape:

```
{
  "app_url": "https://apps.apple.com/...",
  "metadata": { "name": "...", "subtitle": "...", "description": "...", "category": "...", "icon_url": "https://..." },
  "icon": { "url": "https://cdn.pika.art/...", "source_url": "https://is...mzstatic.com/...", "filename": "appstore-icon.png", "mime_type": "image/png", "width": 1024, "height": 1024 },
  "screenshots": [
    { "url": "https://cdn.pika.art/...", "source_url": "https://is...mzstatic.com/.../1290x2796bb.png", "filename": "appstore-screen-01.png", "mime_type": "image/png", "width": 1290, "height": 2796 }
  ],
  "count": 1
}
```

If `mcp__pika__fetch_appstore_screens` returns no screenshots, report the error and ask the user for 3-5 real screenshots plus a logo/icon. Do not fall back to Playwright/headless App Store capture and do not invent UI.

After App Store assets are fetched, pick the 3–5 screens that show the core UI. Skip:
- Pure text/splash screens (no UI)
- Blank or loading states
- Screens with faces (may trigger content policy)

**Screen selection principle — maximize visual contrast.** Each selected screen should look as different as possible from the others: dark vs. light background, UI-dense vs. photo-heavy, micro close-up vs. wide grid, minimal vs. busy. If all your screens look similar, Seedance blends them into a visual mush. What made Dazz Cam work: 3D camera grid + Polaroid output + VHS panels + fisheye orb — four completely distinct visual worlds. What makes teasers fail: four screens of the same UI at slightly different scroll positions.

### Web App / Website (auto-capture)

Use Pika MCP's capture tool:

```python
capture_website(url="https://example.com", mode="screenshot")
# Returns image_url — use directly as a reference
```

Call once per distinct page/view you want to include.

### Local Files

User provides paths → upload each via Pika MCP (see Asset Upload section below).

---

## Stage 1 — App Analysis

After sourcing screens, **read every screenshot** using Claude's vision before writing a single word of prompt. This is the most important step — skip it and you get a generic glass blob with no story.

For each screenshot, record:
- **What UI is shown** — e.g. "chat input with suggested prompts", "video timeline with AI edit chips", "agent result card showing a generated clip"
- **What feature it represents** — e.g. "creation entry", "agent at work", "output/share"
- **Emotional register** — is this the power moment, the ease moment, the aha moment?

Also pull the app metadata from the `mcp__pika__fetch_appstore_screens` result, or from the user-provided description:
- App name, subtitle, one-line value prop
- Category and target user

**Output of Stage 1:** A numbered feature map:
```
Screen 1 — [filename]: Shows [X UI]. Represents [Y feature]. Moment: [hook/build/reveal].
Screen 2 — [filename]: ...
...
```

After the map, score each screen for **visual uniqueness**: does it look completely different from the others you've mapped? Prefer screens with distinct color palettes, distinct layout density, and distinct subject matter. A great set has maximum visual spread — the hook should feel nothing like the build, which should feel nothing like the reveal.

Do NOT proceed to Stage 2 until this map is written out.

---

## Stage 2 — Narrative Architecture

Every 15s promo needs a spine. Design the story arc before touching the prompt template.

### The 4-beat structure

| Beat | Seconds | Job | Which screen(s) |
|------|---------|-----|-----------------|
| **Hook** | 0–3s | Grab attention — show the most dramatic UI moment or the problem being solved | The most visually striking screen |
| **Build** | 3–10s | Feature walkthrough in logical user-journey order | 2–3 screens in sequence |
| **Reveal** | 10–13s | Pull-back or product overview — the "so that's what it does" moment | Wide shot or most complete screen |
| **Logo** | 13–15s | Brand lock — wordmark materializes, accent color pulse | Logo (@Image6 or last ref). `COMING SOON` is added later as a post-generation text overlay. |

### Story arc types — pick one based on the app

| Arc | When to use | Structure |
|-----|------------|-----------|
| **Problem → Solution** | Productivity/tool apps | Hook = pain point UI → Build = app solves it → Reveal = result |
| **Feature Parade** | Feature-rich apps | Hook = most impressive feature → Build = 2 more features → Reveal = overview |
| **Journey** | Consumer/lifestyle apps | Hook = entry point → Build = the experience → Reveal = outcome |
| **Transformation** | Before/after type apps | Hook = the "before" → Build = the process → Reveal = the "after" |

### Output of Stage 2

Write out the arc explicitly before generating:
```
Arc type: [Problem→Solution / Feature Parade / Journey / Transformation]
Hook (0-3s): Screen [N] — [what happens] — camera: [extreme close-up on X]
Build (3-10s): Screen [N] → [N] → [N] — [what each reveals] — camera: [whip pan / orbital / etc.]
Reveal (10-13s): Screen [N] — [what it shows] — camera: [pull-back to show full product]
Logo (13-15s): @Image[N] — wordmark materializes whole in a burst of [accent color] light and holds. Do not ask the video model to render the `COMING SOON` copy; it is added later as a post-generation text overlay.
```

Do NOT write the Seedance prompt until this arc is defined.

---

## Stage 2.5 — GPT-Image-2 Enhancement

After the arc is defined and the 3–5 screens are selected, enhance each one with GPT-image-2 before uploading to Seedance. This lifts compressed website captures and App Store thumbnails to a cleaner, higher-fidelity reference.

For each selected screen (including the logo/end card reference):

```python
result = generate_image(
    provider="gpt-image-2",
    prompt="High quality version, preserve all content exactly",
    reference_images=["<original_cdn_url>"],
    aspect_ratio="16:9",   # match the capture — use 9:16 for portrait screens
    quality="medium",
)
# use result.image_url (or result.url) as the Seedance reference
```

**Rules:**
- Keep the prompt exactly as shown — short, non-descriptive. Describing the image content makes GPT-image-2 hallucinate new details.
- Match `aspect_ratio` to the original capture (desktop = 16:9, mobile = 9:16).
- Run all enhancements in parallel (one call per screen).
- Use the enhanced URLs as the `reference_images` array in the Seedance call — not the originals.
- Keep your Stage 1 feature map descriptions unchanged — they describe the original content, which the enhanced image preserves.

---

## Stage 3 — Prompt Writing

With the feature map (Stage 1) and arc (Stage 2) in hand, write the Seedance prompt. Every `@Image` description must reference the real UI content from the feature map — never write generic descriptions like "a mobile interface with controls."

**Choose the template by reading the app's screenshots — don't default to liquid glass.** Read exactly one of these based on the app's personality; the other never loads:

- **Template A — Cinematic Narrative** (default; productivity, AI, creative, social, food, games): read `references/template-a-cinematic.md`. The proven BEAT-structure template plus validated examples.
- **Template B — Liquid Glass** (photography, camera, filter apps only, where a lens/filter metaphor is apt): read `references/liquid-glass.md`. Template B skeleton plus glass transformation vocabulary.

The accent color is always from the brand — read the icon and primary UI color, never invent one.

### Rules for both templates

- Every `@Image` description comes directly from the Stage 1 feature map
- Camera directions come directly from the Stage 2 arc
- Never write "the app interface" or "a mobile screen" — be specific
- Keep under 200 words
- **Why specificity matters:** Seedance uses `@ImageN` description as its primary brief — "a dark chat interface" vs "a VHS three-panel grid of city streets, a skate park, and a coastal sunset with retro timestamp overlays" produce completely different results. Copy the most visually specific details from your Stage 1 feature map verbatim.

---

## Generate Video

**Primary — Seedance:**
```python
generate_reference_video(
    provider="seedance",
    reference_images=["<url1>", "<url2>", "<url3>", "<url4>", "<url5>"],  # 3–5 screens + icon
    prompt="<prompt using @Image1 … @Image5 tokens>",
    resolution="1080p",   # always
    duration=15,          # always
    sound=True,           # always
    aspect_ratio="16:9",  # or 9:16 / 1:1 per user request
    seed=<int>,           # set one; reuse it for content-policy recovery
)
```

### Seedance generated-audio moderation recovery

If Seedance finishes generation and then returns a 422 whose body includes `type: "content_policy_violation"`, `reason: "partner_validation_failed"`, `loc: ["body", "generated_video"]`, and `msg: "Output audio has sensitive content."`, treat it as a recoverable generated-audio moderation false positive.

1. Retry the exact same prompt and `reference_images` with `sound=False` and the same `seed`.
2. If the silent probe succeeds, retry the exact same prompt/reference set with `sound=True` and the same seed.
3. If the `sound=True` replay succeeds, route the recovered sound-on URL into Stage 4 as `generated_teaser_url`. Keep the silent probe URL only as debugging context.
4. If the silent probe fails, treat the failure as video/reference moderation and use the Kling fallback.
5. If the silent probe succeeds but the `sound=True` replay fails again, run the Kling fallback once. If Kling is unavailable, route the silent URL into Stage 4 as `generated_teaser_url` and explicitly note that generated-audio moderation remained flaky.

Do not change the prompt, references, aspect ratio, duration, or seed during this recovery path. Changing any of them turns the silent probe into a new generation instead of testing whether only generated audio triggered moderation.

### Seedance timeout recovery

If task status remains queued or running until Seedance returns a timeout such as `seedance timed out after 900s` or `seedance timed out after 1200s`, treat it as provider queue saturation, not a prompt/content failure.

When this happens, run the Kling fallback with the same selected references, same beat structure, `duration=15`, `sound=True`, and `quality_mode="pro"`. Convert `@ImageN` prompt tokens to `<<<image_N>>>` before calling Kling.

Do not keep retrying Seedance after a timeout unless the user explicitly asks to wait for Seedance. The timeout path has already spent the launch-demo wall-clock budget; switching provider is the documented recovery.

**Fallback — Kling (non-audio partner_validation_failed or insufficient_balance):**
```python
generate_reference_video(
    provider="kling",
    reference_images=["<url1>", "<url2>", "<url3>", "<url4>", "<url5>"],
    prompt="<prompt using <<<image_1>>> … <<<image_5>>> tokens>",
    quality_mode="pro",   # = 1080p on Kling (NOT resolution=)
    duration=15,
    sound=True,
    aspect_ratio="16:9",
)
```

**Seedance tokens:** `@Image1` … `@Image5` | **Kling tokens:** `<<<image_1>>>` … `<<<image_5>>>`

Seedance constraints: skip `fast=True` because it caps at 720p; skip `negative_prompt` because Seedance rejects it; skip `auto_duration` because this path is fixed at 15s.

Kling constraint: use `quality_mode="pro"` for 1080p; Kling rejects `resolution=`.

### Kling queued/handoff recovery

Kling fallback is async. If `generate_reference_video(provider="kling")` returns a `task_id`, follow the task until terminal.

If `task_status` returns status: `queued` with `statusMessage` containing `Worker handoff: task was requeued for retry on another worker.`, treat it as a worker restart handoff, not a failed render. Keep polling `mcp__pika__task_status(task_id)`; the next worker should reclaim the same task.

If `statusMessage` starts with `Kling is at capacity`, treat it as provider capacity wait. Keep polling the same task while `lastUpdatedAt` continues moving.

Do not submit a duplicate Kling request while the original task is still `queued` or `running`. Duplicates can burn provider quota and make artifact provenance unclear.

If `status` stays `queued` for more than 10 minutes with no `lastUpdatedAt` movement, capture the `task_id`, `status`, `statusMessage`, and `lastUpdatedAt`, then cancel the stalled original with `mcp__pika__task_cancel(task_id)` before retrying. Only after cancel returns `cancelled`, retry the exact same Kling request once with the same prompt, references, shots, aspect ratio, duration, and quality mode. If cancel fails because the task already completed or failed, inspect that terminal result instead of retrying. If the retry also stalls, stop and report both task IDs instead of changing the creative prompt.

---

## Asset Upload (local files → public URL)

If the user provides local file paths, convert them to public URLs before calling generate:

1. Read the file size and MIME type.
2. Call `mcp__pika__upload_asset(filename, mime_type, size_bytes)`.
3. Upload the bytes to the returned `presigned_url` using the host client's file-upload capability.
4. Use the returned `public_url` as the reference URL in generation calls.

Supported mime types: `image/png`, `image/jpeg`, `image/webp`, `video/mp4`, `audio/mpeg`, `audio/wav`

---

## Stage 4 — Deterministic COMING SOON Overlay

Do not ask Seedance or Kling to render `COMING SOON`. Video models garble new
typography, especially all-caps CTA text, so the final two seconds use a
deterministic `COMING SOON` overlay as a post-generation text overlay.

After Seedance or Kling returns the 15s teaser URL, call:

```python
edit_text_overlay(
    video_url=<generated_teaser_url>,
    text="COMING SOON",
    position="bottom_center",
    font_size=56,
    font_color="white",
    start_s=13,
    end_s=15,
)
```

If `edit_text_overlay` returns `{ task_id }`, poll `mcp__pika__task_status`
until it reaches `completed`, `failed`, or `cancelled`, then unwrap the returned
URL. Save the returned URL as `final_url`. If the overlay call fails, surface
that failure and the unoverlaid teaser URL as a diagnostic preview; do not
deliver a teaser whose only `COMING SOON` text was generated by the video model.

---

## Result Delivery

Return the final Pika CDN URL as the primary deliverable. If the host client requires local media markers, create that local preview outside this skill flow after confirming the CDN URL is reachable.

**If generation completes asynchronously:** follow the MCP tool's returned status handle until the video reaches a terminal state, then deliver the final URL.

---

## Prompting Guide

> **The prompt is the output of Stages 1 + 2, not a starting point.** Never fill in the template from imagination — fill it from the feature map and arc you built. A prompt written without Stage 1 analysis will produce a generic glass blob.

### Camera Vocabulary

Use specific camera language — Seedance responds to it:

| Term | Effect |
|------|--------|
| `extreme macro close-up on [specific element]` | Tight detail shot — glass edge, button, icon |
| `crash zoom into [element]` | Fast push-in, creates energy |
| `whip pan to` | Hard lateral cut with motion blur |
| `orbital sweep around` | 360° arc around the floating panel |
| `push-in drift` | Slow, cinematic dolly |
| `pull-back to reveal` | Classic product reveal — shows full form |
| `hard cut to black` | Clean beat before logo |

Alternate fast cuts with slower drifts — pure rapid cuts feel chaotic, pure slow drifts feel boring.

(Glass transformation vocabulary lives in `references/liquid-glass.md` — only relevant on the Template B path.)

### Device Framing

For product shots, lock the device to a black void — never place in environments:

```
# Floating desktop screens (SaaS / desktop apps)
Show the desktop screens floating in 3D space on a pure black background, tilted at
slight angles like a MacBook product shot. The UI elements on screen become translucent
glass with reflections and refractions. No text, no logos, no words.

# iPad reveal
An iPad Pro floating in empty black space, tilted at a cinematic angle like an Apple
product shot. The iPad is a real solid device with visible bezels — only the screen
content has the glass effect. The device slowly rotates. No text, no logos.

# MacBook
A MacBook Pro floating in empty black space, open at a cinematic angle. The screen
displays [content]. Light catches the aluminium edges. No text, no logos.
```

### Reference Count Guide

All runs are 15s, 1080p. Select 3–5 screens based on the narrative arc.

| Refs | Use case |
|------|----------|
| **3** | Standard — one screen per beat (hook / build / reveal) + icon as @Image4 |
| **4** | Two build beats + hook + icon |
| **5** | Feature-rich — hook + 3 build beats + icon. Don't exceed 5. |

**The golden rule: 1 reference per ~3 seconds of video.**

---

## Load-bearing phrases

These phrases are empirical prompt/flow anchors. Keep them when simplifying the skill:

| Phrase | Where | Why load-bearing |
|---|---|---|
| `High quality version, preserve all content exactly` | GPT-image-2 enhancement pass | Keeps the enhancement pass from inventing UI while cleaning compression artifacts. |
| `Do NOT write the Seedance prompt until this arc is defined` | Stage 2.5 gate | Prevents generic motion prompts that are not grounded in the selected screens. |
| `The prompt is the output of Stages 1 + 2, not a starting point` | Prompting guide | Forces the agent to use the screen feature map and story arc instead of template-filling from imagination. |
| `pure black background` / `floating in empty black space` | Device framing prompts | Keeps product shots focused on the app UI rather than hallucinated environments. |
| `materializes whole` / `crystallizes as a single form` / `fades in as a complete element` | Logo reveal wording | Avoids per-letter logo construction, which causes garbled brand text. |

---

## Runtime Expectations

Typical run time is 4-8 minutes:

| Step | Wall clock | Notes |
|---|---:|---|
| Asset sourcing | 10-60s | App Store via `mcp__pika__fetch_appstore_screens`; website capture depends on page load |
| Screen analysis + arc | 2-5 min | User confirmation can add time |
| GPT-image-2 enhancement | 30-90s | Run selected screens in parallel |
| Seedance generation | 3-5 min | Generated-audio moderation recovery adds one silent probe plus one same-seed sound replay |
| Kling fallback | 5-15 min | Capacity wait or worker handoff may temporarily show `queued`; follow the Kling queued/handoff recovery runbook |
| Download verification | <30s | Local sanity check before delivery |

## Engine Choice: Seedance Primary, Kling Fallback

Seedance is the default because it handles polished motion-graphics references and 1080p app teasers well. Kling is the fallback for moderation, balance, or Seedance timeout failures because it is more permissive on some screen content and uses `quality_mode="pro"` for 1080p.

## Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| `fast=True` with `resolution="1080p"` | Seedance caps fast mode at 720p | Remove `fast`; keep `resolution="1080p"` |
| `negative_prompt` rejected | Seedance does not accept this field | Use positive framing such as "smooth motion, stable camera" |
| Seedance generated-audio moderation: `content_policy_violation` / `partner_validation_failed`, `generated_video`, "Output audio has sensitive content." | Often a false positive on non-sensitive app-sizzle references | Follow the generated-audio recovery runbook: same-seed `sound=False` probe, then same-seed `sound=True` replay |
| Seedance timeout such as `seedance timed out after ...` | Provider queue saturation or tail latency exceeded the tool budget | Run the Kling fallback; do not keep retrying Seedance unless the user explicitly asks to wait |
| Seedance `partner_validation_failed` on video | Screen content includes recording UI, celebrity faces, or similar moderation triggers | Switch to `provider="kling"` and convert tokens to `<<<image_N>>>` |
| Faces in screenshots trigger content policy | Screenshot includes real people | Crop faces out before upload, or use Kling |
| 6+ reference images reduce quality | The model blends too many refs | Keep to 3-5 references, roughly one per 3 seconds |
| Prompt tail ignored | Prompt exceeds about 200 words | Trim to the beat structure and the concrete UI details |
| Text in output is garbled | Video model is asked to render new text | Keep text as existing reference-image content; overlay any new branding in post |
| Logo reveal hallucinates letterforms | "assemble/build/construct" language triggers per-glyph rendering | Use "materializes whole", "crystallizes as a single form", or "fades in as a complete element" |
| Task returns `{ task_id }` instead of inline | Long-running generation exceeded inline budget | Poll `mcp__pika__task_status(task_id)` until `completed`, `failed`, or `cancelled`; unwrap `result.structuredContent` when present |
| Kling task returns status: `queued` after previously running | Worker handoff or provider capacity wait | Follow the Kling queued/handoff recovery runbook; do not duplicate-submit unless queued for more than 10 minutes with no `lastUpdatedAt` movement |
| Kling rejects `resolution=` | Kling uses a different quality knob | Use `quality_mode="pro"` |
| App Store icon URL points to promo art | App Store metadata fallback found feature artwork | Prefer the `icon.url` returned by `mcp__pika__fetch_appstore_screens`; if missing, ask for a logo/icon file |
