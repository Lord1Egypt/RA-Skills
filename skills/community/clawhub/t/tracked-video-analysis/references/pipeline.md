# Tracked Video Analysis Pipeline

## Goal

Turn a video into a structured, human-readable summary while keeping progress visible and truthful.

## Working directory

Use:

`tmp/video_analysis/`

Recommended files:

- `video.mp4` — source video
- `status.json` — extraction status
- `progress.log` — extraction progress log
- `transcript.jsonl` — transcript by chunks
- `analysis.md` — extraction draft
- `final_status.json` — structuring status
- `final_progress.log` — structuring log
- `final_analysis.md` — final structured result

---

## Stage 1 — Extraction

### Purpose
Extract transcript content from the video into chunked text.

### Recommended approach

- Use chunking (`15s` or `30s`) instead of one-shot ASR on the whole file.
- Start with a lighter model for stability.
- Write status after every successful chunk.
- Preserve partial outputs aggressively.

### Minimum status shape

```json
{
  "stage": "transcribing",
  "percent": 34,
  "message": "Current chunk summary",
  "durationSeconds": 1851,
  "totalChunks": 124,
  "completedChunks": 45,
  "currentRange": "660-675s",
  "updatedAt": "2026-03-14T18:00:15Z"
}
```

### Extraction failure policy

If the process is killed:

1. inspect existing `transcript.jsonl`
2. inspect `status.json`
3. resume or restart deliberately
4. report exactly what survived

Do not say extraction is still running if only partial files remain.

---

## Stage 2 — Final structuring

### Purpose
Convert noisy transcript chunks into a useful summary.

### Typical transformations

- remove repeated filler
- remove obvious garbage lines
- group chunks by topic
- infer categories
- normalize names of functions/features
- produce the target format requested by the user

### Minimum status shape

```json
{
  "stage": "grouping",
  "percent": 75,
  "message": "Building structured summary",
  "updatedAt": "2026-03-14T19:12:00Z"
}
```

### Final-stage failure policy

If extraction is complete but structuring is not running:

- say that explicitly
- do not imply a live background process exists
- restart final structuring as a separate tracked stage if needed

---

## Media access fallbacks

### If chat media is inaccessible

Ask for one of:

- direct link
- document upload
- external file host

### If direct browser automation is unavailable

Prefer HTTP download and local processing.

### If root install is blocked

Use workspace-local npm tools.

---

## Recommended deliverables

### Format A
Category → function → description → benefit

### Format B
Category → function → short description

### Format C
Function → timestamp → notes

### Format D
Polished Markdown mini-document for file delivery

---

## Productization value

This workflow is worth packaging because it solves recurring operational problems:

1. chat media access failures
2. local tool setup without root
3. unstable long-running transcription jobs
4. false progress claims during background work
5. conversion of noisy ASR into a usable human summary
