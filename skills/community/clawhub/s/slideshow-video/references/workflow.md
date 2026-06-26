# Slideshow workflow

## Full pipeline

1. Collect 5 to 8 portrait-friendly images, prepare remote image URLs, or define image queries.
2. Draft slide copy in a project JSON file.
3. Generate 1080x1920 PNG slides with `scripts/generate_slides.py`.
4. Optionally attach a background music file or URL in the project JSON.
5. Export the PNG set to MP4 with `scripts/export_mp4.py` if the target surface prefers video.
6. Save caption, hashtags, audio settings, and output paths in `summary.json` with `scripts/run_pipeline.py`.
7. Upload the PNG set or MP4 to your scheduler or manual posting workflow.

## Shorts sync workflow

Use this path for TikTok or Shorts posts where voice timing must match the slide timing.

1. Write one spoken sentence per slide.
2. Generate one ordered audio file per sentence, such as `line_01.mp3`, `line_02.mp3`.
3. Keep on-screen text shorter than the sentence. Use captions as emphasis, not full transcript.
4. Generate slides in the same order.
5. Export with `scripts/export_sync_mp4.py` so the hold time comes from each line audio duration plus a small configurable pad.
6. Review the generated `.sync.json` file if you need to inspect per-slide timings.

This workflow is better than fixed `secondsPerSlide` when the post is voice-led or CTA-sensitive.

### Preferred stack for this workspace

- Images: GPT Image 2 via `image_generate`
- Voice: ElevenLabs
- Voice direction: male + professional by default; add more character and emotion when requested
- CTA: final slide and final spoken line should match; current preferred short CTA is `Visit Clawlite.ai`

Do not ship flat placeholder gradients as the final visual pass when GPT Image 2 generation is available.

## Recommended slide structure

Fixed-time slideshow:
- Slide 1: hook
- Slide 2: problem / setup
- Slide 3: point 1
- Slide 4: point 2
- Slide 5: point 3
- Slide 6: CTA

Hook rule: the first 3 seconds should usually deliver a contrarian claim, sharp curiosity gap, or direct payoff promise.
Voice-led synced short:
- Slide 1: hook
- Slide 2 to 3: simple definition
- Slide 4 to 6: concrete scenario
- Slide 7 to 10: differentiators
- Slide 11+: rule of thumb and CTA

Keep hooks under 10 words when possible. Keep body slides readable at phone distance.

## Image selection guidance

Prefer:
- portrait or crop-friendly images
- high contrast backgrounds
- minimal existing text in the image
- one clear subject per slide
- GPT Image 2 scenes with a realistic or cinematic product/tech aesthetic for production TikTok slideshows

Avoid:
- busy collages
- low-resolution screenshots
- backgrounds with bright hotspots behind the main text

## JSON authoring guidance

For each text block:
- `text`: the displayed copy
- `size`: start around 84 to 96 for the hook, 48 to 60 for body copy
- `y`: vertical anchor point in pixels
- `maxWidth`: keep between 820 and 940 for comfortable wrapping
- `bold`: use on the primary line only when possible

For project-level fields:
- `slug`: post identifier used for the output folder and mp4 name
- `caption`: final post caption
- `hashtags`: list of hashtags for downstream scheduling
- `video.enabled`: set false if you only want PNG slides
- `video.secondsPerSlide`: hold time per slide in the mp4
- `video.zoom`: enable a light Ken Burns style zoom
- `video.fade`: optional fade in duration
- `audio.path` or `audio.url`: optional background music source
- `audio.volume`: optional volume multiplier, defaults around `0.22`
- `defaultImageQuery`: optional fallback image query for the whole post
- each slide can use `imagePath`, `imageUrl`, or `imageQuery`

## Commands

Resolve image queries first:

```bash
python3 ~/.openclaw/skills/slideshow-video/scripts/resolve_images.py project.json --output build/resolved-project.json
```

Generate slides only:

```bash
python3 ~/.openclaw/skills/slideshow-video/scripts/generate_slides.py config.json --output-dir output/slides
```

Export mp4 from generated slides:

```bash
python3 ~/.openclaw/skills/slideshow-video/scripts/export_mp4.py output/slides output/post.mp4 --seconds-per-slide 3 --zoom --fade 0.35 --overwrite
```

Export a synced mp4 from per-line voice files:

```bash
python3 ~/.openclaw/skills/slideshow-video/scripts/export_sync_mp4.py output/slides ./line-audio output/post-sync.mp4 --overwrite
```

Run the full pipeline for one project:

```bash
python3 ~/.openclaw/skills/slideshow-video/scripts/run_pipeline.py project.json --output-root build --overwrite
```

Run a directory in batch:

```bash
python3 ~/.openclaw/skills/slideshow-video/scripts/batch_pipeline.py /path/to/projects --pattern "project-*.json" --output-root build --overwrite
```

Export mp4 with background music directly:

```bash
python3 ~/.openclaw/skills/slideshow-video/scripts/export_mp4.py output/slides output/post.mp4 --seconds-per-slide 3 --zoom --audio ./audio/bed.mp3 --audio-volume 0.2 --overwrite
```

The full pipeline writes:
- `build/<slug>/resolved-project.json`
- `build/<slug>/slides/*.png`
- `build/<slug>/<slug>.mp4`
- `build/<slug>/summary.json`
- `build/<slug>/cache/*` for downloaded remote images

`summary.json` includes the audio config when present.

Batch mode prints a JSON report with per-project status (`ok`/`failed`).

## Practical caveats

- Query-based image sourcing is convenience-first, not brand-safe by default. Review image choices before posting.
- Treat Pinterest, TikTok, and third-party hosted images as potential copyright risk. Validate licensing before commercial scale use.
- Do not rely on automation myths for account safety. Draft-based posting may reduce operational risk, but it is not a guarantee.
- Measure hooks and layouts with actual retention data. The production pipeline is only half the game.
- If sync still feels off, shorten the line, regenerate just that line audio, and re-export. Do not keep stretching the caption text to match the voice.
- If a user asks for “more human” or “more emotional” delivery, adjust the ElevenLabs voice settings and rewrite the spoken lines; do not just keep the same flat script with a different voice.
- If the user changes the CTA late, update both the last slide text and the last narration line so the end state stays consistent.
