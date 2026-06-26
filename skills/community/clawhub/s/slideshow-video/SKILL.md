---
name: slideshow-video
description: Generate TikTok-style slideshow assets and MP4 exports from local images, GPT Image 2 visuals, remote image URLs, or lightweight image queries plus structured copy. Use when creating 9:16 slideshow posts, turning hooks plus image sources into PNG slides, exporting those slides into a short vertical video, or building a low-cost short-form content pipeline with reusable JSON configs. Also use when producing shorts with sentence-level voice sync, tighter TikTok-style captions, per-line audio aligned to specific slides, or GPT Image 2 + ElevenLabs voice-led TikTok slideshows with explicit CTA endings.
---

# Slideshow Video

Generate a repeatable short-form slideshow pipeline from local images, GPT Image 2 outputs, remote image URLs, or lightweight image queries and a JSON project file. This skill covers query resolution, PNG slide generation, MP4 export, optional background music, remote image caching, sentence-level sync exports, and a simple project wrapper that saves output metadata for downstream scheduling.

## Default production preferences

For TikTok/shorts builds in this workspace, default to these choices unless the requester says otherwise:

- visuals: GPT Image 2 / `image_generate` scenes instead of flat synthetic gradients
- voice: ElevenLabs
- voice style: male, professional; when requested, push toward more personality and human emotion
- structure: one spoken sentence per slide, with shorter on-screen copy than the narration
- CTA: make the final slide and final voice line explicit; latest preferred short CTA is `Visit Clawlite.ai`

If a fast placeholder visual pass is used, do not present it as the final quality bar. Replace placeholder backgrounds with GPT Image 2 scenes before calling the slideshow ready.

## Quick start

1. Prepare 5 to 8 local images, GPT Image 2 outputs, remote image URLs, or image queries for one slideshow.
2. Copy `references/pipeline.example.json` to a working JSON file and replace the image sources and copy.
3. For production TikTok slideshows, generate or collect your GPT Image 2 scenes first, then write one voice line per slide for ElevenLabs.
4. Run the full pipeline:

```bash
python3 ~/.openclaw/skills/slideshow-video/scripts/run_pipeline.py your-project.json --output-root build --overwrite
```

To process a directory of project files, use:

```bash
python3 ~/.openclaw/skills/slideshow-video/scripts/batch_pipeline.py /path/to/projects --output-root build --overwrite
```

4. Review the generated slides and MP4 on a phone-sized canvas.
5. Use `summary.json` for caption and hashtag handoff into your posting workflow.

## Core resources

- `scripts/resolve_images.py`: resolve `imageQuery` values into usable remote image URLs
- `scripts/generate_slides.py`: generate 1080x1920 PNG slides from local images, remote image URLs, and text blocks
- `scripts/export_mp4.py`: convert ordered slide PNGs into an H.264 vertical MP4, with optional background music
- `scripts/export_sync_mp4.py`: export a voice-synced MP4 from slide PNGs plus per-line audio files, holding each slide for that line's measured duration
- `scripts/run_pipeline.py`: run one project and emit `summary.json`
- `scripts/batch_pipeline.py`: run multiple JSON project files from a directory
- `references/pipeline.example.json`: starter project file with slide, caption, hashtag, and video settings
- `references/slides-config.example.json`: simpler slide-only config when you do not need project metadata
- `references/workflow.md`: structure, command examples, shorts sync workflow, and practical caveats

## Project JSON format

At the top level, use:

- `slug`: identifier for output folders and the mp4 name
- `caption`: final post caption
- `hashtags`: list of hashtags
- `defaultImageQuery`: optional fallback query for image sourcing
- `video`: export options
- `audio`: optional background music options
- `slides`: the slide array

Inside `video`:

- `enabled`: set false to skip MP4 export
- `secondsPerSlide`: hold time per slide
- `fps`: output FPS, usually `30`
- `zoom`: enable a light Ken Burns style zoom
- `fade`: optional fade in duration per slide

Inside `audio`:

- `path`: local audio file
- `url`: remote audio URL if ffmpeg can read it in your environment
- `volume`: optional background music volume multiplier, defaults around `0.22`

