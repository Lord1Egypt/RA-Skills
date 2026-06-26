# Workflow

## Goal

Convert long-form content into reusable text and insight artifacts with the least fragile path available.

## Acquisition Order

1. Pasted text
   - Use directly.

2. Existing transcript files
   - Prefer `txt`, `srt`, then `json`.
   - Skip ASR unless the transcript is obviously incomplete.

3. Readable web content
   - Extract article text directly.

4. Caption-bearing media
   - Prefer platform captions or subtitle endpoints over ASR.

5. Media-only source
   - Acquire media.
   - Extract audio if needed.
   - Run local whisper transcription.

## URL Handling Strategy

For remote URLs:

1. Open the page normally.
2. Inspect rendered text.
3. Inspect network requests for detail APIs, captions, or media URLs.
4. Inspect page scripts when needed.
5. Fall back to media extraction and ASR.

Do not assume any single social platform path is durable.

## Output Policy

Default deliverables:

- `raw`
- `cleaned`
- `rough_speakers`
- `insight`

Default response behavior:

- Put the main summary and analysis directly in the assistant response.
- Use files for transcript artifacts, long supporting materials, or explicitly requested exports.
- Do not answer with only a pointer such as "see insight_memo.md" when the user asked for a summary.

Completion rule for multi-speaker media:

- A job on interviews, podcasts, panels, or other multi-speaker conversational media is not complete if it returns only an insight memo.
- The minimum bar is: cleaned transcript, rough speaker transcript, and then the insight memo, unless the user explicitly asked for summary-only output.

Recommended default destination:

- Write durable artifacts into `output/summarize-anything/<job-id>/` in the current workspace unless the user requested another path.
- Keep temporary conversions, caches, and scratch files inside `runtime/`.
- Treat `runtime/work/` and `runtime/cache/` as disposable.
- Keep `runtime/bin/` and the default whisper model as stable local assets unless the user wants a full cleanup.
- Expect routine maintenance to clear `runtime/work/` and `runtime/cache/` automatically when the runtime crosses configured size thresholds.

If the user asks for only one deliverable, prioritize it but keep intermediate artifacts if they materially help the workflow.
