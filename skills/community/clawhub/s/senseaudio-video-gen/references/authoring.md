# HTML Authoring Guide

## Source Of Truth

The `index.html` file is the video. Do not hide the important composition logic in prompts or generated manifests. The manifest records assets and parameters; HTML controls layout, timing, and render behavior.

## Required Structure

```html
<div data-composition-id="main" data-start="0" data-duration="6" data-width="1280" data-height="720">
  <section class="story-scene" data-scene="intro" data-timeline-id="intro" data-start="0" data-duration="2.5">Scene one</section>
  <section class="story-scene" data-scene="detail" data-timeline-id="detail" data-start="2.5" data-duration="3.5">Scene two</section>
  <div class="caption" data-caption-source="./assets/captions.json" data-caption-target></div>
</div>
<script src="./senseframe-runtime.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = { seek: function (time) { /* deterministic timeline state */ } };
  window.renderFrame = function (time) {
    // optional deterministic visual state for this exact timestamp
  };
</script>
```

## Timing

- Use seconds.
- `data-start` and `data-duration` control visibility for clips and scenes.
- `data-scene` marks named beats and receives `data-scene-active="true|false"` at render time.
- `data-caption-source` loads grouped captions from JSON and writes the active cue into the element.
- Use `window.__timelines["main"].seek(time)` for scene choreography; the runtime seeks registered timelines before calling `window.renderFrame(time)`.
- Use `window.renderFrame(time)` for small transforms, counters, progress bars, and custom highlights that do not conflict with the main timeline.
- For media elements, add `data-media-start` to trim into the source.

## Layout

- Build the final still frame first.
- Animate from or through that layout in the seekable timeline or `renderFrame`.
- Keep text large enough for video: 56px+ headlines, 24px+ body, 18px+ captions.
- Use `inspect` to sample frames before rendering.
- Use `motion-audit --project <dir> --strict` to catch storyboard scenes that are not represented by DOM scenes or timelines.
- Use `motion-map --project <dir> --strict` to find dead zones, weak scene coverage, missing transitions, or unbound audio-reactive motion before spending render time.

## Captions

Run `captions --project <dir> --transcript assets/transcript.json --output assets/captions.json` after ASR. The output shape is:

```json
{"captions":[{"id":"c0","text":"搜索音色","start":0.0,"end":0.8}]}
```

Use short cues. Prefer 18–32 Chinese characters per cue for a 720p short video.

For word highlighting, run `captions --include-words`. Style active words with:

```css
.sf-word { opacity: .45; transition: none; }
.sf-word[data-sf-active="true"] { opacity: 1; color: #ffd08a; }
.sf-word-emphasis[data-sf-active="true"] { text-shadow: 0 0 22px rgba(255,214,140,.66); }
```

The runtime assigns `sf-word-emphasis` to brand/action words and scales active words inline from their timestamps. Do not add wall-clock CSS animations to caption words.

## Audio-Reactive Motion

Generate frame-level voice/music data and bind it to the root composition:

```bash
python3 scripts/senseaudio_video_gen.py audio-data \
  --project my-video \
  --audio my-video/assets/narration.mp3 \
  --output my-video/assets/audio-data.json \
  --fps 24 \
  --bands 8
```

The runtime loads `data-audio-source="./assets/audio-data.json"` and exposes `window.__senseframes.audioData`. The `audio-data` command writes smoothed RMS plus `rawRms`; use smoothed values for visuals. The default composed template maps RMS/bands to mesh intensity, card glow, waveform bars, and transition light, but keeps the global camera independent from audio to avoid speech jitter. Keep text motion subtle: 3–6% scale for captions, stronger motion only for background/card layers.

## Beat Composition

Use layered beats when a scene should contain multiple authored reveals rather than one static text block:

```bash
python3 scripts/senseaudio_video_gen.py compose \
  --project my-video \
  --brief "..." \
  --beat-mode layered \
  --beats-per-scene 3 \
  --timeline-engine gsap-compat \
  --offline
```

`compose --beat-mode layered` writes `assets/beats.json`, inserts `.beat-layer` elements with `data-beat`, and adds local timeline tracks for every beat. The requested beat count is clamped on short scenes so each beat remains readable instead of flashing past. To regenerate only the beat plan after editing `assets/storyboard.json`, run:

```bash
python3 scripts/senseaudio_video_gen.py beats --project my-video --beats-per-scene 3 --json
```

Each beat has `scene_id`, `role`, `start`, `duration`, `text`, and `emphasis`. Keep roles short and visual: `hook` names the promise, `proof` shows the reason to believe, `detail` reveals a concrete interaction, and `cta` lands the action. `motion-map --strict` reports beat coverage plus flashiness risk so both flat sections and overly fast sections are caught before render.

## Brand Extraction

For website explainers, extract brand metadata before composing:

```bash
python3 scripts/senseaudio_video_gen.py brand-extract --url https://www.anthropic.com/ --output brand.json --json
python3 scripts/senseaudio_video_gen.py compose --project my-video --brief "..." --brand-file brand.json --beat-mode layered --offline
```

`compose --brand-url <site>` can fetch and apply the brand in one pass. The resulting `assets/brand.json` records `name`, `description`, `nav`, `colors`, `logos`, `assets.icons`, `assets.social_images`, `typography`, `keywords`, and inferred `voice`. Website shots should use this data for navigation chips, hero copy, palette accents, brand marks, tone labels, and brand-specific wording rather than generic filler UI.