For shorts that need strict voice sync, keep the project JSON focused on slide images plus on-screen text, then generate one audio file per spoken line outside the project JSON and export with `scripts/export_sync_mp4.py`.

Each slide accepts:

- `imagePath`: local source image
- `imageUrl`: remote source image
- `imageQuery`: short sourcing query such as `minimal finance desk`
- `overlay`: optional black overlay opacity from 0 to 255
- `blur`: optional Gaussian blur radius
- `brightness`: optional brightness multiplier, for example `0.9`
- `output`: optional output filename
- `text`: array of text blocks

Each text block accepts:

- `text`: required displayed text
- `size`: font size in pixels
- `bold`: boolean shortcut for heavier font selection
- `weight`: optional string, `bold` also works
- `x`: horizontal anchor, defaults to center
- `y`: vertical anchor
- `align`: `left`, `center`, or `right`
- `maxWidth`: wrapping width in pixels
- `color`: hex color, defaults to white
- `lineSpacing`: defaults to `1.2`
- `shadow`: defaults to true
- `strokeWidth` and `strokeFill`: optional text outline
- `fontPath`: optional absolute or local font path

## Dependencies

Install Pillow for slide generation:

```bash
python3 -m pip install pillow
```

Install ffmpeg for MP4 export if it is not already present.

Remote images are downloaded and cached automatically when you use `imageUrl` or when `imagePath` is itself an `http/https` URL.

When a slide only has `imageQuery`, the pipeline resolves it into a remote image URL first, writes `resolved-project.json`, then continues normally. Review resolved images before posting because query-based sourcing is convenience-first, not quality-safe.

## TikTok production defaults

- Prefer GPT Image 2 visuals with realistic or cinematic tech/product scenes.
- Prefer ElevenLabs for narration; start with a male professional voice, then lower stability / raise style modestly when the user wants more character.
- Make slide 1 a strong contrarian or curiosity hook that lands inside the first 3 seconds.
- Keep final CTA visible on-screen and also spoken in the last voice line.
- When shortening for retention, cut slide count before shrinking text legibility.

## Good defaults

- Keep slide 1 to one strong hook and one supporting line.
- Start hooks around `84` to `96` px.
- Start body lines around `48` to `60` px.
- Keep most text blocks within `820` to `940` px max width.
- Use one visual subject per slide when possible.
- Start with `3` seconds per slide and `zoom: true` for a more alive MP4.
- Start background music around `0.18` to `0.25` volume so it does not overpower on-screen text.
- For TikTok-native shorts, shorten on-screen text until each slide only carries one core idea.
- For voice-led shorts, prefer one spoken sentence per slide and use synced export instead of fixed `secondsPerSlide`.

## Editing guidance

Adjust readability in this order:

1. raise `overlay`
2. reduce `maxWidth`
3. lower font size slightly
4. move the `y` positions away from busy background areas
5. add `strokeWidth` if the image is still noisy

If the MP4 feels too static, enable `zoom`. If it feels too synthetic, disable it and keep the PNG slideshow output instead.

## Output expectations

## Shorts sync workflow

Use this when voice, image, and on-screen text must stay aligned.

1. Write one spoken sentence per target slide.
2. Generate one numbered audio file per sentence, for example `line_01.mp3`, `line_02.mp3`.
3. Build slide PNGs with matching numbered order.
4. Export with `scripts/export_sync_mp4.py` so each slide duration is based on the matching line audio length.
5. Keep captions shorter than the spoken line. Treat the slide text as reinforcement, not a transcript.

Example:

```bash
python3 ~/.openclaw/skills/slideshow-video/scripts/generate_slides.py project.json --output-dir build/slides --cache-dir build/cache
python3 ~/.openclaw/skills/slideshow-video/scripts/export_sync_mp4.py build/slides ./line-audio build/post-sync.mp4 --overwrite
```

The sync export also writes `<output>.sync.json` with per-slide measured durations.

## Output expectations

The pipeline writes:

- `build/<slug>/resolved-project.json`
- `build/<slug>/slides/*.png`
- `build/<slug>/<slug>.mp4`
- `build/<slug>/summary.json`
- `build/<slug>/cache/*` for downloaded remote images

`summary.json` includes audio metadata when present.

Keep generated outputs outside the skill folder unless you are intentionally updating bundled examples.
