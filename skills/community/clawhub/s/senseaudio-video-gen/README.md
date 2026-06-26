# senseaudio-video-gen

HTML-authored video framework powered by SenseAudio media APIs and AudioClaw LLM planning.

## Capabilities

- Compose a project from a brief with storyboard, narration script, caption scaffold, HTML, runtime, and manifests.
- Default general `compose` videos to `executive-film`, a mature launch-film style with letterbox framing, large typography, restrained motion, and fewer toy-like UI ornaments.
- Generate creative plans through AudioClaw by default, with DeepSeek and OpenRouter available as explicit alternatives.
- Default video copy to Chinese (`zh-CN`) unless the brief explicitly asks for another language.
- Run a local build pipeline that validates, prepares captions, renders, and records output metadata.
- Run a one-command `site-video` pipeline that ingests a URL, plans with AudioClaw, captures screenshots, creates narration/audio-reactive data, renders, and audits motion.
- Generate SenseAudio music beds, mix them under narration, and render with the registered `final-audio` track by default.
- Run an automatic second-pass repair that uses motion/vision audit reports to tighten screenshot evidence, stabilize overlays, and rerender.
- Capture timestamped inspect frames and run a local frame-quality gate by default for `site-video`, catching blank/washed frames and leaked planning copy before delivery.
- Add storyboard-driven scene layers, seekable timeline motion, deterministic animation effects, and word-level caption highlighting.
- Split scenes into timed hook/proof/detail/cta beat layers with matching HTML markers and timeline tracks.
- Clamp beat density for readability and report flashiness risk when cuts or overlays move too quickly.
- Rotate website explainer shots across hero overview, navigation scan, feature zoom, trust message, and CTA summary layouts.
- Extract website brand profiles and apply brand colors, navigation labels, descriptions, logos/icons, typography, keywords, and inferred voice to generated shots.
- Ingest real website evidence from headings, sections, CTAs, and page text so URL-to-video projects explain actual page content instead of generic brand templates.
- Ingest local Markdown/text files and GitHub repository READMEs into the same reusable site-profile format for fast document-to-video drafts.
- Classify real website materials into semantic roles such as hero, product, research, safety, developer, enterprise, customer, pricing, and CTA, then use those roles to choose shots, composition modes, and camera paths.
- Plan screenshot crops and focus points before rendering with `site-vision-plan`, using a deterministic heuristic by default and an OpenRouter-compatible vision route when requested.
- Capture real website scroll screenshots with local Chrome and place them into explainer shots as visual evidence.
- Warm live pages before capture, dismiss common cookie/modals, record `site-capture-quality.json`, and optionally load cookies or a dedicated browser profile for gated/region-specific pages.
- Use a cleaner screenshot-first website mode that reduces overlays and keeps one evidence layer per scene.
- Use `--style-preset editorial-pro` for more mature website explainers with fine annotations, smaller type, restrained motion, and less toy-like UI.
- Use `--style-preset executive-film` for non-web product launches, report summaries, technical explainers, title cards, and premium brand films.
- Audit rendered frames with an OpenRouter/OpenAI-compatible vision model through `site-vision-audit`.
- Generate `renders/inspect/contact-sheet.html` for quick frame-by-frame review, inspired by the HyperFrames snapshot/contact-sheet loop.
- Choose visual direction from a local style registry with reusable CSS tokens and recommended motion defaults.
- Add a local GSAP-compatible timeline adapter with `labels`, `tracks`, `set`, `to`, `fromTo`, and deterministic `seek`.
- Add authored transition presets such as editorial wipes, glass flashes, iris focus, ribbon sweeps, and luma sweeps.
- Add pre-extracted audio-reactive motion data for camera, glow, waveform, and transition intensity.
- Audit storyboard/DOM/timeline/transition/audio-reactive alignment with `motion-audit`.
- Map motion density, scene coverage, dead zones, and recommendations with `motion-map`.
- Plan or generate SenseAudio images and b-roll videos as registered project assets.
- Scaffold HTML composition projects.
- Preview HTML videos in a browser.
- Render deterministic frames locally with Chrome and FFmpeg, defaulting to one persistent Chrome session for lower CPU overhead.
- Generate narration, transcripts, captions, images, and model-video clips through SenseAudio.
- Register every generated/local asset in `assets/asset-manifest.json`.
- Export subtitles as SRT or WebVTT for external upload workflows.

