---
name: wechat-article-video
description: Convert Chinese WeChat public-account articles and supplied images into publish-ready vertical WeChat Channels videos. Use for 公众号转视频、图文转视频、医药或药械招商、企业和产品推荐、视频号日更、批量出片, including article analysis, fact-safe scripting, 9:16 layout direction, edge-tts narration, subtitle synchronization, HyperFrames or Remotion rendering, visible first-frame covers, and delivery QA.
---

# WeChat Article Video

Produce a complete WeChat Channels package from an article and its images:

- `video.mp4`: 1080x1920, 30 fps, H.264/AAC
- `cover.jpg`: usable both as frame 0 and as the platform upload cover
- `voiceover.mp3` and `voiceover.srt`
- `storyboard.json` and `timeline.json`
- `publish-copy.md`
- `qa-report.json` and `contact-sheet.jpg`

Default to Chinese, `9:16`, `edge-tts`, synchronized burned-in captions, and a visible cover beginning at frame 0. Preserve medical disclaimers and never expand claims beyond the supplied source.

## Choose The Production Mode

Choose from the article's purpose, not its word count:

| Mode | Duration | Use |
| --- | ---: | --- |
| `brief` | 15-25s | 招商快讯、活动提醒、单一行动 |
| `compact-standard` | 30-40s | 企业/产品推荐的完整信息短版；视频号日更首选 |
| `standard` | 40-75s | 企业入驻、产品推荐、平台宣传; default |
| `detail` | 75-120s | 政策、专题或多产品解读 |

Default enterprise/product recommendations to `compact-standard` when the user wants a concise WeChat Channels video. Keep `standard` when the article needs more explanation or a calmer pace. Do not force an enterprise/product recommendation into 15 seconds.

For `compact-standard`, preserve the key-information matrix while compressing narration:

- company identity plus the strongest date, capital, or scale fact
- material qualification or domain credibility
- every featured product name and dosage form
- each product's main source-supported indication/use
- material specifications when they distinguish the product
- one platform action and the complete required disclaimer

Use “core facts in voiceover + complete key points on screen.” Do not require every visible fact to be spoken. Target 34-38 seconds when an exact 30 seconds would require deleting key information or making text/voice unreadable.

## Choose One Renderer

Use one renderer per video. Both consume the same `storyboard.json` and `timeline.json`.

- **HyperFrames, default**: use for one-off daily articles and visually tailored 30-90 second videos. Read the available `hyperframes`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-animation`, and `hyperframes-cli` skills before authoring. Read HyperFrames Creative's `house-style.md` and `video-composition.md`; they specifically prevent web-card/PPT-looking frames.
- **Remotion, batch-template option**: use when the user explicitly requests Remotion or when a stable React/TypeScript template is being parameterized for repeated batch production. Read `remotion-best-practices` and its `rules/video-layout.md` and `rules/subtitles.md` before editing Remotion code.

Do not render a single composition through both engines. Do not claim a renderer is used unless the project source and render command actually use it.

## Workflow

### 1. Build A Source Bundle

Create a per-article project and preserve original files:

```text
source/
  article.md
  images/
  notes.md
production/
release/
```

Copy supplied assets into `source/images/`; never edit originals in place. Verify every copied file exists, then inspect it visually. Record its subject, crop safety, useful claim, and risks before writing the storyboard. Read [references/content-and-compliance.md](references/content-and-compliance.md).

Treat missing or inaccessible supplied images as blocking. Ask the user to reattach them or use an already verified project copy. Do not create a renderable storyboard containing placeholder asset IDs, unverified candidate objects, or paths in temporary WeChat directories.

### 2. Make An Evidence Map

Extract:

- article objective and one intended viewer action
- company, product, dates, numbers, indications, specifications, and platform claims
- source paragraph for every factual narration sentence
- mandatory disclaimer
- unsupported or illegible details that must not enter the video

Write `production/content-brief.json`. For medical/pharma content, factual traceability is mandatory.

### 3. Write The Storyboard Before Code

Read [references/storyboard-schema.md](references/storyboard-schema.md) and [references/layout-system.md](references/layout-system.md). Use 6-8 purposeful scenes for `compact-standard` and 4-8 for `standard`. Each scene must define:

- narrative job
- source references
- layout template
- focal asset and intended crop
- on-screen text hierarchy
- caption range
- motion intent
- first meaningful visual deadline

Use these layout templates:

- `cover`
- `company-profile`
- `product-hero`
- `fact-focus`
- `cta`

Do not repeat the same template for adjacent product scenes without changing composition, focal position, or information structure.

Validate before generating TTS:

```bash
python scripts/validate_storyboard.py \
  --input production/storyboard.json \
  --content-brief production/content-brief.json \
  --project-root .
