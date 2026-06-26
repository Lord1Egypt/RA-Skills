---
name: senseaudio-video-gen
description: "Use when the user asks to create, inspect, render, or repair an HTML-authored video from a brief, website, Markdown/text file, or GitHub repository; needs captions, voiceover, background music, generated images/video clips, or a HyperFrames-like local video pipeline using SenseAudio media APIs and AudioClaw LLM planning."
---

# SenseAudio Video Gen

Author videos as HTML compositions, preview them in a browser, render them locally through Chrome screenshots plus FFmpeg, plan scripts/storyboards with AudioClaw by default, and generate supporting media through SenseAudio APIs. Treat HTML as the editable source of truth, SenseAudio as the media engine, and AudioClaw as the default LLM route.

## Default Setup

On a new machine, configure the media API and LLM API separately:

```bash
export SENSEAUDIO_API_KEY="..."
```

`SENSEAUDIO_API_KEY` powers only SenseAudio media APIs: TTS, ASR, image, video, and music.

AudioClaw LLM planning uses a separate OpenAI-compatible route. If running inside AudioClaw, no extra LLM env is needed when the local AudioClaw config file exists. Otherwise set the LLM env explicitly:

```bash
export AUDIOCLAW_CONFIG_PATH="config/audioclaw.json"
export AUDIOCLAW_LLM_MODEL="doubao-seed-2-0-pro-260215"
export AUDIOCLAW_LLM_BASE_URL="https://platform.senseaudio.cn/v1"
export AUDIOCLAW_LLM_API_KEY="..."
```

LLM config precedence is CLI flags, then `AUDIOCLAW_LLM_*`, then `AUDIOCLAW_CONFIG_PATH` or the local AudioClaw config file. The CLI deliberately does not reuse `SENSEAUDIO_API_KEY` as an AudioClaw LLM key. Use `--llm none` for deterministic heuristic planning, or `--offline` to skip live media calls.

## Core Loop

Start from a brief when the user wants a complete project shell:

```bash
python3 scripts/senseaudio_video_gen.py compose \
  --project my-video \
  --brief "Make a premium launch film for a new AI research assistant." \
  --duration 12 \
  --style-preset executive-film
```

`compose` is the general video path for product launch films, feature explainers, report summaries, technical walkthroughs, title cards, social cuts, and branded motion pieces. It defaults to `executive-film`, a restrained cinematic style with large typography, letterbox framing, low ornament, and non-web chapter IDs. Use `--offline` when drafting without live API calls, and add `--render` when the project should be rendered immediately.

`compose` now defaults to `--llm audioclaw`. If the default LLM route is unavailable, `--llm-fallback` keeps the project moving with heuristic planning and records a warning in `senseframe.json`. Pass `--no-llm-fallback` when an LLM failure should stop the run.

For the closest HyperFrames-style website workflow, prefer the one-pass `site-video` pipeline:

```bash
python3 scripts/senseaudio_video_gen.py site-video \
  --url https://www.anthropic.com/ \
  --project anthropic-site-video \
  --brief "用中文介绍 Anthropic 官网的 Claude、安全 AI、研究与企业能力。" \
  --duration 14 \
  --fps 30 \
  --llm audioclaw
```

`site-video` defaults to `editorial-pro`, layered beats, cinematic motion, GSAP-compatible timing, real website screenshots, AudioClaw LLM planning, SenseAudio narration/ASR when live media is enabled, audio-reactive data, local rendering, inspect frames, local frame-quality audit, and motion audits. If LLM planning fails, `--llm-fallback` retries with heuristic planning and records the warning. Use `--offline --no-render` for a safe draft that writes the same editable project structure and `pipeline-report.json`.

Add `--music --music-poll` when the site video should request a SenseAudio music bed, download it, mix it under narration as `assets/final-audio.m4a`, and render with that mixed track. If SenseAudio accepts the task but does not return `audio_url` in time, `--music-fallback` creates a local ambient bed so the video still ships with background music while preserving the task manifest. Use `--music-dry-run` or `--offline` to inspect the `/music/song/create` payload without spending credits. Add `--auto-repair` when the project should run a second pass after motion/vision audits, tighten real screenshot crops, damp busy overlays, and rerender the repaired composition.