## Requirements

- Python 3.9+
- Chrome or Chromium (`CHROME_BIN` can override discovery)
- FFmpeg in `PATH`
- `SENSEAUDIO_API_KEY` for live SenseAudio media API calls
- Optional local AudioClaw config file for automatic AudioClaw LLM model discovery
- Optional `AUDIOCLAW_LLM_API_KEY`, `AUDIOCLAW_LLM_BASE_URL`, and `AUDIOCLAW_LLM_MODEL` for env-only LLM routing on a new machine
- Optional `DEEPSEEK_API_KEY` for live LLM planning through DeepSeek
- `OPENROUTER_API_KEY` or `VL_API_KEY` for OpenRouter LLM planning and live visual quality audits

No third-party Python package is required.

## Default Configuration

For a fresh install, configure SenseAudio media first:

```bash
export SENSEAUDIO_API_KEY="..."
```

That key is used for SenseAudio TTS, ASR, image, video, and music APIs.

Configure AudioClaw LLM separately, either through the local AudioClaw config file or env:

```bash
export AUDIOCLAW_LLM_API_KEY="..."
export AUDIOCLAW_LLM_BASE_URL="https://platform.senseaudio.cn/v1"
export AUDIOCLAW_LLM_MODEL="doubao-seed-2-0-pro-260215"
```

When running inside AudioClaw, the CLI automatically reads the local AudioClaw config file and uses the configured default model. Override order for LLM planning is:

1. CLI flags: `--llm-model`, `--llm-base-url`, `--model`, `--base-url`
2. Env vars: `AUDIOCLAW_LLM_MODEL`, `AUDIOCLAW_LLM_BASE_URL`, `AUDIOCLAW_LLM_API_KEY`
3. AudioClaw config: `AUDIOCLAW_CONFIG_PATH` or the local AudioClaw config file

`llm-plan`, `compose`, and `site-video` default to AudioClaw. They do not reuse `SENSEAUDIO_API_KEY` as an LLM key. If AudioClaw LLM is not configured, `compose` and `site-video` can continue through `--llm-fallback` with heuristic planning; use `--llm none` or `--provider deepseek/openrouter` when you intentionally want a different route.

## Smoke Test