```

Do not continue when validation reports inaccessible assets, blocked source status, unknown source references, or invalid asset field types.

### 4. Generate One Continuous Voiceover

Write the complete spoken script to `production/voiceover.txt`. Keep punctuation deliberate because it controls cadence. Normalize symbols for speech while keeping display text faithful:

- `1999年` may be spoken as `一九九九年`
- `2ml` may be spoken as `二毫升`
- brand symbols such as `®` normally stay on screen but are omitted from speech

Generate one continuous stream so voice, pacing, and loudness remain consistent:

```bash
python scripts/edge_tts_generate.py \
  --text production/voiceover.txt \
  --audio production/voiceover.mp3 \
  --subtitles production/voiceover.srt \
  --voice zh-CN-XiaoxiaoNeural \
  --rate +5%
```

Use another Edge voice/rate only when the user asks or the article tone clearly requires it. Do not silently switch to a paid TTS provider.

For `compact-standard`, start between `+12%` and `+20%`. Do not exceed `+20%` merely to hit 30 seconds. If narration still exceeds 40 seconds, remove connective/repeated wording, move supporting facts to on-screen text, preserve all critical claims, and accept 35-38 seconds instead of rushed speech.

### 5. Let Subtitle Boundaries Drive Timing

Map subtitle entries to scenes in `production/scene-map.json`, then build the shared timeline:

```bash
python scripts/subtitles_to_timeline.py \
  --subtitles production/voiceover.srt \
  --scene-map production/scene-map.json \
  --offset 1.5 \
  --tail 0.8 \
  --output production/timeline.json
```

The default 1.5-second lead-in gives the cover a readable silent beat. Place the full voiceover at `timeline.audio_start_sec`; captions and narration scenes use the shifted timestamps from `timeline.json`. Never estimate caption timing by character count after real Edge boundaries exist.

### 6. Author Layout Before Animation

Create the complete static end-state of every scene first. A frame must remain useful with all animation disabled. Then add restrained, seek-safe motion.

Hard layout rules:

- frame 0 is a complete cover, never a black-to-image fade
- main content occupies the visual field; do not leave the lower half unused
- product imagery is usually 60-80% of frame width
- cover headlines are normally 84-108 px at 1080x1920
- scene headlines are normally 72-96 px
- body text is normally 36-48 px; captions 44-54 px
- captions sit in a dedicated safe zone and never cover packaging, QR codes, CTA, or disclaimers
- meaningful scene content is visible within 0.4 seconds
- animation emphasizes existing content; it must not create an initially empty frame
- avoid nested cards, repeated equal cards, tiny UI labels, and generic website layouts

HyperFrames: keep media as direct children of the composition root, start the voiceover at `timeline.audio_start_sec`, register one paused seekable timeline, use deterministic assets, and run `npx hyperframes check`.

Remotion: convert seconds to frames with the composition FPS; convert captions to Remotion's `Caption` type in milliseconds. Use frame-derived `interpolate()` animation, `<Sequence>` for timing, `<Img>`/`<Audio>` for media, and no CSS transitions or CSS animations.

### 7. Preview And Inspect The Whole Video

Before final render, inspect at least the start, middle, and end of every scene. For HyperFrames use snapshots; for Remotion render stills. Build a contact sheet after rendering:

```bash
python scripts/make_contact_sheet.py \
  --video release/video.mp4 \
  --timeline production/timeline.json \
  --output release/contact-sheet.jpg
```

Reject the layout when:

- a scene looks empty at entry
- the product resembles a thumbnail
- more than roughly one third of the frame is purposeless blank space
- adjacent scenes share the same visual silhouette
- text hierarchy cannot be understood in one second
- captions are tiny or visually detached from the narration

### 8. Run Delivery QA

Read [references/qa.md](references/qa.md), then run:

```bash
python scripts/qa_video.py \
  --video release/video.mp4 \
  --timeline production/timeline.json \
  --cover release/cover.jpg \
  --report release/qa-report.json
```

QA must confirm:

- video and audio streams begin correctly
- first encoded frame is visible and non-black
- cover is built into the video and exported separately
- dimensions, codec, pixel format, fps, duration, and fast-start are suitable
- captions follow real Edge timing
- every `critical_claim_id` is represented in the storyboard and final contact sheet
- opening, middle, and closing frames were visually inspected
- medical facts and disclaimer match the article

Do not prepend a still with stream-copy concat. If post-processing is unavoidable, fully re-encode and rerun first-frame QA.

## Reference Routing

- Read [references/content-and-compliance.md](references/content-and-compliance.md) for article compression, evidence mapping, medical copy, and publish copy.
- Read [references/layout-system.md](references/layout-system.md) before designing any scene.
- Read [references/storyboard-schema.md](references/storyboard-schema.md) before creating or validating `storyboard.json`.
- Read [references/qa.md](references/qa.md) before final render and delivery.

## Final Handoff

Return links to the MP4 and cover plus resolution, duration, renderer, voice, synchronization status, first-frame verification, and any compliance caveat. Keep editable project files with the release so the next daily article can reuse the design system.
