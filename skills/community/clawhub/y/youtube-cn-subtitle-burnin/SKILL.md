---
name: youtube-cn-subtitle-burnin
description: Create Simplified Chinese or Chinese-English bilingual hard-subtitled videos from YouTube links or existing video/subtitle files. Use when the user asks to add/burn Chinese subtitles, translate YouTube videos, produce Chinese or bilingual SRT/ASS/MP4 outputs, download or prepare YouTube thumbnails/covers, extract or translate YouTube descriptions, add Chinese-subtitle labels or author information to covers, review subtitle readability, fix subtitle timing/splitting/size/occlusion problems, or incorporate user subtitle feedback into the workflow.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://github.com/woodenxyz/youtube-cn-subtitle-burnin
    emoji: "🎬"
    requires:
      bins:
        - python3
        - ffmpeg
        - ffprobe
        - yt-dlp
---

# YouTube Chinese Subtitle Burn-in

## Overview

Turn a YouTube video into a Simplified Chinese or optional Chinese-English bilingual hard-subtitled MP4 and deliver the reusable subtitle files alongside it. Retain SRT/ASS, thumbnail, original/translated description, screenshots, design confirmation frames, and review notes. Treat subtitle quality as a video QA task, not just a translation task.

## Workflow Decision

1. **New YouTube link**: follow `references/workflow.md` end to end.
2. **Existing subtitle/video needs fixing**: inspect the current outputs, then run only the affected workflow stages.
3. **User reports a subtitle problem**: locate the exact timestamp/subtitle first, then follow "Feedback Iteration" below.

Always load:

- `references/workflow.md` before producing a video.
- `references/quality-gates.md` before accepting or delivering a result.
- `references/review-template.md` when writing the review file.
- `references/feedback-ledger.md` when the user gives feedback about a subtitle problem.

## Non-Negotiable Rules

- Do not deliver a video until subtitle timing, sentence completeness, video streams, and sample screenshots have been checked.
- Do not treat the burned MP4 as the only deliverable. The final Chinese subtitle files must be kept and listed for delivery.
- Download and retain the original video thumbnail when downloading the video.
- Extract and retain the original YouTube description. If the description is not Chinese, translate it into Chinese with the current agent model and preserve proper nouns, product names, URLs, and chapter timestamps.
- Ask whether the video thumbnail/cover should be prepared for the Chinese-subtitled version unless the user already specified a cover preference. If the user asks for direct end-to-end completion and did not mention cover work, keep the original thumbnail only and record `cover edit: not requested`.
- Do not burn the whole video with an unreviewed subtitle style. First create a subtitled one-minute preview clip and confirm readability, especially font size and outline. If the first minute has no subtitles, extend or move the preview until subtitles are visible.
- Before full burn-in, extract 3-5 subtitle design confirmation frames from the preview and confirm size, line count, vertical position, and occlusion. In direct-completion mode, self-check these frames and record the result.
- When the user asks you to handle the whole job directly, self-check the preview with screenshots and continue instead of stopping for preview approval. Record that preview readability was self-checked.
- Default to translating with the current agent model. External LLM APIs or command-line translation tools are fallbacks only, not the main path.
- For long subtitles, translate through numbered batches from the stable `id` values in the cleaned cue JSON, verify every id is returned, save a cache after each batch, and resume from the cache if interrupted.
- Prefer semantic-screen subtitles: each screen should contain a complete sentence or closed meaning block. Avoid ending a screen with dangling words such as "所以，", "并且", "接下来要", "我要", "它会", or "然后会".
- Do not wrap subtitles by raw character count alone. Keep Chinese phrases, product names, English phrases, code, commands, and number/unit pairs intact across line breaks.
- Treat YouTube automatic subtitles as risky. Always check overlap before converting to ASS or burning.
- Bilingual mode is optional. Default to Chinese-only unless the user asks for bilingual subtitles. If the source video already has burned-in English subtitles, default to Chinese-only and move Chinese text away from the existing subtitle area unless the user explicitly requests bilingual output anyway.
- In bilingual mode, use Chinese above English. Chinese may use at most two lines, English defaults to one smaller line, and the whole subtitle area defaults to at most three lines. If Chinese would require three lines, repair or split the Chinese subtitles before generating bilingual ASS.
- If YouTube translated Chinese captions are rate-limited or unavailable, stop retrying after a small number of attempts and use English captions plus the current agent model. Record the source limitation in the review.
- Never overwrite previous MP4/SRT/ASS outputs. Create a new version and record what changed.

