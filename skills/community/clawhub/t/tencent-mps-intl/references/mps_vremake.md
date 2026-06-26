# Video Remix Parameters & Examples — `mps_vremake.py`

**Features**: Video Remix (Video Remake), supporting face swap, person swap, video interleaving (AB), and other creative modes.
> **Core Mechanism**: `AI Analysis Task.Definition=29` + `Extended Parameter(vremake.mode + mode parameters)`.
> The script **automatically polls and waits for completion by default**; add `--no-wait` to submit only without waiting.
> Official Documentation: https://cloud.tencent.com/document/product/862/124394

> ⚠️ **Video Deduplication** (picture-in-picture/video expansion/vertical fill/horizontal fill) should use [`mps_dedupe.py`](mps_dedupe.md) — do not use this script.

## Supported Modes

| Mode | Description |
|------|------|
| `AB` | Video Interleaving: AB video interleaving mode |
| `SwapFace` | Face Swap: Replace faces in video |
| `SwapCharacter` | Person Swap: Replace characters in video |

## Parameter Reference

| Parameter | Description |
|------|------|
| `--local-file` | Local file path; automatically uploaded to COS before processing (mutually exclusive with `--cos-input-*`) |
| `--url` | Video URL (HTTP/HTTPS) |
| `--cos-input-key` | COS input file Key (e.g., `/input/video.mp4`, recommended) |
| `--cos-input-bucket` | COS Bucket name for the input file (defaults to environment variable) |
| `--cos-input-region` | COS Region for the input file (e.g., `ap-guangzhou`) |
| `--mode` | **Required**. Remix mode (see table above) |
| `--output-bucket` | Output COS Bucket name (defaults to `TENCENTCLOUD_COS_BUCKET` environment variable) |
| `--output-region` | Output COS Bucket region (defaults to `TENCENTCLOUD_COS_REGION` environment variable) |
| `--output-cos-dir` | COS output directory (default `/output/vremake/`), must start and end with `/` |
| `--no-wait` | Async mode: submit the task only, return TaskId, do not wait for results |
| `--src-faces` | [SwapFace] List of face URLs from the source video (one-to-one mapping with `--dst-faces`, max 6) |
| `--dst-faces` | [SwapFace] List of target face URLs |
| `--src-character` | [SwapCharacter] Source character URL (front-facing full-body photo) |
| `--dst-character` | [SwapCharacter] Target character URL (front-facing full-body photo) |
| `--llm-prompt` | [AB] LLM prompt |
| `--llm-video-prompt` | [AB] LLM prompt (for generating background **video**, takes priority over `--llm-prompt`) |
| `--random-cut` | [AB] Random cropping |
| `--random-speed` | [AB] Random speed-up |
| `--random-flip` | [AB] Random mirroring (`true`/`false`, default `true`) |
| `--ext-mode` | [AB] Extension mode `1`/`2`/`3` |
| `--custom-json` | Custom vremake extended parameter JSON (auto-merged with `--mode`) |
| `--json` | JSON format output |
| `--output-dir` | Save result JSON to the specified directory |
| `--download-dir` | Download output video to the specified local directory after task completion (by default, only prints pre-signed URL) |
| `--definition` | AI Analysis Task template ID (default `29`) |
| `--region` | Processing region (reads `TENCENTCLOUD_API_REGION` environment variable first, default `ap-guangzhou`) |
| `--dry-run` | Print parameter preview only, do not call the API |

**SwapFace Limitations**: Video resolution ≤ 4K; single image < 10MB (jpg/png); total number of faces ≤ 6.
**SwapCharacter Limitations**: Video duration ≤ 20 minutes; front-facing full-body photo required.

## Mandatory Rules

- `--mode` is **required** and must be one of the preset enum values: `AB` | `SwapFace` | `SwapCharacter`
  - User says "face swap" or "replace face" → use `--mode SwapFace`, and provide `--src-faces` and `--dst-faces` (one-to-one mapping)
  - User says "person swap" or "replace character" → use `--mode SwapCharacter`, and provide `--src-character` and `--dst-character` (front-facing full-body photos)
  - User says "video interleaving" or "AB mashup" → use `--mode AB`
  - **If the user does not specify a mode, you must ask** — do not guess
- **Video Deduplication** (picture-in-picture/video expansion/vertical fill/horizontal fill) must use `mps_dedupe.py` — **using this script is prohibited**
- `SwapFace` limitations: video resolution ≤ 4K; single face image < 10MB (jpg/png); total number of faces ≤ 6
- `SwapCharacter` limitations: video duration ≤ 20 minutes; character photo must be a front-facing full-body photo

## Example Commands

```bash
# ===== Face Swap =====

# Face swap mode (--src-faces and --dst-faces in one-to-one mapping, automatically waits for completion)
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode SwapFace \
    --src-faces https://example.com/src1.png https://example.com/src2.png \
    --dst-faces https://example.com/dst1.jpg https://example.com/dst2.jpg

# ===== Person Swap =====

# Person swap mode (front-facing full-body photos)
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode SwapCharacter \
    --src-character https://example.com/src_fullbody.png \
    --dst-character https://example.com/dst_fullbody.png

# ===== Video Interleaving (AB) =====

python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode AB

# ===== General =====

# Async submission (add --no-wait to submit only without waiting)
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode SwapFace \
    --src-faces https://example.com/src.png \
    --dst-faces https://example.com/dst.png \
    --no-wait

# Query existing task results
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx

# dry-run preview
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode SwapFace \
    --src-faces https://example.com/src.png \
    --dst-faces https://example.com/dst.png \
    --dry-run
```