Website capture follows the useful parts of the HyperFrames loop: warm the live page, dismiss common cookie/modals, scroll to trigger lazy assets, record `assets/site-capture-quality.json`, capture `renders/inspect` frames, and write `renders/inspect/contact-sheet.html` for review. Use `--vision-audit` when a live VL model should judge the rendered frames; the local `frame-quality-audit` still runs by default when rendering.

For gated, cookie-sensitive, or region-personalized sites, keep browser state explicit:

```bash
python3 scripts/senseaudio_video_gen.py site-video \
  --url https://example.com/ \
  --project example-site-video \
  --browser-profile profiles/example-capture \
  --cookie-file cookies/example.json
```

Cookies often make screenshots closer to what a real user sees, but the clean temporary browser remains the default to avoid leaking private account pages into generated videos.

For URL-to-video work, `site-ingest` classifies real page material into semantic roles such as hero, product, research, safety, developer, enterprise, customer, pricing, and CTA. These roles drive `story_evidence`, shot choice, composition mode, camera path, and `data-material-role` markers in the rendered HTML.

Use `source-ingest` for first-stage non-web inputs. It converts local Markdown/text files or a GitHub repository README into the same `site-profile.json` shape used by website projects, so `compose --site-file <profile.json>` can reuse storyboard, narration, semantic role, and production-spec logic without a separate document pipeline:

```bash
python3 scripts/senseaudio_video_gen.py source-ingest \
  --file product-notes.md \
  --output product-notes.site.json \
  --json

python3 scripts/senseaudio_video_gen.py source-ingest \
  --github-url heygen-com/hyperframes \
  --output hyperframes-readme.site.json
```

Use `site-vision-plan` when screenshot crops need to be planned before rendering. The default `heuristic` provider derives crop center, zoom, pan, and focus from DOM highlights and semantic roles. `--provider openrouter` builds an OpenRouter-compatible vision request so a VL model can inspect screenshots first; keep `--fallback` enabled so rendering degrades to deterministic crops if the model route is unavailable.

Use the music and repair commands directly when tuning an existing project:

```bash
python3 scripts/senseaudio_video_gen.py music-create \
  --prompt "Instrumental premium website explainer bed, subtle pulse, no vocals" \
  --duration 16 \
  --poll \
  --download my-video/assets/background-music.mp3 \
  --project my-video

python3 scripts/senseaudio_video_gen.py mix-audio \
  --project my-video \
  --voice my-video/assets/narration.mp3 \
  --music my-video/assets/background-music.mp3 \
  --output my-video/assets/final-audio.m4a \
  --duration 16

python3 scripts/senseaudio_video_gen.py repair --project my-video --json
```

Use the default AudioClaw route for creative plans when the brief needs LLM-written copy and storyboard:

```bash
python3 scripts/senseaudio_video_gen.py llm-plan \
  --brief "Make a concise webpage intro for SenseAudio's sound library." \
  --duration 9 \
  --output my-plan.json

python3 scripts/senseaudio_video_gen.py compose \
  --project my-video \
  --brief "Make a concise webpage intro for SenseAudio's sound library." \
  --generate-images \
  --generate-broll \
  --asset-dry-run \
  --offline
```

`llm-plan` defaults to `--provider audioclaw`. The skill strips LiteLLM-style provider prefixes such as `volcengine/` for `platform.senseaudio.cn` and retries without `response_format` for models that do not support JSON-mode requests.

DeepSeek remains available with `--provider deepseek` or `--llm deepseek`; set `DEEPSEEK_API_KEY`, `DEEPSEEK_MODEL`, or `DEEPSEEK_BASE_URL` when using it.

If the AudioClaw configured model is not strong enough for dense product research, switch planning to OpenRouter with `--provider openrouter` or `--llm openrouter`, and choose a capable model via `--model`, `--llm-model`, `OPENROUTER_LLM_MODEL`, or `OPENROUTER_MODEL`.