## Scripts

Use these helpers from the skill directory:

```bash
python3 scripts/check_subtitle_quality.py path/to/subtitles.srt
python3 scripts/check_subtitle_quality.py path/to/subtitles.ass
python3 scripts/extract_youtube_description.py 01-source/video.info.json --out 01-source/video.description.original.md
python3 scripts/download_youtube_thumbnail.py "https://youtu.be/VIDEO_ID" --out-dir 01-source --format jpg
python3 scripts/prepare_youtube_transcript.py 01-source/video.en.vtt --json-out 02-transcripts/video.en.cues.json --srt-out 02-transcripts/video.en.cleaned.srt
python3 scripts/make_translation_batches.py 02-transcripts/video.en.cues.json --out-dir 03-translation/translation-batches --cache 03-translation/video.zh.cache.json --max-chars 6000
python3 scripts/apply_translation_cache.py 02-transcripts/video.en.cues.json 03-translation/video.zh.cache.json --srt-out 03-translation/video.zh.v1.srt
python3 scripts/repair_chinese_subtitles.py 03-translation/video.zh.v1.srt --out 03-translation/video.zh.v2.srt
python3 scripts/srt_to_ass.py 03-translation/video.zh.v2.srt --out 04-subtitle-ass/video.zh.v2.ass
python3 scripts/make_bilingual_ass.py --zh-srt 03-translation/video.zh.v2.srt --en-srt 02-transcripts/video.en.cleaned.srt --out 04-subtitle-ass/video.zh-en.v1.ass
python3 scripts/check_subtitle_style.py 04-subtitle-ass/video.zh-en.v1.ass --style-profile bilingual-default --require-version-comment
python3 scripts/check_bilingual_alignment.py --zh-srt 03-translation/video.zh.v2.srt --en-srt 02-transcripts/video.en.cleaned.srt --report 06-review/bilingual-alignment.md
python3 scripts/check_ffmpeg_subtitle_support.py
python3 scripts/burn_subtitles_pil.py path/to/source.mp4 path/to/subtitles.ass --out 05-output/output.zh-burned.vN.mp4
python3 scripts/inspect_video.py path/to/output.mp4
python3 scripts/make_preview_clip.py path/to/source.mp4 path/to/subtitles.ass --out 06-review/preview.v1.mp4
python3 scripts/extract_source_subtitle_frames.py path/to/source.mp4 --out-dir 06-review/source-subtitle-check
python3 scripts/extract_design_frames.py 06-review/preview.v1.mp4 path/to/subtitles.ass --out-dir 06-review/design-confirmation-v1
python3 scripts/extract_review_frames.py path/to/output.mp4 --out-dir 06-review/screenshots-vN
python3 scripts/make_cover_preview.py 07-cover/video.cover.zh.v1.png --out 07-cover/video.cover.zh.v1.preview-320.jpg
python3 scripts/record_feedback.py --issue "字幕太小，看不清" --category size --fix "Add style screenshot approval before full burn" --reusable yes
```

