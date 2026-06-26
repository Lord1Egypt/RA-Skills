---
name: ugc-ads
description: >-
  Multi-cut jump-cut UGC product ad — HOOK + 3 JUMP CUTs + OUTRO, 15s, 9:16
  vertical (3:4 optional, seedance only), POV first-person talking-head selfie,
  every beat has spoken dialogue with native lip-sync, 5-act narrative arc
  (set → name → reveal → twist → punchline). Six category essences
  (HAUL / APP / FOOD / BEAUTY / FITNESS / TECH) auto-picked from the input URL.
  Creator-style raw UGC talking-head with multi-beat conversational dialogue.
  Use when the user asks to "make a UGC ad", "jump-cut product ad",
  "POV product reveal", "creator-style ad", "haul-style ad", "unboxing ad",
  "TikTok-style product video", or "talking-head ad about [URL]".
argument-hint: <url> [avatar_url=<url>] [provider=seedance|kling] [aspect_ratio=9:16|3:4] [category=auto|HAUL|APP|FOOD|BEAUTY|FITNESS|TECH] [captions=true]
---

# /pika:ugc-ads

## Parameters

| Param | Default | Notes |
|---|---|---|
| `url` | required | product URL — drives category detection and beat substitution |
| `avatar_url` | built-in fallback | persona portrait URL; fed as `@Image1` reference. When omitted, the skill uses a pre-generated Pixar-style female creator portrait |
| `provider` | `seedance` | seedance: strong at UGC selfie / talking-head POV with native lip-sync, multi-segment in single prompt, supports 3:4. kling: explicit `shots[]`, 9:16/16:9 only |
| `aspect_ratio` | `9:16` | `3:4` is seedance-only (kling rejects 3:4) |
| `category` | auto | `HAUL` / `APP` / `FOOD` / `BEAUTY` / `FITNESS` / `TECH`; auto-picked from URL |
| `captions` | `true` | TikTok-style word-chunked captions burned on top of the final video |

## Runtime expectations

Typical end-to-end run: **6–12 minutes**. Breakdown:

- Step 1 (WebFetch) + Step 3 (capture_website screenshot): ~10–30s
- Step 7 (`generate_reference_video`): ~3–5 min for seedance, ~5–7 min for kling
- Step 7b/c (cartoonize + retry): adds ~1–2 min if seedance moderation rejects the avatar
- Step 8 (captions): single `add_captions` call, ~30s–5 min (transcribe + burn in one shot)

If the run exceeds 15 min without progress, something is wrong — inspect the tool-reported generation status and error message.

## Engine choice: Seedance default, Kling fallback

Default to Seedance for UGC selfie/talking-head ads because it handles native lip-sync, single-prompt multi-beat pacing, and optional 3:4 output well. Use Kling when the caller explicitly passes `provider=kling` or when Seedance moderation keeps rejecting the avatar after the cartoonized retry. Kling's tradeoff is stricter aspect-ratio support but a separate moderation path and explicit shot segmentation.

## Steps

### 0. Resolve input (empty-args menu)

Strip flags and `key=value` parameters from `$ARGUMENTS`. If no product URL remains and there is no usable product URL in prior context, print this menu and stop:

> **Which product should the UGC ad promote?** Required:
>
> - **Product URL** — page to fetch for product name, category, visual references, and language
>
> Optional: `avatar_url=`, `provider=seedance|kling`, `aspect_ratio=9:16|3:4`, `category=auto|HAUL|APP|FOOD|BEAUTY|FITNESS|TECH`, `captions=true|false`.

If the product URL is present, skip this step silently.

### 1. Fetch + categorize

`WebFetch` the URL: pull `product_name`, value prop, brand color, product form, packaging, hero copy, target user, category, **and the primary language of the page**. Use `category=` if passed; else trust the WebFetch signal; fall back to HAUL for physical, APP for digital.

### 2. Resolve the avatar (fallback to built-in if missing)

- If `avatar_url` was passed → use it as-is.
- If NOT passed → use this built-in fallback:
  ```
  https://cdn.pika.art/v2/files/agent/17d62bf9-0edb-49e4-9ba9-2c5419fa518f/seedream-1777624057811.jpeg
  ```
  Pre-generated 3D animated Pixar-style portrait of a young female creator — pre-cartoonized so seedance moderation accepts it directly, neutral enough to fit any category. Note in the final summary that the fallback was used so the caller knows to supply their own portrait for persona consistency next time.

