# Video Transcription Basics

The **Video Transcription** task converts video into readable transcriptions with timestamps and speaker identification.

## Usage
`wayinvideo submit transcribe --url "<url_or_id>" [options]`

*Note: For no-install method, use `PYTHONPATH=<ABS_PATH_TO_SKILL>/wayinvideo-cli python3 -m wayinvideo submit ...`.*

## Options
- `--url <url_or_id>`: (Required) Video URL or identity token.
- `--target <lang>`: Target language code. See `references/supported_languages.md`. Auto-detected if omitted.
    - **Pro Tip**: Always specify `target_lang` during submission for higher quality results.
- `--save-dir <path>`: Directory for the result JSON file. Defaults to `~/.wayinvideo/cache` (or the value in your config). Do not specify unless requested.
