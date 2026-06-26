# Smart Subtitle Parameters & Examples — `mps_subtitle.py`

**Features**: Subtitle extraction, translation, speech recognition (ASR), OCR hard subtitle recognition, supporting 30+ language translations.

## Parameter Description

| Parameter | Description |
|------|------|
| `--local-file` | Local file path, automatically uploaded to COS for processing (mutually exclusive with `--cos-input-*`) |
| `--url` | Video URL address |
| `--cos-input-bucket` | Input COS Bucket name (used with `--cos-input-region`/`--cos-input-key`, recommended) |
| `--cos-input-region` | Input COS Bucket region (e.g., `ap-guangzhou`) |
| `--cos-input-key` | Input COS object Key (e.g., `/input/video.mp4`, **recommended**) |
| `--process-type` | Processing type: `asr` (speech recognition, default) / `ocr` (on-screen text recognition) / `translate` (translation) |
| `--src-lang` | Video source language. **ASR mode**: `zh`, `en`, `ja`, `ko`, `zh-PY`, `yue`, `zh_dialect`, `prime_zh`, `vi`, `ms`, `id`, `th`, `fr`, `de`, `es`, `pt`, `ru`, `ar`, etc.; **OCR mode**: `zh_en` (Chinese-English, default), `multi` (multilingual) |
| `--subtitle-type` | Subtitle type: `0` = source language, `1` = translated language, `2` = bilingual (default when translation is enabled) |
| `--subtitle-format` | Subtitle format: `vtt` / `srt` / `original` |
| `--translate` | Translation target language, supports multiple languages separated by `/`, e.g., `en/ja`. Supports 30+ languages: `zh`, `en`, `ja`, `ko`, `fr`, `es`, `de`, `it`, `ru`, `pt`, `ar`, `th`, `vi`, `id`, `ms`, `tr`, `nl`, `pl`, `sv`, etc. |
| `--hotwords-id` | ASR hotwords library ID, improves recognition accuracy for specialized terms, e.g., `hwd-xxxxx` |
| `--ocr-area` | OCR recognition area (percentage coordinates 0-1), format `x1,y1,x2,y2`, can be specified multiple times |
| `--sample-width` | Width of sample video/image (pixels), used with `--ocr-area` |
| `--sample-height` | Height of sample video/image (pixels), used with `--ocr-area` |
| `--template` | Smart subtitle preset template ID (e.g., `110167`) |
| `--user-ext-para` | User-defined extension parameters (JSON string, advanced option) |
| `--ext-info` | Extension information (JSON string, advanced option) |
| `--output-bucket` | Output COS Bucket name (defaults to `TENCENTCLOUD_COS_BUCKET` environment variable) |
| `--output-region` | Output COS Bucket region (defaults to `TENCENTCLOUD_COS_REGION` environment variable) |
| `--output-dir` | Output directory, default `/output/subtitle/` |
| `--output-object-path` | Output subtitle file path, e.g., `/output/{inputName}_subtitle.{format}` |
| `--no-wait` | Submit task only, do not wait for results (default is automatic polling) |
| `--poll-interval` | Polling interval (seconds), default 10 |
| `--max-wait` | Maximum wait time (seconds), default 1800 (30 minutes) |
| `--download-dir` | Download output files to specified local directory after task completion (default is to print pre-signed URL only) |
| `--verbose` / `-v` | Output detailed information |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` environment variable first, default `ap-guangzhou`) |
| `--notify-url` | Task completion callback URL (optional) |
| `--dry-run` | Print parameters only, do not call API |

## Mandatory Rules

- **`--process-type` selection rules**:
  - User says "speech recognition", "recognize spoken content", "convert to text", "ASR" → use `--process-type asr` (default, can be omitted)
  - User says "OCR", "recognize on-screen text", "hard subtitle recognition", "extract text from video frames" → use `--process-type ocr`, and set `--src-lang` based on language (`zh_en` for Chinese-English, `multi` for multilingual)
  - User says "translate", "subtitle translation", "translate to XX language" → use `--process-type translate` (or add `--translate <target language>` on top of `asr`/`ocr`)
- **`--src-lang` rules**: Defaults to `zh_en` in OCR mode; defaults to `zh` in ASR mode if user does not specify a language
- **`--translate` rules**: The translation parameter is `--translate <lang>` (e.g., `--translate zh`, `--translate en/ja`). There is NO `--trans-lang`, `--target-lang`, or `--source-lang` parameter. Supports multiple target languages separated by `/`; subtitle type defaults to bilingual (`--subtitle-type 2`) when translation is enabled

## Example Commands

```bash
# ASR subtitle recognition (default)
python scripts/mps_subtitle.py --url https://example.com/video.mp4

# ASR + translate to English (bilingual subtitles)
python scripts/mps_subtitle.py --url https://example.com/video.mp4 --src-lang zh --translate en

# OCR hard subtitle recognition + translation
python scripts/mps_subtitle.py --url https://example.com/video.mp4 --process-type ocr --src-lang zh_en --translate en

# Multi-language translation (English + Japanese)
python scripts/mps_subtitle.py --url https://example.com/video.mp4 --src-lang zh --translate en/ja

# COS path input (recommended)
python scripts/mps_subtitle.py --cos-input-bucket mybucket-125xxx --cos-input-region ap-guangzhou \
    --cos-input-key /input/video.mp4 --src-lang zh --translate en

# Submit asynchronously then query task status
python scripts/mps_subtitle.py --url https://example.com/video.mp4 --no-wait
python scripts/mps_get_video_task.py --task-id 1250017490-20260318152230-abcdef123456
```