Build an existing project as a local pipeline:

```bash
python3 scripts/senseaudio_video_gen.py build --project my-video --dry-run
python3 scripts/senseaudio_video_gen.py build --project my-video --output my-video/renders/final.mp4
```

Or scaffold a blank composition:

```bash
python3 scripts/senseaudio_video_gen.py init my-video --duration 6 --fps 24
cd my-video
python3 ../scripts/senseaudio_video_gen.py preview .
python3 ../scripts/senseaudio_video_gen.py inspect . --samples 5
python3 ../scripts/senseaudio_video_gen.py render . --output renders/final.mp4
```

Use SenseAudio assets inside the same project:

```bash
python3 scripts/senseaudio_video_gen.py tts \
  --text "让声音、字幕和画面在一个视频项目里完成。" \
  --voice-id male_0028_a \
  --output my-video/assets/narration.mp3

python3 scripts/senseaudio_video_gen.py asr \
  --file my-video/assets/narration.mp3 \
  --timestamps word \
  --output my-video/assets/transcript.json

python3 scripts/senseaudio_video_gen.py captions \
  --project my-video \
  --transcript my-video/assets/transcript.json \
  --output my-video/assets/captions.json

python3 scripts/senseaudio_video_gen.py captions-export \
  --captions my-video/assets/captions.json \
  --format srt \
  --output my-video/renders/final.srt

python3 scripts/senseaudio_video_gen.py render my-video \
  --audio my-video/assets/narration.mp3 \
  --parallel 4 \
  --resume \
  --output my-video/renders/final-with-voice.mp4

python3 scripts/senseaudio_video_gen.py lint --project my-video --json
python3 scripts/senseaudio_video_gen.py asset-report --project my-video --json

python3 scripts/senseaudio_video_gen.py generate-assets \
  --project my-video \
  --image-prompt "clean product UI hero image for a sound library" \
  --video-prompt "short b-roll of creators choosing voices" \
  --dry-run

python3 scripts/senseaudio_video_gen.py timeline \
  --project my-video \
  --preset cinematic
```

## Composition Contract