```bash
python3 scripts/senseaudio_video_gen.py --help
python3 scripts/senseaudio_video_gen.py styles --json
python3 scripts/senseaudio_video_gen.py llm-plan --brief "Introduce a sound library webpage" --dry-run
python3 scripts/senseaudio_video_gen.py llm-plan --brief "Introduce a sound library webpage" --provider deepseek --dry-run
python3 scripts/senseaudio_video_gen.py llm-plan --brief "Introduce a sound library webpage" --provider openrouter --dry-run
python3 scripts/senseaudio_video_gen.py brand-extract --url https://www.anthropic.com/ --json
python3 scripts/senseaudio_video_gen.py site-ingest --url https://www.anthropic.com/ --json
python3 scripts/senseaudio_video_gen.py source-ingest --file README.md --output readme-site.json --json
python3 scripts/senseaudio_video_gen.py source-ingest --github-url heygen-com/hyperframes --output hyperframes-readme-site.json --json
python3 scripts/senseaudio_video_gen.py site-capture --url https://www.anthropic.com/ --output-dir demo-compose/assets/site-screenshots --json
python3 scripts/senseaudio_video_gen.py frame-quality-audit --project demo-compose --json
python3 scripts/senseaudio_video_gen.py site-vision-plan --project demo-compose --json
python3 scripts/senseaudio_video_gen.py site-vision-audit --project demo-compose --dry-run --json
python3 scripts/senseaudio_video_gen.py site-video --url https://www.anthropic.com/ --project anthropic-site-video --duration 14 --offline --no-render --music --music-dry-run --auto-repair
python3 scripts/senseaudio_video_gen.py compose --project executive-demo --brief "Make a premium launch film for an AI research assistant." --duration 12 --style-preset executive-film --offline --render
python3 scripts/senseaudio_video_gen.py compose --project demo-compose --brief "Introduce a sound library webpage" --style-preset neon-console --beat-mode layered --offline
python3 scripts/senseaudio_video_gen.py compose --project editorial-demo --brief "Introduce this website professionally" --site-url https://www.anthropic.com/ --site-screenshots --style-preset editorial-pro --offline
python3 scripts/senseaudio_video_gen.py beats --project demo-compose --json
python3 scripts/senseaudio_video_gen.py lint --project demo-compose --json
python3 scripts/senseaudio_video_gen.py timeline --project demo-compose --preset cinematic --transition-preset editorial --timeline-engine gsap-compat
python3 scripts/senseaudio_video_gen.py audio-data --project demo-compose --audio demo-compose/assets/narration.mp3 --output demo-compose/assets/audio-data.json --dry-run
python3 scripts/senseaudio_video_gen.py motion-audit --project demo-compose --json
python3 scripts/senseaudio_video_gen.py motion-map --project demo-compose --json
python3 scripts/senseaudio_video_gen.py music-create --prompt "Instrumental premium website explainer bed, subtle pulse, no vocals" --duration 16 --dry-run
python3 scripts/senseaudio_video_gen.py mix-audio --project demo-compose --voice demo-compose/assets/narration.mp3 --music demo-compose/assets/background-music.mp3 --output demo-compose/assets/final-audio.m4a --duration 16 --dry-run --json
python3 scripts/senseaudio_video_gen.py repair --project demo-compose --dry-run --json
python3 scripts/senseaudio_video_gen.py build --project demo-compose --dry-run
python3 scripts/senseaudio_video_gen.py generate-assets --project demo-compose --image-prompt "product UI hero" --video-prompt "creator b-roll" --dry-run
python3 scripts/senseaudio_video_gen.py init demo-video --duration 1 --fps 2
python3 scripts/senseaudio_video_gen.py render demo-video --output demo-video/renders/demo.mp4 --quiet
python3 scripts/senseaudio_video_gen.py render demo-video --output demo-video/renders/demo-fast.mp4 --parallel 2 --resume --quiet
python3 tests/test_cli.py
```

## One-Pass Project

```bash
export SENSEAUDIO_API_KEY="..."
python3 scripts/senseaudio_video_gen.py site-video \
  --url https://www.anthropic.com/ \
  --project anthropic-site-video \
  --brief "用中文介绍 Anthropic 官网的 Claude、安全 AI、研究与企业能力。" \
  --duration 14 \
  --fps 30 \
  --llm audioclaw \
  --music \
  --music-poll \
  --auto-repair
```

`site-video` is the recommended HyperFrames-like path for website explainers. It defaults to `editorial-pro`, layered beats, cinematic motion, GSAP-compatible timing, real website screenshots, AudioClaw LLM planning, SenseAudio TTS/ASR when not offline, audio-reactive data, render, `inspect`, `frame-quality-audit`, `motion-audit`, and `motion-map`. Add `--music --music-poll` to create and mix a SenseAudio music bed; `--music-fallback` is enabled by default so a local ambient bed is mixed when SenseAudio accepts the task but does not return `audio_url` in time. Add `--auto-repair` to run one repaired rerender after audits. If the selected LLM route fails, `--llm-fallback` keeps the pipeline moving with heuristic planning and records the warning in `pipeline-report.json`. If the AudioClaw configured model is weak for a research-heavy product film, use `--llm openrouter --llm-model <capable-model>`.

For sites where a clean browser sees a login wall, wrong region, consent overlay, or anti-bot interstitial, use a dedicated capture profile or exported cookies:

```bash
python3 scripts/senseaudio_video_gen.py site-video \
  --url https://example.com/ \
  --project example-site-video \
  --browser-profile profiles/example-capture \
  --cookie-file cookies/example.json
```