## Site Ingestion

For URL-to-video work, extract real page evidence before composing:

```bash
python3 scripts/senseaudio_video_gen.py site-ingest --url https://www.anthropic.com/ --output site.json --json
python3 scripts/senseaudio_video_gen.py compose --project my-video --brief "介绍这个官网" --site-file site.json --brand-file brand.json --beat-mode layered --offline
```

`compose --site-url <site>` can fetch site evidence in one pass. The resulting `assets/site-profile.json` records headings, sections, CTA labels, evidence snippets, and text samples. Storyboard scenes should prefer these evidence items over generic brief-derived copy, so website explainers stay anchored to actual page content.

## Site Screenshots

Use real screenshots when the video needs to show the actual website, not just a redesigned card:

```bash
python3 scripts/senseaudio_video_gen.py site-capture --url https://www.anthropic.com/ --project my-video --count 3 --json
python3 scripts/senseaudio_video_gen.py compose --project my-video --brief "介绍这个官网" --site-url https://www.anthropic.com/ --site-screenshots --beat-mode layered --offline
```

Screenshots are captured with local Chrome through DevTools, saved under `assets/site-screenshots/`, registered as `website-screenshot` assets, and referenced from `assets/site-profile.json`. Rendered website shots apply deterministic pan/zoom plus a `.site-scan-highlight` evidence box to guide the viewer through real pixels. Use this when visual accuracy matters; DeepSeek can structure the story, but Chrome provides the actual page pixels.

## Composition Templates

Website explainers should vary scene structure instead of repeating one left-copy/right-card layout. `compose` assigns `data-composition-mode` and `data-camera-path` to each scene:

- `full-bleed` + `hero-push` for opening full-page website context.
- `split-scan` + `lateral-scan` for navigation or scroll-path explanation.
- `zoom-callout` + `macro-zoom` for product/detail emphasis.
- `evidence-board` + `board-orbit` for proof, policy, or research evidence.
- `cta-lockup` + `lockup-dolly` for final action and brand close.

The renderer reads these attributes to change layout, visual-card transforms, screenshot pan/zoom, and copy placement.

## Style Registry

Use `styles` to inspect built-in visual presets before composing:

```bash
python3 scripts/senseaudio_video_gen.py styles --json
python3 scripts/senseaudio_video_gen.py compose --project my-video --brief "..." --style-preset neon-console --offline
```

The registry currently includes `product-glass`, `neon-console`, `editorial-cream`, and `midnight-lab`. A composed project records the selected preset in `senseframe.json`, writes `assets/style-preset.json`, and embeds tokens such as `--accent`, `--ember`, `--aqua`, stage background, card gradient, and mesh gradient into `index.html`.

## Timeline DSL

Generate a timeline from the project storyboard:

```bash
python3 scripts/senseaudio_video_gen.py timeline --project my-video --preset cinematic
```

The runtime loads `data-timeline-source="./assets/timeline.json"` and applies scene timing plus effects. Timeline items target matching `data-scene` or `data-timeline-id` values:

```json
{"preset":"cinematic","items":[{"id":"intro","start":0,"end":2.5,"effect":"fade-up"}]}
```

Built-in effects: `fade-up`, `slide-left`, `zoom-in`, `spotlight`, `parallax`.

`compose --animation-preset ...` also creates a seekable `window.__timelines["main"]` bridge with build/breathe/resolve phases for each storyboard scene. Keep storyboard ids stable because they are used for `data-scene`, `data-timeline-id`, nav state, and audit checks.

Transition presets are authored as timeline data, not ad-hoc CSS loops:

```bash
python3 scripts/senseaudio_video_gen.py timeline --project my-video --preset cinematic --transition-preset editorial
```

This writes `transitions[]` entries with `from`, `to`, `at`, `duration`, `kind`, and `intensity`, then patches the inline runtime `transitionPlan`. Pick `glass` for polished UI reveals, `ribbon` for fast explainers, `iris` for feature focus, and `luma` for energetic sweeps.

For HyperFrames-style timeline authoring without external dependencies, enable the local GSAP-compatible engine:

```bash
python3 scripts/senseaudio_video_gen.py timeline --project my-video --preset cinematic --timeline-engine gsap-compat
```

The timeline JSON gains `labels` and `tracks`, and the HTML runtime exposes `window.__senseframes.gsapCompat`. Tracks support `set`, `to`, and `fromTo` with `opacity`, `x`, `y`, `z`, `scale`, `rotate`, `rotateX`, `rotateY`, `filter`, `background`, and `mixBlendMode`.

## Asset Registry

Every reusable file should be registered:

```bash
python3 scripts/senseaudio_video_gen.py asset-add \
  --project my-video \
  --id narration \
  --type audio \
  --path my-video/assets/narration.mp3 \
  --role voiceover
```

The command updates both `assets/asset-manifest.json` and `senseframe.json`.

## Generated Media Slots

Use `data-asset` to mark where generated assets should bind:

```html
<img data-asset="hero-image" src="" alt="Generated hero" />
<video data-asset="broll-video" src="" muted playsinline></video>
```

`generate-assets` records image/video requests in the manifest. When a generated file is downloaded and registered, the helper can update matching `src` values.
