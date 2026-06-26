# Workflow

Use this SOP for YouTube-to-Chinese or optional Chinese-English bilingual hard subtitle work. The final output includes a burned MP4, reusable subtitle files, design confirmation frames, and review notes.

## 1. Intake

Record the URL, title, channel, duration, intended use, output preference, subtitle mode, subtitle style profile, description language/translation status, cover edit preference, cover mode, and any glossary. If the user only gives a URL, default to Simplified Chinese hard subtitles for self-study/internal use, `zh-only-default` subtitle style, and ask whether the video thumbnail/cover should also be prepared for the Chinese-subtitled version. Bilingual mode is optional and should be used only when requested or clearly chosen; its default style is `bilingual-default`. If the user asks for direct end-to-end completion and does not mention cover work, do not stop for a cover question; keep the original thumbnail and record `cover edit: not requested` and `cover mode: none`.

Create a per-video workspace:

```text
01-source/
02-transcripts/
03-translation/
04-subtitle-ass/
05-output/
06-review/
07-cover/
08-description/
```

When downloading the video, also extract the original description and download the thumbnail:

```bash
python3 scripts/extract_youtube_description.py 01-source/<video-id>.info.json \
  --out 08-description/<video-id>.description.original.md
python3 scripts/download_youtube_thumbnail.py "<youtube-url>" --out-dir 01-source --format jpg
```

If the original description is not Chinese, translate it with the current agent model and save a Chinese version such as `08-description/<video-id>.description.zh.md`. Preserve proper nouns, product names, URLs, and chapter timestamps exactly where possible. Do not translate or rewrite URLs.

Keep the original thumbnail even if the user does not need cover editing. If the user wants a Chinese-subtitle cover, enter Cover Processing Mode below, create the edited cover under `07-cover/`, and keep the original and edited files listed in the review.

Before choosing final subtitle layout, extract source-video frames and check whether the original video already has burned-in subtitles:

```bash
python3 scripts/extract_source_subtitle_frames.py 01-source/source.mp4 \
  --out-dir 06-review/source-subtitle-check
```

Record one of these source subtitle states in the review:

- `no burned-in subtitles`: bilingual mode may be used.
- `burned-in English subtitles`: default to Chinese-only and move Chinese text away from the existing subtitle area, unless the user explicitly requests bilingual output anyway.
- `burned-in non-English or unstable subtitles`: inspect frame placement before deciding whether bilingual output is usable.

### Cover Processing Mode

Use this mode when the user asks to prepare, localize, or enhance the YouTube cover for the Chinese-subtitled version.

Default edit for a Chinese-subtitled version:

- Add `中文字幕` in a suitable empty area.
- Add author/source information in a YouTube-style format, for example `作者：<channel>` or `<channel> · @handle`.
- Choose and record one cover mode before editing:
  - `preserve-original-text`: default; keep all original cover text and add only `中文字幕` plus author/source.
  - `translate-original-text`: use only when the user explicitly asks to translate the existing cover copy.
  - `localized-rewrite`: use only when the user asks for a Chinese-platform cover or literal translation is visibly weak.
- Keep all original cover text exactly as-is in the default `preserve-original-text` mode. Do not translate, rewrite, erase, or replace original thumbnail wording by default.
- Preserve the original cover composition, face, product signal, logo, and main title unless the user explicitly requests a redesign.
- Do not cover faces, important UI, product marks, or existing large title text.
- Use a consistent label treatment: `中文字幕` as the prominent label, author/source as the smaller secondary label, both with bold high-contrast text and thick outline or solid label background.
- Save the edited cover as `07-cover/<video-id>.cover.zh.v1.png` or another versioned filename.
- Create a thumbnail-size preview and inspect that, not only the full-size cover:

```bash
python3 scripts/make_cover_preview.py 07-cover/<video-id>.cover.zh.v1.png \
  --out 07-cover/<video-id>.cover.zh.v1.preview-320.jpg
```

If using image generation/editing, copy the generated image into `07-cover/` and leave the generator's original output in place. Verify the edited cover and the 320px preview visually before delivery.

## 2. Source and English Transcript

Prefer subtitle sources in this order:

1. Official English subtitle.
2. YouTube automatic English subtitle.
3. Local ASR transcript.