`extract_youtube_description.py` extracts YouTube metadata and the original description, and reports whether translation is needed. `download_youtube_thumbnail.py` downloads and converts the YouTube thumbnail for retention or cover preparation. `prepare_youtube_transcript.py` turns YouTube rolling VTT into stable cue JSON/SRT. `make_translation_batches.py` creates numbered batches for the current agent model to translate; `make_codex_translation_batches.py` remains as a compatibility alias for older workflows. `apply_translation_cache.py` writes checked translations back to SRT. `repair_chinese_subtitles.py` merges dangling endings, removes empty cues, and repairs simple overlaps. `srt_to_ass.py` creates styled Chinese-only ASS with semantic line wrapping and the fixed `zh-only-default` style unless a raised profile is chosen. `make_bilingual_ass.py` combines reviewed Chinese SRT and cleaned English SRT into bilingual ASS with Chinese above English and the fixed `bilingual-default` style. `check_subtitle_style.py` verifies that ASS files match the selected fixed style profile. `check_bilingual_alignment.py` checks Chinese/English timing overlap and writes representative samples for meaning-and-voice review. `check_subtitle_quality.py` catches overlap, empty cues, short flashes, dangling endings, bad line breaks, and bilingual layout violations. `check_ffmpeg_subtitle_support.py` verifies whether ffmpeg can burn subtitles. `make_preview_clip.py` creates a subtitled preview before full burn using the same fixed style profile. `extract_source_subtitle_frames.py` extracts source frames to check whether the original video already has burned-in subtitles. `extract_design_frames.py` extracts design confirmation frames from the subtitled preview. `inspect_video.py` verifies MP4 duration, resolution, and audio/video streams. `extract_review_frames.py` creates screenshots for visual checks. `make_cover_preview.py` creates a 320px cover preview for thumbnail-size readability checks. `record_feedback.py` appends reusable subtitle feedback to the ledger and can update the shared gates/workflow.

If `check_ffmpeg_subtitle_support.py` reports that no checked ffmpeg can burn subtitles with native filters, use `burn_subtitles_pil.py` for the full MP4 instead of creating a one-off renderer inside the project workspace.

## Cover Processing Mode

Use this mode when the user asks to prepare, localize, or enhance the YouTube thumbnail/cover for the Chinese-subtitled version.

- Keep the original thumbnail unchanged in `01-source/`.
- Create edited covers in `07-cover/` with versioned names such as `<video-id>.cover.zh.v1.png`.
- Record one cover mode before editing:
  - `preserve-original-text`: default; keep all original cover text and add only `中文字幕` plus author/source.
  - `translate-original-text`: use only when the user explicitly asks to translate the existing cover copy.
  - `localized-rewrite`: use only when the user asks for a Chinese-platform cover or a literal translation is visibly weak.
- Default cover treatment for a Chinese-subtitled video is `preserve-original-text`: keep all original cover text exactly as-is; do not translate, rewrite, erase, or replace the original thumbnail wording.
- Add `中文字幕` in a visually suitable empty area.
- Add YouTube author/source information such as `作者：<channel>` or `<channel> · @handle` in a compact YouTube-style label.
- Use a consistent label treatment: `中文字幕` as the prominent label, author/source as the smaller secondary label, both with strong contrast and outline or solid label background.
- Preserve the original thumbnail composition, face, product signal, logo, and main title unless the user explicitly asks for a redesign.
- Do not cover faces, important UI, product marks, or the original title. Text must be readable at thumbnail size with strong contrast and outline.
- Use image editing/generation capability for the cover edit, then copy the generated image into `07-cover/` while leaving the generator's original output in place.
- Create a 320px preview such as `<video-id>.cover.zh.v1.preview-320.jpg`, then verify the label, title, face/product/logo preservation, and author/source readability at thumbnail size before delivery.

## Feedback Iteration

When the user points out a subtitle problem:

1. Locate the exact timestamp, subtitle block, screenshot, or output version.
2. Classify the issue as translation, segmentation, timing, hold duration, size, occlusion, terminology, or readability.
3. Fix the current video/subtitle output and re-run the relevant checks.
4. Record the feedback in `references/feedback-ledger.md`.
5. If the issue can recur on future videos, update `references/quality-gates.md` and `references/workflow.md` so future runs prevent it.
6. Re-package the skill after modifying skill files.

## Output Record

For every video, keep these outputs in the working project:

- source metadata and original subtitles
- original YouTube description, and Chinese translated description when the original is not Chinese
- original video thumbnail, and edited thumbnail/cover if requested
- cleaned English subtitle
- translated Chinese SRT for reuse
- styled Chinese-only or bilingual ASS used for burn-in
- hard-subtitled MP4
- design confirmation frames from the subtitled preview
- review screenshots
- review record using `references/review-template.md`