- Root scene uses `data-composition-id`, `data-width`, `data-height`, `data-duration`.
- Timed clips use `data-start`, `data-duration`, optional `data-media-start`, and optional `data-scene`.
- Timeline DSL uses `assets/timeline.json`, `data-timeline-source`, and optional `data-effect` presets such as `fade-up`, `slide-left`, `zoom-in`, `spotlight`, and `parallax`.
- Visual styles are selected through the local registry with `styles` and `compose --style-preset`; tokens are embedded as CSS variables, written to `assets/style-preset.json`, and recorded in `senseframe.json`.
- The optional `gsap-compat` timeline engine writes `labels` and `tracks` and uses a local `createGsapCompatTimeline` adapter; never load external GSAP/CDN code for deterministic renders.
- Transition presets use `transition_preset` plus `transitions[]` in `assets/timeline.json`; supported presets include `editorial`, `glass`, `ribbon`, `iris`, and `luma`.
- Storyboard ids must bind to real DOM scenes: `compose` maps each storyboard item to matching `data-scene` and `data-timeline-id` elements rather than fixed template beats.
- Beat composition uses `assets/beats.json`, `.beat-layer`, and `data-beat` markers. `compose --beat-mode layered` splits each storyboard scene into hook/proof/detail/cta overlays so a single scene can carry multiple timed visual arguments.
- Beat pacing is readability-first: defaults use 3 requested beats per scene, automatically clamp short scenes to keep each beat around one second or longer, and `motion-map` reports flashiness risk when beat/transition rates are too high.
- Website explainers rotate dedicated shot layouts (`hero-overview`, `nav-scan`, `feature-zoom`, `trust-message`, `cta-summary`) so adjacent scenes do not reuse the same visual structure.
- Composition templates use `data-composition-mode` values such as `full-bleed`, `split-scan`, `zoom-callout`, `evidence-board`, and `cta-lockup`; every website scene should also set a `data-camera-path` so the renderer can apply distinct camera motion instead of a repeated left/right card.
- Brand extraction uses `brand-extract` or `compose --brand-url` to create `assets/brand.json`; brand name, description, nav labels, colors, logos/icons, social images, typography, keywords, and inferred voice should influence website explainer shots.
- Site ingestion uses `site-ingest` or `compose --site-url` to create `assets/site-profile.json`; headings, sections, CTA labels, and evidence snippets should drive storyboard scenes and visual cards before generic brief fallback.
- Source ingestion uses `source-ingest --file <notes.md|notes.txt>` or `source-ingest --github-url <owner/repo>` to create the same site-profile shape from Markdown, plain text, or GitHub README content.
- Website screenshots use `site-capture` or `compose --site-screenshots` to capture scroll positions into `assets/site-screenshots/`; these screenshots should appear in website explainer shots as visual evidence with deterministic pan/zoom and evidence highlight boxes, not decorative stock media.
- Video copy defaults to Chinese (`zh-CN`) for narration, captions, beat text, and storyboard intent unless the user explicitly requests another language.
- Seekable motion uses `window.__timelines["main"]`; the runtime seeks registered timelines during frame capture so entrances, breathing motion, exits, chips, waveforms, and focus highlights render deterministically.
- Audio-reactive motion uses smoothed `assets/audio-data.json` from `audio-data`; the runtime loads `data-audio-source` and maps RMS/bands to local mesh intensity, card glow, waveform motion, and transition light. Do not drive the global camera directly from raw audio.
- Caption containers use `data-caption-source="./assets/captions.json"` or inline `window.__sfCaptions`; `captions --include-words` enables active word highlighting with `.sf-word[data-sf-active="true"]`.
- Word captions use kinetic karaoke states: active words scale, emphasized terms receive `sf-word-emphasis`, and styling must remain deterministic with no CSS animation loops.
- Final renders are silent unless `render --audio <file>` is provided or `build` finds a registered audio asset such as `narration`; `lint` warns when narration text exists but no audio asset is registered.
- Put deterministic frame logic in `window.renderFrame(time)`.
- Run `motion-audit --project <dir> --strict` after composing to catch storyboard/DOM/timeline mismatches and legacy fixed-template markers.
- Run `motion-map --project <dir> --strict` before expensive renders to score motion density, scene coverage, low-motion zones, transitions, and audio-reactive binding.
- The runtime sets `window.__senseframes.time`, CSS variable `--sf-time`, `data-sf-active`, `data-scene-active`, and dispatches `sf-seek`.
- Use CSS for final layout first, then animate from `renderFrame(time)`; avoid wall-clock animation for rendered output.

## Workflow

1. **Plan** — define aspect ratio, duration, audience, scenes, copy, voice, and output target.
2. **Scaffold** — run `compose` for brief-to-project or `init` for a blank source; use `--beat-mode layered` when the video needs dense HyperFrames-style scene internals.
3. **Generate media** — use `voices`, `tts`, `asr`, `captions`, `image-sync`, or `video-create` to produce assets.
4. **Register assets** — use `asset-add` or command manifests so `assets/asset-manifest.json` and `senseframe.json` stay current.
5. **Lint and audit** — run `lint`, `motion-audit`, and `motion-map` to catch missing assets, mismatched scenes, and flat motion.
6. **Inspect frames** — run `inspect` before rendering to catch layout, legibility, and timing issues.
7. **Render** — run `render` or `build`; mux narration with `--audio` when needed.
8. **Deliver** — return the MP4, render report JSON, subtitles, `senseframe.json`, transcripts, prompts, and asset manifests.

## Command Map