Save the raw source and never overwrite it. Mark automatic captions clearly because they often contain overlap, duplicated fragments, bad casing, and weak sentence boundaries.

If YouTube translated Chinese captions fail with rate limits or repeated download errors, do not keep retrying the same endpoint. Record the failure, use English captions as the source, and translate with the current agent model.

Clean the English baseline only enough to make it traceable and useful: remove noise, fix obvious ASR errors, and repair broken sentence boundaries. Do not rewrite the speaker's argument.

For YouTube rolling VTT/SRT captions, first create a cleaned cue baseline. If `yt-dlp --convert-subs srt` deleted the VTT, use the converted SRT directly:

```bash
python3 scripts/prepare_youtube_transcript.py 01-source/<video-id>.en.srt \
  --json-out 02-transcripts/<video-id>.en.cues.json \
  --srt-out 02-transcripts/<video-id>.en.cleaned.srt
```

## 3. Chinese Translation

Default to translating with the current agent model. External LLM APIs and command-line translation tools are fallbacks only.

Translate in numbered batches with nearby context. Maintain a glossary for names, products, commands, and technical terms. Write natural Simplified Chinese for watching, not article prose.

Use the stable `id` values from `02-transcripts/<video-id>.en.cues.json`. Do not renumber batches by hand after cleaning or repair.

Use a cache file such as `03-translation/<video-id>.zh.cache.json`:

```json
[
  {"id": 1, "zh": "你来对地方了。"},
  {"id": 2, "zh": "如果你正在使用 ChatGPT、Claude 或 Codex。"}
]
```

Generate pending batches for agent-model translation:

```bash
python3 scripts/make_translation_batches.py 02-transcripts/<video-id>.en.cues.json \
  --out-dir 03-translation/translation-batches \
  --cache 03-translation/<video-id>.zh.cache.json \
  --max-chars 6000
```

For each batch, the agent model must return JSON only, keep every `id`, and preserve product names such as Codex, ChatGPT, Claude, Claude Code, GitHub, OpenAI, Chronicle, Computer Use, and MCP. After each batch, append or update the cache before continuing. For long videos, reduce `--batch-size` or `--max-chars` before translating if a batch looks too large to check reliably.

For long videos, after each translation batch is applied to the cache, spot-check a few ids from the beginning, middle, and end of that batch against the English source. Confirm that names, negation, numbers, and spoken intent remain aligned before moving to the next batch. Do not wait until the final ASS stage to discover a batch-level drift.

Write the checked cache back to SRT:

```bash
python3 scripts/apply_translation_cache.py 02-transcripts/<video-id>.en.cues.json \
  03-translation/<video-id>.zh.cache.json \
  --srt-out 03-translation/<video-id>.zh.v1.srt
```

After translation, compress only unnecessary filler. Do not remove numbers, negation, conditions, caveats, or speaker intent.

Save the final Chinese subtitle as a versioned SRT file so it can be reused outside the burned video.

## 4. Timing and Semantic Screens

Before ASS generation, run the subtitle quality checker. Fix all overlap and empty cue errors.

Build subtitles as semantic screens:

- Keep each screen as a complete sentence or closed meaning block.
- Allow two or three lines when needed, but avoid half-sentences.
- Do not end a screen with dangling connectors or incomplete predicates.
- Do not end a screen with punctuation that signals an unfinished thought, such as `，`、`、`、`：`、`；`.
- Merge very short flashes when they belong to the same spoken idea.
- Split long blocks at natural Chinese semantic boundaries, then make each block read as complete.
- After fixing dangling endings, check for subtitle screens that are still too long or dense; passing the dangling-ending check alone is not enough.

If the user reports that a screen is incomplete, first repair segmentation and sentence closure. Do not only extend display duration.

Run the repair helper after initial translation, then re-check:

```bash
python3 scripts/repair_chinese_subtitles.py 03-translation/<video-id>.zh.v1.srt \
  --out 03-translation/<video-id>.zh.v2.srt
python3 scripts/check_subtitle_quality.py 03-translation/<video-id>.zh.v2.srt
```

When converting to Chinese-only ASS, use semantic line wrapping. Product names, English phrases, code, commands, and number/unit pairs must not be split across lines.

