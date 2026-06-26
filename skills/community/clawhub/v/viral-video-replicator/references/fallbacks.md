# Fallbacks — viral-video-replicator

> **Role:** Defines recovery procedures for every failure case in the video analysis pipeline.
> Load at: On any error during Steps 2-8. Each case has trigger condition, recovery steps, and user message.
> It does NOT replace execution — these are error recovery paths, not alternative data sources.

## Case 0: FFmpeg Not Installed

**Trigger:** `ffmpeg -version` returns `command not found`.

```
Recovery:
1. Output install command for detected OS:
   macOS: brew install ffmpeg
   Linux: apt install ffmpeg
   Windows: choco install ffmpeg
2. Ask user to run install and retry.
3. If still fails -> STOP. Tell user: "FFmpeg is required. Please install manually."
4. Do NOT proceed without FFmpeg. Do NOT fabricate frame analysis.
```

## Case 1: No API Key

**Trigger:** ARK_API_KEY is empty, missing, or returns 401/403.

```
Recovery:
1. STOP immediately.
2. Guide user: "请在火山方舟控制台获取 API Key: https://console.volcengine.com/ark"
3. Do NOT proceed. Do NOT substitute with training data.
```

## Case 2: Vision LLM Fails (Exact Mode)

**Trigger:** Vision API returns 4xx/5xx or invalid JSON in exact mode.

```
Recovery:
1. Retry once with same grids and prompt.
2. If still fails -> auto-downgrade to REWRITE mode (flat analysis).
   Warn: "Exact analysis failed. Using simplified analysis mode — results will be less precise."
3. If rewrite also fails -> return raw materials:
   - Frame grid images (base64)
   - Transcript (if available)
   Warn: "Automated analysis failed. Returning raw frame grids and transcript for manual analysis."
4. Never fabricate analysis data.
```

## Case 3: ASR Transcription Fails

**Trigger:** ASR returns error status, times out (>120s), or network error after 3 retries.

```
Recovery:
1. Skip transcript entirely.
2. Proceed with visual-only analysis.
3. Mark output: "Audio transcription unavailable. Generated prompt contains visual descriptions only — dialogue content is missing."
4. In the Vision LLM prompt, use the "no transcript" variant (see vision-analysis.md).
```

## Case 4: TOS Upload Fails

**Trigger:** TOS SDK throws exception after 2 retries, or credentials invalid.

```
Recovery:
1. TOS failure = ASR failure (audio cannot be transferred).
2. Apply Case 3 recovery (skip ASR, visual-only).
3. Additional warn: "Cloud storage upload failed — speech transcription skipped."
```

## Case 5: Video Too Large

**Trigger:** Video file exceeds 200MB.

```
Recovery:
1. Reject immediately (do NOT attempt processing).
2. Tell user: "Video exceeds 200MB limit. Please compress (e.g., ffmpeg -i input.mp4 -crf 28 output.mp4) or trim to under 200MB."
```

## Case 6: No Audio Track

**Trigger:** extract_audio() returns None or <5000 bytes.

```
Recovery:
1. This is NORMAL, not an error. Many fashion videos are music-only or silent.
2. Skip ASR pipeline entirely.
3. Proceed with visual-only analysis.
4. Note in output: "No speech detected in video. Analysis is visual-only."
```

## Case 7: Frame Extraction Fails

**Trigger:** FFmpeg returns non-zero exit code during frame extraction.

```
Recovery:
1. Check video format — try re-encoding first:
   ffmpeg -i input.mp4 -c:v libx264 -crf 23 re-encoded.mp4
2. Retry frame extraction on re-encoded video.
3. If still fails -> report error with FFmpeg stderr output for debugging.
4. Do NOT proceed without frames — they are required for Vision analysis.
```

## Case 8: Prompt Assembly Fails

**Trigger:** Exception during build_reverse_prompt() or mode determination.

```
Recovery:
1. Return the analysis JSON + transcript as standalone outputs.
2. Warn: "Prompt assembly failed. Returning raw analysis — you can manually compose the Seedance prompt from these results."
3. Include the 4-mode prompt templates from reverse-prompt.md as a reference for manual composition.
```

## Universal Fallback Principle

Every error path must end with ONE of:
- A clear error message explaining what failed and how to fix it
- A degraded output with explicit warning about what is missing
- A STOP with install/setup guidance

**NEVER:** silently swallow errors, fabricate data, or deliver empty results without explanation.