### 3. Capture the product screenshot (best-effort)

Call `capture_website` with `mode: "screenshot"`. Use `mobile=true` for handheld-product categories (APP / FITNESS / BEAUTY) so the captured page renders as a portrait phone screen; `mobile=false` for desktop-context categories (HAUL / TECH / FOOD).

If the call fails (timeout, browser pool down), retry **once**. If still failing, proceed without the screenshot — the skill is degraded but functional. The close-up beat then describes the page from prose only and Beat 2's `reference_images` is just `[avatar_url]`.

Capture URL → `screenshot_url` (or null).

### 4. Compose the prompt

The full prompt is a single multi-beat string passed to **one** `generate_reference_video` call. Structural prose (not markdown bullets). Every beat has a `Says: "..."` line for lip-sync. Pacing target ~5.5–6 words per second across the whole 15-second ad (≈85–90 words total). `@Image1` is the avatar, `@Image2` is the screenshot when available.

**Write all `Says: "..."` lines in the language detected from step 1's WebFetch.** Both seedance and kling lip-sync handle multilingual; if the product page is Chinese / Japanese / Spanish / etc., the dialogue should be in that language. Hook archetypes from step 5 are language-agnostic — adapt the rhetorical move to the language's natural register.

```
HOOK (0–3 sec) <visual setting + creator framing + face/body cue>. Says to camera, fast and energetic: "<hook line>". <style anchor — POV handheld, authentic, raw>.

JUMP CUT 1 (3–6 sec) <wide POV — creator's body language, product partially in frame edge>. <face cue>, says fast: "<setup line>".

JUMP CUT 2 (6–9 sec) <next visual beat — could be the screen close-up showing @Image2 OR another reaction beat, depending on which beat the dialogue arc puts the reveal>. Says (or voice continues over the shot if it's a screen close-up), fast and confident: "<reveal line>".

JUMP CUT 3 (9–12 sec) <next visual beat — same logic; one of the JUMP CUTs is the screen close-up, the others are wide-POV reaction shots>. Says, fast: "<insight twist line>".

OUTRO (12–15 sec) <selfie POV, mid-chest framing, same setting>. Says to camera, fast: "<punchline line>".

avatar is image 1, asset is image 2
```

**Screen-close-up beat — exactly one across the ad, position is dialogue-driven:**
- Place the screen close-up on whichever JUMP CUT (1, 2, or 3) the *reveal* line lands on. Most ads put it on JUMP CUT 2; if the narrative needs it earlier or later, JUMP CUT 1 or JUMP CUT 3 is fine. Pick by content, not by slot number.
- The screen close-up beat shows `@Image2` exactly as-is and includes ONE finger-point gesture (a single finger entering from the frame edge, pointing at the hero text or product — no tap, no swipe, no scroll, no hover-on-CTA). The point gesture is the only screen interaction in the entire ad.
- The other JUMP CUTs are wide-POV reaction beats: hands stay on knees, on the bed, or at sides.

**Trust `@Image2`** — when the product page is shown, reference the image; do NOT describe its UI in prose. Describing UI triggers the model to invent extra panels / dropdowns / sidebars / animations. Reference the image; trust it.

### 5. Category essences

Each essence is the brief you read before composing the 5 beats. Pick one from category in step 1 and write the actual `Says: "..."` lines tailored to the real product.

#### HAUL_UNBOX
- **When to use & why**: fashion, handbags, jewelry, shoes, designer drops, streetwear, luxury cosmetics with packaging story, accessories — anything where brand packaging + texture/material is the value prop. Viewers convert on vicarious-unboxing dopamine + "I just got this" social proof; texture and hardware ARE what the customer pays for, so the close-up lands on materials, not function. Not TECH (→ TECH_UNBOX), not skincare/makeup application (→ BEAUTY_APPLY).
- **Sensory anchors**: tissue rustle, fabric slide, hardware clinks (chains / clasps / buckles), leather/fabric grain under fingertips, foil glint.
- **Setting**: white unmade bed in natural window light; bathroom mirror in background for the outro held-up reveal; streetwear drops may use desk/floor.
- **Close-up beat device**: NOT a screen — product close-up. `@Image2` is a product photo (or brand-site mobile view); the single finger-point lands on a hardware detail (chain, clasp, embossed logo).
- **Dialogue character**: hook is **mystery tease** — frame the unboxing as something the viewer doesn't yet know the contents of; do NOT name the product in the hook line. Arc: hook the unboxing mystery → brand name + drop context → reveal the material/silhouette while close-up holds on hardware → tactile/wearability insight (how it feels on the body) → punchline that invites the viewer to imagine themselves with the artifact.