```bash
python3 scripts/srt_to_ass.py 03-translation/<video-id>.zh.v2.srt \
  --out 04-subtitle-ass/<video-id>.zh.v2.ass
python3 scripts/check_subtitle_quality.py 04-subtitle-ass/<video-id>.zh.v2.ass
python3 scripts/check_subtitle_style.py 04-subtitle-ass/<video-id>.zh.v2.ass \
  --style-profile zh-only-default --require-version-comment
```

### Optional Bilingual ASS

Use bilingual mode only when the source subtitle state allows it or the user explicitly requests it. The layout is Chinese above English:

- Default to `Chinese primary, English auxiliary`: keep the reviewed Chinese semantic screens as the main readable subtitle, and add smaller English below only as a reference line.
- Do not fragment good Chinese subtitles just to make English align word-for-word. If exact bilingual pairing makes Chinese jumpy or incomplete, keep the Chinese semantic timing and shrink/soften the English line instead.
- Chinese should normally stay one line and may use two lines when needed.
- English should stay smaller than Chinese and visually secondary. Dense English is a warning to inspect in preview frames, not a reason to make the whole subtitle block large.
- Total subtitle area defaults to at most three lines.
- If Chinese would become three lines, repair or split the Chinese SRT before generating bilingual ASS.
- If English becomes too long or distracting in preview, first reduce English font size or clean obvious source-caption filler; only split Chinese timing when the Chinese screen itself remains natural.

Generate bilingual ASS from the reviewed Chinese SRT and cleaned English SRT:

```bash
python3 scripts/make_bilingual_ass.py \
  --zh-srt 03-translation/<video-id>.zh.v2.srt \
  --en-srt 02-transcripts/<video-id>.en.cleaned.srt \
  --out 04-subtitle-ass/<video-id>.zh-en.v1.ass
python3 scripts/check_subtitle_quality.py 04-subtitle-ass/<video-id>.zh-en.v1.ass
python3 scripts/check_subtitle_style.py 04-subtitle-ass/<video-id>.zh-en.v1.ass \
  --style-profile bilingual-default --require-version-comment
python3 scripts/check_bilingual_alignment.py \
  --zh-srt 03-translation/<video-id>.zh.v2.srt \
  --en-srt 02-transcripts/<video-id>.en.cleaned.srt \
  --report 06-review/bilingual-alignment.md
```

If bilingual output looks visually mismatched because semantic Chinese screens are paired with fragmented rolling English captions, do not accept it only because timing checks pass. Review the alignment report samples against the source speech: opening, midpoint, ending, and dense speech sections must have Chinese meaning, English reference, and voice timing in the same neighborhood. Compare two short preview options if needed: (1) Chinese-primary with smaller auxiliary English, and (2) matched cue boundaries. Prefer the option that keeps Chinese readable and the subtitle block calm. Use matched cue boundaries only when it does not make Chinese fragmented.

Before preview/full burn, explicitly check for visible newline artifacts such as stray `N` characters. These usually mean an ASS line break was escaped incorrectly and must be fixed before delivery.

Use the bilingual ASS for preview and burn-in. Keep the English SRT, Chinese SRT, and bilingual ASS as delivery files.

## 5. Subtitled Preview Before Full Burn

Do not burn the full video until the user has checked a subtitled preview clip.

Generate a one-minute preview with burned subtitles:

```bash
python3 scripts/make_preview_clip.py 01-source/source.mp4 04-subtitle-ass/translated.zh.ass \
  --out 06-review/preview.v1.mp4 --style-profile zh-only-default
```

The preview must visibly contain subtitles. If the first minute has no subtitle cue, extend the preview duration or move to the first subtitle-bearing window. The helper does this automatically when possible.

After creating the preview, extract design confirmation frames before full burn:

```bash
python3 scripts/extract_design_frames.py 06-review/preview.v1.mp4 \
  04-subtitle-ass/<video-id>.zh-en.v1.ass \
  --out-dir 06-review/design-confirmation-v1
```

Ask the user to confirm readability, size, outline, position, line count, and whether the subtitle is visually prominent enough when the user expects an intermediate review. For bilingual mode, the confirmation must verify that Chinese is above English and the subtitle area does not feel too large. If the user asks you to handle the full job directly, self-check preview screenshots and design confirmation frames and continue without stopping; record that preview readability was self-checked.