Cookies can improve screenshot fidelity because Chrome sees the same region/session state as a real visitor. Keep this explicit: clean capture is still the default so videos do not accidentally include personalized or private account content.

Use `--offline --no-render` to create the same editable project and pipeline report without live SenseAudio calls or frame rendering.

```bash
export SENSEAUDIO_API_KEY="..."
python3 scripts/senseaudio_video_gen.py compose \
  --project webpage-intro \
  --brief "Show the SenseAudio sound library and explain search, filters, voice clone, and one-click use." \
  --duration 9 \
  --voice-id male_0028_a \
  --generate-images \
  --generate-broll \
  --render
```

Use `--offline` to create the same editable HTML project without calling SenseAudio.
`compose` defaults to `--llm audioclaw`; if the default LLM route is unavailable, `--llm-fallback` keeps the draft moving with heuristic planning and records the warning in `senseframe.json`.
Use `--asset-dry-run` to add image/video planned assets and manifest requests without spending image/video credits.
Use `generate-assets --poll` to submit b-roll video generation, poll until completion, download the MP4, and bind matching `data-asset` slots.
Live `compose` generates SenseAudio TTS by default when `SENSEAUDIO_API_KEY` is available and `--offline` is not set. `render` also auto-muxes a registered `narration` audio asset when `--audio` is omitted; pass `--audio` to override it. Use `render --capture-mode process` only when you explicitly want the older one-Chrome-process-per-frame behavior.

`render` prefers a registered `final-audio` asset before `narration`, so `mix-audio` projects keep music and voice together without passing `--audio` every time.

## LLM Planning

```bash
python3 scripts/senseaudio_video_gen.py llm-plan \
  --brief "Introduce the SenseAudio sound library with search, filters, cloning, and one-click use." \
  --duration 9 \
  --output plan.json

python3 scripts/senseaudio_video_gen.py compose \
  --project webpage-intro \
  --brief "Introduce the SenseAudio sound library with search, filters, cloning, and one-click use." \
  --plan-file plan.json \
  --offline
```

`llm-plan` defaults to AudioClaw and can run from either `AUDIOCLAW_LLM_*` env vars or the local AudioClaw config file.

DeepSeek remains available when explicitly requested:

```bash
export DEEPSEEK_API_KEY="..."
python3 scripts/senseaudio_video_gen.py llm-plan \
  --brief "Introduce the SenseAudio sound library." \
  --provider deepseek \
  --duration 9 \
  --output plan.json
```

DeepSeek defaults to `deepseek-v4-pro`. Set `DEEPSEEK_MODEL`, `DEEPSEEK_BASE_URL`, `--llm-model`, or `--llm-base-url` when using a custom OpenAI-compatible endpoint.

OpenRouter can replace AudioClaw for stronger planning when needed:

```bash
export OPENROUTER_API_KEY="..."
python3 scripts/senseaudio_video_gen.py llm-plan \
  --brief "Introduce Claude Code as a concrete developer workflow product." \
  --provider openrouter \
  --model google/gemini-3.1-flash-lite \
  --duration 12 \
  --output plan.json
```

For `compose` or `site-video`, use `--llm openrouter --llm-model <capable-model>`. The defaults read `OPENROUTER_LLM_MODEL`, then `OPENROUTER_MODEL`, then `google/gemini-3.1-flash-lite`.

Inside AudioClaw, the configured model is used automatically. You can still be explicit:

```bash
python3 scripts/senseaudio_video_gen.py llm-plan \
  --brief "Introduce Anthropic's website in Chinese." \
  --provider audioclaw \
  --duration 10 \
  --output plan.json

python3 scripts/senseaudio_video_gen.py compose \
  --project webpage-intro \
  --brief "Introduce Anthropic's website in Chinese." \
  --site-url https://www.anthropic.com/ \
  --site-screenshots \
  --llm audioclaw \
  --offline
```

`--provider audioclaw` reads the local AudioClaw config file by default. Set `AUDIOCLAW_CONFIG_PATH`, `AUDIOCLAW_LLM_MODEL`, `AUDIOCLAW_LLM_BASE_URL`, or `AUDIOCLAW_LLM_API_KEY` to override it.
