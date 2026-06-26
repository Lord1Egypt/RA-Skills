# Large Model Audio/Video Understanding Parameters & Examples — `mps_av_understand.py`

**Function**: Large model audio/video content understanding, supporting video visual understanding, speech recognition, comparative analysis, etc.
> **Core Mechanism**: Controlled via `AI Analysis Task.Definition=33` + `Extended Parameter(mvc.mode + mvc.prompt)`.
> `--mode` and `--prompt` are the two most important parameters — **it is strongly recommended to explicitly specify them on every call**.

## Parameter Description

| Parameter | Description |
|------|------|
| `--local-file` | Local file path; automatically uploaded to COS before processing (mutually exclusive with `--cos-input-*`) |
| `--url` | Audio/video URL (HTTP/HTTPS), mutually exclusive with `--task-id` |
| `--cos-input-key` | COS input file Key (e.g., `/input/video.mp4`, recommended) |
| `--cos-input-bucket` | COS Bucket name for the input file (defaults to environment variable) |
| `--cos-input-region` | COS Region for the input file (e.g., `ap-guangzhou`) |
| `--task-id` | Directly query an existing task result, skipping task creation |
| `--mode` | **Required**. Understanding mode: `video` (understand video visual content, default) / `audio` (process audio only; audio is automatically extracted from video) |
| `--prompt` | **Required**. Large model prompt that determines the focus and output format of the understanding (e.g., "Please perform speech recognition on the video") |
| `--extend-url` | When comparing two audio/video clips, the URL of the second clip for comparison (up to 1) |
| `--definition` | AI Analysis Task template ID (default `33`, i.e., the preset video understanding template) |
| `--no-wait` | Async mode: submit the task only, do not wait for results |
| `--json` | Output results in JSON format |
| `--output-dir` | Save the result JSON to the specified directory |
| `--verbose` / `-v` | Display detailed log information |
| `--region` | Processing region (reads `TENCENTCLOUD_API_REGION` environment variable first, defaults to `ap-guangzhou`) |
| `--dry-run` | Print parameter preview only, do not call the API |

## Mandatory Rules

- `--mode` and `--prompt` are **required** and must not be omitted:
  - `--mode video`: Understand video visual content
  - `--mode audio`: Process audio only (audio is automatically extracted from video)
  - `--prompt`: Controls the focus of the large model's understanding; results may be empty if omitted

## Example Commands

```bash
# Understand video content (--mode video + prompt)
python scripts/mps_av_understand.py \
    --url https://example.com/video.mp4 \
    --mode video \
    --prompt "Analyze the main content, scenes, and key information of this video"

# Audio mode: speech recognition (audio is automatically extracted from video)
python scripts/mps_av_understand.py \
    --url https://example.com/video.mp4 \
    --mode audio \
    --prompt "Perform speech recognition on this audio and output the complete text"

# Pure audio file
python scripts/mps_av_understand.py \
    --url https://example.com/audio.mp3 \
    --mode audio \
    --prompt "Recognize the content of this audio and output the text"

# Comparative analysis (two audio/video clips)
python scripts/mps_av_understand.py \
    --url https://example.com/standard.mp4 \
    --extend-url https://example.com/user.mp4 \
    --mode audio \
    --prompt "Compare these two audio clips, analyze the differences, and provide a professional evaluation"

# COS object input
python scripts/mps_av_understand.py \
    --cos-input-key /input/my-video.mp4 \
    --mode video \
    --prompt "Summarize the core content of the video"

# Async mode: submit task only
python scripts/mps_av_understand.py \
    --url https://example.com/video.mp4 \
    --mode video --prompt "Analyze video content" --no-wait

# Query an existing task result
python scripts/mps_av_understand.py --task-id 2600011633-WorkflowTask-80108cc3380155d98b2e3573a48a

# Save results to a local directory
python scripts/mps_av_understand.py \
    --url https://example.com/video.mp4 \
    --mode video --prompt "Analyze content" --output-dir /output/
```