After preview and design-frame approval, still generate screenshots from the final MP4 at:

- first minute
- midpoint
- final minute
- dense UI or code area
- any user-reported timestamp

Default style direction:

- use the fixed style profiles: `zh-only-default` for Chinese-only, `bilingual-default` for bilingual, and a `*-raised` profile only when bottom UI, captions, faces, code, or controls would be covered
- high contrast white Chinese text with thick dark outline
- readable on phone-sized playback
- bottom center unless it covers important UI
- record the reason when using `zh-only-raised` or `bilingual-raised`
- for bilingual output, Chinese above English, Chinese larger, English smaller, total subtitle area normally no more than three lines
- for bilingual output, sample the first minute specifically for stray `N`, mismatched Chinese/English pacing, and whether the English line makes the layout feel cluttered

Do not invent a new size for each video. If the fixed profile looks small, thin, too tall, crowded, or easy to miss, first try the corresponding raised profile when the issue is placement; only create a documented exception when both fixed profiles fail.

## 6. Full Burn-in

Use ffmpeg with libass-compatible ASS subtitles. Output MP4 with video and audio preserved or encoded to broadly compatible H.264/AAC.

Before burning the full video, check whether the available ffmpeg can burn subtitles:

```bash
python3 scripts/check_ffmpeg_subtitle_support.py
```

If the default ffmpeg lacks `ass` or `subtitles` filters, first use another ffmpeg build with libass support if one is already available. If no checked ffmpeg can burn subtitle files, use the PIL hard-subtitle fallback instead of writing a one-off project script:

```bash
python3 scripts/burn_subtitles_pil.py 01-source/source.mp4 \
  04-subtitle-ass/translated.zh.ass \
  --out 05-output/<video-id>.zh-burned.vN.mp4
```

For smoke tests or style tuning, render a short segment first:

```bash
python3 scripts/burn_subtitles_pil.py 01-source/source.mp4 \
  04-subtitle-ass/translated.zh.ass \
  --out 06-review/burn-smoke.vN.mp4 \
  --start 00:02:05 --duration 8
```

Do not wait until the final burn to discover missing ffmpeg subtitle support, and do not leave the fallback renderer as an ad hoc file in the project workspace.

Use versioned filenames such as:

```text
03-translation/<video-id>.zh.v1.srt
04-subtitle-ass/<video-id>.zh.v1.ass
04-subtitle-ass/<video-id>.zh-en.v1.ass
05-output/<video-id>.zh-burned.v1.mp4
05-output/<video-id>.zh-en-burned.v1.mp4
05-output/<video-id>.zh-burned.v2-reviewed.mp4
```

Never overwrite prior MP4, SRT, or ASS outputs. If an output path already exists, choose the next versioned filename instead of forcing overwrite.

## 7. Review and Delivery

Run:

```bash
python3 scripts/check_subtitle_quality.py path/to/final.srt
python3 scripts/check_subtitle_quality.py path/to/final.ass
python3 scripts/check_subtitle_style.py path/to/final.ass --style-profile zh-only-default --require-version-comment
python3 scripts/inspect_video.py path/to/final.mp4
python3 scripts/extract_review_frames.py path/to/final.mp4 --out-dir 06-review/screenshots-final
```

Use `review-template.md` for `06-review/review.md`. Delivery is blocked until quality gates pass or every exception is explicitly recorded.

Delivery should list the burned MP4, the final Chinese SRT, the final English SRT when bilingual mode is used, the final ASS file, subtitle style profile, bilingual alignment report when bilingual mode is used, design confirmation frames, the original thumbnail, the original description, and the Chinese description if translation was needed. If the user requested cover editing, also list the cover mode, edited cover, and 320px cover preview. If a subtitle, description, cover, or design frame file is intentionally omitted, record why in the review.

## 8. Feedback Iteration

When the user reports a subtitle issue:

1. Locate the exact timestamp and subtitle block.
2. Classify it as translation, segmentation, timing, hold duration, size, occlusion, terminology, or readability.
3. Fix the current output and re-run checks.
4. Record it with `scripts/record_feedback.py`.
5. If reusable, add the preventive rule to quality gates and this workflow.
6. Re-package the skill so future runs inherit the update.