| Task | Command | Purpose |
| --- | --- | --- |
| One-pass website video | `site-video --url <site>` | Ingest, plan, capture, narrate, bind audio data, render, and audit in one pipeline |
| LLM plan | `llm-plan` / `llm-plan --provider openrouter` | Generate title, narration, visual style, and storyboard JSON; defaults to AudioClaw |
| Brief to project | `compose --project <dir> --brief ...` | Create storyboard, narration script, caption scaffold, HTML, and manifests; defaults to AudioClaw with heuristic fallback |
| Brand extraction | `brand-extract --url <site>` | Extract brand identity, colors, nav, logos/icons, typography, keywords, and voice |
| Site ingestion | `site-ingest --url <site>` | Extract real headings, sections, CTA labels, and evidence snippets for URL-to-video |
| Source ingestion | `source-ingest --file <md/txt>` / `--github-url <repo>` | Convert Markdown, text, or GitHub README content into a reusable `site-profile.json` |
| Site screenshots | `site-capture --url <site>` | Capture real scroll screenshots with Chrome, warm lazy content, clean overlays, and register visual evidence |
| Frame quality | `frame-quality-audit --project <dir>` | Check inspect/site frames for blank captures and leaked planning copy |
| Visual crop plan | `site-vision-plan --project <dir>` | Plan screenshot crop, zoom, pan, and focus before rendering |
| Beat layers | `beats --project <dir>` | Split storyboard scenes into hook/proof/detail/cta timed overlays |
| Local pipeline | `build --project <dir>` | Run lint, create captions when a transcript exists, and render |
| Generated assets | `generate-assets --project <dir>` | Plan or call SenseAudio image/video generation and register results |
| Project validation | `lint --project <dir>` | Check entry HTML, runtime, caption sources, timing, and asset existence |
| Style registry | `styles --json` | List built-in visual presets and recommended motion defaults |
| Motion audit | `motion-audit --project <dir>` | Check storyboard scene binding, beat layers, transition layer, audio-reactive hooks, timeline registry, and legacy markers |
| Motion map | `motion-map --project <dir>` | Score motion density, scene/beat coverage, flashiness risk, transition coverage, dead zones, and audio-reactive binding |
| Audio data | `audio-data --audio <file> --output assets/audio-data.json` | Extract frame-level RMS/band data and bind it with `data-audio-source` |
| Scaffold | `init <dir>` | Create `index.html`, runtime, manifest, assets, renders |
| Preview | `preview <dir>` | Serve project for browser review |
| Inspect | `inspect <dir>` | Capture timestamped sample frames |
| Timeline | `timeline --project <dir> --timeline-engine gsap-compat` | Generate animation tracks, labels, transitions, and bind them to the runtime |
| Render | `render <dir>` | Convert HTML frames to MP4 locally with optional `--parallel`, `--resume`, and `--frame-dir` |
| Voiceover | `tts` | Generate narration from SenseAudio TTS |
| Transcript | `asr --timestamps word` | Produce transcript timing for captions |
| Captions | `captions --transcript ...` | Convert ASR JSON into `assets/captions.json` |
| Subtitle files | `captions-export` | Export captions JSON to `.srt` or `.vtt` |
| Asset registry | `asset-add` | Register local/generated assets in the project manifest |
| Asset inventory | `asset-report` | List registered assets and missing files |
| Still assets | `image-sync` | Generate first frames, backdrops, thumbnails |
| Model clips | `video-create` / `video-status` | Generate AI video clips through SenseAudio |
| Voices | `voices --voice-type all` | Discover usable `voice_id` values |

## Non-Negotiable Rules

- Never rely on CSS `animation`, `setInterval`, or wall-clock playback for final renders; tie motion to `time`.
- Do not use remote video generation when an HTML composition can express the exact UI/layout; use SenseAudio video generation for generative inserts, references, or b-roll.
- Do not invent voice IDs. Query `voices` or use a user-provided voice.
- Keep `senseframe.json` updated with generated assets, task IDs, transcripts, and final output paths.
- For subtitles, use `captions` to convert ASR words into grouped caption cues before authoring caption elements.
- If a local audio/video file must guide SenseAudio model video generation, upload it somewhere first; model video content fields require URLs.

## References

- `references/authoring.md` — HTML composition patterns and timing rules.
- `references/renderer.md` — local renderer requirements and troubleshooting.
- `references/media-pipeline.md` — SenseAudio asset pipeline.
- `references/api.md` — endpoint and model parameter summary.
- `examples/starter-html-video` — minimal editable composition project.