#### APP_REVEAL
- **When to use & why**: SaaS, AI tools, mobile/web apps, agent-style products, dev tools, productivity tools — anything where the screen IS the product. Viewers convert when they see live UI doing the thing in <5 seconds; the close-up beat is the demo, the bookends are the social proof. Not pure hardware (→ TECH_UNBOX).
- **Sensory anchors**: micro-thumb gesture, brand-color highlight, UI alive with small motion, ambient room tone.
- **Setting**: cozy bedroom or couch POV; jeans/joggers at frame edges; warm window light.
- **Close-up beat device**: laptop on bed (desktop screenshot) or phone in hand (mobile screenshot — set `mobile=true` in step 3).
- **Dialogue character**: hook is **bewildered curiosity** — the creator can't categorize the thing yet, that's the point. Do NOT use feature lists or marketing language in the hook; lean into "I don't know what to call this" / "this is wild" register that makes the viewer wait for the name. Arc: bewildered hook → name the product + interaction model in human terms ("you just talk to it", "it builds X from Y") → reveal what it produces (concrete comma-separated examples) while close-up shows the page → personal-insight twist (what it replaces / changes in the user's workflow) → punchline + implicit/explicit "go try it" CTA.

#### FOOD_ASMR
- **When to use & why**: food brands, drinks, kitchen tools, snacks, restaurants with a takeout product — anything where the sensory peak (pour / sizzle / steam / first bite) carries the value prop. Viewers convert on hunger response — show the sensory peak, don't describe it.
- **Sensory anchors**: packaging rustle, knife-on-board, sizzle, pour stream, steam rising, satisfied exhale on the first bite.
- **Setting**: marble counter or warm wood kitchen, top-down framing.
- **Close-up beat device**: a product/dish close-up rather than a screen; phone in hand on the counter only if the brand has a delivery/recipe app.
- **Dialogue character**: hook is **show-don't-tell** — frame as a demonstration the viewer is watching unfold, not a description. The hook line lands while a hand or first ingredient is already in motion; the visual carries the curiosity. Arc: demonstration hook → name the product + first impression → narrate the sensory peak as it happens (pour / sizzle / steam) → satisfaction insight ("this is the new default") → punchline that hands off the recipe or shop link.

#### BEAUTY_APPLY
- **When to use & why**: skincare, makeup, cosmetics, fragrance, hair products, body care — anything where before/after + application ritual is the value prop. Viewers convert on visual transformation under matched lighting; symmetry between hook and outro is what sells the result as real. Not packaging-heavy luxury (→ HAUL_UNBOX).
- **Sensory anchors**: pump press, squeeze, glide on skin, glow lift, droplet beading, brush sweep.
- **Setting**: bathroom mirror, natural daylight or vanity lighting; same angle for the hook and the outro.
- **Close-up beat device**: a product close-up (bottle / tube / compact held in hand), not a screen.
- **Dialogue character**: hook is **time-stamped social proof** — name the duration ("X days in", "morning of week 3", "after one tube") to signal real use rather than paid promo. The hook plants the symmetry payoff that arrives in the after-shot. Arc: timed-claim hook → name + key ingredient or claim → narrate the application as it happens (close-up of fingers/brush on skin) → after-shot reveal (same angle as hook) → punchline that signals exclusivity or repurchase intent.

#### FITNESS_TRANSFORM
- **When to use & why**: workout equipment, supplements, recovery tools, activewear, fitness apps with tracking — anything where the work-to-result transformation is the value prop. Viewers convert on relatable struggle followed by earned payoff — showing the protein-shake bottle is not enough, you have to show the workout.
- **Sensory anchors**: heavy breathing, scoop hitting powder, equipment click, sweat catching light, post-workout exhale.
- **Setting**: gym or home-gym; workout gear at frame edges; floor or bench level.
- **Close-up beat device**: phone in hand showing app stats / heart rate / time elapsed, OR product packaging close-up (scoop in jar, bottle pour).
- **Dialogue character**: hook is **relatable resistance** — name the struggle / friction / not-wanting-to ("I did NOT want to do this", "almost skipped today", "this was supposed to be a rest day"); earns trust by sharing the tired feeling before showing the work. Arc: resistance hook → name the product + protocol ("I'm on day X of Y") → narrate mid-work moment while close-up shows the device or scoop → satisfaction insight that earns trust → punchline that frames continued use.

#### TECH_UNBOX
- **When to use & why**: gadgets, hardware, electronics, smart-home devices, wearables, peripherals, AI hardware (Framework laptop, AirPods, Whoop, Rabbit r1, Friend pendant, mechanical keyboards, ergonomic gear) — anything where the device + first-use moment is the value prop. The box ceremony signals premium positioning; viewers convert on seeing "does it actually work / what does it do" — the first-use beat is the conversion moment. Not HAUL (→ HAUL_UNBOX), not pure software/SaaS (→ APP_REVEAL).
- **Sensory anchors**: utility-knife slice, plastic peel, foam slide-out, power-on chime, tactile button press, haptic click, fan spin-up.
- **Setting**: wood desk, top-down framing during unbox; handheld during first-use; desk/lap context for ongoing use.
- **Close-up beat device**: the device itself once unboxed and powered on. `@Image2` is typically a real photo of the device's screen at its key UI moment (first measurement, paired status, hero feature open); if the device has no screen, a clean hero photo of it mid-use.
- **Dialogue character**: hook is **arrival ceremony** — name that this is happening *now* ("just got this", "opening it"). Anticipation > description; the hook plants the question "what does it do?" that the first-use beat answers. Do NOT lead with specs. Arc: arrival hook → name + one-line spec headline → first-use reveal while close-up is on the device doing its thing → workflow-change insight ("this replaces / changes / fixes my X") → punchline that hands off urgency (price, where to find, time-limited).

### 6. Voice input — fetch the user's voice sample (best-effort)

Right before the generate call, fetch the user's voice sample URL: call `identity_voice_sample_url`. This returns a **short-lived** download URL (mp3/wav) backing the user's registered voice, OR `null` if no voice is on file.

- If non-null → capture as `voice_sample_url` and pass it on the next call's `reference_audio` array. Both seedance and kling accept `reference_audio` (seedance up to 3, ≤15s combined; kling up to 8). The model uses the sample to clone the speaker's timbre for the lip-sync.
- If null → skip; the model uses its default voice.

Always get this URL fresh right before step 7 — do NOT cache or reuse a stale URL across runs.

### 7. Generate — first attempt with the avatar, cartoonize on rejection, retry

Always attempt the call **first** with the avatar resolved in step 2 (caller-supplied or built-in fallback) exactly as-is. The skill does not pre-process or pre-judge it. Only when seedance rejects the call do we restyle.

**7a. First attempt — avatar as-is**

Call `generate_reference_video`:
- `provider`: `seedance` (default) or `kling` if user passed `provider=kling`
- `aspect_ratio`: `9:16` (default); `3:4` allowed only on seedance
- `resolution`: `720p` (seedance only)
- `duration`: 15
- `reference_images`: `[avatar_url, screenshot_url]` (drop `screenshot_url` if step 3 failed)
- `reference_audio`: `[voice_sample_url]` (omit the param entirely if step 6 returned null)
- `prompt`: the multi-beat string from step 4
- `sound`: true (default — ambient + lip-sync produced by the model)

For `provider=kling`: convert the multi-beat prose into `shots: [{prompt, duration}, ...]` (5 shots × 3s = 15s sum), plus a top-level `prompt` summarizing the ad. References use `<<<image_1>>>` / `<<<image_2>>>` instead of `@Image1` / `@Image2`.

If the call returns `{ task_id, status: "queued" }`, poll `task_status(task_id)` in a tight loop (no Bash, no sleep) until terminal (`completed | failed | cancelled`). On `completed`, capture `result.url` → `video_url` and proceed to step 8.

**7b. On rejection — auto-cartoonize the avatar**

If 7a returns `422 content_policy_violation` on `image_urls` / `reference_images` (seedance + fal-queue moderation flags portraits that read as too photorealistic — even some Pixar-style 3D avatars get flagged), restyle the avatar in-place:

Call `generate_image`:
- `provider: "seedream"` (native Pixar/3D-animated look)
- `reference_images: [avatar_url]` (the new plural form; `reference_image: <url>` is still accepted as a deprecated single-image alias for back-compat — see [pika-mcp-server BACK-339, 2026-05-10])
- `aspect_ratio`: same as the ad's aspect ratio
- `resolution: "1K"`
- `watermark: false` (seedream-only knob added by BACK-339 — keep the restyled avatar clean of provider watermark for the downstream lip-sync re-render)
- `prompt: "Stylized 3D game character render — Unreal Engine 5 / Overwatch / Valorant / Apex Legends visual style. Anatomically grounded facial proportions with subtle stylization: slightly larger expressive eyes, defined sculpted cheekbone planes, smooth skin shader (smoother than photoreal, no micropore detail), idealized but believable features. PBR materials with subtle subsurface scattering, strand-based hair simulation, crisp cloth shader. Cinematic three-point studio lighting with strong rim light. Clearly a stylized AAA-game-character render — NOT photorealistic person, NOT Pixar plastic-toy cartoon, NOT exaggerated big-head proportions. Same person, same glasses, same outfit, same accessories. Centered medium portrait, neutral indoor background."`

Capture returned URL → `avatar_url_cartoon`.

**7c. Retry seedance with the cartoonized avatar**

Re-run the exact same `generate_reference_video` call from 7a, swapping the avatar reference: `reference_images: [avatar_url_cartoon, screenshot_url]` (or `[avatar_url_cartoon]` if step 3 failed). All other params unchanged. Capture `result.url` → `video_url`.

**7d. Final fallback — still rejected**

If 7c also returns `content_policy_violation`, stop. Tell the user: the avatar reads as too realistic for seedance moderation even after auto-restyling; ask them to either supply a more stylized portrait themselves or rerun with `provider=kling` (kling has a separate moderation pipeline that accepts realistic avatars).

### 8. Captions — single-shot styled burn (default on)

Skip if `captions=false`. Use **one** `add_captions` call instead of chaining `edit_text_overlay` per chunk — much faster (≤5 min single call vs 5–8 min sequential), and the styles position captions correctly out of the box.

Call `add_captions`:
- `video_url`: `video_url` from step 7
- `style`: `"tiktok"` (default — word-by-word purple highlight, Bebas Neue, all caps, rendered at the **bottom** of the frame; classic TikTok-creator look that keeps the face and screen clear). Alternatives: `"hormozi"` (lower-middle yellow highlight, more aggressive — overlays part of the phone-in-hand close-up beat), `"classic"` (plain bottom subtitle bar, safest), `"karaoke"` (progressive color fill, also bottom).
- `font_size`: `60` — overrides the per-style default; tuned for 9:16 readability without dominating the frame.
- `language`: pass the BCP-47 code for the page language detected in step 1 (`"en"`, `"zh"`, `"ja"`, `"es"`, etc.) — skips auto-detect and avoids misrouting CJK to a Latin-only font path.

Capture the returned URL → `final_url`.

### 9. Return

Return `final_url` on one line, plus a one-line summary: which category ran, whether the avatar was caller-supplied / built-in fallback / cartoonize-recovered, whether the screenshot was used or fell back to prose, whether the user's voice sample was used or default, the provider chosen, the language detected for dialogue, and whether captions were burned on.

## Load-bearing phrases

These anchors keep the ad from drifting into a generic product demo:

| Phrase | Where | Why load-bearing |
|---|---|---|
| `HOOK + 3 JUMP CUTs + OUTRO` | Prompt skeleton | Forces the TikTok-style multi-cut rhythm instead of one continuous presenter shot. |
| `Every beat has a Says: "..." line` | Prompt skeleton | Gives the video engine explicit lip-sync material across all beats. |
| `Trust @Image2` | Screen close-up rule | Prevents invented product UI when a real screenshot is already supplied. |
| `exactly one` screen-close-up beat | Prompt composition | Keeps the ad from becoming a screen recording instead of a creator-style reveal. |
| `Write all Says lines in the language detected from step 1` | Dialogue rule | Keeps localized product pages from getting English dialogue by default. |
| `single add_captions call` | Caption step | Avoids quality loss and drift from chained text overlays. |

## Examples

- `/pika:ugc-ads https://pika.me avatar_url=https://cdn/face.png` → APP_REVEAL, 9:16, seedance, real screenshot, captions on
- `/pika:ugc-ads https://maisonbrune.com avatar_url=https://cdn/face.png aspect_ratio=3:4` → HAUL_UNBOX, 3:4, seedance
- `/pika:ugc-ads https://pika.me avatar_url=https://cdn/face.png provider=kling captions=false` → APP_REVEAL, 9:16, kling shots[], no captions
- `/pika:ugc-ads https://pika.me` → no `avatar_url` → uses the built-in fallback Pixar-style female creator portrait, runs end-to-end
