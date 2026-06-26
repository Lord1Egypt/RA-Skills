# Local Renderer

The renderer serves the project on a local HTTP server, opens Chrome headless once per frame with `?t=<seconds>`, captures PNG screenshots, and assembles them with FFmpeg.

## Commands

```bash
python3 scripts/senseaudio_video_gen.py compose --project my-video --brief "..." --offline
python3 scripts/senseaudio_video_gen.py styles --json
python3 scripts/senseaudio_video_gen.py init my-video
python3 scripts/senseaudio_video_gen.py lint --project my-video --strict
python3 scripts/senseaudio_video_gen.py beats --project my-video --json
python3 scripts/senseaudio_video_gen.py timeline --project my-video --preset cinematic --transition-preset editorial --timeline-engine gsap-compat
python3 scripts/senseaudio_video_gen.py audio-data --project my-video --audio my-video/assets/narration.mp3 --output my-video/assets/audio-data.json
python3 scripts/senseaudio_video_gen.py motion-audit --project my-video --strict
python3 scripts/senseaudio_video_gen.py motion-map --project my-video --strict --samples 32
python3 scripts/senseaudio_video_gen.py inspect my-video --samples 7
python3 scripts/senseaudio_video_gen.py render my-video --fps 24 --output my-video/renders/final.mp4
python3 scripts/senseaudio_video_gen.py render my-video --audio my-video/assets/narration.mp3 --output final.mp4
python3 scripts/senseaudio_video_gen.py render my-video --parallel 4 --frame-dir my-video/renders/frames --resume --output final.mp4
python3 scripts/senseaudio_video_gen.py build --project my-video --output my-video/renders/final.mp4
```

`render` writes a JSON report next to the MP4 by default, and registers the rendered video in the project asset manifest when the project has `senseframe.json`.

`beats` writes `assets/beats.json` from the storyboard. Layered projects use these entries to bind `.beat-layer[data-beat]` overlays and matching local timeline tracks.

`motion-audit` should run before expensive renders. It verifies storyboard ids are present as DOM scenes, checks beat-layer binding, checks the seekable timeline registry, confirms transition/audio-reactive hooks, and warns if legacy fixed-template markers remain.

`motion-map` is the second-pass visual audit. It samples the whole duration, scores active scene motion, beat coverage, flashiness risk, timeline effects, entrance/exit phases, transition boundaries, and audio-reactive hooks, then reports dead zones and practical recommendations.

`timeline --transition-preset` writes authored transition boundaries into `assets/timeline.json` and patches the local runtime plan. Use `editorial` for mixed wipes/flashes, `glass` for luminous product UI, `ribbon` for fast explainers, `iris` for focused feature reveals, and `luma` for energetic sweeps.

`timeline --timeline-engine gsap-compat` adds local GSAP-like `labels` and `tracks` to the timeline JSON and binds them to `createGsapCompatTimeline`. The adapter supports the small render-safe subset this skill needs: `addLabel`, `set`, `to`, `fromTo`, and deterministic `seek(time)`. Do not load external GSAP from npm or CDN inside generated projects.

## Faster Renders

- `--parallel N` captures frames concurrently with separate headless Chrome processes.
- `--frame-dir <dir>` stores PNG frames in a stable directory.
- `--resume` skips existing non-empty frames, useful after interrupted renders.
- `--keep-frames` keeps generated frames for debugging or later reuse.

## Requirements

- Chrome or Chromium available in `PATH`, discoverable on macOS, or configured through `CHROME_BIN`.
- FFmpeg available in `PATH`.

## Troubleshooting

- If Chrome is not found, set `CHROME_BIN` to the browser executable.
- If output is black or incomplete, increase `--virtual-time-budget`.
- If render is slow, lower `--fps` for drafts and render final at 24 or 30 fps.
- If fonts differ between machines, use local web fonts in the project.
- If captions do not appear, confirm the page is served through `preview`, not opened as a raw `file://` URL; caption JSON is fetched by the runtime.
